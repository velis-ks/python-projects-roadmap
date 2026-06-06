import os   # consults OS info
import sys  # controls the system
import subprocess # executes SO commands
from pathlib import Path # controls the paths
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Check for Privileges
def check_privileges():
    # os.geteuid() returns the user ID of the current process.
    # In Linux systems, the root_user (sudo) always has an ID of 0.
    if os.geteuid() != 0:
        print("Try with sudo")
        # sys.exit(1) terminates the script immediately, returning an error code 1 to the OS.
        sys.exit(1)

"""
In Python, we use the subprocess moduclealle to run terminal commands.

Specifically, the subprocess.run() method takes a list of strings representing the command and its arguments.
Adding the argument check=True is crucial: it makes Python automatically end the script and throw an error if 
the Linux command fails (this acts just like the && operator in your Bash script).

For example, running ls -l safely looks like this: subprocess.run(["ls", "-l"], check=True)
"""

# 2. Installing Dependencies
def install_dependencies():
    print("Installing power management tools...")
    subprocess.run(["apt", "update"], check=True)
    subprocess.run(["apt", "install", "-y", "tlp", "tlp-rdw", "cpufrequtils"], check=True)


# 3. Setting the Battery Thresholds
"""
In Python, the safest way to write to system files is using a 'with open(...)' block, 
which automatically closes the file when it's done.

Because we are dealing with hardware paths, we will use the pathlib module.
"""

def set_battery_thresholds(start: int, end: int):
    print(f"Setting battery thresholds: Start at {start}%, end at {end}%")
    
    bat0_path = Path("/sys/class/power_supply/BAT0") # create a Path object and assign it to a variable
    
    if not bat0_path.exists():
        logging.warning(f"BAT0 not found at {bat0_path}. Skipping.")
        return # ends the function here so it doesn't try to write to files that don't exist
    
    """
    To write to a file in Python, we use "w" (write mode). 
    Also, hardware files expect strings, not integers, so we have to wrap our start and end variables in str().
    """
    # Write the start threshold
    with open(bat0_path / "charge_control_start_threshold", "w") as f:
        f.write(str(start))
      
    # Write the end threshold
    with open(bat0_path / "charge_control_end_threshold", "w") as f:
        f.write(str(end))

# 4. CPU Governor Selection
def get_optimal_governor() -> str:
    # 1. We create a Path object representing the hardware file.
    governator = Path("/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors")
    
    # 2. .exists() is a method, so we MUST use () to execute it safely before reading.
    if governator.exists():
        # 3. .read_text() grabs the entire file content as a string without needing a 'with open()' block.
        text_content = governator.read_text()
        if "schedutil" in text_content:
            return "schedutil"
    
    # 4. We put the fallback at the very bottom. If anything above fails, Python implicitly drops down here.
    return "ondemand"

# 5. TLP Configuration
# Notice we added start and end parameters here
def configure_tlp(governor: str, start: int, end: int):
    print("Configuring TLP...")
    
    # The 'f' before the triple quotes creates an "f-string".
    # This allows us to inject variables directly using {governor} instead of Bash's $governor.
    # CRITICAL: The text inside must be flush to the left, otherwise Python writes empty spaces into the Linux config!
    tlp_config = f"""START_CHARGE_THRESH_BAT0={start}
STOP_CHARGE_THRESH_BAT0={end}
CPU_SCALING_GOVERNOR_ON_AC={governor}
CPU_SCALING_GOVERNOR_ON_BAT={governor}
CPU_ENERGY_PERF_POLICY_ON_AC=balance_performance
CPU_ENERGY_PERF_POLICY_ON_BAT=balance_power
CPU_BOOST_ON_AC=1
CPU_BOOST_ON_BAT=0
"""
  
    # 'with open' automatically closes the file when done. "w" means write (overwrite) mode.
    with open("/etc/default/tlp", "w") as f:
        f.write(tlp_config)

# 6. Apply and Notify
def apply_and_notify():
    print("Applying configuration and starting services...")
    try:
        # check=True is our safety net. If 'systemctl' fails, Python throws an error and stops.
        subprocess.run(['systemctl', 'enable', 'tlp', '--now'], check=True)
        
        # stdout=subprocess.DEVNULL swallows the terminal output so our script stays quiet and clean.
        subprocess.run(['tlp', 'start'], check=True, stdout=subprocess.DEVNULL)
        
        # The Notification Workaround: Since we ran the script with 'sudo', Python is acting as root.
        # Root doesn't have a desktop! We extract SUDO_USER to find the actual username...
        real_user = os.environ.get("SUDO_USER")
        if real_user:
            # ...and then we send the notify-send command directly to the specific user session.
            subprocess.run([
                'sudo', '-u', real_user, 
                'DISPLAY=:0', 'DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus',
                'notify-send', 'Power Management', 'Battery thresholds and CPU governor applied!'
            ])
            
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start TLP or send notification: {e}")

# Main execution block
def main():
    check_privileges()
    install_dependencies()
    
    # Single Source of Truth
    charge_start = 15
    charge_end = 80
    
    set_battery_thresholds(charge_start, charge_end)
    
    optimal_gov = get_optimal_governor()
    # Pass the variables into the TLP config as well
    configure_tlp(optimal_gov, charge_start, charge_end)
    
    apply_and_notify()
    print("Power configuration complete.")

if __name__ == "__main__":
    main()