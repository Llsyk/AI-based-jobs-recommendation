import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import subprocess

def continue_button_click():
    print("Continue button clicked")

root = tk.Tk()
root.title("Job Recommendation System")
root.configure(background='#e1edfd')  # Set the background color of the root window

# Set window size
window_width = 800
window_height = 500

# Calculate the position of the window to center it on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Load the image
image_path = "./background_img1.jpg"
original_image = Image.open(image_path)
tk_image = ImageTk.PhotoImage(original_image)

# Create a label with the original image
image_label = tk.Label(root, image=tk_image, bg="#ffffff")
image_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add logo
logo_image = Image.open("logo.png")  # Replace "logo.png" with your logo file path
logo_image = logo_image.resize((90, 80), Image.LANCZOS)  # Resize logo as needed
tk_logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=tk_logo, bg="#ffffff")
logo_label.place(relx=0.1, rely=0.1, anchor=tk.CENTER)

# Create a label for the topic
topic_label = tk.Label(root, text="Choose Your Career Field", font=("Helvetica", 20), bg="#ffffff")
topic_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# Create a themed frame to hold buttons with a glass-like effect
style = ttk.Style()
style.theme_use("clam")  # Use the "clam" theme for a glass-like effect
style.configure('Transparent.TFrame', background='systemTransparent')

button_frame = ttk.Frame(root, style='Transparent.TFrame')
button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Load icons
icon1 = Image.open("IT.png")  # Replace "icon1.png" with your icon file path
icon1 = icon1.resize((38, 33), Image.LANCZOS)  # Resize icon to 32x32 with high-quality
tk_icon1 = ImageTk.PhotoImage(icon1)

icon2 = Image.open("engineer.png")  # Replace "icon2.png" with your icon file path
icon2 = icon2.resize((32,32), Image.LANCZOS)  # Resize icon to 32x32 with high-quality
tk_icon2 = ImageTk.PhotoImage(icon2)

icon3 = Image.open("medical.jpg")  # Replace "icon3.png" with your icon file path
icon3 = icon3.resize((32, 32), Image.LANCZOS)  # Resize icon to 32x32 with high-quality
tk_icon3 = ImageTk.PhotoImage(icon3)

icon4 = Image.open("finance.jpg")  # Replace "icon4.png" with your icon file path
icon4 = icon4.resize((30, 32), Image.LANCZOS)  # Resize icon to 32x32 with high-quality
tk_icon4 = ImageTk.PhotoImage(icon4)

def choosePage(t):
    root.destroy()
    subprocess.call(["python", "main.py",t])

# Create buttons with icons
button1 = tk.Button(button_frame, text="Technical    ", image=tk_icon1, compound=tk.LEFT,command=lambda: choosePage('technical'))
button1.grid(row=0, column=1, padx=25, pady=20)

button2 = tk.Button(button_frame, text="Engineering  ", image=tk_icon2, compound=tk.LEFT,command=lambda: choosePage('engineer'))
button2.grid(row=0, column=2, padx=25, pady=20)

button3 = tk.Button(button_frame, text="  Medical    ", image=tk_icon3, compound=tk.LEFT,command=lambda: choosePage('medical'))
button3.grid(row=1, column=1, padx=25, pady=20)

button4 = tk.Button(button_frame, text="   Finance     ", image=tk_icon4, compound=tk.LEFT,command=lambda: choosePage('finance'))
button4.grid(row=1, column=2, padx=25, pady=20)

# Start the Tkinter event loop
root.mainloop()
