from os import system
from time import sleep
from pynput import keyboard
from random import random

# GRASS = 0
# SNAKE = 1
# APPLE = 2


GRASS = " "
SNAKE = "O"
SNAKE_HEAD = "P"
APPLE = "X"

NO_MOVE = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

SNAKE_BODY_EAT_CHECK = False
DIRECTION = NO_MOVE
APPLE_EXIST = False
SNAKE_ALIVE = True

RESPAWN = True
START = True
EXIT = False

SCORE = 0
SPEED = 0.2


class SnakeNode:
    x: int
    y: int
    count_live: int

    def __init__(self, x: int, y: int, count_live: int):
        self.x = x
        self.y = y
        self.count_live = count_live - 1

    # ((x,y),counter)
    def life_time_down(self):
        self.count_live -= 1


class Snake:
    head_x: int
    head_y: int
    len: int
    snake_nodes: list

    def __init__(self, x: int = 0, y: int = 0, len: int = 3):
        self.head_x = x
        self.head_y = y
        self.len = len
        self.snake_nodes = [SnakeNode(self.head_x, self.head_y, self.len) for i in range(self.len)]

    def __iter__(self):
        return self.snake_nodes.__iter__()

    def __index__(self, index):
        return self.snake_nodes[index]

    def __getitem__(self, item):
        return self.snake_nodes[item]

    def _move_up(self):
        self.head_y -= 1

    def _move_down(self):
        self.head_y += 1

    def _move_left(self):
        self.head_x -= 1

    def _move_right(self):
        self.head_x += 1

    def _no_move(self):
        global SNAKE_BODY_EAT_CHECK
        SNAKE_BODY_EAT_CHECK = False

    def _group_to_move_head(self, directions):
        if directions == MOVE_UP:
            return self._move_up
        elif directions == MOVE_DOWN:
            return self._move_down
        elif directions == MOVE_RIGHT:
            return self._move_right
        elif directions == MOVE_LEFT:
            return self._move_left
        elif directions == NO_MOVE:
            return self._no_move

    def _count_node_life(self):
        index_delete = 0
        for node in self.snake_nodes:
            node.life_time_down()
            if node.count_live == 0:
                self.snake_nodes.index(node)
            elif node.count_live == self.len:
                continue
        self.snake_nodes.pop(index_delete)

    def move(self, direction):
        global SNAKE_BODY_EAT_CHECK
        if not SNAKE_BODY_EAT_CHECK:
            SNAKE_BODY_EAT_CHECK = True
        self._group_to_move_head(direction)()
        head = SnakeNode(x=self.head_x, y=self.head_y, count_live=self.len)
        self.check_eat_body_of_snake()
        self._count_node_life()
        self.snake_nodes.append(head)

    def check_eat_body_of_snake(self):
        global SNAKE_ALIVE, SNAKE_BODY_EAT_CHECK
        if SNAKE_BODY_EAT_CHECK:
            for node in self[:-1]:
                if self.head_x == node.x and self.head_y == node.y:
                    SNAKE_ALIVE = False
                    raise IndexError

    def drow_snake(self, space):
        for node in self.snake_nodes:
            space[node.y][node.x] = SNAKE

    def check_eat_apple(self, aplle_x: int, apple_y: int):
        global APPLE_EXIST, SCORE
        if self.head_x == aplle_x and self.head_y == apple_y:
            APPLE_EXIST = False
            self.len += 1
            SCORE += 1
            head = SnakeNode(x=self.head_x, y=self.head_y, count_live=self.len)
            self.snake_nodes.append(head)

    def get_head_coors(self):
        return self.head_x, self.head_y


class Apple:
    apple_x: int
    apple_y: int

    x_range: int
    y_range: int

    def __init__(self, x_range: int, y_range: int):
        self.x_range = x_range
        self.y_range = y_range
        self.generate_apple()

    def generate_apple(self):
        global APPLE_EXIST
        if not APPLE_EXIST:
            self.apple_x = int(self.x_range * random())
            self.apple_y = int(self.y_range * random())
            APPLE_EXIST = True

    def drow_apple(self, space):
        space[self.apple_y][self.apple_x] = APPLE

    def get_coors(self):
        return self.apple_x, self.apple_y


