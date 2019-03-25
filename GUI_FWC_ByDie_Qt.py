# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'C:\Users\shreyas.bharadwaj\Desktop\python\getText.ui'
#From Qt folder, type the following in cmd prompt to generate python file: pyuic5 -x "C:\Users\shreyas.bharadwaj\Desktop\python\getText2.ui" -o "C:\Users\shreyas.bharadwaj\Desktop\python\getText3.py"
# P:\BACKUP\VPE\Shreyas\Tools\PyTools\FWC_Shmoo\Testing\SampleData\Passing\
# Created by: PyQt5 UI code generator 5.11.3
# WARNING! All changes made in this file will be lost!
#**********TO DO**********************
# Add logging data and checkpoints.
# Change loops to 'map and filter and Lambda expression' function where applicable.
# Check test time and minimize longest test time items.
# implement 'import gc' for garbage collection and memory management.
#
#
from PyQt5 import QtCore, QtGui, QtWidgets#, QtFileDialog
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os.path
#%matplotlib inline
#import re
#import seaborn as sns
plt.style.use('ggplot')
class Ui_Dialog(object):
    """UI setup using Qt Library for GUI """
    def setupUi(self, FWC_SHMOO_PLOT):
        FWC_SHMOO_PLOT.setObjectName("FWC_SHMOO_PLOT")
        FWC_SHMOO_PLOT.resize(400, 250)
        self.csvFilePath1 = None
        #self.textEdit = QtWidgets.QTextEdit(FWC_SHMOO_PLOT)
        #self.textEdit.setGeometry(QtCore.QRect(10, 40, 271, 31))
        #self.textEdit.setObjectName("textEdit")
        self.fileList = QtWidgets.QListWidget(FWC_SHMOO_PLOT)
        self.fileList.setGeometry(QtCore.QRect(10, 40, 271, 51))
        self.fileList.setObjectName("fileList")
        self.fileList.setAlternatingRowColors(True)
        self.fwcShmoo = QtWidgets.QPushButton(FWC_SHMOO_PLOT)
        self.fwcShmoo.setGeometry(QtCore.QRect(240, 150, 111, 31))
        self.fwcShmoo.setObjectName("fwcShmoo")
        self.readPath = QtWidgets.QPushButton(FWC_SHMOO_PLOT)
        self.readPath.setGeometry(QtCore.QRect(70, 150, 101, 31))
        self.readPath.setObjectName("readPath")
        self.Browse = QtWidgets.QPushButton(FWC_SHMOO_PLOT)
        self.Browse.setGeometry(QtCore.QRect(300, 40, 75, 23))
        self.Browse.setObjectName("Browse")
        self.fwc = FWC_Shmoo()
        self.Browse.clicked.connect(self.browseFile)
        self.readPath.clicked.connect(self.readpathdata)
        self.fwcShmoo.clicked.connect(self.fwc.FWC_Main)
        self.retranslateUi(FWC_SHMOO_PLOT)
        QtCore.QMetaObject.connectSlotsByName(FWC_SHMOO_PLOT)

    def readpathdata(self, fpath):
        """Reads file path and file name from Text Box QListWidget"""
        fpath = self.fileList.item(0).text() # Add hightlight to select feature.
        #fpath = self.fileList.selectedItems()#.text()
        print('Reading file: '+fpath)
        self.csvFilePath1 = fpath
        dataFile = str(self.csvFilePath1)
        FWC_Shmoo.dataFile = dataFile
        return fpath

    def retranslateUi(self, FWC_SHMOO_PLOT):
        """Qt method descriptions """
        _translate = QtCore.QCoreApplication.translate
        FWC_SHMOO_PLOT.setWindowTitle(_translate("FWC_SHMOO_PLOT", "FWC_SHMOO_PLOT"))
        self.fwcShmoo.setText(_translate("FWC_SHMOO_PLOT", "FWC Shmoo"))
        self.readPath.setText(_translate("FWC_SHMOO_PLOT", "Read Data"))
        self.Browse.setText(_translate("FWC_SHMOO_PLOT", "Browse"))

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
        try:
            file = file[file['AUTORUN_VER_BOOL'] == True]
            file['AUTORUN_VER_BOOL'] = file['variable'].str.contains('AUTORUN', regex=True)
            file = file[file.AUTORUN_VER_BOOL == True]
            file['AUTORUN'] = file.variable.str.extract('(\d+)').astype(int)
            AutoRun_Ver = str(file.AUTORUN.unique()) 
            print('Autorun Version is '+ AutoRun_Ver)
        except:
            pass

    def REMOVE_CHAR(self,file,char):
        """Ensures the data log has numericals only"""
        file = file[~file.value.str.contains(char, na= False)]
        return(file)

    def PLOT_FWC(self,file,plot_type):
        """Plot FWC curve - withcontrol over plot range - Default set to 'gg plot' """
        channel_color = {'R':'red','B':'blue','Gr':'Green','Gb':'lime','Ir':'firebrick','GbGr':'yellowgreen','All':'black'}

        filec = file.pivot_table(index='LUX',columns='CHANNEL',values='value',fill_value='scalar').reset_index()#.plot()
        filec.set_index('LUX', inplace = True)
        filec.plot(color = [channel_color.get(x, '#ffffff') for x in filec.columns])

        plt.title(plot_type +'_CHANNEL_PLOTS', color = 'black')
        plt.xlabel('LUX')
        plt.ylabel('Value')

        #################################Die wise plot#####################################
        file1 = file.pivot_table(index=['LUX','CHANNEL'],columns='DIE_XY',values='value',fill_value='scalar').reset_index()#.plot(legend=False)#, c = file['CHANNEL'].apply(lambda x:channel_color[x]))
        file1.set_index('LUX', inplace = True)
        file1.reset_index().pivot('LUX','CHANNEL').plot(legend=False, color = file1.CHANNEL.map(channel_color))

        plt.title(plot_type +'_DIE LEVEL_PLOTS', color = 'black')
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
        
        file_path = os.path.dirname(path)
        #print(file_path)
        FWC_Shmoo.file_path = file_path
        
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

        try:
            fwc.to_csv(file_path +'\\'+'Debug.csv')
        except:
            print('Close Debug.csv file')


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

        try:
            fwc.to_csv(file_path +'\\'+'Debug.csv')
            fwc_mean.to_csv(file_path +'\\'+'mean.csv')
            fwc_std.to_csv(file_path +'\\'+'Stdev.csv')
        except:
            print('Close Debug.csv file')

        self.PLOT_FWC(fwc_mean,'FWC_MEAN')
        self.PLOT_FWC(fwc_std,'FWC_STDEV')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FWC_SHMOO_PLOT = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(FWC_SHMOO_PLOT)
    FWC_SHMOO_PLOT.show()
    sys.exit(app.exec_())
