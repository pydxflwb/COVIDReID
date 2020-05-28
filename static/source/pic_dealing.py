import os, sys
from shutil import copyfile

path = sys.argv[0]
path0 = path.split('\\')[:-1]

path1=''

# 单层文件夹

#for i in range(len(path0)-1):
#    path1 =  path1+path0[i]+'\\'

#opath = path1 + path0[-1]+'\\'
#print(opath)
#npath = path1 + path0[-1]+'_new\\'
#print(npath)
#if not os.path.exists(npath):
 #   os.mkdir(npath)
    

#fileList = os.listdir(opath)
#t = 0
#for filename in fileList:
 #   if filename.split('.')[-1] == "jpg":
  #      if t==0:
   #         copyfile(opath+filename, npath+filename)
    #    t+=1
     #   if t>=10:
      #      t=0
        
# 两层文件夹
# 三层文件夹

for i in range(len(path0)):
    path1 =  path1+path0[i]+'\\'
print(path1)

dirl = os.listdir(path1)
for d in dirl:
    if len(d.split(".")) == 1:
        path2 = path1 + d +'\\'
        print(path2)
        dirlist = os.listdir(path2)
        # for di in range(len(dirlist)):
        #        direc = dirlist[di]
        for direc in dirlist:
                if len(direc.split(".")) == 1:
                    path3 = path2 + direc +'\\'
                    print(path3)
                    # npath = path2 + d+'_p' + str(di+1) + '\\'
                    # print(npath)
                    #os.rename(opath,npath)
                    filelist = os.listdir(path3)
                    for file in filelist:
                        opath = path3 + file
                        # print(opath)
                        
                        n1 = file.split("t")[1]
                        n1 = "t" +n1.split("f")[0]
                        nfile = file.split("t")[0] +"_"+ n1 + "_f"+file.split("f")[1]
                        # print(nfile)
                        #nfile = direc + file.split("_")[0] + file.split("_")[1] +'.jpg'
                        npath = path3 + nfile
                        # print(npath)
                        os.rename(opath,npath)
                        #opath = path2 + direc +'\\' +file
                        #npath = path2 +  + '\\' +file
                        #os.rename(opath,npath)
                    
                #filelist = os.listdir(opath)
            #t = 0
            #for filename in filelist:
             #   if filename.split('.')[-1] == "jpg":
              #      if t==0:
               #         copyfile(opath+filename, npath+filename)
                #    t+=1
                 #   if t>=10:
                  #      t=0
            
