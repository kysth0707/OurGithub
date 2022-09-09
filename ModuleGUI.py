from PIL import ImageFile

from ModuleRequestFunc import RequestImageGet
ImageFile.LOAD_TRUNCATED_IMAGES = True
# 출처: https://deep-deep-deep.tistory.com/34 [딥딥딥:티스토리]

import pygame
from PIL import Image
import os
import time
from ModuleGUIFunc import LastCommitRefresh, MyRepoRefresh, ReturnLimitText, GetDatas
from ModuleRequestFunc import RequestImageGet, RequestGet
import ModuleRequest
from threading import Thread

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
	clock = None
	ImageName = ["Background", "FollowersAndFavoriteUsers", "MenuRepository", "NewRepositories", "RecentCommit", "TopCommit", "TopStar", "MyProfile", "PopUp"]
	ImageResizeDict = {"MyProfile" : (75, 75)}
	ImageDict = {}
	FollowersDict = {}
	FollowerKeys = []
	FavoriteUsersDict = {}
	FavoriteUsersKeys = []

	TopStars = []
	TopCommiters = []
	RecentCommiters = []
	RecentCommiterImgs = []

	TextImageDict = {}
	NewRepositories = []

	def ThreadMyRepo(self):
		time.sleep(1)
		a = os.listdir(ReturnPos(f"\\imgs\\profiles\\Followers"))
		for b in a:
			os.remove(ReturnPos(f"\\imgs\\profiles\\Followers\\{b}"))
		a = os.listdir(ReturnPos(f"\\imgs\\profiles\\Favorite"))
		for b in a:
			os.remove(ReturnPos(f"\\imgs\\profiles\\Favorite\\{b}"))
		ModuleRequest.GetRepoDatas(self.MyID)
		self.MyRepoStar, self.MyRepoName, self.MyRepoTime = MyRepoRefresh()
		self.LastCommitDate = LastCommitRefresh()
		self.ImageResize()

	def ThreadTopStars(self):
		self.TopStars = ModuleRequest.GetTopStar()

	def ThreadTopCommiters(self):
		self.TopCommiters = ModuleRequest.GetTopCommiters()

	def ThreadNewRepositories(self):
		self.NewRepositories = ModuleRequest.GetNewRepositories()

	def ThreadRecentCommiters(self):
		time.sleep(1)
		a = os.listdir(ReturnPos(f"\\imgs\\profiles\\RecentCommit"))
		for b in a:
			os.remove(ReturnPos(f"\\imgs\\profiles\\RecentCommit\\{b}"))
		
		self.RecentCommiters = ModuleRequest.GetRecentCommiters()
		for i in range(len(self.RecentCommiters)):
			User = self.RecentCommiters[i]['ID']
			ModuleRequest.RequestImageGet(ModuleRequest.GetUserData(User)['avatar_url'], ReturnPos(f"\\imgs\\profiles\\RecentCommit\\{i}.png"))

	def __init__(self, ID) -> None:
		self.MyID = ID
		# ModuleRequest.GetRepoDatas(ID)
		# 나중에 .txt 말고 변수로 저장하게 변경시키기
		self.MyRepoStar, self.MyRepoName, self.MyRepoTime = MyRepoRefresh()
		self.LastCommitDate = LastCommitRefresh()

		functions = [self.ThreadMyRepo, self.ThreadTopStars, self.ThreadTopCommiters, self.ThreadNewRepositories, self.ThreadRecentCommiters]
		for i in range(len(functions)):
			temp = Thread(target=functions[i], daemon=True)
			temp.start()

		pygame.init()

		self.clock = pygame.time.Clock()

		self.ScreenWidth = 1000
		self.ScreenHeight = 800
		self.screen = pygame.display.set_mode((self.ScreenWidth, self.ScreenHeight), pygame.RESIZABLE)

		self.ImageResize()


	# ==================================================

	def GetLastCommit(self):
		return self.LastCommitDate


	#  =============================================


	def WidthPercent(self):
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

			SizeValue = (self.WidthPercent())
			if ImgName in self.ImageResizeDict:
				b = a.resize((int(SizeValue * self.ImageResizeDict[ImgName][0]), int(SizeValue * self.ImageResizeDict[ImgName][1])))
			else:
				b = a.resize((int(SizeValue * a.size[0]), int(SizeValue * a.size[1])))

			b.save(ReturnPos(f"\\imgs\\edited\\{ImgName}.png"))
			self.ImageDict[ImgName] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\{ImgName}.png"))



		ProfileDatas = os.listdir(ReturnPos(f"\\imgs\\profiles\\Followers"))
		for DataName in ProfileDatas:
			Name = DataName[:-4]
			a = Image.open(ReturnPos(f"\\imgs\\profiles\\Followers\\{Name}.png"))
			

			SizeValue = self.WidthPercent()
			b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

			b.save(ReturnPos(f"\\imgs\\edited\\Followers\\{Name}.png"))
			self.FollowersDict[Name] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\Followers\\{Name}.png"))
			self.FollowerKeys.append(Name)

		ProfileDatas = os.listdir(ReturnPos(f"\\imgs\\profiles\\Favorite"))
		for DataName in ProfileDatas:
				Name = DataName[:-4]
				a = Image.open(ReturnPos(f"\\imgs\\profiles\\Favorite\\{Name}.png"))
				

				SizeValue = self.WidthPercent()
				b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

				b.save(ReturnPos(f"\\imgs\\edited\\Favorite\\{Name}.png"))
				self.FavoriteUsersDict[Name] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\Favorite\\{Name}.png"))
				self.FavoriteUsersKeys.append(Name)

		ProfileDatas = os.listdir(ReturnPos(f"\\imgs\\profiles\\RecentCommit"))
		for DataName in ProfileDatas:
				Name = DataName[:-4]
				a = Image.open(ReturnPos(f"\\imgs\\profiles\\RecentCommit\\{Name}.png"))
				

				SizeValue = self.WidthPercent()
				b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

				b.save(ReturnPos(f"\\imgs\\edited\\RecentCommit\\{Name}.png"))
				self.RecentCommiterImgs.append(pygame.image.load(ReturnPos(f"\\imgs\\edited\\RecentCommit\\{Name}.png")))


	# ==================================================================


	def DrawText(self, text, xy, Color, FontSize, IsBold = False, IsRightJustify = False):
		ImageDictFormat = f"{xy}{text}{self.WidthPercent()}"
		if not ImageDictFormat in self.TextImageDict:
			self.TextImageDict[ImageDictFormat] = pygame.font.SysFont("malgungothic", int(FontSize * self.WidthPercent()), IsBold).render(str(text), True, Color)
		# 없으면 새로 렌더하고 있으면 그대로 쓰기

		if IsRightJustify:
			self.screen.blit(self.TextImageDict[ImageDictFormat], self.ConvertWidthPercent(xy[0] - self.TextImageDict[ImageDictFormat].get_size()[0], xy[1]))
		else:
			self.screen.blit(self.TextImageDict[ImageDictFormat], self.ConvertWidthPercent(xy[0], xy[1]))

	def ShowMousePos(self):
		MousePos = pygame.mouse.get_pos()
		self.screen.blit(pygame.font.SysFont("malgungothic", 17).render(str(MousePos), True, self.Black), MousePos)

	# ==================================================================

	def DrawTopStar(self, x, y, RepoName, RepoOwner, StarCount):
		self.screen.blit(self.ImageDict['TopStar'], self.ConvertWidthPercent(x, y))
		self.DrawText(RepoName, (x + 20, y + 15), self.LightGray, 16,  True)
		self.DrawText(RepoOwner, (x + 20, y + 50), self.NormalGray, 12)
		self.DrawText(str(StarCount), (x + 195, y + 15), self.LightGray, 12, IsBold=True, IsRightJustify=True)

	def DrawTopCommiter(self, x, y, RepoName, RepoOwner, DayData):
		self.screen.blit(self.ImageDict['TopCommit'], self.ConvertWidthPercent(x, y))
		self.DrawText(RepoName, (x + 20, y + 15), self.LightGray, 16,  True)
		self.DrawText(RepoOwner, (x + 20, y + 50), self.NormalGray, 12)
		

		if DayData != "?":
			Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
			for i in range(7):
				val = self.ConvertWidthPercent(141 + x + i * 8, y + 16)
				x2, y2 = val[0], val[1]
				pygame.draw.rect(self.screen, (40, 255 - int(DayData[Days[i]]) * 20, 40) , [x2, y2, 7 * self.WidthPercent(), 47 * self.WidthPercent()])
				# self.DrawText(DayData[Days[i]], (x2, y2), self.NormalGray, 12)

	def DrawNewRepository(self, x, y, RepoName, ID, StarCount):
		self.screen.blit(self.ImageDict['NewRepositories'], self.ConvertWidthPercent(x, y))
		self.DrawText(RepoName, (x + 20, y + 13), self.LightGray, 16,  True)
		self.DrawText(ID, (x + 20, y + 42), self.NormalGray, 12)
		self.DrawText(str(StarCount), (x + 170, y + 12), self.NormalGray, 12, IsBold=True, IsRightJustify=True)

	def DrawRecentCommit(self, x, y, ID, RepoName, Date, i = None):
		ID = ReturnLimitText(ID, 7)
		RepoName = ReturnLimitText(RepoName, 5)
		Date = Date[2:10].replace('-','.')
		
		self.screen.blit(self.ImageDict['RecentCommit'], self.ConvertWidthPercent(x, y))
		self.DrawText(Date, (x + 7, y + 63), self.NormalGray, 13)
		self.DrawText(RepoName, (x + 10, y + 87), self.NormalGray, 13)
		self.DrawText(ID, (x + 10, y + 123), self.NormalGray, 13)

		if i == None:
			return
		self.screen.blit(self.RecentCommiterImgs[i], self.ConvertWidthPercent(x + 10, y + 10))
		

	def DrawRepositories(self):
		# Top Stars
		i = 0
		for x in range(2):
			for y in range(2):
				try:
					RepoName = self.TopStars[i]['RepoName']
					RepoOwner = self.TopStars[i]['ID']
					Star = self.TopStars[i]['Star']
					self.DrawTopStar(380 + x * 330, 100 + y * 100 + self.AnimationValue(), RepoName, RepoOwner, Star)
				except:
					self.DrawTopStar(380 + x * 330, 100 + y * 100 + self.AnimationValue(), "?", "?", "?")
				i += 1

		# Top Commiters
		i = 0
		for x in range(2):
			for y in range(2):
				try:
					Commiter = self.TopCommiters[i]['ID']
					Sum = f"총 {self.TopCommiters[i]['Sum']} 회"
					self.DrawTopCommiter(380 + x * 330, 380 + y * 100 + self.AnimationValue(), Commiter, Sum, self.TopCommiters[i])
				except:
					self.DrawTopCommiter(380 + x * 330, 380 + y * 100 + self.AnimationValue(), "?", "?", "?")
				i += 1

		# Recent Commits
		for i in range(4):
			try:
				self.DrawRecentCommit(322 + i * 75, 643 + self.AnimationValue(), self.RecentCommiters[i]['ID'], self.RecentCommiters[i]['RepoName'], self.RecentCommiters[i]['LastCommit'], i)
			except:
				self.DrawRecentCommit(322 + i * 75, 643 + self.AnimationValue(), "?", "?", "?")
		
		# New Repsoitories
		for i in range(2):
			try:
				self.DrawNewRepository(750, 650 + i * 80, self.NewRepositories[i]['RepoName'], self.NewRepositories[i]['ID'], self.NewRepositories[i]['Star'])
			except:
				self.DrawNewRepository(750, 650 + i * 80, "?", "?", "?")
				
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
			try:
				self.DrawMenuUser(14 + i * 90, 170 + self.AnimationValue(), self.FollowerKeys[i], self.FollowersDict[self.FollowerKeys[i]])
			except:
				pass

		# Repositories
		for i in range(4):
			try:
				self.DrawMenuRepository(14, 325 + self.AnimationValue() + i * 67, self.MyRepoName[i], self.MyID, self.MyRepoStar[i])
			except:
				self.DrawMenuRepository(14, 325 + self.AnimationValue() + i * 67, "?", "?", "?")

		# Favorites
		for i in range(3):
			try:
				self.DrawMenuUser(14 + i * 90, 630 + self.AnimationValue(), self.FavoriteUsersKeys[i], self.FavoriteUsersDict[self.FavoriteUsersKeys[i]])
			except:
				pass


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
		self.clock.tick(60)
		
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
				raise
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