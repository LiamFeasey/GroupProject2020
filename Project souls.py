import pygame
from Game import Game, Menu
from Game_States import GameStates
from pygame import mixer

pygame.init()       #initiatin pygame

mixer.music.load('Music/backgroundMusicFixed.wav')
mixer.music.play(-1)

GameWindow = pygame.display.set_mode((832, 832))        #Creating the game window

pygame.display.set_caption("Project Souls")      #adding the project name

clock = pygame.time.Clock()         #creating the framerate


GameWindow.fill((0, 0, 0))

game = Game(GameWindow)
menu = Menu(GameWindow)


game.set_up()   #Setting up the objects
menu.set_up_menu()


while game.Game_States == GameStates.RUNNING and menu.Game_States_Menu == GameStates.RUNNING:    #Keeps the game running while the state is in RUNNING
    clock.tick(60)      #setting the fps to 60
    if menu.isMenu:
        #print(Menu.isMenu)
        menu.update()
    else:
        game.update()       #Updating the game
    pygame.display.flip() #Update the full display Surface to the screen




