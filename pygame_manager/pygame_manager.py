import pygame

# Initialize pygame globally
pygame.init()
pygame.display.set_caption("Quantum Chess")

# Shared resources
clock = pygame.time.Clock()
symbol_font = pygame.font.SysFont('Comic Sans MS', 20)
game_over_font = pygame.font.SysFont('Comic Sans MS', 50)