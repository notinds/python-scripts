import tkinter as tk
from tkinter import simpledialog

# Game settings
WIDTH = 800
HEIGHT = 400
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
BALL_SIZE = 20
PADDLE_SPEED = 20
BALL_X_SPEED = 6
BALL_Y_SPEED = 4

# AI difficulty settings
AI_DIFFICULTY = {
    'Easy': {'speed': 8, 'delay': 40},
    'Medium': {'speed': 14, 'delay': 20},
    'Hard': {'speed': 20, 'delay': 0}
}

class PongGame:
    def __init__(self, master):
        self.master = master
        self.master.title('pong')
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()
        # Paddles
        self.paddle1 = self.canvas.create_rectangle(20, HEIGHT//2 - PADDLE_HEIGHT//2, 20 + PADDLE_WIDTH, HEIGHT//2 + PADDLE_HEIGHT//2, fill='white')
        self.paddle2 = self.canvas.create_rectangle(WIDTH-30, HEIGHT//2 - PADDLE_HEIGHT//2, WIDTH-30 + PADDLE_WIDTH, HEIGHT//2 + PADDLE_HEIGHT//2, fill='white')
        # Ball
        self.ball = self.canvas.create_oval(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, WIDTH//2 + BALL_SIZE//2, HEIGHT//2 + BALL_SIZE//2, fill='white')
        self.ball_x_speed = BALL_X_SPEED
        self.ball_y_speed = BALL_Y_SPEED
        # Scores
        self.score1 = 0
        self.score2 = 0
        self.score_text = self.canvas.create_text(WIDTH//4, 30, text='0', font=('Arial', 24), fill='white')
        self.score_text2 = self.canvas.create_text(3*WIDTH//4, 30, text='0', font=('Arial', 24), fill='white')
        # Game mode and AI difficulty
        self.mode = simpledialog.askstring('Game Mode', 'Enter mode: PvP or PvAI', parent=master)
        if self.mode and self.mode.lower() == 'pvai':
            self.ai_difficulty = simpledialog.askstring('AI Difficulty', 'Enter difficulty: Easy, Medium, Hard', parent=master)
            if self.ai_difficulty not in AI_DIFFICULTY:
                self.ai_difficulty = 'Medium'
        else:
            self.mode = 'PvP'
            self.ai_difficulty = None
        # AI randomness seed
        import random
        self.random = random
        # Bindings
        self.master.bind('<w>', lambda e: self.move_paddle(self.paddle1, -PADDLE_SPEED))
        self.master.bind('<s>', lambda e: self.move_paddle(self.paddle1, PADDLE_SPEED))
        if self.mode == 'PvP':
            self.master.bind('<Up>', lambda e: self.move_paddle(self.paddle2, -PADDLE_SPEED))
            self.master.bind('<Down>', lambda e: self.move_paddle(self.paddle2, PADDLE_SPEED))
        self.animate()

    def move_paddle(self, paddle, dy):
        x0, y0, x1, y1 = self.canvas.coords(paddle)
        if y0 + dy >= 0 and y1 + dy <= HEIGHT:
            self.canvas.move(paddle, 0, dy)

    def animate(self):
        self.move_ball()
        if self.mode == 'PvAI':
            self.move_ai_paddle()
        self.master.after(20, self.animate)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_x_speed, self.ball_y_speed)
        bx0, by0, bx1, by1 = self.canvas.coords(self.ball)
        # Top and bottom collision
        if by0 <= 0 or by1 >= HEIGHT:
            self.ball_y_speed = -self.ball_y_speed
        # Paddle collision
        if self.hit_paddle(self.paddle1) or self.hit_paddle(self.paddle2):
            self.ball_x_speed = -self.ball_x_speed
        # Left and right wall (score)
        if bx0 <= 0:
            self.score2 += 1
            self.update_score()
            self.reset_ball(direction=1)
        elif bx1 >= WIDTH:
            self.score1 += 1
            self.update_score()
            self.reset_ball(direction=-1)

    def move_ai_paddle(self):
        bx0, by0, bx1, by1 = self.canvas.coords(self.ball)
        px0, py0, px1, py1 = self.canvas.coords(self.paddle2)
        ai = AI_DIFFICULTY.get(self.ai_difficulty, AI_DIFFICULTY['Medium'])
        ball_center = (by0 + by1) / 2
        paddle_center = (py0 + py1) / 2
        # AI only reacts if ball is past halfway (reaction zone)
        reaction_zone = WIDTH * 0.6 if self.ai_difficulty == 'Hard' else WIDTH * 0.75
        if bx0 < reaction_zone:
            return
        # Add randomness to AI movement for Easy and Medium
        if self.ai_difficulty == 'Easy':
            if self.random.random() < 0.3:
                return
        elif self.ai_difficulty == 'Medium':
            if self.random.random() < 0.1:
                return
        # Limit AI speed so it can't always catch up
        max_move = ai['speed']
        diff = ball_center - paddle_center
        if abs(diff) > max_move:
            move = max_move if diff > 0 else -max_move
        else:
            move = diff
        # Add a small error for all difficulties
        if self.ai_difficulty == 'Easy':
            move += self.random.randint(-8, 8)
        elif self.ai_difficulty == 'Medium':
            move += self.random.randint(-4, 4)
        elif self.ai_difficulty == 'Hard':
            move += self.random.randint(-1, 1)
        self.move_paddle(self.paddle2, move)

    def hit_paddle(self, paddle):
        px0, py0, px1, py1 = self.canvas.coords(paddle)
        bx0, by0, bx1, by1 = self.canvas.coords(self.ball)
        return px1 >= bx0 and px0 <= bx1 and py1 >= by0 and py0 <= by1

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=str(self.score1))
        self.canvas.itemconfig(self.score_text2, text=str(self.score2))

    def reset_ball(self, direction):
        self.canvas.coords(self.ball, WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, WIDTH//2 + BALL_SIZE//2, HEIGHT//2 + BALL_SIZE//2)
        self.ball_x_speed = direction * BALL_X_SPEED
        self.ball_y_speed = BALL_Y_SPEED

if __name__ == '__main__':
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()
