from cgitb import text
from math import floor
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import json


class Spell:
	def __init__(self, parantWiget, imgFile, cardName, school):
		self.imgFile = imgFile
		self.img = ImageTk.PhotoImage(Image.open(imgFile))
		self.btn = tk.Button(parantWiget, image=self.img)
		self.cardName = cardName
		self.school = school

	def imgFileResize(self, newdamageSpellCardWidth):

		baseimage = Image.open(self.imgFile)

		wpercent = (newdamageSpellCardWidth / float(baseimage.width))

		hsize = int(float(baseimage.height) * float(wpercent))

		self.img = ImageTk.PhotoImage(baseimage.resize((newdamageSpellCardWidth, hsize), Image.LANCZOS))

		self.btn.config(image=self.img)
	
	def DefineBtnCommand(self, spellArray):
		self.btn.config(command=lambda: self.BtnToggle(spellArray))

	def BtnToggle(self, spellArray):
		baseimage = Image.open(self.imgFile)
		imgHeight = self.img.height()
		imgWidth = self.img.width()

		if(self not in spellArray):
			spellArray.append(self)
			baseimage = ImageOps.grayscale(baseimage)
			self.img = ImageTk.PhotoImage(baseimage.resize((imgWidth, imgHeight), Image.LANCZOS))
		else:
			spellArray.remove(self)
			self.img = ImageTk.PhotoImage(baseimage.resize((imgWidth, imgHeight), Image.LANCZOS))

		self.btn.config(image=self.img)


class DamageSpell(Spell):
	def __init__(self, parantWiget, imgFile, cardName,  school, minAttackVal, maxAttackVal):
		Spell.__init__(self, parantWiget, imgFile, cardName, school)
		self.minAttackVal = minAttackVal
		self.maxAttackVal = maxAttackVal

	def BtnToggle(self, spellArray):
		baseimage = Image.open(self.imgFile)
		imgHeight = self.img.height()
		imgWidth = self.img.width()

		if(self not in spellArray):
			
			for damageSpell in spellArray:
				if(type(damageSpell) == DamageSpell):
					spellArray.remove(damageSpell)
					damageSpell.Colorize()

			spellArray.append(self)
			baseimage = ImageOps.grayscale(baseimage)
			self.img = ImageTk.PhotoImage(baseimage.resize((imgWidth, imgHeight), Image.LANCZOS))
		else:
			spellArray.remove(self)
			self.img = ImageTk.PhotoImage(baseimage.resize((imgWidth, imgHeight), Image.LANCZOS))

		self.btn.config(image=self.img)

	def Colorize(self):
		baseimage = Image.open(self.imgFile)
		imgHeight = self.img.height()
		imgWidth = self.img.width()

		self.img = ImageTk.PhotoImage(baseimage.resize((imgWidth, imgHeight), Image.LANCZOS))
		self.btn.config(image=self.img)

class BuffingSpell(Spell):
	def __init__(self, parantWiget, imgFile, cardName, school, damageBuff):
		Spell.__init__(self, parantWiget, imgFile, cardName, school)
		self.damageBuff = damageBuff

class DebuffingSpell(Spell):
	def __init__(self, parantWiget, imgFile, cardName, school, damageDebuff):
		Spell.__init__(self, parantWiget, imgFile, cardName, school)
		self.damageDebuff = damageDebuff

class ArmorSpec():
	def __init__(self, baseWidget , schoolName, schoolImgFile):
		self.Name = schoolName
		self.imgFile = schoolImgFile
		self.specHolder = tk.Frame(baseWidget)
		self.img = ImageTk.PhotoImage(Image.open(schoolImgFile))
		self.schoolLogo = tk.Label(self.specHolder, image=self.img)
		self.armorPercent = tk.Entry(self.specHolder)
		self.armorFlat = tk.Entry(self.specHolder)

	def pack(self):
		self.specHolder.pack(side=tk.LEFT, expand=tk.FALSE)
		self.schoolLogo.pack()
		self.armorPercent.pack()
		self.armorFlat.pack()
	
	def imgFileResize(self, newWidth):

		baseimage = Image.open(self.imgFile)

		wpercent = (newWidth / float(baseimage.width))

		hsize = int(float(baseimage.height) * float(wpercent))

		self.img = ImageTk.PhotoImage(baseimage.resize((newWidth, hsize), Image.LANCZOS))

		self.schoolLogo.config(image=self.img)

		self.specHolder.config(width=newWidth)

CardDataBank = json.load(open("Cards.json"))

spellHistory = []

root = tk.Tk()

root.title("Wizard 101 Calculator")

MAXWINDOWWIDTH = 720
MAXWINDOWHEIGHT = 1280

root.configure(height=MAXWINDOWHEIGHT, width=MAXWINDOWWIDTH)

# create Containers
damageOutputFrame = tk.Frame(root, width=MAXWINDOWWIDTH)
cardSelectionFrame = tk.Frame(root, height=1000, width=MAXWINDOWWIDTH)

