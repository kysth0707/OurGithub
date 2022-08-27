import requests
import json

# GithubUser = "kysth0707"
GithubUser = "banksemi"

# https://api.github.com/users/kysth0707
TestLink = f"https://api.github.com/users/{GithubUser}/repos"
ResponseData = requests.get(TestLink)

ResponseJsonData = json.loads(ResponseData.text)

for i in range(len(ResponseJsonData)):
	print(f"{ResponseJsonData[i]['name']} / fork : {ResponseJsonData[i]['fork']}")