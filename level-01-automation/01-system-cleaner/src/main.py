import shutil
from pathlib import Path
import logging
import time
import os
import sys

# Configure logging to output standard timestamps and error levels
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_root_privileges() -> None:
    """
    Ensures the script is run with sudo.
    We check the Effective User ID (euid). If it's not 0 (root), execution halts.
    This prevents permission denial errors halfway through the cleanup process.
    """
    if os.geteuid() != 0:
        logging.error("❌ Error: This script requires administrator (sudo) privileges.")
        sys.exit(1)

def get_real_user_home() -> Path:
    """
    Resolves the "Sudo Trap". When a user runs 'sudo python3 script.py', 
    Path.home() resolves to '/root'. We must check the 'SUDO_USER' environment 
    variable to find the actual human user's home directory so we don't accidentally 
    empty the root user's trash.
    """
    sudo_user = os.environ.get('SUDO_USER')
    if sudo_user:
        return Path(f"/home/{sudo_user}")
    return Path.home()

def check_disk_health() -> None:
    """
    Verifies storage health on the root partition.
    Uses shutil to grab raw byte counts, then performs floor division using 
    bitwise operations (2**30) to efficiently convert Bytes directly to Gigabytes.
    """
    total, used, free = shutil.disk_usage("/")
    
    # Efficient conversion from Bytes to GB
    total_gb = total // (2**30)
    used_gb = used // (2**30)
    free_gb = free // (2**30)
    
    percentage_used = (used / total) * 100
    
    print("\n\033[33m--- STORAGE HEALTH ---\033[0m")
    print(f"💾 Root Partition (/) -> Used: {used_gb}GB | Free: {free_gb}GB | Total: {total_gb}GB")
    
    # Warn the user if they are dangerously close to running out of space
    if percentage_used > 90:
        print(f"\033[31m⚠️ CRITICAL ALERT! Less than 10% disk space remaining ({100 - percentage_used:.1f}% free).\033[0m")
    else:
        print(f"✅ Disk capacity in optimal state ({percentage_used:.1f}% used).")

def clean_directory_by_age(target_dir: Path, max_age_days: int) -> int:
    """
    Iterates through a target directory and removes files/folders older than max_age_days.
    Uses robust exception handling to ensure that if one file is locked by the OS, 
    the script continues cleaning the rest instead of crashing.
    """
    bytes_cleared = 0
    now = time.time()
    
    # Convert days to total seconds for accurate timestamp math
    max_age_seconds = max_age_days * 86400

    if not target_dir.exists():
        logging.warning(f"Directory {target_dir} does not exist. Skipping.")
        return bytes_cleared

    for item in target_dir.iterdir():
        try:
            # Get the last modification time of the item
            file_age = now - item.stat().st_mtime
            
            if file_age > max_age_seconds:
                if item.is_file() or item.is_symlink():
                    bytes_cleared += item.stat().st_size
                    item.unlink() # Delete the file
                elif item.is_dir():
                    # If it's a directory, calculate the size of all contents before deleting
                    dir_size = sum(f.stat().st_size for f in item.glob('**/*') if f.is_file())
                    bytes_cleared += dir_size
                    shutil.rmtree(item) # Recursively delete the directory
        except Exception as e:
            # Catch locked files or permission issues safely
            logging.error(f"Permission denied or error removing {item.name}: {e}")
            
    return bytes_cleared


def main() -> None:
    # Print formatted, colored terminal headers
    print("\033[36m==================================================\033[0m")
    print("    ⚡ MASTER SYSTEM: DIAGNOSTICS & CLEANUP ⚡")
    print("                  (2026 Pro Edition)")
    print("\033[36m==================================================\033[0m")

    # 1. Verify we have the power to delete system files
    check_root_privileges()

    # 2. Run diagnostics on the primary hard drive
    check_disk_health()

    # 3. Locate the actual user's folders, bypassing the sudo root path
    user_home = get_real_user_home()
    cache_path = user_home / ".cache"
    trash_path = user_home / ".local/share/Trash/files"
    
    print("\n\033[33m--- TEMPORARY FILE CLEANUP ---\033[0m")
    
    # 4. Failsafe execution: Require explicit consent
    response = input("Do you want to proceed with cache and trash cleanup? (y/n): ").lower()
    
    if response == "y":
        # Delete cache older than 2 weeks
        cache_freed_bytes = clean_directory_by_age(cache_path, 14)
        # Empty the trash completely (0 days limit)
        trash_freed_bytes = clean_directory_by_age(trash_path, 0)
        
        # Convert total bytes to Megabytes (1024 * 1024)
        total_mb = (cache_freed_bytes + trash_freed_bytes) / 1048576
        print(f"✅ Total freed: {total_mb:.2f} MB")
    else:
        print("Cleanup operation cancelled.")

if __name__ == "__main__":
    main()