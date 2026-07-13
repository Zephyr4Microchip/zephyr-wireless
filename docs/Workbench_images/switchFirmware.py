import os
import subprocess
import sys
import site

if __name__ == "__main__":
    repo_dir = "OpenOCD_WSG_BZx"

    # Get user input for IDE selection
    print("Select firmware to switch to:")
    print("1. zephyr - OpenOCD CMSIS-DAP (uses pkob4_app_cmsis-dap.hex)")
    print("2. mplab  - Default MPLAB PKOB4 (uses pkob4_app.hex)")

    ide_choice = input("Enter choice (1/2 or zephyr/mplab) or press Enter for zephyr: ").strip().lower()

    # Handle both numeric and text input
    if ide_choice == "1" or ide_choice == "zephyr":
        ide_choice = "zephyr"
    elif ide_choice == "2" or ide_choice == "mplab":
        ide_choice = "mplab"
    else:
        ide_choice = "zephyr"  # default

    print(f"Selected: {ide_choice}")

    # Prepare environment to use bundled libusb from pip package
    print("\nPreparing environment with pip-installed libusb...")
    env = os.environ.copy()

    # Search for libusb DLL in site-packages
    try:
        found_dll = None
        search_names = ['libusb-1.0.dll', 'libusb1.dll']

        for sp in site.getsitepackages():
            for root, dirs, files in os.walk(sp):
                for name in files:
                    if name.lower() in search_names:
                        found_dll = os.path.join(root, name)
                        break
                if found_dll:
                    break
            if found_dll:
                break

        if found_dll:
            dll_dir = os.path.dirname(found_dll)
            env["PATH"] = dll_dir + os.pathsep + env.get("PATH", "")
            print(f"✓ Added libusb to PATH: {dll_dir}")
        else:
            print("⚠ Warning: Could not find libusb DLL in site-packages")
    except Exception as e:
        print(f"⚠ Error searching for libusb DLL: {e}")

    # Run the CMSIS-DAP switcher
    if ide_choice == "zephyr":
        source_path = os.path.join(repo_dir, "pkob4-cmsis_dap-switcher", "pkob4_app_cmsis-dap.hex")
        fwtype = "cmsis"
        switcher_desc = "Zephyr CMSIS-DAP"
    else:  # mplab
        source_path = os.path.join(repo_dir, "pkob4-cmsis_dap-switcher", "pkob4_app.hex")
        fwtype = "mplab"
        switcher_desc = "MPLAB"

    if os.path.exists(source_path):
        print(f"\nSwitching to {switcher_desc} firmware...")
        print(f"Source: {source_path}")
        cmd = [sys.executable, "-m", "pycmsisdapswitcher", "--action", "switch", "--target=evalboard",
               f"--source={source_path}", f"--fwtype={fwtype}"]
        print(f"Command: {' '.join(cmd)}")
        proc = subprocess.run(cmd, env=env)
        if proc.returncode != 0:
            print(f"⚠ Failed to switch to {switcher_desc} firmware!")
        else:
            print(f"✓ Successfully switched to {switcher_desc} firmware!")
    else:
        print(f"Source file not found: {source_path}")
        print(f"Make sure you have run installOpenOCD_WSG_BZx.py first to clone the repository.")
