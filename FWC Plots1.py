
# coding: utf-8

# # IMPORT DATA

# In[350]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os.path
get_ipython().run_line_magic('matplotlib', 'inline')
import csv
import re
import seaborn as sns

LCG_path = r'O:\VPE\UserWorkSpace\Shreyas\OX01D10\Setting bring up and data\Full well setup 00_01_01_B\First_touchdown_LD_FWC_schmoo_datalog\LCG'
HCG_path = r'O:\VPE\UserWorkSpace\Shreyas\OX01D10\Setting bring up and data\Full well setup 00_01_01_B\First_touchdown_LD_FWC_schmoo_datalog\HCG'

LCG_mean1 = r'LCG_stdev_P9AG52-24F3_OVTKYEC_96_SLT2.csv_20181106102246.csv'
LCG_stdev1 = r'LCG_StDev_P9AG52-24F3_OVTKYEC_96_SLT2.csv_20181106102246.csv'
HCG_mean1 = r'HCG_stdev_P9AG52-24F3_OVTKYEC_96_SLT2.csv_20181106102246.csv'
HCG_stdev1 = r'HCG_StDev_P9AG52-24F3_OVTKYEC_96_SLT2.csv_20181106102246.csv'

lcg_mean = pd.read_csv(LCG_path+'\\'+ LCG_mean1)
lcg_stdev = pd.read_csv(LCG_path+'\\'+ LCG_stdev1)
hcg_mean = pd.read_csv(HCG_path+'\\'+ HCG_mean1)
hcg_stdev = pd.read_csv(HCG_path+'\\'+ HCG_stdev1)

paths = [hcg_mean, hcg_stdev, lcg_mean, lcg_stdev]
#strmap = map(str,[paths])
#strmap = str(paths).strip('[]')
#for i in strmap:
    #print(i)

