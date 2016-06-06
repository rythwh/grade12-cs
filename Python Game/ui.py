import pygame, math
from pygame.locals import *

class Screen:
	def __init__(self):
		displayInfo = pygame.display.Info()
		self.width = displayInfo.current_w
		self.height = displayInfo.current_h

class UI:
	def __init__(self):
	
		self.mousePos = pygame.mouse.get_pos()
	
		self.panels = []
		self.updatePanels = []
		self.buttons = []
		self.texts = []
		self.updateTexts = []
		
		self.uiSurface = pygame.display.set_mode((screen.width,screen.height),pygame.FULLSCREEN)
		
		self.AddUI()
		
		self.mouseDown = False
		self.mouseOverUI = False
		
		self.selectedBuilding = None
		
		self.mouseOverTile = None
		
	def AddUI(self):
	
		global cityPanelSize
	
		# City panel
		cityPanelPosition = (10,10)
		cityPanelSize = (100,100)
		self.AddPanel(Panel(cityPanelPosition,cityPanelSize,(255,255,255),5,(200,200,200)))	
		
		global cityTextPosition
		cityTextPosition = (cityPanelPosition[0]+5,cityPanelPosition[1])
				
		self.AddText(Text(cityTextPosition,cityPanelSize,"Population","verdana",14,(50,50,50)))
		self.AddText(Text((cityTextPosition[0],cityTextPosition[1]+35),cityPanelSize,"Money","verdana",14,(50,50,50)))
		
		global buildingPanelPosition
		buildingPanelPosition = (cityPanelPosition[0]+cityPanelSize[0]+15,cityPanelPosition[1])
		global buildingTextPosition
		buildingTextPosition = (buildingPanelPosition[0]+5,buildingPanelPosition[1])
		
		global rciPanelPosition
		rciPanelPosition = (cityPanelPosition[0],cityPanelPosition[1]+cityPanelSize[1]+15)
		global rciTextPosition
		rciTextPosition = (rciPanelPosition[0]+5,rciPanelPosition[1])
		
		self.AddPanel(Panel(rciPanelPosition,(cityPanelSize[0],cityPanelSize[1]+10),(255,255,255),5,(200,200,200)))
		
		self.AddText(Text(rciTextPosition,cityPanelSize,"Demand","verdana",14,(50,50,50)))
		self.AddText(Text((rciTextPosition[0],rciTextPosition[1]+15),cityPanelSize,"Residential","verdana",12,(50,50,50)))
		self.AddText(Text((rciTextPosition[0],rciTextPosition[1]+45),cityPanelSize,"Commercial","verdana",12,(50,50,50)))
		self.AddText(Text((rciTextPosition[0],rciTextPosition[1]+75),cityPanelSize,"Industrial","verdana",12,(50,50,50)))
		
		global datePanelPosition
		datePanelPosition = (rciPanelPosition[0],rciPanelPosition[1]+cityPanelSize[1]+25)
		global dateTextPosition
		dateTextPosition = (datePanelPosition[0]+5,datePanelPosition[1])
		
		self.AddPanel(Panel(datePanelPosition,(cityPanelSize[0],cityPanelSize[1]-35),(255,255,255),5,(200,200,200)))
		
		self.AddText(Text(dateTextPosition,cityPanelSize,"Date","verdana",14,(50,50,50)))
		
		# Building panel
		from buildings import buildingPrefabs
		
		buildingButtonNum = len(buildingPrefabs.prefabs)
		buildingButtonSize = (100,35)
		buildingPanelSize = (5+(buildingButtonSize[0]+5)*buildingButtonNum,buildingButtonSize[1]+10)
		
		buildingPanelRect = (screen.width/2-buildingPanelSize[0]/2,screen.height-buildingPanelSize[1]-10,buildingPanelSize[0],buildingPanelSize[1])
		self.AddPanel(Panel((buildingPanelRect[0],buildingPanelRect[1]),(buildingPanelRect[2],buildingPanelRect[3]),(255,255,255),5,(200,200,200)))
		
		for index in range(buildingButtonNum):
			buildingPrefab = buildingPrefabs.prefabs[index]
			
			buildingButtonPosition = (buildingPanelRect[0] + 5 + (index * (buildingButtonSize[0] + 5)),buildingPanelRect[1]+5)
			
			buildingButtonTextPosition = (buildingButtonPosition[0]+5,buildingButtonPosition[1])
			buttonText = Text(buildingButtonTextPosition,buildingButtonSize,buildingPrefab.buildingType,"verdana",12,(200,200,200))
			
			self.AddButton(Button(buildingButtonPosition,buildingButtonSize,buttonText,(50,50,50),(75,75,75),(100,100,100)))
			
			previewButtonPosition = (buildingButtonPosition[0]+5,buildingButtonPosition[1]+15)
			previewButtonSize = (buildingButtonSize[0]-10,buildingButtonSize[1]-20)
			
			self.AddButton(Button(previewButtonPosition,previewButtonSize,buttonText,buildingPrefab.colour,buildingPrefab.colour,buildingPrefab.colour))
		
	def AddUIUpdate(self):
		from city import city
		self.AddUpdateText(Text((cityTextPosition[0],cityTextPosition[1]+15),cityPanelSize,str(round(city.population)) + " Citizens","verdana",12,(50,50,200)))
		
		self.AddUpdateText(Text((cityTextPosition[0],cityTextPosition[1]+50),cityPanelSize,"$" + str(round(city.bank)),"verdana",12,(50,50,200)))
		self.AddUpdateText(Text((cityTextPosition[0],cityTextPosition[1]+65),cityPanelSize,"+$" + str(round(city.income)),"verdana",12,(50,200,50)))
		self.AddUpdateText(Text((cityTextPosition[0],cityTextPosition[1]+80),cityPanelSize,"-$" + str(round(city.expense)),"verdana",12,(200,50,50)))	
		
		if (self.mouseOverTile != None and self.mouseOverTile.building != None and self.mouseOverTile.building.prefab.buildingType != "Road"):
			building = self.mouseOverTile.building
			self.AddUpdatePanel(Panel(buildingPanelPosition,(cityPanelSize[0]+25,cityPanelSize[1]),(255,255,255),5,(200,200,200)))
			self.AddUpdateText(Text(buildingTextPosition,cityPanelSize,building.prefab.buildingType,"verdana",14,(50,50,50)))
			if (building.prefab.buildingType == "Residential"):
				self.AddUpdateText(Text(buildingTextPosition,cityPanelSize,"Population","verdana",14,(50,50,50)))
				self.AddUpdateText(Text((buildingTextPosition[0],buildingTextPosition[1]+45),cityPanelSize,"Value","verdana",14,(50,50,50)))
				self.AddUpdateText(Text((buildingTextPosition[0],buildingTextPosition[1]+15),cityPanelSize,str(len(building.population)) + "/" + str(int(building.prefab.maxPopulation)) + " Citizens","verdana",12,(50,50,200)))
				self.AddUpdateText(Text((buildingTextPosition[0],buildingTextPosition[1]+30),cityPanelSize,str(building.employed) + " Employed","verdana",12,(50,50,200)))
				self.AddUpdateText(Text((buildingTextPosition[0],buildingTextPosition[1]+60),cityPanelSize,"$" + str(round(building.landValue)),"verdana",12,(50,200,50)))
				self.AddUpdateText(Text((buildingTextPosition[0],buildingTextPosition[1]+75),cityPanelSize,"$" + str(round(building.prefab.maintenanceBase)),"verdana",12,(200,50,50)))
			elif (building.prefab.buildingType != "Road"):
				self.AddUpdateText(Text((buildingTextPosition[0],buildingTextPosition[1]+15),cityPanelSize,str(len(building.population)) + "/" + str(int(building.prefab.maxPopulation)) + " Employees","verdana",12,(50,50,200)))
				self.AddUpdateText(Text((buildingTextPosition[0],buildingTextPosition[1]+30),cityPanelSize,"-$" + str(round(building.prefab.maintenanceBase)),"verdana",12,(200,50,50)))
		else:
			self.AddUpdateText(Text(buildingTextPosition,cityPanelSize,"Mouse over a building for more information.","verdana",10,(50,50,50)))
			
		from buildings import buildingPrefabs
		self.AddUpdateText(Text((rciTextPosition[0],rciTextPosition[1]+30),cityPanelSize,str(round(city.resDemand,2) * 100) + "%","verdana",12,buildingPrefabs.FindPrefabFromType("Residential").colour))
		self.AddUpdateText(Text((rciTextPosition[0],rciTextPosition[1]+60),cityPanelSize,str(round(city.comDemand,2) * 100) + "%","verdana",12,buildingPrefabs.FindPrefabFromType("Commercial").colour))
		self.AddUpdateText(Text((rciTextPosition[0],rciTextPosition[1]+90),cityPanelSize,str(round(city.indDemand,2) * 100) + "%","verdana",12,buildingPrefabs.FindPrefabFromType("Industrial").colour))
		
		from times import time
		self.AddUpdateText(Text((screen.width-20,0),(0,0),str(round(time.clock.get_fps())),"verdana",12,(50,50,50)))
		
		self.AddUpdateText(Text((dateTextPosition[0],dateTextPosition[1]+15),cityPanelSize,str(time.day) + self.AddS(" Day",time.day),"verdana",12,(50,50,50)))
		self.AddUpdateText(Text((dateTextPosition[0],dateTextPosition[1]+30),cityPanelSize,str(time.month) + self.AddS(" Month",time.month),"verdana",12,(50,50,50)))
		self.AddUpdateText(Text((dateTextPosition[0],dateTextPosition[1]+45),cityPanelSize,str(time.year) + self.AddS(" Year",time.year),"verdana",12,(50,50,50)))
		
	def AddS(self,string,value):
		if (value != 1):
			return string + "s"
		else:
			return string
		
	def AddPanel(self,panel):
		self.panels.append(panel)
		
	def AddButton(self,button):
		self.buttons.append(button)
		
	def AddText(self,text):
		self.texts.append(text)
		
	def AddUpdateText(self,text):
		self.updateTexts.append(text)
		
	def AddUpdatePanel(self,panel):
		self.updatePanels.append(panel)
		
	def Update(self):
		
		self.updatePanels.clear()
		self.updateTexts.clear()
		self.AddUIUpdate()
		
		self.mousePos = pygame.mouse.get_pos()
		
		self.mouseOverUI = False
	
		for panel in self.panels:
			self.DrawPanel(panel)
				
		for panel in self.updatePanels:
			self.DrawPanel(panel)
			
		for button in self.buttons:
				
			from buildings import buildingPrefabs
				
			buttonColour = button.normalColour
	
			if (self.MouseWithinBounds((button.position)+(button.size)) and button.disabled == False):
				buttonColour = button.hoverColour
				if (self.mouseDown):
					
					buttonColour = button.clickColour
					self.selectedBuilding = buildingPrefabs.FindPrefabFromType(button.text.text)
					
			from city import city
			if (city.cityHall == None and button.text.text != "City Hall"):			
				button.disabled = True
			elif (city.cityHall != None):
				if (button.text.text == "City Hall"):
					button.disabled = True
				else:
					button.disabled = False
					if (city.bank < buildingPrefabs.FindPrefabFromType(button.text.text).cost):
						button.disabled = True
					
			if (button.disabled):
				buttonColour = (button.normalColour[0]/2,button.normalColour[1]/2,button.normalColour[2]/2)
				if (ui.selectedBuilding != None and ui.selectedBuilding.buildingType == button.text.text):
					ui.selectedBuilding = None
					
			pygame.draw.rect(self.uiSurface,buttonColour,(button.position)+(button.size))
			if (button.text != None):
				self.uiSurface.blit(button.text.textObject,button.text.position)
				
			if (self.MouseWithinBounds((button.position)+(button.size))):
				self.mouseOverUI = True
				
		for text in self.texts:
			self.DrawText(text)
			
		for text in self.updateTexts:
			self.DrawText(text)
			
	def MouseWithinBounds(self,bounds):
		if (self.mousePos[0] >= bounds[0] and self.mousePos[0] < bounds[2]+bounds[0] and self.mousePos[1] >= bounds[1] and self.mousePos[1] < bounds[3]+bounds[1]):
			return True
		return False
		
	def DrawPanel(self,panel):
		if (panel.borderThickness > 0):
				pygame.draw.rect(self.uiSurface,panel.borderColour,(panel.borderPosition)+(panel.borderSize))
			
		pygame.draw.rect(self.uiSurface,panel.colour,(panel.position)+(panel.size))
		
		if (self.MouseWithinBounds((panel.position)+(panel.size))):
			self.mouseOverUI = True
			
	def DrawText(self,text):
		self.uiSurface.blit(text.textObject,text.position)

class Panel:
	def __init__(self,position,size,colour,borderThickness,borderColour):
		self.position = position
		self.size = size
		
		self.colour = colour
		
		self.borderThickness = borderThickness
		self.borderPosition = (self.position[0]-self.borderThickness,self.position[1]-self.borderThickness)
		self.borderSize = (self.size[0]+(self.borderThickness*2),self.size[1]+(self.borderThickness*2))
		self.borderColour = borderColour

class Button:
	def __init__(self,position,size,text,normalColour,hoverColour,clickColour):
		self.position = position
		self.size = size
		
		self.text = text
		
		self.normalColour = normalColour
		self.hoverColour = hoverColour
		self.clickColour = clickColour
		
		self.disabled = False

class Text:
	def __init__(self,position,size,text,font,fontSize,colour):
		self.position = position
		self.size = size
		
		self.text = text
		self.font = font
		self.fontSize = fontSize
		self.colour = colour
		
		self.textObject = pygame.font.SysFont(self.font,self.fontSize).render(self.text,1,self.colour)

def Awake():
	global screen
	screen = Screen()
	global ui
	ui = UI()
	
def Update():
	ui.Update()