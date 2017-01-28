import os
import sys
import re
import fileinput
import glob
import datetime

class converter:
    def __init__(self, projectName):
        self.folderBase = "."
        self.pn = projectName
        self.html = self.pn + ".html"
        self.filesPath = os.path.join(self.folderBase, self.pn + "_files")
        self.folderUrlPath = "http://hummingbirdzgarden.azurewebsites.net/wp-content/uploads/" + datetime.date.today().strftime("%Y") + "/" + datetime.date.today().strftime("%m") + "/"

    def RenameJpg(self):
        if os.path.exists(os.path.join(self.filesPath, "0.jpg")):
            os.rename(os.path.join(self.filesPath, "0.jpg"), os.path.join(self.filesPath, "0 [0].jpg"))
        
        for file in glob.iglob(os.path.join(self.filesPath, "*.jpg")):
            title, ext = os.path.splitext(os.path.basename(file))
            newtitle = title.replace(" [", "_")
            newtitle = newtitle.replace("]", "")
            newtitle = newtitle.replace("0_", self.pn+"_")
            os.rename(file, os.path.join(self.filesPath, newtitle+".jpg"))

    def convertSquareToUnderscoreHtml(self):
        r = re.compile("0 \[\d+\].jpg")
        file = fileinput.FileInput([self.html], inplace=True, backup=".bak")
        filearr = []
        for line in file:
            match = r.findall(line)
            if match:
                filearr = [f.replace(" [", "_") for f in match]
                filearr = [f.replace("]", "") for f in filearr]
                filearr = [f.replace("0_", self.pn+"_") for f in filearr]
                for id, f in enumerate(filearr):
                    line = line.replace(match[id], filearr[id])
                # convert the folder name into url address
                #line = line.replace(self.pn + "_files", "http://hummingbirdzgarden.azurewebsites.net/wp-content/uploads/2016/12/")
            print line
        file.close()
    
    def convertImageName(self):
        # first pass to convert 0.jpg into 0 [0].jpg
        file = fileinput.FileInput([self.html], inplace=True, backup=".bak")
        for line in file:
            print(line.replace("0.jpg", "0 [0].jpg"))
        file.close();
    
    def convertUrl(self):
        re_url = re.compile("https?://[^\s<]+")
        re_site = re.compile("www.[^\s.]+")
        file = fileinput.FileInput([self.html], inplace = True, backup=".bak")
        urls = []
        for line in file:
            match = re_url.findall(line)
            if match:
                # the first one is user url
                urls = match[1:]
                for url in urls:
                    siteName = url
                    site = re_site.search(url)                    
                    if site:
                        siteName = site.group(0)[4:]
                    newText = "<a href=\"" + url + "\"><span style=\"margin:0;padding:0;max-width:100% !important;box-sizing:border-box !important;-webkit-box-sizing:border-box !important;word-wrap:break-word !important;font-size:16px;color:rgb(0,128,255)\">" + siteName + "</span></a>"
                    line = line.replace(url, newText)
            print(line)
        file.close()
    
    def convertFolderIntoUploadUrl(self):
        r = re.compile(".jpg")
        file = fileinput.FileInput([self.html], inplace=True, backup=".bak")
        filearr = []
        for line in file:
            match = r.findall(line)
            if match:
                line = line.replace(self.pn + "_files/", self.folderUrlPath)
            print(line)
        file.close()

def main(projectName):
    conv = converter(projectName[0])

    conv.RenameJpg()
    conv.convertImageName()
    conv.convertSquareToUnderscoreHtml()

    conv.convertUrl()
    conv.convertFolderIntoUploadUrl()

if __name__ == "__main__":
    main(sys.argv[1:])