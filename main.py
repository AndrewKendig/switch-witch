import shutil
import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, QFileDialog, QLabel, QComboBox, QPushButton
from PyQt6.QtGui import QAction
import parts.data_handler as dh
import parts.elements as elements


version_number = '2.0'


class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        file_menu = self.addMenu("File")

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.parent().save_project)
        file_menu.addAction(save_action)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.parent().open_project)
        file_menu.addAction(open_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.parent().close)
        file_menu.addAction(exit_action)

        edit_menu = self.addMenu("Edit")

        display_folder_action = QAction("Set Display Folder", self)
        display_folder_action.triggered.connect(self.parent().prompt_display_folder)
        edit_menu.addAction(display_folder_action)

        source_folder_action = QAction("Set Source Folder", self)
        source_folder_action.triggered.connect(self.parent().prompt_source_folder)
        edit_menu.addAction(source_folder_action)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = None

        self.information_panel = None
        self.images_panel = None
        self.texts_panel = None

        self.init_ui()
        self.init_data()

    def init_ui(self):
        self.setWindowTitle(f'Switch Witch v{version_number}')
        self.setGeometry(100, 100, 800, 400)

        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the main layout for the central widget
        main_layout = QHBoxLayout(central_widget)
        central_widget.setLayout(main_layout)

        # Create the left column widget
        left_column = QWidget(self)
        left_column_layout = QVBoxLayout()
        left_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_column.setLayout(left_column_layout)
        self.information_panel = elements.InfoPanel(self)
        left_column_layout.addWidget(self.information_panel)

        self.texts_panel = elements.TextsPanel(self)
        left_column_layout.addWidget(self.texts_panel)

        main_layout.addWidget(left_column, 2)  # Weight 2 for 2:1 ratio

        self.information_panel.load_click.connect(self.load_version_button_pressed)
        self.information_panel.save_click.connect(self.save_changes_button_pressed)
        self.information_panel.switch_click.connect(self.switch_button_pressed)

        # Create the right column widget
        right_column = QWidget(self)
        right_column_layout = QVBoxLayout()
        right_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_column.setLayout(right_column_layout)
        self.images_panel = elements.ImagesPanel(self)
        right_column_layout.addWidget(self.images_panel)
        main_layout.addWidget(right_column, 1)  # Weight 1 for 2:1 ratio

        self.images_panel.convert_click.connect(self.convert_button_pressed)

        # Create the menu bar
        menubar = MenuBar(self)
        self.setMenuBar(menubar)

    def init_data(self, display_folder=None, source_folder=None):
        self.data = dh.Data(display_folder, source_folder)

    def save_project(self):
        if self.data:
            if self.data.settings.settings_file:
                self.data.settings.save_to_file()
            else:
                self.save_project_as()

    def save_project_as(self):
        if self.data:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Switch Witch Project", "", "SWS Files (*.sws);;All Files (*)")
            if file_path:
                self.data.settings.save_to_file(file_path)

    def open_project(self):
        self.prompt_settings_file()
        self.data.settings.load_from_file()
        self.update_display()

    def prompt_display_folder(self):
        if self.data:
            folder_path = QFileDialog.getExistingDirectory(self, "Select Display Folder")
            if folder_path:
                self.data.settings.set_display_folder(folder_path)
                self.update_display()

    def prompt_source_folder(self):
        if self.data:
            folder_path = QFileDialog.getExistingDirectory(self, "Select Source Folder")
            if folder_path:
                self.data.settings.set_source_folder(folder_path)
                self.update_display()

    def prompt_settings_file(self):
        if self.data:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Switch Witch Project", "", "SWS Files (*.sws);;All Files (*)")
            if file_path:
                self.data.settings.set_settings_file(file_path)

    def update_display(self):
        if self.data.settings.display_folder:
            self.information_panel.set_display_folder(self.data.settings.display_folder)
        if self.data.settings.source_folder:
            self.information_panel.set_source_folder(self.data.settings.source_folder)
        if self.data.settings.versions:
            self.information_panel.set_versions(self.data.settings.versions)

    def load_version_button_pressed(self, index, value):
        path = os.path.join(self.data.settings.source_folder, self.data.settings.versions[index])
        self.images_panel.load_images(path)
        try:
            self.texts_panel.load_texts(path)
        except Exception as e:
            print(e)

    def save_changes_button_pressed(self, index, value):
        path = os.path.join(self.data.settings.source_folder, self.data.settings.versions[index])
        self.texts_panel.save_texts()

    def switch_button_pressed(self, index, value):
        source_path = os.path.join(self.data.settings.source_folder, self.data.settings.versions[index])
        images_source_path = os.path.join(source_path, 'Images')
        images_destination_path = os.path.join(self.data.settings.display_folder, 'Images')
        texts_source_path = os.path.join(source_path, 'Texts')
        texts_destination_path = os.path.join(self.data.settings.display_folder, 'Texts')
        if os.path.isdir(images_source_path):
            self.data.files.copy_all(images_source_path, images_destination_path)
        if os.path.isdir(texts_source_path):
            self.data.files.copy_all(texts_source_path, texts_destination_path)

    def convert_button_pressed(self):
        self.data.files.set_convert_flag(True)
        self.images_panel.flag_convert()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
