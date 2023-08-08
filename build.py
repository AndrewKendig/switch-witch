import os
import shutil
import sys
import zipfile

from cx_Freeze import setup, Executable

app_name = "Switch-Witch"
app_version = "2.1.1"
app_description = "For Jolfwe"
author_name = "AndrewKendig"
author_email = "andrewtkendig@gmail.com"
app_entry_point = "main.py"
packages = ["PIL", "PyQt6"]  # List of packages to include

build_path = 'build/exe.win-amd64-{}.{}'.format(sys.version_info.major, sys.version_info.minor)
if os.path.exists(build_path):
    shutil.rmtree(build_path)

if not os.path.exists('build/exe'):
    os.makedirs('build/exe')

if os.path.isfile('build/exe/switch-witch-{}.zip'.format(app_version)):
    os.remove('build/exe/switch-witch-{}.zip'.format(app_version))

# Dependencies (add more if needed)
build_exe_options = {
    "packages": [],
    "includes": packages,
    "excludes": [],
    "include_files": [],
    "zip_include_packages": "*",
    "zip_exclude_packages": []
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

def zip_folder(folder_path, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path, )
    zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)

    for root, folders, files in contents:
        # Include all subfolders, including empty ones.
        for folder_name in folders:
            absolute_path = os.path.join(root, folder_name)
            relative_path = absolute_path.replace(parent_folder + '\\',
                                                  '')
            zip_file.write(absolute_path, relative_path.replace(build_path, ''))
        for file_name in files:
            absolute_path = os.path.join(root, file_name)
            relative_path = absolute_path.replace(parent_folder + '\\',
                                                  '')
            zip_file.write(absolute_path, relative_path.replace(build_path, ''))
    zip_file.close()

try:
    shutil.copyfile('LICENSE', build_path + '/LICENSE')
    shutil.copyfile('SOURCE', build_path + '/SOURCE')
except:
    pass

zip_folder(build_path, 'build/exe/switch-witch-{}.zip'.format(app_version))