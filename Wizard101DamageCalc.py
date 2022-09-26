import tkinter as tk

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


root = tk.Tk()

root.configure(height=1280, width=720)

# create Containers
title = tk.Frame(root, borderwidth=1, relief="solid", height=80, width=720)
damageOutput = tk.Frame(root, width=720)
cardSelection = tk.Frame(root, height=1000, width=720)
attackCards = tk.Canvas(cardSelection, borderwidth=2, relief="solid")
modifications = tk.Frame(cardSelection)
buffs = tk.Canvas(modifications, borderwidth=2, relief="solid")
debuffs = tk.Canvas(modifications, borderwidth=2, relief="solid")
incBoost_Resist = tk.Canvas(modifications, borderwidth=2, relief="solid")
armorStats = tk.Frame(modifications, borderwidth=2, relief="solid")

# Title creation
titleLabel = tk.Label(title, text="Wizard 101 Damage Calculator", justify=tk.CENTER)

# DamageOutput
damageMinVar = tk.StringVar(damageOutput)
damageMinVar.set("0")

damageMaxVar = tk.StringVar(damageOutput)
damageMaxVar.set("0")

effectHistoryVar = tk.StringVar(damageOutput)
effectHistoryVar.set("")

damageMin = tk.Label(
	damageOutput, textvariable=damageMinVar, borderwidth=2, relief="solid"
)
damageMax = tk.Label(
	damageOutput, textvariable=damageMaxVar, borderwidth=2, relief="solid"
)
effectHistory = tk.Label(
	damageOutput, textvariable=effectHistoryVar, width=50, borderwidth=2, relief="solid"
)

# Damage Cards creation
ghoulBtnImg = tk.PhotoImage(file="Images\Ghoul.png")
ghoulBtn = tk.Button(attackCards, text="Ghoul", image=ghoulBtnImg)
vampireBtmImg = tk.PhotoImage(file="Images\Vampire.png")
vampireBtm = tk.Button(attackCards, text="Vampire", image=vampireBtmImg)
skeletalPirateBtnImg = tk.PhotoImage(file="Images\Skeletal_Pirate.png")
skeletalPirateBtn = tk.Button(
	attackCards, text="Skeletal Pirate", image=skeletalPirateBtnImg
)

# Buffs Creation
deathTrapBtnImg = tk.PhotoImage(file="Images\Death_Trap.png")
deathTrapBtn = tk.Button(buffs, background="green", text="25%", image=deathTrapBtnImg)
feintBtn = tk.Button(buffs, background="green", text="70%")

# Debufs Creation
weakness = tk.Button(debuffs, background="red", text="-25")

# Inc boost and resist Creation
tempButton = tk.Button(incBoost_Resist, background="grey", text="Tempt")

# Armor Stats creation
deathBoost = tk.LabelFrame(armorStats, text="death boost:")
deathBoostIn = tk.Entry(deathBoost, name="death boost: ")

# -------------------------------------------------------------------------------------------------------

# place Containers
title.grid(row=0, column=0)
damageOutput.grid(row=1, column=0)
cardSelection.grid(row=2, column=0)
attackCards.grid(row=0, column=0, sticky=tk.N)
attackCards.grid_propagate(0)
modifications.grid(row=0, column=1)
buffs.grid(row=0, column=0)
debuffs.grid(row=1, column=0)
incBoost_Resist.grid(row=2, column=0)
armorStats.grid(row=3, column=0)

# title Placement
titleLabel.grid()

# DamageOutput Placement
damageMin.grid(row=0, column=0, sticky="N, S, E, W")
damageMax.grid(row=0, column=1, sticky="N, S, E, W")
effectHistory.grid(row=1, columnspan=2, sticky="N, S, E, W")

# Damage Cards placement
rowIndx = 0
columnIndx = 0
for Btn in attackCardBtns:
	Btn.configure(width=120)
	Btn.grid(row=rowIndx, column=columnIndx, sticky="N, S, E, W")
	columnIndx += 1
	if columnIndx == 3:
		rowIndx += 1
		columnIndx = 0

# Buffs Placement

deathTrapBtn.grid()
feintBtn.grid()

# Debufs Placement

weakness.grid()

# Inc boost and resist Placement
tempButton.grid()

# Armor Stats placement
deathBoostIn.grid()

root.mainloop()
