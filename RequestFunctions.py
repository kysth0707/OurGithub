import requests
import json

TokenAPI = ""

def RequestGet(url):
	Header = {'Authorization' : f'token {TokenAPI}'}


	ResponseData = requests.get(url, headers=Header)
	if not ResponseData.ok:
		return None

	return json.loads(ResponseData.text)

def SetTokenAPI(Token):
	global TokenAPI
	TokenAPI = Token