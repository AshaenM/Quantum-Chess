import os
import pygame
from settings.config import PIECE_IMAGES, ASSET_DIR

def load_images():
    """Load and scale chess piece images."""
    images = {}
    for piece, filename in PIECE_IMAGES.items():
        path = os.path.join(ASSET_DIR, filename)
        image = pygame.image.load(path)
        scale_size = 40 if piece in ['P', 'p', 'na'] else 45 if piece in ['R', 'r', 'N', 'n'] else 55
        images[piece] = pygame.transform.smoothscale(image, (scale_size, scale_size))
    return images
