import os, re, csv
#os.system("export https_proxy='http://proxy-dmz.intel.com:912'")

#Regex list
#reAuthor = re.compile(r"^author:[\t].*")
reAuthor = re.compile(r"author:[\t](?P<sAuthor_Result>.*)")
reLabels = re.compile(r'^labels:[\t](?P<sLabels_Result>.*)')
reMilestone = re.compile(r'^milestone:[\t](?P<sMilestone_Result>.*)')
reNumber = re.compile(r'^number:[\t](?P<sNumber_Result>.*)')
reQualDoc = re.compile(r'^- \[X] TPDB QualDoc is not.*')
QualDoc_Default = 'Qual Doc is Present'
os.system('gh pr list --state "closed" > temp.txt')

with open ('temp.txt', 'r') as RecentPR:
    RecentPRNum = csv.reader(RecentPR, delimiter = "\t")
    PRMax = next(RecentPRNum)
    CurrPR = PRMax[0]
    CurrPR = int(CurrPR)

csvReport = 'PR_QualDoc_Report.csv'
if os.path.exists(csvReport):
    os.remove(csvReport)
with open(csvReport, 'a', newline='') as csvFile:
    newRow = ['PRNumber','TP Name','Author','Module Labels','QualDoc']
    writer = csv.writer(csvFile)
    writer.writerow(newRow)

    for PR in range (CurrPR-250, CurrPR):
        os.system('gh pr view {0} > temp.txt'.format(PR))
    
        with open ('temp.txt', 'r') as PRInfo:
            Author, Labels, PRNumber, Milestone = 'NA','NA','NA','NA'
            for line in PRInfo:
    
                sAuthor = re.search(reAuthor,line)
                if sAuthor is not None:
                    Author = str(sAuthor.group("sAuthor_Result"))
                    #print((Author))
    
                sLabels = re.search(reLabels,line)
                if sLabels is not None:
                    Labels = sLabels.group("sLabels_Result")
                    #print(Labels)
    
                sMilestone = re.search(reMilestone,line)
                if sMilestone is not None:
                    Milestone = sMilestone.group("sMilestone_Result")
                    #print(Milestone)
    
                sNumber = re.search(reNumber,line)
                if sNumber is not None:
                    PRNumber = sNumber.group("sNumber_Result")
                    #print(PRNumber)
    
                sQualDoc = re.search(reQualDoc,line)
                if sQualDoc is not None:
                    QualDoc = sQualDoc.group(0)
                    #print(QualDoc)
                else:
                    QualDoc = QualDoc_Default
            newRow = [PRNumber,Milestone,Author,Labels,QualDoc]
            writer.writerow(newRow)

csvFile.close()
os.remove('temp.txt')

#print(sNumber.group(sNumber_Result),sMilestone.group(sMilestone_Result),sAuthor.group(sAuthor_Result),sLabels.group(sLabels_Result),sQualDoc.group(0))
#os.system('gh pr view "666" > temp.txt')
#proc = Popen(['gh' 'pr' 'list' '--state' '"closed"'], stdout = open('temp.txt', 'r'))
