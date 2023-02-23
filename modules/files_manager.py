
def init_data_folder(os):
    # get the current working directory
    current_directory = os.getcwd()

    # create the folder path by joining the current directory with the folder name
    folder_path = os.path.join(current_directory, 'Data\\')

    # check if the folder already exists
    if not os.path.exists(folder_path):
        # create the folder if it does not exist
        os.mkdir(folder_path)
    return folder_path


def init_group_structure(os, path):
    if not os.path.exists(path):
        os.mkdir(path)
    output_folder = path + 'Output\\'
    versions_folder = path + 'Versions\\'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        init_content_structure(os, output_folder)
    if not os.path.exists(versions_folder):
        os.mkdir(versions_folder)
    return output_folder, versions_folder


def init_version_structure(os, path):
    if not os.path.exists(path):
        os.mkdir(path)
    images_folder, texts_folder = init_content_structure(os, path)
    return images_folder, texts_folder


def init_content_structure(os, path):
    images_folder = path + 'Images\\'
    texts_folder = path + 'Texts\\'
    if not os.path.exists(images_folder):
        os.mkdir(images_folder)
    if not os.path.exists(texts_folder):
        os.mkdir(texts_folder)
    return images_folder, texts_folder


def get_groups(os, data_path):
    folders = os.scandir(path=data_path)
    groups = []
    for entry in folders:
        groups.append(os.path.basename(entry))
    return groups


def get_versions(os, versions_path):
    folders = os.scandir(path=(versions_path + '\\Versions\\'))
    groups = []
    for entry in folders:
        groups.append(os.path.basename(entry))
    return groups


def push_files(shutil, source_folder, destination_folder):
    shutil.rmtree(destination_folder)
    shutil.copytree(source_folder, destination_folder)
    return True
