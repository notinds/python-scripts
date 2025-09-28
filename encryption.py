import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import base64
import os
try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography'])
    from cryptography.fernet import Fernet, InvalidToken


def derive_key(user_key: str) -> bytes:
    key = user_key.encode('utf-8')
    key = key.ljust(32, b'0')[:32]
    return base64.urlsafe_b64encode(key)


def encrypt_text(text: str, key: str) -> str:
    f = Fernet(derive_key(key))
    token = f.encrypt(text.encode('utf-8'))
    return token.decode('utf-8')


def decrypt_text(token: str, key: str) -> str:
    f = Fernet(derive_key(key))
    try:
        text = f.decrypt(token.encode('utf-8'))
        return text.decode('utf-8')
    except InvalidToken:
        raise ValueError('Invalid key or corrupted data.')


def encrypt_file(filepath: str, key: str, savepath: str):
    f = Fernet(derive_key(key))
    with open(filepath, 'rb') as infile:
        data = infile.read()
    token = f.encrypt(data)
    with open(savepath, 'wb') as outfile:
        outfile.write(token)

def decrypt_file(filepath: str, key: str, savepath: str):
    f = Fernet(derive_key(key))
    with open(filepath, 'rb') as infile:
        token = infile.read()
    try:
        data = f.decrypt(token)
    except InvalidToken:
        raise ValueError('Invalid key or corrupted data.')
    with open(savepath, 'wb') as outfile:
        outfile.write(data)


class EncryptorGUI:
    def __init__(self, root):
        self.root = root
        root.title('what the fuck is a key')
        root.geometry('500x500')
        root.resizable(False, False)
        root.configure(bg='#23272f')

        self.mode = tk.StringVar(value='encrypt')
        self.filepath = None

        # Title
        tk.Label(root, text='Encrypt/Decrypt Anything', font=('Segoe UI', 18, 'bold'), fg='#fff', bg='#23272f').pack(pady=10)

        # Mode selection
        mode_frame = tk.Frame(root, bg='#23272f')
        tk.Radiobutton(mode_frame, text='Encrypt', variable=self.mode, value='encrypt', fg='#fff', bg='#23272f', selectcolor='#23272f', font=('Segoe UI', 10)).pack(side='left', padx=10)
        tk.Radiobutton(mode_frame, text='Decrypt', variable=self.mode, value='decrypt', fg='#fff', bg='#23272f', selectcolor='#23272f', font=('Segoe UI', 10)).pack(side='left', padx=10)
        mode_frame.pack(pady=5)

        # Key entry
        tk.Label(root, text='Key:', fg='#fff', bg='#23272f', font=('Segoe UI', 10)).pack()
        self.key_entry = tk.Entry(root, show='*', width=40, font=('Segoe UI', 10))
        self.key_entry.pack(pady=5)

        # Text area
        tk.Label(root, text='Text to Encrypt/Decrypt:', fg='#fff', bg='#23272f', font=('Segoe UI', 10)).pack()
        self.text_area = scrolledtext.ScrolledText(root, width=55, height=8, font=('Segoe UI', 10), bg='#1e222a', fg='#fff', insertbackground='#fff')
        self.text_area.pack(pady=5)

        # File buttons
        file_frame = tk.Frame(root, bg='#23272f')
        tk.Button(file_frame, text='Select File...', command=self.select_file, font=('Segoe UI', 9)).pack(side='left', padx=5)
        tk.Button(file_frame, text='Clear File', command=self.clear_file, font=('Segoe UI', 9)).pack(side='left', padx=5)
        self.file_label = tk.Label(file_frame, text='No file selected', fg='#aaa', bg='#23272f', font=('Segoe UI', 9))
        self.file_label.pack(side='left', padx=5)
        file_frame.pack(pady=5)

        # Action button
        tk.Button(root, text='Go!', command=self.process, font=('Segoe UI', 12, 'bold'), bg='#3a82ee', fg='#fff', activebackground='#2563c7', activeforeground='#fff', width=10).pack(pady=10)

        # Output area
        tk.Label(root, text='Output:', fg='#fff', bg='#23272f', font=('Segoe UI', 10)).pack()
        self.output_area = scrolledtext.ScrolledText(root, width=55, height=6, font=('Segoe UI', 10), bg='#1e222a', fg='#fff', insertbackground='#fff')
        self.output_area.pack(pady=5)
        tk.Button(root, text='Copy Output', command=self.copy_output, font=('Segoe UI', 9)).pack(pady=2)

    def select_file(self):
        filetypes = [('All files', '*.*')]
        path = filedialog.askopenfilename(title='Select file to encrypt/decrypt', filetypes=filetypes)
        if path:
            self.filepath = path
            self.file_label.config(text=os.path.basename(path), fg='#fff')
        else:
            self.filepath = None
            self.file_label.config(text='No file selected', fg='#aaa')

    def clear_file(self):
        self.filepath = None
        self.file_label.config(text='No file selected', fg='#aaa')

    def process(self):
        key = self.key_entry.get()
        if not key:
            messagebox.showerror('Error', 'Please enter a key.')
            return
        mode = self.mode.get()
        if self.filepath:
            # File mode
            savepath = filedialog.asksaveasfilename(title='Save result as', defaultextension='.bin' if mode=='encrypt' else '', filetypes=[('All files', '*.*')])
            if not savepath:
                return
            try:
                if mode == 'encrypt':
                    encrypt_file(self.filepath, key, savepath)
                else:
                    decrypt_file(self.filepath, key, savepath)
                messagebox.showinfo('Success', f'File {mode}ed and saved to {savepath}')
            except Exception as e:
                messagebox.showerror('Error', str(e))
        else:
            # Text mode
            text = self.text_area.get('1.0', tk.END).strip()
            if not text:
                messagebox.showerror('Error', 'Please enter text to process.')
                return
            try:
                if mode == 'encrypt':
                    result = encrypt_text(text, key)
                else:
                    result = decrypt_text(text, key)
                self.output_area.delete('1.0', tk.END)
                self.output_area.insert(tk.END, result)
            except Exception as e:
                messagebox.showerror('Error', str(e))

    def copy_output(self):
        output = self.output_area.get('1.0', tk.END).strip()
        if output:
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            messagebox.showinfo('Copied', 'Output copied to clipboard!')


def main():
    root = tk.Tk()
    app = EncryptorGUI(root)
    root.mainloop()

# im going to fucking kill myself i cant do this anymore
# help me please

if __name__ == '__main__':
    main()

