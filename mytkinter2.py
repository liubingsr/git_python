import tkinter as tk
from tkinter import messagebox

a = 100

class Application(tk.Frame):
	def __init__(self, master = None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Hello World\n(click me)"
		self.hi_there["fg"] = "green"
		self.hi_there["command"] = self.say_hi
		self.hi_there.pack(side = "top")
		
		# self.hi_there = tk.Button(self, text = "HI", fg = "green", command = self.say_hi)
		self.quit = tk.Button(self, text = "QUIT", fg = "red", command = self.master.destroy)
		self.quit.pack(side = "bottom")
		self.cal = tk.Button(self, text = "CAL", fg = "blue", command = self.cal)		
		self.cal.pack(side = "right")

		self.label01 = tk.Label(self, text = "宋睿", width = 4, height = 2, bg = "blue", fg = "white")
		self.label01.pack(side = "left")

		global photo 
		photo = tk.PhotoImage(file = "ess.gif")
		self.label02 = tk.Label(self, image = photo)
		self.label02.pack()

		self.label03 = tk.Label(self, text = "欢迎使用储能系统容量优化配置计算软件", borderwidth = 1, relief = "solid", justify = "center")
		self.label03.pack()

		v1 = tk.StringVar()
		self.entry01 = tk.Entry(self, textvariable = v1)
		self.entry01.pack()

	def say_hi(self):
		print("hi there, everyone!")
		print("abcd")
	
	def cal(self):
		b = a - 1
		print(b)
		for i in range(b):
			messagebox.showinfo("送花", f"送你{b}朵玫瑰花")

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry("1000x1000+200+300")
	root.title("一个经典的GUI程序类测试")
	app = Application(master = root)
	app.mainloop()