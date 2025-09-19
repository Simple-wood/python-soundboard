import pygame
from tkinter import filedialog
from tkinter import messagebox
from utils import get_nickname

class Menu:
    def __init__(self, position, image):
        self.position = position
        self.image = image

        self.option_x = self.position[0] - 130
        self.option_y = self.position[1] - 5

        self.option = Options((self.option_x, self.option_y)) #We create an instance of the options class
        self.option.generate_option_positions()

    def check_clicked(self, mouse_pos, mouse_down):
        button_clicked = False
        image_rect = pygame.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())

        if image_rect.collidepoint(mouse_pos) and mouse_down:
            #Checks whether the menu button has been clicked
            button_clicked = True

        return button_clicked
    
    def update(self, mouse_pos, display, mouse_down, buttons_dictionary, button_position):

        if self.check_clicked(mouse_pos, mouse_down):
            self.option.clicked = True
            mouse_down = False #Set this to False so the options menu doesnt immediately close

        display.blit(self.image, self.position)

        self.option.update(mouse_pos, display, mouse_down, buttons_dictionary, button_position)
    
class Options:
    def __init__(self, position):
        self.position = position
        self.clicked = False
        self.buttons = []
        self.font = pygame.font.SysFont("couriernew", 16)

    def generate_option_positions(self):
        options = {
            0: "add",
            1: "remove",
            2: "edit",
        }
        for y in range(3):
            new_y = self.position[1] + (25 * y)

            self.buttons.append([self.position[0] + 10, new_y, options[y]])
            #The options menu consists of three buttons - add, remove and edit

    def get_file(self, buttons_dictionary, position):
        is_valid = False
        file_name = filedialog.askopenfilename() #We open a file search menu and get the file path
        type =  (file_name[-3::]) #This gets the file extension

        if file_name != "":
            if type in ["mp3", "wav"]:
                is_valid = True
                
        if is_valid:
            #Updates the sound button's information in the dictionary
            buttons_dictionary[position]["file"] = file_name
            
            sound = pygame.mixer.Sound(file_name)
            buttons_dictionary[position]["pysound"] = sound

            nickname = get_nickname(file_name)
            buttons_dictionary[position]["display_name"] = nickname

        else:
            messagebox.showerror("Error", "Please select a valid file")


    def check_button(self, mouse_down, button, buttons_dictionary, position):
        #We check which option button has been clicked, if it has been clicked, and perform an appropiate action
        #The key - which is called position - is used to identify which button has been pressed

        if buttons_dictionary[position]["pysound"] == "None":
            if mouse_down and button[2] != "remove":
                self.get_file(buttons_dictionary, position)
            elif mouse_down and button[2] == "remove":
                messagebox.showinfo("Information", "There is no file to remove")

        else:
            if mouse_down and button[2] == "edit":
                self.get_file(buttons_dictionary, position)

            elif mouse_down and button[2] == "remove":
                buttons_dictionary[position]["pysound"] = "None"
                buttons_dictionary[position]["file"] = "None"
                buttons_dictionary[position]["display_name"] = "None"

            elif mouse_down and button[2] == "add":
                messagebox.showinfo("Information", "There is already a file here")


    def update(self, mouse_pos, display, mouse_down, buttons_dictionary, position):
        #if count is 0, the mouse is no longer hovering over the options menu
        count = 0
        if self.clicked: #If the menu button has been clicked
            
            for button in self.buttons:
                button_rect = pygame.Rect(button[0], button[1], 120, 25)

                if button_rect.collidepoint(mouse_pos):
                    colour = (80, 95, 110)
                    count += 1 #The mouse is still hovering over the options menu
                    self.check_button(mouse_down, button, buttons_dictionary, position)
                else:
                    colour = (112, 128, 144)

                text = self.font.render(button[2], True, (0,0,0))

                pygame.draw.rect(display, colour, button_rect, border_radius=4)
                pygame.draw.rect(display, (0,0,0), button_rect, width=2, border_radius=4)

                display.blit(text, (button[0] + 5, button[1] + 2))

        #We want the options menu to close if the user has clicked elsewhere, this handles that
        if mouse_down and count == 0:
            self.clicked = False

    
                

                


        