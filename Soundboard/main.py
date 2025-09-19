import pygame
import sys

import utils
from button_menu import Menu

#This is required so that the audio is routed to the virtual microphone and not the speakers
pygame.mixer.pre_init(devicename="CABLE Input (VB-Audio Virtual Cable)")
pygame.init()
pygame.mixer.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class game:
    def __init__(self, display):
        self.display = display
        self.clock = pygame.time.Clock()
        self.running = True
        self.clicked = False
        self.font = pygame.font.SysFont("couriernew", 16)

        self.button_width = (SCREEN_WIDTH // 4) - 50
        self.button_height = (SCREEN_HEIGHT // 2) - 50

        self.buttons_pos = []

        self.assets = {"menu": pygame.transform.smoothscale_by(utils.get_image("menu.png"), 0.4),
                       "speaker": pygame.transform.smoothscale_by(utils.get_image("speaker.png"), 0.05)}

    def generate_positions(self):
        #Position for the first sound button - the starting position
        start_pos = [(SCREEN_WIDTH - (self.button_width * 4)) // 2, (SCREEN_HEIGHT - (self.button_height * 2)) // 2]

        self.buttons_pos.append(start_pos)

        #This position is for sound button below the first one - at the starting position
        self.buttons_pos.append([start_pos[0], start_pos[1] + self.button_height])

        for x in range(1, 4):
            new_pos_x = (start_pos[0] + (self.button_width * x), start_pos[1])
            new_pos_y = (start_pos[0] + (self.button_width * x), start_pos[1] + self.button_height)

            self.buttons_pos.append(new_pos_x)
            self.buttons_pos.append(new_pos_y)

    def generate_rects(self):
        buttons_dictionary = {}
        self.generate_positions()

        for position in self.buttons_pos:
            #We create a rect object and an instance of the menu class for each sound button
            button_rect = (pygame.Rect(position[0], position[1], self.button_width, self.button_height))

            #This menu object represents our menu button which is located on each sound button
            menu = Menu((button_rect.topright[0] - 50, button_rect.topright[1] + 20), self.assets['menu'])

            buttons_dictionary[str(position[0]) + "," +  str(position[1])] = {
                "rect": button_rect,
                "menu": menu,
                "display_name": None,
                "file": "None",
                "pysound": "None",
            }


        #pysound key represents our sound object, file is just the path to the sound file we are using
        #display_name is just the nickname we display on each sound button - if it has an associated sound file 

        buttons_dictionary = utils.process_data(buttons_dictionary)
        return buttons_dictionary
            
    def run(self):
        last_pos = []
        buttons_dictionary = self.generate_rects()

        while self.running:
            x, y = pygame.mouse.get_pos() #Gets position of the mouse
            self.display.fill((25, 25, 25))

            for key in list(buttons_dictionary):
                menu = buttons_dictionary[key]["menu"] #Menu object
                rec = buttons_dictionary[key]["rect"] #Rect object

                if rec.collidepoint(x, y): #This checks if the mouse is hovering over the button
                    colour = 60, 110, 155

                    pysound = buttons_dictionary[key]["pysound"]

                    if pysound != "None":
                        if self.clicked and not(menu.check_clicked((x, y), self.clicked)):
                            #If the mouse was clicked but not on the menu button, we play the sound
                            pygame.mixer.stop()
                            pysound.play()
                            #Last_pos represents the position of the sound button - which played a sound - that was clicked
                            last_pos = rec.bottomright
                else:
                    colour = 70, 130, 180

                #These are just how ui/ sound buttons look visually
                pygame.draw.rect(display, (192, 192, 192), rec)
                pygame.draw.rect(display, (0, 0, 0), rec, width=2)

                rec_copy = rec.copy()
                
                rec_copy.width = rec.width - 15
                rec_copy.height = rec.height - 15

                rec_copy.x = rec.x + 8
                rec_copy.y = rec.y + 8

                pygame.draw.rect(display, (colour), rec_copy)
                pygame.draw.rect(display, (25, 25, 25), rec_copy, width=3)

                menu.update([x, y], self.display, self.clicked, buttons_dictionary, key)

                display_name = buttons_dictionary[key]["display_name"]
                if display_name != "None":
                    #We render the display name of the button to the screen 
                    text = self.font.render(buttons_dictionary[key]["display_name"], True, (255, 255, 255))
                    self.display.blit(text, (rec.bottomleft[0] + 15, rec.bottomleft[1] - 35))

                if pygame.mixer.get_busy() and last_pos:
                    #This provides visual clarity as to whether the sound is still playing
                    self.display.blit(self.assets["speaker"], (last_pos[0] - 40, last_pos[1] - 40))

            self.clicked = False
                  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            pygame.display.update()
            self.clock.tick(60)

        utils.save_data(buttons_dictionary)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game(display).run()