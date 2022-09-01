import time
from threading import Thread

def GUIThread():
	import ModuleGUI

temp = Thread(target=GUIThread)
# temp.daemon = True
temp.start()

# Infinity Loop
