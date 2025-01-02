import pyautogui
import random

class Guesser():
    
    def __init__(self):
        self.initial_guess = "audio"
        self.previous_guess = None
        
        
        # Load in words from txt file
        self.all_words = []
        with open("Games/wordle/assets/answers.txt", "r") as file:
            self.all_words = file.readlines()
            
        # Clean words
        self.all_words = [word.strip() for word in self.all_words]
        
        self.possible_answers = self.all_words
        
        self.wrong_letters = []
        self.right_letter_wrong_pos = []
        self.right_letters = []
        self.letters_in_word = []
        
    # Reset the guesser between rounds to get ready for next game
    def reset(self):
        self.previous_guess = None
        self.possible_answers = self.all_words
        self.wrong_letters.clear()
        self.right_letter_wrong_pos.clear()
        self.right_letters.clear()
        self.letters_in_word.clear()
    
    
    # Function to execute a guess
    def make_guess(self):
        # Call helper function to get a guess
        guess = self.find_guess()
        
        # Write and store guess
        pyautogui.write(guess, interval=0.02)
        pyautogui.press("enter")
        self.previous_guess = guess
        
    # Function to choose what word to guess
    def find_guess(self):
        # If first guess, default guess
        if (self.previous_guess == None):
            return self.initial_guess
        else:
            # Not first turn, need to find a word
            updated_possible_answers = []
            
            # Iterate through all words and see if it qualifies
            for word in self.possible_answers:
                
                # Check correct letters first to quickly eliminate words
                for right_letter in self.right_letters:
                    letter = right_letter[0]
                    index = right_letter[1]
                    if (word[index] != letter):
                        break
                else:
                    # If no break occured, check for correct letters in wrong pos
                    for misplaced in self.right_letter_wrong_pos:
                        letter = misplaced[0]
                        index = misplaced[1]
                        if (word[index] == letter):
                            break
                        elif (letter not in word):
                            break
                        
                    else: 
                        # No break occured, verify word doesn't contain known wrong letter, costly loop so run last
                        for letter in word:
                            if letter in self.wrong_letters:
                                break
                        else:
                            # Passes all checks, add to valid words
                            updated_possible_answers.append(word)
                            # print(f"Possible word found: {word}")
                            continue
                        
                # If a break was hit, continue to next word
                continue
            
            # Update possible answers
            self.possible_answers = updated_possible_answers
            # Return random word from possible answers
            if (len(self.possible_answers) > 0):
                return random.choice(self.possible_answers)
            else:
                return None
        
        
    def record_guess_results(self, results):
        for i in range(len(results)):
            
            result = results[i]
            # print(f"Result: {result}")
            letter = self.previous_guess[i]
            # Add record to lists
            if (result == "N"):
                # Letter not in answer
                self.wrong_letters.append(letter)
            elif (result == "Y"):
                # Letter in answer but unknown location, not in current pos tho
                self.right_letter_wrong_pos.append((letter, i))
                self.letters_in_word.append(letter)
                
            elif (result == "G"):
                # Letter in correct pos
                self.right_letters.append((letter, i))
                self.letters_in_word.append(letter)
                
        # Need to iterate through right letters and ensure they arent also in wrong letters
        # bc if it guesses a word with a repeat letter, one may be grey even though there is one in the right word
        for letter in self.letters_in_word:
            if letter in self.wrong_letters:
                self.wrong_letters.remove(letter)
                        
        # print(f"Wrong letters: {self.wrong_letters}")
        # print(f"Right letter wrong place: {self.right_letter_wrong_pos}")
        # print(f"Right letters right place: {self.right_letters}")

        