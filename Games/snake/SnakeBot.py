import random
import pyautogui
import time
from collections import deque
from copy import deepcopy

### Pseudocode to plan logic ###

# Initialize / start game
# Run Loop
#   Locate food (target)
#   Find path
#   Execute path:
#       make a move
#       record new head location
#       wait until square that it just travelled into is blue (reached_square() or something)
#       remove tail square from end of snake
#       

### Functions

# Find Path:
# 

# Needs to know which squares are snake body, when it will be able to go to squares that are currently snake but wont be by the time it gets there

# All gameplay will then be handled by AutoSnake in a while loop, game loop in main class will only continue once autosnake ends
class SnakeBot():
    
    def __init__(self, speed, board):
        
        self.board = board
        self.num_vertical_squares = board.get_board_size()[0]
        self.num_horizontal_squares = board.get_board_size()[1]
        
        # Coordinates of head
        self.head_position = board.get_snake_starting_pos()
        
        # Body var to track the snakes location
        self.body = SnakeBody(board.get_board_size())
        
    
        
    # Main driver function that will run the whole game, only leaves loop when game ends. 
    def run(self):
        
        # Pause for a second then update before beginning
        time.sleep(2)
        self.board.update()
        running = True
        # Run until death
        while(running):
            # time.sleep(0.02)
            self.board.update()
            # Benchmark time for pathfinding (its quick)
            # start_time = time.time()
            path = self.find_route()
            # print(f"Time to find path: {time.time() - start_time:.4f} seconds")
            # print(f"Path Found: {path}")
            
            if (path): # Non-empty path returned, execute
                self.execute_path(path)
            else: # No path found, survie
                survival_path = self.find_survival_route()
                print(f"SURVIVAL MODE! Path: {survival_path}")
                self.execute_survival_path(survival_path)
                
            
    # A function to find a route (of designated length) of moves with the sole purpose of survival; no food is reachable according to find_route()
    def find_survival_route(self):
        # Var for number of moves to make before exiting survival mode:
        num_moves = 4
        starting_position = self.body.get_head()
        
        # print(f"FINDING SURVIVAL ROUTE! Head at: {starting_position}")
        
        # Queue to store current snake and the path recorded so far
        queue = deque([(deepcopy(self.body), [starting_position])]) 
        visited = set()
        visited.add(starting_position)
        
        # Iterate until queue is empty
        while queue:
            # Pop next tile to visit (oldest addition to queue)
            snake, path = queue.popleft()
            current_position = snake.get_head()
            
            # If this tile is food, return path
            if (len(path) >= num_moves):
                return path
            
            # Explore neighbors
            for neighbor in self.board.get_neighbors(current_position):
                # print(neighbor)
                
                # Ensure neighbor is valid target (not visited, not part of the snake, and not an obstacle)
                if (neighbor not in visited) and (neighbor not in snake.get_snake()) and (not self.board.is_obstacle(neighbor)):
                    # Add to visited
                    visited.add(neighbor)
                    # Create new snake and update w/ new head
                    new_snake = deepcopy(snake)
                    new_snake.new_head(neighbor)
                    queue.append((new_snake, path + [neighbor]))
        
    # A function to execute survival path, differs from normal execution because snake doesnt grow at end (no food is eaten)
    def execute_survival_path(self, path):
        # Get starting pos, removes it from path so now 0 element is where we want to go
        current_tile = (0, 0)
        if (path):
            current_tile = path.pop(0)
        
        while path: # Iterate through path until food is reached
            next_tile = path.pop(0)
            direction = self.get_dir(current_tile, next_tile)
            self.execute_move(direction)
            
            # Wait until snake moves into next square before continuing
            self.wait_until_enters(next_tile)
            # Update snake location and current tile
            self.body.new_head(next_tile)
            current_tile = next_tile
            # Short wait to prevent clipping, excluding last move because needs to search
            if not (len(path) == 0):
                time.sleep(0.01)
            
        
        # print("Executed Path Successfully")
    
    # A function to execute the moves of the path in order, grows by one lengths once food is reached
    def execute_path(self, path):
        # Get starting pos, removes it from path so now 0 element is where we want to go
        current_tile = (0, 0)
        if (path):
            current_tile = path.pop(0)
        
        while path: # Iterate through path making moves until empty
            next_tile = path.pop(0)
            direction = self.get_dir(current_tile, next_tile)
            self.execute_move(direction)
            
            # Wait until snake moves into next square before continuing
            self.wait_until_enters(next_tile)
            
            # Update snake location and current tile, unless food
            if (not len(path) == 0):
                self.body.new_head(next_tile)
                current_tile = next_tile
                # Short wait to prevent clipping
                time.sleep(0.01)                
            else: # last element has been popped, this is food tile
                self.body.eat_food(next_tile)
                # print(f"Food ate at: {next_tile}")            
        
        # print("Executed Path Successfully")
            
    # Function to block path execution until snake moves into desired next square
    def wait_until_enters(self, tile):
        while (not self.board.is_snake(tile)):
            self.board.update()
        
            
    
    # Helper function to move in specified direction using pyautogui    
    def execute_move(self, direction):
        print(f"Moving " + direction)
        pyautogui.press(direction)
        
    # Helper function to get relative dir of move to next tile
    def get_dir(self, current_tile, next_tile):
        if next_tile[0] < current_tile[0]: 
            return "up"
        elif next_tile[0] > current_tile[0]:  
            return "down"
        elif next_tile[1] > current_tile[1]:
            return "right"
        elif next_tile[1] < current_tile[1]:
            return "left"
                    
            
    # BFS function that returns a path to food as a list of coordinates, starting from the current head position and ending at the coordinates of the food
    def find_route(self):
        self.board.update()
        food_position = self.board.get_food_pos()
        
        # Will need to create new snake objects during search so as to not modify self.body
        # Record starting head pos
        starting_position = self.body.get_head()
        
        print(f"Searching for path, food at: {food_position}, head at: {starting_position}")
        # print(f"Current snake: {self.body.get_snake()}")
        
        # Queue to store current snake and the path recorded so far
        queue = deque([(deepcopy(self.body), [starting_position])]) 
        visited = set()
        visited.add(starting_position)
        # print(f"Visited at start of search: {visited}")
        
        # Iterate until queue is empty
        while queue:
            # Pop next tile to visit (oldest addition to queue)
            snake, path = queue.popleft()
            current_position = snake.get_head()
            # print(f"Current Position: {current_position}")
            
            # If this tile is food, return path
            if (current_position == food_position):
                return path
            
            # Explore neighbors
            for neighbor in self.board.get_neighbors(current_position):
                # Ensure neighbor is valid target (not visited, not part of the snake, and not an obstacle)
                if (neighbor not in visited) and (neighbor not in snake.get_snake()) and (not self.board.is_obstacle(neighbor)): 
                    # Add to visited
                    visited.add(neighbor)
                    # print(neighbor)
                    # Create new snake and update w/ new head
                    new_snake = deepcopy(snake)
                    new_snake.new_head(neighbor)
                    queue.append((new_snake, path + [neighbor]))
                    
        # If no path is found, return an empty path  
        print("No path found!")
        return []  
        
        
    # Function to create a short list of additional moves, to append to found route to food so as to give time for food to spawn and new path to be found

