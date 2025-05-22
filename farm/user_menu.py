import os
import tkinter as tk
from tkinter import font

from PIL import Image, ImageTk

from chosen_user import ChosenUser
from game_ui import GameUI
from user import User

class UserMenu:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("User selection")
        self.window.geometry("1536x1024")
        self.init_background()
        self.game_ui = GameUI(self.canvas)
        self.create_user_buttons()
        self.create_text_field(695, 630, 17, 1)
        self.game_ui.add_gui_rectangle_element(
            x=200, y=670, width=320, height=80,
            text=f"Delete chosen user", image_path="",
            color_in="tomato",
            color_out="wheat",
            onclick=self.delete_user
        )
        self.game_ui.add_gui_rectangle_element(
            x=780, y=700, width=270, height=80,
            text=f"Create new user", image_path="",
            color_in="orange",
            color_out="yellow",
            onclick=self.create_user
        )
        self.game_ui.add_gui_rectangle_element(
            x=1350, y=750, width=130, height=80,
            text=f"Close", image_path="",
            color_in="red",
            color_out="yellow",
            onclick=self.close_menu
        )
        self.window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.window.destroy()
        )
        self.window.mainloop()

    # Initialize the background
    def init_background(self):
        bckgrnd_path = "assets/user_menu_background.png"
        if not os.path.exists(bckgrnd_path):
            raise FileNotFoundError(f"Background image '{bckgrnd_path}' not found.")

        bg_image = Image.open(bckgrnd_path)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.window, width=bg_image.width, height=bg_image.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

    # Creates a text field, where the new user's nickname will be written
    def create_text_field(self, x, y, width, height):
        self.text_field = tk.Text(
            self.window,
            font=("Georgia", 40),
            wrap="word",
            width=width,
            height=height,
            bg="lightyellow",
            fg="black",
            borderwidth=2,
            relief="sunken"
        )
        self.text_field.place(x=x, y=y)

    # Get the nickname, written in the textfield
    def get_textfield_content(self):
        return self.text_field.get("1.0", tk.END).strip()

    # Creates the buttons (represented by usernames)
    def create_user_buttons(self):

        x = 150
        y = 20

        for user in User.users:
            btn = self.game_ui.add_gui_rectangle_element(
                x=x, y=y, width=260, height=80,
                text=user.username, image_path="",
                color_in="green" if user.username == ChosenUser.user.username else "sienna",
                color_out="wheat",
                onclick=self.create_user_button_callback(user)
            )

            y += 100

    # Handles choosing the user event
    def choose_the_user(self, user, event=None):
        ChosenUser.user = user
        self.create_user_buttons()

    # Handles deleting the user event
    def delete_user(self, event=None):
        username_to_delete = ChosenUser.user.username
        for us in User.users:
            if us.username == username_to_delete:
                User.users.remove(us)
                break
        else:
            return
        User.delete_user(username_to_delete)
        ChosenUser.user = User.users[0] if User.users else None
        self.window.destroy()
        UserMenu(self.window.master)

    # Handles creating the user event
    def create_user(self, event=None):
        if len(User.users) == 4:
            self.text_field.delete("1.0", tk.END)
            self.text_field.insert(tk.END, "! Max users !")
            return

        nickname = self.get_textfield_content()

        if nickname.strip() == "":
            return

        new_user = User(nickname)
        User.write_into_db(new_user)
        ChosenUser.user = new_user
        self.text_field.delete("1.0", tk.END)
        self.create_user_buttons()

    # Chooses the newly created user
    def create_user_button_callback(self, user):
        return lambda event=None: self.choose_the_user(user)

    # Handles closing the window event
    def close_menu(self, event=None):
        self.window.destroy()

        parent = self.window.master
        if isinstance(parent, tk.Tk):
            parent.deiconify()

