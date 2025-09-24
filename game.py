import pygame
import pytmx
import pyscroll
from player import Player

class Game:

    def __init__(self):
        #configuration de la fenetre de jeu
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("pygame - adventure")
        self.map = "world"  

        #chargement de data de 1er map (nature)
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
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        #les collisions
        self.walls = []

        for col in tmx_data.objects:
            if col.type == "collision":
                rect = pygame.Rect(col.x, col.y, col.width, col.height)
                self.walls.append(rect)

        # mecanism d'entre à la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP] or pressed[pygame.K_DOWN] or pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]:
            self.player.save_location()  

        if pressed[pygame.K_UP]:
            self.player.change_animation('up')
            self.player.move_up()

        if pressed[pygame.K_DOWN]:
            self.player.change_animation('down')
            self.player.move_down()

        if pressed[pygame.K_LEFT]:
            self.player.change_animation('left')
            self.player.move_left()

        if pressed[pygame.K_RIGHT]:
            self.player.change_animation('right')
            self.player.move_right()

    def update(self):
        self.group.update()
        
        # verification de l'entre dans la maison
        if self.map == "world" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = "house"

        # verification de la sortie de la maison - FIXED: use exit_house_rect instead of enter_house_rect
        if self.map == "house" and self.player.feet.colliderect(self.exit_house_rect):
            self.switch_world()
            self.map = "world"
            
        # verification de collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()


    def switch_house(self):
        #chargement de data de 2eme map (maison)
        tmx_data = pytmx.util_pygame.load_pygame('house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #les collisions
        self.walls = []

        for col in tmx_data.objects:
            if col.type == "collision":
                rect = pygame.Rect(col.x, col.y, col.width, col.height)
                self.walls.append(rect)
        
        #dessiner les calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # mecanism de sortir de la maison
        exit_house = tmx_data.get_object_by_name("exit_house")
        self.exit_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        # spawing devans la maison
        spawn_point_house = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn_point_house.x
        self.player.position[1] = spawn_point_house.y -20

    def switch_world(self):
        #chargement de data de 2eme map (maison)
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        #les collisions
        self.walls = []

        for col in tmx_data.objects:
            if col.type == "collision":
                rect = pygame.Rect(col.x, col.y, col.width, col.height)
                self.walls.append(rect)
        
        #dessiner les calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # mecanism d'entre à la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
    
        # spawing devans la maison
        spawn_point_house = tmx_data.get_object_by_name("enter_house_exit")
        self.player.position[0] = spawn_point_house.x
        self.player.position[1] = spawn_point_house.y -20

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

