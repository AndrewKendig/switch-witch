from cx_Freeze import setup, Executable

app_name = "Switch-Witch"
app_version = "2.0"
app_description = "For Jolfwe"
author_name = "AndrewKendig"
author_email = "andrewtkendig@gmail.com"
app_entry_point = "main.py"
packages = ["PIL", "PyQt6"]  # List of packages to include

# Dependencies (add more if needed)
build_exe_options = {
    "packages": packages,
    "includes": [],
    "excludes": [],
    "include_files": []
}

# Executable
exe = Executable(
    script=app_entry_point,
    base="Win32GUI",  # Set this to None for console-based apps, "Win32GUI" for GUI apps
    target_name=f"{app_name}.exe",  # Change the executable name as needed
    icon=None  # Path to the application icon if desired
)

# Setup configuration
setup(
    name=app_name,
    version=app_version,
    description=app_description,
    author=author_name,
    author_email=author_email,
    options={"build_exe": build_exe_options},
    executables=[exe]
)
