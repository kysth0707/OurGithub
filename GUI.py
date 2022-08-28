import pygame
from PIL import Image
import os

import GUIVariables as var

pygame.init()

ScreenWidth = 1000
ScreenHeight = 800
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight), pygame.RESIZABLE)


def HeightPercent():
	return ScreenHeight / 1000

def WidthPercent():
	return ScreenHeight / 1000

def ReturnPos(loc : str):
	return os.getcwd() + loc

def RefreshCurrentSize():
	global ScreenWidth, ScreenHeight
	ScreenWidth, ScreenHeight = pygame.display.get_surface().get_size()

ImageName = []
ImageDict = {}

def ImageResize():
	global ImageName, ImageDict
	RefreshCurrentSize()

	for ImgName in ImageName:
		a = Image.open(ReturnPos(f"\\img\\original\\{ImgName}.png"))
		SizeValue = HeightPercent()
		b = a.resize((SizeValue, SizeValue))

		b.save(ReturnPos(f"\\img\\edited\\{ImgName}.png"))
		ImageDict[ImgName] = pygame.image.load(ReturnPos(f"\\img\\edited\\{ImgName}.png"))



def DrawScreen():
	global screen

	screen.fill(var.BackgroundColor)

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
			ImageResize()