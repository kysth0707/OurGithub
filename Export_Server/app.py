from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import ModuleDB

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

def IsAvailable(text):
	AvailableList = "abcdefghijklmnopqrstuvwxyz0123456789!_"
	AvailableList = list(AvailableList)
	for txt in text:
		if txt in AvailableList:
			return True
		else:
			return False


@app.get('/')
def a():
	return '/docs'

@app.get('/repos/{ID}/') #get repo
def b(ID, request : Request):
	# IP : request.client.host
	if IsAvailable(str(ID)):
		return ModuleDB.GetRepoDatas(str(ID))
	else:
		return False

@app.get('/contris/{ID}/') #get repo
def b(ID, request : Request):
	# IP : request.client.host
	if IsAvailable(str(ID)):
		return ModuleDB.GetContributions(str(ID))
	else:
		return False


@app.get('/topstars/') #get repo
def c( request : Request):
	# IP : request.client.host
	return ModuleDB.GetTopStars()

@app.get('/topcommiters/') #get repo
def c( request : Request):
	# IP : request.client.host
	return ModuleDB.GetTopCommiters()

@app.get('/recentcommits/') #get repo
def d(request : Request):
	# IP : request.client.host
	return ModuleDB.GetRecentCommits()

@app.get('/newrepos/') #get repo
def e(request : Request):
	# IP : request.client.host
	return ModuleDB.GetNewRepos()


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)