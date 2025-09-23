import pygame
import pytmx
import pyscroll
from player import Player

class Game:

    def __init__(self):
        #configuration de la fenetre de jeu
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("pygame - adventure")

        #chargement de data de map
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # generer un joueur
        player_position = tmx_data.get_object_by_name("player_spawn")
        self.player = Player(player_position.x, player_position.y)

        #dessiner les calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)
    
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            print("haut")
            self.player.change_animation('up')
            self.player.move_up()

        elif pressed[pygame.K_DOWN]:
            print("bas")
            self.player.move_down()
            self.player.change_animation('down')

        elif pressed[pygame.K_LEFT]:
            print("gauche")
            self.player.move_left()
            self.player.change_animation('left')

        elif pressed[pygame.K_RIGHT]:
            print("droite")
            self.player.move_right()
            self.player.change_animation('right')



    def run(self):

        clock = pygame.time.Clock()

        #active le jeu - boucle
        running = True

        while running:

            self.handle_input()
            self.group.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # 60 images/sec
            clock.tick(60)

        pygame.quit()

