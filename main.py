import os
import sys
import requests
from ollama import chat
from ollama import ChatResponse
from ollama import Client
from dotenv import load_dotenv

load_dotenv()

# === Configuration ===
USE_OLLAMA = os.getenv("USE_OLLAMA", "True").lower() in ("true", "1", "yes")  # Toggle between Ollama (True) and OpenTyphoon (False)

ALLOWED_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"}

# === OpenTyphoon Config ===
OPENTYPHOON_API_URL = os.getenv("OPENTYPHOON_API_URL", "https://api.opentyphoon.ai/v1/chat/completions")
OPENTYPHOON_API_KEY = os.getenv("OPENTYPHOON_API_KEY")
OPENTYPHOON_MODEL = os.getenv("OPENTYPHOON_MODEL", "typhoon-v2-70b-instruct")

# === Ollama Config ===
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:12b")

client = Client(
    host=OLLAMA_API_URL
)

# === Shared Prompt ===
DEFAULT_SYSTEM_PROMPT = """
You are a movie renaming assistant that formats filenames into a Plex-friendly format. Given a filename, you must rename it into a structured format while removing unnecessary details.

Rules:
1. Format the name as:
   - <Movie/Show Name> SXXEYY (for TV shows)
   - <Movie Name (Year)> (for movies, if the year is available)
2. Remove unnecessary data, such as:
   - Resolution (e.g., 1080p, 4K)
   - Encoding formats (e.g., H.264, x264, WEB-DL, DDP5.1)
   - Release group names (e.g., MESSI@BearBIT)
   - Special characters that are not part of the title
3. Keep important parts of the title, including:
   - Season and episode numbers
   - Show/movie names (even if in another language)
   - Year (if available for movies)
4. Standardize season/episode notation as SXXEYY.
5. Ignore file extensions like .mp4, .mkv, .avi.

Special Rules:
1.if have Warning for name Task condition Rule from User, give it priority over default system prompt.

Examples:
EP.01 ดอกเตอร์สโตน ซีซัน 2 → S02E01 ดอกเตอร์สโตน  
High.Potential.S01E01.Pilot.1080p.HS.WEB-DL.DDP5.1.H.264-MESSI@BearBIT → High Potential S01E01  
The.Dark.Knight.2008.2160p.UHD.BluRay.HDR.x265 → The Dark Knight (2008)
"""
PROMPT_FILE = os.getenv("PROMPT_FILE", "prompt.txt")
file_prompt = ""
try:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        file_prompt = f.read().strip()
except FileNotFoundError:
    print(f"Warning: Prompt file '{PROMPT_FILE}' not found. Using default system prompt.")

if file_prompt:
    SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT
    print(f"Loaded additional prompt from '{PROMPT_FILE}', giving it priority over default prompt.")
else:
    SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT

def get_new_filename(filename):
    """Get a cleaned filename from either Ollama or OpenTyphoon."""
    if USE_OLLAMA:
        return get_filename_from_ollama(filename)
    else:
        return get_filename_from_opentyphoon(filename)

def get_filename_from_ollama(filename):
    response: ChatResponse = client.chat(model=OLLAMA_MODEL, messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content":  "Warning! rename movie name Rule: "+ file_prompt +"\n"+ filename }
    ])

    try:
        return response.message.content
    except requests.exceptions.RequestException as e:
        print(f"[Ollama] Error: {e}")
        return None

def get_filename_from_opentyphoon(filename):
    headers = {
        "Authorization": f"Bearer {OPENTYPHOON_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": OPENTYPHOON_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Warning! rename movie name Rule: "+ file_prompt +"\n"+ filename }
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(OPENTYPHOON_API_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"[OpenTyphoon] Error: {e}")
        return None

def rename_files_in_directory(directory):
    # Verify directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if not os.path.isfile(file_path) or not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            continue

        print(f"Processing: {filename}")
        new_name = get_new_filename(filename)
        if new_name:
            new_file_path = os.path.join(directory, new_name + os.path.splitext(filename)[1])
            try:
                os.rename(file_path, new_file_path)
                print(f"✅ Renamed: {filename} -> {new_name}{os.path.splitext(filename)[1]}")
            except Exception as e:
                print(f"❌ Error renaming {filename}: {e}")
        else:
            print(f"❌ Failed to get new name for {filename}")

if __name__ == "__main__":
    # Check if directory path is provided as command-line argument
    if len(sys.argv) < 2:
        print("Error: No directory path provided.")
        print("Usage: python main.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    rename_files_in_directory(directory)