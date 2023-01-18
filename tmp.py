# Python Version 2.7.3
# File: minesweeper.py

from tkinter import *
from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime
import pygame
from login import *



pygame.init()

SIZE_X = int(level)
SIZE_Y = int(level)

STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

window = None

test_sound = pygame.mixer.Sound("going_on_foot-133469.mp3")
test_sound.play(-1)

rank_list=[]
score = ""
total_score =""

class Minesweeper:

    def __init__(self, tk):

        # import images
        self.images = {
            "plain": PhotoImage(file = "images/tile_plain.gif"),
            "clicked": PhotoImage(file = "images/tile_clicked.gif"),
            "mine": PhotoImage(file = "images/tile_mine.gif"),
            "flag": PhotoImage(file = "images/tile_flag.gif"),
            "wrong": PhotoImage(file = "images/tile_wrong.gif"),
            "numbers": []
        }
        for i in range(1, 9):
            self.images["numbers"].append(PhotoImage(file = "images/tile_"+str(i)+".gif"))

        # set up frame
        self.tk = tk
        self.frame = Frame(self.tk)
        self.frame.pack()
        
        
        # set up labels/UI
        self.labels = {
            "time": Label(self.frame, text = "00:00:00"),
            "username" : Label(self.frame, text = namesss),
            "mines": Label(self.frame, text = "Mines: 0"),
            "flags": Label(self.frame, text = "Flags: 0"),
            "remain": Label(self.frame, text = "Remain: 0")
            
        }
        self.labels["time"].grid(row = 0, column = 0, columnspan = SIZE_Y) # top full width
        self.labels["username"].grid(row = 0, column = int(SIZE_Y/2)-1, columnspan = SIZE_Y) # bottom left
        
        self.labels["mines"].grid(row = SIZE_X+1, column = 0, columnspan = int(SIZE_Y/2)) # bottom left
        self.labels["flags"].grid(row = SIZE_X+1, column = int(SIZE_Y/2)-1, columnspan = int(SIZE_Y/2)) # bottom right
        self.labels["remain"].grid(row = SIZE_X+1, column = int(SIZE_Y/3)-1, columnspan = int(SIZE_Y/2)) # middle
        

        self.restart() # start game
        self.updateTimer() # init timer

    def setup(self):
        # create flag and clicked tile variables
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None

        # create buttons
        self.tiles = dict({})
        self.mines = 0
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if y == 0:
                    self.tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False

                # tile image changeable for debug reasons:
                gfx = self.images["plain"]

                # currently random amount of mines
                if random.uniform(0.0, 1.0) < 0.1:
                    isMine = True
                    self.mines += 1

                tile = {
                    "id": id,
                    "isMine": isMine,
                    "state": STATE_DEFAULT,
                    "coords": {
                        "x": x,
                        "y": y
                    },
                    "button": Button(self.frame, image = gfx),
                    "mines": 0 # calculated after grid is built
                }

                tile["button"].bind(BTN_CLICK, self.onClickWrapper(x, y))
                tile["button"].bind(BTN_FLAG, self.onRightClickWrapper(x, y))
                tile["button"].grid( row = x+1, column = y ) # offset by 1 row for timer

                self.tiles[x][y] = tile

        # loop again to find nearby mines and display number on tile
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                mc = 0
                for n in self.getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                self.tiles[x][y]["mines"] = mc

    def restart(self):
        self.setup()
        self.refreshLabels()
        
        

    def refreshLabels(self):
        self.labels["flags"].config(text = "Flags: "+str(self.flagCount))
        self.labels["mines"].config(text = "Mines: "+str(self.mines))
        self.labels["remain"].config(text = "Remain: "+str(self.mines- self.flagCount))
    
    '''
    def login(self):
        win = tk.Tk()
        win.geometry("390x180")
        win.title("이름 말해라")
        namesss= ""

        def click_me():
            global namesss
            msgbox.showinfo(title="완료", message=name_entered.get() + '님 안녕하세요! :)')
            namesss = name_entered.get() 

        frame = tk.LabelFrame(win, text='냠', padx=15, pady=15) # padx / pady 내부여백
        frame.pack(padx=10, pady=10) # padx / pady 외부여백

        ttk.Label(frame, text="이름을 입력해주세요.").grid(column=0, row=0)

        name = tk.StringVar()
        name_entered = ttk.Entry(frame, width=15, textvariable=name)
        name_entered.grid(column=0, row=1)


        action = ttk.Button(frame, text="Click!", command=click_me)
        action.grid(column=2, row=1)

        name_entered.focus()
 
        win.mainloop()
    '''
        
    def gameOver(self, won):
        
        max_time= datetime.now() - self.startTime
        max_time_ts = str(max_time).split('.')[0] # drop ms
        rank_list.append(max_time_ts)
        self.startTime=0
        
        global score
        global total_score
        
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if self.tiles[x][y]["isMine"] == False and self.tiles[x][y]["state"] == STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["wrong"])
                if self.tiles[x][y]["isMine"] == True and self.tiles[x][y]["state"] != STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["mine"])

        self.tk.update()

        msg1 = "You Win! Play again?" if won else "You Lose! Play again?"
        res = tkMessageBox.askyesno("Game Over", msg1) 

        cur_score = max_time_ts
        if won==0:

            rank_list.sort(reverse=False) # 점수 오름차순
            ranking = rank_list.index(cur_score)
            
            for i in range(len(rank_list)):
                score = " "
                score = score + "나는 " + namesss +" "+ str(ranking+1)+ "등!! \n" + '\n'.join(rank_list)
            #rank_res = tkMessageBox.showinfo("RANK", score)

            new_window= Tk()
            new_window.title("RANKKKKKKK")
            new_window.geometry("400x400")
            label = Label(new_window, text = score)
            label.pack()
            score = ""
        
        if res:
            self.restart()
            self.updateTimer()
            
        else:
            self.tk.quit()
            
        new_window.mainloop()


    def updateTimer(self):
        ts = "00:00:00"
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            ts = str(delta).split('.')[0] # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts # zero-pad
        self.labels["time"].config(text = ts)
        self.frame.after(100, self.updateTimer)

    def getNeighbors(self, x, y):
        neighbors = []
        coords = [
            {"x": x-1,  "y": y-1},  #top right
            {"x": x-1,  "y": y},    #top middle
            {"x": x-1,  "y": y+1},  #top left
            {"x": x,    "y": y-1},  #left
            {"x": x,    "y": y+1},  #right
            {"x": x+1,  "y": y-1},  #bottom right
            {"x": x+1,  "y": y},    #bottom middle
            {"x": x+1,  "y": y+1},  #bottom left
        ]
        for n in coords:
            try:
                neighbors.append(self.tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors

    def onClickWrapper(self, x, y):
        return lambda Button: self.onClick(self.tiles[x][y])

    def onRightClickWrapper(self, x, y):
        return lambda Button: self.onRightClick(self.tiles[x][y])

    def onClick(self, tile):
        if self.startTime == None:
            self.startTime = datetime.now()

        if tile["isMine"] == True:
            # end game
            self.gameOver(False)
            return

        # change image
        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            self.clearSurroundingTiles(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"][tile["mines"]-1])
        # if not already set as clicked, change state and count
        if tile["state"] != STATE_CLICKED:
            tile["state"] = STATE_CLICKED
            self.clickedCount += 1
        if self.clickedCount == (SIZE_X * SIZE_Y) - self.mines:
            self.gameOver(True)
            

    def onRightClick(self, tile):
        if self.startTime == None:
            self.startTime = datetime.now()

        # if not clicked
        if tile["state"] == STATE_DEFAULT:
            tile["button"].config(image = self.images["flag"])
            tile["state"] = STATE_FLAGGED
            tile["button"].unbind(BTN_CLICK)
            # if a mine
            if tile["isMine"] == True:
                self.correctFlagCount += 1
            self.flagCount += 1
            self.refreshLabels()
        # if flagged, unflag
        elif tile["state"] == 2:
            tile["button"].config(image = self.images["plain"])
            tile["state"] = 0
            tile["button"].bind(BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
            # if a mine
            if tile["isMine"] == True:
                self.correctFlagCount -= 1
            self.flagCount -= 1
            self.refreshLabels()

    def clearSurroundingTiles(self, id):
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in self.getNeighbors(x, y):
                self.clearTile(tile, queue)

    def clearTile(self, tile, queue):
        if tile["state"] != STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            queue.append(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"][tile["mines"]-1])

        tile["state"] = STATE_CLICKED
        self.clickedCount += 1

### END OF CLASSES ###

def main():
    # create Tk instance
    window = Tk()
    # set program title
    window.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(window)
    # run event loop
    window.mainloop()

if __name__ == "__main__":
    main()
