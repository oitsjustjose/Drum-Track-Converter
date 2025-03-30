import platform
import subprocess
import sys
from pathlib import Path
from typing import Callable, List

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.music_file import MODEL_CHOICES

APP_ID = "com.oitsjustjose.drum-track-converter"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Actual used data
        self.input_dir: str = ""
        self.output_dir: str = ""
        self.model_name: str = list(MODEL_CHOICES.values())[0]
        # The subprocess used for the internal call to cli.py
        self.__child_proc: subprocess.Popen = None

        # Widgets that we'll want to set & mutate throughout the runtime
        self.start_button: QPushButton = None
        self.interactive_elements: List[QWidget] = list()

        self.setWindowTitle("Drum Track Converter by oitsjustjose")
        self.__setup_layout()
        self.__center()
        # Set fixed size only once we've established the contents of the window
        self.setMaximumSize(self.size())

    def on_input_clicked(self, button_ref: QPushButton):
        """Sets the output directory to the selected value from a QFileDialog
            Mutates the button_ref's text to reflect the selected folder
            If Input and Output are set, enables the Start button

        Args:
            button_ref (QPushButton): A reference to the button pressed
        """
        self.input_dir = QFileDialog.getExistingDirectory(None, "Select Input Folder")
        self.__common_io_clicked(button_ref, self.input_dir)

    def on_output_clicked(self, button_ref: QPushButton):
        """Sets the output directory to the selected value from a QFileDialog
            Mutates the button_ref's text to reflect the selected folder
            If Input and Output are set, enables the Start button

        Args:
            button_ref (QPushButton): A reference to the button pressed
        """
        self.output_dir = QFileDialog.getExistingDirectory(None, "Select Output Folder")
        self.__common_io_clicked(button_ref, self.output_dir)

    def on_model_changed(self, model_display_name: str) -> None:
        """Sets the model_name to the new model_name based on the display name

        Args:
            model_display_name (str): The display name of the model
        """
        self.model_name = MODEL_CHOICES[model_display_name]

    def on_start_clicked(self):
        """Passes through basic assertions, spins up thread to process files from the input and output params"""
        if not (self.input_dir and self.output_dir):
            return

        # Since wait() is blocking, hide the main window so that the user doesn't get confused by it looking forzen
        self.setHidden(True)
        [x.setEnabled(False) for x in self.interactive_elements]

        prefix = "start /wait" if platform.system() == "Windows" else ""
        command = f"{prefix} {sys.executable} -m src.cli {self.input_dir} {self.output_dir} -m {self.model_name}"
        self.__child_proc = subprocess.Popen(command.split(" "), shell=True)
        self.__child_proc.wait()

        # Re-enable elements now that everything is done
        self.setHidden(False)
        [x.setEnabled(True) for x in self.interactive_elements]

    def stop(self):
        """Stops the working thread (if it's been started) at its soonest convenience..."""
        if self.__child_proc:
            self.__child_proc.kill()

    """~~Hidden / private methods~~"""

    def __center(self) -> None:
        """Centers the window to the middle of the Screen"""
        frame_geo = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        frame_geo.moveCenter(center)
        self.move(frame_geo.topLeft())

    def __setup_layout(self):
        """Sets up the main layout of the window, including children"""
        self.layout = QVBoxLayout()
        self.__setup_children()
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def __setup_children(self):
        """Sets up the children of the main window element using [nested] HBox and VBox layouts"""
        # Start Button gets manually defined since its contents are changed
        self.start_button = QPushButton("Start")
        self.start_button.setEnabled(False)
        self.start_button.adjustSize()
        self.start_button.clicked.connect(self.on_start_clicked)

        # These should stay in the same order as intended visually, so smaller index = closer to top.
        #   These elements will all be disabled/enabled as the process starts & stops
        self.interactive_elements = [
            self.__make_io_buttons(),
            self.__make_model_combobox(),
            self.start_button,
        ]

        [self.layout.addWidget(x) for x in self.interactive_elements]

    def __make_io_buttons(self) -> QWidget:
        """Makes the Input and Output Folder Buttons

        Returns:
            QWidget: The VBox widget created
        """

        def create_io_button_group(
            self: MainWindow, label_text: str, on_click: Callable
        ) -> QWidget:
            """Re-usable template to create an input or output button group
            This group contains a label and a clickable button, which calls the
            on_click callable passed in when clicked.

            Args:
                self (MainWindow): The parent object
                label_text (str): The label to place above the text
                on_click (Callable): The method to fire when the included button is clicked

            Returns:
                QWidget: _description_
            """
            vbox = QWidget()
            layout = QVBoxLayout()

            label = self.__create_label(label_text)
            button = QPushButton("Choose Folder...")
            button.clicked.connect(lambda: on_click(button))

            layout.addWidget(label)
            layout.addWidget(button)

            vbox.setLayout(layout)
            return vbox

        # Input and Output directory items
        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(
            create_io_button_group(self, "Select Input Folder", self.on_input_clicked)
        )
        layout.addWidget(
            create_io_button_group(self, "Select Output Folder", self.on_output_clicked)
        )
        widget.setLayout(layout)
        return widget

    def __make_model_combobox(self) -> QWidget:
        """Makes a Combobox to choose which demucs model to use

        Returns:
            QWidget: The VBox widget created
        """
        widget = QWidget()
        layout = QHBoxLayout()

        label = self.__create_label(
            'Demucs Model <a style="text-decoration: none !important;" href="https://github.com/facebookresearch/demucs?tab=readme-ov-file#separating-tracks">ℹ️</a>'
        )
        label.setOpenExternalLinks(True)

        combo_box = QComboBox()
        combo_box.currentTextChanged.connect(self.on_model_changed)
        for model_name in MODEL_CHOICES:
            combo_box.addItem(model_name)

        layout.addWidget(label)
        layout.addWidget(combo_box)
        widget.setLayout(layout)
        return widget

    def __create_label(self, text: str) -> QLabel:
        """Creates a label in a single call that is horizontally centered and automatically sized, with the provided text and pos.

        Args:
            parent (QWidget): The parent widget
            text (str): The text to render
            pos (QPoint): The position to render the label at

        Returns:
            QLabel: The label created
        """
        label = QLabel(text)
        label.adjustSize()
        return label

    def __common_io_clicked(self, button_ref: QPushButton, path: str) -> None:
        """Performs a common set of actions for both on_input_clicked and on_output_clicked
            Mutates the button_ref's text to reflect the selected folder
            If Input and Output are set, enables the Start button

        Args:
            button_ref (QPushButton): A reference to the button pressed
            path (str): The path chosen by the click event
        """
        display_path: Path = Path(path).resolve()

        button_ref.setText(f"Set: '{display_path.stem}'")
        enabled = bool(self.input_dir and self.output_dir)
        self.start_button.setEnabled(enabled)


def main() -> None:
    """
    Creates a QApplication, main window and shows the window
      When the app is closed, the exit code is stored for sys.exit() while
      in the meantime the off-thread processing (if any) is stopped.
    """
    app = QApplication(sys.argv)

    icon = QIcon()
    icon.addFile("assets/icon.png")
    icon.addFile("assets/icon.ico")

    app.setWindowIcon(icon)
    window = MainWindow()
    window.show()
    exit_code = app.exec()
    window.stop()
    sys.exit(exit_code)


if __name__ == "__main__":
    # Set the AppUserModelId so that the proper taskbar icon renders
    if platform.system() == "Windows":
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

    main()
