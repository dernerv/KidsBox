import pygame
import os

class MusicRepo:
    def __init__(self, rootFolder):
        self.rootFolder = rootFolder

    def GetSubFolders(self):
        return [name for name in os.listdir(self.rootFolder)
            if os.path.isdir(os.path.join(self.rootFolder, name))]

    def GetCover(self, foldername):
        subfolder = os.path.join(self.rootFolder, foldername)
        for name in os.listdir(subfolder):
            fileName = os.path.join(subfolder, name)
            if os.path.isfile(fileName):
                if (name.endswith(".png")):
                    return pygame.image.load(fileName)

