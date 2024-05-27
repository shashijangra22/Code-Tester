from bs4 import BeautifulSoup as bs
import requests
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument(
    "-f", "--file", help="Enter path of file to be tested", required=True)
args = vars(ap.parse_args())

def getUrlFromFile():
    f = open(args["file"], "r")
    URL = f.read().split('\n')[0]
    f.close()
    pos = URL.find("http")
    if pos != -1:
        return URL[pos:]
    return None


args["url"] = getUrlFromFile()


def getTests():
    inputs, outputs = [], []
    res = requests.get(args["url"]).text
    soup = bs(res, 'html.parser')

    def scrapeInputText(div):
        ans = [i.text for i in div.find('pre').children]
        return "\n".join(ans).strip()

    def scrapeOutputText(div):
        return div.find('pre').text.strip()

    inputDiv = soup.find_all('div', {"class": "input"})
    outputDiv = soup.find_all('div', {"class": "output"})
    for x in range(len(inputDiv)):
        inputs.append(scrapeInputText(inputDiv[x]))
        outputs.append(scrapeOutputText(outputDiv[x]))
    for ind in range(len(inputs)):
        with open("test-"+str(ind+1)+".in", "w") as f:
            f.write(inputs[ind])
        with open("test-"+str(ind+1)+".out", "w") as f:
            f.write(outputs[ind])
    os.chdir("..")


try:
    dirName = args["url"].split('/')[-1]+"test"
except:
    print("Invalid URL!")
    exit()

if os.path.exists(dirName):
    print("Directory already exists! Reading from Directory...")
else:
    print("Fetching sample tests from server...")
    os.mkdir(dirName)
    os.chdir(dirName)
    getTests()

tests = sorted([file.split('.')[0]
               for file in os.listdir(dirName) if 'in' in file])

ext = args["file"][args["file"].find('.'):]


def getCommand(ext, test):
    if ext == ".cpp":
        return "./a.out" + " < " + dirName + "/" + test + ".in > " + dirName + "/my" + test + ".out"
    elif ext == ".py":
        return "python3 " + args["file"] + " < " + dirName + "/" + test + ".in > " + dirName + "/my" + test + ".out"


commands = ""
if ext == ".cpp":
    command = "g++ " + args["file"] + " -std=c++17"
    print("Compiling source code...")
    os.system(command)
elif ext == ".py":
    pass
else:
    print("[Error]: Language not supported!")
    exit()

for test in tests:
    print("\nRunning", test, "=>", end=" ")
    command = getCommand(ext, test)
    op = os.system(command)
    expectedFile = open(dirName+'/'+test+'.out', "r")
    myresultFile = open(dirName+'/my'+test+'.out', "r")
    expected = expectedFile.read().strip()
    myresult = myresultFile.read().strip()
    if (expected == myresult):
        print("Passed!")
    else:
        print("Failed !!!")
        print("\nInput\n")
        print(open(dirName+'/'+test+'.in').read().strip())
        print("\nExpected Output\n")
        print(expected)
        print("\nMy Output\n")
        print(myresult)
    expectedFile.close()
    myresultFile.close()
