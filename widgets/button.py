import pygame as pg


#The button class
class Button():
    def __init__(self, surface, type, pos, size, detail):
        self.surface = surface
        self.type = type
        self.pos = pos
        self.size = size
        self.detail = detail
        self.center = (self.pos[0] + (self.size[0] / 2), self.pos[1] + (self.size[1] / 2))
        # self.text = None

        if self.type == 'rect':
            self.rect = (self.pos, self.size)
        elif self.type == 'img':
            self.img = pg.transform.scale(pg.image.load(self.detail), self.size)

    #Draws the button onto the screen
    def draw(self):
        if self.type == 'rect':
            pg.draw.rect(self.surface, self.detail, self.rect)
        elif self.type == 'img':
            self.surface.blit(self.img, self.pos)
        if self.text != None:
            self.surface.blit(self.text, self.textPos)
    
    #Checks if the mouse_pos is within the Button
    def touching(self, mouse_pos):
        if (mouse_pos[0] > self.pos[0] and mouse_pos[0] < (self.pos[0] + self.size[0])):
            if (mouse_pos[1] > self.pos[1] and mouse_pos[1] < (self.pos[1] + self.size[1])): 			
                return True
            else:
                return False
        else:
            return False
    
    #Adds text to the Button
    def add_text(self, text, textSize, textColor, antiAlias = 0, font='courier'):
        self.actual_text = text
        self.font = pg.font.SysFont(font, textSize)
        self.text = self.font.render(text, antiAlias, textColor)
        size = self.font.size(text)
        z = (size[0] / 2, size[1] / 2)
        self.textPos = (self.center[0] - z[0], self.center[1] - z[1])
    
    #Adds a bevel to the rectangle
    def bevel(self, color, width, sides):
        if 'all' in sides:
            sides = ['top', 'bottom', 'left', 'right']
        if 'top' in sides:
            pg.draw.rect(self.surface, color, (self.pos, (self.size[0], width)))
        if 'left' in sides:
            pg.draw.rect(self.surface, color, (self.pos, (width, self.size[1])))
        if 'bottom' in sides:
            pg.draw.rect(self.surface, color, ((self.pos[0], (self.pos[1] + self.size[1]) - width), (self.size[0], width)))
        if 'right' in sides:
            pg.draw.rect(self.surface, color, (((self.pos[0] + self.size[0]) - width, self.pos[1]), (width, self.size[1])))