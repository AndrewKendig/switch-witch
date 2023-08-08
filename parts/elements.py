from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton


class InfoPanel(QWidget):
    load_click = pyqtSignal(int, str)
    save_click = pyqtSignal(int, str)
    switch_click = pyqtSignal(int, str)

    def __init__(self, parent):
        super().__init__(parent)

        self.source_folder_display = None
        self.display_folder_display = None

        self.versions_box = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.source_folder_display = TextDisplay('Source Folder:')
        main_layout.addWidget(self.source_folder_display)

        self.display_folder_display = TextDisplay('Display Folder:')
        main_layout.addWidget(self.display_folder_display)

        self.versions_box = VersionsBox()
        main_layout.addWidget(self.versions_box)

        switch_button = QPushButton('Switch')
        main_layout.addWidget(switch_button)

        switch_button.clicked.connect(self.switch_button_pressed)
        self.versions_box.load_click.connect(self.load_button_pressed)
        self.versions_box.save_click.connect(self.save_button_pressed)

        self.setLayout(main_layout)

    def set_source_folder(self, source_folder):
        self.source_folder_display.set_text(source_folder)

    def set_display_folder(self, display_folder):
        self.display_folder_display.set_text(display_folder)

    def set_versions(self, versions):
        self.versions_box.set_versions(versions)

    def load_button_pressed(self, index, value):
        self.load_click.emit(index, value)

    def save_button_pressed(self, index, value):
        self.save_click.emit(index, value)

    def switch_button_pressed(self):
        self.switch_click.emit(self.versions_box.active['index'], self.versions_box.active['value'])


class TextDisplay(QWidget):
    def __init__(self, fixed_text):
        super().__init__()

        self.fixed_text = fixed_text
        self.display_text = None

        self.text_label = None

        self.init_ui()

    def init_ui(self):

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        fixed_label = QLabel(self.fixed_text)
        self.text_label = QLabel()

        layout.addWidget(fixed_label)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

    def set_text(self, text):
        self.display_text = text
        self.text_label.setText(self.display_text)

    def clear(self):
        self.display_text = None
        self.text_label.setText('')


class VersionsBox(QWidget):
    load_click = pyqtSignal(int, str)
    save_click = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()

        self.active = None
        self.save_active = None

        self.versions_combobox = None
        self.load_button = None
        self.save_button = None

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        self.versions_combobox = QComboBox()
        layout.addWidget(self.versions_combobox, stretch=3)

        self.load_button = QPushButton("Load")
        layout.addWidget(self.load_button, stretch=0)

        self.save_button = QPushButton("Save")
        layout.addWidget(self.save_button, stretch=0)

        self.versions_combobox.currentIndexChanged.connect(self.version_changed)
        self.load_button.clicked.connect(self.load_button_pressed)
        self.save_button.clicked.connect(self.save_button_pressed)

        self.setLayout(layout)

    def set_versions(self, versions):
        self.versions_combobox.clear()
        self.versions_combobox.addItems(versions)

    def version_changed(self):
        selected_item_index = self.versions_combobox.currentIndex()
        selected_item_text = self.versions_combobox.currentText()
        self.active = dict(index=selected_item_index, value=selected_item_text)

    def load_button_pressed(self):
        self.save_active = self.active
        self.load_click.emit(self.active['index'], self.active['value'])

    def save_button_pressed(self):
        self.save_click.emit(self.save_active['index'], self.save_active['value'])
