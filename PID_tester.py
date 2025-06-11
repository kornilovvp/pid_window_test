import tkinter as tk

class MovableCirclesApp:
    def __init__(self, master):
        self.master = master
        master.title("Movable Circles")

        # Window dimensions
        self.window_width = 1024
        self.window_height = 768
        master.geometry(f"{self.window_width}x{self.window_height}")
        master.resizable(False, False) # Fixed window size

        # Working area (Canvas) dimensions
        self.canvas_width = 900
        self.canvas_height = 600
        self.canvas_bg = "white"

        # StringVars for coordinate labels
        self.green_coord_var = tk.StringVar()
        self.blue_coord_var = tk.StringVar()

        # Create and place coordinate labels at the top of the main window
        green_label = tk.Label(master, textvariable=self.green_coord_var, font=("Arial", 10))
        green_label.place(x=10, y=10) # Position near top-left

        blue_label = tk.Label(master, textvariable=self.blue_coord_var, font=("Arial", 10))
        blue_label.place(x=10, y=35)  # Position below the green label

        # Calculate padding for centering the canvas
        self.pad_x = (self.window_width - self.canvas_width) // 2
        self.pad_y = (self.window_height - self.canvas_height) // 2

        self.canvas = tk.Canvas(
            master,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.canvas_bg,
            highlightthickness=0  # Remove canvas border
        )
        self.canvas.place(x=self.pad_x, y=self.pad_y)

        # Circle properties
        self.circle_radius = 20
        self.green_color = "green"
        self.blue_color = "blue"

        # Create green circle (center of working area)
        gc_center_x = self.canvas_width / 2
        gc_center_y = self.canvas_height / 2
        self.green_circle = self.canvas.create_oval(
            gc_center_x - self.circle_radius, gc_center_y - self.circle_radius,
            gc_center_x + self.circle_radius, gc_center_y + self.circle_radius,
            fill=self.green_color, outline=self.green_color, tags="green_circle"
        )

        # Create blue circle (bottom-center of working area)
        # Its bottom edge will be at the bottom of the canvas.
        bc_center_x = self.canvas_width / 2
        # Center Y such that its bottom edge is at canvas_height
        bc_center_y = self.canvas_height - self.circle_radius
        self.blue_circle = self.canvas.create_oval(
            bc_center_x - self.circle_radius, bc_center_y - self.circle_radius,
            bc_center_x + self.circle_radius, bc_center_y + self.circle_radius,
            fill=self.blue_color, outline=self.blue_color, tags="blue_circle"
        )

        # Drag and drop state for green circle
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # Bind mouse events for the green circle
        self.canvas.tag_bind(self.green_circle, "<ButtonPress-1>", self._on_green_press)
        self.canvas.tag_bind(self.green_circle, "<B1-Motion>", self._on_green_drag)
        self.canvas.tag_bind(self.green_circle, "<ButtonRelease-1>", self._on_green_release)

        # Initialize coordinate display
        self._update_coordinate_labels()

    def _get_circle_center_coords(self, circle_id):
        """
        Calculates the center coordinates of a circle item on the canvas.
        Returns coordinates as integers, relative to the canvas.
        """
        coords = self.canvas.coords(circle_id) # (x1, y1, x2, y2)
        center_x = (coords[0] + coords[2]) / 2
        center_y = (coords[1] + coords[3]) / 2
        return int(center_x), int(center_y)

    def _update_coordinate_labels(self):
        """Updates the text of the coordinate labels."""
        gx, gy = self._get_circle_center_coords(self.green_circle)
        bx, by = self._get_circle_center_coords(self.blue_circle)
        self.green_coord_var.set(f"Green: X={gx}  Y={gy}")
        self.blue_coord_var.set(f"Blue:  X={bx}  Y={by}")

    def _on_green_press(self, event):
        """Handles mouse button press on the green circle."""
        # Find the item clicked; ensure it's the green circle
        item = self.canvas.find_closest(event.x, event.y)[0]
        if item == self.green_circle:
            self._drag_data["item"] = item
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
        else:
            self._drag_data["item"] = None

    def _on_green_drag(self, event):
        """Handles mouse drag event for the green circle."""
        if self._drag_data["item"] == self.green_circle:
            # Calculate the distance to move
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]

            # Get current coordinates of the green circle's bounding box
            x1, y1, x2, y2 = self.canvas.coords(self._drag_data["item"])

            # Calculate potential new top-left and bottom-right coordinates
            new_x1, new_y1 = x1 + dx, y1 + dy
            new_x2, new_y2 = x2 + dx, y2 + dy

            # Boundary checks: Adjust dx, dy to keep the circle within the canvas
            if new_x1 < 0:
                dx = -x1  # Adjust dx to align left edge with canvas left
            if new_x2 > self.canvas_width:
                dx = self.canvas_width - x2  # Adjust dx to align right edge

            if new_y1 < 0:
                dy = -y1  # Adjust dy to align top edge
            if new_y2 > self.canvas_height:
                dy = self.canvas_height - y2  # Adjust dy to align bottom edge

            # Move the circle by the (potentially adjusted) dx, dy
            self.canvas.move(self._drag_data["item"], dx, dy)

            # Update the last mouse position for the next drag event
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

            # Update coordinate display
            self._update_coordinate_labels()

    def _on_green_release(self, event):
        """Handles mouse button release."""
        # Reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = MovableCirclesApp(root)
    root.mainloop()