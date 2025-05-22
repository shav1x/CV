import tkinter as tk
from PIL import Image, ImageTk


class GameUI:
    def __init__(self, canvas):
        self.canvas = canvas
        self._image_refs = []

    # Create a beautiful shape of a rectangle with rounded corners at the given coordinates
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=15, **kwargs):
        fill = kwargs.get("fill", None)
        outline = kwargs.get("outline", None)
        width = kwargs.get("width", 1)

        shapes = []

        shapes.append(self.canvas.create_arc(x1, y1, x1 + radius * 2, y1 + radius * 2,
                                             start=90, extent=90, style="pieslice", fill=fill, outline=fill))
        shapes.append(self.canvas.create_arc(x2 - radius * 2, y1, x2, y1 + radius * 2,
                                             start=0, extent=90, style="pieslice", fill=fill, outline=fill))
        shapes.append(self.canvas.create_arc(x1, y2 - radius * 2, x1 + radius * 2, y2,
                                             start=180, extent=90, style="pieslice", fill=fill, outline=fill))
        shapes.append(self.canvas.create_arc(x2 - radius * 2, y2 - radius * 2, x2, y2,
                                             start=270, extent=90, style="pieslice", fill=fill, outline=fill))

        shapes.append(self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2,
                                                   fill=fill, outline=fill))

        shapes.append(self.canvas.create_rectangle(x1, y1 + radius, x1 + radius, y2 - radius,
                                                   fill=fill, outline=fill))
        shapes.append(self.canvas.create_rectangle(x2 - radius, y1 + radius, x2, y2 - radius,
                                                   fill=fill, outline=fill))

        if outline:
            shapes.append(self.canvas.create_arc(x1, y1, x1 + radius * 2, y1 + radius * 2,
                                                 start=90, extent=90, style="arc", outline=outline, width=width))
            shapes.append(self.canvas.create_arc(x2 - radius * 2, y1, x2, y1 + radius * 2,
                                                 start=0, extent=90, style="arc", outline=outline, width=width))
            shapes.append(self.canvas.create_arc(x1, y2 - radius * 2, x1 + radius * 2, y2,
                                                 start=180, extent=90, style="arc", outline=outline, width=width))
            shapes.append(self.canvas.create_arc(x2 - radius * 2, y2 - radius * 2, x2, y2,
                                                 start=270, extent=90, style="arc", outline=outline, width=width))

            shapes.append(self.canvas.create_line(x1 + radius, y1, x2 - radius, y1, fill=outline, width=width))  # Top
            shapes.append(self.canvas.create_line(x1 + radius, y2, x2 - radius, y2, fill=outline, width=width))  # Bottom
            shapes.append(self.canvas.create_line(x1, y1 + radius, x1, y2 - radius, fill=outline, width=width))  # Left
            shapes.append(self.canvas.create_line(x2, y1 + radius, x2, y2 - radius, fill=outline, width=width))  # Right

        return shapes

    # Adds details to the rectangle and/or gives it animations or makes a button out of it
    def add_gui_rectangle_element(self, x, y, width, height, text, image_path, color_in, color_out, onclick=None):
        tag_name = f"button_{len(self._image_refs)}"

        shape_ids = self.create_rounded_rectangle(x, y, x + width, y + height, fill=color_in, outline=color_out, width=5)

        if image_path != "":
            image_size = height - 10
            image = Image.open(image_path).resize((image_size, image_size), Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(image)
            self._image_refs.append(photo_image)
            image_id = self.canvas.create_image(x + 15, y + 5, anchor=tk.NW, image=photo_image)

            text_id = self.canvas.create_text(
                x + width - 10, y + height // 2,
                text=text, anchor="e", font=("Galvji", 20, "bold"), fill="black"
            )

        else:
            self._image_refs.append(None)
            text_id = self.canvas.create_text(
                x + width // 2, y + height // 2,
                text=text, anchor="center", font=("Galvji", 30, "bold"), fill="black"
            )

        for shape_id in shape_ids:
            self.canvas.addtag_withtag(tag_name, shape_id)
        if image_path != "":
            self.canvas.addtag_withtag(tag_name, image_id)
        self.canvas.addtag_withtag(tag_name, text_id)

        if onclick:
            self.canvas.tag_bind(tag_name, "<Button-1>", onclick)
            self._add_hover_effect(tag_name, x, y, width, height)

        return text_id

    # Adds an animation and plays a sound if it is toggled in the options
    def _add_hover_effect(self, tag_name, x, y, width, height):

        import pygame
        pygame.mixer.init()

        hover_sound = pygame.mixer.Sound("assets/click.wav")
        is_hovering = False

        original_bbox = self.canvas.bbox(tag_name)

        def on_enter(event):
            nonlocal is_hovering
            if not is_hovering:
                is_hovering = True

                from options import Options
                hover_sound.play() if Options.game_sound_toggle else None

            scale_factor = 1.1
            x_min, y_min, x_max, y_max = self.canvas.bbox(tag_name)
            original_width = x_max - x_min
            original_height = y_max - y_min
            center_x = x_min + original_width / 2
            center_y = y_min + original_height / 2

            self.canvas.scale(tag_name, center_x, center_y, scale_factor, scale_factor)

        def on_leave(event):
            mouse_x, mouse_y = event.x, event.y
            x_min, y_min, x_max, y_max = self.canvas.bbox(tag_name)

            if not x_min <= mouse_x <= x_max or not y_min <= mouse_y <= y_max:
                nonlocal is_hovering
                is_hovering = False

            x_min, y_min, x_max, y_max = original_bbox
            original_width = x_max - x_min
            original_height = y_max - y_min
            center_x = x_min + original_width / 2
            center_y = y_min + original_height / 2

            scale_factor = 1.1
            self.canvas.scale(tag_name, center_x, center_y, 1 / scale_factor, 1 / scale_factor)

        self.canvas.tag_bind(tag_name, "<Enter>", on_enter)
        self.canvas.tag_bind(tag_name, "<Leave>", on_leave)

    # Find the appropriate element (to be able to destroy or update it)
    def find_element_by_text(self, text):
        for item in self.canvas.find_all():
            if self.canvas.type(item) == "text" and self.canvas.itemcget(item, "text") == text:
                return item
        return None

