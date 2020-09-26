#LIBRARY GUI
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *

#LIBRARY ESENSIAL
import numpy as np
import os
import sys
import logging
import threading
import cv2

#LIBRARY CUSTOM
import utils

global isAkuisisi
global usedDevice
global changeDevice

URL = "http://192.168.1.18:8080/video?type=some.mjpeg"
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    print('INSIDE THREAD')

    def run(self):
        global usedDevice
        global isAkuisisi
        global changeDevice
        usedDevice = 0
        isAkuisisi = False
        changeDevice = False
        video_capture = cv2.VideoCapture(usedDevice)
        while True:
            if(changeDevice):
                print('DEVICE CHANGED')
                video_capture = cv2.VideoCapture(usedDevice)
                changeDevice = False
                isAkuisisi = True
            elif(isAkuisisi):
                retAkuisisi, citraAkuisisi = video_capture.read()
                if retAkuisisi:
                    print('INSIDE THREAD LOOP. CITRA AKUISISI : ',citraAkuisisi)
                    rgbImage = cv2.cvtColor(citraAkuisisi, cv2.COLOR_BGR2RGB)
                    print('CONVERSION SUCCESS')
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUiThread()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUiThread(self):
        print('running thread')

        global citraAkuisisi
        global isAkuisisi

        isAkuisisi = False

        #VARIABEL YANG DIBUTUHKAN UNTUK AKUISISI : KAMERA DEVICES
        retrieved_devices = utils.returnCameraIndexes()

        # super(MainWindow, self).__init__(*args, **kwargs)
        self._want_to_close = False

        self.citraGroup = QGroupBox("Citra Didapatkan")

        #LAYOUT UTAMA VERTIKAL
        mainlayout = QVBoxLayout()

        #MAIN LAYOUT TERDAPAT 2 BARIS LAYOUT HORIZONTAL
        hlayout_t = QHBoxLayout()
        hlayout_b = QHBoxLayout()

        #SUB LAYOUT BARIS HORIZONTAL PERTAMA
        vlayout_h_t_1 = QVBoxLayout()
        vlayout_h_t_2 = QVBoxLayout()


        #Menu untuk layout baris pertama, kolom pertama

        #Fitur pertama, pilih dari mana mau akuisisi
        #Form pilih kamera usb
        vlayout_labelAkuisisiGroup = QVBoxLayout()
        vlayout_OptionAkuisisiGroup = QVBoxLayout()
        vlayout_ActionAkuisisiGroup = QVBoxLayout()
        layoutOptionsFormAkuisisiGroup = QHBoxLayout()

        akuisisiGroup = QGroupBox("Opsi Akuisisi Citra")
        vakuisisiLayout = QVBoxLayout()

        labelFormAkuisisiCombo = QLabel("INTERNAL CAMERA")
        self.akuisisiCombo = QComboBox()
        vlayout_labelAkuisisiGroup.addWidget(labelFormAkuisisiCombo)
        vlayout_OptionAkuisisiGroup.addWidget(self.akuisisiCombo)
        #SET VALUE COMBOBOX DENGAN DEVICE INTERNAL
        for i in retrieved_devices:
            self.currentDevice = 0
            self.akuisisiCombo.addItem("KAMERA"+str(i+1))
        #Listener Combobox
        self.akuisisiCombo.currentIndexChanged.connect(self.akuisisiSelectionChange)

        #Form insert alamat IP
        labelFormAkuisisiIP = QLabel("IP CAMERA")
        self.formAkuisisiIP = QLineEdit("192.168.1.2:8080")
        vlayout_labelAkuisisiGroup.addWidget(labelFormAkuisisiIP)
        vlayout_OptionAkuisisiGroup.addWidget(self.formAkuisisiIP)

        #BUTTON MEMILIH OPSI
        confirmAkuisisiIpButton = QPushButton("USE DEVICE")
        confirmAkuisisiIpButton.clicked.connect(self.changeDeviceToInternal)
        vlayout_ActionAkuisisiGroup.addWidget(confirmAkuisisiIpButton)

        confirmAkuisisiCameraButton = QPushButton("USE IP CAM")
        confirmAkuisisiCameraButton.clicked.connect(self.changeDeviceToIp)
        vlayout_ActionAkuisisiGroup.addWidget(confirmAkuisisiCameraButton)

        layoutOptionsFormAkuisisiGroup.addLayout(vlayout_labelAkuisisiGroup)
        layoutOptionsFormAkuisisiGroup.addLayout(vlayout_OptionAkuisisiGroup)
        layoutOptionsFormAkuisisiGroup.addLayout(vlayout_ActionAkuisisiGroup)


        #GABUNGIN LAYOUT
        vakuisisiLayout.addLayout(layoutOptionsFormAkuisisiGroup)
        akuisisiGroup.setLayout(vakuisisiLayout)

        #Fitur terakhir, keluar aplikasi
        menuGroup = QGroupBox("Opsi menu")
        vmenuLayout = QVBoxLayout()

        exitButton = QPushButton("Keluar")
        #LISTENER EXIT BUTTON
        exitButton.clicked.connect(self.exitConfirmation)

        vmenuLayout.addWidget(exitButton)
        menuGroup.setLayout(vmenuLayout)

        #SUSUN WIDGET-WIDGET DAN SUBLAYOUT BERURUTAN

        vlayout_h_t_1.addWidget(akuisisiGroup)
        vlayout_h_t_1.addWidget(akuisisiGroup)
        vlayout_h_t_1.addWidget(menuGroup)

        hlayout_t.addLayout(vlayout_h_t_1)

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.path = None

        mainlayout.addLayout(hlayout_t)
        mainlayout.addLayout(hlayout_b)

        container = QWidget()
        container.setLayout(mainlayout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.update_title()

        self.label = QLabel(self)
        vlayout_h_t_2.addWidget(self.label)
        hlayout_t.addLayout(vlayout_h_t_2)

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()

    def akuisisiSelectionChange(self,i):
        self.currentDevice = i
        print('SELECTION CHANGED TO : ',self.currentDevice)

    def changeDeviceToInternal(self):
        global isAkuisisi
        global usedDevice
        global changeDevice
        usedDevice = self.currentDevice
        print('DEVICE USED IS : ',usedDevice)
        changeDevice = True
        isAkuisisi = False

    def changeDeviceToIp(self):
        global isAkuisisi
        global usedDevice
        global changeDevice
        device = self.formAkuisisiIP.text()
        usedDevice = "http://"+device+"/video?type=some.mjpeg"
        print('DEVICE USED IS : ', usedDevice)
        changeDevice = True
        isAkuisisi = False

    def exitConfirmation(self):
        dlg = QMessageBox()
        dlg.setIcon(QMessageBox.Question)
        dlg.setWindowTitle("Konfirmasi")
        dlg.setText("Apakah anda yakin ingin keluar aplikasi ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setDefaultButton(QMessageBox.No)
        buttonYes = dlg.button(QMessageBox.Yes)
        buttonYes.setText("Ya")
        buttonNo = dlg.button(QMessageBox.No)
        buttonNo.setText("Tidak")
        dlg.exec_()

        if dlg.clickedButton() == buttonYes:
            self._want_to_close=True
            qApp.quit()

    def closeEvent(self, event):
        self.exitConfirmation()
        if not self._want_to_close:
            event.ignore()

    def dialog_info(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Images (*.bmp *.jpg);;All files (*.*)")
        if path:
            try:
                print(path)
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.update_title()

    def file_save(self):
        if self.originalImage.size>0:
            return self.file_saveas()
        self.dialog_critical("Buka citra terlebih dahulu sebelum menyimpan !")

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Images (*.bmp *.jpg);;All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        try:
            self.image_l.save(path)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def update_title(self):
        self.setWindowTitle("Computer Vision and Soft Computing Software")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Computer Vision and Soft Computing Software")

    window = MainWindow()
    app.exec_()

