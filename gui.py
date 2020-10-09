#LIBRARY GUI
import urllib

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#LIBRARY ESENSIAL
import sys
import cv2
import imghdr
import os

#LIBRARY CUSTOM
import utils
import operasiTitikBackend as operasiTitik

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


class OperasiCitraDialog(QDialog):
    def __init__(self, jenis_operasi, parent=None):
        super(OperasiCitraDialog, self).__init__(parent)
        self.result = ""
        mainLayout = QVBoxLayout()

        self.jenis_operasi = jenis_operasi
        if(jenis_operasi=='Atur Contrast'):
            layoutSlider1 = QHBoxLayout()
            layoutSlider2 = QHBoxLayout()

            self.setWindowTitle("Atur Nilai Minimum dan Maksimum Kontras")
            self.convertslider = QSlider()
            self.convertslider.setOrientation(Qt.Horizontal)
            self.convertslider.setTickPosition(QSlider.TicksBelow)
            self.convertslider.setTickInterval(1)
            self.convertslider.setMinimum(0)
            self.convertslider.setMaximum(255)
            layoutSlider1.addWidget(self.convertslider)

            slider1Group = QGroupBox("Nilai Minimum")
            slider1Group.setLayout(layoutSlider1)

            self.convertslider2 = QSlider()
            self.convertslider2.setOrientation(Qt.Horizontal)
            self.convertslider2.setTickPosition(QSlider.TicksBelow)
            self.convertslider2.setTickInterval(1)
            self.convertslider2.setMinimum(0)
            self.convertslider2.setMaximum(255)
            layoutSlider2.addWidget(self.convertslider2)

            slider2Group = QGroupBox("Nilai Maksimum")
            slider2Group.setLayout(layoutSlider2)

            mainLayout.addWidget(slider1Group)
            mainLayout.addWidget(slider2Group)

        elif(jenis_operasi=='Atur Brightness'):
            layoutSlider1 = QHBoxLayout()

            self.setWindowTitle("Atur nilai brightness")
            self.convertslider = QSlider()
            self.convertslider.setOrientation(Qt.Horizontal)
            self.convertslider.setTickPosition(QSlider.TicksBelow)
            self.convertslider.setTickInterval(1)
            self.convertslider.setMinimum(0)
            self.convertslider.setMaximum(255)
            layoutSlider1.addWidget(self.convertslider)

            slider1Group = QGroupBox("Nilai Brightness")
            slider1Group.setLayout(layoutSlider1)

            mainLayout.addWidget(slider1Group)
        elif(jenis_operasi=='Konversi ke Biner'):
            layoutSlider1 = QHBoxLayout()

            self.setWindowTitle("Atur threshold")
            self.convertslider = QSlider()
            self.convertslider.setOrientation(Qt.Horizontal)
            self.convertslider.setTickPosition(QSlider.TicksBelow)
            self.convertslider.setTickInterval(1)
            self.convertslider.setMinimum(0)
            self.convertslider.setMaximum(255)
            layoutSlider1.addWidget(self.convertslider)

            slider1Group = QGroupBox("Nilai Threshold")
            slider1Group.setLayout(layoutSlider1)

            mainLayout.addWidget(slider1Group)

        buttonLayout = QHBoxLayout()
        self.btnJalankan = QPushButton("OK")
        buttonLayout.addWidget(self.btnJalankan)
        self.btnJalankan.clicked.connect(self.OnOk)

        self.btnBatalkan = QPushButton("Cancel")
        buttonLayout.addWidget(self.btnBatalkan)
        self.btnBatalkan.clicked.connect(self.OnCancel)

        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    def OnOk(self):
        if(self.jenis_operasi=='Atur Contrast'):
            self.result = [self.convertslider.value(),self.convertslider2.value()]
        elif(self.jenis_operasi=='Atur Brightness'):
            self.result = [self.convertslider.value()]
        elif(self.jenis_operasi=='Konversi ke Biner'):
            self.result = [self.convertslider.value()]
        self.done(1)
        return self.result

    def OnCancel(self):
        self.close()

    def GetValue(self):
        return self.result

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global imageState
        imageState = 0
        self.initUiThread()

    @pyqtSlot(QImage)
    def takeVideo(self, image):
        self.akuisisiImage.setPixmap(QPixmap.fromImage(image))

    def initUiThread(self):
        self._want_to_close = False
        self.menuOperasi = ['Konversi ke RGB','Konversi ke Grayscale','Konversi ke Biner',
                            'Atur Brightness','Atur Contrast','Operasi Negasi']

        #LAYOUT UTAMA VERTIKAL
        self.mainlayout = QHBoxLayout()

        #INIT COLUMN LEFT TERMASUK PENGGABUNGAN DI FUNCTION YANG DIPISAH
        self.initColumnLeftGui()
        #INIT COLUMN RIGHT TERMASUK PENGGABUNGAN DI FUNCTION YANG DIPISAH
        self.initColumnCenterGui()
        self.initColumnRightGui()

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

    def switchOperasiCitra(self, selectedOperasi):

        imageArray = utils.convertQImageToMat(self.akuisisiImage.pixmap().toImage())
        h, w, ch = imageArray.shape

        print('imageArray',imageArray)
        if(selectedOperasi=='Konversi ke RGB'):
            print('AKAN KONVERSI KE RGB')
        elif(selectedOperasi=='Konversi ke Grayscale'):
            print('AKAN KONVERSI KE Grayscale')
            imageArray = operasiTitik.rgb2Gray(imageArray,h, w, ch)
        elif(selectedOperasi=='Konversi ke Biner'):
            print('AKAN KONVERSI KE Biner')
            dlg = OperasiCitraDialog('Konversi ke Biner')
            if dlg.exec_():
                value = dlg.GetValue()
                print(value)
                imageArray = operasiTitik.gray2Bin(imageArray,h, w, ch, value[0])
                print("Success!")
            else:
                print("Cancel!")
                return
        elif(selectedOperasi=='Atur Brightness'):
            print('AKAN Atur Brightness')
            dlg = OperasiCitraDialog('Atur Brightness')
            if dlg.exec_():
                value = dlg.GetValue()
                imageArray = operasiTitik.brighten(imageArray,h, w, ch, value[0])
                print(value)
                print("Success!")
            else:
                print("Cancel!")
                return
        elif(selectedOperasi=='Atur Contrast'):
            print('AKAN Atur Contrast')
            dlg = OperasiCitraDialog('Atur Contrast')
            if dlg.exec_():
                value = dlg.GetValue()
                print(value)
                if(value[0]>value[1]):
                    self.dialog_critical("Nilai minimum tidak boleh lebih dari nilai maksimum !")
                    return
                imageArray = operasiTitik.conStrech(imageArray,h, w, ch, value[0],value[1])
                print("Success!")
            else:
                print("Cancel!")
                return
        elif(selectedOperasi=='Operasi Negasi'):
            print('AKAN Operasi Negasi')
            imageArray = operasiTitik.negative(imageArray,h, w, ch)

        bytesPerLine = ch * w
        convertToQtFormat = QImage(imageArray.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.convertedImage.setPixmap(QPixmap.fromImage(convertToQtFormat))

    def initColumnRightGui(self):
        #MAIN LAYOUT TERDAPAT 3 KOLOM
        columnRight = QVBoxLayout()

        #SUB LAYOUT COLUMN RIGHT
        columnRightRow1 = QHBoxLayout()
        columnRightRow2 = QHBoxLayout()

        #SUB LAYOUT COLUMN RIGHT ROW
        columnRightRow1Col1 = QHBoxLayout()
        self.listOperasiTitik = QListWidget()
        for n in self.menuOperasi:
            self.listOperasiTitik.addItem(str(n))
        self.listOperasiTitik.itemSelectionChanged.connect(self.operasiTitikChanged)

        columnRightRow1Col1.addWidget(self.listOperasiTitik)
        listOperasiTitikGroup = QGroupBox("Operasi Citra")
        listOperasiTitikGroup.setLayout(columnRightRow1Col1)
        columnRightRow1.addWidget(listOperasiTitikGroup)

        #ISI DARI SUB SUB LAYOUT COLUMN CENTER ROW 2 COL 2
        columnCenterRow2Col1 = QVBoxLayout()
        columnCenterRow2Col2 = QVBoxLayout()

        self.imageStartOperationButton = QPushButton("JALANKAN OPERASI")
        self.imageStartOperationButton.clicked.connect(self.operasiTitikStart)
        self.imageUndoOperationButton = QPushButton("URUNGKAN OPERASI")

        #GABUNGKAN
        columnCenterRow2Col1.addWidget(self.imageStartOperationButton)
        columnCenterRow2Col2.addWidget(self.imageUndoOperationButton)

        columnRightRow2.addLayout(columnCenterRow2Col1)
        columnRightRow2.addLayout(columnCenterRow2Col2)

        columnRight.addLayout(columnRightRow1)
        columnRight.addLayout(columnRightRow2)

        self.mainlayout.addLayout(columnRight)

    def initColumnCenterGui(self):
        #COLUMN CENTER
        columnCenter = QVBoxLayout()

        #SUB LAYOUT COLUMN CENTER
        columnCenterRow1 = QHBoxLayout()
        columnCenterRow2 = QHBoxLayout()

        #ISI DARI SUB LAYOUT COLUMN CENTER ROW 1 : INFORMASI IMAGE SEPERTI PROPERTIES, DLL
        columnCenterRow1Col1 = QVBoxLayout()
        self.convertedImage = QLabel(self)
        columnCenterRow1Col1.addWidget(self.convertedImage)

        listOperasiTitikGroup = QGroupBox("Citra Hasil")
        listOperasiTitikGroup.setLayout(columnCenterRow1Col1)
        columnCenterRow1.addWidget(listOperasiTitikGroup)

        #ISI DARI SUB LAYOUT COLUMN CENTER ROW 2 : MENU PROPERTIES
        columnCenterRow2Col1 = QVBoxLayout()
        columnCenterRow2Col2 = QVBoxLayout()

        #ISI DARI SUB SUB LAYOUT COLUMN CENTER ROW 2 COL 1
        columnCenterRow2Col1Row1 = QHBoxLayout()
        columnCenterRow2Col1Row2 = QHBoxLayout()

        self.imageTransformedSelectButton = QPushButton("PILIH GAMBAR")
        self.imageTransformedSelectButton.clicked.connect(self.file_converted_open)
        self.imageTransformedSaveButton = QPushButton("SIMPAN HASIL")
        self.imageTransformedSaveButton.clicked.connect(self.file_converted_save)

        #GABUNGKAN
        columnCenterRow2Col1Row1.addWidget(self.imageTransformedSelectButton)
        columnCenterRow2Col1Row2.addWidget(self.imageTransformedSaveButton)

        #GABUNGKAN DENGAN PARENT
        columnCenterRow2Col1.addLayout(columnCenterRow2Col1Row1)
        columnCenterRow2Col1.addLayout(columnCenterRow2Col1Row2)

        #ISI DARI SUB SUB LAYOUT COLUMN CENTER ROW 2 COL 2
        columnCenterRow2Col2Row1 = QHBoxLayout()
        columnCenterRow2Col2Row2 = QHBoxLayout()

        self.imageSavePropertiesButton = QPushButton("SIMPAN PROPERTI")
        self.imageSavePropertiesButton.clicked.connect(self.saveImageProperties)
        self.imageOpenPropertiesButton = QPushButton("PINDAHKAN <<")
        self.imageOpenPropertiesButton.clicked.connect(self.pindahkanImageToAwal)

        #GABUNGKAN
        columnCenterRow2Col2Row1.addWidget(self.imageSavePropertiesButton)
        columnCenterRow2Col2Row2.addWidget(self.imageOpenPropertiesButton)

        #GABUNGKAN DENGAN PARENT
        columnCenterRow2Col2.addLayout(columnCenterRow2Col2Row1)
        columnCenterRow2Col2.addLayout(columnCenterRow2Col2Row2)

        #GABUNGKAN DENGAN PARENT
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
        columnLeftRow1Col1 = QVBoxLayout()
        akuisisiImageGroup = QGroupBox()
        self.akuisisiImage = QLabel(self)
        columnLeftRow1Col1.addWidget(self.akuisisiImage)

        listOperasiTitikGroup = QGroupBox("Citra Awal")
        listOperasiTitikGroup.setLayout(columnLeftRow1Col1)
        columnLeftRow1.addWidget(listOperasiTitikGroup)

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

    def operasiTitikChanged(self):
        print("Selected item : ",self.listOperasiTitik.selectedItems())

    def operasiTitikStart(self):
        print("Operasi akan dijalankan")
        if self.akuisisiImage.pixmap():
            selectedItem = self.listOperasiTitik.currentItem()
            if(selectedItem):
                selectedItem = selectedItem.text()
                print("Selected item : ",selectedItem)
                self.switchOperasiCitra(selectedItem)
            else:
                self.dialog_critical("Tidak ada opsi dipilih !")
        else:
            self.dialog_critical("Tidak ada citra awal yang dapat diproses !")


    def pindahkanImageToAwal(self):
        if self.akuisisiImage.pixmap():
            tempPixmap = self.convertedImage.pixmap()
            self.akuisisiImage.setPixmap(tempPixmap)
        else:
            self.dialog_critical("Tidak ada citra hasil yang dapat dipindahkan !")


    def mulaiAkuisisiCitra(self):
        global usedDevice
        global imageState
        imageState = 1

        if(self.selectDeviceRadioBtn2.isChecked() or self.selectDeviceRadioBtn1.isChecked()):
            if(self.selectDeviceRadioBtn2.isChecked()):
                device = self.formAkuisisiIP.text()
                usedDevice = "http://"+device+"/video?type=some.mjpeg"
            self.videoThread.start()
        else:
            self.dialog_critical("Silahkan pilih opsi perangkat akuisisi citra !")

    def mulaiAmbilGambar(self):
        global imageState
        if(imageState==1):
            imageState = 2
            self.videoThread.terminate()
        else:
            self.dialog_critical("Akuisisi citra terlebih dahulu sebelum mengambil gambar !")


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
        global imageState
        imageState = 3
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
        global imageState
        imageState = 3
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

    def file_converted_open(self):
        global img, typeFile
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Images (*.bmp *.jpg);;All files (*.*)")
        if path:
            try:
                print('path of opened file',path)
                self.convertedImage.setPixmap(QPixmap(path))
                img = cv2.imread(path)
                typeFile = imghdr.what(path)
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.update_title()

    def file_converted_save(self):
        if(self.videoThread.isRunning()):
            self.dialog_critical("Ambil gambar terlebih dahulu sebelum menyimpan !")
        else:
            if self.convertedImage.pixmap():
                return self.file_converted_saveas()
            self.dialog_critical("Tidak ada citra akuisisi yang dapat disimpan !")

    def file_converted_saveas(self):
        print('TRYING TO SAVE AS')
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Images (*.bmp *.jpg);;All files (*.*)")
        if not path:
            # If dialogf is cancelled, will return ''
            return
        self._save_converted_to_path(path)

    def _save_converted_to_path(self, path):
        global img, typeFile
        try:
            self.convertedImage.pixmap().toImage().save(path)
            img = cv2.imread(path)
            typeFile = imghdr.what(path)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def update_title(self):
        self.setWindowTitle("Computer Vision and Soft Computing Software")

    def saveImageProperties(self):
        print('TRYING TO SAVE IMG PROP')
        global imageState
        global img, typeFile
        if(imageState==3):
            print('SAVING IMAGE PROPERTIES')

            h, w, c = img.shape
            bitDepth = str(len(img[0][0]))
            imageResolution = str(img.shape)
            imageFileType = str(typeFile)
            imageSize = str(img.size)

            print('WILL BE SAVED TO:',os.path.join(os.getcwd(),"RESULTS.txt"))

            textPropertiesFile = open(r""+os.path.join(os.getcwd(),"RESULTS.txt")+"", "w+")

            textPropertiesFile.write('HEIGHT : '+str(h)+'\n')
            textPropertiesFile.write('WIDTH : '+str(w)+'\n')
            textPropertiesFile.write('COLOR : '+str(c)+'\n')
            textPropertiesFile.write('BIT DEPTH : '+bitDepth+'\n')
            textPropertiesFile.write('RESOLUTION : '+imageResolution+'\n')
            textPropertiesFile.write('FILE TYPE : '+imageFileType+'\n')
            textPropertiesFile.write('FILE SIZE : '+imageSize+'\n')

            redImg = [[0 for j in range(w)] for k in range(h)]
            greenImg = [[0 for j in range(w)] for k in range(h)]
            blueImg = [[0 for j in range(w)] for k in range(h)]

            for i in range(h):
                for j in range(w):
                    for k in range(c):
                        if k is 2:
                            blueImg[i][j] = img[i,j,2]
                        if k is 1:
                            greenImg[i][j] = img[i,j,1]
                        if k is 0:
                            redImg[i][j] = img[i,j,0]

            textPropertiesFile.write('RED PIXEL : \n')
            textPropertiesFile.write('[')
            for i in range(h):
                textPropertiesFile.write('[')
                for j in range(w):
                    textPropertiesFile.write('['+str(redImg[i][j])+']')
                textPropertiesFile.write(']\n')
            textPropertiesFile.write(']\n')

            textPropertiesFile.write('GREEN PIXEL : \n')
            textPropertiesFile.write('[')
            for i in range(h):
                textPropertiesFile.write('[')
                for j in range(w):
                    textPropertiesFile.write('['+str(greenImg[i][j])+']')
                textPropertiesFile.write(']\n')
            textPropertiesFile.write(']\n')

            textPropertiesFile.write('BLUE PIXEL : \n')
            textPropertiesFile.write('[')
            for i in range(h):
                textPropertiesFile.write('[')
                for j in range(w):
                    textPropertiesFile.write('['+str(blueImg[i][j])+']')
                textPropertiesFile.write(']\n')
            textPropertiesFile.write(']\n')
            textPropertiesFile.close()
            self.dialog_info("Berhasil menyimpan file. File disimpan di :\n"+str(os.path.join(os.getcwd(),"RESULTS.txt")))
        else:
            self.dialog_critical("Simpan atau buka gambar terlebih dahulu sebelum melihat properti citra !")

    def showImageProperties(self):
        global imageState
        global img, typeFile
        if(imageState==3):
            print('SHOWING IMAGE PROPERTIES')
            h, w, c = img.shape
            self.labelDepth.setText("Bit Depth :")

            bitDepth = len(img[0][0])
            if(str(img.dtype)=='uint4'):
                self.imageDepth.setText(str(bitDepth*4)+' bit ('+str(bitDepth/2)+' Bytes)')
            elif(str(img.dtype)=='uint8'):
                self.imageDepth.setText(str(bitDepth*8)+' bit ('+str(bitDepth)+' Bytes)')
            elif(str(img.dtype)=='uint16'):
                self.imageDepth.setText(str(bitDepth*16)+' bit ('+str(bitDepth*2)+' Bytes)')
            else:
                self.imageDepth.setText('-tidak dapat membaca-')

            self.labelResolusi.setText("Resolusi Gambar HxWxC :")
            self.resolusi.setText(str(img.shape))
            self.labelTipefile.setText("Tipe File :")
            self.tipeFile.setText(str(typeFile))
            self.labelSize.setText("Size :")
            self.size.setText(str(img.size))
        else:
            self.dialog_critical("Simpan atau buka gambar terlebih dahulu sebelum melihat properti citra !")


    def showIntensity(self):
        global imageState
        if(imageState==3):
            red = img[0, :, :]
            green = img[:, 0,:]
            blue = img[:,:,0]
            self.labelred.setText("Red Intensity :")
            self.red.setText(str(red))
            self.labelgreen.setText("Green Intensity :")
            self.green.setText(str(green))
            self.labelblue.setText("Blue Intensity :")
            self.blue.setText(str(blue))
        else:
            self.dialog_critical("Simpan atau buka gambar terlebih dahulu sebelum melihat properti citra !")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Computer Vision and Soft Computing Software")

    window = MainWindow()
    app.exec_()

