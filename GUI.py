import pygame
from PIL import Image
import os

#  ================ vars =======================

BackgroundColor = (240, 240, 240)
MyID = "kysth0707"

Black = (0, 0, 0)
White = (255, 255, 255)
LightGray = (195, 195, 195)
NormalGray = (180, 180, 180)
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

# ==================================================================

ImageName = ["Background", "FollowersAndFavoriteUsers", "MenuRepository", "NewRepositories", "RecentCommit", "TopCommit", "TopStar", "MyProfile"]
ImageResizeDict = {"MyProfile" : (75, 75)}
ImageDict = {}
FollowersDict = {}
FollowerKeys = []

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



	ProfileDatas = os.listdir(ReturnPos(f"\\imgs\\profiles"))
	for DataName in ProfileDatas:
		if DataName[:10] == "Followers-":
			Name = DataName[10:][:-4]
			a = Image.open(ReturnPos(f"\\imgs\\profiles\\Followers-{Name}.png"))
			

			SizeValue = HeightPercent()
			b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

			b.save(ReturnPos(f"\\imgs\\edited\\Followers-{Name}.png"))
			FollowersDict[Name] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\Followers-{Name}.png"))
			FollowerKeys.append(Name)
	# for i in range(3):


# ==================================================================


def DrawText(text, xy, Color, FontSize, IsBold = False, IsRightJustify = False):
	if IsRightJustify:
		TextImage = pygame.font.SysFont("malgungothic", int(FontSize * WidthPercent()), IsBold).render(str(text), True, Color)
		screen.blit(TextImage, ConvertWidthPercent(xy[0] - TextImage.get_size()[0], xy[1]))
	else:
		screen.blit(pygame.font.SysFont("malgungothic", int(FontSize * WidthPercent()), IsBold).render(str(text), True, Color), ConvertWidthPercent(xy[0], xy[1]))

def ShowMousePos():
	MousePos = pygame.mouse.get_pos()
	screen.blit(pygame.font.SysFont("malgungothic", 17).render(str(MousePos), True, Black), MousePos)

# ==================================================================

def DrawTopStar(x, y, RepoName, RepoOwner, StarCount):
	screen.blit(ImageDict['TopStar'], ConvertWidthPercent(x, y))
	DrawText(RepoName, (x + 20, y + 15), LightGray, 16,  True)
	DrawText(RepoOwner, (x + 20, y + 50), NormalGray, 12)
	DrawText(str(StarCount), (x + 195, y + 15), LightGray, 12, IsBold=True, IsRightJustify=True)


def DrawRepositories():
	# Top Stars
	for x in range(2):
		for y in range(2):
			DrawTopStar(380 + x * 330, 100 + y * 100, "RepoName", "RepoOwner", x * 10 + y * 100)
			
# ==================================================================

def DrawMenuUser(x, y, Name, Image):
	screen.blit(ImageDict['FollowersAndFavoriteUsers'], ConvertWidthPercent(x, y))
	screen.blit(Image, ConvertWidthPercent(x + 11, y + 10))
	if len(Name) > 6:
		Name = Name[:5]+"..."
	
	DrawText(Name, (x + 7, y + 65), NormalGray, 12,  True)

def DrawMenu():
	# Followers
	for i in range(3):
		DrawMenuUser(14 + i * 90, 170, FollowerKeys[i], FollowersDict[FollowerKeys[i]])


# ==================================================================

def DrawNotice():
	DrawText(NoticeText, (280, 10), White, 16)

def DrawProfile():
	screen.blit(ImageDict['MyProfile'], ConvertWidthPercent(20, 7))
	DrawText(MyID, (140, 30), White, 17)

def DrawScreen():
	global screen

	screen.fill(BackgroundColor)
	screen.blit(ImageDict['Background'], (0, 0))
	DrawNotice()
	DrawProfile()
	DrawRepositories()
	DrawMenu()

# ==================================================================

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