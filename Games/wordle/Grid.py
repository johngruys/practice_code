import pygame as py

class Grid():
    
    def __init__(self, screen):
        
        # Pass screen variable to allow draw functions to work
        self.screen = screen
        
        # Colors
        self.GRAY = (58, 58, 60)
        self.GREEN = (83, 141, 78)
        self.YELLOW = (181, 159, 59)
        
        # Grid creation parameters
        square_width = 100
        square_dimensions = (square_width, square_width)
        square_gap = 13
        horizontal_padding = 124
        vertical_padding = 260
        
        # Create a list of the squares for the grid
        self.squares = []
        for i in range(6):
            for j in range(5):
                x_coord = horizontal_padding + ((square_width + square_gap) * j)
                y_coord = vertical_padding + ((square_width + square_gap) * i)
                # coords.append((x_coord, y_coord))
                square_coords = (x_coord, y_coord)
                self.squares.append(py.Rect(square_coords, square_dimensions))
        
        self.square_colors = []
        for i in range(30):
            self.square_colors.append(self.GRAY)
            
        self.defualt_colors = self.square_colors
        
        
    # Function to draw a calibration grid, passed an integer representing current square
    # that is being selected, that square is drawn with a different color to highlight it
    def draw_calibration_grid(self, current_square):
        # Iterate through all squares
        for i in range(30):
            color = self.GRAY
            # If square is the one being calibrated, make it green
            if (i == current_square):
                color = self.GREEN
            py.draw.rect(self.screen, color, self.squares[i])
            
    def draw_grid(self):
        # Iterate through all squares
        for i in range(30):
            py.draw.rect(self.screen, self.square_colors[i], self.squares[i])
            
    def update_colors(self, new_colors):
        self.square_colors = new_colors
        
    
        
if __name__ == "__main__":
    grid = Grid(0)