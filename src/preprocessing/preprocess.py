# preprocessing/normalize.py
# Python program which takes a whole file and outputs a list of normalized lines
# strip, collapse spaces, maybe lowercase, maybe remove comments
# Puts everything in lowercase by default


string_mode = False  # Global variable, allowing strings to be multi line
comment_mode = False # Global variable, allowing comments like /* */ to be multi line

def normalize_file_with_index_map(path: str):
    """
    Returns:
      normalized_lines: list[str]
      index_map: dict[int → int] mapping normalized index → raw index
    """
    normalize_list = []
    index_map = {}

    global string_mode, comment_mode
    string_mode = False
    comment_mode = False

    with open(path) as f:
        raw_lines = f.readlines()

    norm_index = 0
    for raw_index, raw_line in enumerate(raw_lines):
        temp = normalize_line(raw_line, True)
        if temp != "":
            normalize_list.append(temp)
            index_map[norm_index] = raw_index
            norm_index += 1

    return normalize_list, index_map



def normalize_line(line: str, lowercase: bool) -> str:
    """ Method to normalize a line of text.
        Works by first tokenizing all of the characters in a loop, lowercasing non string stuff if asked, and putting
        them into the list Tokens(new line is not included, not sure if that is desireable or not)
        It sends back an empty string if there are no tokens
        otherwise it loops through the tokens list and makes space between each
    """
    global string_mode  # Declare intent to modify the global variable
    global comment_mode  # Declare intent to modify the global variable
    if line == "":
        return ""
    list_length = len(line) #length of line
    tokens = []  # makes a list of tokens that will separated with space
    token = ""  # an element of tokens
    new_line = ""  # the output of this method
    prev_quotation = ''  # makes sure that the same initial quotation is being used
    prev_char = ""  # Used to see what the previous character in the string was
    operators = {"+", "-", "*", "/", "%", "!", ">", "<", ":", ";", "(", ")", "[", ']', '{', '}'}  # list of characters we want as individual tokens
    for index, char in enumerate(line):  # go through each character of line
        if char == '\n':  # like I said, new line character is excluded
            if token != '':
                tokens.append(token)
            break
        if string_mode:  # string mode, the loop will stay here until the same quotation marks appear
            token += char
            if char == prev_quotation:
                string_mode = False
                tokens.append(token)
                token = ''
        elif comment_mode:
            if prev_char == '*' and char == '/':
                comment_mode = False
                prev_char = ''
        else:  # the normal loop
            if char == "\"" or char == "'":  # Checks if a quotation mark forms to turn into string mode
                if token != "":
                    tokens.append(token)
                    token = ""
                string_mode = True
                prev_quotation = char
                token += char
            elif char == " ":  # checks for a space character, ignores it, only really using it to isolate tokens
                if token != "":
                    tokens.append(token)
                    token = ''
            elif char == "#" or index < list_length -1 and (char == "/" and line[index+1] == "/"):  # checks if it is a comment, if so, exits the loop
                break
            elif index < list_length -1 and char == "/" and line[index+1] == "*": #checks if the line has /*
                if token != '':
                    tokens.append(token)
                token = ''
                comment_mode = True
                prev_char = ""
                continue
            elif char in operators:  # checks if it is an operator, if so tokenize it individually
                if token != '':
                    tokens.append(token)
                token = ''
                tokens.append(char)
            else:  # basic case, will lowercase it if the lowercase option is turned on
                if lowercase and char.isupper():  # converts uppercase into lowercase
                    char = char.lower()
                token += char
        prev_char = char
    if tokens == []:  # checks for empty list and returns an empty string if so
        return ""
    for index, token in enumerate(tokens):  # Combine each string and seperate them with space character
        if index == 0:
            new_line += token
            continue
        if token == "":
            continue
        new_line += ' ' + token
    return new_line


def normalize_file(path: str) -> list[str]:  # reads from a file and makes a list of lines in the file
    normalize_list = []  # output of method
    with open(path) as f:  # opens file
        lines = f.readlines()  # makes the lines list
    for l in lines:  # basic loop that gives each line to normalize_line() and combines them into a list of non empty strings
        temp = normalize_line(l, True)
        if temp != "":
            normalize_list.append(temp)
    return normalize_list
