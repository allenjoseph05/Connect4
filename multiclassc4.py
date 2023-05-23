import pygame
import numpy as np
import pygame_menu
from pygame_menu import themes

# Initialize Pygame
pygame.init()
w = 800
h = 800
surface = pygame.display.set_mode((w, h))


class GameBoard:
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.board = self.board_structure()
        self.screen_width = 800
        self.screen_height = 800
        self.window = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Connect 4")

        self.red = (220, 53, 69)
        self.yellow = (255, 193, 7)
        self.black = (20, 20, 20)
        self.white = (255, 255, 255)
        self.cyan = ((0, 127, 225))
        self.blue = (0, 83, 255)
        self.myfont = pygame.font.SysFont("monospace", 75)

        self.cell_width = (self.screen_width - 200) // self.columns
        self.cell_height = (self.screen_height - 300) // self.rows
        self.radius = min(self.cell_width, self.cell_height) // 2 - 5

    def board_structure(self):
        board = np.zeros((self.rows, self.columns))
        return board

    def create_board(self):
        pygame.draw.rect(self.screen, self.cyan, (75, 170, 660, 560))
        pygame.draw.rect(self.screen, self.blue, (75, 170, 660, 560), 10)
        for row in range(self.rows):
            for col in range(self.columns):
                center_x = col * self.cell_width + self.cell_width // 2 + 70 + self.radius
                center_y = row * self.cell_height + self.cell_height // 2 + 170 + self.radius
                pygame.draw.circle(self.screen, self.white, (center_x, center_y), self.radius, 0)
                pygame.draw.circle(self.screen, self.blue, (center_x, center_y), self.radius, 5)

        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] == 1:
                    center_x = col * self.cell_width + self.cell_width // 2 + 70 + self.radius
                    center_y = (self.rows - 1 - row) * self.cell_height + self.cell_height // 2 + 170 + self.radius
                    pygame.draw.circle(self.screen, self.red, (center_x, center_y), self.radius - 5, 0)
                elif self.board[row][col] == 2:
                    center_x = col * self.cell_width + self.cell_width // 2 + 70 + self.radius
                    center_y = (self.rows - 1 - row) * self.cell_height + self.cell_height // 2 + 170 + self.radius
                    pygame.draw.circle(self.screen, self.yellow, (center_x, center_y), self.radius - 5, 0)

        pygame.display.update()


class GameWin:
    def __init__(self, gb):
        self.gb = gb

    def win_move(self, board, row, column, coin):
        for c in range(self.gb.columns - 3):
            if (
                board[row][c] == coin
                and board[row][c + 1] == coin
                and board[row][c + 2] == coin
                and board[row][c + 3] == coin
            ):
                return True

        for r in range(self.gb.rows - 3):
            if (
                board[r][column] == coin
                and board[r + 1][column] == coin
                and board[r + 2][column] == coin
                and board[r + 3][column] == coin
            ):
                return True

        for r in range(max(0, row - 3), min(self.gb.rows, row + 4)):
            for c in range(max(0, column - 3), min(self.gb.columns, column + 4)):
                if (
                    r + 3 < self.gb.rows
                    and c + 3 < self.gb.columns
                    and board[r][c] == coin
                    and board[r + 1][c + 1] == coin
                    and board[r + 2][c + 2] == coin
                    and board[r + 3][c + 3] == coin
                    and (r - c == row - column or r - c == row - column + 3)
                ):
                    return True

        for r in range(min(self.gb.rows - 1, row + 3), max(0, row - 3), -1):
            for c in range(max(0, column - 3), min(self.gb.columns - 3, column + 1)):
                if (
                    r - 3 >= 0
                    and c + 3 < self.gb.columns
                    and board[r][c] == coin
                    and board[r - 1][c + 1] == coin
                    and board[r - 2][c + 2] == coin
                    and board[r - 3][c + 3] == coin
                    and (r + c == row + column or r + c == row + column - 3)
                ):
                    return True

        return False


