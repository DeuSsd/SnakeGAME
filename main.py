from os import system
from time import sleep
from pynput import keyboard
from random import random

GRASS = " "  # Sample of grass
SNAKE = "O"  # Sample of snake's body
SNAKE_HEAD = "P"  # Sample of snake's head (not need)
APPLE = "X"  # Sample of apples

NO_MOVE = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4
DIRECTION = NO_MOVE  # Kind vector of direction

SNAKE_ALIVE = True  # Flag means that snake steel alive
APPLE_EXIST = False  # Flag means that apple steel exist and snake didn't eat it
SNAKE_BODY_EAT_CHECK = False  # Flag means that snake didn't eat own body
RESPAWN = True  # Flag means that game will be restarted
START = True  # Flag means that game will be started
EXIT = False  # Flag means that exit from game

SCORE = 0  # Game score
SPEED = 0.2  # Snakes speed


class SnakeNode:
    '''
    Class SnakeNode for create every node of snake's body.
    x,y - node coordinators
    count_live - countdown of live instance node
    '''
    x: int
    y: int
    count_live: int

    def __init__(self, x: int, y: int, count_live: int):
        self.x = x
        self.y = y
        self.count_live = count_live - 1

    def life_time_down(self):
        '''
        Node life countdown
        :return: None
        '''
        self.count_live -= 1


class Snake:
    '''
    Class Snake suggest to create instance of object Snake fo game.
    head_x, head_y - coordinates of snake head
    len - length of snake body
    snake_nodes - "container" of snake's body for store instances snake's nodes
    '''
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
        '''
        method for choice snake's head direction
        :param directions: kind of direction
        :return: suitable method
        '''
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
        '''
        Method for process every node and countdowns their lifetime counter,
        if lifetime is equal to zero, then dead node destroy
        :return: None
        '''
        index_delete = 0
        for node in self.snake_nodes:
            node.life_time_down()
            if node.count_live == 0:
                self.snake_nodes.index(node)
            elif node.count_live == self.len:
                continue
        self.snake_nodes.pop(index_delete)

    def move(self, direction):
        '''
        Method suggest movement of snake's body:
            1. Check: snake is steel alive?
            2. Move snake's head
            3. Check: snake didn't eat itself
            4. Create new node and recount lifetime of existing nodes
            5. Append head node by existing nodes

            example:
            past:              present:
            [0]0000 + (0)  --> [0] 0000(0)
            [0] will deleted, () will added
            length of snakes steel 4

        :param direction: kind of direction
        :return: None
        '''
        global SNAKE_BODY_EAT_CHECK
        if not SNAKE_BODY_EAT_CHECK:
            SNAKE_BODY_EAT_CHECK = True
        self._group_to_move_head(direction)()
        head = SnakeNode(x=self.head_x, y=self.head_y, count_live=self.len)
        self.check_eat_body_of_snake()
        self._count_node_life()
        self.snake_nodes.append(head)

    def check_eat_body_of_snake(self):
        '''
        method for check snake body was eating by snake's head or not?
        If yes then raise except IndexError
        :return: None
        '''
        global SNAKE_ALIVE, SNAKE_BODY_EAT_CHECK
        if SNAKE_BODY_EAT_CHECK:
            for node in self[:-1]:
                if self.head_x == node.x and self.head_y == node.y:
                    SNAKE_ALIVE = False  # Snake died X_X
                    raise IndexError

    def draw_snake(self, space):
        '''
        methods for draw snake on the screen:
        actually replace cells of GRASS on cells of SNAKE which declare on top
        :param space: matrix of game's space
        :return: None
        '''
        for node in self.snake_nodes:
            space[node.y][node.x] = SNAKE

    def check_eat_apple(self, aplle_x: int, apple_y: int):
        '''
        method for check did snake eat apple or not?
        if snake did it, then len snake will be increased by one and snake's body will added on head's coordinates a new
        snake's node with new life counter
        :param aplle_x: x coordinate of apple which snake eat
        :param apple_y: y coordinate of apple which snake eat
        :return: None
        '''
        global APPLE_EXIST, SCORE
        if self.head_x == aplle_x and self.head_y == apple_y:
            APPLE_EXIST = False
            self.len += 1
            SCORE += 1
            head = SnakeNode(x=self.head_x, y=self.head_y, count_live=self.len)
            self.snake_nodes.append(head)

    def get_head_coors(self):
        '''
        method return coordinates of snake's head
        :return: (x:int,y:int)
        '''
        return self.head_x, self.head_y


class Apple:
    '''
    Class Apple suggest to create instance of object apple in game.
    apple_x, apple_y - coordinates of apple
    x_range, y_range - allowable maximum range for x and y
    '''
    apple_x: int
    apple_y: int

    x_range: int
    y_range: int

    def __init__(self, x_range: int, y_range: int):
        self.x_range = x_range
        self.y_range = y_range
        self.generate_apple()

    def generate_apple(self):
        '''
        method suggest to create new apple: actually apple just change itself coordinates
        :return: None
        '''
        global APPLE_EXIST
        if not APPLE_EXIST:
            self.apple_x = int(self.x_range * random())
            self.apple_y = int(self.y_range * random())
            APPLE_EXIST = True

    def draw_apple(self, space):
        '''
        methods for draw apple on the screen:
        actually replace cells of GRASS on cells of APPLE which declare on top
        :param space: matrix of game's space
        :return: None
        '''
        space[self.apple_y][self.apple_x] = APPLE

    def get_coors(self):
        '''
        method return coordinates of apple
        :return: (x:int,y:int)
        '''
        return self.apple_x, self.apple_y


