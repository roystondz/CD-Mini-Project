DIGITS = '0123456789'

#LEXER

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        print("Tokens are: ")
        modified_ip = ''
        temp = ''
        inc = 0
        while self.current_char != None:
            if self.current_char in ' \t\n':
                self.advance()
                modified_ip += ' '

            elif self.current_char in DIGITS:
                temp = self.current_char
                while self.text[self.pos + 1] in DIGITS:
                    self.advance()
                    temp += self.current_char
                print(f"Constant : {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char == '+':
                temp = self.current_char
                if self.text[self.pos + 1] == '+':
                    self.advance()
                    temp += self.current_char
                    print(f"Increment Operator : {temp}")
                    modified_ip += temp
                else:
                    print(f"Addition Operator : {temp}")
                    modified_ip += temp
                    self.advance()
                self.advance()
            elif self.current_char == '-':
                temp = self.current_char
                print(f"Subtraction Operator : {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char == '*':
                temp = self.current_char
                print(f"Multiplication Operator : {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char == '/':
                temp = self.current_char
                print(f"Division Operator: {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char == '(':
                temp = self.current_char
                print(f"Left Parenthesis : {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char == ')':
                temp = self.current_char
                print(f"Right Parenthesis : {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char == '=':
                temp = self.current_char
                if self.text[self.pos + 1] == '=':
                    self.advance()
                    temp += self.current_char
                    print(f"Relational Operator : {temp}")
                else:
                    print(f"Assignment Operator : {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char == '<':
                temp = self.current_char
                if self.text[self.pos + 1] == '=':
                    self.advance()
                    temp += self.current_char
                    print(f"Relational Operator : {temp}")
                else:
                    print(f"Relational Operator : {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char == '>':
                temp = self.current_char
                if self.text[self.pos + 1] == '=':
                    self.advance()
                    temp += self.current_char
                    print(f"Relational Operator : {temp}")
                else:
                    print(f"Relational Operator : {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char == '!':
                temp = self.current_char
                if self.text[self.pos + 1] == '=':
                    self.advance()
                    temp += self.current_char
                    print(f"Relational Operator : {temp}")
                else:
                    print(f"NOT Operator : {temp}")
                modified_ip += temp
                self.advance()

            elif self.current_char.isalpha():
                if self.text[self.pos:self.pos+6] == 'main()' and self.text[self.pos+6] in ' \n\t':
                    for inc in range(0,6):
                        self.advance()
                    temp = 'main()'
                    modified_ip += temp
                    print(f"Keyword : {temp}")
                    self.advance()

                elif self.text[self.pos:self.pos+3] == 'int' and self.text[self.pos+3] in ' \n\t':
                    for inc in range(0,3):
                        self.advance()
                    temp = 'int'
                    modified_ip += temp
                    print(f"Keyword : {temp}")
                    self.advance()

                elif self.text[self.pos:self.pos+5] == 'begin' and self.text[self.pos+5] in ' \n\t':
                    for inc in range(0,5):
                        self.advance()
                    temp = 'begin'
                    modified_ip += temp
                    print(f"Keyword : {temp}")
                    self.advance()

                elif self.text[self.pos:self.pos+3] == 'end' and (self.pos+3 >= len(self.text) or self.text[self.pos+3] in ' \n\t'):
                #elif self.text[self.pos:self.pos+3] == 'end' and self.text[self.pos+3] in ' \n\t':
                    for inc in range(0,3):
                        self.advance()
                    temp = 'end'
                    modified_ip += temp
                    print(f"Keyword : {temp}")
                    self.advance()

                elif self.text[self.pos:self.pos+3] == 'for' and self.text[self.pos+3] == '(':
                    for inc in range(0,2):
                        self.advance()
                    temp = 'for'
                    modified_ip += temp
                    print(f"Keyword : {temp}")
                    self.advance()

                else:
                    temp = self.current_char
                    while self.text[self.pos+1].isalpha():
                        self.advance()
                        temp += self.current_char
                    modified_ip += temp
                    print(f"Identifier : {temp}")
                    self.advance()

            elif self.current_char in ';:,.':
                temp = self.current_char
                print(f"Special Character : {temp}")
                modified_ip += temp
                self.advance()

            else:
                char = self.current_char
                self.advance()

                return False, f"Illegal Character '{char}'"

            modified_ip += ' '
        return True, modified_ip[:-1]

def run(text):
    lexer = Lexer(text)
    return lexer.make_tokens()