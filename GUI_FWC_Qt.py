# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'C:\Users\shreyas.bharadwaj\Desktop\python\getText.ui'
#From Qt folder, type the following in cmd prompt to generate python file: pyuic5 -x "C:\Users\shreyas.bharadwaj\Desktop\python\getText2.ui" -o "C:\Users\shreyas.bharadwaj\Desktop\python\getText3.py"
# Created by: PyQt5 UI code generator 5.11.3
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets#, QtFileDialog
import csv
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os.path
#%matplotlib inline
import csv
#import re
#import seaborn as sns
plt.style.use('ggplot')
class Ui_Dialog(object):
    """UI setup using Qt Library for GUI """
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.csvFilePath1 = None
        #self.textEdit = QtWidgets.QTextEdit(Dialog)
        #self.textEdit.setGeometry(QtCore.QRect(10, 40, 271, 31))
        #self.textEdit.setObjectName("textEdit")
        self.fileList = QtWidgets.QListWidget(Dialog)
        self.fileList.setGeometry(QtCore.QRect(10, 40, 271, 101))
        self.fileList.setObjectName("fileList")
        self.fileList.setAlternatingRowColors(True)
        self.fwcShmoo = QtWidgets.QPushButton(Dialog)
        self.fwcShmoo.setGeometry(QtCore.QRect(240, 150, 111, 31))
        self.fwcShmoo.setObjectName("fwcShmoo")
        self.readPath = QtWidgets.QPushButton(Dialog)
        self.readPath.setGeometry(QtCore.QRect(70, 150, 101, 31))
        self.readPath.setObjectName("readPath")
        self.Browse = QtWidgets.QPushButton(Dialog)
        self.Browse.setGeometry(QtCore.QRect(300, 40, 75, 23))
        self.Browse.setObjectName("Browse")
        self.fwc = FWC_Shmoo()
        self.Browse.clicked.connect(self.browseFile)
        self.readPath.clicked.connect(self.readpathdata)
        self.fwcShmoo.clicked.connect(self.fwc.FWC_Main)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def readpathdata(self, fpath):
        """Reads file path and file name from Text Box QListWidget"""
        fpath = self.fileList.item(0).text() # Add hightlight to select feature.
        #fpath = self.fileList.selectedItems()#.text()
        print('Reading file: '+fpath)
        self.csvFilePath1 = fpath
        dataFile = str(self.csvFilePath1)
        FWC_Shmoo.dataFile = dataFile
        return fpath

    def retranslateUi(self, Dialog):
        """Qt method descriptions """
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.fwcShmoo.setText(_translate("Dialog", "FWC Shmoo"))
        self.readPath.setText(_translate("Dialog", "Read Data"))
        self.Browse.setText(_translate("Dialog", "Browse"))

    def browseFile(self, csvFilePath2):
        """Browse windows file directory to find .csv file """
        csvFilePath, fileType = QtWidgets.QFileDialog.getOpenFileName(None, 'Select File','','*.csv')
        self.fileList.addItem(csvFilePath)
        return csvFilePath

class standBy(Ui_Dialog):
    pass

