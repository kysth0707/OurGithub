import pygame
from PIL import Image
import os

#  ================ vars =======================

BackgroundColor = (240, 240, 240)
MyID = "kysth0707"

Black = (0, 0, 0)
White = (255, 255, 255)
NoticeText = f"[ 공지 ]   이번 주의 Top Commiter 은 {MyID} 님 입니다! 축하합니다!"

#  =============================================


pygame.init()

ScreenWidth = 1000
ScreenHeight = 800
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), pygame.RESIZABLE)


def HeightPercent():
	return ScreenHeight / 800

def WidthPercent():
	return ScreenWidth / 1000

def ConvertWidthPercent(x, y):
	return (int(x * WidthPercent()), int(y * WidthPercent()))

def ReturnPos(loc : str):
	return os.getcwd() + loc

def RefreshCurrentSize():
	global ScreenWidth, ScreenHeight
	ScreenWidth, ScreenHeight = pygame.display.get_surface().get_size()

ImageName = ["Background", "FollowersAndFavoriteUsers", "MenuRepository", "NewRepositories", "RecentCommit", "TopCommit", "TopStar", "MyProfile"]
ImageResizeDict = {"MyProfile" : (75, 75)}
ImageDict = {}

def ImageResize():
	global ImageName, ImageDict
	RefreshCurrentSize()

	for ImgName in ImageName:
		try:
			a = Image.open(ReturnPos(f"\\imgs\\original\\{ImgName}.png"))
		except:
			a = Image.open(ReturnPos(f"\\imgs\\profiles\\{ImgName}.png"))

		SizeValue = (HeightPercent())
		if ImgName in ImageResizeDict:
			b = a.resize((int(SizeValue * ImageResizeDict[ImgName][0]), int(SizeValue * ImageResizeDict[ImgName][1])))
		else:
			b = a.resize((int(SizeValue * a.size[0]), int(SizeValue * a.size[1])))

		b.save(ReturnPos(f"\\imgs\\edited\\{ImgName}.png"))
		ImageDict[ImgName] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\{ImgName}.png"))




def DrawText(text, xy, Color, FontSize):
	screen.blit(pygame.font.SysFont("malgungothic", FontSize).render(str(text), True, Color), (xy[0], xy[1]))

def ShowMousePos():
	MousePos = pygame.mouse.get_pos()
	DrawText(MousePos, (MousePos[0], MousePos[1] + 20), Black, 17)



def DrawNotice():
	DrawText(NoticeText, ConvertWidthPercent(280, 10), White, int(16 * WidthPercent()))

def DrawProfile():
	screen.blit(ImageDict['MyProfile'], ConvertWidthPercent(20, 7))
	DrawText(MyID, ConvertWidthPercent(140, 30), White, int(17 * WidthPercent()))

def DrawScreen():
	global screen

	screen.fill(BackgroundColor)
	screen.blit(ImageDict['Background'], (0, 0))
	DrawNotice()
	DrawProfile()

ImageResize()
Run = True
while Run:
	DrawScreen()

	ShowMousePos()

	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Run = False
			pygame.quit()

		elif event.type == pygame.VIDEORESIZE:
			LastScreen = (ScreenWidth, ScreenHeight)
			RefreshCurrentSize()
			if LastScreen[0] == ScreenWidth:
				ScreenWidth = int(ScreenHeight / 8 * 10)
			elif LastScreen[1] == ScreenHeight:
				ScreenHeight = int(ScreenWidth / 10 * 8)
			else:
				ScreenHeight = int(ScreenWidth / 10 * 8)
			screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), pygame.RESIZABLE)
			ImageResize()