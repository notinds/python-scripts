import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("snake")
        self.width = 400
        self.height = 400
        self.cell_size = 20
        self.direction = 'Right'
        self.running = True
        self.speed = 150  # milliseconds

        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg='black')
        self.canvas.pack()

        self.score = 0
        self.score_label = tk.Label(master, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack()

        self.speed_scale = tk.Scale(master, from_=50, to=300, orient=tk.HORIZONTAL, label="Speed (ms)", command=self.change_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.pack()

        self.reset_game()
        self.master.bind('<Key>', self.on_key_press)
        self.after_id = None
        self.game_loop()

    def reset_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'Right'
        self.score = 0
        self.running = True
        self.food = self.spawn_food()
        self.update_score()
        self.canvas.delete('all')
        self.draw_snake()
        self.draw_food()

    def spawn_food(self):
        while True:
            x = random.randint(0, (self.width - self.cell_size) // self.cell_size) * self.cell_size
            y = random.randint(0, (self.height - self.cell_size) // self.cell_size) * self.cell_size
            if (x, y) not in self.snake:
                return (x, y)

    def draw_snake(self):
        self.canvas.delete('snake')
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+self.cell_size, y+self.cell_size, fill='lime', tag='snake')

    def draw_food(self):
        x, y = self.food
        self.canvas.delete('food')
        self.canvas.create_oval(x, y, x+self.cell_size, y+self.cell_size, fill='red', tag='food')

    def move_snake(self):
        if not self.running:
            return
        head_x, head_y = self.snake[0]
        if self.direction == 'Left':
            new_head = (head_x - self.cell_size, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + self.cell_size, head_y)
        elif self.direction == 'Up':
            new_head = (head_x, head_y - self.cell_size)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + self.cell_size)
        else:
            return

        # Check collisions
        if (
            new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake
        ):
            self.game_over()
            return

        self.snake = [new_head] + self.snake
        if new_head == self.food:
            self.score += 1
            self.update_score()
            self.food = self.spawn_food()
            self.draw_food()
        else:
            self.snake.pop()
        self.draw_snake()

    def on_key_press(self, event):
        key = event.keysym
        opposites = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
        if key in ['Left', 'Right', 'Up', 'Down']:
            if len(self.snake) > 1 and opposites[key] == self.direction:
                return  # Prevent reversing
            self.direction = key
        elif key == 'r' and not self.running:
            self.reset_game()
            self.running = True
            self.game_loop()

    def game_over(self):
        self.running = False
        self.canvas.create_text(self.width//2, self.height//2, text="GAME OVER\nPress 'r' to restart", fill='white', font=("Arial", 18), tag='gameover')

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def change_speed(self, val):
        self.speed = int(val)

    def game_loop(self):
        if self.running:
            self.move_snake()
            self.after_id = self.master.after(self.speed, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