class FWC_Shmoo(Ui_Dialog):

    def AUTORUN_VER(self,file):
        """Returns Autorun version if available"""
        file = file[file['AUTORUN_VER_BOOL'] == True]
        file['AUTORUN_VER_BOOL'] = file['variable'].str.contains('AUTORUN', regex=True)
        file = file[file.AUTORUN_VER_BOOL == True]
        file['AUTORUN'] = file.variable.str.extract('(\d+)').astype(int)
        AutoRun_Ver = str(file.AUTORUN.unique()) 
        print('Autorun Version is '+ AutoRun_Ver)

    def REMOVE_CHAR(self,file,char):
        """Ensures the data log has numericals only"""
        file = file[~file.value.str.contains(char, na= False)]
        return(file)

    def PLOT_FWC(self,file,plot_type):
        """Plot FWC curve - withcontrol over plot range"""
        file.pivot_table(index='LUX',columns='CHANNEL',values='value',fill_value='scalar').plot()
        #file = file.pivot(index='LUX',columns = 'CHANNEL', values = 'value').plot(legend=False)
        plt.title(plot_type +'_CHANNEL_PLOTS', color = 'black')
        plt.xlabel('LUX')
        plt.ylabel('Value')
        plt.show()
    
    def GET_CHANNELS(self,file):
        """Locates Channel names"""
        file['CHANNEL'] = file.variable.str.split('_').str[-1]
        channels = str(file.CHANNEL.unique())
        channels = channels.split(' ')
        return(file)
        return(channels)
    
    def MAX_LUX(self,file,max_ill):
        """Suggested max Lux value to achieve Full Well"""
        abc = file.pivot_table(index='LUX',columns='CHANNEL',values='value')
        max_2 = abc['Gr'].argmax()
        if int(max_2) <= max_ill/2:
            print('The FWC illumination should be '+ str(2*int(max_2))+' LUX')
        else:
            print('Data not reliable. Please refer to plots ')
        
    def FWC_Main(self):
        """Full well curve main func """
        path = FWC_Shmoo.dataFile
        fwc = pd.read_csv(path)
        fwc.columns = fwc.columns.str.replace(' ','')

        try:
            fwc['DIE_XY'] = fwc['DIE_X'].astype(str)+fwc['DIE_Y'].astype(str)    
            fwc = pd.melt(fwc, id_vars=['Parameter','SBIN','HBIN','DIE_X','DIE_Y','SITE','TP_VERSION','TIME','LOT_ID','WAFER_ID','DIE_XY','RD_SETTING_VER'])
        except:
            try:
                fwc = pd.melt(fwc, id_vars=['Parameter','SBIN','HBIN','DIE_X','DIE_Y','SITE','TP_VERSION','TIME','LOT_ID','WAFER_ID','DIE_XY'])#,'RD_SETTING_VER'])
            except :
                print('Please match the Columns in List to data file')

        try:
            fwc['AUTORUN_VER_BOOL'] = ~fwc['variable'].str.contains('LUX', regex=False)
            
        except:
            fwc['AUTORUN_VER_BOOL'] = False
        
        fwc.replace(r'\s+', np.nan, regex=True)
        fwc.dropna(inplace= True)

        #try:
        #    fwc.to_csv(file_path +'\\'+'Debug1.csv')
        #except:
        #    print('Close Debug.csv file')

        try:
            self.AUTORUN_VER(fwc)
        except:
            print('Autorun Version not available')
            fwc.AUTORUN_VER_BOOL.value() == False
        fwc = fwc[fwc['AUTORUN_VER_BOOL'] == False]
        fwc['LUX'] = fwc.variable.str.extract('(\d+)').astype(int)
        fwc = self.GET_CHANNELS(fwc)
        #fwc = fwc[~fwc.value.str.contains('_', na= False)]
        fwc = self.REMOVE_CHAR(fwc,'_')
        try:
            fwc.to_csv(file_path +'\\'+'Debug.csv')
        except:
            print('Close Debug.csv file')
        fwc['LUX']=fwc['LUX'].astype(int)
        fwc['value']=fwc['value'].astype(float)
        fwc_mean = fwc[fwc.variable.str.contains('Mean')]
        fwc_mean= fwc_mean[fwc_mean.CHANNEL.str.len() < 3]
        fwc_std = fwc[fwc.variable.str.contains('Std')]
        fwc_std= fwc_std[fwc_std.CHANNEL.str.len() < 3]
        #abc = fwc_std.pivot_table(index='LUX',columns='CHANNEL',values='value',fill_value='scalar').plot()
        max_ill=fwc.LUX.max()
        int(max_ill)
            
        self.MAX_LUX(fwc_std,max_ill)
            
        self.PLOT_FWC(fwc_mean,'FWC_MEAN')
        self.PLOT_FWC(fwc_std,'FWC_STDEV')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
