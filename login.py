import tkinter as tk
import database
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk


root = tk.Tk()
root.title('Login Page')
root.geometry('900x500+300+100')
root.resizable(0, 0)


def login():
    if database.validate_user(username.get(), password.get()):
        messagebox.showinfo('Loading…', '███████▒▒▒ ↻\n\n Login is successful!')
        root.destroy()
        import system
    else:
        messagebox.showerror('↻ Try again ↻', 'Incorrect login details or user not registered.')


def open_signup_window():
    signup_window = tk.Toplevel(root)
    signup_window.title("Signup")
    signup_window.geometry("400x300+250+210")
    signup_window.configure(bg="#212162")

    header = tk.Label(signup_window, text="Create Your Account", bg="#212162", fg="white", font=("Helvetica", 16, "bold"))
    header.pack(pady=10)

    form_frame = tk.Frame(signup_window, bg="#34495e", padx=20, pady=20, relief="ridge", bd=2)
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Username", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, sticky="e")
    new_username = tk.Entry(form_frame, font=("Helvetica", 12), width=20)
    new_username.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(form_frame, text="Password", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=1, column=0, pady=5, sticky="e")
    new_password = tk.Entry(form_frame, show="*", font=("Helvetica", 12), width=20)
    new_password.grid(row=1, column=1, pady=5, padx=10)

    def signup_action():
        if database.register_user(new_username.get(), new_password.get()):
            messagebox.showinfo("Success", "███████▒▒▒ ↻\n\n Signup is successful!")
            signup_window.destroy() 
        else:
            messagebox.showerror("Error", "Username already exists.")

    tk.Button(signup_window, text="Sign Up", command=signup_action, bg="#34495e", fg="white", font=("Helvetica", 10, "bold"), width=15).pack(pady=10)




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\User\miniconda3\envs\myproject\MY SYSTEM\assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


bg_image = None

# Load images
def load_images():
    global bg_image
    try:
        bg_image_path = relative_to_assets("bg.png")
        bg_image = ImageTk.PhotoImage(Image.open(bg_image_path))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load background image: {e}")


load_images()


canvas = tk.Canvas(root, width=900, height=500)
canvas.pack(fill='both', expand=True)


if bg_image:
    canvas.create_image(0, 0, image=bg_image, anchor='nw')
else:
    messagebox.showerror("Error", "Background image not loaded!")


title = tk.Label(root, text='Welcome back!', bg='#222264', fg='#fff', font=('Helvetica', 23, 'bold'))
title.place(x=80, y=80)


username_label = tk.Label(root, text='Username:', bg='#07966d', fg='#fff', font=('Helvetica', 10, 'bold'))
username_label.place(x=80, y=160)
username = tk.Entry(root, font=('Helvetica', 13, 'bold'), width=25, relief=tk.RIDGE, bd=4, highlightbackground='#07966d', highlightcolor='yellow', highlightthickness=2)
username.place(x=80, y=180)

password_label = tk.Label(root, text='Password:', bg='#07966d', fg='#fff', font=('Helvetica', 10, 'bold'))
password_label.place(x=80, y=230)
password = tk.Entry(root, font=('Helvetica', 13, 'bold'), width=25, show='*', relief=tk.RIDGE, bd=5, highlightbackground='#07966d', highlightcolor='yellow', highlightthickness=2)
password.place(x=80, y=250)


btnFrame = tk.Frame(root, highlightbackground='#14dea4', highlightthickness=3)
btnFrame.place(x=80, y=320)

button = tk.Button(btnFrame, text='Login', font=('Helvetica', 10, 'bold'), width=27, bg='#222264', fg='white', bd=5, relief=tk.FLAT, command=login)
button.pack()


signupFrame = tk.Frame(root, highlightbackground='#156069', highlightthickness=3)
signupFrame.place(x=80, y=370)

signupbtn = tk.Button(signupFrame, text="Signup", font=('Helvetica', 9), width=31, bg='#222264', fg='white', bd=3, relief=tk.FLAT, command=open_signup_window)
signupbtn.pack()


root.mainloop()
