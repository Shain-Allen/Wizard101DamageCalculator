from math import floor
import tkinter as tk
from turtle import width
from PIL import Image, ImageTk
import json


class Spell:
	def __init__(self, cardName, imgFile, school):
		self.cardName = cardName
		self.imgFile = imgFile
		self.img = ImageTk.PhotoImage(Image.open(imgFile))
		self.school = school

	def imgFileResize(self, newCardWidth):

		baseimage = Image.open(self.imgFile)

		wpercent = (newCardWidth / float(baseimage.width))

		hsize = int(float(baseimage.height) * float(wpercent))

		self.img = ImageTk.PhotoImage(baseimage.resize((newCardWidth, hsize), Image.LANCZOS))


class DamageSpell(Spell):
	def __init__(self, cardName, imgFile, school, minAttackVal, maxAttackVal):
		Spell.__init__(self, cardName, imgFile, school)
		self.minAttackVal = minAttackVal
		self.maxAttackVal = maxAttackVal

class BuffingSpell(Spell):
	def __init__(self, cardName, imgFile, school, damageBuff):
		Spell.__init__(self, cardName, imgFile, school)
		self.damageBuff = damageBuff

class DebuffingSpell(Spell):
	def __init__(self, cardName, imgFile, school, damageDebuff):
		Spell.__init__(self, cardName, imgFile, school)
		self.damageDebuff = damageDebuff

CardDataBank = json.load(open("Cards.json"))

root = tk.Tk()

MAXWINDOWWIDTH = 720
MAXWINDOWHEIGHT = 1280

root.configure(height=MAXWINDOWHEIGHT, width=MAXWINDOWWIDTH)

# create Containers
titleFrame = tk.Frame(root, borderwidth=1, relief="solid", width=MAXWINDOWWIDTH)
damageOutputFrame = tk.Frame(root, width=MAXWINDOWWIDTH)
cardSelectionFrame = tk.Frame(root, height=1000, width=MAXWINDOWWIDTH)
attackCardsFrameOuter = tk.Frame(cardSelectionFrame,width=MAXWINDOWWIDTH/2, borderwidth=2, relief="solid")
attackCardsCanvasInner = tk.Canvas(attackCardsFrameOuter)
attackCardsFrame = tk.Frame(attackCardsCanvasInner)
modificationsFrame = tk.Frame(cardSelectionFrame)
buffsFrameOuter = tk.Frame(modificationsFrame, height=200, width=MAXWINDOWWIDTH/2, borderwidth=2, relief="solid")
debuffsFrameOuter = tk.Frame(modificationsFrame, height=200, width=MAXWINDOWWIDTH/2, borderwidth=2, relief="solid")
incBoost_ResistFrame = tk.Frame(modificationsFrame, height=200, width=MAXWINDOWWIDTH/2, borderwidth=2, relief="solid")
armorStatsFrame = tk.Frame(modificationsFrame,  height=200, width=MAXWINDOWWIDTH/2, borderwidth=2, relief="solid")

# Title creation
titleLabel = tk.Label(titleFrame, text="Wizard 101 Damage Calculator", justify=tk.CENTER)

# DamageOutputFrame
damageMinVar = tk.StringVar(damageOutputFrame)
damageMinVar.set("0")

damageMaxVar = tk.StringVar(damageOutputFrame)
damageMaxVar.set("0")

effectHistoryVar = tk.StringVar(damageOutputFrame)
effectHistoryVar.set("")

damageMin = tk.Label(
	damageOutputFrame, textvariable=damageMinVar, borderwidth=2, relief="solid"
)
damageMax = tk.Label(
	damageOutputFrame, textvariable=damageMaxVar, borderwidth=2, relief="solid"
)
effectHistory = tk.Label(
	damageOutputFrame, textvariable=effectHistoryVar, width=50, borderwidth=2, relief="solid"
)

# Attack Cards creation
damageSpells = []
attackCardBtns = []

