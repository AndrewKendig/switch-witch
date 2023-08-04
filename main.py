import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, QFileDialog
from PyQt6.QtGui import QAction
import parts.data_handler as dh


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
        main_layout.addWidget(left_column, 2)  # Weight 2 for 2:1 ratio

        # Create the right column widget
        right_column = QWidget(self)
        main_layout.addWidget(right_column, 1)  # Weight 1 for 2:1 ratio

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

    def prompt_display_folder(self):
        if self.data:
            folder_path = QFileDialog.getExistingDirectory(self, "Select Display Folder")
            if folder_path:
                self.data.settings.set_display_folder(folder_path)

    def prompt_source_folder(self):
        if self.data:
            folder_path = QFileDialog.getExistingDirectory(self, "Select Source Folder")
            if folder_path:
                self.data.settings.set_source_folder(folder_path)

    def prompt_settings_file(self):
        if self.data:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Switch Witch Project", "", "SWS Files (*.sws);;All Files (*)")
            if file_path:
                self.data.settings.set_settings_file(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