attackCardsFrameOuter = tk.Frame(cardSelectionFrame,width=MAXWINDOWWIDTH/2, borderwidth=2, relief=tk.SOLID)
attackCardsCanvasInner = tk.Canvas(attackCardsFrameOuter)
attackCardsFrame = tk.Frame(attackCardsCanvasInner)
attackCardsScroll_y = tk.Scrollbar(attackCardsFrameOuter, orient=tk.VERTICAL, command=attackCardsCanvasInner.yview)

modificationsFrame = tk.Frame(cardSelectionFrame)

buffCardsFrameOuter = tk.Frame(modificationsFrame, height=200, width=MAXWINDOWWIDTH/2, borderwidth=2, relief=tk.SOLID)
buffCardsCanvasInner = tk.Canvas(buffCardsFrameOuter)
buffCardsFrame = tk.Frame(buffCardsCanvasInner)
buffCardsScroll_y = tk.Scrollbar(buffCardsFrameOuter, orient=tk.VERTICAL, command=buffCardsCanvasInner.yview)

debuffCardsFrameOuter = tk.Frame(modificationsFrame, height=200, width=MAXWINDOWWIDTH/2, borderwidth=2, relief=tk.SOLID)
debuffCardsCanvasInner = tk.Canvas(debuffCardsFrameOuter)
debuffCardsFrame = tk.Frame(debuffCardsCanvasInner)
debuffCardsScroll_y = tk.Scrollbar(debuffCardsFrameOuter, orient=tk.VERTICAL, command=debuffCardsCanvasInner.yview)


incBoost_ResistFrameOuter = tk.Frame(modificationsFrame, height=200, width=MAXWINDOWWIDTH/2, borderwidth=2, relief=tk.SOLID)
armorStatsFrameOuter = tk.Frame(modificationsFrame,  height=200, width=MAXWINDOWWIDTH/2, borderwidth=2, relief=tk.SOLID)

# DamageOutputFrame
damageMinVar = tk.StringVar(damageOutputFrame)
damageMinVar.set("0")

damageMaxVar = tk.StringVar(damageOutputFrame)
damageMaxVar.set("0")

damageMin = tk.Label(damageOutputFrame, textvariable=damageMinVar, borderwidth=2, relief="solid")
damageMax = tk.Label(damageOutputFrame, textvariable=damageMaxVar, borderwidth=2, relief="solid")

# Attack Cards creation
damageSpells = []

for spell in CardDataBank["DamageSpells"]:
	newDamageSpell = DamageSpell(attackCardsFrame, spell["imgFile"], spell["name"], spell["school"], spell["minDmg"], spell["maxDmg"])
	newDamageSpell.DefineBtnCommand(spellHistory)
	damageSpells.append(newDamageSpell)


# BuffsFrameOuter Creation
buffSpells = []

for spell in CardDataBank["BuffingSpells"]:
	newBuffSpell = BuffingSpell(buffCardsFrame, spell["imgFile"], spell["name"], spell["school"], spell["buff"])
	newBuffSpell.DefineBtnCommand(spellHistory)
	buffSpells.append(newBuffSpell)

# Debufs Creation
debuffSpells = []

for spell in CardDataBank["DebuffingSpells"]:
	newDebuffSpell = DebuffingSpell(debuffCardsFrame, spell["imgFile"], spell["name"], spell["school"], spell["debuff"])
	newDebuffSpell.DefineBtnCommand(spellHistory)
	debuffSpells.append(newDebuffSpell)


# Inc boost and resist Creation


# Armor Stats creation
fireDamage = ArmorSpec(armorStatsFrameOuter, "Fire", "Images/SchoolIcons/Fire-School.gif")
iceDamage = ArmorSpec(armorStatsFrameOuter, "Ice", "Images/SchoolIcons/Ice-School.gif")
stormDamage = ArmorSpec(armorStatsFrameOuter, "Storm", "Images/SchoolIcons/Storm-School.gif")
mythDamage = ArmorSpec(armorStatsFrameOuter, "Myth", "Images/SchoolIcons/Myth-School.gif")
lifeDamage = ArmorSpec(armorStatsFrameOuter, "Life", "Images/SchoolIcons/Life-School.gif")
deathDamage = ArmorSpec(armorStatsFrameOuter, "Death", "Images/SchoolIcons/Death-School.gif")
balanceDamage = ArmorSpec(armorStatsFrameOuter, "Balance", "Images/SchoolIcons/Balance-School.gif")

# -------------------------------------------------------------------------------------------------------
# place Containers
damageOutputFrame.grid(row=1, column=0)
cardSelectionFrame.grid(row=2, column=0, sticky="N, S, E, W")