class Functionality:
    def __init__(self):
        self.gb = GameBoard()
        self.gw = GameWin(self.gb)
        self.turn = 0

    def coin_movement(self, row, col, coin):
        self.gb.board[row][col] = coin

    def valid_location(self, col):
        return self.gb.board[self.gb.rows - 1][col] == 0

    def next_row(self, col):
        for r in range(self.gb.rows):
            if self.gb.board[r][col] == 0:
                return r

    def run(self):
        self.gb.screen.fill(self.gb.black)
        self.gb.create_board()
        image1 = pygame.image.load("quit.png")
        image2 = pygame.image.load("restart.png")

        quit_image = pygame.transform.scale(image1, (48, 44))
        restart_image = pygame.transform.scale(image2, (44, 44))

        quit_rect = quit_image.get_rect()
        quit_rect.top = 30
        quit_rect.right = self.gb.screen_width - 26

        restart_rect = restart_image.get_rect()
        restart_rect.top = 90
        restart_rect.right = self.gb.screen_width - 30

        self.gb.screen.blit(quit_image, quit_rect)
        self.gb.screen.blit(restart_image, restart_rect)

        pygame.display.update()

        is_running = True
        game_end = False

        while is_running:
            sq_x, sq_y = 110, 160
            sq_w, sq_h = 585, 550

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    mouse_pos = pygame.mouse.get_pos()
                    mouse_click = pygame.mouse.get_pressed()

                    if quit_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                        is_running = False

                    if restart_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
                        self.gb.board = self.gb.board_structure()
                        self.turn = 0
                        is_running = True
                        game_end = False
                        self.gb.screen.fill(self.gb.black)
                        self.gb.create_board()
                        self.gb.screen.blit(quit_image, quit_rect)
                        self.gb.screen.blit(restart_image, restart_rect)
                        pygame.display.update()

                    if sq_x <= mouse_x <= sq_x + sq_w and sq_y <= mouse_y <= sq_y + sq_h:
                        col = int((event.pos[0] - 70 - self.gb.radius) / self.gb.cell_width)

                        if self.valid_location(col) and not game_end:
                            row = self.next_row(col)
                            self.coin_movement(row, col, self.turn + 1)

                            if self.gw.win_move(self.gb.board, row, col, self.turn + 1):
                                game_end = True
                                label_text = f"Player {self.turn + 1} wins!!"
                                label = self.gb.myfont.render(
                                    label_text,
                                    1,
                                    (self.gb.red if self.turn == 0 else self.gb.yellow),
                                )
                                self.gb.screen.blit(label, (40, 10))
                                pygame.display.update()

                            if not game_end:
                                if np.count_nonzero(self.gb.board == 0) == 0:
                                    label_text = f"DRAW!"
                                    label = self.gb.myfont.render(
                                        label_text, 1, (self.gb.white)
                                    )
                                    self.gb.screen.blit(label, (40, 10))
                                    pygame.display.update()

                                self.turn = (self.turn + 1) % 2

                        self.gb.create_board()
                        pygame.display.update()
        return

class Connect4Menu:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 800
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.menu = pygame_menu.Menu(
            "Welcome",
            self.width,
            self.height,
            theme=themes.THEME_BLUE,
            onclose=pygame_menu.events.EXIT,
        )
        self.menu.add.button("Play", self.start_game)
        self.menu.add.button("Instructions", self.show_instructions)
        self.menu.add.button("Quit", self.quit_game)
        self.should_quit = False
        self.instructions_menu = None

    def start_game(self):
        game = Functionality()
        game.run()

    def show_instructions(self):
        if self.instructions_menu is None:
            self.instructions_menu = pygame_menu.Menu(
                "Instructions",
                self.width,
                self.height,
                theme=themes.THEME_BLUE,
                onclose=self.close_instructions,
            )
            instructions_text = "Connect 4 is a two-player game played on a grid of 6 rows and 7 columns.\n" \
                                "Players take turns dropping their colored discs into any of the columns.\n" \
                                "Once a disc is dropped into a column, it occupies the lowest available empty slot\n" \
                                "in that column.\n" \
                                "Discs always fall straight down and stack on top of each other.\n" \
                                "The game continues until one player successfully connects four discs or \n" \
                                "the entire game board is filled.\n"
            self.instructions_menu.add.label(instructions_text, font_size=20)
            self.instructions_menu.add.button("Back", self.close_instructions)

        self.instructions_menu.enable()
        self.instructions_menu.mainloop(self.surface)

    def close_instructions(self):
        self.instructions_menu.disable()
        self.instructions_menu = None

    def quit_game(self):
        self.should_quit = True

    def run(self):
        while not self.should_quit:
            self.surface.fill((0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.should_quit = True

            if self.instructions_menu is not None:
                self.instructions_menu.update(events)
                self.instructions_menu.draw(self.surface)
            else:
                self.menu.update(events)
                self.menu.draw(self.surface)

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    menu = Connect4Menu()
    menu.run()