import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import ImageGrab, Image

class WhiteboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard App")
        self.root.geometry("800x600")

        self.is_drawing = False
        self.prev_x = None
        self.prev_y = None
        self.drawing_color = "blue"
        self.line_width = 2
        self.eraser_mode = False
        self.text_items = {}
        self.drag_data = {"item": None}

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        controls = tk.Frame(self.root)
        controls.pack(side="top", fill="x")

        tk.Button(controls, text="Color", command=self.change_color).pack(side="left")
        tk.Button(controls, text="Eraser", command=self.toggle_eraser).pack(side="left")
        tk.Button(controls, text="Clear", command=lambda: self.canvas.delete("all")).pack(side="left")
        tk.Button(controls, text="Add Text", command=self.add_text).pack(side="left")
        tk.Button(controls, text="Save", command=self.save_canvas).pack(side="left")

        tk.Label(controls, text="Width").pack(side="left", padx=5)
        width_slider = tk.Scale(controls, from_=1, to=10, orient="horizontal", command=self.set_line_width)
        width_slider.set(self.line_width)
        width_slider.pack(side="left")

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def set_line_width(self, val):
        self.line_width = int(val)

    def change_color(self):
        color = askcolor()[1]
        if color:
            self.drawing_color = color
            self.eraser_mode = False

    def toggle_eraser(self):
        self.eraser_mode = True
        self.drawing_color = "white"

    def start_drawing(self, event):
        # If clicked on text, prepare for dragging
        item = self.canvas.find_closest(event.x, event.y)
        if item and item[0] in self.text_items:
            self.drag_data["item"] = item[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
        else:
            self.is_drawing = True
            self.prev_x, self.prev_y = event.x, event.y

    def draw(self, event):
        if self.drag_data["item"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.canvas.move(self.drag_data["item"], dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
        elif self.is_drawing:
            self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y,
                                    fill=self.drawing_color, width=self.line_width,
                                    capstyle=tk.ROUND, smooth=True)
            self.prev_x, self.prev_y = event.x, event.y

    def stop_drawing(self, event):
        self.is_drawing = False
        self.drag_data["item"] = None

    def add_text(self):
        def place_text():
            text = entry.get()
            x, y = int(x_entry.get()), int(y_entry.get())
            if text:
                text_id = self.canvas.create_text(x, y, text=text, font=("Arial", 14), fill=self.drawing_color, anchor="nw")
                self.text_items[text_id] = text
            popup.destroy()

        popup = tk.Toplevel()
        popup.title("Add Text")

        tk.Label(popup, text="Text:").grid(row=0, column=0)
        entry = tk.Entry(popup)
        entry.grid(row=0, column=1)

        tk.Label(popup, text="X:").grid(row=1, column=0)
        x_entry = tk.Entry(popup, width=5)
        x_entry.insert(0, "50")
        x_entry.grid(row=1, column=1)

        tk.Label(popup, text="Y:").grid(row=2, column=0)
        y_entry = tk.Entry(popup, width=5)
        y_entry.insert(0, "50")
        y_entry.grid(row=2, column=1)

        tk.Button(popup, text="Add", command=place_text).grid(row=3, columnspan=2, pady=5)

    def save_canvas(self):
        self.root.update()
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        
        self.root.after(100, lambda: self.capture_and_export((x, y, x1, y1)))

    def capture_and_export(self, bbox):
        image = ImageGrab.grab(bbox)
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("PDF Document", "*.pdf")
        ])
        if file_path:
            ext = file_path.split('.')[-1].lower()
            if ext == "pdf":
                image.convert("RGB").save(file_path, "PDF")
            elif ext == "jpg":
                image.convert("RGB").save(file_path, "JPEG")
            else:
                image.save(file_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = WhiteboardApp(root)
    root.mainloop()
