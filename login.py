import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox

win = tk.Tk()
win.geometry("390x180")
win.title("ID 입력")
names= ""

def click_me():
    global namesss
    msgbox.showinfo(title="완료", message=name_entered.get() + '님 안녕하세요! :)')
    namesss = name_entered.get() 

frame = tk.LabelFrame(win, text='로그인', padx=15, pady=15) # padx / pady 내부여백
frame.pack(padx=10, pady=10) # padx / pady 외부여백

ttk.Label(frame, text="이름을 입력해주세요.").grid(column=0, row=0)

name = tk.StringVar()
name_entered = ttk.Entry(frame, width=15, textvariable=name)
name_entered.grid(column=0, row=1)


action = ttk.Button(frame, text="Click!", command=click_me)
action.grid(column=2, row=1)

name_entered.focus()

win.mainloop()

