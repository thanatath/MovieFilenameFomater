import os
import sys
from config import ALLOWED_EXTENSIONS
from llm_provider import get_llm_provider

# Initialize provider
provider = get_llm_provider()

def get_new_filename(filename):
    """Get a cleaned filename using the selected LLM provider."""
    return provider.get_response(filename)

def rename_files_in_directory(directory):
    # Verify directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    actions = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if not os.path.isfile(file_path) or not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            continue
        # Separate base name and extension to prevent duplicate ext
        base_name, ext = os.path.splitext(filename)
        print(f"Processing: {filename}")
        # Send only the name without extension to LLM
        new_name = get_new_filename(base_name)
        if new_name:
            new_path = os.path.join(directory, new_name + ext)
            actions.append((file_path, new_path))
        else:
            print(f"❌ Failed to get new name for {filename}")

    if not actions:
        print("No files to rename.")
        return

    print("\nProposed renames:")
    for old, new in actions:
        print(f"{os.path.basename(old)} -> {os.path.basename(new)}")
    choice = input("\nApply these changes? [y/N]: ").strip().lower()
    if choice not in ("y", "yes"):
        print("Aborted.")
        return

    for old, new in actions:
        try:
            os.rename(old, new)
            print(f"✅ Renamed: {os.path.basename(old)} -> {os.path.basename(new)}")
        except Exception as e:
            print(f"❌ Error renaming {os.path.basename(old)}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No directory path provided.")
        print("Usage: python main.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    rename_files_in_directory(directory)