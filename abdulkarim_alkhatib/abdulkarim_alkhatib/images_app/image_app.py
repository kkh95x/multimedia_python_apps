import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.load_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        self.load_button.pack(pady=10)
        self.zoom_in_button = tk.Button(self.root, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.zoom_out_button = tk.Button(self.root, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.zoom_factor = 1.0

   
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if file_path:
            self.original_image = Image.open(file_path)

            self.display_image()

    def display_image(self):
        resized_image = self.original_image.resize(
            (int(self.original_image.width * self.zoom_factor), int(self.original_image.height * self.zoom_factor)))
        photo = ImageTk.PhotoImage(resized_image)

        self.image_label.config(image=photo)
        self.image_label.image = photo

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.display_image()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.display_image()


root = tk.Tk()
app = ImageViewerApp(root)
root.mainloop()
