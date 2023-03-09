from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

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

def create_user_worksheet():
    while True:
        username = input("Username: ")
        try:
            worksheet = SHEET.add_worksheet(title=username, rows=1000, cols=8)
        except gspread.exceptions.APIError as e:
            print("Username already in use")
        else:
            password = input("Passowrd: ")
            worksheet.append_row(["Username", "Password", "Date"])
            worksheet.format('A1:C1', {'textFormat': {'bold': True}})
            worksheet.append_row([username, password, str(datetime.now().date())])
            worksheet.append_row(["word", "sentence", "translation", "date reviewed", "reviews", "correct",	"incorrect"])
            worksheet.format('A3:G3', {'textFormat': {'bold': True}})
            print("User created successfully!")
            return worksheet


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

create_user_worksheet()
