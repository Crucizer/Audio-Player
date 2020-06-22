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

        # layout = QtWidgets.QHBoxLayout(self)

        # layout = QtWidgets.QVBoxLayout(self)
        #
        # mywidget = QtWidgets.QListWidget()
        # mywidget.setAlternatingRowColors(True)
        # mywidget.setDragDropMode(
        #     QtWidgets.QAbstractItemView.InternalMove
        # )
        # mywidget.addItems([str(i) for i in range(1, 6)])
        # layout.addWidget(mywidget)
        #
        # mywidget.show()

        # DELETE THIS------------------DELETE THIS-------------------------------------DELETE THIS
        # self.layout = QtWidgets.QVBoxLayout(self)
        # self.widget = QtWidgets.QListWidget()
        # self.widget.setAlternatingRowColors(True)
        # self.widget.setDragDropMode(
        #     QtWidgets.QAbstractItemView.InternalMove)
        #
        # self.widget.addItems([str(i) for i in range(1, 6)])
        # self.layout.addWidget(self.widget)
        # self.widget.show()
        # em = ["hey", "there", "delihah"]
        # QtWidgets.QListWidget.addItem("hey", self)

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

        # self.m_time = pg.mixer.music.get_pos()
        # self.mm_time = self.m_time * 0.001
        # self.s_time = self.mm_time // 1
        # self.slider.setValue(self.s_time)
        # print(self.s_time)

        self.flag = 0

        self.home()

    def home(self):

        # colors
        black = (13, 13, 13)
        light_black = (36, 36, 36)

        # Gif

        # self.gif = QtWidgets.QLabel(self)
        # self.gif.setPixmap(QPixmap('music_bars'))
        # self.gif.setGeometry(0, 100, 100, 150)
        # layout = QtWidgets.QHBoxLayout
        #
        # delete_button = QtWidgets.QPushButton("Hey")
        # layout.addWidget(delete_button)

        # self.setLayout(layout)

        # Pause Button
        self.pause_btn = QtWidgets.QPushButton(self)
        self.pause_btn.setText("Pause")
        self.pause_btn.setShortcut("p")
        self.pause_btn.move(0, 120)
        self.pause_btn.clicked.connect(self.pause)
        #self.pause_btn.setStyleSheet("background-color: %s" % light_black)

        # Play Button
        self.play_btn = QtWidgets.QPushButton(self)
        self.play_btn.setText("Play")
        self.play_btn.setShortcut("Space")
        self.play_btn.move(150, 120)
        self.play_btn.clicked.connect(self.play)
        #self.play_btn.setStyleSheet("background-color: %s" % light_black)

        # Stop Button
        self.stop_btn = QtWidgets.QPushButton(self)
        self.stop_btn.setText("Stop")
        self.stop_btn.setShortcut("s")
        self.stop_btn.move(300, 120)
        # self.stop_btn.setStyleSheet("background-color: %s" % light_black)

        self.stop_btn.clicked.connect(self.stop)
        # color for the window

        # color = QColor(200, 220, 240)
        color = QColor(70, 70, 70)
        # self.setStyleSheet("QWidget { background-color: %s}" % color)
        # self.setStyleSheet("background-color: %s;" % color)

        # palette = self.palette()
        # role = self.backgroundRole()
        # palette.setColor(role, color)
        # self.setPalette(palette)

        # palette = self.palette()
        # role = self.backgroundRole()
        # palette.setColor(role, QColor('green'))
        # self.setPalette(palette)

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
        # self.v_slider.valueChanged.connect(self.slider_value_changed)
        # print(self.v_slider.value() / 100)
        

    def msg(self, title, message):
        msg1 = QtWidgets.QMessageBox()  # self maybe
        msg1.setWindowIcon(QtGui.QIcon("icon"))
        msg1.setWindowTitle(title)
        msg1.setText(message)
        msg1.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg1.exec_()

    def open_mp3(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self)
        # if name == None:
        #     print("hello")
        # else:
        # print(name[0])

        # import wave
        # import contextlib
        # with contextlib.closing(wave.open(name, 'r')) as f:
        #     frames = f.getnframes()
        #     rate = f.getframerate()
        #     length = frames / float(rate)
        #     print(length)

        format = os.path.splitext(name[0])
        if format[1] == ".mp3":

            # if format[0] == ".mp3":
            self.audio = MP3(name[0])
            self.duration = self.audio.info.length // 1
            # print(self.duration)

            self.min = int(self.duration // 60)
            self.sec = int(self.duration % 60)

            self.total_time = str(self.min) + ":" + str(self.sec)
            # print(self.total_time)

            self.slider.setMaximum(self.duration)
            self.slider.setMinimum(0)
            # self.slider.valueChanged.connect(self.seek_changed)
            # time = []
            # time.append(self.total_time)
            self.label = QtWidgets.QLabel(self)
            self.label.setText(self.total_time)
            self.label.setFont(QtGui.QFont("Arial", 9))
            self.label.adjustSize()
            self.label.move(373, 77)
            # palette = self.palette()
            # role = self.backgroundRole()
            # palette.setColor(role, QColor('green'))
            # self.setPalette(palette)
            self.label.show()
            # self.time[-1].setParent(None)
            # self.time.pop(-1)

            # else:

            song = name[0]
            pg.mixer.music.load(song)
            pg.mixer.music.play(1)
            pg.mixer.music.set_volume(self.v_slider.value() / 100)
            # print(pg.mixer.music.get_pos())

            self.label = QtWidgets.QLabel(self)
            self.label.setText(song)
            self.label.setFont(QtGui.QFont("Arial", 15))
            self.label.adjustSize()
            self.label.move(0, 36)
            self.label.show()

            # if self.s_time > 0:
            #     self.cur_time()
            # self.cur_time()

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
                # if self.slider.value != self.s_time:
                #     self.slider.valueChanged.connect(self.seek_changed())
                self.slider.setValue(self.s_time)
                # self.hey = "hey"
                print(self.s_time)
                # self.slider.sliderMoved.connect(self.seek_changed)
                # self.slider.slider
                # self.slider.valueChanged.connect(self.seek_changed)
                # if self.s_time != self.slider.value:
                #     self.slider.value.connect(self.seek_changed)

            if self.s_time == -1:
                # self.slider.setValue(0)
                true = 2

            # if self.flag == 1:
                # print(self.s_time)
            # if self.flag != 1:
            #     self.m_time = pg.mixer.music.get_pos()
            #     self.mm_time = self.m_time * 0.001
            #     self.s_time = self.mm_time // 1
            #     self.slider.setValue(self.s_time)
            #     slider_value = self.slider.ge
            #     # self.hey = "hey"
            #     print(self.s_time)

        # self.slider.setValue(self.s_time)
        # while self.s_time >= self.duration:
        #     print(self.s_time)


# ---------------X---------------------X-------------------------X------------------------------X-------X
        # while True:
        #     print("hey")

        # self.m_time = pg.mixer.music.get_pos()
        # self.mm_time = self.m_time * 0.001
        # self.s_time = self.mm_time // 1
        #
        # print(self.s_time)

    # def seek_changed(self):
    #     # first you gotta move the slider and then come back to this
    #     print(self.slider.value())
    #     pg.mixer.music.set_pos(self.slider.value())

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
        #self.v_slider.value() - 10
        # print(self.volume_value)
        self.v_slider.setValue(self.volume_value)

        # DELETE THIS---------------------X------------------------X---------------------------X------------X
        # self.m_time = pg.mixer.music.get_pos()
        # self.mm_time = self.m_time * 0.001
        # self.s_time = self.mm_time // 1
        # self.slider.setValue(self.s_time)
        # print(self.s_time)

        if self.volume_value <= 0:
            self.volume_value = 0

        # if self.sound < 0:
        #     self.sound = 0
        # pg.mixer.music.set_volume(self.sound)

        # self.sound = self.volume_value/10
        # if self.sound < 0:
        #     self.sound = 0
        # if self.sound > 1:
        #     self.sound = 1
        pg.mixer.music.set_volume(self.v_slider.value() / 100)
        # print(self.v_slider.value() / 100)

    def pause(self):
        pg.mixer.music.pause()
        self.flag = 1

    def stop(self):
        pg.mixer.music.stop()
        self.flag = -1

    def play(self):
        # try:
        #     pause
        # except NameError:
        #     pg.mixer.music.unpause()

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


#
# def main_():
#     app = QApplication(sys.argv)
#     win = window()
#     win.show()
#     sys.exit(app.exec_())
#
#
# main_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

    # app = QApplication(sys.argv)
    # win = window()
    # win.show()
    # sys.exit(app.exec_())
