import pygame
import os
from Board import Board
from Colors import black, white


high_score_file_name = 'high_score.txt'


def set_up_game():
    # Initialize pygame
    pygame.init()
    pygame.font.init()

    # Set up screen
    screen_size = (800, 1000)
    screen = pygame.display.set_mode(screen_size)
    screen.fill(white)

    # Display start screen
    font = pygame.font.SysFont('Comic Sans MS', 20)

    text = "Press arrow keys to move tiles and 'u' to undo a move. Press any key to continue."
    start_message = font.render(text, False, black)
    screen.blit(start_message, (20, 250))

    pygame.display.set_caption('2048')
    pygame.display.flip()
    pygame.display.update()

    # Wait until a key is pressed for game to start
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                wait = False

    # Set up game board and display it
    screen.fill(white)
    font = pygame.font.SysFont('Comic Sans MS', 60)

    board = Board(screen, screen_size, font, get_high_score_file_path())
    board.add_tile()
    board.display()

    pygame.display.flip()
    pygame.display.update()
    
    return board, screen, font


def get_high_score_file_path():
    file_path = os.path.join(os.getcwd(), high_score_file_name)

    # If the high score file doesn't exist, create it
    if not os.path.exists(file_path):
        file = open(file_path, 'w+')
        file.write('0')  # Initial high score is 0

    return file_path

def main():
    board, screen, font = set_up_game()

    # Game loop
    game_over = False
    while not game_over:
        for event in pygame.event.get():

            # Quits game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Checks if moves are possible
            # and if the game should continue
            if event.type == pygame.KEYUP:
                if not board.move_possible():
                    game_over = True

            moved = False

            if event.type == pygame.KEYDOWN:
                # Undoes last move if 'u' is pressed
                if event.key == pygame.K_u: board.undo()

                # Performs corresponding move if arrow keys are pressed
                if event.key == pygame.K_UP: moved = board.up()
                if event.key == pygame.K_LEFT: moved = board.left()
                if event.key == pygame.K_DOWN: moved = board.down()
                if event.key == pygame.K_RIGHT:moved = board.right()

                # Adds tile if move was made
                if moved: board.add_tile()

                # Displays board
                screen.fill(white)
                board.display()
                pygame.display.flip()
                pygame.display.update()

    # Display end message
    end_message = font.render("GAME OVER", False, black)
    screen.blit(end_message, (50, 250))
    final_score = font.render("Final Score: " + str(board.get_score()), False, black)
    screen.blit(final_score, (50, 400))

    pygame.display.flip()
    pygame.display.update()


if __name__ == "__main__":
    main()