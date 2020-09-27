#LIBRARY GUI
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#LIBRARY ESENSIAL
import numpy as np
import os
import sys
import logging
import threading
import cv2

#LIBRARY CUSTOM
import utils

<<<<<<< HEAD
=======
global isAkuisisi
global usedDevice
global changeDevice

URL = "http://192.168.1.18:8080/video?type=some.mjpeg"
>>>>>>> parent of 02d5a25... Fix bug freeze saat IP tidak ditemukan
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    print('INSIDE THREAD')

    def run(self):
<<<<<<< HEAD
        print('INSIDE THREAD')
        global usedDevice
        global isTakingImage
        video_capture = cv2.VideoCapture(usedDevice)
        while True:
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
                if(isTakingImage):
                    print('IM TAKING PICTURE')
                    isTakingImage = False
                    break
=======
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
>>>>>>> parent of 02d5a25... Fix bug freeze saat IP tidak ditemukan

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUiThread()

    @pyqtSlot(QImage)
<<<<<<< HEAD
    def takeVideo(self, image):
        self.akuisisiImage.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def takePicture(self, image):
        self.pictureLabel.setPixmap(QPixmap.fromImage(image))
=======
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
>>>>>>> parent of 02d5a25... Fix bug freeze saat IP tidak ditemukan

    def initUiThread(self):
        #VARIABEL YANG DIBUTUHKAN UNTUK AKUISISI : KAMERA DEVICES
        retrieved_devices = utils.returnCameraIndexes()

        self._want_to_close = False

        self.citraGroup = QGroupBox("Citra Didapatkan")

        #LAYOUT UTAMA VERTIKAL
        mainlayout = QHBoxLayout()

        #MAIN LAYOUT TERDAPAT 3 KOLOM
        columnLeft = QVBoxLayout()
        columnCenter = QVBoxLayout()
        columnRight = QVBoxLayout()

        #SUB LAYOUT COLUMN LEFT
        columnLeftRow1 = QHBoxLayout()
        columnLeftRow2 = QHBoxLayout()

        #SUB LAYOUT COLUMN CENTER
        columnCenterRow1 = QHBoxLayout()
        columnCenterRow2 = QHBoxLayout()

        #SUB LAYOUT COLUMN RIGHT
        #BELUM DIBUAT. TUNGGU SAMPE DIMINTA BUAT FEATURE EXTRACTION


        #ISI DARI SUB LAYOUT COLUMN LEFT ROW 1 : VIDEO ATAU GAMBAR AKUISISI
        #LANGSUNG AJA ISIIN GAMBAR AKUISISINYA
        akuisisiImageGroup = QGroupBox()
        self.akuisisiImage = QLabel(self)
        columnLeftRow1.addWidget(self.akuisisiImage)
        #GABUNGKAN LAYOUT JIKA SEMUA WIDGET SUDAH TERDEFINISI
        akuisisiImageGroup.setLayout(columnLeftRow1)

        #ISI DARI SUB LAYOUT COLUMN LEFT ROW 2 : MENU AKUISISI
        columnLeftRow2Col1 = QVBoxLayout()
        columnLeftRow2Col2 = QVBoxLayout()

        #ISI DARI SUB SUB LAYOUT COLUMN LEFT ROW 2 COL 1 : MENU AKUISISI DARI DEVICE
        columnLeftRow2Col1Row1 = QHBoxLayout()

        #SUB NYA : COLUMN 1 -> RADIO BUTTON MEMILIH DEVICE
        columnLeftRow2Col1Row1Col1 = QVBoxLayout()
        #radio button untuk milih opsi akuisisi dari internal device
        self.selectDeviceRadioBtn1 = QRadioButton()
        self.selectDeviceRadioBtn1.toggled.connect(self.changeDeviceToInternal)
        #radio button untuk milih opsi akuisisi dari IP
        self.selectDeviceRadioBtn2 = QRadioButton()
        self.selectDeviceRadioBtn2.toggled.connect(self.changeDeviceToIp)
        #GABUNGKAN
        columnLeftRow2Col1Row1Col1.addWidget(self.selectDeviceRadioBtn1)
        columnLeftRow2Col1Row1Col1.addWidget(self.selectDeviceRadioBtn2)

        #SUB NYA : COLUMN 2 -> COMBOBOX DAN FORM INPUT IP
        columnLeftRow2Col1Row1Col2 = QVBoxLayout()
        #Combobox untuk pilih device
        self.akuisisiCombo = QComboBox()
        #SET VALUE COMBOBOX DENGAN DEVICE INTERNAL YANG SUDAH DIBACA
        for i in range(3):
            self.currentDevice = 0
            self.akuisisiCombo.addItem("KAMERA"+str(i+1))
        #Listener Combobox
        self.akuisisiCombo.currentIndexChanged.connect(self.akuisisiSelectionChange)
        #Form untuk insert alamat IP
        self.formAkuisisiIP = QLineEdit("192.168.1.2:8080")
