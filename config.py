import os
from dotenv import load_dotenv

load_dotenv()

# === Configuration ===
USE_OLLAMA = os.getenv("USE_OLLAMA", "True").lower() in ("true", "1", "yes")
ALLOWED_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"}

# === OpenTyphoon Config ===
OPENTYPHOON_API_URL = os.getenv("OPENTYPHOON_API_URL", "https://api.opentyphoon.ai/v1/chat/completions")
OPENTYPHOON_API_KEY = os.getenv("OPENTYPHOON_API_KEY")
OPENTYPHOON_MODEL = os.getenv("OPENTYPHOON_MODEL", "typhoon-v2-70b-instruct")

# === Ollama Config ===
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:12b")

# === Prompt Configuration ===
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
1. If a user-defined rule is provided in a prompt file, that rule takes priority over the default system prompt.

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

# Use user-defined prompt if available, otherwise default
if file_prompt:
    SYSTEM_PROMPT = file_prompt
    print(f"Loaded additional prompt from '{PROMPT_FILE}', giving it priority over default prompt.")
else:
    SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT
