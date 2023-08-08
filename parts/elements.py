import os

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QScrollArea, QLineEdit


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


class ImagesPanel(QWidget):
    convert_click = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.convert_button = None
        self.images_box = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.convert_button = QPushButton("Convert All To PNG")
        main_layout.addWidget(self.convert_button)

        self.images_box = ImagesBox()
        scroll_box = QScrollArea()
        scroll_box.setWidgetResizable(True)
        scroll_box.setWidget(self.images_box)
        main_layout.addWidget(scroll_box)

        self.convert_button.clicked.connect(self.convert_button_pressed)

        self.setLayout(main_layout)

    def load_images(self, path):
        self.images_box.load_images(path)

    def flag_convert(self):
        self.images_box.flag_convert()

    def convert_button_pressed(self):
        self.convert_click.emit()


class ImagesBox(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = None

        self.convert_flagged = False
        self.image_displays = []

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)

    def load_images(self, path):
        self.clear_images()
        images_path = os.path.join(path, 'Images')
        for item in os.listdir(images_path):
            if os.path.isfile(os.path.join(images_path, item)):
                image_display = ImageDisplay(os.path.join(images_path, item))
                self.layout.addWidget(image_display)
                self.image_displays.append(image_display)

    def clear_images(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.image_displays = []
        self.convert_flagged = False

    def flag_convert(self):
        if not self.convert_flagged:
            for image in self.image_displays:
                if not image.type.lower() == 'png':
                    image.type_label.setText(image.type_label.text() + ' -> (png)')
            self.convert_flagged = True


class ImageDisplay(QWidget):
    def __init__(self, path):
        super().__init__()
        self.path = path
        extension = os.path.splitext(self.path)[1]
        self.type = extension[1:]

        self.type_label = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        if os.path.isfile(self.path):
            self.type_label = QLabel(self.type)
            layout.addWidget(self.type_label)

            pixmap = QPixmap(self.path)
            scaled_pixmap = pixmap.scaled(150, 200, Qt.AspectRatioMode.KeepAspectRatio)
            image = QLabel()
            image.setPixmap(scaled_pixmap)
            layout.addWidget(image)

        self.setLayout(layout)


class TextsPanel(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.texts_box = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.texts_box = TextsBox()
        scroll_box = QScrollArea()
        scroll_box.setWidgetResizable(True)
        scroll_box.setWidget(self.texts_box)
        main_layout.addWidget(scroll_box)

        self.setLayout(main_layout)

    def save_texts(self):
        self.texts_box.save_texts()

    def load_texts(self, path):
        self.texts_box.load_texts(path)


class TextsBox(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = None
        self.text_displays = []

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)

    def save_texts(self):
        for item in self.text_displays:
            item.save_changes()

    def load_texts(self, path):
        self.clear_texts()
        texts_path = os.path.join(path, 'Texts')
        for item in os.listdir(texts_path):
            if os.path.isfile(os.path.join(texts_path, item)):
                text_display = TextEditDisplay(os.path.join(texts_path, item))
                self.layout.addWidget(text_display)
                self.text_displays.append(text_display)

    def clear_texts(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.text_displays = []


class TextEditDisplay(QWidget):
    def __init__(self, path):
        super().__init__()

        self.path = path
        self.is_number = False

        self.editor = None

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        if os.path.isfile(self.path):
            name = os.path.basename(self.path)
            name_label = QLabel(name)
            layout.addWidget(name_label)

            self.editor = QLineEdit()
            layout.addWidget(self.editor)
            with open(self.path, 'r') as file:
                self.editor.setText(file.read())

        self.setLayout(layout)

    def save_changes(self):
        if os.path.isfile(self.path):
            with open(self.path, 'w') as file:
                file.write(self.editor.text())