class GameWindow:
    window_width: int
    window_hight: int

    width: int
    hight: int

    space: list

    # coors of centre game
    centre_x: int
    centre_y: int

    snake_object: Snake
    apple_object: Apple

    def __init__(self, hight: int = 20, width: int = 100):

        self.window_width = width
        self.window_hight = hight

        self.width = width - 2
        self.hight = hight - 4

        self.centre_x = int(self.width / 2)
        self.centre_y = int(self.hight / 2)

        self.snake_object = Snake(x=self.centre_x, y=self.centre_y, len=3)
        self.apple_object = Apple(self.width, self.hight)

        self.update_screen(SCORE)

        # system('cls')  # TODO исправить на возврат курсора в начало экрана

    def restart(self):
        global SCORE, SNAKE_BODY_EAT_CHECK, DIRECTION, APPLE_EXIST, SNAKE_ALIVE
        SNAKE_BODY_EAT_CHECK = False
        DIRECTION = NO_MOVE
        APPLE_EXIST = False
        SNAKE_ALIVE = True
        SCORE = 0

        self.snake_object = Snake(x=self.centre_x, y=self.centre_y, len=3)
        self.apple_object = Apple(self.width, self.hight)

        self.update_screen(SCORE)


    def get_move(self, direction):
        self.snake_object.move(direction)

    def check_eat_apple(self):
        self.snake_object.check_eat_apple(*self.apple_object.get_coors())

    def generate_apple(self):
        self.apple_object.generate_apple()

    def clear_game_space(self):
        # generate clear space
        self.space = [[GRASS for field_w in range(self.width)] for field_h in range(self.hight)]

    def check_borders(self):
        global SNAKE_ALIVE
        head_x, head_y = self.snake_object.get_head_coors()
        if (head_x >= self.width or head_x <= 0) or (head_y >= self.hight or head_y <= 0):
            SNAKE_ALIVE = False
            print("bye")
            raise IndexError

    def update_screen(self, score: int):
        self.clear_game_space()
        self.apple_object.drow_apple(self.space)
        self.snake_object.drow_snake(self.space)

        score_str_len = 0
        score_flag = True

        system('cls')  # TODO исправить на возврат курсора в начало экрана
        for y in range(self.window_hight):
            for x in range(self.window_width):
                if y == 0 or y == self.window_hight - 1 or y == 2:
                    print("-", end="")
                elif x == 0 or x == self.window_width - 1:
                    print("|", end="")
                else:
                    if y == 1 and score_flag:
                        score_str = "Score: {}".format(score)
                        score_str_len = len(score_str) - 1
                        print(score_str, end="")
                        score_flag = False
                    else:
                        if score_str_len == 0:
                            if y > 2:
                                print(self.space[y - 3][x - 1], end="")
                            else:
                                print(" ", end="")
                        else:
                            score_str_len -= 1
            print()


