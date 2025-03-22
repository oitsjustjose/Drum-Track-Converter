import sys
from pathlib import Path

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
)


def __make_window() -> QMainWindow:
    """Automatically creates a window centered to the current screen

    Returns:
        QMainWindow: The created and centered window
    """
    window = QMainWindow()
    window.setWindowTitle("Drum Track Converter by oitsjustjose")
    window.setFixedSize(640, 400)

    frame_geo = window.frameGeometry()
    center = window.screen().availableGeometry().center()

    frame_geo.moveCenter(center)
    window.move(frame_geo.topLeft())
    return window


def __create_label(parent: QWidget, text: str, pos: QPoint) -> QLabel:
    """Creates a label in a single call that is horizontally centered and automatically sized, with the provided text and pos.

    Args:
        parent (QWidget): The parent widget
        text (str): The text to render
        pos (QPoint): The position to render the label at

    Returns:
        QLabel: The label created
    """
    label = QLabel(text, parent, alignment=Qt.AlignmentFlag.AlignHCenter)
    label.adjustSize()
    label.move(pos)
    return label


def main() -> None:
    # Values for the actual methods called later down
    input_directory: str = ""

    app = QApplication(sys.argv)
    window = __make_window()

    __create_label(window, "Select Input Directory", QPoint(36, 20))
    input_dir_button = QPushButton("Choose Folder...", window)
    input_dir_button.move(QPoint(40, 40))

    # Event triggers start here so we can access the above variables within event handlers
    def input_dir_button_clicked() -> None:
        input_directory = QFileDialog.getExistingDirectory(None, "Select Input Folder")

        path = Path(input_directory).name
        input_dir_button.setText(path)
        input_dir_button.adjustSize()

    # Event trigger hookups
    input_dir_button.clicked.connect(input_dir_button_clicked)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
