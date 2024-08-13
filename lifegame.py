import tkinter as tk
from tkinter import ttk
from random import randint
import time
import math
from tkinter import font

# 変数・定数の定義 --- (*1)
# 600 1(12, 50) 2(24 25) 3(40, 15) 4(60, 12) 5(120 5)
SIZE_LIST = [12, 24, 40, 60, 120]
COLS, ROWS = [SIZE_LIST[2], SIZE_LIST[2]] # ステージのサイズを定義
CW = 600//COLS # セルの描画サイズ

root_width = CW * COLS
root_height = CW * ROWS


gray = "gray90"
white = "white"
black = "black"


class MyFrame(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)



        # ボタンを作成
        self.b = ttk.Button(self, text="スタート", command=self.start_stop)
        self.b2 = ttk.Button(self, text="ステップ", command=self.step)
        self.b3 = ttk.Button(self, text="ランダム", command=self.reset_random)
        self.b4 = ttk.Button(self, text="リセット", command=self.reset_all)

        self.b.grid(row = 0, column = 0, padx=5)
        self.b2.grid(row = 1, column = 0, padx=5)
        self.b3.grid(row = 2, column = 0, padx=5)
        self.b4.grid(row = 3, column = 0, padx=5)

        label1 = ttk.Label(self, text='速度', font=("", 14)) # (left, top, right, bottom)
        label1.grid(row=4, column=0, sticky=tk.S)

        # 世代を進める速度を変更するためのスライドバー
        self.scale1 = tk.Scale(self, from_=1, to=2000, orient=tk.HORIZONTAL)
        self.scale1.set(1000)
        self.scale1.grid(row=5, column=0, sticky=tk.N)

        label2 = ttk.Label(self, text='確率', font=("", 14))
        label2.grid(row=6, column=0, sticky=tk.S)

        # ランダム生成の確率を変更するためのスライドバー
        self.scale2 = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.scale2.set(50)
        self.scale2.grid(row=7, column=0, sticky=tk.N)

        label3 = ttk.Label(self, text='フィールド', font=("", 14))
        label3.grid(row=8, column=0, sticky=tk.S)

        # フィールドの大きさを変更するためのスライドバー
        self.scale3 = tk.Scale(self, from_=0, to=4, orient=tk.HORIZONTAL)
        self.scale3.set(2)
        self.scale3.grid(row=9, column=0, sticky=tk.N)


        # ライフゲームのキャンバスを作成
        self.cv = tk.Canvas(self, width=root_width, height=root_height, background=white)
        self.cv.grid(row=0, column=1, rowspan=16)


        # 左クリックでclick_cellを実行
        self.cv.bind('<Button-1>', self.click_cell)

        # 時間経過で世代を進めるか
        self.start = True

        # データのセット
        self.data = []
        self.setdata()
        self.draw_stage()
        self.start = False
    
    def change_size(self):
        global COLS
        global ROWS
        global CW
        COLS = SIZE_LIST[self.scale3.get()]
        ROWS = SIZE_LIST[self.scale3.get()]
        CW = 600//COLS

    def start_stop(self):
        if self.start == False:
            self.start = True
            self.b['text'] = "ストップ"
        else:
            self.start = False
            self.b['text'] = "スタート"

    def step(self):
        self.start = True
        self.next_turn()
        self.draw_stage()
        self.start = False
        self.b['text'] = "スタート"

    def reset_random(self):
        self.setdata()
        self.start = True
        self.draw_stage()
        self.start = False
        self.b['text'] = "スタート"
    
    def reset_all(self):
        self.change_size()
        self.data = [[0] * COLS for i in range(ROWS)]
        self.step()

    def setdata(self):
        self.change_size()
        self.data = []
        for y in range(0, ROWS): # ステージをランダムに初期化
            self.data.append([(randint(0, 99) < self.scale2.get()) for x in range(0, COLS)])

    def click_cell(self, event):
        x, y = event.x, event.y
        x = x // CW
        y = y // CW
        self.data[y][x] = not self.data[y][x]
        self.start = True
        self.draw_stage()
        self.start = False
        self.b['text'] = "スタート"


    # ライフゲームのルールを実装したもの --- (*2)
    def check(self, x, y):
        # 周囲の生存セルを数える
        cnt = 0
        tbl = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        for t in tbl:
            xx, yy = [x + t[0], y + t[1]]
            if 0 <= xx < COLS and 0 <= yy < ROWS:
                if self.data[yy][xx]:
                    cnt += 1
        # ルールに沿って次世代の生死を決める
        if cnt == 3:
            return True # 誕生
        if self.data[y][x]:
            if 2 <= cnt <= 3: return True # 生存
            return False # 過疎 or 過密
        return self.data[y][x]

    # データを次の世代に進める --- (*3)
    def next_turn(self):
        if self.start == False:
            pass
        else:
            data2 = []
            for y in range(0, ROWS):
                data2.append([self.check(x, y) for x in range(0, COLS)])
            self.data = data2 # データの内容を次の世代へ差し替え

    def draw_stage(self):
        if self.start == False:
            pass
        else:
            self.cv.delete('all') # 既存の描画内容を破棄
            for y in range(0, ROWS):
                for x in range(0, COLS):
                    if not self.data[y][x]: continue
                    x1, y1 = [x * CW, y * CW]
                    self.cv.create_rectangle(x1+1, y1+1, x1 + CW-1, y1 + CW-1,
                        fill="red", width=0) # 生きているセルを描画


root = tk.Tk()
root.title("ライフゲーム")
f = MyFrame(root)
f.pack()

def game_loop():
    f.next_turn() # 世代を進める
    f.draw_stage() # ステージを描画
    root.after(f.scale1.get(), game_loop) # 指定時間後に再度描画

game_loop() # ゲームループを実行
root.mainloop()
