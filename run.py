from datetime import datetime
from getpass import getpass
from os import system, name
import sys
import time
import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable, DOUBLE_BORDER
from colorama import init, Fore
import random

init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pocket_of_words')

default_card_content = ["WORD", "Here a sentence to help you remember the word.", "ANSWER"]


def clear():
    _ = system("cls" if name == "nt" else "clear")


def center_logo(logo, width):
    """Manual centering"""
    padding =  ' '*(width//2)
    parts = [ padding[0: (width-len(p))//2+1]+p for p in logo]
    return '\n'.join(parts)


def logo():
    logo = ('''
   ___           _        _    
  / _ \___   ___| | _____| |_  
 / /_)/ _ \ / __| |/ / _ \ __| 
/ ___/ (_) | (__|   <  __/ |_  
\/    \___/ \___|_|\_\___|\__| 
                               
                __             
          ___  / _|            
         / _ \| |_             
        | (_) |  _|            
         \___/|_|              
                               
 __    __              _       
/ / /\ \ \___  _ __ __| |___   
\ \/  \/ / _ \| '__/ _` / __|  
 \  /\  / (_) | | | (_| \__ \  
  \/  \/ \___/|_|  \__,_|___/  
                               
    ''')
    clear()
    print(center_logo(logo.splitlines(), 80))


def main_menu():
    while True:
        logo()
        print("Welcome to Pocket of Words\n".center(80))
        print("To Start, press one of the options bellow + Enter".center(80))
        print("[R] to Register | [L] to Login | [G] to Read our Guide | [E] to Exit".center(80))
        option = getpass("").upper()
        if option == "R":
            worksheet = register()
            if worksheet is not None:
                logged_menu(worksheet)
            break
        elif option == "L":
            worksheet = login()
            if worksheet is not None:
                logged_menu(worksheet)
            break
        elif option == "G":
            guide()
            break
        elif option == "E":
            print("Sad to see you going. Please, come back soon.".center(80))
            time.sleep(2)
            sys.exit(0)


def register():
    clear()
    print("R E G I S T E R\n")
    while True:
        username = input("Username: ")
        try:
            worksheet = SHEET.add_worksheet(title=username, rows=1000, cols=8)
        except gspread.exceptions.APIError as e:
            print("Username already in use. Please try again.\n")
        else:
            password = getpass("Password: ")
            worksheet.append_row(["Username", "Password", "Date"])
            worksheet.format('A1:C1', {'textFormat': {'bold': True}})
            worksheet.append_row([username, password, str(datetime.now().date())])
            worksheet.append_row([
                "Word", 
                "Sentence", 
                "Translation", 
                "Date Reviewed", 
                "Reviews", 
                "Used Hints",
                "Correct",	
                "Incorrect"
                ])
            worksheet.format('A3:H3', {'textFormat': {'bold': True}})
            print("\nUser created successfully!")
            time.sleep(2)
            return worksheet

    return None


def logged_menu(worksheet):
    while True:
        clear()
        print("Welcome to Pocket of Words".center(80))
        print("You're now logged in.\n".center(80))
        print("Press one of the options bellow + Enter".center(80))
        print("[A] to Add a Word | [R] to Review Words | [L] to See your List | [E] to Exit"
              .center(80))
        option = getpass("").upper()
        if option == "A":
            add_word(worksheet)
            break
        elif option == "R":
            review_words(worksheet)
            break
        elif option == "L":
            see_list_of_words(worksheet)
            break
        elif option == "E":
            print("Sad to see you going. Please, come back soon.".center(80))
            time.sleep(2)
            sys.exit(0)


def login():
    clear()
    print("L O G I N\n")
    while True: 
        username = input("Username: ")
        try:
            worksheet = SHEET.worksheet(username)
        except gspread.exceptions.WorksheetNotFound as e:
            print("Username not found. Please try again.\n")
        else:
            registered_password = worksheet.acell('B2').value
            while True:
                password = getpass("Password: ")
                if password == registered_password:
                    return worksheet
                else:
                    print("Wrong Password. Please try again.\n")
            break
    return None

def guide():
    clear()
    print("\nG U I D E\n")
    guide = "About Us\n"
    guide += "\nPocket of Words was created to help people who want to learn a new language.\n"
    guide += "Here you can insert new words that you learnt and review them.\n"
    guide += "\nHow to Use\n"
    guide += "\n1. Register with a username and password.\n"
    guide += "2. If you're already registered enter your name and password.\n"
    guide += "3. Enter the new word you learnt.\n"
    guide += "4. Enter a sentence to help you remember the word.\n"
    guide += "5. Enter the translation of the word on your mother tongue.\n"
    guide += "6. Now you can add more words, review, delete, and see a list.\n"
    print(guide.center(80))
    input("\nPress Enter to go back to the menu")
    print("We are redirecting you back to the menu.")
    time.sleep(2)
    main_menu()


def add_word(worksheet):
    clear()
    print("A D D  A  W O R D\n")
    word = input("New word: ")
    sentence = input("A sentence to help me remember: ")
    translation = input("Translation: ")
    try:
        worksheet.append_row([word, sentence, translation," ", 0, 0, 0, 0])
    except gspread.exceptions.APIError as e:
        print("An error occurred on adding your word. Please try again.\n")
        time.sleep(2)
        add_word(worksheet)
    else:
        print("\nWord added successfully!")
        print("Would you like to add another word?")
        option = input("Y/N? ").upper()
        if option == "Y":
            add_word(worksheet)
        else:
            print("We are redirecting you back to the menu.")
            time.sleep(2)
            logged_menu(worksheet)


def see_list_of_words(worksheet):
    clear()
    print("\n")
    print(Fore.CYAN + "L I S T  O F  W O R D S\n".center(80))
    table_of_words = PrettyTable()
    table_of_words.set_style(DOUBLE_BORDER)
    list_header = worksheet.row_values(3)
    del list_header[1:4]
    table_of_words.field_names = ["ID"] + list_header
    list_values = worksheet.get_all_values()[3:]
    index = 0
    for row in list_values:
        del row[1:4]
        index += 1
        row.insert(0, index)       
    table_of_words.add_rows(list_values)
    table_of_words.align["Word"] = "l"
    print(table_of_words)
    action = input("\nPress Enter to go back to the menu or [D] to delete a word: ").upper()
    if action == "D":
        while True:
            word_id = int(input("\nEnter the ID of the word to delete: "))
            if word_id > 0 and word_id <= index:
                worksheet.delete_rows(word_id+3)
                print("Word deleted. We'll now reload your list.")
                time.sleep(2)
                see_list_of_words(worksheet)
            else:
                print(f"Please inform a number between 1 - {index}")
    else:
        print("We are redirecting you back to the menu.")
        time.sleep(2)
        logged_menu(worksheet)


def review_words(worksheet):
    list_of_words = worksheet.get_all_values()[3:]
    i = 4
    for word in list_of_words:
        word.append(i)
        i += 1
    total_words = len(list_of_words)
    while True:
        clear()
        print("R E V I E W  W O R D S\n")
        how_many_words = int(input(f"You have {total_words} words. How many would you like to review? "))
        if how_many_words > 0 and how_many_words <= total_words:
            select_words(list_of_words, how_many_words, worksheet)
            break
        else:
            print(f"Please inform a number between 1 - {total_words}")
            

def select_words(list_of_words, total_words, worksheet):
    chosen_words = random.sample(list_of_words, total_words)
    current_index = 0
    state = "initial"
    
    while current_index < total_words:
        clear()
        if state == "initial":
            current_word = chosen_words[current_index]
            current_word[3] = str(datetime.now().date())
            current_word[4] = int(current_word[4]) + 1

        current_word = print_card(current_word, state)
        answer = input("\nPress [H] for a Hint | [Q] to Quit | or enter your answer: ").upper()
        if answer == "H":
            state = "hint"
        elif answer == "Q":
            print("We are redirecting you back to the menu.")
            time.sleep(2)
            logged_menu(worksheet)
        else:
            clear()
            current_word = print_card(current_word, "answer")
            if answer == current_word[2].upper():
                current_word[6] = int(current_word[6]) + 1
                print("\nCongratulations! You got it!")
            else:
                current_word[7] = int(current_word[7]) + 1
                print("\nOh no! Better luck next time!")
            id = 'A'+str(current_word[8])+':H'+str(current_word[8])
            worksheet.update(id, [current_word[:8]])
            input("\nPress [Enter] to go for the next card")
            state = "initial"
            current_index += 1
            

    print("\nCongratulations You reviewed all the cards", current_index)


def print_card(current_word, state="initial"):
    """
    Prints the card for review
    """
    word_index = 0
    CARD_SIZE = 58

    card = ''
    card_sides = ''

    card_content = [current_word[0], "Here a sentence to help you remember the word.", "ANSWER"]

    if state == "hint" :
        current_word[5] = int(current_word[5]) + 1
        card_content = [current_word[0], current_word[1], "ANSWER"]
    elif state == "answer":
        card_content = [current_word[0], current_word[1], current_word[2]]

    for i in range(CARD_SIZE):
        card += '-'

    for i in range(10):
        card_sides += '|'
        count_spaces = CARD_SIZE
        if i in (1, 4, 8):
            word = card_content[word_index]
            word_index += 1
            count_spaces = CARD_SIZE - len(word)
            for i in range(count_spaces):
                if i == int(count_spaces / 2):
                    card_sides += word
                card_sides += ' '
        elif i == 6:
            card_sides += card
        else:
            for i in range(count_spaces):
                card_sides += ' '
        card_sides += '|\n'

    card_final = ' ' + card + '\n' + card_sides + ' ' + card
    print(card_final.center(80))
    

    return current_word

main_menu()
