import os
import json


class Data:
    def __init__(self, display_folder=None, source_folder=None):
        self.settings = Settings()

        if display_folder:
            self.settings.set_display_folder(display_folder)
        if source_folder:
            self.settings.set_source_folder(source_folder)


class Settings:
    def __init__(self):
        self.display_folder = None
        self.source_folder = None
        self.settings_file = None

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
            return True
        return False

    def set_settings_file(self, settings_file):
        if os.path.isfile(settings_file):
            self.settings_file = settings_file
            return True
        return False
