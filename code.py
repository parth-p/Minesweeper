from tkinter import *
import random
from tkinter import messagebox
import os
import math

class App:
	def __init__(self,root):
		# import images
		self.tile_plain = PhotoImage(file = "images/tile_plain.gif")
		self.tile_clicked = PhotoImage(file = "images/tile_clicked.gif")
		self.tile_mine = PhotoImage(file = "images/tile_mine.gif")
		self.tile_flag = PhotoImage(file = "images/tile_flag.gif")
		self.tile_wrong = PhotoImage(file = "images/tile_wrong.gif")
		self.tile_happy = PhotoImage(file = "images/happy.gif")
		self.tile_sad = PhotoImage(file = "images/sad.gif")
		self.tile_no = []
		for x in range(1, 9):
			self.tile_no.append(PhotoImage(file = "images/tile_"+str(x)+".gif"))

		self.menubar = Menu(root)
		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="New", command=self.restart)

		self.filemenu.add_separator()

		self.filemenu.add_command(label="Exit", command=root.quit)
		self.menubar.add_cascade(label="Game", menu=self.filemenu)
		self.editmenu = Menu(self.menubar, tearoff=0)
		self.editmenu.add_command(label="Instructions", command=self.instructions)

		#self.editmenu.add_separator()
		#editmenu.add_command(label="About", command=self.about)
		self.menubar.add_cascade(label="Help", menu=self.editmenu)
		root.config(menu=self.menubar)

		self.f0 = Frame(root)
		self.f0.pack()	

		self.b = Button(self.f0 , image=self.tile_happy , command=self.restart)
		self.b.grid(row=0 , column=1)

		self.f1 = Frame(root)
		self.f1.pack()

		# unmarked tile = 0
		# marked = 1
		# bomb = 2

		self.tilet = 100
		self.flagno = 16
		self.sqrt = int(self.tilet**(1/(2.0)))
		self.checkflag = 0
		self.count = 0
		self.flag = [0]*self.tilet
		self.marked = [0]*self.tilet
		self.button = dict({})	
		self.nearby = dict({})
		# creating matrix (10x10) of buttons 
		for i in range(0,self.tilet):
			self.button[i]=Button(self.f1 , image=self.tile_plain)
			self.button[i].bind('<Button-1>' , self.lclick_command(i))
			self.button[i].bind('<Button-3>' , self.rclick_command(i))
		
		for i in range(0,self.tilet):
			self.button[i].grid(row=int(i/self.sqrt) , column=i%self.sqrt)

		self.data = [0]*self.tilet
		for i in range(0,self.tilet):
			self.data[i]=0

		# planting bombs 	
		i=0
		while i!=self.flagno:
			x = random.randrange(self.tilet)
			if self.data[x]==0:
				self.data[x]=2
				i=i+1	

		# for marked[] =>
		#	1 = flag
		#	2 = other	

		# for flag[] =>
		#	0 = no flag
		#	1 = flag
		
		for i in range(0,self.tilet):
			self.nearby[i]=0
			self.marked[i]=0
			self.flag[i]=0

			if i%self.sqrt!=0:
				if self.find_bomb(i-1-self.sqrt):
					self.nearby[i]+=1
			if self.find_bomb(i-self.sqrt):
				self.nearby[i]+=1
			if i%self.sqrt!=self.sqrt-1:
				if self.find_bomb(i-self.sqrt+1):
					self.nearby[i]+=1
			if i%self.sqrt!=0:
				if self.find_bomb(i-1):
					self.nearby[i]+=1
			if i%self.sqrt!=self.sqrt-1:		
				if self.find_bomb(i+1):
					self.nearby[i]+=1												
			if i%self.sqrt!=0:
				if self.find_bomb(i+self.sqrt-1):
					self.nearby[i]+=1
			if self.find_bomb(i+self.sqrt):
				self.nearby[i]+=1
			if i%self.sqrt!=self.sqrt-1:
				if self.find_bomb(i+self.sqrt+1):
					self.nearby[i]+=1											

		self.f2=Frame(root)
		self.f2.pack()

		self.bu = Button(self.f2 , text="Quit" , command=root.quit)
		self.bu.pack()

	def instructions(self):
		os.system("python3 instproj4.py")	

	def restart(self):
		self.b.configure(image = self.tile_happy)
		os.execl(sys.executable, sys.executable, *sys.argv)		

	def rclick_command(self,x):
		return lambda Button: self.rclick(x)

	def lclick_command(self,x):
		return lambda Button: self.lclick(x)		

	def find_bomb(self,key):
		if key>=0 and key<self.tilet:
			if self.data[key]==2:
				return True
			else:
				return False
		else :
			return False

	def rclick(self,x):
		if self.flag[x]==0 and self.marked[x]==0:
			if self.checkflag<self.flagno:		
				self.marked[x]=2
				self.flag[x]=1
				self.button[x].configure(image = self.tile_flag)
				self.checkflag+=1	
		elif self.flag[x]==1 :
			self.marked[x]=0
			self.flag[x]=0
			self.button[x].configure(image = self.tile_plain)
			self.checkflag-=1

	def lclick(self,x):
		if x>=0 and x<self.tilet:
			if self.data[x]==2:
				self.showallbomb()
				self.you_loose()

			elif self.data[x]==0 and self.marked[x]==0:
				if self.nearby[x]>0:
					self.button[x].configure(image = self.tile_no[self.nearby[x]-1])
					self.marked[x]=2
					self.count += 1
				elif self.nearby[x]==0:
					self.button[x].configure(image = self.tile_clicked)
					self.marked[x]=2
					self.count += 1	
					if x%self.sqrt!=0:
						self.lclick(x-self.sqrt-1)
					self.lclick(x-self.sqrt)
					if x%self.sqrt!=self.sqrt-1:
						self.lclick(x-self.sqrt+1)
					if x%self.sqrt!=0:
						self.lclick(x-1)
					if x%self.sqrt!=self.sqrt-1:
						self.lclick(x+1)
					if x%self.sqrt!=0:
						self.lclick(x+self.sqrt-1)
					self.lclick(x+self.sqrt)
					if x%self.sqrt!=self.sqrt-1:
						self.lclick(x+self.sqrt+1)
		if self.count ==self.tilet - self.flagno:
			self.victory()	
		#print(self.count)
						
	def victory(self):
		messagebox.showinfo("Game Over" , "You Win !!" )
		self.restart()				

	def showallbomb(self):
		for x in range(0,self.tilet):
			if self.data[x]==2 	 and self.marked[x]==0:
				self.button[x].configure(image = self.tile_mine)		
			if self.data[x]==0 and self.flag[x]==1:
				self.button[x].configure(image = self.tile_wrong)	

	def you_loose(self):
		messagebox.showinfo("Game Over" , "You Lose" )
		self.b.configure(image = self.tile_sad)		
		self.restart()

root=Tk()
root.title('Minesweeper')
App(root)
root.mainloop()
