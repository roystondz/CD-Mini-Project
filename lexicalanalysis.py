import re
from tabulate import tabulate 

# Define token categories
DELIMITERS = {'(', ')', '{', '}', ';', ',', ':'}
KEYWORDS = {'int', 'main', 'begin', 'end', 'if', 'printf', 'for'}
OPERATORS = {'=', '==', '<', '>', '<=', '>='}

def tokenize_line(line, line_no):
    tokens = []
    pattern = r"\d+|\w+|[(){};:,=+*/<>]"
    words = re.findall(pattern, line)

    for word in words:
        if word in KEYWORDS:
            token_type = "Keyword"
        elif word in DELIMITERS:
            token_type = "Delimiter"
        elif word in OPERATORS:
            token_type = "Operator"
        elif word.isdigit():
            token_type = "Number"
        else:
            token_type = "Identifier"  

        tokens.append((word, token_type, line_no))

    return tokens

def lexical_analyzer(filename):
    token_table = []
    all_tokens = []
    token_count = 0

    with open(filename, "r") as file:
        for line_no, line in enumerate(file, start=1):
            line_tokens = tokenize_line(line, line_no)
            for token in line_tokens:
                token_count += 1
                token_table.append((token_count, token[0], token[1], token[2]))
                all_tokens.append(token)

    # Print the token table
    print(tabulate(token_table, headers=["Token No", "Lexeme", "Token Type", "Line No"]))
    return all_tokens
    

# Run lexical analysis on a sample file
tokens = lexical_analyzer("input.txt")

print("\nAll tokens:")
for item in tokens:
    print(item[0],end=",")