class GameWindow:
    '''
    Class GameWindow suggest to create visible space of game.
    window_width - width of window game
    window_hight - hight of window game
    width - width of game space
    hight - hight of game space
    space - matrix of game space
    centre_x,centre_y - coordinates of game space's centre
    snake_object - instance of Snake class actually snake what player will be played
    apple_object - instance of Apple class actually apple what player will be ate in game
    '''

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

    def restart(self):
        '''
        method suggest to restart game, for this all variable and objects to change to initial state
        :return: None
        '''
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
        '''
        method move snake on game space
        :param direction: kind of direction move
        :return: None
        '''
        self.snake_object.move(direction)

    def check_eat_apple(self):
        '''
        method check did snake eat apple on game space
        :return: None
        '''
        self.snake_object.check_eat_apple(*self.apple_object.get_coors())

    def generate_apple(self):
        '''
        method generate apple on game space
        :return: None
        '''
        self.apple_object.generate_apple()

    def clear_game_space(self):
        '''
        method generate new game space
        actually: initiate every cells by GRASS which be declared on the top
        :return: None
        '''
        self.space = [[GRASS for field_w in range(self.width)] for field_h in range(self.hight)]

    def check_borders(self):
        '''
        method check did snake head collide with borders or not?
        if it exist then Game will be stopped and show restart menu
        :return: None
        '''
        global SNAKE_ALIVE
        head_x, head_y = self.snake_object.get_head_coors()
        if (head_x >= self.width or head_x <= 0) or (head_y >= self.hight or head_y <= 0):
            SNAKE_ALIVE = False
            print("bye")
            raise IndexError

    def update_screen(self, score: int):
        '''
        method clear the screen, show borders, game score, snake and apples
        :param score: game score
        :return: None
        '''
        self.clear_game_space()
        self.apple_object.draw_apple(self.space)
        self.snake_object.draw_snake(self.space)

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
    '''
    Class Game suggest to create visible space of game.
    Suggest to show start menu, game menu, restart menu
    '''

    def __init__(self, hight: int = 20, width: int = 100):
        super(Game, self).__init__(hight, width)  # generate game space

    def start(self):
        '''
        method start to listen keyboard 
        :return: None 
        '''
        listener = keyboard.Listener(
            on_press=self.on_press)
        listener.start()

    def on_press(self, key):
        global DIRECTION
        DIRECTION = self._group_to_direct_head(key)
        if key == keyboard.Key.esc:
            # Stop keyboard's listener  
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
        '''
        method show to switch choices in start menu
        :param key: type of key which pressed
        :return: False 
        '''
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

    def _on_press_restart_menu(self, key):
        '''
        method show to switch choices in restart menu
        :param key: type of key which pressed
        :return: False 
        '''
        global RESPAWN, EXIT
        if key == keyboard.Key.up:
            restart_str = "  [Restart] "
            exit_str = "   Exit "
            RESPAWN = True
            EXIT = False
            self.draw_restart_menu(restart_str, exit_str)
        elif key == keyboard.Key.down:
            restart_str = "   Restart "
            exit_str = "  [Exit   ]"
            RESPAWN = False
            EXIT = True
            self.draw_restart_menu(restart_str, exit_str)
        elif key == keyboard.Key.enter:
            return False

    def menu(self):
        start_str = "   [Start] "
        exit_str = "    Exit "
        self.draw_menu(start_str, exit_str)
        with keyboard.Listener(on_press=self._on_press_start_menu) as listener:
            listener.join()

    def restart(self):
        restart_str = "  [Restart] "
        exit_str = "    Exit "
        self.draw_restart_menu(restart_str, exit_str)
        with keyboard.Listener(on_press=self._on_press_restart_menu) as listener:
            listener.join()

    def draw_restart_menu(
            self,
            restart_str="   [Restart] ",
            exit_str="    Exit "):
        '''
        method show restart menu and suggest to restart game or exit from game
        :param restart_str: [Restart] or Restart
        :param exit_str: [Exit] or Exit
        :return: None
        '''
        system('cls')  # TODO исправить на возврат курсора в начало экрана
        menu_y0 = self.centre_y - 3
        menu_x0 = self.centre_x - 8
        score_str = "   Score: {}".format(SCORE)
        rerestart_str_len = len(restart_str)
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
                    elif (x > menu_x0 and x < menu_x0 + 15) and y == menu_y0 + 2 and rerestart_str_len > 0:
                        print(restart_str[x_menu], end="")
                        x_menu += 1
                        rerestart_str_len -= 1
                    elif (x > menu_x0 and x < menu_x0 + 15) and y == menu_y0 + 3 and exit_str_len > 0:
                        print(exit_str[x_menu], end="")
                        x_menu += 1
                        exit_str_len -= 1
                    else:
                        print(" ", end="")
            print()

    def draw_menu(
            self,
            start_str="   [Start] ",
            exit_str="    Exit "):
        '''
        method show start menu and suggest to start game or exit from game
        :param start_str: [Start] or Start
        :param exit_str: [Exit] or Exit
        :return: None
        '''
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
                game.restart()
                game.restart()