#attack card containers + scroll bar configuration
attackCardsFrameOuter.grid(row=0, column=0, sticky="N, S, E, W")
attackCardsCanvasInner.pack(side=tk.RIGHT, fill="y", expand=tk.YES)
attackCardsScroll_y.pack(side=tk.LEFT, fill="y")
attackCardsCanvasInner['yscrollcommand'] = attackCardsScroll_y.set
attackCardsCanvasInner.bind("<Configure>", lambda e: attackCardsCanvasInner.configure(scrollregion=attackCardsCanvasInner.bbox("all")))
attackCardsCanvasInner.create_window((0,0), window=attackCardsFrame, anchor="nw")

#modifications side configuration
modificationsFrame.grid(row=0, column=1, sticky="N, S, E, W")

#buff Card containers + scroll bar configuration
buffCardsFrameOuter.grid(row=0, column=0, sticky="N, S, E, W")
buffCardsCanvasInner.pack(side=tk.RIGHT, fill="y", expand=tk.YES)
buffCardsScroll_y.pack(side=tk.LEFT, fill="y")
buffCardsCanvasInner['yscrollcommand'] = buffCardsScroll_y.set
buffCardsCanvasInner.bind("<Configure>", lambda e: buffCardsCanvasInner.configure(scrollregion=buffCardsCanvasInner.bbox("all")))
buffCardsCanvasInner.create_window((0,0), window=buffCardsFrame, anchor="nw")

#debuff Card Containers + scroll bar configuration
debuffCardsFrameOuter.grid(row=1, column=0, sticky="N, S, E, W")
debuffCardsCanvasInner.pack(side=tk.RIGHT, fill="y", expand=tk.YES)
debuffCardsScroll_y.pack(side=tk.LEFT, fill="y")
debuffCardsCanvasInner['yscrollcommand'] = debuffCardsScroll_y.set
debuffCardsCanvasInner.bind("<Configure>", lambda e: debuffCardsCanvasInner.configure(scrollregion=debuffCardsCanvasInner.bbox("all")))
debuffCardsCanvasInner.create_window((0,0), window=debuffCardsFrame, anchor="nw")

#Natural monster boosts/resist container configuration
incBoost_ResistFrameOuter.grid(row=2, column=0, sticky="N, S, E, W")

#Player armor stat entry configuration
armorStatsFrameOuter.grid(row=3, column=0, sticky="N, S, E, W")

# DamageOutputFrame Placement
damageMin.grid(row=0, column=0, sticky="N, S, E, W")
damageMax.grid(row=0, column=1, sticky="N, S, E, W")

#--------------------------------------------------------------------------------

root.update_idletasks()
damageSpellCardWidth = floor((attackCardsCanvasInner.winfo_reqwidth() - attackCardsScroll_y.winfo_reqwidth())/3)
buffSpellCardWidth = floor((buffCardsCanvasInner.winfo_reqwidth() - buffCardsScroll_y.winfo_reqwidth())/4)
debuffSpellCardWidth = floor((debuffCardsCanvasInner.winfo_reqwidth() - debuffCardsScroll_y.winfo_reqwidth())/4)

# Attack Cards placement
rowIndx = 0
columnIndx = 0
for spell in damageSpells:
	spell.imgFileResize(damageSpellCardWidth)
	spell.btn.grid(row=rowIndx, column=columnIndx, sticky="N, S, E, W")
	columnIndx += 1
	if columnIndx == 3:
		rowIndx += 1
		columnIndx = 0

# BuffsFrameOuter Placement
rowIndx = 0
columnIndx = 0
for spell in buffSpells:
	spell.imgFileResize(buffSpellCardWidth)
	spell.btn.grid(row=rowIndx, column=columnIndx, sticky="N, S, E, W")
	columnIndx += 1
	if columnIndx == 4:
		rowIndx += 1
		columnIndx = 0

# Debufs Placement
rowIndx = 0
columnIndx = 0
for spell in debuffSpells:
	spell.imgFileResize(debuffSpellCardWidth)
	spell.btn.grid(row=rowIndx, column=columnIndx, sticky="N, S, E, W")
	columnIndx += 1
	if columnIndx == 4:
		rowIndx += 1
		columnIndx = 0

# Inc boost and resist Placement



# Armor Stats placement
armorStatsImgWidth = floor(armorStatsFrameOuter.winfo_width()/7)

fireDamage.imgFileResize(armorStatsImgWidth)
iceDamage.imgFileResize(armorStatsImgWidth)
stormDamage.imgFileResize(armorStatsImgWidth)
mythDamage.imgFileResize(armorStatsImgWidth)
lifeDamage.imgFileResize(armorStatsImgWidth)
deathDamage.imgFileResize(armorStatsImgWidth)
balanceDamage.imgFileResize(armorStatsImgWidth)

fireDamage.pack()
iceDamage.pack()
stormDamage.pack()
mythDamage.pack()
lifeDamage.pack()
deathDamage.pack()
balanceDamage.pack()


root.mainloop()