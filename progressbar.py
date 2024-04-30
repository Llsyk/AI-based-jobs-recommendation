import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import subprocess
import time


def continue_button_click():
    # Destroy the continue button
    continue_button.destroy()
    
    # Display the progress bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate", style="Custom.Horizontal.TProgressbar")
    progress_bar.pack(pady=20)
    progress_bar.start(10)  # Start the progress animation
    
    # Transition to the next page after a delay (simulating a process)
    root.after(3000, transition_to_input)


def transition_to_input():
    # Run input.py using subprocess
    subprocess.Popen(["python", "page2.py"])

    # Close the current window
    root.destroy()


# Function to display typewriter text animation
def display_typewriter_text(label, text, delay=0.05):
    if text:
        label.config(text=label.cget("text") + text[0])
        label.after(int(delay * 1000), display_typewriter_text, label, text[1:], delay)

    
# Function to change button color on hover
def on_enter(e):
    continue_button.configure(style='Hover.TButton')


def on_leave(e):
    continue_button.configure(style='TButton')


# Create a Tkinter window
root = tk.Tk()
root.title("Job Recommendation System")
root.configure(background='white')  # Set the background color of the root window

# Set window size
window_width = 800
window_height = 600

# Calculate the position of the window to center it on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


# Create a frame to hold the title and typewriter text
title_frame = tk.Frame(root, bg="white")
title_frame.pack(pady=10)

# Create a label for the title
title_label = tk.Label(title_frame, text="Welcome to JobJunction", font=("Helvetica", 16), bg="white")
title_label.pack()

# Create a label for typewriter text animation
typewriter_label = tk.Label(root, text="", font=("Helvetica", 12), bg="white")
typewriter_label.pack()

# Start typewriter text animation
display_typewriter_text(typewriter_label, "Welcome to our system")

# Create a frame to hold the image and button
frame = tk.Frame(root, bg="white")
frame.pack()

# Load the image
image_path = "./background_img1.jpg"  # Specify the path to your image file
image = Image.open(image_path)
tk_image = ImageTk.PhotoImage(image)

# Create a label with the image
image_label = tk.Label(frame, image=tk_image, bg="white")
image_label.pack()

# Load the logo image
# logo_path = "./logo.png"  # Specify the path to your logo file
# logo_image = Image.open(logo_path)

# # Resize the logo image
# logo_image = logo_image.resize((90, 80), Image.LANCZOS)

# # Convert the logo image to Tkinter PhotoImage
# tk_logo = ImageTk.PhotoImage(logo_image)
logo_image = Image.open("logo.png")  # Replace "logo.png" with your logo file path
logo_image = logo_image.resize((90, 80), Image.LANCZOS)  # Resize logo as needed
tk_logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=tk_logo, bg="#ffffff")
logo_label.place(relx=0.1, rely=0.1, anchor=tk.CENTER)

# Create a label with the logo
# logo_label = tk.Label(root, image=tk_logo, bg="white")
# logo_label.pack(side="top", anchor="ne", pady=10, padx=10)  # Place the logo label at the top-right corner with padding

# Create a frame to hold the button
frame = tk.Frame(root, bg="white")
frame.pack()

# Create a custom style for the button with rounded corners and hover effect
style = ttk.Style()
style.configure('TButton', background='orange', foreground='white', borderwidth=0, relief=tk.FLAT, font=('Helvetica', 12))
style.map('TButton',  background='orange', foreground='white')
style.configure('Hover.TButton', background='orange', foreground='white')

# Create a custom style for the themed progress bar
style.theme_use('clam')
style.configure("Custom.Horizontal.TProgressbar", background='sky blue', troughcolor='light blue', thickness=20, borderwidth=0, relief=tk.FLAT)

# Create the "Continue" button with icon
continue_button = tk.Button(frame, text="Continue", command=continue_button_click,  bg="orange", fg="white", font=("TkDefaultFont", 12, "bold"))
# To prevent image garbage collection
continue_button.pack(pady=10)

# Bind events for hover effect
continue_button.bind("<Enter>", on_enter)
continue_button.bind("<Leave>", on_leave)

# Start the Tkinter event loop
root.mainloop()
