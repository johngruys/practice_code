import pygame as py
from PIL import Image
import pyautogui
import time
from mss import mss
import numpy as np


class Board():
    
    def __init__(self, screen, corner_coordinates, size):
        
        # Store screen to allow drawing
        self.screen = screen
        self.corner_coordinates = corner_coordinates
        
        # Colors
        self.GRAY = (58, 58, 60)
        self.GREEN = (162, 209,  73)
        self.LGREEN = (170, 215,  81)
        self.YELLOW = (181, 159, 59)
        self.FOOD_COLOR = (231, 71,  29)
        
        # Need the pixels representing the color of each square (midpoint of each square)
        # Size gives number of squares
        # Default to regular google snake dims
        self.num_vertical_squares = 15
        self.num_horizontal_squares = 17
        
        game_board_height = corner_coordinates[1][1] - corner_coordinates[0][1]
        game_board_width = corner_coordinates[1][0] - corner_coordinates[0][0]
        
        # Snake starting position in google snake
        self.snake_starting_position = (7, 3) # Default medium
        
        # Track the position of the food for use by bot, update location in update function so a search isn't needed each time
        self.food_position = (0, 0)
        
        # Google snake dimensions
        if (size == "Small"):
            self.num_vertical_squares = 9
            self.num_horizontal_squares = 10
            self.snake_starting_position = (4, 2)
        elif (size == "Medium"):
            self.num_vertical_squares = 15
            self.num_horizontal_squares = 17
            self.snake_starting_position = (7, 3)
        elif (size == "Large"):
            self.num_vertical_squares = 21
            self.num_horizontal_squares = 24
            self.snake_starting_position = (10, 5)
            
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
        
        # Using a bbox screenshot to optimize update function, define it here and translate coordinates upon construction to speed up function  
        self.bbox = (self.corner_coordinates[0][0], self.corner_coordinates[0][1], 
                self.corner_coordinates[1][0], self.corner_coordinates[1][1])
    
        for i in range(self.num_vertical_squares):
            row = []
            for j in range(self.num_horizontal_squares):
                midpoint_x = (left_x + half_square_width) + (game_square_width * j)
                midpoint_y = (top_y + half_square_height) + (game_square_height * i)
                midpoint_x = int(midpoint_x)
                midpoint_y = int(midpoint_y)
                # center = (midpoint_x, midpoint_y)
                
                # Translate center for use w/ bbox
                translated_center = (midpoint_x - self.bbox[0], midpoint_y - self.bbox[1])
                row.append(translated_center)
                
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
        
        # print(self.square_colors[0])
        py.display.flip() # Update
                
    def update(self):
        # screenshot the game board
        
        # Using mss for faster screen capture
        with mss() as sct:
            sct_img = sct.grab(self.bbox)
            screenshot = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

        screenshot_np = np.array(screenshot)
        
        
        new_colors = []
        for i in range(self.num_vertical_squares):
            row = []
            for j in range(self.num_horizontal_squares):
                # Center coords now translated to work with bbox from contructor, can use directly
                coords = self.center_coordinates[i][j]
                # Translate grid coordinates
                pixel_color = tuple(screenshot_np[coords[1], coords[0]])
                row.append(pixel_color)
                
                # Update food location if this is food
                if (pixel_color == self.FOOD_COLOR):
                    self.food_position = (i, j)
                    
            new_colors.append(row)
        
        self.square_colors = new_colors
        self.draw_board()
        
    def get_board_size(self):
        return (self.num_horizontal_squares, self.num_vertical_squares)
    
    def get_snake_starting_pos(self):
        return self.snake_starting_position
    
    def get_food_pos(self):
        return self.food_position
    
    # A function that returns the indexes of the neigboring squares to a given tile (y, x) eg top left corner (0, 0)
    def get_neighbors(self, tile):
        tile_x = tile[1]
        tile_y = tile[0]
        neighbor_indexes = []
        # If not on left or top edge
        if (not tile_x == 0):
            neighbor_indexes.append((tile_y, tile_x - 1))
        if (not tile_y == 0):
            neighbor_indexes.append((tile_y - 1, tile_x))
        # If not on right or bottom edge
        if (tile_x < (self.num_horizontal_squares - 2)):
            neighbor_indexes.append((tile_y, tile_x + 1))
        if (tile_y < (self.num_vertical_squares - 2)):
            neighbor_indexes.append((tile_y + 1, tile_x))
            
        return neighbor_indexes
    
    # A function that tells if the given square corresponds to an obstacle (snake or wall) 
    # Since snake color varies, if it is not background color or food color, assume it is obstacle
    def is_obstacle(self, tile):
        obstacle = True
        print(f"Tile 1: {tile[1]}, Tile 0: {tile[0]}")
        color = self.square_colors[tile[1]][tile[0]]
        if (color == self.LGREEN):
            obstacle = False
        elif (color == self.GREEN):
            obstacle = False
        elif (color == self.FOOD_COLOR):
            obstacle = False
        
        return obstacle
        
        
        
        
# if __name__ == "__main__":
#     board = Board("")
#     ["Large", "Normal", [[206, 623], [1716, 1943]]]
                