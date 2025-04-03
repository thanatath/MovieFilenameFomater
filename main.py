import os
import requests

# Configuration
API_URL = "https://api.opentyphoon.ai/v1/chat/completions"
API_KEY = ""  # Replace with your actual API key
DIRECTORY = ""  # Replace with the directory containing your media files
ALLOWED_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"}  # Video file types

system_prompt = """You are a movie renaming assistant that formats filenames into a Plex-friendly format. Given a filename, you must rename it into a structured format while removing unnecessary details.

## Rules:
1. **Format the name as:**
   - `<Movie/Show Name> SXXEYY` (for TV shows)
   - `<Movie Name (Year)>` (for movies, if the year is available)
2. **Remove unnecessary data**, such as:
   - Resolution (e.g., 1080p, 4K, 720p)
   - Encoding formats (e.g., H.264, x264, WEB-DL, DDP5.1)
   - Release group names (e.g., YIFY, NTb, MESSI@BearBIT)
   - Special characters and dots (replace dots with spaces, except for SXXEYY notation)
   - Extra episode titles (only keep `<Show Name> SXXEYY`)
3. **Keep important parts** of the title, including:
   - Season and episode numbers (if it's a TV show)
   - Show/movie names (even if in another language)
   - Year (if available for movies)
4. **Standardize season/episode notation** as `SXXEYY`.
5. **Ignore file extensions** like `.mp4`, `.mkv`, `.avi`.

## Examples:

| Input Filename | Output Filename |
|---------------|----------------|
| EP.01 ดอกเตอร์สโตน ซีซัน 2 | S02E01 ดอกเตอร์สโตน |
| High.Potential.S01E01.Pilot.1080p.HS.WEB-DL.DDP5.1.H.264-MESSI@BearBIT | High Potential S01E01 |
| Breaking.Bad.S03E05.720p.BluRay.x264-REWARD | Breaking Bad S03E05 |
| Spider-Man.No.Way.Home.2021.1080p.BluRay.x264-YTS | Spider-Man No Way Home (2021) |
| The.Dark.Knight.2008.2160p.UHD.BluRay.HDR.x265 | The Dark Knight (2008) |
| Game.of.Thrones.S08E03.The.Long.Night.1080p.AMZN.WEB-DL.DDP5.1.H.264-GoT | Game of Thrones S08E03 |
| Money.Heist.La.Casa.de.Papel.S04E02.720p.NF.WEB-DL.DDP5.1.x264-NTb | Money Heist La Casa de Papel S04E02 |
| Stranger.Things.S02E06.1080p.NF.WEB-DL.DDP5.1.x264-STR | Stranger Things S02E06 |
| Inception.2010.720p.BluRay.x264.YIFY | Inception (2010) |
| Avatar.The.Way.of.Water.2022.1080p.WEBRip.DD5.1.x264-NOGRP | Avatar The Way of Water (2022) |
| The.Boys.S03E01.Payback.4K.WEB-DL.DDP5.1.Atmos.H.264-MZABI | The Boys S03E01 |
| Attack.on.Titan.Final.Season.Part.2.EP.03.1080p.WEB-DL.x265 | Attack on Titan Final Season Part 2 S04E03 |

Your task is to rename the given filename according to these rules and return **only the renamed filename as plain text**, without any extra formatting or explanations.
"""

def get_new_filename(filename):
    """Send filename to OpenTyphoon API and get the renamed result."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "typhoon-v2-70b-instruct",  # You can change to another available model
        "messages": [
            {
                "role": "system", "content": system_prompt
            },
            {
                "role": "user",
                "content": f"{filename}"
            }
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting API: {e}")
        return None


def rename_files_in_directory(directory):
    """Scan and rename files in the given directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip directories and non-video files
        if not os.path.isfile(file_path) or not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            continue

        new_name = get_new_filename(filename)
        if new_name:
            new_file_path = os.path.join(directory, new_name + os.path.splitext(filename)[1])
            try:
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_name}{os.path.splitext(filename)[1]}")
            except Exception as e:
                print(f"Error renaming {filename}: {e}")


if __name__ == "__main__":
    rename_files_in_directory(DIRECTORY)
