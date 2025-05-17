# MovieFilenameFormatter

MovieFilenameFormatter is a Python script that automatically renames movie and TV show files into a **Plex-friendly format** using AI models (Ollama or OpenTyphoon).

<img src="./screenshot.png" alt="Screenshot">

## Features
- Automatic batch renaming with a single confirmation prompt
- Supports both Ollama and OpenTyphoon AI backends
- Configurable via a `.env` file and an optional `prompt.txt` override
- Removes unnecessary details (resolution, encoding, release groups)
- Standardizes naming (`SXXEYY` for TV, `Movie Name (Year)` for films)
- Supports `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`

## Prerequisites
- Python 3.7+
- `requests` and `python-dotenv` libraries

```powershell
pip install requests python-dotenv ollama
```

## Configuration
1. Create a `.env` file in the project root (see [.env.example](.env) for a template):
   ```properties
   USE_OLLAMA=True                     # True for Ollama, False for OpenTyphoon
   OPENTYPHOON_API_URL=...             # OpenTyphoon endpoint
   OPENTYPHOON_API_KEY=your_key_here   # Your OpenTyphoon API key
   OPENTYPHOON_MODEL=typhoon-v2-70b-instruct
   OLLAMA_API_URL=http://localhost:11434
   OLLAMA_MODEL=gemma3:12b
   PROMPT_FILE=prompt.txt              # Optional override prompt
   ```
2. (Optional) Create `prompt.txt` to supply custom instructions. If present and non-empty, its content takes priority over the default system prompt.

## Usage
Run the renaming script on a target directory:

```powershell
python main.py "C:\Path\To\Your\MediaFolder"
```

1. The script analyzes filenames and suggests a batch of new names.
2. You’ll see a summary of proposed renames.
3. Confirm once with `y` or `yes` to apply all changes.

## Examples
Before:
```
High.Potential.S01E01.Pilot.1080p.HS.WEB-DL.mkv
The.Dark.Knight.2008.x265.mp4
```
After:
```
High Potential S01E01.mkv
The Dark Knight (2008).mp4
```

## Contributing
Feel free to open issues or submit pull requests.

## License
MIT License