<<<<<<< HEAD
        #GABUNGKAN
        columnLeftRow2Col1Row1Col2.addWidget(self.akuisisiCombo)
        columnLeftRow2Col1Row1Col2.addWidget(self.formAkuisisiIP)

        #SUB NYA : COLUMN 3 -> BUTTON AKUISISI DAN AMBIL GAMBAR
        columnLeftRow2Col1Row1Col3 = QVBoxLayout()
        #BUTTON BUTTON
        self.mulaiAkuisisiButton = QPushButton("MULAI AKUISISI")
        self.mulaiAkuisisiButton.clicked.connect(self.mulaiAkuisisiCitra)
        self.akuisisiGambarButton = QPushButton("AMBIL GAMBAR")
        self.akuisisiGambarButton.clicked.connect(self.mulaiAmbilGambar)
        #GABUNGKAN
        columnLeftRow2Col1Row1Col3.addWidget(self.mulaiAkuisisiButton)
        columnLeftRow2Col1Row1Col3.addWidget(self.akuisisiGambarButton)
        #GABUNGKAN DENGAN PARENT
        columnLeftRow2Col1Row1.addLayout(columnLeftRow2Col1Row1Col1)
        columnLeftRow2Col1Row1.addLayout(columnLeftRow2Col1Row1Col2)
        columnLeftRow2Col1Row1.addLayout(columnLeftRow2Col1Row1Col3)
        columnLeftRow2Col1.addLayout(columnLeftRow2Col1Row1)

        #ISI DARI SUB SUB LAYOUT COLUMN LEFT ROW 2 COL 2 : MENU AKUISISI DARI GAMBAR TERAKUISIS
        #LANGSUNG AJA ISIIN BUTTON, KARENA LAYOUT SUDAH VERTIKAL DAN HANYA BUTUH 1 COLUMN
        self.pilihGambarAkuisisiButton = QPushButton("PILIH GAMBAR")
        self.simpanGambarAkuisisiButton = QPushButton("SIMPAN GAMBAR")
        #GABUNGKAN
        columnLeftRow2Col2.addWidget(self.pilihGambarAkuisisiButton)
        columnLeftRow2Col2.addWidget(self.simpanGambarAkuisisiButton)
        #GABUNGKAN DENGAN PARENT
        columnLeftRow2.addLayout(columnLeftRow2Col1)
        columnLeftRow2.addLayout(columnLeftRow2Col2)
        columnLeft.addLayout(columnLeftRow1)
        columnLeft.addLayout(columnLeftRow2)

        #LAYOUT-LAYOUT LAINNYA DISINI

        #JIKA SEMUA SUDAH DIDEFINISIKAN, GABUNGKAN DENGAN MAIN LAYOUT
        mainlayout.addLayout(columnLeft)
        mainlayout.addLayout(columnCenter)
        mainlayout.addLayout(columnRight)
=======
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
>>>>>>> parent of 02d5a25... Fix bug freeze saat IP tidak ditemukan

        container = QWidget()
        container.setLayout(mainlayout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.path = None

<<<<<<< HEAD
        self.update_title()

        #INIT THREAD UNTUK AKUISISI CITRA
        self.videoThread = Thread(self)
        self.videoThread.changePixmap.connect(self.takeVideo)

=======
        self.label = QLabel(self)
        vlayout_h_t_2.addWidget(self.label)
        hlayout_t.addLayout(vlayout_h_t_2)

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
>>>>>>> parent of 02d5a25... Fix bug freeze saat IP tidak ditemukan
        self.show()

    def akuisisiSelectionChange(self,i):
        global usedDevice
        self.currentDevice = i
        print('SELECTION CHANGED TO : ',self.currentDevice)
        if(self.selectDeviceRadioBtn1.isChecked()):
            usedDevice = self.currentDevice
            print('DEVICE USED IS : ',usedDevice)

    def mulaiAkuisisiCitra(self):
        global isTakingImage
        isTakingImage = False
        self.videoThread.start()

    def mulaiAmbilGambar(self):
        global isTakingImage
        isTakingImage = True

    def changeDeviceToInternal(self):
        global usedDevice
<<<<<<< HEAD
        if(self.selectDeviceRadioBtn1.isChecked()):
            usedDevice = self.currentDevice
            print('DEVICE USED IS : ',usedDevice)
=======
        global changeDevice
        usedDevice = self.currentDevice
        print('DEVICE USED IS : ',usedDevice)
        changeDevice = True
        isAkuisisi = False
>>>>>>> parent of 02d5a25... Fix bug freeze saat IP tidak ditemukan

    def changeDeviceToIp(self):
        global usedDevice
<<<<<<< HEAD
        if(self.selectDeviceRadioBtn2.isChecked()):
            device = self.formAkuisisiIP.text()
            usedDevice = "http://"+device+"/video?type=some.mjpeg"
            print('DEVICE USED IS : ', usedDevice)
=======
        global changeDevice
        device = self.formAkuisisiIP.text()
        usedDevice = "http://"+device+"/video?type=some.mjpeg"
        print('DEVICE USED IS : ', usedDevice)
        changeDevice = True
        isAkuisisi = False
>>>>>>> parent of 02d5a25... Fix bug freeze saat IP tidak ditemukan

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

