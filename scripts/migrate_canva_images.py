import os
import shutil
import re
from pathlib import Path

# Paths
PRACTICE_DIR = Path("practice")
THEORY_CANVA_DIR = PRACTICE_DIR / "data" / "theory" / "canva"
CONTENT_CANVA_DIR = PRACTICE_DIR / "data" / "content" / "canva"
ASSETS_IMAGES_DIR = CONTENT_CANVA_DIR / "assets" / "images"

def migrate_images():
    print("--- 1. Migrating Images ---")
    if not THEORY_CANVA_DIR.exists():
        print(f"Error: Source directory {THEORY_CANVA_DIR} does not exist.")
        return

    # Find all Week* directories
    for week_dir in THEORY_CANVA_DIR.glob("Week*"):
        if week_dir.is_dir():
            src_images_dir = week_dir / "images"
            if src_images_dir.exists():
                week_name = week_dir.name
                dest_images_dir = ASSETS_IMAGES_DIR / week_name
                
                print(f"Copying {src_images_dir} to {dest_images_dir}")
                # Create destination directory if it doesn't exist
                dest_images_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy files
                for item in src_images_dir.iterdir():
                    if item.is_file():
                        dest_file = dest_images_dir / item.name
                        shutil.copy2(item, dest_file)
                print(f"  -> Done copying for {week_name}.")
            else:
                print(f"  -> No 'images' folder found in {week_name}.")

def update_markdown_paths():
    print("\n--- 2. Updating Markdown Paths ---")
    if not CONTENT_CANVA_DIR.exists():
        print(f"Error: Target directory {CONTENT_CANVA_DIR} does not exist.")
        return

    # Regex pattern to match the legacy paths
    # Matches: ./data/theory/canva/Week01/images/filename.png
    # Or: ../images/filename.png (just in case)
    pattern1 = re.compile(r'\./data/theory/canva/(Week\d+)/images/([^)]+\.(?:png|jpg|jpeg|gif|svg))')
    pattern2 = re.compile(r'\.\./data/theory/canva/(Week\d+)/images/([^)]+\.(?:png|jpg|jpeg|gif|svg))')
    
    count_files_updated = 0
    count_replacements = 0

    for md_file in CONTENT_CANVA_DIR.rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content
        
        # Replace pattern 1
        # Replaces with: /data/content/canva/assets/images/WeekXX/filename.png
        new_content, num1 = pattern1.subn(r'/data/content/canva/assets/images/\1/\2', new_content)
        # Replace pattern 2
        new_content, num2 = pattern2.subn(r'/data/content/canva/assets/images/\1/\2', new_content)

        total_subs = num1 + num2

        if total_subs > 0:
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {md_file.relative_to(PRACTICE_DIR)} ({total_subs} replacements)")
            count_files_updated += 1
            count_replacements += total_subs

    print(f"\nCompleted! Updated {count_files_updated} files with {count_replacements} path replacements.")

if __name__ == "__main__":
    migrate_images()
    update_markdown_paths()
