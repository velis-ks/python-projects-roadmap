import shutil
from pathlib import Path
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_directory_by_age(target_dir: Path, max_age_days: int) -> int:
    """
    Removes files and folders inside target_dir that haven't been modified 
    in the last max_age_days. Returns the total bytes cleared.
    """
    bytes_cleared = 0
    now = time.time()
    max_age_seconds = max_age_days * 86400

    if not target_dir.exists():
        logging.warning(f"Directory {target_dir} does not exist.")
        return bytes_cleared

    for item in target_dir.iterdir():
        try:
            # Check modification time
            file_age = now - item.stat().st_mtime
            if file_age > max_age_seconds:
                if item.is_file() or item.is_symlink():
                    bytes_cleared += item.stat().st_size
                    item.unlink()
                elif item.is_dir():
                    # Calculate directory size before removing
                    dir_size = sum(f.stat().st_size for f in item.glob('**/*') if f.is_file())
                    bytes_cleared += dir_size
                    shutil.rmtree(item)
                logging.info(f"Removed dynamic item: {item.name}")
        except Exception as e:
            logging.error(f"Permission denied or error removing {item.name}: {e}")
            
    return bytes_cleared

def main() -> None:
    user_home = Path.home()
    # Define target paths for Linux environments
    cache_path = user_home / ".cache"
    trash_path = user_home / ".local/share/Trash/files"
    
    logging.info("Starting system cleanup script setup.")
    
    # Execution logic will go here
    response = input("Do you want to proceed? (y/n): ").lower()
    if (response != "y"):
        print("Operation Cancelled")
        return
    
    # 1. Clean cache (older than 14 days)
    cache_freed_bytes = clean_directory_by_age(cache_path, 14)

    # 2. Clean trash
    trash_freed_bytes = clean_directory_by_age(trash_path, 0)

    # 3. Total
    total_mb = (cache_freed_bytes + trash_freed_bytes) / 1048576


    print(f"Target cache: {cache_path}")
    print(f"Target trash: {trash_path}")
    print(f"Total freed: {total_mb:.2f} MB")

if __name__ == "__main__":
    main()
