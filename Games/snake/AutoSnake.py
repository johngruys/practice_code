from collections import deque
import pyautogui
import time

# Autosnake object will be called once game begins in main class
# All gameplay will then be handled by AutoSnake in a while loop, game loop in main class will only continue once autosnake ends
class AutoSnake():
    
    def __init__(self, speed, board):
        
        self.board = board
        
        # Google snake params
        self.initial_length = 4
        self.length_increment = 1
        self.speed = speed
        
        # Need a wait time between moves, based on snake speed, (might need asjusted)
        self.wait_between_moves = 0.129 # Default to normal
        if (speed == "Slow"):
            self.wait_between_moves = 0.175
        elif (speed == "Normal"):
            self.wait_between_moves = 0.129
        elif (speed == "Fast"):
            self.wait_between_moves = 0.86
        
        
        # Need coordinates of head
        self.head_position = board.get_snake_starting_pos()
        
        self.num_horizontal_squares = board.get_board_size()[0]
        self.num_vertical_squares = board.get_board_size()[1]
        
    # Main driver function that will run the whole game, only leaves loop when game ends. 
    def run(self):
        running = True
        self.board.update()
        time.sleep(2)
        while (running):
            print("Looping!")
            # Each iteration of this loop constitues one path executed, so need a new path at the start of each loop
            current_postion = self.head_position
            food_position = self.board.get_food_pos()
            path = self.find_path(current_postion, food_position)
            self.execute_path(path)
            self.board.update()
            
        

        
        
    # BFS Function to find shortest path
    def find_path(self, head_pos, food_position):
        # Queue to store current pos and the path recorded so far
        queue = deque([(head_pos, [])]) 
        visited = set()
        visited.add(head_pos)
        
        while queue:
            # Pop next tile to visit
            (current_y, current_x), path = queue.popleft()
            
            # If this tile is food, return path
            if (current_y, current_x) == food_position:
                # print(path + [(current_y, current_x)])
                return path + [(current_y, current_x)]
            
            # Explore neighbors
            for neighbor in self.board.get_neighbors((current_y, current_x)):
                print(neighbor)
                # Ensure valid (Not visited and not obstacle)
                if neighbor not in visited and not self.board.is_obstacle(neighbor):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        # If no path is found, return an empty path  
        return []          
    
    # Function to execute the path moves using pynput
    def execute_path(self, path):
        print("Starting path execution")
        # Num steps needed to execute
        steps = len(path)   
        ending_square = path[len(path) - 1]
        
        # Immediately execute first move
        dir = self.get_dir(path[0], path[1])
        self.execute_move(dir)
        
        # Iterate through rest of moves, pausing between
        for i in range(1, steps - 1): # Skip first move, 
            current_tile = path[i]
            next_tile = path[i + 1]
            dir = self.get_dir(current_tile, next_tile)
            self.execute_move(dir)
            time.sleep(self.wait_between_moves)
            
        # Update snake head position at the end of execution
        self.head_position = ending_square
        print("Path execution ended")
            
    def execute_move(self, direction):
        if (direction == "Up"):
            pyautogui.press('up')
        elif (direction == "Down"):
            pyautogui.press('down')
        elif (direction == "Left"):
            pyautogui.press('left')
        else:
            pyautogui.press('right')
        
    # Helper function to get relative dir of move to next tile
    def get_dir(self, current_tile, next_tile):
        
        if next_tile[0] < current_tile[0]: 
            return "Up"
        elif next_tile[0] > current_tile[0]:  
            return "Down"
        elif next_tile[1] > current_tile[1]:
            return "Right"
        elif next_tile[1] < current_tile[1]:
            return "Left"
            
        
        
