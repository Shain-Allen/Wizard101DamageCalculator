from math import floor
import tkinter as tk
import json
import copy

class Spell:
	def __init__(self, cardName, imgFile, school):
		self.cardName = cardName
		self.imgFile = imgFile
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
attackCardsCanvas = tk.Canvas(cardSelectionFrame,width=MAXWINDOWWIDTH/2 , borderwidth=2, relief="solid")
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
attackCardBtns = []

darkSpirteBtnImg = tk.PhotoImage(file=CardDataBank["DamageSpells"][0]["imgFile"])
#darkSpirteBtn = 
attackCardBtns.append(tk.Button(attackCardsCanvas, text=CardDataBank["DamageSpells"][0]["name"], image=darkSpirteBtnImg))
ghoulBtnImg = tk.PhotoImage(file="Images\Ghoul.png")
ghoulBtn = tk.Button(attackCardsCanvas, text="Ghoul", image=ghoulBtnImg)
vampireBtmImg = tk.PhotoImage(file="Images\Vampire.png")
vampireBtm = tk.Button(attackCardsCanvas, text="Vampire", image=vampireBtmImg)
skeletalPirateBtnImg = tk.PhotoImage(file="Images\Skeletal_Pirate.png")
skeletalPirateBtn = tk.Button(attackCardsCanvas, text="Skeletal Pirate", image=skeletalPirateBtnImg)


#for spell in CardDataBank["DamageSpells"]:
#	buttonImg = tk.PhotoImage(spell["imgFile"])
#	button = tk.Button(attackCardsCanvas, textvariable=spell["name"], image=buttonImg)
#	attackCardBtns.append(button)


# BuffsCanvas Creation
deathTrapBtnImg = tk.PhotoImage(file="Images\Death_Trap.png")
deathTrapBtn = tk.Button(buffsCanvas, background="green", text="25%", image=deathTrapBtnImg)
feintBtnImg = tk.PhotoImage(file="Images\Feint.png")
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
attackCardsCanvas.grid(row=0, column=0, sticky="N, S, E, W")
attackCardsCanvas.grid_propagate(0)
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
for Btn in attackCardBtns:
	Btn.configure(width=floor((MAXWINDOWWIDTH/2)/3))
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
