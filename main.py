import pygame
pygame.init()

#configuration de la fenetre de jeu
pygame.display.set_mode((800,600))
pygame.display.set_caption("pygame - adventure")

#active le jeu - boucle
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False