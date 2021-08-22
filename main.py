from os import system
from time import sleep


class game_space:
    def __init__(self, hight=10, width=10):
        self.width = width
        self.hight = hight

        # generate clear space
        self.space = [[0 for field_w in range(self.width)] for field_h in range(self.hight)]

    def show_space(self):
        for item in self.space:
            for field in item:
                print(field, end="\t")
            print()

    def clear_game_space(self):
        # generate clear space
        self.space = [[0 for field_w in range(self.width)] for field_h in range(self.hight)]


class game_window:
    def __init__(self, hight=10, width=100):
        self.width = width
        self.hight = hight + 4

        # show borders
        for x in range(self.hight):
            for y in range(self.width):
                if x == 0 or x == self.hight - 1:
                    print("-", end="")
                elif y == 0 or y == self.width - 1:
                    print("|", end="")
                else:
                    print(" ", end="")
            print()
        system('cls')  # TODO исправить на возврат курсора в начало экрана

    def update_screen(self, score):
        score_str_len = 0
        score_flag = True
        system('cls')  # TODO исправить на возврат курсора в начало экрана
        for x in range(self.hight):
            for y in range(self.width):
                if x == 0 or x == self.hight - 1 or x == 2:
                    print("-", end="")
                elif y == 0 or y == self.width - 1:
                    print("|", end="")
                else:

                    if y == 2 and score_flag:
                        score_str = "Score: {}".format(score)
                        score_str_len = len(score_str)-1
                        print(score_str, end="")
                        score_flag = False
                    else:
                        if score_str_len == 0:
                            print(" ", end="")
                        else:
                            score_str_len -= 1
            print()


if __name__ == "__main__":
    Game = game_window()
    for item in range(100):
        sleep(1)
        Game.update_screen(item)

    # Game.show_space()
