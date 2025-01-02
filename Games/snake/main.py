import pygame as py
import random
import time
import pyautogui
import keyboard
from pynput.mouse import Listener
import json
from board import Board


### Initialize ###
py.init()
running = True

### Screen (Object) ###
screen_width = 1200
screen_height = 1600
screen = py.display.set_mode((screen_width, screen_height))

### Title and Logo ###
py.display.set_caption(" Snake Bot")

icon = py.image.load("Games/snake/Assets/snake.png")
py.display.set_icon(icon)

### Background ###
# background = py.image.load("Games/snake/Assets/background.png")


### Clock ###
clock = py.time.Clock()


# Colors #
WHITE = (254, 255, 236)
BLACK = (0, 0, 0)
GRAY = (58, 58, 60)
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
LBLUE = (0, 255, 255)
BLUE = (0, 0, 255)
TAN = (200, 180, 140)

# Fonts
button_font = py.font.Font(None, 50)
title_font = py.font.Font(None, 80)

# Buttons
button_color = GRAY
button_hover_color = GREEN
calibrate_rect = py.Rect(300, 200, 600, 200)
calibrate_text = "Calibrate"
load_calibration_rect = py.Rect(300, 500, 600, 200)
load_calibration_text = "Load Previous"


# Calibration
calibrated = False
calibration_selected = False
space_bar_pressed = False

input_board_size = None
input_snake_speed = None
# List to store top left and bottom right corners
corner_coordinates = []
# List to store all cal vars - for ease of save
calibration_variables = []

# Game vars
board = None



# Functions
def draw_button(screen, rect, color, text):
    py.draw.rect(screen, color, rect, border_radius=10)
    rendered_text = button_font.render(text, True, WHITE)
    text_rect = rendered_text.get_rect(center=rect.center)
    screen.blit(rendered_text, text_rect)
    
def draw_title(screen, rect, color, text):
    py.draw.rect(screen, color, rect, border_radius=10)
    rendered_text = title_font.render(text, True, WHITE)
    text_rect = rendered_text.get_rect(center=rect.center)
    screen.blit(rendered_text, text_rect)
    
    

# Calibration Functions

# Function to select board size
def select_board_size():
    # print("Board select function called")
    select_board_rect = py.Rect(300, 180, 600, 180)
    select_board_text = "Select Board Size"
    instructions_rect = py.Rect(350, 420, 500, 150)
    incstructions_text = "S-M-L || Return to Confirm"
    selected_rect = py.Rect(350, 620, 500, 150)
    selected_text = "Selected: "
    
    board_size = "None"
    board_size_selected = False
    
    # Loop until board size confirmed
    while not board_size_selected:
        # Fill background color
        screen.fill(WHITE)
        
        draw_title(screen, select_board_rect, GREEN, select_board_text)  
        draw_button(screen, instructions_rect, GRAY, incstructions_text)
        current_selection_text = selected_text + board_size
        draw_title(screen, selected_rect, GRAY, current_selection_text)
        
        # Event handling
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_s:
                    board_size = "Small"
                if event.key == py.K_m:
                    board_size = "Medium"
                if event.key == py.K_l:
                    board_size = "Large"
                if event.key == py.K_RETURN:
                    if (not board_size == "None"):
                        board_size_selected = True
                    
            # Closing Window #
            if event.type == py.QUIT:
                board_size_selected = True
                
        py.display.flip()
        py.display.update()
            
    return board_size
        
        
# Function to select board size
def select_snake_speed():
    # print("Speed select function called")
    select_speed_rect = py.Rect(300, 180, 600, 180)
    select_speed_text = "Select Snake Speed"
    instructions_rect = py.Rect(350, 420, 500, 150)
    incstructions_text = "S-N-F || Return to Confirm"
    selected_rect = py.Rect(350, 620, 500, 150)
    selected_text = "Selected: "
    
    speed = "None"
    speed_selected = False
    
    # Loop until board size confirmed
    while not speed_selected:
        # Fill background color
        screen.fill(WHITE)
        
        draw_title(screen, select_speed_rect, GREEN, select_speed_text)
        draw_button(screen, instructions_rect, GRAY, incstructions_text)
        current_selection_text = selected_text + speed
        draw_title(screen, selected_rect, GRAY, current_selection_text)
        
        # Event handling
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_s:
                    speed = "Slow"
                if event.key == py.K_n:
                    speed = "Normal"
                if event.key == py.K_f:
                    speed = "Fast"
                if event.key == py.K_RETURN:
                    if (not speed == "None"):
                        speed_selected = True
                    
            # Closing Window #
            if event.type == py.QUIT:
                speed_selected = True
                
        py.display.flip()
        py.display.update()
            
    return speed

