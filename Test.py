from bs4 import BeautifulSoup as bs
import urllib.request
import argparse
import sys
import os

ap = argparse.ArgumentParser()
ap.add_argument("-u","--url",help="Enter URL to the problem",required=True)
ap.add_argument("-f","--file",help="Enter path of file to be tested",required=True)
args = vars(ap.parse_args())

def getTests():
    inputs,outputs = [],[]
    source = urllib.request.urlopen(args["url"]).read()
    soup = bs(source,"lxml")

    def scrapeText(div):
        temp = str(div.find('pre'))
        temp = temp.replace("<pre>","").replace("</pre>","").replace("<br/>","\n")
        return temp

    inputDiv = soup.find_all('div',{"class":"input"})
    outputDiv = soup.find_all('div',{"class":"output"})

    for x in range(len(inputDiv)):
        inputs.append(scrapeText(inputDiv[x]))
        outputs.append(scrapeText(outputDiv[x]))
    for ind in range(len(inputs)):
        with open("test-"+str(ind+1)+".in","w") as f:
            f.write(inputs[ind])
        with open("test-"+str(ind+1)+".out","w") as f:
            f.write(outputs[ind])
    os.chdir("..")

dirName = args["url"].split('/')[-1]+"test"

if os.path.exists(dirName):
    print("Directory already exists! Reading from Directory...")
else:
    print("Fetching sample tests from server...")
    os.mkdir(dirName)
    os.chdir(dirName)
    getTests()

tests = [file.split('.')[0] for file in os.listdir(dirName) if 'in' in file]

for test in tests:
    print("\nRunning",test,"=>",end=" ")
    command = "python3 " + args["file"] + " < " + dirName + "/" + test + ".in > " + dirName + "/my" + test + ".out" 
    op  = os.system(command)
    expected = open(dirName+'/'+test+'.out').read().strip()
    myresult = open(dirName+'/my'+test+'.out').read().strip()
    if(expected==myresult):
        print("Passed!")
    else:
        print("Failed !!!")
        print("\nInput\n")
        print(open(dirName+'/'+test+'.in').read().strip())
        print("\nExpected Output\n")
        print(expected)
        print("\nMy Output\n")
        print(myresult)