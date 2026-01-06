import pygame

import colours


pygame.init()
font = pygame.font.SysFont("dejavuserif", 30, False)

class Button():
  def __init__(self, x, y, height, width, text, colour, func, alternate_draw=None):
    self.x = x
    self.y = y
    self.height = height
    self.width = width
    self.text = text
    self.colour = colour


    # The passed in function that runs when the 
    self.check_pressed = self.make_func(func)


    if alternate_draw is not None:
      self.draw = alternate_draw

  def make_func(self, func):
    def wrapper(self, x, y):
      if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
        func()
    return wrapper

  def draw(self, win):
    pygame.draw.rect(win, colours.BLACK, (self.x, self.y, self.width, self.height))
    pygame.draw.rect(win, self.colour, (self.x+5, self.y+5, self.width-10, self.height-10))
    
    text = font.render(self.text, True, colours.BLACK)
    width = text.get_width()
    height = text.get_height()
    win.blit(text, (self.x - width/2 + self.width/2, self.y - height/2 + self.height/2))
    
  
