import pygame
from PIL import Image
import os
import time
from ModuleGUIFunc import LastCommitRefresh, MyRepoRefresh, ReturnLimitText, GetDatas

def ReturnPos(loc : str):
	return os.getcwd() + loc

class OutGithubGUI:
	Run = True
	LastCommitDate = None
	MyRepoStar, MyRepoName, MyRepoTime = None, None, None

	BackgroundColor = (240, 240, 240)
	MyID = "kysth0707"

	Black = (0, 0, 0)
	White = (255, 255, 255)
	LightGray = (195, 195, 195)
	NormalGray = (180, 180, 180)
	NoticeText = f"[ 공지 ]   공지 테스트"

	screen, ScreenHeight, ScreenWidth = None, None, None
	ImageName = ["Background", "FollowersAndFavoriteUsers", "MenuRepository", "NewRepositories", "RecentCommit", "TopCommit", "TopStar", "MyProfile", "PopUp"]
	ImageResizeDict = {"MyProfile" : (75, 75)}
	ImageDict = {}
	FollowersDict = {}
	FollowerKeys = []
	FavoriteUsersDict = {}
	FavoriteUsersKeys = []

	def __init__(self) -> None:
		self.LastCommitDate = LastCommitRefresh()		
		self.MyRepoStar, self.MyRepoName, self.MyRepoTime = MyRepoRefresh()

		pygame.init()

		self.ScreenWidth = 1000
		self.ScreenHeight = 800
		self.screen = pygame.display.set_mode((self.ScreenWidth, self.ScreenHeight), pygame.RESIZABLE)

		self.ImageResize()

	# ==================================================

	def GetLastCommit(self):
		return self.LastCommitDate


	#  =============================================


	def HeightPercent(self):
		return self.ScreenHeight / 800

	def WidthPercent(self):
		return self.ScreenWidth / 1000

	def ConvertWidthPercent(self, x, y):
		return (int(x * self.WidthPercent()), int(y * self.WidthPercent()))

	def RefreshCurrentSize(self):
		self.ScreenWidth, self.ScreenHeight = pygame.display.get_surface().get_size()

	# ==================================================================

	def ImageResize(self):
		self.RefreshCurrentSize()

		for ImgName in self.ImageName:
			try:
				a = Image.open(ReturnPos(f"\\imgs\\original\\{ImgName}.png"))
			except:
				a = Image.open(ReturnPos(f"\\imgs\\profiles\\{ImgName}.png"))

			SizeValue = (self.HeightPercent())
			if ImgName in self.ImageResizeDict:
				b = a.resize((int(SizeValue * self.ImageResizeDict[ImgName][0]), int(SizeValue * self.ImageResizeDict[ImgName][1])))
			else:
				b = a.resize((int(SizeValue * a.size[0]), int(SizeValue * a.size[1])))

			b.save(ReturnPos(f"\\imgs\\edited\\{ImgName}.png"))
			self.ImageDict[ImgName] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\{ImgName}.png"))



		ProfileDatas = os.listdir(ReturnPos(f"\\imgs\\profiles"))
		for DataName in ProfileDatas:
			if DataName[:10] == "Followers-":
				Name = DataName[10:][:-4]
				a = Image.open(ReturnPos(f"\\imgs\\profiles\\Followers-{Name}.png"))
				

				SizeValue = self.HeightPercent()
				b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

				b.save(ReturnPos(f"\\imgs\\edited\\Followers-{Name}.png"))
				self.FollowersDict[Name] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\Followers-{Name}.png"))
				self.FollowerKeys.append(Name)

			elif DataName[:9] == "Favorite-":
				Name = DataName[9:][:-4]
				a = Image.open(ReturnPos(f"\\imgs\\profiles\\Favorite-{Name}.png"))
				

				SizeValue = self.HeightPercent()
				b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

				b.save(ReturnPos(f"\\imgs\\edited\\Favorite-{Name}.png"))
				self.FavoriteUsersDict[Name] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\Favorite-{Name}.png"))
				self.FavoriteUsersKeys.append(Name)


	# ==================================================================


	def DrawText(self, text, xy, Color, FontSize, IsBold = False, IsRightJustify = False):
		if IsRightJustify:
			TextImage = pygame.font.SysFont("malgungothic", int(FontSize * self.WidthPercent()), IsBold).render(str(text), True, Color)
			self.screen.blit(TextImage, self.ConvertWidthPercent(xy[0] - TextImage.get_size()[0], xy[1]))
		else:
			self.screen.blit(pygame.font.SysFont("malgungothic", int(FontSize * self.WidthPercent()), IsBold).render(str(text), True, Color), self.ConvertWidthPercent(xy[0], xy[1]))

	def ShowMousePos(self):
		MousePos = pygame.mouse.get_pos()
		self.screen.blit(pygame.font.SysFont("malgungothic", 17).render(str(MousePos), True, self.Black), MousePos)

	# ==================================================================

	def DrawTopStar(self, x, y, RepoName, RepoOwner, StarCount):
		self.screen.blit(self.ImageDict['TopStar'], self.ConvertWidthPercent(x, y))
		self.DrawText(RepoName, (x + 20, y + 15), self.LightGray, 16,  True)
		self.DrawText(RepoOwner, (x + 20, y + 50), self.NormalGray, 12)
		self.DrawText(str(StarCount), (x + 195, y + 15), self.LightGray, 12, IsBold=True, IsRightJustify=True)


	def DrawRepositories(self):
		# Top Stars
		for x in range(2):
			for y in range(2):
				self.DrawTopStar(380 + x * 330, 100 + y * 100 + self.AnimationValue(), "RepoName", "RepoOwner", x * 10 + y * 100)
				
	# ==================================================================

	def DrawMenuUser(self, x, y, Name, Image):
		Name = ReturnLimitText(Name, 5)
		self.screen.blit(self.ImageDict['FollowersAndFavoriteUsers'], self.ConvertWidthPercent(x, y))
		self.screen.blit(Image, self.ConvertWidthPercent(x + 11, y + 10))
		
		self.DrawText(Name, (x + 7, y + 65), self.NormalGray, 12,  True)

	def DrawMenuRepository(self, x, y, RepoName, RepoOwner, StarCount):
		RepoName = ReturnLimitText(RepoName, 10)
		RepoOwner = ReturnLimitText(RepoOwner, 10)
		self.screen.blit(self.ImageDict['MenuRepository'], self.ConvertWidthPercent(x, y))
		self.DrawText(RepoName, (x + 10, y + 7), self.LightGray, 16,  True)
		self.DrawText(RepoOwner, (x + 10, y + 33), self.NormalGray, 12)
		self.DrawText(str(StarCount), (x + 145, y + 10), self.LightGray, 12, IsBold=True, IsRightJustify=True)

	def DrawMenu(self):
		# LastCommit
		self.DrawText(str(self.LastCommitDate).split(' ')[0], (250, 99), self.White, 20, IsRightJustify=True)
		
		# Followers
		for i in range(3):
			self.DrawMenuUser(14 + i * 90, 170 + self.AnimationValue(), self.FollowerKeys[i], self.FollowersDict[self.FollowerKeys[i]])

		# Repositories
		LoopCnt = 4
		if len(self.MyRepoName) < 4:
			LoopCnt = len(self.MyRepoName)
		for i in range(4):
			try:
				self.DrawMenuRepository(14, 325 + self.AnimationValue() + i * 67, self.MyRepoName[i], self.MyID, self.MyRepoStar[i])
			except:
				self.DrawMenuRepository(14, 325 + self.AnimationValue() + i * 67, "?", "?", "?")

		# Favorites
		for i in range(3):
			self.DrawMenuUser(14 + i * 90, 630 + self.AnimationValue(), self.FavoriteUsersKeys[i], self.FavoriteUsersDict[self.FavoriteUsersKeys[i]])


	# ==================================================================

	def DrawNotice(self):
		self.DrawText(self.NoticeText, (280, 10), self.White, 16)

	def DrawProfile(self):
		self.screen.blit(self.ImageDict['MyProfile'], self.ConvertWidthPercent(20, 7 + self.AnimationValue()))
		self.DrawText(self.MyID, (140, 30 + self.AnimationValue()), self.White, 17)

	def DrawScreen(self):
		self.screen.fill(self.BackgroundColor)
		self.screen.blit(self.ImageDict['Background'], (0, 0))
		self.DrawNotice()
		self.DrawProfile()
		self.DrawRepositories()
		self.DrawMenu()

		self.DrawPopUp()

	# ==================================================================

	IsPopUp = False

	def PopUp(self, Title, Subtitle):
		self.IsPopUp = True
		pass

	def DrawPopUp(self):
		if self.IsPopUp:
			self.screen.blit(self.ImageDict['PopUp'], (0, 0))

	# ==================================================================

	IsAnimation = False
	AniYValue = 10
	AniTargetValue = 0
	StartTime = time.time()

	def AnimationValue(self):
		if self.IsAnimation:
			return self.AniYValue
		else:
			return 0

	def MathLerp(a, b, t):
		return a + (b - a) * t

	# ==================================================================
	
	def Update(self):
		if self.IsAnimation:
			self.AniYValue = self.MathLerp(self.AniYValue, self.AniTargetValue, 0.1)
			if time.time() - self.StartTime > 1:
				self.IsAnimation = False

		self.DrawScreen()

		self.ShowMousePos()

		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Run = False
				pygame.quit()

			elif event.type == pygame.VIDEORESIZE:
				LastScreen = (self.ScreenWidth, self.ScreenHeight)
				self.RefreshCurrentSize()
				if LastScreen[0] == self.ScreenWidth:
					self.ScreenWidth = int(self.ScreenHeight / 8 * 10)
				elif LastScreen[1] == self.ScreenHeight:
					self.ScreenHeight = int(self.ScreenWidth / 10 * 8)
				else:
					self.ScreenHeight = int(self.ScreenWidth / 10 * 8)
				self.screen = pygame.display.set_mode((self.ScreenWidth, self.ScreenHeight), pygame.RESIZABLE)
				self.ImageResize()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					if self.IsPopUp:
						self.IsPopUp = False
					else:
						self.PopUp("ㅎㅇ", "ㅎㅇ")