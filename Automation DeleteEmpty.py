############################################################################################################################
#
#   Importing requried Library
#  
#############################################################################################################################

import sys
import os
import time
import schedule

############################################################################################################################
#
#   Function name:  DirectoryScanner
#   Input:          Name of Directory
#   Description:    Delete of Empty Files periodically
#   Date :          19/07/2026
#   Author :        Omkar Dnyandev Shinde
#  
#############################################################################################################################

def DirectoryScanner(DirectoryPath):

    Border="-"*40

    timestamp=time.ctime()
    LogFileName="Marvellous%s.log"%(timestamp)
    LogFileName=LogFileName.replace(" ","_")
    LogFileName=LogFileName.replace(":","_")

    Ret =False

    Ret=os.path.exists(DirectoryPath)

    if(Ret==False):
        print("Marvellus Automation Error: There is No Such Directory with name",DirectoryPath)
        return
    
    Ret=os.path.isdir(DirectoryPath)
    if(Ret==False):
        print("Marvellus Automation Error: It Is Not A Directory with name",DirectoryPath)
        return

    print("file gets created with name :",LogFileName)
    fobj=open(LogFileName,"w")

    fobj.write(Border+"\n")

    fobj.write("Marvellous Infosystem Automation Script\n")

    fobj.write(Border+"\n\n")

    fobj.write("Files From the Directory Are :\n")

    fobj.write(Border+"\n\n")

    TotalFiles=0
    EmptyFiles=0

    for FolderName,SubFolder,FileName in os.walk(DirectoryPath):

        for fname in FileName :
            TotalFiles=TotalFiles+1
            fname= os.path.join(FolderName,fname)
            fobj.write(f"{fname}: {os.path.getsize(fname)}\n")

            if(os.path.getsize(fname)==0):
                os.remove(fname)
                EmptyFiles=EmptyFiles+1

    fobj.write(Border+"\n")
    fobj.write(f"Total Files scanned :{TotalFiles}\n")
    fobj.write(f"Total  Empty Files Found And Deleted  :{EmptyFiles}\n")
            

    
    fobj.write(Border+"\n")
    fobj.write("Log file gets created at:"+timestamp)
    fobj.write("\n"+Border+"\n")

    fobj.close()
############################################################################################################################
#
#   Function name:  main
#   Input:          Command Line Argument
#   Description:    It Control the Script
#   Date :          19/07/2026
#   Author :        Omkar Dnyandev Shinde
#  
#############################################################################################################################

def main():
    Border = "-"*50
    print(Border)
    print("Marvellous Infosystem Automation Script")
    print(Border)
    if(len(sys.argv)==2):

        if(sys.argv[1]=="--h" or sys.argv[1]=="--H" ):

            print("This Automation Script is Used to Travel the Directory")
            print("For Brtter Usage Please Check --U Flag")

        elif(sys.argv[1]=="--u" or sys.argv[1]=="--U"):
            print("Please Execute the Script As :")
            print("python Filename.py DirectoryName")
            print("Directory name Should be Absolute Path")


        else:
            
            schedule.every(1).minute.do(DirectoryScanner,sys.argv[1])   
                 

            while True:
                schedule.run_pending()
                time.sleep(1)


    else:
         print("Invalid Number of arguments")
         print("Please use --h or --u for more information")


    print(Border)
    print("Thankyou for using Automation Script")
    print(Border)
        
############################################################################################################################
#
#   Starter of Automation
#  
#############################################################################################################################
if __name__=="__main__":
    main()