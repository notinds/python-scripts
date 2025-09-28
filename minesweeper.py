import tkinter as tk
from tkinter import messagebox
import random

class MinesweeperGUI:
    def __init__(self, master, size=16, mines=40):
        self.master = master
        self.size = size
        self.mines = mines
        self.frame = tk.Frame(master)
        self.frame.pack()
        self.flag_label = tk.Label(master, text="Flags left: 0")
        self.flag_label.pack()
        self.reset_game()

    def reset_game(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.board = self.generate_board(self.size, self.mines)
        self.revealed = [[False]*self.size for _ in range(self.size)]
        self.flagged = [[False]*self.size for _ in range(self.size)]
        self.buttons = [[None]*self.size for _ in range(self.size)]
        self.flags_left = self.mines
        self.game_over = False
        self.flag_label.config(text=f"Flags left: {self.flags_left}")
        for i in range(self.size):
            for j in range(self.size):
                btn = tk.Button(self.frame, width=2, height=1, command=lambda x=i, y=j: self.on_left_click(x, y))
                btn.grid(row=i, column=j)
                btn.bind('<Button-3>', lambda event, x=i, y=j: self.on_right_click(x, y))
                self.buttons[i][j] = btn
        reset_btn = tk.Button(self.master, text="Reset", command=self.reset_game)
        reset_btn.pack(side=tk.BOTTOM)

    def generate_board(self, size, mines):
        board = [[0 for _ in range(size)] for _ in range(size)]
        mine_positions = set()
        while len(mine_positions) < mines:
            x, y = random.randint(0, size-1), random.randint(0, size-1)
            mine_positions.add((x, y))
        for (x, y) in mine_positions:
            board[x][y] = -1
            for i in range(max(0, x-1), min(size, x+2)):
                for j in range(max(0, y-1), min(size, y+2)):
                    if board[i][j] != -1:
                        board[i][j] += 1
        return board

    def on_left_click(self, x, y):
        if self.game_over or self.revealed[x][y] or self.flagged[x][y]:
            return
        if self.board[x][y] == -1:
            self.reveal_all_mines()
            self.buttons[x][y].config(bg='red')
            self.game_over = True
            messagebox.showinfo("Game Over", "You hit a mine!")
            return
        self.reveal_cells(x, y)
        if self.check_win():
            self.game_over = True
            messagebox.showinfo("Congratulations!", "You cleared the board!")

    def on_right_click(self, x, y):
        if self.game_over or self.revealed[x][y]:
            return
        if self.flagged[x][y]:
            self.flagged[x][y] = False
            self.buttons[x][y].config(text="", bg='SystemButtonFace')
            self.flags_left += 1
        else:
            if self.flags_left == 0:
                return
            self.flagged[x][y] = True
            self.buttons[x][y].config(text="F", fg='red', bg='yellow')
            self.flags_left -= 1
        self.flag_label.config(text=f"Flags left: {self.flags_left}")

    def reveal_cells(self, x, y):
        stack = [(x, y)]
        while stack:
            i, j = stack.pop()
            if not (0 <= i < self.size and 0 <= j < self.size):
                continue
            if self.revealed[i][j] or self.flagged[i][j]:
                continue
            self.revealed[i][j] = True
            val = self.board[i][j]
            btn = self.buttons[i][j]
            btn.config(relief=tk.SUNKEN, state=tk.DISABLED)
            if val == -1:
                btn.config(text='*', bg='gray')
            elif val == 0:
                btn.config(text='', bg='lightgray')
                for ni in range(i-1, i+2):
                    for nj in range(j-1, j+2):
                        if 0 <= ni < self.size and 0 <= nj < self.size:
                            if not self.revealed[ni][nj] and not self.flagged[ni][nj]:
                                stack.append((ni, nj))
            else:
                btn.config(text=str(val), bg='white')

    def reveal_all_mines(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == -1:
                    self.buttons[i][j].config(text='*', bg='gray', relief=tk.SUNKEN)

    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != -1 and not self.revealed[i][j]:
                    return False
        return True

def main():
    root = tk.Tk()
    root.title("minesweeper but by notinds (im dumb as shit)")
    app = MinesweeperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
