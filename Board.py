import random
from Tile import Tile
from Colors import black, white, colors


class Board:
    size = 4

    def __init__(self, screen, screen_size, font, filename):
        self.screen = screen
        self.screen_size = screen_size
        self.font = font
        self.grid = [[0 for i in range(self.size)] for i in range(self.size)]
        self.prev_grid = [[0 for i in range(self.size)] for i in range(self.size)]
        self.empty = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.prev_empty = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.score = 0
        self.prev_score = 0
        self.filename = filename

    def add_tile(self):
        if not self.is_empty():
            val = 2
            if random.random() > 0.9: val = 4

            pos = random.choice(self.empty)
            self.grid[pos[0]][pos[1]] = val
            self.empty.remove(pos)

    def is_empty(self):
        return len(self.empty) == 0

    # Rotates a position on the board by 90 degrees n times
    def rotated_pos(self, pos, n):
        x, y = pos

        for i in range(n):
            x2 = y
            y2 = -x + self.size - 1
            x, y = x2, y2

        return x, y

    # Rotates the board 90 degrees n times clockwise
    def rotate(self, n):
        new_grid = [[0 for i in range(self.size)] for i in range(self.size)]

        for x in range(self.size):
            for y in range(self.size):
                new_pos = self.rotated_pos((x, y), n)
                new_grid[new_pos[0]][new_pos[1]] = self.grid[x][y]

        return new_grid


    # To make a move, rotates grid n times, moves tiles up (if possible), rotates grid back to original position
    # Returns whether or not any moves were made (boolean value)
    def move(self, n):

        # Store previous grid
        self.prev_grid = self.grid
        self.prev_empty = self.empty
        self.prev_score = self.score

        # Rotate positions
        self.grid = self.rotate(n)
        self.empty = [self.rotated_pos(pos, n) for pos in self.empty]

        moved = False

        # Moves each tile
        for x in range(1, self.size):
            for y in range(self.size):

                # Ignore empty tiles
                if self.grid[x][y] == 0: continue

                # Finds highest empty spot
                new_x = x
                while new_x > 0 and self.grid[new_x - 1][y] == 0: new_x -= 1

                # Moves tile up
                self.grid[new_x][y], self.grid[x][y] = self.grid[x][y], self.grid[new_x][y]
                self.empty.append((x, y))
                self.empty.remove((new_x, y))

                if (x, y) != (new_x, y): moved = True

                # Combines tile with tile above if necessary
                if new_x > 0 and self.grid[new_x - 1][y] == self.grid[new_x][y]:
                    self.grid[new_x - 1][y] *= 2
                    self.grid[new_x][y] = 0
                    self.empty.append((new_x, y))

                    self.score += self.grid[new_x - 1][y]
                    moved = True

        # Rotate positions back to original orientation
        self.grid = self.rotate(self.size - n)
        self.empty = [self.rotated_pos(pos, self.size - n) for pos in self.empty]

        return moved

    # Moves tiles up
    def up(self):
        return self.move(0)

    # Moves tiles left
    def left(self):
        return self.move(1)

    # Moves tiles down
    def down(self):
        return self.move(2)

    # Moves tiles right
    def right(self):
        return self.move(3)

    # Undoes last move
    def undo(self):
        self.grid = self.prev_grid
        self.empty = self.prev_empty
        self.score = self.prev_score

    # Tests a move to see if it is possible; returns boolean value
    def test(self, move):

        # Store what are currently the previous values
        prev_grid = self.prev_grid
        prev_empty = self.prev_empty
        prev_score = self.prev_score

        # Try a move and undo it
        moved = move()
        self.undo()

        # Restore old previous values
        self.prev_grid = prev_grid
        self.prev_empty = prev_empty
        self.prev_score = prev_score

        return moved

    # Returns whether or not any moves are possible
    def move_possible(self):
        # Tests all moves to see if any are possible
        return self.test(self.up) or self.test(self.left) or self.test(self.down) or self.test(self.right)

    def get_score(self):
        return self.score

    def get_high_score(self):
        # Get high score from file
        file = open(self.filename, 'r+')
        high_score = int(file.readline())

        # See if current score is higher than high score
        if self.score > high_score:
            # Write new high score to file
            high_score = self.score
            file.seek(0)
            file.truncate()
            file.write(str(high_score))

        file.close()
        return high_score

    def display(self):
        screen_width = self.screen_size[0]
        screen_height = self.screen_size[1]

        # Displays tiles
        for i in range(self.size):
            for j in range(self.size):
                x = j * screen_width / self.size
                y = i * screen_width / self.size

                tile_position = (x, y)
                tile_width = screen_width / self.size - 10
                tile_value = self.grid[i][j]

                tile = Tile(tile_value, tile_position, tile_width, colors[tile_value], white)
                tile.display(self.screen, self.font)

        # Displays current score
        score_text = self.font.render("Score: " + str(self.score), False, black)
        score_position = (0, screen_height - 220)
        self.screen.blit(score_text, score_position)

        # Displays high score
        high_score_text = self.font.render("High Score: " + str(self.get_high_score()), False, black)
        high_score_position = (0, screen_height - 120)
        self.screen.blit(high_score_text, high_score_position)