for spell in CardDataBank["DamageSpells"]:
	newDamageSpell = DamageSpell(spell["name"], spell["imgFile"], spell["school"], spell["minDmg"], spell["maxDmg"])
	damageSpells.append(newDamageSpell)
	newButton = tk.Button(attackCardsFrame, text=spell["name"])
	attackCardBtns.append(newButton)


# BuffsFrameOuter Creation
# deathTrapBtnImg = tk.PhotoImage(file="Images/DeathSchool/BuffingSpells/Death_Trap.png")
# deathTrapBtn = tk.Button(buffsFrameOuter, text="25%", image=deathTrapBtnImg)
# feintBtnImg = tk.PhotoImage(file="Images/DeathSchool/BuffingSpells/Feint.png")
# feintBtn = tk.Button(buffsFrameOuter, text="70%", image=feintBtnImg)

# Debufs Creation
# deathSheildBtnImg = ImageTk.PhotoImage(Image.open("Images\DeathSchool\DebuffingSpells\Death_Shield.png"))
# deathShieldBtn = tk.Button(debuffsFrameOuter, text="", image=deathSheildBtnImg)

# Inc boost and resist Creation
#tempButton = tk.Button(incBoost_ResistFrame, background="grey", text="Tempt")

# Armor Stats creation
# deathBoost = tk.LabelFrame(armorStatsFrame, text="death boost:")
# deathBoostIn = tk.Entry(deathBoost, name="death boost: ")

# -------------------------------------------------------------------------------------------------------
# place Containers
titleFrame.grid(row=0, column=0)
damageOutputFrame.grid(row=1, column=0)
cardSelectionFrame.grid(row=2, column=0, sticky="N, S, E, W")

attackCardsFrameOuter.grid(row=0, column=0, sticky="N, S, E, W")
attackCardsCanvasInner.pack(side=tk.RIGHT, fill="y", expand="yes")

scroll_y = tk.Scrollbar(attackCardsFrameOuter, orient="vertical", command=attackCardsCanvasInner.yview)
scroll_y.pack(side=tk.LEFT, fill="y")

attackCardsCanvasInner['yscrollcommand'] = scroll_y.set

attackCardsCanvasInner.bind("<Configure>", lambda e: attackCardsCanvasInner.configure(attackCardsCanvasInner.bbox("all")))

attackCardsCanvasInner.create_window((0,0), window=attackCardsFrame, anchor="nw")

modificationsFrame.grid(row=0, column=1, sticky="N, S, E, W")
buffsFrameOuter.grid(row=0, column=0, sticky="N, S, E, W")
buffsFrameOuter.propagate(0)
debuffsFrameOuter.grid(row=1, column=0, sticky="N, S, E, W")
debuffsFrameOuter.propagate(0)
incBoost_ResistFrame.grid(row=2, column=0, sticky="N, S, E, W")
incBoost_ResistFrame.propagate(0)
armorStatsFrame.grid(row=3, column=0, sticky="N, S, E, W")
armorStatsFrame.propagate(0)

# title Placement
#titleLabel.grid()

# DamageOutputFrame Placement
damageMin.grid(row=0, column=0, sticky="N, S, E, W")
damageMax.grid(row=0, column=1, sticky="N, S, E, W")
effectHistory.grid(row=1, columnspan=2, sticky="N, S, E, W")

# Attack Cards placement
rowIndx = 0
columnIndx = 0
for i, Btn in enumerate(attackCardBtns):
	damageSpells[i].imgFileResize(122)
	Btn.configure(image=damageSpells[i].img)
	Btn.grid(row=rowIndx, column=columnIndx, sticky="N, S, E, W")
	columnIndx += 1
	if columnIndx == 3:
		rowIndx += 1
		columnIndx = 0

# BuffsFrameOuter Placement
# deathTrapBtn.grid()
# feintBtn.grid()

# Debufs Placement
# deathShieldBtn.grid()

# Inc boost and resist Placement
#tempButton.grid()

# Armor Stats placement
#deathBoostIn.grid()

root.mainloop()