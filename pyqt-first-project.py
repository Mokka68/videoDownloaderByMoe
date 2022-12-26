from threading import Thread
from PyQt5.QtWidgets import QWidget
import sys
import pytube

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QLineEdit, QVBoxLayout, QPushButton, QTextEdit


# use QColor.colorNames() to print out the colors strings 
def set_widget_color(widget, color):
    palette = widget.palette()
    palette.setColor(QPalette.Window, QColor(color))
    widget.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Youtube Downloader By Mo")
        self.resize(600, 300)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter the Youtube link here")
        self.input.setStyleSheet("""
               background-color: #262626;
            color: #FFFFFF;
            font-family: Titillium;
            font-size: 18px;
            """)

        self.button = QPushButton()
        self.button.setText("Download")
        self.button.setStyleSheet("""
            background-color: #262626;
            color: #FFFFFF;
            font-family: Titillium;
            font-size: 18px;
            """)

        self.output = QTextEdit()
        self.output.setText("YouTube downloader Ready!")
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color:slategray;")

        self.button.clicked.connect(self.download_video)

        layout = QVBoxLayout()
        layout.setSpacing(50)

        layout.addWidget(self.input)
        layout.addWidget(self.button, 1)
        self.setCentralWidget(self.output)

        container = QWidget()
        container.setStyleSheet("background-color:gray;")
        container.setLayout(layout)

        self.setMenuWidget(container)

    def download_video(self):
        self.output.setText("Downloading...")
        QApplication.processEvents()
        url = self.input.text()

        if not url:
            self.output.setText(f"URL Field is empty")
            return

        try:
            yt = pytube.YouTube(url)
        except Exception as error:
            self.output.setText(f"URL is not valid!\n{error}")
            return
        try:
            yt_object = yt.streams.get_highest_resolution()
        except Exception as error:
            self.output.setText(f"could not get the required resolution of the video\n{error}")
            return
        try:
            yt_object.download('./videos')
        except Exception as error:
            self.output.setText(f"ERROR: could not download the video\n{error}")
            return
        else:
            self.output.setText("Video is downloaded")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
