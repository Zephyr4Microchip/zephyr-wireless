import os
import shutil
import subprocess
import tempfile
import urllib.request
import sys
import platform
import time
import struct

if __name__ == "__main__":
    # Get user input for IDE selection
    print("Select IDE environment:")
    print("1. zephyr (uses pkob4_app_cmsis-dap.hex)")
    print("2. mplab (uses pkob4_app.hex)")
    
    ide_choice = input("Enter choice (1/2 or zephyr/mplab) or press Enter for zephyr: ").strip().lower()
    
    # Handle both numeric and text input
    if ide_choice == "1" or ide_choice == "zephyr":
        ide_choice = "zephyr"
    elif ide_choice == "2" or ide_choice == "mplab":
        ide_choice = "mplab"
    else:
        ide_choice = "zephyr"  # default
    
    print(f"Selected: {ide_choice}")
    
    repo_url = "https://github.com/MicrochipTech/openOCD-wireless.git"
    repo_dir = "OpenOCD_WSG_BZx"

    # Check if required folders already exist
    dst1 = os.path.join(repo_dir, "pkob4-cmsis_dap-switcher")
    dst2 = os.path.join(repo_dir, "prebuilt_binaries", "windows", "openocd_support_wbz_pic32wm")
    
    if os.path.exists(dst1) and os.path.exists(dst2):
        print(f"✓ Repository files already exist in {repo_dir}, skipping clone...")
    else:
        print(f"Cloning {repo_url} to {repo_dir}...")
        
        # Remove existing folder if it exists
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir)
        
        # Clone the repository directly to OpenOCD_WSG_BZx
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
        
        print(f"✓ Clone completed")

    # Force overwrite openocd in zi_tools_dir
    print("\nChecking openocd in zi_tools_dir...")
    try:
        # Try to find zi_tools_dir from environment or default location
        zi_tools_dir = os.environ.get("ZI_TOOLS_DIR")
        if not zi_tools_dir:
            # Try default location in user's home .zinstaller
            user_home = os.path.expanduser("~")
            zi_tools_dir = os.path.join(user_home, ".zinstaller", "tools")
        
        if os.path.exists(zi_tools_dir):
            openocd_dest = os.path.join(zi_tools_dir, "openocd")
            wbz451_cfg = os.path.join(openocd_dest, "share", "openocd", "scripts", "target", "wbz451.cfg")
            
            # Check if wbz451.cfg already exists
            if os.path.exists(wbz451_cfg):
                print(f"✓ wbz451.cfg already exists at {wbz451_cfg}, skipping overwrite")
            else:
                print(f"⚠ wbz451.cfg not found, overwriting openocd...")
                openocd_src = dst2  # prebuilt_binaries/windows/openocd_support_wbz_pic32wm
                
                if os.path.exists(openocd_src):
                    # Remove existing openocd folder if it exists
                    if os.path.exists(openocd_dest):
                        print(f"Removing existing openocd at {openocd_dest}...")
                        shutil.rmtree(openocd_dest)
                    
                    # Copy all contents
                    print(f"Copying {openocd_src} to {openocd_dest}...")
                    shutil.copytree(openocd_src, openocd_dest)
                    print(f"✓ Successfully overwritten openocd in {openocd_dest}")
                else:
                    print(f"⚠ Source openocd not found at {openocd_src}")
        else:
            print(f"⚠ zi_tools_dir not found at {zi_tools_dir}")
            print(f"  Set ZI_TOOLS_DIR environment variable or ensure .zinstaller exists")
    except Exception as e:
        print(f"⚠ Failed to overwrite openocd in zi_tools_dir: {e}")

    # Install pycmsisdapswitcher (only if not already installed)
    print("Checking for pycmsisdapswitcher...")
    try:
        import pycmsisdapswitcher
        print("✓ pycmsisdapswitcher is already installed.")
    except ImportError:
        print("Installing pycmsisdapswitcher...")
        subprocess.run(["pip", "install", "pycmsisdapswitcher"], check=True)

    # Install/upgrade libusb and pyusb (only if not already installed)
    print("Checking for libusb and pyusb...")
    libusb_missing = False
    pyusb_missing = False
    try:
        import libusb1
        print("✓ libusb is already installed.")
    except ImportError:
        libusb_missing = True
    
    try:
        import usb
        print("✓ pyusb is already installed.")
    except ImportError:
        pyusb_missing = True
    
    if libusb_missing or pyusb_missing:
        print("Installing/upgrading libusb and pyusb...")
        subprocess.run(["pip", "install", "--upgrade", "libusb", "pyusb"], check=True)
    else:
        print("Both libusb and pyusb are already installed.")

    # Check if libusb backend is available
    print("\nChecking libusb backend availability...")
    def has_libusb_backend():
        try:
            import usb.backend.libusb1 as libusb1
            return libusb1.get_backend() is not None
        except Exception:
            return False
    
    if not has_libusb_backend():
        print("⚠ libusb backend not available. Downloading and installing libusb-1.0.dll...")
        
        # Download libusb 7z archive
        libusb_url = "https://github.com/libusb/libusb/releases/download/v1.0.29/libusb-1.0.29.7z"
        temp_7z = os.path.join(tempfile.gettempdir(), "libusb-1.0.29.7z")
        
        try:
            print(f"Downloading {libusb_url}...")
            urllib.request.urlretrieve(libusb_url, temp_7z)
            print(f"✓ Downloaded to {temp_7z}")
            
            # Extract 7z archive
            extract_dir = os.path.join(tempfile.gettempdir(), "libusb-1.0.29")
            print(f"Extracting to {extract_dir}...")
            
            # Try using 7z command-line tool first
            extracted = False
            
            # Try different 7z command variants and common paths
            seven_zip_commands = [
                "7z",
                "7z.exe",
                r"C:\Program Files\7-Zip\7z.exe",
                r"C:\Program Files (x86)\7-Zip\7z.exe",
            ]
            
            for cmd in seven_zip_commands:
                try:
                    print(f"Trying {cmd}...")
                    result = subprocess.run([cmd, "x", f"-o{extract_dir}", temp_7z, "-y"], 
                                           capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"✓ Extracted with {cmd}")
                        extracted = True
                        break
                    else:
                        print(f"⚠ {cmd} extraction failed: {result.stderr}")
                except FileNotFoundError:
                    continue
                except Exception as e:
                    print(f"⚠ Error with {cmd}: {e}")
                    continue
            
            if not extracted:
                print("⚠ 7z command-line tool not found in PATH or common locations")
            
            # Fallback to py7zr
            if not extracted:
                try:
                    import py7zr
                    with py7zr.SevenZipFile(temp_7z, mode='r') as archive:
                        archive.extractall(path=extract_dir)
                    print("✓ Extracted with py7zr")
                    extracted = True
                except ImportError:
                    # Try installing py7zr
                    print("Installing py7zr for extraction...")
                    subprocess.run([sys.executable, "-m", "pip", "install", "py7zr"], check=False)
                    try:
                        import py7zr
                        with py7zr.SevenZipFile(temp_7z, mode='r') as archive:
                            archive.extractall(path=extract_dir)
                        print("✓ Extracted with py7zr")
                        extracted = True
                    except Exception as e:
                        print(f"⚠ Could not extract with py7zr: {e}")
                except Exception as e:
                    print(f"⚠ Could not extract with py7zr: {e}")
            
            if not extracted:
                print("Please manually extract the 7z file and copy MinGW64\\dll\\libusb-1.0.dll to C:\\Python312")
                extract_dir = None
            
            # Copy DLL to Python folder
            if extract_dir:
                dll_source = os.path.join(extract_dir, "MinGW64", "dll", "libusb-1.0.dll")
                dll_dest = os.path.join(os.path.dirname(sys.executable), "libusb-1.0.dll")
                
                if os.path.exists(dll_source):
                    shutil.copyfile(dll_source, dll_dest)
                    print(f"✓ Copied libusb-1.0.dll to {dll_dest}")
                else:
                    print(f"⚠ DLL not found at expected path: {dll_source}")
                    print(f"  Looking for DLL in extraction directory...")
                    # Search for the DLL
                    for root, dirs, files in os.walk(extract_dir):
                        if "libusb-1.0.dll" in files:
                            dll_source = os.path.join(root, "libusb-1.0.dll")
                            shutil.copyfile(dll_source, dll_dest)
                            print(f"✓ Found and copied libusb-1.0.dll from {dll_source} to {dll_dest}")
                            break
                
                # Clean up
                try:
                    os.remove(temp_7z)
                    shutil.rmtree(extract_dir)
                    print("✓ Cleaned up temporary files")
                except Exception as e:
                    print(f"⚠ Could not clean up temp files: {e}")
        
        except Exception as e:
            py_dir = os.path.dirname(sys.executable)
            print(f"✗ Failed to download/extract libusb: {e}")
            print(f"Please manually download from: {libusb_url}")
            print(f"Extract and copy MinGW64\\dll\\libusb-1.0.dll to {py_dir}")
    else:
        print("✓ libusb backend is already available")

    # Prepare environment to use bundled libusb from pip package
    print("\nPreparing environment with pip-installed libusb...")
    env = os.environ.copy()
    
    # Search for libusb DLL in site-packages
    try:
        import site
        found_dll = None
        search_names = ['libusb-1.0.dll', 'libusb1.dll']
        
        for sp in site.getsitepackages():
            print(f"Searching in {sp}...")
            for root, dirs, files in os.walk(sp):
                for name in files:
                    if name.lower() in search_names:
                        found_dll = os.path.join(root, name)
                        print(f"✓ Found: {found_dll}")
                        break
                if found_dll:
                    break
            if found_dll:
                break
        
        if found_dll:
            dll_dir = os.path.dirname(found_dll)
            env["PATH"] = dll_dir + os.pathsep + env.get("PATH", "")
            print(f"✓ Added to PATH: {dll_dir}")
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
            py_dir = os.path.dirname(sys.executable)
            print(f"⚠ Failed to switch to {switcher_desc} firmware!")
        else:
            print(f"✓ Successfully switched to {switcher_desc} firmware!")
    else:
        print(f"Source file not found: {source_path}")

