from ObjectData001_BasePlayer import *


class SwordMan(Player):
    def __init__(self, x, y):
        super(SwordMan, self).__init__(100, 100, 25, 25, 50, 50, 7, 5, 2, 5, 2, 3)
        self.image = load_image("Player001_SwordMan.png")
        self.x = x;
        self.y = y;

    def show_stat(self):
        super(SwordMan, self).show_stat(self)