# Snake Body class, tracks the coordinates corresponding to squares that the snake is currently located in
class SnakeBody:
    def __init__(self, board_size=None):
        self.body = deque()
        
        # Initialize differently depending on board size, if not specified, default to 0
        num_vertical_squares = 0
        if board_size:
            num_vertical_squares = board_size[0] # Base it on corresponding starting pos rel to num vertical, Can just add head location x4 since they will get removed as it moves
            
    
        # print(f"Creating body, num vertical square = {num_vertical_squares}")
        if (num_vertical_squares == 9): # Small board
            self.body.append((4, 2))
            self.body.append((4, 2))
            self.body.append((4, 2))
            self.body.append((4, 2)) # Starting head pos
            
        elif (num_vertical_squares == 15): # Med board
            self.body.append((7, 3))
            self.body.append((7, 3))
            self.body.append((7, 3))
            self.body.append((7, 3)) # Starting head pos       
            
        elif (num_vertical_squares == 21): # Large board
            self.body.append((10, 5))
            self.body.append((10, 5))
            self.body.append((10, 5))
            self.body.append((10, 5)) # Starting head pos  
            
        else: # If not specified, dont initialize a position
            pass
    
    # Function to update the snake according to a move made
    def new_head(self, coord):
        # Add new head location, remove the oldest entry (tail)
        self.body.append(coord)
        self.body.popleft()
        
    # Function to update snake when food is consumed, grows head by one, leaving tail
    def eat_food(self, coord):
        self.body.append(coord)
        
    # Returns a list of all coordinates currently occupied by snake
    def get_snake(self):
        return list(self.body)
    
    # Returns the coordinates of the current head of the snake
    def get_head(self):
        if self.body:
            return self.body[-1]
        else:
            return None