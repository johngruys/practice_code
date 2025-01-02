import pygame as py
from PIL import ImageGrab
import pyautogui
import time

class Board():
    
    def __init__(self, screen, corner_coordinates, size):
        
        # Store screen to allow drawing
        self.screen = screen
        self.corner_coordinates = corner_coordinates
        
        # Colors
        self.GRAY = (58, 58, 60)
        self.GREEN = (83, 141, 78)
        self.LGREEN = (78, 160, 70)
        self.YELLOW = (181, 159, 59)
        
        # Need the pixels representing the color of each square (midpoint of each square)
        # Size gives number of squares
        # Default to regular google snake dims
        self.num_vertical_squares = 15
        self.num_horizontal_squares = 17
        
        game_board_height = corner_coordinates[1][1] - corner_coordinates[0][1]
        game_board_width = corner_coordinates[1][0] - corner_coordinates[0][0]
        
        # Google snake dimensions
        if (size == "Small"):
            self.num_vertical_squares = 9
            self.num_horizontal_squares = 10
        elif (size == "Medium"):
            self.num_vertical_squares = 15
            self.num_horizontal_squares = 17
        elif (size == "Large"):
            self.num_vertical_squares = 21
            self.num_horizontal_squares = 24
            
        game_square_height = game_board_height / self.num_vertical_squares
        game_square_width = game_board_width / self.num_horizontal_squares
        
        # Create a list of lists containing coordinates of center pixel of each square, [0][0] is top left square
        self.center_coordinates = []
        # half height/width for first center paddings
        half_square_height = game_square_height/2
        half_square_width = game_square_width/2
        # Edges
        left_x = corner_coordinates[0][0]
        top_y = corner_coordinates[0][1]
    
        for i in range(self.num_vertical_squares):
            row = []
            for j in range(self.num_horizontal_squares):
                midpoint_x = (left_x + half_square_width) + (game_square_width * j)
                midpoint_y = (top_y + half_square_height) + (game_square_height * i)
                midpoint_x = int(midpoint_x)
                midpoint_y = int(midpoint_y)
                center = (midpoint_x, midpoint_y)
                row.append(center)
                
            self.center_coordinates.append(row)
            
        # Also need a list of rects to be the classes own representation of the board for display
        # Grid creation parameters
        square_width = 800/self.num_horizontal_squares
        square_dimensions = (square_width, square_width)
        horizontal_padding = 200
        vertical_padding = 500
        self.squares = []
        for i in range(self.num_vertical_squares):
            row = []
            for j in range(self.num_horizontal_squares):
                x_coord = horizontal_padding + (square_width * j)
                y_coord = vertical_padding + (square_width * i)
                
                square_coords = (x_coord, y_coord)
                row.append(py.Rect(square_coords, square_dimensions))
            
            self.squares.append(row)
                
                
        self.square_colors = []
        for i in range(self.num_vertical_squares):
            row = []
            for j in range(self.num_horizontal_squares):
                if (i % 2 == 0):
                    if (j % 2 == 0):
                        row.append(self.GREEN)
                    else:
                        row.append(self.LGREEN)
                else:
                    if (j % 2 == 0):
                        row.append(self.LGREEN)
                    else:
                        row.append(self.GREEN)
                    
                
            self.square_colors.append(row)
                
    def check_center_coords(self):
        for row in self.center_coordinates:
            for center in row:
                pyautogui.moveTo(center[0], center[1])
                time.sleep(0.01)
                
        time.sleep(10)
                
    def draw_board(self):
        # Iterate through every square and draw it
        for i in range(self.num_vertical_squares):
            for j in range(self.num_horizontal_squares):
                py.draw.rect(self.screen, self.square_colors[i][j], self.squares[i][j])
                
    def update(self):
        # screenshot the game board
        bbox = (self.corner_coordinates[0][0], self.corner_coordinates[0][1], 
                self.corner_coordinates[1][0], self.corner_coordinates[1][1])
        screenshot = ImageGrab.grab(bbox)
        pixels = screenshot.load()
        
        new_colors = []
        for i in range(self.num_vertical_squares):
            row = []
            for j in range(self.num_horizontal_squares):
                coords = self.center_coordinates[i][j]
                # Translate grid coordinates
                pixel_color = pixels[coords[0] - bbox[0], coords[1] - bbox[1]]
                row.append(pixel_color)
            new_colors.append(row)
        
        self.square_colors = new_colors
        self.draw_board()
                