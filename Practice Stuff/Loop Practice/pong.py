import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the window dimensions
width = 400
height = 600

# Create the window
window = pygame.display.set_mode((width, height))

# Set the window title
pygame.display.set_caption('My Simple Pygame Game')

# Game loop
while True:
  # Check for events
  for event in pygame.event.get():
    # Close the game if the user clicks the X button on the window
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  # Update the game logic here
  
  # Clear the screen
  window.fill((0, 0, 0))

  # Draw the game objects here

  # Update the screen
  pygame.display.flip()

