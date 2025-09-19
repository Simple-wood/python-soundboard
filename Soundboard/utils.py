import pygame 

PATH = "sfx.txt" #Where the information about the sound buttons and what sound files are associated with them are stored

def get_image(path):
    #Retrieves an image from a path in a format that pygame can work with
    image = (pygame.image.load(path)).convert_alpha()
    return image

def save_data(dictionary):
    #This erases all data in the text file
    file = open(PATH, "w")
    file.close()

    for key in list(dictionary):
        file = open(PATH, "a")
        #We save the data - stored in the buttons dictionary - to the text file
        file.write(str(key) + "|" + dictionary[key]["file"] + "\n")

    file.close()

def get_data():
    data = []
    try:
        file = open(PATH, "r")

        #We go through each line in the text file
        for line in file.readlines():
            #This splits the line into two chunks, the key and the file path for each button
            pairs = line.split("|")

            sfx = pairs[1]
            sfx = sfx[:-1] #The original file path includes \n at the end, this gets rid of that \n

            data.append([pairs[0], sfx])

        file.close()

    except FileNotFoundError:
        #If the text file does not exist, we create one
        file = open(PATH, "w")
        file.close()

    return data

def get_nickname(file_path):
    #We split the file path into chunks
    pieces = file_path.split("/")
    
    name = pieces[-1] #The last item in the pieces array is the name of the file
    type = name[-3::] #We get the file extension

    #We generate a nickname based on the first first 2 characters, the last character (of the actual name) and the file extension
    nickname = name[:2] + name[-5] + "." + type
    return nickname


def process_data(button_dictionary):
    data = get_data()

    for pair in data:
        if pair[1] != "None":
            #If the sound button has associated information with it, we update the buttons dictionary
            sound = pygame.mixer.Sound(pair[1])

            button_dictionary[pair[0]]["file"] = pair[1]
            button_dictionary[pair[0]]["pysound"] = sound
            button_dictionary[pair[0]]["display_name"] = get_nickname(pair[1])

    return button_dictionary
