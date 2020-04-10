import os
Test_location = os.getcwd()
#Test_location = r'C:\Intel\hdmtProgs\Lab8new\Lab8new\Lab8\trainingTP_MTD'
BasePath = Test_location
os.chdir(BasePath)
print('Searching in Directory: ' + os.getcwd())
bypass_extn = {'dll', 'pinObj', 'Onetoc2', 'py', 'xlsm','zip', 'xlsx'}
def searchstring(test_dir, test_str):
    for dir_path, dirs, file_names in os.walk(test_dir):
        
        for file_name in file_names:
            extn = file_name.split('.')[-1]
            if extn not in bypass_extn:
                fullpath = os.path.join(dir_path, file_name)
                
                try:
                    with open(fullpath,'r') as f:
                        if test_str in f.read():
                            print(fullpath)
                except:
                    print('Cannot read: '+ fullpath)
            else:
                pass
                
search_str = input('Enter String to Search: ')
searchstring(BasePath, search_str)
print('*****End of search*****')
a = input('Press any key to exit')
print(a)