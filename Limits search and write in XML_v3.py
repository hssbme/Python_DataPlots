#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import numpy as np
import glob, re, os, sys
from xml.etree import ElementTree as etree
# import matplotlib.pyplot as plt
# from scipy import stats

file_path = r'I:\program\1274\eng\hdmtprogs\tgl_sds\TestProgram\VIPR_b30_\Modules\TPI_SIU_STATIC\InputFiles'

module_name = 'TPI_SIU' #Add module name here 
combine_fabs = False
delimited_data = True
delimiter_char = '|'


try:
    os.makedirs(file_path+'\\'+'Results')
except:
    print('***Results folder already exists or/and Check for Write permissions at file path***')
    
results_file_path = (file_path+'\\'+'Results')


# In[30]:


"""Analog Config xml read and log"""
all_files = glob.glob(file_path + "/*.xml")
row_num = 0
rail_dict = {'_C01_':'_CORE01_','_C23_':'_CORE23_','_C45_':'_CORE45_','_C67_':'_CORE67_','_IN_':'_VCCIN_','_GT_':'_GT_','_RING_':'_RING_','_IO_':'_IO_','_1P8_':'_VCC1P8_','_DD2_':'_VCCDD2_','_DDQ_':'_VCCDDQ_','_PCIE_':'_VCCPCIE_','_ST_':'_VCCST_','_STG_':'_VCCSTG_','_ANAEHV_':'_VCCANAEHV_','_STGFUSE_':'_VCCSTGFUSE_','_TCPHY_':'_VCCTCPHY_'}
Col_names = dict.fromkeys(['xml_file','Config_list','Pin_Name','limit_low','limit_high','clamp_low','clamp_high','Rail_Name'])

Limits = pd.DataFrame(columns = ['xml_file','Config_list','Pin_Name','limit_low','limit_high','clamp_low','clamp_high','Rail_Name'])
limit_low = None
limit_high = None
clamp_low = None
clamp_high = None

def panda_write(Col_names):

    for col_name in Col_names:
        Limits.at[row_num, col_name] = Col_names[col_name]

    limit_low = None
    limit_high = None
    clamp_low = None
    clamp_high = None
    


for xml_file in all_files:

    vcc_xml = etree.parse(xml_file)
    root = vcc_xml.getroot()
    ConfigList = root.findall('ConfigList')
    
    for child in ConfigList:
        Curr_ConfigList = child.attrib['name']

        for node in child.iter():
            if node.tag == 'Cores':
                pd_print = False
            if node.tag == 'Measurements':
                pd_print = True
            
            if node.tag == 'Pin' and pd_print:
                row_num += 1
                
                Pin_Name = node.text
                
#                 panda_write(Col_names)

            if node.tag == 'limit_high' and pd_print:
                limit_high = node.text
                
            if node.tag == 'limit_low' and pd_print:
                limit_low = node.text

            if node.tag == 'clamp_low' and pd_print:
                clamp_low = node.text
                
            if node.tag == 'clamp_high' and pd_print:
                clamp_high = node.text
            
            try:
                Rail_name = Pin_Name.split('_')
                Rail_name = '_'+Rail_name[1]+'_'         
                Rail_name = rail_dict[Rail_name]
                
            except:
                pass
            
#             print(Rail_name)
            xml_file = xml_file.split('\\')
            xml_file = xml_file[-1]
    
            try:
                Col_names['xml_file'] = xml_file  
                Col_names['Config_list'] = Curr_ConfigList
                Col_names['Pin_Name'] = Pin_Name
                Col_names['limit_low'] = limit_low
                Col_names['limit_high'] = limit_high
                Col_names['clamp_low'] = clamp_low
                Col_names['clamp_high'] = clamp_high
                Col_names['Rail_Name'] = Rail_name
            except:
                pass
            
            panda_write(Col_names)

Limits['xml_file'] = Limits['xml_file'].shift(1)
Limits['Config_list'] = Limits['Config_list'].shift(1)
Limits = Limits.drop(Limits.index[0])
Limits = Limits.reset_index()
Limits = Limits.drop(['index'],axis = 1)

try:
    Limits.to_csv(results_file_path +'\\'+'Limits.csv')
except:
    print('Close Limits.csv file')


# In[31]:


def separate_lots(file_path):
    """ Use this to keep sites separate """

    all_files = glob.glob(file_path + "/*.csv")
    t2t_files = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)#, nrows=100)
