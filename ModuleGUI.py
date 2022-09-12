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
	Blue = (0, 0, 180)
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

	ThreadCount = 0
	Clicked = False

	def ThreadMyRepo(self):
		ModuleRequest.GetRepoDatas(self.MyID)
		self.MyRepoStar, self.MyRepoName, self.MyRepoTime = MyRepoRefresh()
		self.LastCommitDate = LastCommitRefresh()
		self.ThreadCount += 1

		while True:
			if self.ThreadCount >= 8:
				self.ImageResize()
				break
			time.sleep(1)

	def ThreadFavoriteUsers(self):
		a = os.listdir(ReturnPos(f"\\imgs\\profiles\\Favorite"))
		for b in a:
			os.remove(ReturnPos(f"\\imgs\\profiles\\Favorite\\{b}"))
		ModuleRequest.ThreadFavoriteUsers()
		self.ThreadCount += 1

	def ThreadFollowers(self):
		a = os.listdir(ReturnPos(f"\\imgs\\profiles\\Followers"))
		for b in a:
			os.remove(ReturnPos(f"\\imgs\\profiles\\Followers\\{b}"))
		ModuleRequest.ThreadFollowers(self.MyID)
		self.ThreadCount += 1

	def ThreadTopStars(self):
		self.TopStars = ModuleRequest.GetTopStar()
		self.ThreadCount += 1

	def ThreadTopCommiters(self):
		self.TopCommiters = ModuleRequest.GetTopCommiters()
		self.ThreadCount += 1

	def ThreadNewRepositories(self):
		self.NewRepositories = ModuleRequest.GetNewRepositories()
		self.ThreadCount += 1

	def ThreadNotice(self):
		try:
			self.NoticeText = ModuleRequest.GetNotice()['Text']
		except:
			self.NoticeText = "공지 불러오기 실패"
		self.ThreadCount += 1

	def ThreadRecentCommiters(self):
		time.sleep(1)
		a = os.listdir(ReturnPos(f"\\imgs\\profiles\\RecentCommit"))
		for b in a:
			os.remove(ReturnPos(f"\\imgs\\profiles\\RecentCommit\\{b}"))
		
		self.RecentCommiters = ModuleRequest.GetRecentCommiters()
		for i in range(len(self.RecentCommiters)):
			User = self.RecentCommiters[i]['ID']
			ModuleRequest.RequestImageGet(ModuleRequest.GetUserData(User)['avatar_url'], ReturnPos(f"\\imgs\\profiles\\RecentCommit\\{i}.png"))
		self.ThreadCount += 1

	def __init__(self, ID) -> None:
		self.MyID = ID
		# ModuleRequest.GetRepoDatas(ID)
		# 나중에 .txt 말고 변수로 저장하게 변경시키기
		self.MyRepoStar, self.MyRepoName, self.MyRepoTime = MyRepoRefresh()
		self.LastCommitDate = LastCommitRefresh()

		pygame.init()

		self.clock = pygame.time.Clock()

		self.ScreenWidth = 1000
		self.ScreenHeight = 800
		self.screen = pygame.display.set_mode((self.ScreenWidth, self.ScreenHeight), pygame.RESIZABLE)

		self.ImageResize()
		functions = [self.ThreadMyRepo, self.ThreadTopStars, self.ThreadTopCommiters, self.ThreadNewRepositories, self.ThreadRecentCommiters, self.ThreadFavoriteUsers, self.ThreadFollowers, self.ThreadNotice]
		for i in range(len(functions)):
			temp = Thread(target=functions[i], daemon=True)
			temp.start()


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

	def CheckClick(self, x1y1, x2y2):
		if not self.Clicked:
			return

		MousePos = pygame.mouse.get_pos()
		x1, y1 = self.ConvertWidthPercent(x1y1[0], x1y1[1])
		x2, y2 = self.ConvertWidthPercent(x2y2[0], x2y2[1])

		if x1 > x2:
			x1, x2 = x2, x1
		if y1 > y2:
			y1, y2 = y2, y1

		if x1 < MousePos[0] and MousePos[0] < x2:
			if y1 < MousePos[1] and MousePos[1] < y2:
				self.Clicked = False
				return True
		
		return False

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


		try:
			ProfileDatas = os.listdir(ReturnPos(f"\\imgs\\profiles\\Followers"))
			for DataName in ProfileDatas:
				Name = DataName[:-4]
				a = Image.open(ReturnPos(f"\\imgs\\profiles\\Followers\\{Name}.png"))
				

				SizeValue = self.WidthPercent()
				b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

				b.save(ReturnPos(f"\\imgs\\edited\\Followers\\{Name}.png"))
				self.FollowersDict[Name] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\Followers\\{Name}.png"))
				self.FollowerKeys.append(Name)
		except:
			pass

		try:
			ProfileDatas = os.listdir(ReturnPos(f"\\imgs\\profiles\\Favorite"))
			for DataName in ProfileDatas:
					Name = DataName[:-4]
					a = Image.open(ReturnPos(f"\\imgs\\profiles\\Favorite\\{Name}.png"))
					

					SizeValue = self.WidthPercent()
					b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

					b.save(ReturnPos(f"\\imgs\\edited\\Favorite\\{Name}.png"))
					self.FavoriteUsersDict[Name] = pygame.image.load(ReturnPos(f"\\imgs\\edited\\Favorite\\{Name}.png"))
					self.FavoriteUsersKeys.append(Name)
		except:
			pass

		try:
			self.RecentCommiterImgs = []
			for Name in range(4):
				a = Image.open(ReturnPos(f"\\imgs\\profiles\\RecentCommit\\{Name}.png"))
				

				SizeValue = self.WidthPercent()
				b = a.resize((int(SizeValue * 40), int(SizeValue * 40)))

				b.save(ReturnPos(f"\\imgs\\edited\\RecentCommit\\{Name}.png"))
				self.RecentCommiterImgs.append(pygame.image.load(ReturnPos(f"\\imgs\\edited\\RecentCommit\\{Name}.png")))
		except:
			pass


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

	def DrawTopStar(self, x, y, RepoName, RepoOwner, StarCount, LastCommit, CreateDate):
		self.screen.blit(self.ImageDict['TopStar'], self.ConvertWidthPercent(x, y))
		self.DrawText(RepoName, (x + 20, y + 15), self.LightGray, 16,  True)
		self.DrawText(RepoOwner, (x + 20, y + 50), self.NormalGray, 12)
		self.DrawText(str(StarCount), (x + 195, y + 15), self.LightGray, 12, IsBold=True, IsRightJustify=True)

		if self.CheckClick((x, y), (x + 224, y + 75)):
			if self.IsPopUp == False:
				self.PopUp(f"[ TopStar ] {RepoName} by {RepoOwner}", 
						   f"저장소 명 : {RepoName}\n\n\n저장소 소유자 : {RepoOwner}\n\n\n저장소 별 개수 : {StarCount}\n\n\n<link>https://github.com/{RepoOwner}/{RepoName}</link>\n\n생성 일자 : {CreateDate}\n\n최종 커밋 : {LastCommit}")
			# print(f"TopStar Clicked {RepoName}")

	def DrawTopCommiter(self, x, y, RepoName, RepoOwner, DayData):
		self.screen.blit(self.ImageDict['TopCommit'], self.ConvertWidthPercent(x, y))
		self.DrawText(RepoName, (x + 20, y + 15), self.LightGray, 16,  True)
		self.DrawText(RepoOwner, (x + 20, y + 50), self.NormalGray, 12)
		

		CloseDayData = ""
		if DayData != "?":
			Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
			for i in range(7):
				val = self.ConvertWidthPercent(141 + x + i * 8, y + 16)
				x2, y2 = val[0], val[1]
				try:
					pygame.draw.rect(self.screen, (40, 255 - int(DayData[Days[i]]) * 20, 40) , [x2, y2, 7 * self.WidthPercent(), 47 * self.WidthPercent()])
				except:
					pygame.draw.rect(self.screen, (40, 0, 40) , [x2, y2, 7 * self.WidthPercent(), 47 * self.WidthPercent()])
				# self.DrawText(DayData[Days[i]], (x2, y2), self.NormalGray, 12)
				CloseDayData += f"{Days[i]} : {DayData[Days[i]]}회\n"
		
		if self.CheckClick((x, y), (x + 207, y + 78)):
			if self.IsPopUp == False:
				self.PopUp(f"[ TopCommiter ] {RepoName} / {RepoOwner}", 
						   f"대상 사용자 : {RepoName}\n\n\n이번 주 기여도: {RepoOwner}\n\n\n자세한 기여도\n\n{CloseDayData}\n\n\n<link>https://github.com/{RepoName}</link>")

	def DrawNewRepository(self, x, y, RepoName, ID, StarCount, CreateDate, LastCommit):
		self.screen.blit(self.ImageDict['NewRepositories'], self.ConvertWidthPercent(x, y))
		self.DrawText(RepoName, (x + 20, y + 13), self.LightGray, 16,  True)
		self.DrawText(ID, (x + 20, y + 42), self.NormalGray, 12)
		self.DrawText(str(StarCount), (x + 170, y + 12), self.NormalGray, 12, IsBold=True, IsRightJustify=True)

		if self.CheckClick((x, y), (x + 195, y + 64)):
			if self.IsPopUp == False:
				self.PopUp(f"[ NewRepository ] {RepoName} / {ID}", 
						   f"저장소 명 : {RepoName}\n\n\n저장소 소유자 : {ID}\n\n\n저장소 별 개수 : {StarCount}\n\n\n<link>https://github.com/{ID}/{RepoName}</link>\n\n생성 일자 : {CreateDate}\n\n최종 커밋 : {LastCommit}")

	def DrawRecentCommit(self, x, y, ID, RepoName, Date, StarCount, CreateDate, i = None):
		if self.CheckClick((x, y), (x + 62, y + 154)):
			if self.IsPopUp == False:
				self.PopUp(f"[ RecentCommit ] {RepoName} / {ID}", 
						   f"저장소 명 : {RepoName}\n\n\n저장소 소유자 : {ID}\n\n\n저장소 별 개수 : {StarCount}\n\n\n<link>https://github.com/{ID}/{RepoName}</link>\n\n생성 일자 : {CreateDate}\n\n최종 커밋 : {Date}")

		ID = ReturnLimitText(ID, 6)
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
					LastCommit = self.TopStars[i]['LastCommit']
					CreateDate = self.TopStars[i]['CreateDate']
					self.DrawTopStar(380 + x * 330, 100 + y * 100 + self.AnimationValue(), RepoName, RepoOwner, Star, LastCommit, CreateDate)
				except:
					self.DrawTopStar(380 + x * 330, 100 + y * 100 + self.AnimationValue(), "?", "?", "?", "?", "?")
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
				self.DrawRecentCommit(322 + i * 75, 643 + self.AnimationValue(), self.RecentCommiters[i]['ID'], self.RecentCommiters[i]['RepoName'], self.RecentCommiters[i]['LastCommit'], self.RecentCommiters[i]['Star'], self.RecentCommiters[i]['CreateDate'], i)
			except:
				self.DrawRecentCommit(322 + i * 75, 643 + self.AnimationValue(), "?", "?", "?", "?", "?")
		
		# New Repsoitories
		for i in range(2):
			try:
				self.DrawNewRepository(750, 650 + i * 80, self.NewRepositories[i]['RepoName'], self.NewRepositories[i]['ID'], self.NewRepositories[i]['Star'], self.NewRepositories[i]['CreateDate'], self.NewRepositories[i]['LastCommit'])
			except:
				self.DrawNewRepository(750, 650 + i * 80, "?", "?", "?", "?", "?")
				
	# ==================================================================

	def DrawMenuUser(self, x, y, Name, Image):
		if self.CheckClick((x, y), (x + 62, y + 94)):
			if self.IsPopUp == False:
				self.PopUp(f"[ User ] {Name}", f"대상 사용자 : {Name}\n\n\n<link>https://github.com/{Name}</link>")
		Name = ReturnLimitText(Name, 5)
		self.screen.blit(self.ImageDict['FollowersAndFavoriteUsers'], self.ConvertWidthPercent(x, y))
		self.screen.blit(Image, self.ConvertWidthPercent(x + 11, y + 10))
		
		self.DrawText(Name, (x + 7, y + 65), self.NormalGray, 12,  True)

	def DrawMenuRepository(self, x, y, RepoName, RepoOwner, StarCount, CreateDate):
		if self.CheckClick((x, y), (x + 167, y + 55)):
			if self.IsPopUp == False:
				self.PopUp(f"[ MyRepository ] {RepoName}",
				           f"저장소 명 : {RepoName}\n\n\n저장소 소유자 : {RepoOwner}\n\n\n저장소 별 개수 : {StarCount}\n\n\n<link>https://github.com/{RepoOwner}/{RepoName}</link>\n\n생성 일자 : {CreateDate}")
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
				self.DrawMenuRepository(14, 325 + self.AnimationValue() + i * 67, self.MyRepoName[i], self.MyID, self.MyRepoStar[i], self.MyRepoTime[i])
			except:
				self.DrawMenuRepository(14, 325 + self.AnimationValue() + i * 67, "?", "?", "?", "?")

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

		if not self.IsPopUp:
			if self.CheckClick((0, 733), (273, 800)):
				self.PopUp("About & Credit",
						   "제작자 : kysth0707 ( 김태형 )\n<link>https://github.com/kysth0707</link>\n\n\n버그 제보 및 건의하기\n<link>https://github.com/kysth0707/OurGithub/issues</link>\n\n\n서버지원\n<link>https://github.com/banksemi</link>\n\n\n개발자 메세지\n\n안녕하세요 김태형입니다! 서로의 깃허브 현황을 알아볼 수 있는 프로그램을 만들게 되었습니다.\n서로의 깃허브에 들어가 별도 눌러주고 함께 커밋도 열심히해보아서 잔디를 계속 채워봅시다!")
		if self.IsPopUp:
			if self.CheckClick((902, 73), (924, 95)):
				self.IsPopUp = False

	# ==================================================================

	IsPopUp = False
	PopUpTitle = ""
	PopUpSubtitle = ""

	def PopUp(self, Title, Subtitle):
		self.IsPopUp = True
		self.PopUpTitle = Title
		self.PopUpSubtitle = Subtitle
		pass

	def DrawPopUp(self):
		if self.IsPopUp:
			self.screen.blit(self.ImageDict['PopUp'], (0, 0))
			self.DrawText(self.PopUpTitle, (68, 68), self.White, 22)
			Subtitles = self.PopUpSubtitle.split('\n')
			
			for i in range(len(Subtitles)):
				if "<link>" in Subtitles[i]:
					URLValue = str(Subtitles[i])[6:len(Subtitles[i]) - 7]
					self.DrawText(URLValue, (68, 140 + i * 20), self.Blue, 17)
					if self.IsPopUp:
						if self.CheckClick((68, 140 + i * 20), (800, 140 + (i + 1) * 20)):
							os.system(f"start \"\" {URLValue}")
				else:
					self.DrawText(Subtitles[i], (68, 140 + i * 20), self.Black, 17)

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

		# self.ShowMousePos()

		pygame.display.update()

		if self.Clicked:
			self.Clicked = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Run = False
				pygame.quit()
				raise

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
						self.PopUp("test", "1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\nasdf\n테스ㅡ트\n<link>https://www.naver.com/</link>")

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.Clicked = True