from Player import Player
import pygame
import math
from Game_States import GameStates
from pygame import mixer

SCALE = 64

class Game:


    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.Game_States = GameStates.NONE
        self.map = []
        self.camera = [0, 0]

    def set_up(self):
        player = Player(1, 0) # More aesthetically pleasing to have him start on the path :-) -- DoctorMike
        self.player = player
        self.objects.append(player)
        self.Game_States = GameStates.RUNNING
        self.load_map("map2") # Changed the map to test X Axis scrolling -- DoctorMike
        print("do the setup")


    def update(self):
        self.screen.fill((0, 0, 0))
        print("updating")
        self.handle_events()
        self.render_the_map(self.screen)

        for object in self.objects:
            object.render(self.screen, self.camera)

    def handle_events(self):
        walksoundone = pygame.mixer.Sound('Sounds/Walking sounds/Walk for project one.wav')
        walksoundtwo = pygame.mixer.Sound('Sounds/Walking sounds/Walk for project two.wav')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           #this will end the while loop
                self.Game_States = GameStates.GAMEOVER

            elif event.type == pygame.KEYDOWN:          #Key events
                if event.key == pygame.K_ESCAPE:
                    self.Game_States = GameStates.GAMEOVER
                elif event.key == pygame.K_LEFT:
                    self.move_unit(self.player, [-1, 0])
                    walksoundone.play()
                elif event.key == pygame.K_RIGHT:
                    self.move_unit(self.player, [1, 0])
                    walksoundtwo.play()
                elif event.key == pygame.K_UP:
                    self.move_unit(self.player, [0, -1])
                    walksoundone.play()
                elif event.key == pygame.K_DOWN:
                    self.move_unit(self.player, [0,1])
                    walksoundtwo.play()

    def load_map(self, file_name):
        with open("maps/" + file_name + ".txt") as map_file:
            for line in map_file:
                tile = []
                for i in range(0, len(line) - 1, 2):
                    tile.append(line[i])
                    
                self.map.append(tile)

    def render_the_map(self, screen):

        self.position_camera()
        tile_y = 0
        for line in self.map:
            tile_x = 0
            for tile in line:
                image = images_for_map[tile]
                rect = pygame.Rect((tile_x - self.camera[0]) * SCALE, (tile_y - self.camera[1]) * SCALE, SCALE, SCALE)
                screen.blit(image, rect)
                tile_x += 1
            tile_y += 1

    def move_unit(self, unit, position_change):
        new_position = [unit.position[0] + position_change[0], unit.position[1] + position_change[1]]

        if new_position[0] < 0 or new_position[0] > (len(self.map[0]) - 1): # changed from -2
            return

        if new_position[1] < 0 or new_position[1] > (len(self.map[1]) - 1): # changed from -2
            return

        unit.update_position(new_position)
        return

    def position_camera(self):
        # Added X Axis Camera Stuff -- DoctorMike
        max_x_position = len(self.map[0]) - 832 / SCALE
        x_position = self.player.position[0] - math.ceil(round(832 / SCALE / 2))

        if x_position < max_x_position and x_position >= 0:
            self.camera[0] = x_position
        elif x_position < 0:
            self.camera[0] = 0
        else:
            self.camera[0] = max_x_position


        # End of additions -- DoctorMike
        
        max_y_position = len(self.map[1]) - 832 / SCALE
        y_position = self.player.position[1] - math.ceil(round(832 / SCALE / 2))

        if y_position < max_y_position and y_position >= 0:
            self.camera[1] = y_position
        elif y_position < 0:
            self.camera[1] = 0
        else:
            self.camera[1] = max_y_position




images_for_map = {
    "G": pygame.transform.scale(pygame.image.load("images/_tile1.png"), (SCALE, SCALE)),
    "R": pygame.transform.scale(pygame.image.load("images/_tile3.png"), (SCALE, SCALE))
}

class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.Game_States_Menu = GameStates.NONE
        self.isMenu = True
        self.xPos = 0
        self.yPos = 0
        self.mousePos = [self.xPos, self.yPos]
        self.start_button_image = pygame.image.load("images/menu_button_start.png").convert_alpha()
        self.quit_button_image = pygame.image.load("images/menu_button_quit.png").convert_alpha()

    def set_up_menu(self):
        self.Game_States_Menu = GameStates.RUNNING

    def mouse_click(self, xPos, yPos):
        if xPos > 64 and xPos < 192:
            if yPos > 64 and yPos < 128:
                self.isMenu = False
                print("Start Button Clicked")
            elif yPos > 192 and yPos < 256:
                self.Game_States_Menu = GameStates.GAMEOVER
                print("Game Quit")

    def draw_menu(self, screen):

        screen.blit(self.start_button_image, (64, 64))# Draws the start button

        screen.blit(self.quit_button_image, (64, 192))# Draws the quit button


    def update(self):
        self.screen.fill((0, 0, 0))
        self.draw_menu(self.screen)
        self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           #this will end the while loop
                self.Game_States_Menu = GameStates.GAMEOVER
                self.isMenu = False

            elif event.type == pygame.MOUSEBUTTONDOWN:          #Key events
                self.mousePos = pygame.mouse.get_pos()
                self.mouse_click(self.mousePos[0], self.mousePos[1])
                print(pygame.mouse.get_pos())