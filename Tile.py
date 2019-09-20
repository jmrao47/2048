import pygame
from operator import add


class Tile:
    text_offset = (5, 40)

    # Initializer / Instance attributes
    def __init__(self, val, pos, width, color, font_color):
        self.value = val
        self.position = pos
        self.width = width
        self.color = color
        self.font_color = font_color

    def display(self, screen, font):
        # Display square
        pygame.draw.rect(screen, self.color, [self.position[0], self.position[1], self.width, self.width])

        # Display text
        if self.value != 0:
            text = font.render(str(self.value), False, self.font_color)
            screen.blit(text, list(map(add, self.position, self.text_offset)))