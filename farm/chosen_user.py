from user import User

# The class is used to inform each class where it's necessary about the current user playing the game
class ChosenUser:
    user = None
    def __init__(self):
        User.append_all_users()
        ChosenUser.user = User.users[0]