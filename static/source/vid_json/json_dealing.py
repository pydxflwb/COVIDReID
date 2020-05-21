import os, sys
import json

path = sys.argv[0]
path0 = path.split('\\')[:-1]

path1=''


def findcontact(jsonfile,camera):
    output = []
    cutthresh = 0.3
    frametrack = 15
    with open(jsonfile,"r") as f:
        jsondata = json.load(f) 
    f.close()
    print(len(jsondata))
    jlen = len(jsondata)
    for i in range(jlen):
        fnum = i+1
        framedata = jsondata[str(fnum)]
        if framedata != []:
            for person in framedata:
                if person["score"] >= cutthresh:
                    bbox = person["bbox"]
                    for b in bbox:
                        b = float(b)
                    tid1 = person["tracking_id"]
                    for j in range(i+1, min(i+1+frametrack, jlen)):
                         fnum2 = j+1
                         framedata2 = jsondata[str(fnum2)]
                         if framedata2 != []:
                            for person2 in framedata2:
                                if person2["score"] >= cutthresh:
                                    tid2 = person2["tracking_id"]
                                    if tid2 != tid1:
                                        bbox2 = person2["bbox"]
                                        for b1 in bbox2:
                                            b1 = float(b1)
                                        # 比例大于0.7
                                        a = (bbox[3]-bbox[1])/(bbox2[3]-bbox2[1]) # 高
                                        b = (bbox[2]-bbox[0])/(bbox2[2]-bbox2[0]) # 宽
                                        if (min(a,b)>=0.7) and (max(a,b)<=1.43):
                                            flag_pro = True
                                        else:
                                            flag_pro = False

                                        # 重叠
                                        if bbox[2] >= bbox2[0] and bbox[0] <= bbox2[2] and bbox[3] >= bbox2[1] and bbox[1] <= bbox2[3]:
                                            flag_in = True
                                        else:
                                            flag_in = False

                                        if abs((bbox[3] + bbox[1]) / 2 - (bbox2[3] + bbox2[1]) / 2) <= min((bbox2[3] - bbox2[1]), (bbox[3] - bbox[1])) and abs((bbox[2] + bbox[0]) / 2 - (bbox2[2] + bbox2[0]) / 2) <= min((bbox2[2] - bbox2[0]), (bbox[2] - bbox[0])):
                                            flag_near = True
                                        else:
                                            flag_near = False

                                        if flag_pro and (flag_in or flag_near):
                                            out = [camera.split(".")[0], tid1, tid2, j+1]
                                            # print(camera+" person" +str(tid1) +" and person"+str(tid2)+" contacted in frame "+str(j+1))
                                            flag_exists = False
                                            for o in output:
                                                if o == '':
                                                    continue
                                                if out[0] == o[0] and ((out[1] == o[1] and out[2] == o[2]) or (out[1] == o[2] and out[2] == o[1])):                                                
                                                    flag_exists = True
                                                    break
                                            if not flag_exists:
                                                output.append(out)
                                                

    return output                                
    #while(jsondata[str(tt)]):
     #   print(jsondata[str(tt)])
      #  tt+=1
     
    # print(framedata)

    
for i in range(len(path0)):
    path1 =  path1+path0[i]+'\\'
print(path1)
jsonpathlist = os.listdir(path1)
olist = []

for jp in jsonpathlist:
    if jp.split(".")[-1]=="json" and jp.split(".")[0] !="contact":
        jname = path1 + jp
        print(jname)
        output1 = findcontact(jname,jp)
        if output1 != []:
            olist.append(output1)

print(olist)

outfile="./contact.json"
with open(outfile,"w") as of:
    of.write(json.dumps(olist))
of.close()
