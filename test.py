# from ModuleRequestFunc import RequestGet, SetTokenAPI

# GithubAPIToken = ""
# with open("E:\\GithubProjects\\githubapitoken.txt", "r", encoding="utf-8") as f:
# 	GithubAPIToken = f.readline()
# 	SetTokenAPI(GithubAPIToken)

# GithubUser = "kysth0707"

# Commits = RequestGet(f"https://api.github.com/repos/{GithubUser}/41x41display/commits")

# print(Commits[0]['commit']['author']['date']) # 가장 최근꺼임

# # Branch test


# Auto Download Test

import requests
import os
import zipfile

def ReturnPos(loc : str):
	return os.getcwd() + loc

url = "https://github.com/kysth0707/OurGithub/releases/download/v1.0/OurGithub_v1.0.zip"
DownloadLoc = '\\AutoUpdate'


response = requests.get(url)

try:
	os.remove(ReturnPos(DownloadLoc))
except:
	pass

open(ReturnPos(DownloadLoc+"\\Download\\temp.zip"), "wb").write(response.content)

MyZip = zipfile.ZipFile(ReturnPos(DownloadLoc+"\\Download\\temp.zip"))
MyZip.extractall(ReturnPos(DownloadLoc+"\\Download"))

Files = os.listdir(ReturnPos(DownloadLoc+"\\Download"))
FileName = ""
for Name in Files:
	if Name != "temp.zip":
		FileName = Name

MyZip = zipfile.ZipFile(ReturnPos(DownloadLoc+"\\Download\\"+FileName))
MyZip.extractall(ReturnPos(DownloadLoc+"\\ZipExtract"))