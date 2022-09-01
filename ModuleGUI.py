import pygame
from PIL import Image
import os
import time
from ModuleGUIFunc import LastCommitRefresh, MyRepoRefresh, ReturnLimitText, GetDatas

Run = True

def ReturnPos(loc : str):
	return os.getcwd() + loc

# =================================================

# def GetFavoriteUsers():
# 	return FavoriteUsers

# f = open(ReturnPos(f"\\Datas\\FavoriteUsers.txt"), "r", encoding="utf-8")
# FavoriteUsers = []
# Datas = f.readlines()
# for i in range(len(Datas)):
# 	if i >= 3:
# 		break
# 	FavoriteUsers.append(Datas[i][:-1])
# f.close()

# ==================================================

def GetLastCommit():
	return LastCommitDate

LastCommitDate = LastCommitRefresh()

# ==================================================

MyRepoStar, MyRepoName, MyRepoTime = MyRepoRefresh()

#  ================ vars =======================

BackgroundColor = (240, 240, 240)
# MyID = "kysth0707"

Black = (0, 0, 0)
White = (255, 255, 255)
LightGray = (195, 195, 195)
NormalGray = (180, 180, 180)
# NoticeText = f"[ 공지 ]   공지 테스트"

MyID, NoticeText = GetDatas()

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

def RefreshCurrentSize():
	global ScreenWidth, ScreenHeight
	ScreenWidth, ScreenHeight = pygame.display.get_surface().get_size()

# ==================================================================

ImageName = ["Background", "FollowersAndFavoriteUsers", "MenuRepository", "NewRepositories", "RecentCommit", "TopCommit", "TopStar", "MyProfile", "PopUp"]
ImageResizeDict = {"MyProfile" : (75, 75)}
ImageDict = {}
FollowersDict = {}
FollowerKeys = []
FavoriteUsersDict = {}
FavoriteUsersKeys = []

def ImageResize():
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

		elif DataName[:9] == "Favorite-":
			Name = DataName[9:][:-4]
			a = Image.open(ReturnPos(f"\\imgs\\profiles\\Favorite-{Name}.png"))
			

			SizeValue = HeightPercent()
			b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

			b.save(ReturnPos(f"\\imgs\\edited\\Favorite-{Name}.png"))
			FavoriteUsersDict[Name] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\Favorite-{Name}.png"))
			FavoriteUsersKeys.append(Name)


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
			DrawTopStar(380 + x * 330, 100 + y * 100 + AnimationValue(), "RepoName", "RepoOwner", x * 10 + y * 100)
			
# ==================================================================

def DrawMenuUser(x, y, Name, Image):
	Name = ReturnLimitText(Name, 5)
	screen.blit(ImageDict['FollowersAndFavoriteUsers'], ConvertWidthPercent(x, y))
	screen.blit(Image, ConvertWidthPercent(x + 11, y + 10))
	
	DrawText(Name, (x + 7, y + 65), NormalGray, 12,  True)

def DrawMenuRepository(x, y, RepoName, RepoOwner, StarCount):
	RepoName = ReturnLimitText(RepoName, 10)
	RepoOwner = ReturnLimitText(RepoOwner, 10)
	screen.blit(ImageDict['MenuRepository'], ConvertWidthPercent(x, y))
	DrawText(RepoName, (x + 10, y + 7), LightGray, 16,  True)
	DrawText(RepoOwner, (x + 10, y + 33), NormalGray, 12)
	DrawText(str(StarCount), (x + 145, y + 10), LightGray, 12, IsBold=True, IsRightJustify=True)

def DrawMenu():
	# LastCommit
	DrawText(str(LastCommitDate).split(' ')[0], (250, 99), White, 20, IsRightJustify=True)
	
	# Followers
	for i in range(3):
		DrawMenuUser(14 + i * 90, 170 + AnimationValue(), FollowerKeys[i], FollowersDict[FollowerKeys[i]])

	# Repositories
	LoopCnt = 4
	if len(MyRepoName) < 4:
		LoopCnt = len(MyRepoName)
	for i in range(4):
		DrawMenuRepository(14, 325 + AnimationValue() + i * 67, MyRepoName[i], MyID, MyRepoStar[i])

	# Favorites
	for i in range(3):
		DrawMenuUser(14 + i * 90, 630 + AnimationValue(), FavoriteUsersKeys[i], FavoriteUsersDict[FavoriteUsersKeys[i]])


# ==================================================================

def DrawNotice():
	DrawText(NoticeText, (280, 10), White, 16)

def DrawProfile():
	screen.blit(ImageDict['MyProfile'], ConvertWidthPercent(20, 7 + AnimationValue()))
	DrawText(MyID, (140, 30 + AnimationValue()), White, 17)

def DrawScreen():
	global screen

	screen.fill(BackgroundColor)
	screen.blit(ImageDict['Background'], (0, 0))
	DrawNotice()
	DrawProfile()
	DrawRepositories()
	DrawMenu()

	DrawPopUp()

# ==================================================================

IsPopUp = False

def PopUp(Title, Subtitle):
	global IsPopUp
	IsPopUp = True
	pass

def DrawPopUp():
	if IsPopUp:
		screen.blit(ImageDict['PopUp'], (0, 0))

# ==================================================================

IsAnimation = False
AniYValue = 10
AniTargetValue = 0
StartTime = time.time()

def AnimationValue():
	if IsAnimation:
		return AniYValue
	else:
		return 0

def MathLerp(a, b, t):
	return a + (b - a) * t

# ==================================================================

ImageResize()

LastTime = time.time()
while Run:
	if time.time() - LastTime > 5:
		MyID, NoticeText = GetDatas()
		LastTime = time.time()
	if IsAnimation:
		AniYValue = MathLerp(AniYValue, AniTargetValue, 0.1)
		if time.time() - StartTime > 1:
			IsAnimation = False

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

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if IsPopUp:
					IsPopUp = False
				else:
					PopUp("ㅎㅇ", "ㅎㅇ")