#Name all channels name files as strings ******* Will need automation to detect Channel names automatically
lcg_mean.name = 'lcg_mean'
lcg_stdev.name = 'lcg_stdev'
hcg_mean.name = 'hcg_mean'
hcg_stdev.name = 'hcg_stdev'
`
global paths
global lcg_mean
global lcg_stdev
global hcg_mean
global hcg_stdev

for file in paths:
    print(file.name)
    file['DIEID'] = file['DIE_X'].astype(str)+file['DIE_Y'].astype(str)
    file = pd.melt(file, id_vars=['SBIN','HBIN','DIE_X','DIE_Y','SITE','TP_VERSION','LOT_ID','WAFER_ID','DIEID'])#'LOG_NAME'
    file['LUX'] = file.variable.str.extract('(\d+)').astype(float)
    file.dropna(axis='rows')
    
    file['VC']= file['variable'].str[7:10]
    vc = str(file.VC.unique())
    file['CHANNEL'] = np.where(file['variable'].str[-2:-1] == "_",
                                    file['variable'].str[-1:],
                                    file['variable'].str[-2:])
    #file.to_csv(LCG_path+'\\'+'Debug.csv')
    #file[file.LUX.apply(lambda x: x.isnumeric())]
    file[file.LUX.str.isnumeric()]
    
    channels = file.CHANNEL.unique()
    #print (channels)
    for channel in channels:
        locals()['file_{}'.format(channel)] = file.loc[file['CHANNEL']== channel]
    #print(file_gr)
    plt.style.use('ggplot')

    for channel in channels:
        locals()['file_{}_pvt'.format(channel)] = locals()['file_{}'.format(channel)].pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
        plt.title('file_'+channel+'_DIE_PLOTS', color = 'black')
        plt.xlabel('LUX')
        plt.ylabel('Value')
        plt.show()
        
        


# In[289]:


#for files in paths:
    #locals()['{}'.format(files)]['DIEID'] = locals()['{}'.format(files)]['DIE_X'].astype(str)+locals()['{}'.format(files)]['DIE_Y'].astype(str)
    #locals()['lcg_mean_{}'.format(channel)] = lcg_mean.loc[lcg_mean['CHANNEL']== channel]
for files in paths:
    locals()['{}'.format(files)].to_csv(LCG_path +'\\'+'Debug'+str(files)+'.csv')


# In[274]:



lcg_mean['DIEID'] = lcg_mean['DIE_X'].astype(str)+lcg_mean['DIE_Y'].astype(str)

lcg_mean = pd.melt(lcg_mean, id_vars=['SBIN','HBIN','DIE_X','DIE_Y','SITE','TP_VERSION','LOT_ID','WAFER_ID','DIEID'])

lcg_mean['VC']= lcg_mean['variable'].str[7:10]
vc = str(lcg_mean.VC.unique())
lcg_mean['CHANNEL'] = np.where(lcg_mean['variable'].str[-2:-1] == "_",
                                  lcg_mean['variable'].str[-1:],
                                 lcg_mean['variable'].str[-2:])

lcg_mean['temp1']= lcg_mean['variable'].str[11:]
lcg_mean['LUX'] = lcg_mean.temp1.str.extract('(\d+)').astype(int)

channels = lcg_mean.CHANNEL.unique()

for channel in channels:
    locals()['lcg_mean_{}'.format(channel)] = lcg_mean.loc[lcg_mean['CHANNEL']== channel]
#print(lcg_mean_gr)
plt.style.use('ggplot')

for channel in channels:
    locals()['lcg_mean_{}_pvt'.format(channel)] = locals()['lcg_mean_{}'.format(channel)].pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
    plt.title('LCG_MEAN_'+channel+'DIE_PLOTS', color = 'black')
    plt.xlabel('LUX')
    plt.ylabel('Value')
    plt.show()


# In[ ]:



lcg_mean_r = lcg_mean.loc[lcg_mean['CHANNEL']== 'R']
lcg_mean_gr = lcg_mean.loc[lcg_mean['CHANNEL']== 'GR']
lcg_mean_gb = lcg_mean.loc[lcg_mean['CHANNEL']== 'GB']
lcg_mean_b = lcg_mean.loc[lcg_mean['CHANNEL']== 'B']



lcg_mean_r_pvt = lcg_mean_r.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_MEAN_R PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()

lcg_mean_r_pvt
#lcg_mean_r_max_lux = lcg_mean_r_pvt.idxmax(axis=1)
#print(lcg_mean_r_max_lux)

lcg_mean_gr_pvt = lcg_mean_gr.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_MEAN_GR PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


lcg_mean_gb_pvt = lcg_mean_gb.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_MEAN_GB PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


lcg_mean_b_pvt = lcg_mean_b.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_MEAN_B PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()



#lcg_mean_pvt = pd.pivot_table(lcg_mean,index=['LUX','DIEID','CHANNEL'])

#try:
    #lcg_mean_gr.to_csv(LCG_path +'\\'+'Debug.csv')
#except:
    #print('Close Debug.csv file')


#for value in lcg_mean_gr_pvt.DIEID():
        #y = ab1[currentParam] # ,fontweight = 'bold']
        #x = np.arange(0,100,1)
#plt.
        

#lcg_mean.to_csv(LCG_path +'\\'+'Debug.csv')
#print(lcg_mean_gr_pvt)


# # LCG MEAN

# In[246]:




lcg_mean['DIEID'] = lcg_mean['DIE_X'].astype(str)+lcg_mean['DIE_Y'].astype(str)

#df = df.loc[df['VERDICT']=='PASS']
#print(lcg_mean['DIEID'])
#global lcg

lcg_mean = pd.melt(lcg_mean, id_vars=['SBIN','HBIN','DIE_X','DIE_Y','SITE','TP_VERSION','LOT_ID','WAFER_ID','DIEID'])
#df.to_csv(LCG_path+'\\'+'Debug.csv')


lcg_mean['CHANNEL'] = np.where(lcg_mean['variable'].str[-2:-1] == "_",
                                  lcg_mean['variable'].str[-1:],
                                 lcg_mean['variable'].str[-2:])

lcg_mean['temp1']= lcg_mean['variable'].str[11:]
lcg_mean['LUX'] = lcg_mean.temp1.str.extract('(\d+)').astype(int)

#channels = [R,GR,GB,B]

lcg_mean_r = lcg_mean.loc[lcg_mean['CHANNEL']== 'R']
lcg_mean_gr = lcg_mean.loc[lcg_mean['CHANNEL']== 'GR']
lcg_mean_gb = lcg_mean.loc[lcg_mean['CHANNEL']== 'GB']
lcg_mean_b = lcg_mean.loc[lcg_mean['CHANNEL']== 'B']

plt.style.use('ggplot')

lcg_mean_r_pvt = lcg_mean_r.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_MEAN_R PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()

lcg_mean_r_pvt
#lcg_mean_r_max_lux = lcg_mean_r_pvt.idxmax(axis=1)
#print(lcg_mean_r_max_lux)

lcg_mean_gr_pvt = lcg_mean_gr.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_MEAN_GR PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


lcg_mean_gb_pvt = lcg_mean_gb.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_MEAN_GB PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


lcg_mean_b_pvt = lcg_mean_b.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_MEAN_B PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()







#lcg_mean_pvt = pd.pivot_table(lcg_mean,index=['LUX','DIEID','CHANNEL'])

#try:
    #lcg_mean_gr.to_csv(LCG_path +'\\'+'Debug.csv')
#except:
    #print('Close Debug.csv file')


#for value in lcg_mean_gr_pvt.DIEID():
        #y = ab1[currentParam] # ,fontweight = 'bold']
        #x = np.arange(0,100,1)
#plt.
        

#lcg_mean.to_csv(LCG_path +'\\'+'Debug.csv')
#print(lcg_mean_gr_pvt)


# In[222]:




lcg_stdev['DIEID'] = lcg_stdev['DIE_X'].astype(str)+lcg_stdev['DIE_Y'].astype(str)

#df = df.loc[df['VERDICT']=='PASS']
#print(lcg_stdev['DIEID'])
#global lcg

lcg_stdev = pd.melt(lcg_stdev, id_vars=['SBIN','HBIN','DIE_X','DIE_Y','SITE','TP_VERSION','LOT_ID','WAFER_ID','DIEID'])
#df.to_csv(LCG_path+'\\'+'Debug.csv')


lcg_stdev['CHANNEL'] = np.where(lcg_stdev['variable'].str[-2:-1] == "_",
                                  lcg_stdev['variable'].str[-1:],
                                 lcg_stdev['variable'].str[-2:])

lcg_stdev['temp1']= lcg_stdev['variable'].str[11:]
lcg_stdev['LUX'] = lcg_stdev.temp1.str.extract('(\d+)').astype(int)

#channels = [R,GR,GB,B]

lcg_stdev_r = lcg_stdev.loc[lcg_stdev['CHANNEL']== 'R']
lcg_stdev_gr = lcg_stdev.loc[lcg_stdev['CHANNEL']== 'GR']
lcg_stdev_gb = lcg_stdev.loc[lcg_stdev['CHANNEL']== 'GB']
lcg_stdev_b = lcg_stdev.loc[lcg_stdev['CHANNEL']== 'B']



lcg_stdev_r_pvt = lcg_stdev_r.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_stdev_R PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


lcg_stdev_gr_pvt = lcg_stdev_gr.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_stdev_GR PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


lcg_stdev_gb_pvt = lcg_stdev_gb.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_stdev_GB PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


lcg_stdev_b_pvt = lcg_stdev_b.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('LCG_stdev_B PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()
#lcg_stdev_pvt = pd.pivot_table(lcg_stdev,index=['LUX','DIEID','CHANNEL'])

try:
    lcg_stdev_gr.to_csv(LCG_path +'\\'+'Debug.csv')
except:
    print('Close Debug.csv file')

#for value in lcg_stdev_gr_pvt.DIEID():
        #y = ab1[currentParam] # ,fontweight = 'bold']
        #x = np.arange(0,100,1)
#plt.
        

#lcg_stdev.to_csv(LCG_path +'\\'+'Debug.csv')
#print(lcg_stdev_gr_pvt)


# In[207]:



hcg_mean['DIEID'] = hcg_mean['DIE_X'].astype(str)+hcg_mean['DIE_Y'].astype(str)


hcg_mean = pd.melt(hcg_mean, id_vars=['SBIN','HBIN','DIE_X','DIE_Y','SITE','TP_VERSION','LOT_ID','WAFER_ID','LOG_NAME','DIEID'])
#df.to_csv(hcg_path+'\\'+'Debug.csv')


hcg_mean['CHANNEL'] = np.where(hcg_mean['variable'].str[-2:-1] == "_",
                                  hcg_mean['variable'].str[-1:],
                                 hcg_mean['variable'].str[-2:])

hcg_mean['temp1']= hcg_mean['variable'].str[11:]
hcg_mean['LUX'] = hcg_mean.temp1.str.extract('(\d+)').astype(int)

#channels = [R,GR,GB,B]

hcg_mean_r = hcg_mean.loc[hcg_mean['CHANNEL']== 'R']
hcg_mean_gr = hcg_mean.loc[hcg_mean['CHANNEL']== 'GR']
hcg_mean_gb = hcg_mean.loc[hcg_mean['CHANNEL']== 'GB']
hcg_mean_b = hcg_mean.loc[hcg_mean['CHANNEL']== 'B']



hcg_mean_r_pvt = hcg_mean_r.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('hcg_MEAN_R PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


hcg_mean_gr_pvt = hcg_mean_gr.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('hcg_MEAN_GR PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


hcg_mean_gb_pvt = hcg_mean_gb.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('hcg_MEAN_GB PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


hcg_mean_b_pvt = hcg_mean_b.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('hcg_MEAN_B PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


# In[205]:


hcg_stdev['DIEID'] = hcg_stdev['DIE_X'].astype(str)+hcg_stdev['DIE_Y'].astype(str)

hcg_stdev = pd.melt(hcg_stdev, id_vars=['SBIN','HBIN','DIE_X','DIE_Y','SITE','TP_VERSION','LOT_ID','WAFER_ID','LOG_NAME','DIEID'])
#df.to_csv(hcg_path+'\\'+'Debug.csv')


hcg_stdev['CHANNEL'] = np.where(hcg_stdev['variable'].str[-2:-1] == "_",
                                  hcg_stdev['variable'].str[-1:],
                                 hcg_stdev['variable'].str[-2:])

hcg_stdev['temp1']= hcg_stdev['variable'].str[11:]
hcg_stdev['LUX'] = hcg_stdev.temp1.str.extract('(\d+)').astype(int)

#channels = [R,GR,GB,B]

hcg_stdev_r = hcg_stdev.loc[hcg_stdev['CHANNEL']== 'R']
hcg_stdev_gr = hcg_stdev.loc[hcg_stdev['CHANNEL']== 'GR']
hcg_stdev_gb = hcg_stdev.loc[hcg_stdev['CHANNEL']== 'GB']
hcg_stdev_b = hcg_stdev.loc[hcg_stdev['CHANNEL']== 'B']



hcg_stdev_r_pvt = hcg_stdev_r.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('hcg_stdev_R PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


hcg_stdev_gr_pvt = hcg_stdev_gr.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('hcg_stdev_GR PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


hcg_stdev_gb_pvt = hcg_stdev_gb.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('hcg_stdev_GB PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()


hcg_stdev_b_pvt = hcg_stdev_b.pivot(index='LUX',columns = 'DIEID', values = 'value').plot(legend=False)
plt.title('hcg_stdev_B PLOTS', color = 'black')
plt.xlabel('LUX')
plt.ylabel('Value')
plt.show()