#         df = pd.read_csv(filename, index_col=None, header=0, nrows=100)
        for col in df.columns:
            if 'IB DIEBIN' in col:
                df['IB DIEBIN'+' 1'] = df[col]
                df = df.drop(columns = col, axis=1)
            elif 'FB DIEBIN' in col:
                df['FB DIEBIN'+' 1'] = df[col]
                df = df.drop(columns = col, axis=1)



        t2t_files.append(df)
    
    passbin = [1,2,3,4]

    for dfs in t2t_files:
        data0 = pd.concat(t2t_files, axis=0, ignore_index=True)


    for col in data0.columns:
        if 'IB DIEBIN' in col:
            data0['GoodBadBin'] = data0[col].isin(passbin)

    data0['GoodBadBin'] = data0['GoodBadBin'].replace({True:'Good',False:'Bad'})
    
    if delimited_data:

        for col in data0.columns:
            if module_name in col:
                data0[col+' 1'] = data0[col].astype(str).str.split(delimiter_char).str[2]
                data0 = data0.drop(columns = col, axis=1)

    try:
        data0.to_csv(results_file_path +'\\'+'Delimited_Raw_Data.csv')
    except:
        print('Close Debug.csv file')
    return data0


# In[23]:


def combine_lots(file_path):
    """ Use this to combine sites """

    all_files = glob.glob(file_path + "/*.csv")

    t2t_files = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)#, nrows=100)
#         df = pd.read_csv(filename, index_col=None, header=0, nrows=100)
        for col in df.columns:
            if 'IB DIEBIN' in col:
                df['IB DIEBIN'+' 1'] = df[col]
                df = df.drop(columns = col, axis=1)
            elif 'FB DIEBIN' in col:
                df['FB DIEBIN'+' 1'] = df[col]
                df = df.drop(columns = col, axis=1)
            elif module_name in col:
                col_name = col.split(' ')[0]
                df[col_name] = df[col]
                df = df.drop(columns = col, axis=1)


        t2t_files.append(df)
    
    passbin = [1,2,3,4]

    for dfs in t2t_files:
        data0 = pd.concat(t2t_files, axis=0, ignore_index=True)

    
    for col in data0.columns:
        if 'IB DIEBIN' in col:
            data0['GoodBadBin'] = data0[col].isin(passbin)

    data0['GoodBadBin'] = data0['GoodBadBin'].replace({True:'Good',False:'Bad'})
    
    if delimited_data:
        for col in data0.columns:
            if module_name in col:
                data0[col+' 1'] = data0[col].astype(str).str.split(delimiter_char).str[2]
                data0 = data0.drop(columns = col, axis=1)
    
    try:
        data0.to_csv(results_file_path +'\\'+'Delimited_Raw_Data.csv')
    except:
        print('Close Debug.csv file')
    return data0


# In[24]:


if combine_fabs:
    data0 = combine_lots(file_path)
    print('1')
else:
    data0 = separate_lots(file_path)
    print('2')


# In[32]:


all_files = glob.glob(file_path + "/*.mtpl")
mtpl_file = all_files[0]
# mtpl_file = r'TPI_SIU_STATIC.mtpl'

def panda_write_mtpl(Col_names):

    for col_name in Col_names:
        mtpl.at[row_num, col_name] = Col_names_mtpl[col_name]

row_num = 0

Col_names_mtpl = dict.fromkeys(['xml_file','Config_list','Pin_Name','limit_low','limit_high','clamp_low','clamp_high','Rail_Name'])
mtpl = pd.DataFrame(columns = ['mtpl_TestName','mtpl_xmlFile','mtpl_ConfigSet'])

pTestBegin = re.compile(r'^Test iCAnalogMeasureTest (?P<re_testName>[A-Za-z0-9_]+)')
pConfigFile = re.compile(r'config_file = "(?P<re_ConfigFile>.+)";')
pConfigSet = re.compile(r'config_set = "(?P<re_ConfigSet>.+)";')


pEndTest = re.compile(r'^}')

pullData = False
with open(os.path.join(file_path,mtpl_file),'r') as lines:
    for line in lines:
        
        matchBegin = re.search(pTestBegin,line)
        if matchBegin:
            currTest = matchBegin.group("re_testName")
#             print(currTest)
            pullData = True
            
        matchConfigFile = re.search(pConfigFile,line)
        if matchConfigFile:
            configFile = matchConfigFile.group("re_ConfigFile")
            configFile = configFile.split('/')
            configFile = configFile[-1]
            
        matchConfigSet = re.search(pConfigSet,line)
        if matchConfigSet:
            configSet = matchConfigSet.group("re_ConfigSet")
