# Pocket of Words - TESTING

### Deployed Site: [Pocket of Words](https://pocket-of-words.herokuapp.com/)

![Main](docs/main.JPG)

---

## CONTENTS

* [AUTOMATED TESTING](#automated-testing)
  * [Jigsaw Validator](#jigsaw-validator)
  * [CI Python Linter](#ci-python-linter)
  * [Lighthouse](#lighthouse)

* [MANUAL TESTING](#manual-testing)
  * [Testing User Stories](#testing-user-stories)
  * [Full Testing](#full-testing)

* [BUGS](#bugs)
  * [Known Bugs](#known-bugs)

Testing was realised during the whole development of this project. Chrome Devtools was the primary tool utilised in this process. 

Additionally, since the quiz became functional, the site was deployed. The link was shared with friends and family to get their constant feedback towards the functionalities, design and accessibility.

---

## AUTOMATED TESTING

### Jigsaw Validator

As I added some CSS to style the layout.html page, I ran the [Jigsaw Validator](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fpocket-of-words.herokuapp.com%2F&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en) on the project.

![CSS Validation](docs/testing/css-validator.JPG)

### CI Python Linter

No errors were found when passing through [CI Python Linter](https://pep8ci.herokuapp.com/). However, some warnings regarding whitespace and invalid escape have shown on the result between lines 53-70. They don't affect the functionality of this program, they are actually necessary to make the logo display correctly.

![Python Validation](docs/testing/python-validator.JPG)

### Lighthouse

I used Chrome Developer Tools' Lighthouse to test the Performance, Accessibility, Best practices and SEO of the project. The low score on SEO is regarding the lack of the meta tag description.

![Lighthouse](docs/testing/lighthouse.JPG)

---

## MANUAL TESTING

### Testing User Stories

| Goals | How are they achieved? |
| :--- | :--- | 
| I want to create an account. | The program gives the user the option to create an account. | 
| I want to see a guide on how to use the program. | The program gives the user the option to see the guide. | 
| I want to log in on my account. | The program gives the user the option to log in on their account. | 
| I want to exit the program. | The program gives the user the option to exit the program. | 
| I want to add a new word. | After the login the user can add words to their 'pocket'. | 
| I want to see a list of my words. | After the login the user has the option to see the list with all their words. | 
| I want to delete a word. | When seeing the list of words the user has the option to delete a word. | 
| I want to review my words. | After the login the user has the option to review their words. | 
| I want to quit before review all the words. | While reviewing the words, the user has the option to quit the review before finish. | 
| I want to choose how many words to review. | When the user select the option to review the words, the program will display how many words they have added and give the user the option to choose how many words to review. |
| I want to know if my word is correct/incorrect. | When reviewing the words the system will display if the user guessed the word correct or not. |


### Features Testing

`Main Menu`

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Register | Open the Register Section | Press R + Enter | Opens the Register Section | Pass |
| Login | Open the Login Section | Press L + Enter | Opens the Login Section | Pass |
| Guide | Open the Guide Section | Press G + Enter | Opens the Guide Section | Pass |
| Exit | Open the Exit Message | Press E + Enter | Opens the Exit Message | Pass |
| None of the Options on the Menu | Display invalid option message | Press Any other key + Enter or only Enter | Displays invalid option message | Pass |
|  |  |  |  |  |

Display invalid option message
![Invalid Option](docs/testing/main-menu-invalid.JPG)

`Register`

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail | Image |
| --- | --- | --- | --- | --- | --- |
| Username - length validation | Only accept usernames between 4-10 caracteres | Enter user with less than 4 characteres | Only accepts usernames between 4-10 caracteres | Pass | ![User less](docs/testing/user-less-length.JPG) |
| Username - length validation | Only accept usernames between 4-10 caracteres | Enter user with more than 10 characteres | Only accepts usernames between 4-10 caracteres | Pass | ![User more](docs/testing/user-more-length.JPG) |
| Username - alphanumeric validation | Only accept usernames with alphanumeric characteres | Enter user with special characteres | Only accepts usernames with alphanumeric characteres | Pass | ![User alphanumeric](docs/testing/user-alpha.JPG) |
| Username - existent | Only accept usernames that are different from the current ones registered | Enter username already registered before | Only accepts usernames that are different from the current ones registered | Pass | ![User existent](docs/testing/user-in-use.JPG) |
| Password - minimum length | Only accept passwords with 8 or more characteres | Enter password with less than 8 characteres | Only accept passwords with 8 or more characteres | Pass | ![User password](docs/testing/user-password.JPG) |
| Create user | Display the logged menu and create worksheet on the Google Spreadsheet with the username | Enter valids username and password | Displays the logged menu and create worksheet on the Google Spreadsheet with the username | Pass | ![User created](docs/testing/user-created.JPG) ![User created logged](docs/testing/user-created-logged.JPG) ![User created worksheet](docs/testing/user-created-worksheet.JPG)|
|  |  |  |  |  |  |

`Login`

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail | Image |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

`Guide`

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail | Image |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |


`Logged Menu`

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail | Image |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

`Add a Word`

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail | Image |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

`Review Words`

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail | Image |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

`See your List`

| Feature | Expected Outcome | Testing Performed | Result | Pass/Fail | Image |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |


---

## BUGS

### Known Bugs

The List of Words does not centralise.

---

Back to [README.md](README.md)