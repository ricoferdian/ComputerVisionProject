#LIBRARY GUI
import urllib

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#LIBRARY ESENSIAL
import sys
import cv2
import imghdr

#LIBRARY CUSTOM
import utils

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    takePicture = pyqtSignal(QImage)
    def run(self):
        global usedDevice
        global video_capture
        video_capture = cv2.VideoCapture(usedDevice)
        while True:
            retAkuisisi, citraAkuisisi = video_capture.read()
            if retAkuisisi:
                rgbImage = cv2.cvtColor(citraAkuisisi, cv2.COLOR_BGR2RGB)
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
    def takeVideo(self, image):
        self.akuisisiImage.setPixmap(QPixmap.fromImage(image))

    def initUiThread(self):
        self._want_to_close = False

        #LAYOUT UTAMA VERTIKAL
        self.mainlayout = QHBoxLayout()

        #INIT COLUMN LEFT TERMASUK PENGGABUNGAN DI FUNCTION YANG DIPISAH
        self.initColumnLeftGui()
        #INIT COLUMN RIGHT TERMASUK PENGGABUNGAN DI FUNCTION YANG DIPISAH
        self.initColumnCenterGui()

        columnRight = QVBoxLayout()

        #SUB LAYOUT COLUMN RIGHT
        #BELUM DIBUAT. TUNGGU SAMPE DIMINTA BUAT FEATURE EXTRACTION

        #JIKA SEMUA SUDAH DIDEFINISIKAN, GABUNGKAN DENGAN MAIN LAYOUT
        self.mainlayout.addLayout(columnRight)

        container = QWidget()
        container.setLayout(self.mainlayout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.path = None

        self.update_title()

        #INIT THREAD UNTUK AKUISISI CITRA
        self.videoThread = Thread(self)
        self.videoThread.changePixmap.connect(self.takeVideo)
        self.show()

    def initColumnCenterGui(self):
        #COLUMN CENTER
        columnCenter = QVBoxLayout()

        #SUB LAYOUT COLUMN CENTER
        columnCenterRow1 = QHBoxLayout()
        columnCenterRow2 = QHBoxLayout()

        #ISI DARI SUB LAYOUT COLUMN CENTER ROW 1 : INFORMASI IMAGE SEPERTI PROPERTIES, DLL
        columnCenterRow1Col1 = QVBoxLayout()
        columnCenterRow1Col2 = QVBoxLayout()

        #ROW 1 : JUDUL
        columnCenterRow1Col1Row1 = QHBoxLayout()
        self.imageProperties = QLabel(self)
        columnCenterRow1Col1Row1.addWidget(self.imageProperties)

        #ROW 2 TIPE FILE
        columnCenterRow1Col1Row2 = QHBoxLayout()
        self.labelTipefile = QLabel(self)
        self.tipeFile = QLabel(self)
        columnCenterRow1Col1Row2.addWidget(self.labelTipefile)
        columnCenterRow1Col1Row2.addWidget(self.tipeFile)

        #ROW 3 RESOLUSI
        columnCenterRow1Col1Row3 = QHBoxLayout()
        self.labelResolusi = QLabel(self)
        self.resolusi = QLabel(self)
        columnCenterRow1Col1Row3.addWidget(self.labelResolusi)
        columnCenterRow1Col1Row3.addWidget(self.resolusi)

        #ROW 4 UKURAN
        columnCenterRow1Col1Row4 = QHBoxLayout()
        self.labelSize = QLabel(self)
        self.size = QLabel(self)
        columnCenterRow1Col1Row4.addWidget(self.labelSize)
        columnCenterRow1Col1Row4.addWidget(self.size)

        #ROW 1 RED
        columnCenterRow1Col2Row1 = QHBoxLayout()
        self.labelred = QLabel(self)
        self.red = QLabel(self)
        columnCenterRow1Col2Row1.addWidget(self.labelred)
        columnCenterRow1Col2Row1.addWidget(self.red)

        #ROW 2 GREEN
        columnCenterRow1Col2Row2 = QHBoxLayout()
        self.labelgreen = QLabel(self)
        self.green = QLabel(self)
        columnCenterRow1Col2Row2.addWidget(self.labelgreen)
        columnCenterRow1Col2Row2.addWidget(self.green)

        #ROW 3 BLUE
        columnCenterRow1Col2Row3 = QHBoxLayout()
        self.labelblue = QLabel(self)
        self.blue = QLabel(self)
        columnCenterRow1Col2Row3.addWidget(self.labelblue)
        columnCenterRow1Col2Row3.addWidget(self.blue)

        columnCenterRow1Col1.addLayout(columnCenterRow1Col1Row1)
        columnCenterRow1Col1.addLayout(columnCenterRow1Col1Row2)
        columnCenterRow1Col1.addLayout(columnCenterRow1Col1Row3)
        columnCenterRow1Col1.addLayout(columnCenterRow1Col1Row4)

        columnCenterRow1Col2.addLayout(columnCenterRow1Col2Row1)
        columnCenterRow1Col2.addLayout(columnCenterRow1Col2Row2)
        columnCenterRow1Col2.addLayout(columnCenterRow1Col2Row3)

        #ISI DARI SUB LAYOUT COLUMN CENTER ROW 2 : MENU PROPERTIES
        columnCenterRow2Col1 = QVBoxLayout()
        columnCenterRow2Col2 = QVBoxLayout()

        #ISI DARI SUB SUB LAYOUT COLUMN CENTER ROW 2 COL 1
        columnCenterRow2Col1Row1 = QHBoxLayout()
        columnCenterRow2Col1Row2 = QHBoxLayout()

        self.imagePropertiesButton = QPushButton("IMAGE PROPERTIES")
        self.imagePropertiesButton.clicked.connect(self.showImageProperties)
        self.imageIntensityButton = QPushButton("INTENSITY IMAGE")
        self.imageIntensityButton.clicked.connect(self.showIntensity)

        #GABUNGKAN
        columnCenterRow2Col1Row1.addWidget(self.imagePropertiesButton)
        columnCenterRow2Col1Row2.addWidget(self.imageIntensityButton)

        #GABUNGKAN DENGAN PARENT
        columnCenterRow2Col1.addLayout(columnCenterRow2Col1Row1)
        columnCenterRow2Col1.addLayout(columnCenterRow2Col1Row2)

        #GABUNGKAN DENGAN PARENT
        columnCenterRow1.addLayout(columnCenterRow1Col1)
        columnCenterRow1.addLayout(columnCenterRow1Col2)
        columnCenterRow2.addLayout(columnCenterRow2Col1)
        columnCenterRow2.addLayout(columnCenterRow2Col2)
        columnCenter.addLayout(columnCenterRow1)
        columnCenter.addLayout(columnCenterRow2)

        self.mainlayout.addLayout(columnCenter)


    def initColumnLeftGui(self):
        #VARIABEL YANG DIBUTUHKAN UNTUK AKUISISI : KAMERA DEVICES
        retrieved_devices = utils.returnCameraIndexes()

        #MAIN LAYOUT TERDAPAT 3 KOLOM
        columnLeft = QVBoxLayout()

        #SUB LAYOUT COLUMN LEFT
        columnLeftRow1 = QHBoxLayout()
        columnLeftRow2 = QHBoxLayout()
        #ISI DARI SUB LAYOUT COLUMN LEFT ROW 1 : VIDEO ATAU GAMBAR AKUISISI
        #LANGSUNG AJA ISIIN GAMBAR AKUISISINYA
        akuisisiImageGroup = QGroupBox()
        self.akuisisiImage = QLabel(self)
        columnLeftRow1.addWidget(self.akuisisiImage)

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
        for i in retrieved_devices:
            self.currentDevice = 0
            self.akuisisiCombo.addItem("KAMERA"+str(i+1))
        #Listener Combobox
        self.akuisisiCombo.currentIndexChanged.connect(self.akuisisiSelectionChange)
        #Form untuk insert alamat IP
        self.formAkuisisiIP = QLineEdit("192.168.1.2:8080")
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
        self.pilihGambarAkuisisiButton.clicked.connect(self.file_open)
        self.simpanGambarAkuisisiButton = QPushButton("SIMPAN GAMBAR")
        self.simpanGambarAkuisisiButton.clicked.connect(self.file_save)
        #GABUNGKAN
        columnLeftRow2Col2.addWidget(self.pilihGambarAkuisisiButton)
        columnLeftRow2Col2.addWidget(self.simpanGambarAkuisisiButton)
        #GABUNGKAN DENGAN PARENT
        columnLeftRow2.addLayout(columnLeftRow2Col1)
        columnLeftRow2.addLayout(columnLeftRow2Col2)
        columnLeft.addLayout(columnLeftRow1)
        columnLeft.addLayout(columnLeftRow2)

        self.mainlayout.addLayout(columnLeft)


    def akuisisiSelectionChange(self,i):
        global usedDevice
        self.currentDevice = i
        print('SELECTION CHANGED TO : ',self.currentDevice)
        if(self.selectDeviceRadioBtn1.isChecked()):
            usedDevice = self.currentDevice
            print('DEVICE USED IS : ',usedDevice)

    def mulaiAkuisisiCitra(self):
        global usedDevice
        if(self.selectDeviceRadioBtn2.isChecked()):
            device = self.formAkuisisiIP.text()
            usedDevice = "http://"+device+"/video?type=some.mjpeg"
            print('DEVICE USED ISSSSSS : ', usedDevice)
        self.videoThread.terminate()
        if(self.selectDeviceRadioBtn2.isChecked() or self.selectDeviceRadioBtn1.isChecked()):
            if(self.selectDeviceRadioBtn2.isChecked()):
                device = self.formAkuisisiIP.text()
                usedDevice = "http://"+device+"/video?type=some.mjpeg"
            self.videoThread.start()
        else:
            self.dialog_critical("Silahkan pilih opsi perangkat akuisisi citra !")
        self.videoThread.start()

    def mulaiAmbilGambar(self):
        self.videoThread.terminate()
        global img, typeFile
        img = self.akuisisiImage.pixmap().toImage()
        print('img',img)

    def changeDeviceToInternal(self):
        global usedDevice
        if(self.selectDeviceRadioBtn1.isChecked()):
            usedDevice = self.currentDevice
            print('DEVICE USED IS : ',usedDevice)

    def changeDeviceToIp(self):
        global usedDevice
        if(self.selectDeviceRadioBtn2.isChecked()):
            device = self.formAkuisisiIP.text()
            usedDevice = "http://"+device+"/video?type=some.mjpeg"
            print('DEVICE USED IS : ', usedDevice)

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
        global img, typeFile
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Images (*.bmp *.jpg);;All files (*.*)")
        if path:
            try:
                print('path of opened file',path)
                self.akuisisiImage.setPixmap(QPixmap(path))
                img = cv2.imread(path)
                typeFile = imghdr.what(path)
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.update_title()

    def file_save(self):
        if(self.videoThread.isRunning()):
            self.dialog_critical("Ambil gambar terlebih dahulu sebelum menyimpan !")
        else:
            if self.akuisisiImage.pixmap():
                return self.file_saveas()
            self.dialog_critical("Tidak ada citra akuisisi yang dapat disimpan !")

    def file_saveas(self):
        print('TRYING TO SAVE AS')
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Images (*.bmp *.jpg);;All files (*.*)")
        if not path:
            # If dialogf is cancelled, will return ''
            return
        self._save_to_path(path)

    def _save_to_path(self, path):
        global img, typeFile
        try:
            self.akuisisiImage.pixmap().toImage().save(path)
            img = cv2.imread(path)
            typeFile = imghdr.what(path)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def update_title(self):
        self.setWindowTitle("Computer Vision and Soft Computing Software")

    def showImageProperties(self):
        print('SHOWING IMAGE PROPERTIES')
        h, w, c = img.shape
        self.imageProperties.setText("Image Properties")
        self.labelResolusi.setText("Resolusi Gambar HxWxC :")
        self.resolusi.setText(str(img.shape))
        self.labelTipefile.setText("Tipe File :")
        self.tipeFile.setText(str(typeFile))
        self.labelSize.setText("Size :")
        self.size.setText(str(img.size))

    def showIntensity(self):
        red = img[0, :, :]
        green = img[:, 0,:]
        blue = img[:,:,0]
        self.labelred.setText("Red Intensity :")
        self.red.setText(str(red))
        self.labelgreen.setText("Green Intensity :")
        self.green.setText(str(green))
        self.labelblue.setText("Blue Intensity :")
        self.blue.setText(str(blue))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Computer Vision and Soft Computing Software")

    window = MainWindow()
    app.exec_()

