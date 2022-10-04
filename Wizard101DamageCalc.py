from distutils.command.config import config
from math import floor
import tkinter as tk
from PIL import Image, ImageTk
import json

from click import command


class Spell:
	def __init__(self, cardName, imgFile, school):
		self.cardName = cardName
		self.img = ImageTk.PhotoImage(Image.open(imgFile))
		self.school = school

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
titleFrame = tk.Frame(root, borderwidth=1, relief="solid", height=80, width=MAXWINDOWWIDTH)
damageOutputFrame = tk.Frame(root, width=MAXWINDOWWIDTH)
cardSelectionFrame = tk.Frame(root, height=1000, width=MAXWINDOWWIDTH)
attackCardsCanvasOuter = tk.Canvas(cardSelectionFrame,width=MAXWINDOWWIDTH/2, borderwidth=2, relief="solid")
attackCardsCanvasInner = tk.Canvas(attackCardsCanvasOuter)
attackCardsFrame = tk.Frame(attackCardsCanvasInner)
modificationsFrame = tk.Frame(cardSelectionFrame)
buffsCanvas = tk.Canvas(modificationsFrame, borderwidth=2, relief="solid")
debuffsCanvas = tk.Canvas(modificationsFrame, borderwidth=2, relief="solid")
incBoost_ResistCanvas = tk.Canvas(modificationsFrame, borderwidth=2, relief="solid")
armorStatsFrame = tk.Frame(modificationsFrame, borderwidth=2, relief="solid")

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


# BuffsCanvas Creation
deathTrapBtnImg = tk.PhotoImage(file="Images/DeathSchool/BuffingSpells/Death_Trap.png")
deathTrapBtn = tk.Button(buffsCanvas, background="green", text="25%", image=deathTrapBtnImg)
feintBtnImg = tk.PhotoImage(file="Images/DeathSchool/BuffingSpells/Feint.png")
feintBtn = tk.Button(buffsCanvas, background="green", text="70%", image=feintBtnImg)

# Debufs Creation
weakness = tk.Button(debuffsCanvas, background="red", text="-25")

# Inc boost and resist Creation
tempButton = tk.Button(incBoost_ResistCanvas, background="grey", text="Tempt")

# Armor Stats creation
deathBoost = tk.LabelFrame(armorStatsFrame, text="death boost:")
deathBoostIn = tk.Entry(deathBoost, name="death boost: ")

# -------------------------------------------------------------------------------------------------------
# place Containers
titleFrame.grid(row=0, column=0)
damageOutputFrame.grid(row=1, column=0)
cardSelectionFrame.grid(row=2, column=0, sticky="N, S, E, W")

attackCardsCanvasOuter.grid(row=0, column=0, sticky="N, S, E, W")
attackCardsCanvasInner.pack(side=tk.RIGHT, fill="y", expand="yes")

scroll_y = tk.Scrollbar(attackCardsCanvasOuter, orient="vertical", command=attackCardsCanvasInner.yview)
scroll_y.pack(side=tk.LEFT, fill="y")

attackCardsCanvasInner.configure(yscrollcommand=scroll_y.set)

attackCardsCanvasInner.bind("<Configure>", lambda e: attackCardsCanvasInner.configure(attackCardsCanvasInner.bbox("all")))

attackCardsCanvasInner.create_window((0,0), window=attackCardsFrame, anchor="nw")

modificationsFrame.grid(row=0, column=1, sticky="N, S, E, W")
buffsCanvas.grid(row=0, column=0, sticky="N, S, E, W")
debuffsCanvas.grid(row=1, column=0, sticky="N, S, E, W")
incBoost_ResistCanvas.grid(row=2, column=0, sticky="N, S, E, W")
armorStatsFrame.grid(row=3, column=0, sticky="N, S, E, W")


# title Placement
titleLabel.grid()

# DamageOutputFrame Placement
damageMin.grid(row=0, column=0, sticky="N, S, E, W")
damageMax.grid(row=0, column=1, sticky="N, S, E, W")
effectHistory.grid(row=1, columnspan=2, sticky="N, S, E, W")

# Attack Cards placement
rowIndx = 0
columnIndx = 0
for i, Btn in enumerate(attackCardBtns):
	Btn.configure(width=floor(attackCardsFrame.winfo_width()/3), image=damageSpells[i].img)
	Btn.grid(row=rowIndx, column=columnIndx, sticky="N, S, E, W")
	columnIndx += 1
	if columnIndx == 3:
		rowIndx += 1
		columnIndx = 0

# BuffsCanvas Placement

deathTrapBtn.grid()
feintBtn.grid()

# Debufs Placement

weakness.grid()

# Inc boost and resist Placement
tempButton.grid()

# Armor Stats placement
deathBoostIn.grid()

root.mainloop()
