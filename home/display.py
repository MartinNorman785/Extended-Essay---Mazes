import pygame

from button import Button
import colours
from grid import Grid


def main(grid=None):
  # Initialising pygame
  pygame.init()
  

  # Initialsing the buttons on the grid
  buttons = [
    #Button(50, 20, 50, 200, "New Game", colours.GRAY, lambda: grid.grid_reset())
  ]
  if grid is None:
    grid = Grid(100, 50)

  win = pygame.display.set_mode((1000*(5)+300,500*(5)+200))

  # Main loop
  run = True
  while run:

    grid.draw_main(win)


    for button in buttons:
      button.draw(win)
      
    
    # Checking for user input
    for event in pygame.event.get():
      
      # If pygame is closed
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        run = False
        pygame.quit()
        
      # If a location is pressed
      if event.type == pygame.MOUSEBUTTONDOWN:
        mousepos = pygame.mouse.get_pos()
        for button in buttons:
          button.check_pressed(button, mousepos[0], mousepos[1])

    # Processing the updates to the display
    pygame.display.update()
  pygame.quit()



if __name__ == "__main__":
  # Running the main code
  main()
