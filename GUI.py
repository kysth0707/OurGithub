import pygame
from PIL import Image
import os

import GUIVariables as var

pygame.init()

ScreenWidth = 1000
ScreenHeight = 800
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), pygame.RESIZABLE)


def HeightPercent():
	return ScreenHeight / 800

def WidthPercent():
	return ScreenWidth / 1000

def ReturnPos(loc : str):
	return os.getcwd() + loc

def RefreshCurrentSize():
	global ScreenWidth, ScreenHeight
	ScreenWidth, ScreenHeight = pygame.display.get_surface().get_size()

ImageName = ["Background", "FollowersAndFavoriteUsers", "MenuRepository", "NewRepositories", "RecentCommit", "TopCommit", "TopStar"]
ImageDict = {}

def ImageResize():
	global ImageName, ImageDict
	RefreshCurrentSize()

	for ImgName in ImageName:
		a = Image.open(ReturnPos(f"\\imgs\\original\\{ImgName}.png"))
		SizeValue = (HeightPercent())
		b = a.resize((int(SizeValue * a.size[0]), int(SizeValue * a.size[1])))

		b.save(ReturnPos(f"\\imgs\\edited\\{ImgName}.png"))
		ImageDict[ImgName] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\{ImgName}.png"))



def DrawScreen():
	global screen

	screen.fill(var.BackgroundColor)
	screen.blit(ImageDict['Background'], (0, 0))

ImageResize()
Run = True
while Run:
	DrawScreen()

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