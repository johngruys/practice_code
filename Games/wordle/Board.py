import pyautogui
from Grid import Grid

class Board():
    
    def __init__(self, screen, square_locations):
        self.square_locations = square_locations
        
        # Grid object for storing colors/drawing graphics
        self.grid = Grid(screen)
        
        self.GRAY = (0, 0, 0)
        
        
    def get_color(self, coords):
        color = pyautogui.pixel(coords[0], coords[1])
        # print(f"Color at {coords}: {color}")
        return color
        
        
    def draw(self):
        self.grid.draw_grid()
    
    def update(self):
        # Iterate through all squares, checking and updating colors
        all_colors = []
        for i in range(30):
            coords = self.square_locations[i]
            color = self.get_color(coords)
            print(f"Color of Square {i}: {color}")
            all_colors.append(color)
            
        self.grid.update_colors(all_colors)
        self.draw()
            
        
        