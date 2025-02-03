from pathlib import Path
import re

# Set your directory path
folder_path = Path("/home/gifted-24/download/Naruto Shippuden")

# Regex patterns for extracting episode numbers
patterns = [
    re.compile(r'EP\.(\d+)'),  # Matches "EP.77"
    re.compile(r'episode-(\d+)'), # Matches "naruto-shippuden-episode-2"
    re.compile(r'Naruto Shippuden - (\d+)')
]

def extract_episode_number(filename):
    """Extract episode number from different naming formats."""
    for pattern in patterns:
        match = pattern.search(filename.stem)
        if match:
            return int(match.group(1))
    return None  # Return None if no episode number is found

# Get all video files in the folder
files = [f for f in folder_path.iterdir() if f.suffix in {".mp4", ".mkv"}]

# Extract episode numbers and sort
sorted_files = sorted(files, key=lambda f: extract_episode_number(f) or 0)

# Rename files in order
for index, file in enumerate(sorted_files, start=1):
    episode_number = extract_episode_number(file)
    if episode_number is None:
        print(f"Skipping: {file.name} (No episode number found)")
        continue

    new_name = f"Naruto Shippuden - Episode {episode_number:03d}{file.suffix}"
    new_path = folder_path / new_name

    file.rename(new_path)
    print(f"Renamed: {file.name} → {new_name}")

print("Renaming Complete!")
