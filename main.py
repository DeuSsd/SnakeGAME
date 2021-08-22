
class game_space:
    def __init__(self,hight = 10,width = 10):
        self.width = width
        self.hight = hight

        # generate clear space
        self.space = [[0 for field_w in range(self.width)] for field_h in range(self.hight)]




    def show_space(self):
        for item in self.space:
            for field in item:
                print(field,end="\t")
            print()


    def clear_game_space(self):
        # generate clear space
        self.space = [[0 for field_w in range(self.width)] for field_h in range(self.hight)]


class game_window:
    def __init__(self):
        pass


if __name__ == "__main__":
    Game = game_space()
    Game.show_space()