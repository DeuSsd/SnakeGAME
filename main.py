from os import system
from time import sleep

# GRASS = 0
# SNAKE = 1
# APPLE = 2
GRASS = " "
SNAKE = "O"
SNAKE_HEAD = "X"
APPLE = ""

NO_MOVE = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4


class SnakeNode:
    x: int
    y: int
    type_move: int
    count_live: int

    def __init__(self, x: int, y: int, type_move: int, count_live: int):
        self.x = x
        self.y = y
        self.type_move = type_move
        self.count_live = count_live

    # (x,y)
    def _move_up(self):
        self.count_live -= 1
        self.y -= 1

    # (x,y)
    def _move_down(self):
        self.count_live -= 1
        self.y += 1

    # (x,y)
    def _move_left(self):
        self.count_live -= 1
        self.x -= 1

    # (x,y)
    def _move_right(self):
        self.count_live -= 1
        self.x += 1

    def _no_move(self):
        self.count_live -= 1
        pass

    def _group_to_move(self,directions):
        if directions == MOVE_UP: return self._move_up
        elif directions == MOVE_DOWN: return self._move_down
        elif directions == MOVE_RIGHT: return self._move_right
        elif directions == MOVE_LEFT: return self._move_left
        elif directions == NO_MOVE: return self._no_move

    # ((x,y),counter)
    def move(self):
        self._group_to_move(self.type_move)()


class Snake:
    head_x: int
    head_y: int
    len: int
    snake_nodes: list

    def __init__(self, x: int = 0, y: int = 0, len: int = 3, ):
        self.head_x = x
        self.head_y = y
        self.len = len
        self.snake_nodes = [SnakeNode(self.head_x, self.head_y, NO_MOVE, len-1) for i in range(len)]

        # (x,y)

    def _move_up(self):
        self.head_y -= 1

        # (x,y)

    def _move_down(self):
        self.head_y += 1

        # (x,y)

    def _move_left(self):
        self.head_x -= 1

        # (x,y)

    def _move_right(self):
        self.head_x += 1

    def _no_move(self):
        pass

    def _group_to_move(self,directions):
        if directions == MOVE_UP: return self._move_up
        elif directions == MOVE_DOWN: return self._move_down
        elif directions == MOVE_RIGHT: return self._move_right
        elif directions == MOVE_LEFT: return self._move_left
        elif directions == NO_MOVE: return self._no_move

    def _count_node_coors(self):
        for node in self.snake_nodes:
            node.move()
            if node.count_live == 0:
                self.snake_nodes.remove(node)

    def move(self, direction):
        self._group_to_move(direction)()
        self._count_node_coors()
        self.snake_nodes.append(SnakeNode(type_move=direction, x=self.head_x, y=self.head_y, count_live=self.len))


    def drow_snake(self, space):
        for node in self.snake_nodes:
            space[node.y][node.x] = SNAKE


class GameWindow:
    window_width: int
    window_hight: int

    width: int
    hight: int

    # coors of centre game
    centre_x: int
    centre_y: int

    snake_object: Snake

    def __init__(self, hight: int = 20, width: int = 100):

        self.window_width = width
        self.window_hight = hight + 4

        self.width = width
        self.hight = hight

        self.centre_x = width // 2
        self.centre_y = hight // 2

        self.snake_object = Snake(x=self.centre_x, y=self.centre_y,len = 3)

        self.space = [[GRASS for field_w in range(self.width)] for field_h in range(self.hight)]
        self.snake_object.drow_snake(self.space)

        system('cls')  # TODO исправить на возврат курсора в начало экрана

    def get_move(self):
        self.snake_object.move(MOVE_UP)

    def clear_game_space(self):
        # generate clear space
        self.space = [[GRASS for field_w in range(self.width)] for field_h in range(self.hight)]

    def update_screen(self, score: int):
        self.clear_game_space()
        self.snake_object.drow_snake(self.space)
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
                        score_str_len = len(score_str) - 1
                        print(score_str, end="")
                        score_flag = False
                    else:
                        if score_str_len == 0:
                            if x > 2:
                                print(self.space[x - 2][y], end="")
                            else:
                                print(" ", end="")
                        else:
                            score_str_len -= 1
            print()


#
# class GameSpace(GameWindow):
#     # coors of centre game
#     centre_x: int
#     centre_y: int
#
#     snake_head_x: int
#     snake_head_y: int
#     len: int = 3
#     num_apple_ate: int = 0
#
#     def __init__(self, hight: int = 10, width: int = 100):
#         super(GameSpace, self).__init__(hight, width)  # generate game space
#
#         # calculate coors of centre game space
#         self.centre_x = width // 2
#         self.centre_y = hight // 2
#
#         # calculate coors of snake's head
#         self.snake_head_x = self.centre_x
#         self.snake_head_y = self.centre_y
#
#     def show_space(self):
#         for item in self.space:
#             for field in item:
#                 print(field, end="\t")
#             print()

# def clear_game_space(self):
#     # generate clear space
#     self.space = [[GRASS for field_w in range(self.width)] for field_h in range(self.hight)]


if __name__ == "__main__":
    Game = GameWindow()
    for item in range(100):
        sleep(1)
        Game.update_screen(item)
        Game.get_move()

    # Game.show_space()
