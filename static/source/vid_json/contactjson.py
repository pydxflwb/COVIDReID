import os, sys
import json

path = sys.argv[0]
path0 = path.split('\\')[:-1]
path1=''

for i in range(len(path0)):
    path1 =  path1+path0[i]+'\\'

contactfilename = "contact.json"

path1 = path1 + contactfilename

with open(path1,"r") as f:
    contactdata = json.load(f)
f.close()

print(contactdata[0][2])

