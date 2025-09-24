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
        if player_position is None:
            raise ValueError("No object named 'player_spawn' found in the TMX map.")
        self.player = Player(player_position.x, player_position.y)

        #dessiner les calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        #les collisions
        self.walls = []

        for col in tmx_data.objects:
            if col.type == "collision":
                rect = pygame.Rect(col.x, col.y, col.width, col.height)
                self.walls.append(rect)
    
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        moved = False

        if pressed[pygame.K_UP] or pressed[pygame.K_DOWN] or pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]:
            self.player.save_location()  

        if pressed[pygame.K_UP]:
            self.player.change_animation('up')
            self.player.move_up()
            moved = True

        if pressed[pygame.K_DOWN]:
            self.player.change_animation('down')
            self.player.move_down()
            moved = True

        if pressed[pygame.K_LEFT]:
            self.player.change_animation('left')
            self.player.move_left()
            moved = True

        if pressed[pygame.K_RIGHT]:
            self.player.change_animation('right')
            self.player.move_right()
            moved = True

    def update(self):
        self.group.update()

        # verification de collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
            

    def run(self):

        clock = pygame.time.Clock()

        #active le jeu - boucle
        running = True

        while running:

            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # 60 images/sec
            clock.tick(60)

        pygame.quit()

