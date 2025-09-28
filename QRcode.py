import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import io

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("qr thing (yes really)")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="Enter text or URL:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        self.generate_btn = tk.Button(root, text="Generate QR Code", command=self.generate_qr)
        self.generate_btn.pack(pady=10)

        self.qr_canvas = tk.Label(root)
        self.qr_canvas.pack(pady=10)

        self.save_btn = tk.Button(root, text="Save QR Code", command=self.save_qr, state=tk.DISABLED)
        self.save_btn.pack(pady=10)

        self.qr_image = None
        self.qr_pil_image = None

    def generate_qr(self):
        data = self.entry.get().strip()
        if not data:
            messagebox.showwarning("Input Error", "Please enter some text or URL.")
            return
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        self.qr_pil_image = img
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        pil_img = Image.open(img_byte_arr)
        pil_img = pil_img.resize((250, 250), Image.LANCZOS)
        self.qr_image = ImageTk.PhotoImage(pil_img)
        self.qr_canvas.config(image=self.qr_image)
        self.qr_canvas.image = self.qr_image  # Prevent garbage collection
        self.save_btn.config(state=tk.NORMAL)

    def save_qr(self):
        if self.qr_pil_image is None:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.qr_pil_image.save(file_path)
            messagebox.showinfo("Saved", f"QR code saved to {file_path}")

def main():
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
