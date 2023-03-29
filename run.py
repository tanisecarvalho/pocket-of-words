""" Main module of the program. Run all the functions. """
from datetime import datetime
from getpass import getpass
from os import system, name
import sys
import time
import random
import re
import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable, DOUBLE_BORDER
from colorama import init, Fore
import bcrypt

# to autoreset colors back to standart with colorama
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


# Code adapted from GeeksForGeeks: How to clear screen in python?
def clear():
    """
    Clear the screen
    """
    _ = system("cls" if name == "nt" else "clear")


# Code from stackoverflow: Centering Ascii Graphics Python
def center_logo(logo, width):
    """
    Manual centering
    """
    padding = ' '*(width//2)
    parts = [padding[0: (width-len(p))//2+1]+p for p in logo]
    return '\n'.join(parts)


def print_logo():
    """
    Clear screen and print logo in cyan.
    """
    logo = '''
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
                               
    '''
    clear()
    print(Fore.CYAN + center_logo(logo.splitlines(), 80))


def invalid_option_message():
    """
    Print message in red for invalid option.
    It has a time.sleep of 2 seconds before the menu appear again.
    It's called on menu validation.
    """
    print("\n" + Fore.RED + "Invalid option. Please try again.".center(80))
    time.sleep(2)


def exit_program():
    """
    Print logo and exit message.
    Exit system.
    """
    print_logo()
    print("Sad to see you going. Please, come back soon.\n".center(80))
    print("To start again click on the 'RUN PROGRAM' button bellow.".center(80))
    sys.exit(0)


def main_menu():
    """
    Print the main menu.
    Call the print_logo and print the options for the main menu.
    Redirect according to user input.
    """
    menu_options = "[R] to Register | [L] to Login "
    menu_options += "| [G] to Read our Guide | [E] to Exit"
    while True:
        print_logo()
        print("To Start, enter one of the options bellow + Enter".center(80))
        print(Fore.CYAN + menu_options.center(80))
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
            print_guide()
            break
        elif option == "E":
            exit_program()
        else:
            invalid_option_message()


def validate_username(username):
    """
    Check if username is valid.
    Validate if username is alphanumeric and has between 4-10 characters.
    """
    username_pattern = re.compile(r"[\w+]{4,10}$")
    if re.fullmatch(username_pattern, username):
        return True

    return False


def validate_password(password):
    """
    Check if password is valid.
    Validate if username has 8 characters.
    """
    if len(password) < 8:
        print("\n" + Fore.RED +
              "Password must have a minimum of 8 characters.".center(80))
        print("\n" + Fore.RED + "Please, try again!".center(80))
        return False
    return True


def register():
    """
    Create worksheet for the user.
    Require username, password.
    Validate username.
    Validate password.
    """
    while True:
        clear()
        print("\n" + Fore.CYAN + "R E G I S T E R\n".center(80))
        username = input("Username: ")
        if validate_username(username):
            try:
                worksheet = SHEET.add_worksheet(
                    title=username,
                    rows=1000,
                    cols=8)
            except gspread.exceptions.APIError:
                print("\n" + Fore.RED +
                      "Username already in use. Please try again.\n")
                time.sleep(2)
            else:
                while True:
                    password = getpass("Password: ")
                    if validate_password(password):
                        hashed_password = bcrypt.hashpw(
                            password.encode("utf-8"),
                            bcrypt.gensalt())
                        worksheet.append_row(["Username", "Password", "Date"])
                        worksheet.format('A1:C1',
                                         {'textFormat': {'bold': True}})
                        worksheet.append_row([
                            username,
                            hashed_password.decode('utf-8'),
                            str(datetime.now().date())
                            ])
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
                        worksheet.format('A3:H3',
                                         {'textFormat': {'bold': True}})
                        print("\n" + Fore.GREEN +
                              "User created successfully!".center(80))
                        time.sleep(2)
                        return worksheet
        else:
            print("\n" + Fore.RED +
                  "Username must be: alphanumeric and between 4-10 characters."
                  .center(80))
            print("\n" + Fore.RED + "Please, try again!".center(80))
            time.sleep(3)


def logged_menu(worksheet):
    """
    Print the menu after user has logged or registered.
    Redirecters user to the chosen option or shows invalid option message.
    """
    menu_options = "[A] to Add a Word | [R] to Review Words "
    menu_options += "| [L] to See your List | [E] to Exit"
    while True:
        clear()
        print("\n" + Fore.CYAN + "Welcome to Pocket of Words".center(80))
        print("You're now logged in.\n\n".center(80))
        print("Enter one of the options bellow + Enter".center(80))
        print(Fore.CYAN + menu_options.center(80))
        option = getpass("").upper()
        if option == "A":
            add_word(worksheet)
            break
        if option == "R":
            review_words(worksheet)
            break
        if option == "L":
            see_list_of_words(worksheet)
            break
        if option == "E":
            exit_program()

        invalid_option_message()


def login():
    """
    Login user on the system.
    Check if username exists.
    Check if password is the same as registered.
    """
    while True:
        clear()
        print("\n" + Fore.CYAN + "L O G I N\n".center(80))
        username = input("Username: ")
        if validate_username(username):
            try:
                worksheet = SHEET.worksheet(username)
            except gspread.exceptions.WorksheetNotFound:
                print("\n" + Fore.RED +
                      "Username not found. Please try again.\n".center(80))
                time.sleep(2)
            else:
                registered_password = worksheet.acell('B2').value
                while True:
                    password = getpass("Password: ")
                    if validate_password(password):
                        is_password = bcrypt.checkpw(
                            password.encode('utf-8'),
                            registered_password.encode('utf-8')
                            )
                        if is_password:
                            return worksheet

                        print("\n" + Fore.RED +
                              "Wrong Password. Please, try again!\n"
                              .center(80))
        else:
            print("\n" + Fore.RED +
                  "Username must be: alphanumeric and between 4-10 characters."
                  .center(80))
            print("\n" + Fore.RED + "Please, try again!".center(80))
            time.sleep(3)


def print_guide():
    """
    Print the guide on how to use the system.
    """
    clear()
    print("\n" + Fore.CYAN + "G U I D E\n\n".center(80))
    print(Fore.CYAN + "About Us\n\n".center(80))
    guide_description = "Pocket of Words was created to help people"
    guide_description += " who want to learn a new language.\n"
    print(guide_description.center(80))
    print("Here you can add new words that you learnt and review them.\n\n"
          .center(80))
    print(Fore.CYAN + "How to Use\n\n".center(80))
    guide = "1. Register/login with a username and password.\n"
    guide += "2. Enter the new word you learnt.\n"
    guide += "3. Enter a sentence to help you remember the word.\n"
    guide += "4. Enter the translation of the word on your language.\n"
    guide += "5. Now you can add more words, review, delete and see your list."
    print(guide)
    input("\n" + "Press Enter to go back to the menu".center(80))
    print("\n" + "We are redirecting you back to the menu.".center(80))
    time.sleep(2)
    main_menu()


def add_word(worksheet):
    """
    Add a new word to the list.
    Max size for word is 25.
    Max size for sentence and translation is 56.
    """
    clear()
    print("\n" + Fore.CYAN + "A D D  A  W O R D\n".center(80))
    word = ""
    sentence = ""
    translation = ""

    while True:
        word = input("New word: ")
        if len(word) < 2 or len(word) > 25:
            print("\n" + Fore.RED +
                  "Word must have between 2-25 characters. Please, try again!"
                  .center(80) + "\n")
        else:
            break

    while True:
        sentence = input("A sentence to help you remember: ")
        sentence_error_msg = "Sentence must have between 2-56 characters."
        sentence_error_msg += " Please, try again!\n"
        if len(sentence) < 2 or len(sentence) > 56:
            print("\n" + Fore.RED + sentence_error_msg.center(80))
        else:
            break

    while True:
        translation = input("Translation: ")
        translation_error_msg = "Translation must have between 2-56 characters"
        translation_error_msg += ". Please, try again!\n"
        if len(translation) < 2 or len(translation) > 56:
            print("\n" + Fore.RED + translation_error_msg.center(80))
        else:
            break

    try:
        worksheet.append_row([word, sentence, translation, " ", 0, 0, 0, 0])
    except gspread.exceptions.APIError:
        print("An error occurred on adding your word. Please try again.\n")
        time.sleep(2)
        add_word(worksheet)
    else:
        print("\n" + Fore.GREEN + "Word added successfully!".center(80))
        while True:
            option = input(
                "\nWould you like to add another word? (Y/N): ").upper()
            if option == "Y":
                add_word(worksheet)
            elif option == "N":
                print("\n" +
                      "We are redirecting you back to the menu.".center(80))
                time.sleep(2)
                logged_menu(worksheet)
            else:
                invalid_option_message()


def see_list_of_words(worksheet):
    """
    Load the words the user has added.
    Print it on a table.
    Give user the option to delete words.
    """
    clear()
    print("\n" + Fore.CYAN + "L I S T  O F  W O R D S\n".center(80))
    table_of_words = PrettyTable()
    table_of_words.set_style(DOUBLE_BORDER)
    # Get the values from the 3rd row for headers
    list_header = worksheet.row_values(3)
    # Delete the values Sentence, Translation and Date
    del list_header[1:4]
    # Add an ID to the words to facilitate delete
    table_of_words.field_names = ["ID"] + list_header
    list_values = worksheet.get_all_values()[3:]
    index = 0
    for row in list_values:
        del row[1:4]
        index += 1
        row.insert(0, index)
    table_of_words.add_rows(list_values)
    # Align words to the left
    table_of_words.align["Word"] = "l"
    print(table_of_words)
    while True:
        action = input(
            "\nPress Enter to go back to the menu or [D] to delete a word: "
            ).upper()
        if action == "D":
            delete_word(worksheet, index)
        elif action == "":
            print("\n" + "We are redirecting you back to the menu.".center(80))
            time.sleep(2)
            logged_menu(worksheet)
        else:
            invalid_option_message()


def delete_word(worksheet, list_size):
    """
    Delete a word from the user's list.
    """
    while True:
        try:
            word_id = int(input("\nEnter the ID of the word to delete: "))
        except ValueError:
            print("\n" + Fore.RED +
                  f"Please inform a number between 1 - {list_size}."
                  .center(80))
        else:
            if word_id > 0 and word_id <= list_size:
                # Add 3 to word list to match position on the worksheet
                worksheet.delete_rows(word_id+3)
                print("\n" + Fore.GREEN +
                      "Word deleted. We'll now reload your list.".center(80))
                time.sleep(2)
                see_list_of_words(worksheet)
            else:
                print("\n" + Fore.RED +
                      f"Please inform a number between 1 - {list_size}."
                      .center(80))


def review_words(worksheet):
    """
    Ask user for words to review.
    Send list and total words to be selected.
    """
    # Create list starting from the position where words are on the worksheet
    list_of_words = worksheet.get_all_values()[3:]
    index_position = 4
    for word in list_of_words:
        word.append(index_position)
        index_position += 1
    total_words = len(list_of_words)
    while True:
        clear()
        print()
        print("\n" + Fore.CYAN + "R E V I E W  W O R D S\n".center(80))
        try:
            print(f"You have {total_words} words.")
            how_many_words = int(input("How many would you like to review? "))
        except ValueError:
            print("\n" + Fore.RED +
                  f"Please inform a number between 1 - {total_words}."
                  .center(80))
            time.sleep(2)
        else:
            if 0 < how_many_words <= total_words:
                select_words(list_of_words, how_many_words, worksheet)
            else:
                print("\n" + Fore.RED +
                      f"Please inform a number between 1 - {total_words}."
                      .center(80))
                time.sleep(2)


def select_words(list_of_words, total_words, worksheet):
    """
    Select the amount of words informed by the user.
    Choose random words from the list.
    """
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
        answer = input(
            "\nPress [H] for a Hint | [Q] to Quit | or enter your answer: "
            ).upper()
        if answer == "H":
            state = "hint"
        elif answer == "Q":
            print("\n" + "We are redirecting you back to the menu.".center(80))
            time.sleep(2)
            logged_menu(worksheet)
        else:
            clear()
            current_word = print_card(current_word, "answer")
            if answer == current_word[2].upper():
                current_word[6] = int(current_word[6]) + 1
                print(Fore.GREEN + "\n" +
                      "Congratulations! You got it!".center(80))
            else:
                current_word[7] = int(current_word[7]) + 1
                print(Fore.RED + "\n" + "Oh no! Better luck next time!"
                      .center(80))
            worksheet_id = 'A'+str(current_word[8])+':H'+str(current_word[8])
            worksheet.update(worksheet_id, [current_word[:8]])
            input("\n" + "Press [Enter] to go for the next card".center(80))
            state = "initial"
            current_index += 1

    clear()
    print("\n" + Fore.CYAN +
          "Congratulations You reviewed all the cards".center(80))
    input("\n" + "Press Enter to go back to the menu".center(80))
    print("\n" + "We are redirecting you back to the menu.".center(80))
    time.sleep(2)
    logged_menu(worksheet)


def print_card(current_word, state="initial"):
    """
    Print the card for review.
    There are three states:
        initial: Print showing only the word
        hint: Print showing the hint
        answer: Print showing all
    """
    word_index = 0
    CARD_SIZE = 58

    card = ''
    card_sides = ''

    card_content = [current_word[0], "Press [H] to see a hint", "ANSWER"]

    if state == "hint":
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
    print("\n")
    print(center_logo(card_final.splitlines(), 80))

    return current_word


def main():
    """
    Start the program.
    Call main_menu to run the program.
    """
    main_menu()


main()
