import json
import pyautogui
import time
import pygame as py
from Grid import Grid
from Board import Board
from guesser import Guesser
from pynput.mouse import Listener


# # Prevent dpi remapping
# import ctypes
# ctypes.windll.shcore.SetProcessDpiAwareness(0)

### Initialize ###
py.init()
running = True

### Screen (Object) ###
screen_width = 800
screen_height = 1000
screen = py.display.set_mode((screen_width, screen_height))

### Title and Logo ###
py.display.set_caption(" Wordle Solver")
icon = py.image.load("Games/wordle/assets/wordle_logo.png")
py.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (58, 58, 60)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)


# Fonts
button_font = py.font.Font(None, 50)
title_font = py.font.Font(None, 80)


# Objects
Grid = Grid(screen)
guesser = Guesser()

# Calibration variables
calibrated = False
calibration_selected = False
squares_calibrated = False
listener = None
calibration_chosen = "None"
calibration_title_text = "Click on Corresponding Square"
restart_calibration_title_text = "Cick on Play Again"
calibration_title_background_rect = py.Rect(100, 85, 600, 100)

# Screen coordinates for all squares, indexed as in grid class
square_locations = []
restart_location = None

# bool for calibration listener status
listener_on = False

# Buttons
button_color = GRAY
button_hover_color = GREEN
calibrate_rect = py.Rect(200, 200, 400, 150)
calibrate_text = "Calibrate"
load_calibration_rect = py.Rect(200, 400, 400, 150)
load_calibration_text = "Load Previous"
running_rect = py.Rect(200, 400, 400, 150)
running_text = "Solving Wordles"


# Main game vars/objects
turn = 1
won = False
board = None
inital_wait = 2
wait_between_guesses = 2
wait_between_games = 2

# Functions
def draw_button(screen, rect, color, text):
    py.draw.rect(screen, color, rect, border_radius=10)
    rendered_text = button_font.render(text, True, WHITE)
    text_rect = rendered_text.get_rect(center=rect.center)
    screen.blit(rendered_text, text_rect)
    
    
# Function to check for a win
def is_win(results):
    all_green = True
    for result in results:
        if not result == "G":
            all_green = False   
            
    return all_green

# Function to reset after a win or loss
def restart_game():
    global turn
    global won
    print("RESTETTING GAME!!!!!")
    print(f"TURN: {turn}")
    turn = 1
    won = False
    guesser.reset()
    board.reset()
    time.sleep(wait_between_games)
    pyautogui.click(x=restart_location[0], y=restart_location[1])
    Grid.draw_grid()
    time.sleep(inital_wait)
    
    
def start_listener():
    global listener
    listener = Listener(on_click=on_click)
    listener.start()
    
def stop_listener():
    global listener
    if listener is not None:
        listener.stop()
        listener = None
    
# function for pynput calibration event
def on_click(x, y, button, pressed):
    if pressed:
        cursor_position = (x, y)
        # print(f"Mouse clicked at: {cursor_position}")
        square_locations.append(cursor_position)

# Save the calibration just completed to reload later
def save_calibration():
    with open("Games/wordle/assets/saved_configuration.json", "w") as file:
        json.dump(square_locations, file)
        
    restart_location = square_locations.pop()
    create_board(square_locations)
    
    

# Load the stored calibration for use now
def load_calibration():
    with open("Games/wordle/assets/saved_configuration.json", "r") as file:
        square_locations = json.load(file)
        return square_locations
    
# Create a board object, stored in global var
def create_board(square_locations):
    board = Board(screen, square_locations)
    board.update()
    
    
    
