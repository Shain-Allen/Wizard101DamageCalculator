from math import floor
import tkinter as tk
from turtle import width
from PIL import Image, ImageTk
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


class DamageSpell(Spell):
	def __init__(self, parantWiget, imgFile, cardName,  school, minAttackVal, maxAttackVal):
		Spell.__init__(self, parantWiget, imgFile, cardName, school)
		self.minAttackVal = minAttackVal
		self.maxAttackVal = maxAttackVal

class BuffingSpell(Spell):
	def __init__(self, parantWiget, imgFile, cardName, school, damageBuff):
		Spell.__init__(self, parantWiget, imgFile, cardName, school)
		self.damageBuff = damageBuff

class DebuffingSpell(Spell):
	def __init__(self, parantWiget, imgFile, cardName, school, damageDebuff):
		Spell.__init__(self, parantWiget, imgFile, cardName, school)
		self.damageDebuff = damageDebuff

CardDataBank = json.load(open("Cards.json"))

root = tk.Tk()

MAXWINDOWWIDTH = 720
MAXWINDOWHEIGHT = 1280

root.configure(height=MAXWINDOWHEIGHT, width=MAXWINDOWWIDTH)

# create Containers
titleFrame = tk.Frame(root, width=MAXWINDOWWIDTH, borderwidth=1, relief=tk.SOLID)
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

# Title creation
titleLabel = tk.Label(titleFrame, text="Wizard 101 Damage Calculator", justify=tk.CENTER)

# DamageOutputFrame
damageMinVar = tk.StringVar(damageOutputFrame)
damageMinVar.set("0")

damageMaxVar = tk.StringVar(damageOutputFrame)
damageMaxVar.set("0")

effectHistoryVar = tk.StringVar(damageOutputFrame)
effectHistoryVar.set("")

damageMin = tk.Label(damageOutputFrame, textvariable=damageMinVar, borderwidth=2, relief="solid")
damageMax = tk.Label(damageOutputFrame, textvariable=damageMaxVar, borderwidth=2, relief="solid")
effectHistory = tk.Label(damageOutputFrame, textvariable=effectHistoryVar, width=50, borderwidth=2, relief="solid")

# Attack Cards creation
damageSpells = []

for spell in CardDataBank["DamageSpells"]:
	newDamageSpell = DamageSpell(attackCardsFrame, spell["imgFile"], spell["name"], spell["school"], spell["minDmg"], spell["maxDmg"])
	damageSpells.append(newDamageSpell)


# BuffsFrameOuter Creation
buffSpells = []

for spell in CardDataBank["BuffingSpells"]:
	newBuffSpell = BuffingSpell(buffCardsFrame, spell["imgFile"], spell["name"], spell["school"], spell["buff"])
	buffSpells.append(newBuffSpell)

# Debufs Creation
debuffSpells = []

for spell in CardDataBank["DebuffingSpells"]:
	newDebuffSpell = DebuffingSpell(debuffCardsFrame, spell["imgFile"], spell["name"], spell["school"], spell["debuff"])
	debuffSpells.append(newDebuffSpell)


# Inc boost and resist Creation


# Armor Stats creation
# deathBoost = tk.LabelFrame(armorStatsFrame, text="death boost:")
# deathBoostIn = tk.Entry(deathBoost, name="death boost: ")

# -------------------------------------------------------------------------------------------------------
# place Containers
titleFrame.grid(row=0, column=0)
damageOutputFrame.grid(row=1, column=0)
cardSelectionFrame.grid(row=2, column=0, sticky="N, S, E, W")

#attack card containers + scroll bar configuration
attackCardsFrameOuter.grid(row=0, column=0, sticky="N, S, E, W")
attackCardsCanvasInner.pack(side=tk.RIGHT, fill="y", expand="yes")
attackCardsScroll_y.pack(side=tk.LEFT, fill="y")
attackCardsCanvasInner['yscrollcommand'] = attackCardsScroll_y.set
attackCardsCanvasInner.bind("<Configure>", lambda e: attackCardsCanvasInner.configure(scrollregion=attackCardsCanvasInner.bbox("all")))
attackCardsCanvasInner.create_window((0,0), window=attackCardsFrame, anchor="nw")

#modifications side configuration
modificationsFrame.grid(row=0, column=1, sticky="N, S, E, W")

#buff Card containers + scroll bar configuration
buffCardsFrameOuter.grid(row=0, column=0, sticky="N, S, E, W")
buffCardsCanvasInner.pack(side=tk.RIGHT, fill="y", expand="yes")
buffCardsScroll_y.pack(side=tk.LEFT, fill="y")
buffCardsCanvasInner['yscrollcommand'] = buffCardsScroll_y.set
buffCardsCanvasInner.bind("<Configure>", lambda e: buffCardsCanvasInner.configure(scrollregion=buffCardsCanvasInner.bbox("all")))
buffCardsCanvasInner.create_window((0,0), window=buffCardsFrame, anchor="nw")

#debuff Card Containers + scroll bar configuration
debuffCardsFrameOuter.grid(row=1, column=0, sticky="N, S, E, W")
debuffCardsCanvasInner.pack(side=tk.RIGHT, fill="y", expand="yes")
debuffCardsScroll_y.pack(side=tk.LEFT, fill="y")
debuffCardsCanvasInner['yscrollcommand'] = debuffCardsScroll_y.set
debuffCardsCanvasInner.bind("<Configure>", lambda e: debuffCardsCanvasInner.configure(scrollregion=debuffCardsCanvasInner.bbox("all")))
debuffCardsCanvasInner.create_window((0,0), window=debuffCardsFrame, anchor="nw")

#Natural monster boosts/resist container configuration
incBoost_ResistFrameOuter.grid(row=2, column=0, sticky="N, S, E, W")

#Player armor stat entry configuration
armorStatsFrameOuter.grid(row=3, column=0, sticky="N, S, E, W")


# title Placement
titleLabel.grid()

# DamageOutputFrame Placement
damageMin.grid(row=0, column=0, sticky="N, S, E, W")
damageMax.grid(row=0, column=1, sticky="N, S, E, W")
effectHistory.grid(row=1, columnspan=2, sticky="N, S, E, W")

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
#deathBoostIn.grid()

root.mainloop()