#             print(configSet)
        
        matchWriteTable = re.search(pEndTest,line)
        if matchWriteTable and pullData:
#             print('abc')
            Col_names_mtpl['mtpl_xmlFile'] = configFile
            Col_names_mtpl['mtpl_TestName'] = currTest
            Col_names_mtpl['mtpl_ConfigSet'] = configSet
            
            panda_write_mtpl(mtpl)
            row_num += 1
            pullData = False
 
    try:
        mtpl.to_csv(results_file_path +'\\'+'MTPL_data.csv')
    except:
        print('Close Debug.csv file')


# In[26]:


#data0
#mtpl
#Limits
# print(Limits)
printThis = 0
Limits1 = pd.DataFrame()
Limits2 = Limits
df_size = len(mtpl)
rowLoc = 0
data0_temp = []
Limits['Test_Name'] = np .nan
# Limits['Test_Name1'] = np .nan
    
for mtpl_index, mtpl_row in mtpl.iterrows():
    

    Limits1 = Limits[Limits['xml_file'] == mtpl.mtpl_xmlFile[mtpl_index]]
#     print(mtpl.mtpl_ConfigSet[mtpl_index])
    Limits1 = Limits1[Limits1['Config_list'] == mtpl.mtpl_ConfigSet[mtpl_index]]
#     print(Limits1)
    try:
        Limits1 = Limits1.reset_index()
        Limits1 = Limits1.drop(columns = ['index'], axis = 1)
    except:
        pass
        
    for Limits1_index, Limits1_row in Limits1.iterrows():
        
#         print((mtpl.mtpl_TestName[mtpl_index]))
#         print(Limits1.Rail_Name[Limits1_index])
        data0_temp = []
        for col in data0.columns:
            
            if mtpl.mtpl_TestName[mtpl_index].upper() in col:# and Limits1.Rail_Name[Limits1_index] in col:
                print(mtpl.mtpl_TestName[mtpl_index])
                if Limits1.Rail_Name[Limits1_index] in col:
                    print((col))
                    data0_temp.append(str(col))

#         try:
#         print(Limits1)
        print(data0_temp)
        Limits1['Test_Name'].iloc[Limits1_index] = data0_temp[0].split(' ')[0]
#         Limits1['Test_Name1'].iloc[Limits1_index] = data0_temp[1].split(' ')[0]
#         except:
#             pass
        Limits2.loc[((Limits2.xml_file == Limits1.xml_file[Limits1_index])&(Limits2.Config_list == Limits1.Config_list[Limits1_index])&(Limits2.Rail_Name == Limits1.Rail_Name[Limits1_index])&(Limits2.Pin_Name == Limits1.Pin_Name[Limits1_index])&(Limits2.limit_low == Limits1.limit_low[Limits1_index])&(Limits2.limit_high == Limits1.limit_high[Limits1_index])&(Limits2.clamp_low ==  Limits1.clamp_low[Limits1_index])&(Limits2.clamp_high ==  Limits1.clamp_high[Limits1_index])),'Test_Name'] = Limits1['Test_Name'].iloc[Limits1_index]
#         Limits2.loc[((Limits2.xml_file == Limits1.xml_file[Limits1_index])&(Limits2.Config_list == Limits1.Config_list[Limits1_index])&(Limits2.Rail_Name == Limits1.Rail_Name[Limits1_index])&(Limits2.Pin_Name == Limits1.Pin_Name[Limits1_index])&(Limits2.limit_low == Limits1.limit_low[Limits1_index])&(Limits2.limit_high == Limits1.limit_high[Limits1_index])&(Limits2.clamp_low ==  Limits1.clamp_low[Limits1_index])&(Limits2.clamp_high ==  Limits1.clamp_high[Limits1_index])),'Test_Name'] = Limits1['Test_Name1'].iloc[Limits1_index]
# print(Limits1)
# print(Limits2) 

try:
    Limits2.to_csv(results_file_path +'\\'+'Limits - Optional_delete.csv')
except:
    print('Close Limits.csv file')


# In[28]:


Limits['mean'] = np .nan
Limits['stdev'] = np .nan
Limits['max'] = np .nan
Limits['10Sigma'] = np .nan
Limits['% Outside Proposed Sigma'] = np.nan