# Function to get coordinates of corners
listener_on = False
def calibrate_corners():
    # print("Speed select function called")
    select_corners_rect = py.Rect(300, 180, 600, 180)
    select_corners_text = "Calibrate Corners"
    instructions_1_rect = py.Rect(350, 420, 500, 60)
    instructions_2_rect = py.Rect(350, 460, 500, 60)
    instructions_1_text = "Activate snake window"
    instructions_2_text = "then press space to begin"
    select_now_rect = py.Rect(350, 620, 500, 150)
    select_now_text = "Select Now"
    
    corners_selected = False
    
    # Input vars
    listener = None
    
    # Loop until board size confirmed
    while not corners_selected:
        # Fill background color
        screen.fill(WHITE)
        
        draw_title(screen, select_corners_rect, YELLOW, select_corners_text)
        draw_button(screen, instructions_1_rect, GRAY, instructions_1_text)
        draw_button(screen, instructions_2_rect, GRAY, instructions_2_text)
        
        
        # Detect space bar and prompt clicks once detected
        detect_global_space_press()
        if listener_on:
            draw_title(screen, select_now_rect, GREEN, select_now_text)
            draw_title(screen, select_corners_rect, GREEN, select_corners_text)
    
    
        # Event handling
        for event in py.event.get():
                                                
            # Closing Window #
            if event.type == py.QUIT:
                corners_selected = True
                
        if (len(corner_coordinates) >= 2):
            corners_selected = True
                
        py.display.flip()
        py.display.update()
        
    stop_listener()
    print(corner_coordinates)
    return None

# Helper functions for corner calibration
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
        corner_coordinates.append(cursor_position)
        
def detect_global_space_press():
    global listener_on
    if keyboard.is_pressed("space"):
        if (listener_on == False):
            listener_on = True
            start_listener()
    
def load_calibration():
    global calibrated
    global board
    # Extract params from save and load into correct vars
    tmp_calibration_variables = None
    with open("Games/snake/assets/saved_configuration.json", "r") as file:
        calibration_variables = json.load(file)
        tmp_calibration_variables = calibration_variables
    
    corner_coordinates = tmp_calibration_variables.pop()
    input_snake_speed = tmp_calibration_variables.pop()
    input_board_size = tmp_calibration_variables.pop()
    print(f"Board Size: {input_board_size} || Snake Speed: {input_snake_speed} || Corners: {corner_coordinates}")
    calibrated = True
    board = Board(screen, corner_coordinates, input_board_size)

def save_calibration():
    # Add calibrated parameters to list and save it
    global calibrated
    global board
    
    calibration_variables.append(input_board_size)
    calibration_variables.append(input_snake_speed)
    calibration_variables.append(corner_coordinates)
    with open("Games/snake/assets/saved_configuration.json", "w") as file:
        json.dump(calibration_variables, file)
        
    calibrated = True
    board = Board(screen, corner_coordinates, input_board_size)

while running:
    
    # Fill background at start of each frame
    screen.fill(WHITE)
    
    # Initial loop when game started, needs to be calibrated
    if not calibrated:
        
        # Reset screen with background color
        # screen.fill(WHITE)
        
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
            draw_title(screen, calibrate_rect, calibrate_color, calibrate_text)
            draw_title(screen, load_calibration_rect, load_calibration_color, load_calibration_text)
                       
            py.display.flip()
            
        else:
            # Calibration selected, either calibrate or load
            if calibration_chosen == "load":
                calibration = load_calibration()
                
            elif calibration_chosen == "calibrate":
                input_board_size = select_board_size()
                input_snake_speed = select_snake_speed()
                calibrate_corners()
                
                print(f"Board Size: {input_board_size} || Snake Speed: {input_snake_speed} || Corners: {corner_coordinates}")
                
                # Calibration complete, save and continue
                save_calibration()
                
    else:
        # Calibration complete/loaded, game loop here
        board.update()
        py.display.flip()
        
                
    

    ### Event Handling for Quitting ###
    for event in py.event.get():
        # Closing Window #
        if event.type == py.QUIT:
            running = False

    ### Update !!! ###
    clock.tick(60)
    py.display.update()