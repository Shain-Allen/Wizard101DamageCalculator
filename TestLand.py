import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
import json
from math import floor

from numpy import imag

from Wizard101DamageCalc import Btn

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()

root.geometry("500x500")

Cards = json.load(open("Cards.json"))
DamageSpellBtns = []

for spell in Cards["DamageSpells"]:
	img = ImageTk.PhotoImage(Image.open(spell["imgFile"]))

	btn = customtkinter.CTkButton(master=root, image=img, text="")
	DamageSpellBtns.append(btn)

for btn in DamageSpellBtns:
	btn.grid()


root.mainloop()