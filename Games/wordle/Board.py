import pyautogui
from Grid import Grid

class Board():
    
    def __init__(self, screen, square_locations):
        self.square_locations = square_locations
        self.screen = screen
        
        # Grid object for storing colors/drawing graphics
        self.grid = Grid(screen)
        
        self.GREEN = (83, 141, 78)
        self.YELLOW = (181, 159, 59)
        self.GRAY = (58, 58, 60)
        self.BLACK = (18, 18, 19)
        
    def reset(self):
        self.grid = Grid(self.screen)
        
        
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
            # print(f"Color of Square {i}: {color}")
            all_colors.append(color)
            
        self.grid.update_colors(all_colors)
        self.draw()
            
    def get_guess_results(self):
        # If no black in list, must be last guess so default to last (+1) index
        first_black_index = 30
        if (self.BLACK in self.grid.square_colors):
            first_black_index = self.grid.square_colors.index(self.BLACK)
            
        guess_colors = self.grid.square_colors[first_black_index - 5: first_black_index]
        translated = []
        for color in guess_colors:
            if (color == self.GRAY):
                translated.append("N")
            elif (color == self.YELLOW):
                translated.append("Y")
            elif (color == self.GREEN):
                translated.append("G")
            
        print(f"Translated results: {translated}")
        return translated
        
        