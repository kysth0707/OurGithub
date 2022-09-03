# contributions main

import requests
import datetime
from bs4 import BeautifulSoup

Response = requests.get("https://github.com/kysth0707")
soup = BeautifulSoup(Response.text, 'html.parser')

today = str(datetime.date.today().strftime("%Y-%m-%d"))
yesterday = str((datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

DOF = datetime.date.weekday(datetime.date.today())
# Day of Week
Monday = (datetime.date.today() - datetime.timedelta(days=DOF))

ThisWeeks = []
WeekName = ['월' , '화','수','목','금','토','일']
for i in range(7):
	ThisWeeks.append((Monday + datetime.timedelta(days = i)).strftime("%Y-%m-%d"))

Contributions = {}
datas = soup.select("#js-pjax-container > div.container-xl.px-3.px-md-4.px-lg-5 > div > div.Layout-main > div:nth-child(2) > div > div.mt-4.position-relative > div.js-yearly-contributions > div > div > div > svg")
datas = str(datas).split('\n')
for data in datas:
	for i in range(7):
		if ThisWeeks[i] in data:
			ContributionValue = data[data.find("data-count") + 12:data.find("data-date") - 2]
			Contributions[i] = ContributionValue

for i in range(7):
	if i in Contributions:
		print(f"{ThisWeeks[i]} / {WeekName[i]} : {Contributions[i]}")
	else:
		print(f"{ThisWeeks[i]} / {WeekName[i]} : 0")