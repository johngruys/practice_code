import pyautogui


class Guesser():
    
    def __init__(self):
        self.previous_guess = None
    
    def make_guess(self, guess):
        pyautogui.write(guess, interval=0.1)
        pyautogui.press("enter")
        self.previous_guess = guess
        
    def record_guess_results(self, results):
        pass
        