import os
import shutil
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGridLayout, QSlider, QLabel, QPushButton, QFileDialog, QMessageBox

from frontengine.show.image.paint_image import ImageWidget


class ImageSettingUI(QWidget):

    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout()
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        # Init variable
        self.image_widget_list = list()
        self.show_all_screen = False
        # Opacity setting
        self.opacity_slider = QSlider()
        self.opacity_slider.setOrientation(Qt.Orientation.Horizontal)
        self.opacity_label = QLabel("Opacity")
        self.opacity_slider.setMinimum(1)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(20)
        self.opacity_slider.setTickInterval(1)
        self.opacity_slider_value_label = QLabel(str(self.opacity_slider.value()))
        self.opacity_slider.actionTriggered.connect(self.opacity_trick)
        self.setLayout(self.grid_layout)
        # Choose file button
        self.choose_file_button = QPushButton("Choose Image")
        self.choose_file_button.clicked.connect(self.choose_and_copy_file_to_cwd_image_dir_then_play)
        # Ready label and variable
        self.ready_label = QLabel("Not Ready yet.")
        self.gif_image_path: [str, None] = None
        # Start button
        self.start_button = QPushButton("Start Play Image")
        self.start_button.clicked.connect(self.start_play_image)
        # Add to layout
        self.grid_layout.addWidget(self.opacity_label, 0, 0)
        self.grid_layout.addWidget(self.opacity_slider_value_label, 0, 1)
        self.grid_layout.addWidget(self.opacity_slider, 0, 2)
        self.grid_layout.addWidget(self.choose_file_button, 1, 0)
        self.grid_layout.addWidget(self.ready_label, 1, 1)
        self.grid_layout.addWidget(self.start_button, 2, 0)
        self.setLayout(self.grid_layout)

    def start_play_image(self):
        if self.gif_image_path is None:
            message_box = QMessageBox(self)
            message_box.setText("Please choose a Image")
            message_box.show()
        else:
            image_widget = ImageWidget(
                image_path=self.gif_image_path,
                opacity=float(self.opacity_slider.value()) / 100
            )
            self.image_widget_list.append(image_widget)
            image_widget.showMaximized()

    def choose_and_copy_file_to_cwd_image_dir_then_play(self):
        file_path = QFileDialog().getOpenFileName(
            parent=self,
            dir=os.getcwd(),
            filter="Images (*.png;*.jpg;*.webp)"
        )[0]
        file_path = Path(file_path)
        if file_path.is_file() and file_path.exists():
            image_path = Path(str(Path.cwd()) + "/image")
            if not image_path.exists() or not image_path.is_dir():
                image_path.mkdir(parents=True, exist_ok=True)
            if file_path.suffix.lower() in [
                ".png", ".jpg", ".webp"
            ]:
                try:
                    self.gif_image_path = shutil.copy(file_path, image_path)
                except shutil.SameFileError:
                    self.gif_image_path = str(Path(f"{image_path}/{file_path.name}"))
                self.ready_label.setText("Ready")
            else:
                message_box = QMessageBox(self)
                message_box.setText("Please choose a Image")
                message_box.show()

    def opacity_trick(self):
        self.opacity_slider_value_label.setText(str(self.opacity_slider.value()))
