import requests
import json
from io import BytesIO
from PIL import Image

TokenAPI = ""

def RequestGet(url):
	Header = {'Authorization' : f'token {TokenAPI}'}


	ResponseData = requests.get(url, headers=Header)
	if not ResponseData.ok:
		return None

	return json.loads(ResponseData.text)

def RequestImageGet(url, SaveLoc):
	Header = {'Authorization' : f'token {TokenAPI}'}


	ResponseData = requests.get(url, headers=Header)
	if not ResponseData.ok:
		return None

	a = Image.open(BytesIO(ResponseData.content))
	a.save(SaveLoc)
	return True

def SetTokenAPI(Token):
	global TokenAPI
	TokenAPI = Token