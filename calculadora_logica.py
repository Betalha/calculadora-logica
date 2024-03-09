import ttg
import re

def verify_fbf(expression):
    if expression == "": return False
    stack = []
    counter = 0
    c = 0
    for caractere in expression:
        if caractere in "ABCDEFGHIJKLMNOPQRSTUWXYZ" or caractere in "01~":
            if caractere == "~": c+=1
            stack.append(caractere)
        elif caractere in "~∧V↔→":
            if len(stack) < 1 or stack.pop() == "~":
                return False
            
        elif caractere == '(': counter += 1
        elif caractere == ')':
            counter -= 1
            if counter < 0:
                return False
        else: 
            if caractere != " ": return False

    stack.pop()
    if counter != 0: return False
    return len(stack) == c

class Calculator:
    def __init__(self):
        self.expression = ""
        self.truth_table = ""
        self.valuation = ""

    def replace_characters(self, input_string):
        replacements = {
            '→': ' => ',
            '↔': ' = ',
            'V': ' or ',
            '⊻': ' xor ',
            '∧': ' and ',
            '~': 'not '
        }
        pattern = re.compile('|'.join(re.escape(key) for key in replacements.keys()))
        return pattern.sub(lambda match: replacements[match.group(0)], input_string)

    def get_propositions(self):
        if self.expression != "":
            values = re.findall(r"\b(?!and\b|or\b|not\b|xor\b)\w+\b", self.expression)

            propositions = list(dict.fromkeys(values))  # removing duplicates

            return propositions
        else:
            print("Error: Must set expression first")
            raise SyntaxError

    def set_valuation(self, valuation):
        if valuation != "":
            if valuation == "Contingency":
                return "A expressão é uma contingência."
            elif valuation == "Tautology":
                return "A expressão é uma tautologia."
            elif valuation == "Contradiction":
                return "A expressão é uma contradição."
        else:
            print("Error: Must set expression first")
            raise SyntaxError

    def get_truth_table(self):
        return self.truth_table

    def set_expression(self, expression):
        self.expression = self.replace_characters(expression)
        propositions = self.get_propositions()
        self.truth_table = ttg.Truths(propositions, [self.expression])
        self.valuation = self.set_valuation(self.truth_table.valuation())


expressao = "-"

while expressao != "":
    expressao = input("digite a expressao (proposicoes devem ser simbolizadas com letras maiusculas e o seguintes simbolos "+"~ ∧ V ↔ →"+"):")
    if verify_fbf(expressao):
        resultado = Calculator()
        resultado.set_expression(expressao)
        print(resultado.valuation)
        print(resultado.truth_table)