while running:
    
    # Initial loop when game started, needs to be calibrated
    if not calibrated:
        
        # Reset screen with background color
        screen.fill(WHITE)
        
        # Selection Screen
        if not calibration_selected:
            # Get mouse position for hover behavior
            mouse_pos = py.mouse.get_pos()
            button_clicked = "None"
            
            
            calibrate_color = button_color
            load_calibration_color = button_color
            # Check pos for hover color
            if calibrate_rect.collidepoint(mouse_pos):
                calibrate_color = button_hover_color
            if load_calibration_rect.collidepoint(mouse_pos):
                load_calibration_color = button_hover_color
                
            
            # Event handling
            for event in py.event.get():
                if event.type == py.MOUSEBUTTONDOWN:
                    if calibrate_rect.collidepoint(mouse_pos):
                        calibration_chosen = "calibrate"
                        calibration_selected = True
                    elif load_calibration_rect.collidepoint(mouse_pos):
                        calibration_chosen = "load"
                        calibration_selected = True
            
                # Closing Window #
                if event.type == py.QUIT:
                    running = False
                    
            # Draw buttons
            draw_button(screen, calibrate_rect, calibrate_color, calibrate_text)
            draw_button(screen, load_calibration_rect, load_calibration_color, load_calibration_text)
                       
            py.display.flip()
            
        else:
            # Calibrate button selected, run calibration
            if calibration_chosen == "calibrate":
                
                # Loop for calibrating squares, after this needs to calibrate play again button
                if not squares_calibrated:
                
                    # Draw title/instructions
                    draw_button(screen, calibration_title_background_rect, YELLOW, calibration_title_text)
                    
                    # Current index of square to calibrate given by len of list storing them
                    # eg. len 2 means index 2 needs to be stored next
                    current_calibration_square = len(square_locations)
                    
                    
                    # Draw corresponding grid
                    Grid.draw_calibration_grid(current_calibration_square)
                    
                    # pynput mouse listener for calibration
                    if not listener_on:
                        start_listener()
                        listener_on = True
                        
                    # Once len is 30, end calibration of squares
                    if (current_calibration_square >= 30):
                        squares_calibrated = True
                        # listener_on = False
                        # stop_listener()
                        
                        
                else:
                    # Squares calibrate, needs location of play again button
                    # Draw title/instructions
                    draw_button(screen, calibration_title_background_rect, YELLOW, restart_calibration_title_text)
                    
                    if (len(square_locations) >= 31):
                        save_calibration()
                        calibrated = True
                    
                    
                    
                # Event Handling
                for event in py.event.get():
                    # Pynput used for calibration clicks, see function above game loop
                    # Closing Window #
                    if event.type == py.QUIT:
                        running = False

                py.display.flip()

            else:
                # Load calibration from previous save
                locations = load_calibration()
                restart_location = locations.pop()
                square_locations = locations
                calibrated = True
                board = Board(screen, square_locations)
                board.update()
    
    else:
        # Calibration completed at this point
        # This is Main game loop 
        draw_button(screen, load_calibration_rect, load_calibration_color, load_calibration_text)
        if (won == False):
            # board.update()
            # First Guess:
            if (turn == 1):
                board.update()
                # Wait for game to load
                time.sleep(inital_wait)
                
                # Make initial guess
                guesser.make_guess()
                time.sleep(wait_between_guesses)
                board.update()
                
                results = board.get_guess_results()
                
                # print(f"Previous guess results: {results}")
                # Send results to guesser
                guesser.record_guess_results(results)
                
                # Check for win
                if (is_win(results)):
                    won = True
                    restart_game()
                
                # Not won, continue
                turn += 1
                
            else:
                # Not first turn, dont need initial wait
                if (turn <= 7):
                    guesser.make_guess()
                    time.sleep(wait_between_guesses)
                    board.update()
                    results = board.get_guess_results()
                    print(f"Results of last guess: {results}")
                    
                    guesser.record_guess_results(results)
                    
                    # Check for win
                    if (is_win(results)):
                        won = True
                        restart_game()
                        
                    # Not won, continue
                    turn += 1
                    
                else:
                    # Used 6 turns, loss
                    restart_game() 
                    
                
                
                
                
                
                
                
            
        
            
        
    
    ### User Input in main loop ###
    for event in py.event.get():

        if event.type == py.KEYDOWN:
            pass
        
        # Closing Window #
        if event.type == py.QUIT:
            running = False

    ### Update ###
    # clock.tick(60)
    py.display.update()