# data0 = data0.head(150)
for col in data0.columns:
    if module_name in col:
        col_name = col.split(' ')[0]
        colname = data0[col].dropna()
        colname = colname.astype(float)
        SampleN = len(colname)
        col_mean = colname.mean()
        col_std = colname.std()
        col_max = colname.max()
        col_10Sigma = col_mean +(10*col_std)

        Outside_Sigma = len(colname[colname.iloc[:]>=col_10Sigma])
        try:
            Outside_Sigma = (Outside_Sigma/SampleN)*100
        except:
            Outside_Sigma = 0
        
#         print(Outside_Sigma)
#         print(col_name)
#         for Limits2_index, Limits2_row in Limits2.iterrows():

        Limits2.loc[Limits2['Test_Name'] == col_name,'mean'] = col_mean
        Limits2.loc[Limits2['Test_Name'] == col_name,'stdev'] = col_std
        Limits2.loc[Limits2['Test_Name'] == col_name,'max'] = col_max
        Limits2.loc[Limits2['Test_Name'] == col_name,'10Sigma'] = col_10Sigma
        Limits2.loc[Limits2['Test_Name'] == col_name,'% Outside Proposed Sigma'] = round(Outside_Sigma,3)
        
print(Limits2)

try:
    Limits2.to_csv(results_file_path +'\\'+'Limits and Stats Summary.csv')
except:
    print('Close Limits.csv file')        
        


# In[ ]:


"""Write limits into xmls"""

file_path = r'L:\sbharadwaj\TGL81\TGL81_F32_SIU_STATIC_Leakage\Kappa'
data_file = r'Limits - Optional_delete.csv'
Prop_Limits0 = pd.read_csv(file_path +'\\'+ data_file)
Prop_Limits1 = Prop_Limits0[Prop_Limits0['Proposed_Limits'].notna()]
Prop_Limits1 = Prop_Limits1.reset_index()

file_path = r'L:\sbharadwaj\TGL81\TGL81_F32_SIU_STATIC_Leakage\Limits'
all_files = glob.glob(file_path + "/*.xml")

for xml_file_path in all_files:
    xml_file = xml_file_path.split('\\')
    xml_file = xml_file[-1]
    
    print(xml_file)
    Prop_Limits2 = Prop_Limits1[Prop_Limits1['xml_file']==xml_file]
    Prop_Limits2 = Prop_Limits2.reset_index()
    xml_root_rewrite = True
    
    if len(Prop_Limits2) >0 :
        print('xml file length:'+ str(len(Prop_Limits2)))
        for write_index, write_row in Prop_Limits2.iterrows():
            pd_print = False
            pd_print_pin = False
            if xml_root_rewrite == True:
                vcc_xml = etree.parse(xml_file_path)
                root = vcc_xml.getroot()
                xml_root_rewrite = False
#             else:
#                 root = root
            ConfigList = root.findall('ConfigList')
            
            for child in ConfigList:
                Curr_ConfigList = child.attrib['name']

                if Curr_ConfigList == Prop_Limits2['Config_list'].iloc[write_index]:
                    print((Prop_Limits2['Config_list'].iloc[write_index]))
                    
                    for node in child.iter():
                        if node.tag == 'Cores':
                            pd_print = False
                        if node.tag == 'Measurements':
                            pd_print = True
                        
                        if node.tag == 'Pin' and pd_print:
#                             row_num += 1

                        
                            if node.text == Prop_Limits2['Pin_Name'].iloc[write_index]:
                                    pd_print_pin = True
#                         print(type(limit_high))
                        
                        if node.tag == 'limit_high' and pd_print_pin:          
                            print(node.text)
                            
                            pd_print_pin = False
                            node.text = str(round(Prop_Limits2['Proposed_Limits'].iloc[write_index],2))
                            print(node.text)
                            
                            vcc_xml = etree.ElementTree(root)
                            
                            with open(r'C:\Users\shreyasb\Desktop\python\Limits' +'\\'+xml_file,'wb') as fileupdate:
                                vcc_xml.write(fileupdate)
                            
                            
#                             pd_print_pin = False
                            
#                             Pin_Name = node.text
                

#             print(Prop_Limits2['Config_list'].iloc[write_index])
#             print(Prop_Limits2['Pin_Name'].iloc[write_index])
            
#             print(write_index)


# In[ ]:


###Extra code blocks###


# In[ ]:


def separate_lots(file_path):
""" Use this to keep sites separate """


    all_files = glob.glob(file_path + "/*.csv")

    t2t_files = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)#, nrows=100)
        t2t_files.append(df)

    data0 = pd.concat(t2t_files, axis=0, ignore_index=True)
    # data0.dropna(how='all', axis=1)
    passbin = [1,2,3,4]
    for col in data0.columns:
        if 'IB DIEBIN' in col:
            data0['GoodBadBin'] = data0[col].isin(passbin)

    data0['GoodBadBin'] = data0['GoodBadBin'].replace({True:'Good',False:'Bad'})

    for col in data0.columns:
        if 'SIU_STATIC' in col:
            data0[col+' 1'] = data0[col].str.split('|').str[2]
            data0 = data0.drop(columns = col, axis=1)

    try:
        data0.to_csv(results_file_path +'\\'+'Delimited_Raw_Data.csv')
    except:
        print('Close Debug.csv file')


# In[ ]:


#         Limits1['Test_Name'].astype(str)
#         print(Limits1.loc[Limits1_index])
#         print(Limits1)
#         Limits2 = Limits2.merge(Limits1)
#         Limits2 = pd.concat([Limits2,Limits1],axis=1)
#         Limits = Limits.append(Limits1,sort = False)
#         print(Limits1)

#         print(Limits1.xml_file[Limits1_index])
#         print(Limits.shape,Limits1.shape,Limits2.shape)
#         Limits2 = Limits1.iloc[Limits1_index].combine_first(Limits2)
#         print(Limits2.apply(lambda x: Limits1[(Limits1.xml_file == x.xml_file) & (Limits1.Config_list == x.Config_list) & (Limits1.Pin_Name == x.Pin_Name) & (Limits1.limit_low == x.limit_low) & (Limits1.limit_high == x.limit_high) & (Limits1.Rail_Name == x.Rail_Name) & (Limits1.clamp_low == x.clamp_low) & (Limits1.clamp_high == x.clamp_high)].index[0]))
#         Limits2['Test_Name'] =  Limits2.apply(lambda x: Limits1[(Limits1.xml_file == x.xml_file) & (Limits1.Config_list == x.Config_list) & (Limits1.Pin_Name == x.Pin_Name) & (Limits1.limit_low == x.limit_low) & (Limits1.limit_high == x.limit_high) & (Limits1.Rail_Name == x.Rail_Name) & (Limits1.clamp_low == x.clamp_low) & (Limits1.clamp_high == x.clamp_high)].index[0], axis=1)
#         Limits2.loc[(Limits2.Test_Name == str(data0_temp)), ['xml_file', 'Config_list','Rail_Name', 'Pin_Name','limit_low', 'limit_high','clamp_low', 'clamp_high']] = Limits1.xml_file[Limits1_index], Limits1.Config_list[Limits1_index], Limits1.Rail_Name[Limits1_index], Limits1.Pin_Name[Limits1_index], Limits1.limit_low[Limits1_index],Limits1.limit_high[Limits1_index], Limits1.clamp_low[Limits1_index], Limits1.clamp_high[Limits1_index]
#         Limits2.loc[(Limits2.Test_Name == Limits1.xml_file[Limits1_index], Limits1.Config_list[Limits1_index], Limits1.Rail_Name[Limits1_index], Limits1.Pin_Name[Limits1_index], Limits1.limit_low[Limits1_index],Limits1.limit_high[Limits1_index], Limits1.clamp_low[Limits1_index], Limits1.clamp_high[Limits1_index]), ['xml_file', 'Config_list','Rail_Name', 'Pin_Name','limit_low', 'limit_high','clamp_low', 'clamp_high']] = Limits1.xml_file[Limits1_index], Limits1.Config_list[Limits1_index], Limits1.Rail_Name[Limits1_index], Limits1.Pin_Name[Limits1_index], Limits1.limit_low[Limits1_index],Limits1.limit_high[Limits1_index], Limits1.clamp_low[Limits1_index], Limits1.clamp_high[Limits1_index]
#         Limits2 = pd.merge(Limits1, Limits2, on = ['xml_file', 'Config_list','Rail_Name', 'Pin_Name','limit_low', 'limit_high','clamp_low', 'clamp_high'], how = 'outer')
  


# In[ ]:


# try:
# data0.to_csv(file_path +'\\'+'Test'+'\\'+'Outputs'+'\\'+'Delimited.csv')
# except:
#     print('Close Debug.csv file')
file_path = r'L:\sbharadwaj\TGL81\TGL81_F32_SIU_STATIC_Leakage'
data0 = pd.read_csv(file_path +'\\'+'temp'+'\\'+'SIU_STATIC_Leakage_Delimited_delete.csv', index_col=None, header=0)
print(data0)


# if __name__ == "__main__":
#     pass

