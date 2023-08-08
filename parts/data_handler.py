import os
import json
import shutil
from PIL import Image


class Data:
    def __init__(self, display_folder=None, source_folder=None):
        self.settings = Settings()
        if display_folder:
            self.settings.set_display_folder(display_folder)
        if source_folder:
            self.settings.set_source_folder(source_folder)

        self.files = Files()


class Settings:
    def __init__(self):
        self.display_folder = None
        self.source_folder = None
        self.settings_file = None

        self.versions = []

    def save_settings(self):
        settings_dict = dict(source_folder=self.source_folder,
                             display_folder=self.display_folder)
        settings_json = json.dumps(settings_dict)
        return settings_json

    def load_settings(self, settings_json):
        settings_dict = json.loads(settings_json)
        if 'display_folder' in settings_dict:
            self.display_folder = settings_dict['display_folder']
        if 'source_folder' in settings_dict:
            self.source_folder = settings_dict['source_folder']
            self.update_versions()

    def save_to_file(self, settings_file=None):
        if settings_file:
            self.settings_file = settings_file
        if self.settings_file:
            settings_json = self.save_settings()
            with open(self.settings_file, 'w') as file:
                file.write(settings_json)
            return True

    def load_from_file(self, settings_file=None):
        if settings_file:
            if not self.set_settings_file(settings_file):
                return False
        if self.settings_file:
            with open(self.settings_file, 'r') as file:
                settings_json = file.read()
                self.load_settings(settings_json)

    def set_display_folder(self, display_folder):
        if os.path.isdir(display_folder):
            self.display_folder = display_folder
            return True
        return False

    def set_source_folder(self, source_folder):
        if os.path.isdir(source_folder):
            self.source_folder = source_folder
            self.update_versions()
            return True
        return False

    def set_settings_file(self, settings_file):
        if os.path.isfile(settings_file):
            self.settings_file = settings_file
            return True
        return False

    def update_versions(self):
        if self.source_folder:
            self.versions = []
            for item in os.listdir(self.source_folder):
                item_path = os.path.join(self.source_folder, item)
                if os.path.isdir(item_path):
                    self.versions.append(item)


class Files:
    def __init__(self):
        self.convert_flag = False

    def copy_all(self, source_path, destination_path):
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        else:
            for root, dirs, files in os.walk(destination_path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for directory in dirs:
                    os.rmdir(os.path.join(root, directory))
        for item in os.listdir(source_path):
            if os.path.isfile(os.path.join(source_path, item)):
                item_source_path = os.path.join(source_path, item)
                item_destination_path = os.path.join(destination_path, item)
                shutil.copy(item_source_path, item_destination_path)

    def set_convert_flag(self, convert_flag):
        self.convert_flag = convert_flag

    def convert_images(self, path):
        if self.convert_flag:
            image_formats = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]  # Supported image formats
            for index, item in enumerate(os.listdir(path)):
                file_path = os.path.join(path, item)
                if os.path.isfile(file_path) and os.path.splitext(item)[1].lower() in image_formats:
                    image = Image.open(file_path)

                    # Convert the image to PNG format and change name
                    output_path = os.path.join(path, "image-" + str(index) + ".png")
                    image.save(output_path, format="PNG")

                    image.close()
                    os.remove(file_path)

