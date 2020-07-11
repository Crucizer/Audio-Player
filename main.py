from PyQt5 import QtWidgets, QtGui
# , QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtGui import QColor  # , QMovie
from PyQt5.QtCore import Qt
import sys
import pygame as pg
from mutagen.mp3 import MP3
import os
import threading

pg.init()


class window(QMainWindow):
    def __init__(self):

        super(window, self).__init__()
        self.setGeometry(425, 65, 400, 190)
        self.setWindowIcon(QtGui.QIcon("icon"))
        self.setWindowTitle("MultiMedia Player")
        # MenuBar
        file = QtWidgets.QAction("&Open Mp3", self)
        file.setShortcut("Ctrl + O")
        file.triggered.connect(self.open_mp3)

        # Quit
        quit = QtWidgets.QAction("&Quit", self)
        quit.setShortcut("Ctrl + Q")
        quit.triggered.connect(self.close_app)

        # Add Items

        items = QtWidgets.QAction("&Add Items", self)
        items.setShortcut("Ctrl + A")
        # items.triggered.connect(self.items)

        mainmenu = self.menuBar()
        filemenu = mainmenu.addMenu("&Open")
        filemenu.addAction(file)
        add_items = mainmenu.addMenu("&Add Items")
        add_items.addAction(items)
        filemenu.addAction(quit)


        self.flag = 0

        self.home()

    def home(self):

        # colors
        black = (13, 13, 13)
        light_black = (36, 36, 36)

        # Pause Button
        self.pause_btn = QtWidgets.QPushButton(self)
        self.pause_btn.setText("Pause")
        self.pause_btn.setShortcut("p")
        self.pause_btn.move(0, 120)
        self.pause_btn.clicked.connect(self.pause)

        # Play Button
        self.play_btn = QtWidgets.QPushButton(self)
        self.play_btn.setText("Play")
        self.play_btn.setShortcut("Space")
        self.play_btn.move(150, 120)
        self.play_btn.clicked.connect(self.play)
        # Stop Button
        self.stop_btn = QtWidgets.QPushButton(self)
        self.stop_btn.setText("Stop")
        self.stop_btn.setShortcut("s")
        self.stop_btn.move(300, 120)

        self.stop_btn.clicked.connect(self.stop)
        # color for the window
        color = QColor(70, 70, 70)
        # Volume_Up Button
        self.vup_btn = QtWidgets.QPushButton(self)
        self.vup_btn.setText("V(+)")
        self.vup_btn.setShortcut("+")
        self.vup_btn.move(300, 160)
        self.vup_btn.clicked.connect(self.volume_up)

        # Volume_Down Button
        self.vdown_btn = QtWidgets.QPushButton(self)
        self.vdown_btn.setText("V(-)")
        self.vdown_btn.setShortcut("-")
        self.vdown_btn.move(0, 160)
        self.vdown_btn.clicked.connect(self.volume_down)

        # Seek Slider

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(20, 75, 350, 20)

        # Volume Slider

        self.v_slider = QSlider(Qt.Horizontal, self)
        self.v_slider.setGeometry(120, 165, 160, 20)
        self.v_slider.setMinimum(0)
        self.v_slider.setMaximum(100)
        self.v_slider.setValue(70)
        self.volume_value = self.v_slider.value()

    def msg(self, title, message):
        msg1 = QtWidgets.QMessageBox()  # self maybe
        msg1.setWindowIcon(QtGui.QIcon("icon"))
        msg1.setWindowTitle(title)
        msg1.setText(message)
        msg1.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg1.exec_()

    def open_mp3(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self)

        format = os.path.splitext(name[0])
        if format[1] == ".mp3":

            self.audio = MP3(name[0])
            self.duration = self.audio.info.length // 1

            self.min = int(self.duration // 60)
            self.sec = int(self.duration % 60)

            self.total_time = str(self.min) + ":" + str(self.sec)

            self.slider.setMaximum(self.duration)
            self.slider.setMinimum(0)
            self.label = QtWidgets.QLabel(self)
            self.label.setText(self.total_time)
            self.label.setFont(QtGui.QFont("Arial", 9))
            self.label.adjustSize()
            self.label.move(373, 77)
            self.label.show()

            song = name[0]
            pg.mixer.music.load(song)
            pg.mixer.music.play(1)
            pg.mixer.music.set_volume(self.v_slider.value() / 100)

            self.label = QtWidgets.QLabel(self)
            self.label.setText(song.split("/")[-1])
            self.label.setFont(QtGui.QFont("Arial", 15))
            self.label.adjustSize()
            self.label.move(0, 36)
            self.label.show()
            threading_1 = threading.Thread(target=self.cur_time).start()

        else:
            self.msg("Invalid Format", "Choose A .Mp3 File Only!")

    volume_level = pg.mixer.music.get_volume()
    # print(volume_level)

    def cur_time(self):

        # NEEDS EDITING-----NEEDS EDITING-----NEEDS EDITING-----NEEDS EDITING-----NEEDS EDITING-----NEEDS EDITING
        true = 1
        while true == 1:
            if self.flag == 0:
                self.m_time = pg.mixer.music.get_pos()
                self.mm_time = self.m_time * 0.001
                self.s_time = self.mm_time // 1
                self.slider.setValue(self.s_time)
            if self.s_time == -1:
                true = 2

    def slider_value_changed(self):
        self.volume_value = self.v_slider.value()
        pg.mixer.music.set_volume(self.v_slider.value() / 100)

    def volume_up(self):
        #self.v_slider.value() - 10
        self.volume_value = self.volume_value + 10
        # print(self.volume_value)
        self.v_slider.setValue(self.volume_value)

        if self.volume_value >= 100:
            self.volume_value = 100

        # pg.mixer.music.set_volume(self.sound)
        pg.mixer.music.set_volume(self.v_slider.value() / 100)
        # print(self.v_slider.value() / 100)

    def volume_down(self):
        self.volume_value = self.volume_value - 10
        self.v_slider.setValue(self.volume_value)

        if self.volume_value <= 0:
            self.volume_value = 0

        pg.mixer.music.set_volume(self.v_slider.value() / 100)
        # print(self.v_slider.value() / 100)

    def pause(self):
        pg.mixer.music.pause()
        self.flag = 1

    def stop(self):
        pg.mixer.music.stop()
        self.flag = -1

    def play(self):
        pg.mixer.music.unpause()
        self.flag = 0

    def close_app(self):
        choice = QtWidgets.QMessageBox.question(
            self, "QUIT", "You Sure You Wanna Quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def items(self):
        # add item name to a list and then use this to add
        layout = QtWidgets.QVBoxLayout(self)
        song_name = QtWidgets.QFileDialog.getOpenFileName(self)

        widget = QtWidgets.QListWidget()
        widget.setAlternatingRowColors(True)
        widget.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove)

        widget.addItems([str(i) for i in range(1, 6)])
        layout.addWidget(widget)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())
