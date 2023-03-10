from datetime import datetime
from getpass import getpass
from os import system, name
import sys
import time
import gspread
from google.oauth2.service_account import Credentials
# from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes
# from colorama import init, Fore

# init(autoreset=True)

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
        print("[R] to Register | [L] to Login | [E] to Exit".center(80))
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
                "Correct",	
                "Incorrect",
                "Used Hints"
                ])
            worksheet.format('A3:G3', {'textFormat': {'bold': True}})
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


def add_word(worksheet):
    clear()
    print("A D D  A  W O R D\n")
    word = input("New word: ")
    sentence = input("A sentence to help me remember: ")
    translation = input("Translation: ")
    try:
        worksheet.append_row([word, sentence, translation," ", 0, 0, 0])
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
    print("L I S T  O F  W O R D S\n")
    table_of_words = ColorTable()
    table_of_words = ColorTable(theme=Themes.OCEAN)
    table_of_words.field_names = worksheet.row_values(3)
    table_of_words.add_rows(worksheet.get_all_values()[3:])
    print(table_of_words)
    input("\nPress Enter to go back to the menu\n")
    print("We are redirecting you back to the menu.")
    time.sleep(2)
    logged_menu(worksheet)


def review_words(worksheet):
    total_words = len(worksheet.get_all_values()) - 3
    while True:
        clear()
        print("R E V I E W  W O R D S\n")
        how_many_words = input(f"You have {total_words} words. How many would you like to review? ")
        if how_many_words.isnumeric() and int(how_many_words) > 0 and int(how_many_words) <= total_words:
            print(how_many_words)
            input("words")
            break
        else:
            print(f"Please inform a number between 1 - {total_words}")
            time.sleep(2)
    


def print_card(card_content):
    """
    Prints the card for review
    """
    word_index = 0
    CARD_SIZE = 58

    card = ''
    card_sides = ''

    for i in range(CARD_SIZE):
        card += '-'

    for i in range(10):
        card_sides += '|'
        count_spaces = CARD_SIZE
        if i in (1, 4, 8):
            word = card_content[word_index]
            word_index += 1
            count_spaces = CARD_SIZE - len(word)
            print(word, count_spaces)
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

# print_card(default_card_content)

main_menu()
# worksheet = create_user_worksheet()
# worksheet.append_row(["casa", "Eu moro em uma casa.", "house"])



# print(Fore.CYAN + 'some red text')
# print('automatically back to default color again')
