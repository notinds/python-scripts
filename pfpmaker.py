import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageOps

def make_circular_pfp(profile_path, border_path, output_path):
    # Target output size
    output_size = 200
    border_thickness = 10  # 10px border all around
    profile_diameter = output_size - 2 * border_thickness  # 180

    # Open and process profile image
    profile = Image.open(profile_path).convert("RGBA")
    profile = ImageOps.fit(profile, (profile_diameter, profile_diameter), centering=(0.5, 0.5))

    # Create circular mask for profile
    mask = Image.new("L", (profile_diameter, profile_diameter), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, profile_diameter, profile_diameter), fill=255)
    profile.putalpha(mask)

    # Open and resize border image
    border = Image.open(border_path).convert("RGBA")
    border = ImageOps.fit(border, (output_size, output_size), centering=(0.5, 0.5))

    # Create output image
    output = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))
    output.paste(border, (0, 0))
    output.paste(profile, (border_thickness, border_thickness), profile)
    output.save(output_path)


class PFPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PFP Maker")
        self.profile_path = ""
        self.border_path = ""

        tk.Label(root, text="Profile Image:").pack()
        self.profile_btn = tk.Button(root, text="Choose...", command=self.choose_profile)
        self.profile_btn.pack()

        tk.Label(root, text="Border Image:").pack()
        self.border_btn = tk.Button(root, text="Choose...", command=self.choose_border)
        self.border_btn.pack()

        self.make_btn = tk.Button(root, text="Make PFP", command=self.make_pfp, state=tk.DISABLED)
        self.make_btn.pack(pady=10)

    def choose_profile(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.profile_path = path
            self.check_ready()

    def choose_border(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.border_path = path
            self.check_ready()

    def check_ready(self):
        if self.profile_path and self.border_path:
            self.make_btn.config(state=tk.NORMAL)

    def make_pfp(self):
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if output_path:
            try:
                make_circular_pfp(self.profile_path, self.border_path, output_path)
                messagebox.showinfo("Success", "Profile picture created!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PFPApp(root)
    root.mainloop()
