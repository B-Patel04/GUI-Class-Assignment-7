# converter.py
# Student: Bhavik Patel
# Course: GUI Class
# Project: Assignment 7 (PySide6)
# Date: May 9, 2026

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, \
    QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QFrame

from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

in_to_meter_const = 0.0254


class ConverterWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Measurement Converter (PySide6)")
        self.resize(760, 400)

        self._build_ui()
        self._wire_events()
        self._reset_form()

    def _build_ui(self):

        central = QWidget(self)
        self.setCentralWidget(central)

        # title
        self.lblTitle = QLabel("Measurement Converter")
        self.lblTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        titleFont = QFont()
        titleFont.setPointSize(18)
        titleFont.setBold(True)

        self.lblTitle.setFont(titleFont)

        # Input
        self.lblPrompt = QLabel("Enter a Value:")
        self.txtInput = QLineEdit()

        self.txtInput.setPlaceholderText("Eg: 10 or 5.5")

        # Radio Button Group
        self.grp = QGroupBox("Conversion Type")

        self.rbInToM = QRadioButton("Inches to Meters")
        self.rbMToIn = QRadioButton("Meters to Inches")

        radioLayout = QHBoxLayout()
        radioLayout.addWidget(self.rbInToM)
        radioLayout.addWidget(self.rbMToIn)

        self.grp.setLayout(radioLayout)

        # Buttons
        self.btnConvert = QPushButton("Convert")
        self.btnClear = QPushButton("Clear")
        self.btnExit = QPushButton("Exit")

        # Result Label
        self.lblResult = QLabel("")
        self.lblResult.setAlignment(Qt.AlignmentFlag.AlignCenter)

        resultFont = QFont()
        resultFont.setBold(True)

        self.lblResult.setFont(resultFont)

        # Image Section
        self.imgFrame = QFrame()
        self.imgLabel = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        pix = QPixmap("house.png")

        if not pix.isNull():
            self.imgLabel.setPixmap(
                pix.scaled(400, 400, Qt.KeepAspectRatio,Qt.SmoothTransformation)
            )
        else:
            self.imgLabel.setText("Image Not Found")

        imgLayout = QVBoxLayout(self.imgFrame)
        imgLayout.addWidget(self.imgLabel)

        # Main Layout
        grid = QGridLayout(central)

        grid.setContentsMargins(20, 20, 20, 20)
        grid.setSpacing(15)

        # Title
        grid.addWidget(self.lblTitle, 0, 0, 1, 3)

        # Input
        grid.addWidget(self.lblPrompt, 1, 0)
        grid.addWidget(self.txtInput, 1, 1)

        # Radio buttons
        grid.addWidget(self.grp, 2, 0, 1, 2)

        # Result label
        grid.addWidget(self.lblResult, 3, 0, 1, 2)

        # Image
        grid.addWidget(self.imgFrame, 1, 2, 3, 1)

        # Button layout
        hbtns = QHBoxLayout()

        hbtns.addStretch()

        hbtns.addWidget(self.btnConvert)
        hbtns.addWidget(self.btnClear)
        hbtns.addWidget(self.btnExit)

        grid.addLayout(hbtns, 4, 0, 1, 3)

        # Styling / Theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #243447;
            }

            QLabel {
                color: white;
                font-size: 14px;
            }

            QGroupBox {
                color: white;
                font-size: 14px;
                border: 2px solid #4f6475;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
            }

            QRadioButton {
                color: white;
                font-size: 14px;
                padding: 4px;
            }

            QLineEdit {
                background-color: white;
                color: black;
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
            }

            QPushButton {
                background-color: #3b82f6;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }

            QFrame {
                border-radius: 8px;
                padding: 10px;
                background-color: #1b2836;
            }
        """)

    def _wire_events(self):

        self.btnConvert.clicked.connect(self.on_convert)
        self.btnClear.clicked.connect(self.on_clear)
        self.btnExit.clicked.connect(QApplication.instance().quit)

    def _reset_form(self):

        self.txtInput.clear()
        self.lblResult.clear()

        # Default radio button
        self.rbInToM.setChecked(True)

        # Return focus to input field
        self.txtInput.setFocus()

    def _error(self, message: str):

        QMessageBox.critical(self, "Error", message)

    def inches_to_meters(self, inches):

        return inches * in_to_meter_const

    def meters_to_inches(self, meters):

        return meters / in_to_meter_const

    def on_clear(self):

        self._reset_form()

    def on_convert(self):

        text = self.txtInput.text().strip()

        # Empty input validation
        if not text:
            self._error("Value entered is not numeric.")
            return

        # Numeric validation
        try:
            value = float(text)

        except ValueError:
            self._error("Value entered is not numeric.")
            return

        # Positive number validation
        if value <= 0:
            self._error("Converted value is negative.")
            return

        # Inches to meters
        if self.rbInToM.isChecked():

            meters = self.inches_to_meters(value)

            if meters < 0:
                self._error("Converted value is negative.")
                return

            self.lblResult.setText(
                f"{value:.3f} inches = {meters:.3f} meters"
            )

        # Meters to inches
        else:

            inches = self.meters_to_inches(value)

            if inches < 0:
                self._error("Converted value is negative.")
                return

            self.lblResult.setText(
                f"{value:.3f} meters = {inches:.3f} inches"
            )


def main():
    app = QApplication(sys.argv)

    window = ConverterWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