class Game(GameWindow):
    def __init__(self, hight: int = 20, width: int = 100):
        super(Game, self).__init__(hight, width)  # generate game space

    def start(self):
        listener = keyboard.Listener(
            on_press=self.on_press)
        listener.start()

    def on_press(self, key):
        # print(key)
        global DIRECTION
        DIRECTION = self._group_to_direct_head(key)
        if key == keyboard.Key.esc:
            # Stop listener
            return False

    def _group_to_direct_head(self, key):
        if key == keyboard.Key.up and DIRECTION != MOVE_DOWN:
            return MOVE_UP
        elif key == keyboard.Key.down and DIRECTION != MOVE_UP:
            return MOVE_DOWN
        elif key == keyboard.Key.right and DIRECTION != MOVE_LEFT:
            return MOVE_RIGHT
        elif key == keyboard.Key.left and DIRECTION != MOVE_RIGHT:
            return MOVE_LEFT
        else:
            return DIRECTION

    def _on_press_start_menu(self, key):
        global START, EXIT
        if key == keyboard.Key.up:
            start_str = "   [Start] "
            exit_str = "    Exit "
            START = True
            EXIT = False
            self.draw_menu(start_str, exit_str)
        elif key == keyboard.Key.down:
            start_str = "    Start "
            exit_str = "   [Exit ]"
            START = False
            EXIT = True
            self.draw_menu(start_str, exit_str)
        elif key == keyboard.Key.enter:
            return False

    def _on_press_respawn_menu(self, key):
        global RESPAWN, EXIT
        if key == keyboard.Key.up:
            restart_str = "  [Restart] "
            exit_str = "   Exit "
            RESPAWN = True
            EXIT = False
            self.draw_respawn_menu(restart_str, exit_str)
        elif key == keyboard.Key.down:
            restart_str = "   Restart "
            exit_str = "  [Exit   ]"
            RESPAWN = False
            EXIT = True
            self.draw_respawn_menu(restart_str, exit_str)
        elif key == keyboard.Key.enter:
            return False

    def menu(self):
        start_str = "   [Start] "
        exit_str = "    Exit "
        self.draw_menu(start_str, exit_str)
        with keyboard.Listener(on_press=self._on_press_start_menu) as listener:
            listener.join()

    def respawn(self):
        restart_str = "  [Restart] "
        exit_str = "    Exit "
        self.draw_respawn_menu(restart_str, exit_str)
        with keyboard.Listener(on_press=self._on_press_respawn_menu) as listener:
            listener.join()

    def draw_respawn_menu(
            self,
            start_str="   [Start] ",
            exit_str="    Exit "):
        system('cls')  # TODO исправить на возврат курсора в начало экрана
        menu_y0 = self.centre_y - 3
        menu_x0 = self.centre_x - 8
        score_str = "   Score: {}".format(SCORE)
        restart_str_len = len(start_str)
        exit_str_len = len(exit_str)
        score_str_len = len(score_str)
        for y in range(self.window_hight):
            x_menu = 0
            for x in range(self.window_width):
                if y == 0 or y == self.window_hight - 1:
                    print("-", end="")
                elif x == 0 or x == self.window_width - 1:
                    print("|", end="")
                else:
                    if (y >= menu_y0 and y <= (menu_y0 + 4)) and (x == menu_x0 or x == menu_x0 + 15):
                        print("|", end="")
                    elif (y == menu_y0 or y == (menu_y0 + 4)) and (x > menu_x0 and x < menu_x0 + 15):
                        print("-", end="")
                    elif (x > menu_x0 and x < menu_x0 + 15) and y == menu_y0 + 1 and score_str_len > 0:
                        print(score_str[x_menu], end="")
                        x_menu += 1
                        score_str_len -= 1
                    elif (x > menu_x0 and x < menu_x0 + 15) and y == menu_y0 + 2 and restart_str_len > 0:
                        print(start_str[x_menu], end="")
                        x_menu += 1
                        restart_str_len -= 1
                    elif (x > menu_x0 and x < menu_x0 + 15) and y == menu_y0 + 3 and exit_str_len > 0:
                        print(exit_str[x_menu], end="")
                        x_menu += 1
                        exit_str_len -= 1
                    else:
                        print(" ", end="")
                    # else:
                    #     print(" ", end="")

            print()

    def draw_menu(
            self,
            start_str="   [Start] ",
            exit_str="    Exit "):
        system('cls')  # TODO исправить на возврат курсора в начало экрана
        menu_y0 = self.centre_y - 3
        menu_x0 = self.centre_x - 8

        start_str_len = len(start_str)
        exit_str_len = len(exit_str)
        for y in range(self.window_hight):
            x_menu = 0
            for x in range(self.window_width):
                if y == 0 or y == self.window_hight - 1:
                    print("-", end="")
                elif x == 0 or x == self.window_width - 1:
                    print("|", end="")
                else:
                    if (y >= menu_y0 and y <= (menu_y0 + 4)) and (x == menu_x0 or x == menu_x0 + 15):
                        print("|", end="")
                    elif (y == menu_y0 or y == (menu_y0 + 4)) and (x > menu_x0 and x < menu_x0 + 15):
                        print("-", end="")
                    elif (x > menu_x0 and x < menu_x0 + 15) and y == menu_y0 + 1 and start_str_len > 0:
                        print(start_str[x_menu], end="")
                        x_menu += 1
                        start_str_len -= 1
                    elif (x > menu_x0 and x < menu_x0 + 15) and y == menu_y0 + 3 and exit_str_len > 0:
                        print(exit_str[x_menu], end="")
                        x_menu += 1
                        exit_str_len -= 1
                    else:
                        print(" ", end="")
                    # else:
                    #     print(" ", end="")

            print()


if __name__ == "__main__":
    game = Game(20, 40)
    game.menu()

    if EXIT:
        exit()
    if START:
        while RESPAWN:
            game.start()
            try:
                while SNAKE_ALIVE:
                    game.check_borders()
                    game.generate_apple()
                    game.get_move(DIRECTION)
                    game.check_eat_apple()
                    game.update_screen(SCORE)
                    sleep(SPEED)
            except IndexError:
                game.respawn()
                game.restart()
                # print("You Died!\nYou Score: {0}".format(SCORE))
