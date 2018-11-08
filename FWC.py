import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os.path
%matplotlib inline
import csv
import re


LCG_path = r'O:\VPE\UserWorkSpace\Shreyas\OX01D10\Full well setup 00_01_01_B\First_touchdown_LD_FWC_schmoo_datalog\LCG'
HCG_path = r'O:\VPE\UserWorkSpace\Shreyas\OX01D10\Full well setup 00_01_01_B\First_touchdown_LD_FWC_schmoo_datalog\HCG'

LCG_MEAN = r'LCG_Mean_P9AG52-24F3_OVTKYEC_96_SLT2.csv_20181106102246.csv'
#LCG_STDEV = r'LCG_StDev_P9AG52-24F3_OVTKYEC_96_SLT2.csv_20181106102246.csv'
#HCG_MEAN = r''
#HCG_STDEV = r''


lcg_mean = pd.read_csv(LCG_path+'\\'+ LCG_MEAN)
#lcg_stdev = pd.read_csv(LCG_path+'\\'+ LCG_MEAN)
#hcg_mean = pd.read_csv(LCG_path+'\\'+ LCG_MEAN)
#hcg_stdev = pd.read_csv(LCG_path+'\\'+ LCG_MEAN)

lcg_mean['DIEID'] = lcg_mean['DIE_X'].astype(str)+lcg_mean['DIE_Y'].astype(str)

#df = df.loc[df['VERDICT']=='PASS']
#print(lcg_mean['DIEID'])
#global lcg

lcg_mean = pd.melt(lcg_mean, id_vars=['SBIN','HBIN','DIE_X','DIE_Y','SITE','TP_VERSION','LOT_ID','WAFER_ID','LOG_NAME','DIEID'])
#df.to_csv(LCG_path+'\\'+'Debug.csv')


lcg_mean['CHANNEL'] = np.where(lcg_mean['variable'].str[-2:-1] == "_",
                                  lcg_mean['variable'].str[-1:],
                                 lcg_mean['variable'].str[-2:])

lcg_mean['temp1']= lcg_mean['variable'].str[11:]
lcg_mean['LUX'] = lcg_mean.temp1.str.extract('(\d+)')

lcg_mean_pvt = pd.pivot_table(lcg_mean,index=['LUX','DIEID','CHANNEL'])
#lcg_mean['lux'] = int(s) for s in lcg_mean['temp1'].str[:].split() if lcg_mean['temp1'].isdigit()
#int(lcg_mean['lux']) for lcg_mean['lux'] in lcg_mean['temp1'].str[:].split() if lcg_mean['temp1'].isdigit()
#lcg_mean.to_csv(LCG_path +'\\'+'Debug.csv')
lcg_mean_pvt.to_csv(LCG_path +'\\'+'Debug.csv')
#print(lcg_mean['temp1'])
#df.A.str.extract('(\d+)')