"""
    COMPILER DESIGN COURSEWORK
    EPIPHANY 2020
    BEN NAPIER
    DUE: 2020-03-13
"""
# IMPORTS
import re
import sys

from anytree import *
from anytree.exporter import DotExporter


# LOGGING

def log_error(message):
    """
    Will take a message, output it to a log.txt file then will exit execution.
    """
    with open('log.txt', 'w') as f:
        f.write(message)
    print('Parsing failed, see log.txt file.')
    exit()


def log_success():
    """
    Sends a success message to log.txt then exits. 
    """
    with open('log.txt', 'w') as f:
        f.write("Parsing successful.")
    print('Parsing successful.')
    exit()


# LOOKING AT SYS ARGS
input_file_name = ''
output_grammar_file_name = ''
output_ast_file_name = ''
if len(sys.argv) != 4:
    raise Exception(
        'You must give 3 arguments, the first for the input file, the second for the output file for the grammar, '
        'and the third for the output file for the abstract syntax tree.')
else:
    input_file_name = sys.argv[1]
    output_grammar_file_name = sys.argv[2]
    output_ast_file_name = sys.argv[3]

if output_ast_file_name[-4:] != '.png':
    raise Exception('Output file must end with .png.')

# READING THE FILE
with open(input_file_name, 'r') as f:
    data = f.read().split('\n')
formula_input = ''
predicate_input = ''
equality_input = ''
connective_input = ''
quantifier_input = ''
variable_input = ''
constant_input = ''
for line_index in range(0, len(data)):
    data[line_index] = re.sub(' +', ' ', data[line_index])  # remove multiple consecutive whitespace
    if data[line_index].startswith('formula:'):
        formula_input = data[line_index][8:].strip()
        # handling formula over multiple lines
        temp_line_index = line_index + 1
        while temp_line_index < len(data) and ':' not in data[temp_line_index]:
            data[temp_line_index] = re.sub(' +', ' ', data[temp_line_index])
            if data[temp_line_index] != "":
                formula_input += data[temp_line_index]
            temp_line_index += 1

    elif data[line_index].startswith('predicates:'):
        predicate_input = data[line_index][11:].strip()
    elif data[line_index].startswith('equality:'):
        equality_input = data[line_index][9:].strip()
    elif data[line_index].startswith('connectives:'):
        connective_input = data[line_index][12:].strip()
    elif data[line_index].startswith('quantifiers:'):
        quantifier_input = data[line_index][12:].strip()
    elif data[line_index].startswith('variables:'):
        variable_input = data[line_index][10:].strip()
    elif data[line_index].startswith('constants:'):
        constant_input = data[line_index][10:].strip()

# SLIGHT MODIFICATION TO FORMULA, ADDS SPACING TO PREDICATES
formula_input = re.sub('(?<=[(),])(?=[^\s])', ' ', formula_input)
formula_input = re.sub('(?<=[^\s])(?=[(),])', ' ', formula_input)

# EXTRACTING PREDICATE ARITY
predicate_list = []
predicate_input_list = predicate_input.split(" ")
if predicate_input != "":
    for predicate_input in predicate_input_list:
        match = re.match(r'(.+)\[([1-9][0-9]*)\]', predicate_input)
        if match is None:
            log_error("Predicate input '{}' is not formatted properly.".format(predicate_input))
        else:
            predicate_list.append((match.group(1), int(match.group(2))))

# EXTRACTING VARIABLES, CONSTANTS, EQUALITY
variable_list = variable_input.split(" ")
if variable_input == "":
    variable_list = []
constant_list = constant_input.split(" ")
if constant_input == "":
    constant_list = []

# EXTRACTING EQUALITY
equality_list = []
if equality_input != "":
    equality_list = equality_input.split(" ")
if len(equality_list) != 1:
    log_error("Caradinality of the set of equality is {}, not 1.".format(len(equality_list)))

# EXTRACTING CONNECTIVES
connective_list = connective_input.split(" ")
# Error handling
if len(connective_list) != 5:
    log_error("Caradinality of the set of connectives is {}, not 5.".format(len(connective_list)))

# EXTRACTING QUANTIFIERS
quantifier_list = quantifier_input.split(" ")
# Error handling
if len(quantifier_list) != 2:
    log_error("Cardinality of the set of quantifiers is {}, not 2.".format(len(quantifier_list)))

# PRODUCTIONS ("S", "aS") \iff S \to aS
production_list = [("S", "F")]
terminal_symbol_list = [" ", "|", ",", "(", ")"]
non_terminal_symbol_list = ["S", "F"]

# CHECKING NO NAMING OVERLAP
for predicate in predicate_list:
    if predicate[0] in constant_list:
        log_error('Predicate {} named the same as constant.'.format(predicate[0]))
    if predicate[0] in variable_list:
        log_error('Predicate {} named the same as variable.'.format(predicate[0]))
for constant in constant_list:
    if constant in variable_list:
        log_error('Constant {} named the same as variable.'.format(constant))

# PRODUCING THE GRAMMAR
# 1. PREDICATES AND VARIABLES
predicate_initial_production_rule_list = []
for predicate in predicate_list:
    production_list.append(("F", "{}[{}]".format(predicate[0], predicate[1])))
    non_terminal_symbol_list.append("{}[{}]".format(predicate[0], predicate[1]))
    predicate_rule = "{}({})".format(predicate[0], ",".join(["V" for i in range(0, predicate[1])]))
    production_list.append(("{}[{}]".format(predicate[0], predicate[1]), predicate_rule))
production_list.append(("V", " | ".join(variable_list)))
non_terminal_symbol_list.append("V")
terminal_symbol_list += variable_list
terminal_symbol_list += [predicate[0] for predicate in predicate_list]

# 2. EQUALITY
if len(constant_list) > 0:
    production_list.append(("F", "(C = V) | (V = C) | (C = C) | (V = V)"))
    production_list.append(("C", " | ".join(constant_list)))
    terminal_symbol_list += constant_list
else:
    production_list.append(("F", "(V = V)"))

# 3. CONNECTIVES
for connective in connective_list:
    if connective == connective_list[4]:
        production_list.append(("F", "{} F".format(connective)))
    else:
        production_list.append(("F", "(F {} F)".format(connective)))
terminal_symbol_list += connective_list

# 4. QUANTIFIERS
production_list.append(("F", " | ".join(["{} {} F".format(quantifier, "V") for quantifier in quantifier_list])))
terminal_symbol_list += quantifier_list

# Making production rule listings more concise
unique_left_side_set = {production_rule[0] for production_rule in production_list}
concise_production_list = []
for unique_left_side in unique_left_side_set:
    concise_production_list.append((unique_left_side,
                                    " | ".join(
                                        [production_rule[1] for production_rule in production_list if
                                         production_rule[0] == unique_left_side]))
                                   )
production_list = concise_production_list
production_list.sort(key=lambda t: len(t[1]), reverse=True)


def get_predicate(input_predicate):
    for predicate in predicate_list:
        if input_predicate == predicate[0]:
            return predicate
    return None


def find_matching_bracket_index(input_list):
    """
    Finds matching bracket (assumes first entry is a left bracket).
    """
    depth = 1
    index = 0
    while depth != 0:
        index += 1
        if index == len(input_list):
            log_error("No matching bracket found.")
        if input_list[index] == "(":
            depth += 1
        elif input_list[index] == ")":
            depth -= 1
    if depth != 0:
        log_error("No matching bracket found.")
    else:
        return index


def parse_bracket_bound(input_list):
    """
    Parse the string assuming it was bound in brackets
    """
    # and or implies iff checking
    depth = 0
    for i in range(0, len(input_list)):
        if input_list[i] == "(":
            depth += 1
        elif input_list[i] == ")":
            depth -= 1
        elif input_list[i] in connective_list[:-1]:
            if depth == 0:
                return [input_list[i],
                        parse_formula(input_list[0:i]),
                        parse_formula(input_list[i + 1:])]
    # Check for constants and variables
    if input_list[0] in constant_list or input_list[0] in variable_list:
        if input_list[1] in equality_list:
            if input_list[2] in constant_list or input_list[2] in variable_list:
                return [equality_input[0], [input_list[0]], [input_list[2]]]
            log_error('Expected a variable or constant but got {}.'.format(input_list[2]))
        log_error('Expected an equality symbol but got {}.'.format(input_list[1]))
    # Just incase we gotta go again
    if input_list[0] == "(":
        matching_bracket_index = find_matching_bracket_index(input_list)
        return parse_bracket_bound(input_list[1:matching_bracket_index])
    log_error('Expected a valid bracket bound expression but got ({}).'.format(" ".join(input_list)))


def parse_predicate(input_list, predicate):
    """
    Assumes we get V,V,V,...,V according to the arity of the predicate
    """
    if len(input_list) != (predicate[1] * 2) - 1:
        log_error('Expected {} characters in predicate, got {}.'
                  .format((predicate[1] * 2) - 1, len(input_list)))
    return_tree = [predicate[0]]
    for i in range(0, len(input_list)):
        if i % 2 == 0:
            if input_list[i] not in variable_list:
                log_error('Expected a variable but got {}.'.format(input_list[i]))
            return_tree.append([input_list[i]])
        elif i % 2 == 1:
            if input_list[i] != ",":
                log_error('Expected \', \' but got {}.'.format(input_list[i]))
    return return_tree


def parse_quantifier(input_list):
    if len(input_list) < 3:
        log_error('Expected 3 or more characters but got {}.'.format(len(input_list)))
    if input_list[1] not in variable_list:
        log_error('Expected a variable but got {}.'.format(input_list[1]))
    return [input_list[0],
            [input_list[1]],
            parse_formula(input_list[2:])]


def parse_formula(input_list):
    """
        Parse an input stream. Will return a parse tree of the character stream.
    """
    parse_tree = []
    # Checking for brackets
    if input_list[0] == "(":
        matching_bracket_index = find_matching_bracket_index(input_list)
        return parse_bracket_bound(input_list[1:matching_bracket_index])
    # not checking
    if input_list[0] == connective_list[4]:
        return [connective_list[4],
                parse_formula(input_list[1:])]
    # Predicate checking
    is_predicate = get_predicate(input_list[0])
    if is_predicate is not None:
        if input_list[1] != "(":
            log_error('Expected \'(\', got {}.'.format(input_list[1]))
        matching_bracket_index = find_matching_bracket_index(input_list[1:])
        return parse_predicate(input_list[2:matching_bracket_index + 1], is_predicate)
    # Quantifier checking
    if input_list[0] in quantifier_list:
        return parse_quantifier(input_list)
    log_error('Expected a valid formula but got {}.'.format(' '.join(input_list)))


node_list = []
counter = 0


def anytree_format_tree(formula, parent_index):
    global counter
    counter += 1
    # base case
    if parent_index is None:
        node_list.append(Node(counter, display_name=formula[0].replace('\\', '\\\\')))
        for i in range(1, len(formula)):
            anytree_format_tree(formula[i], 0)
        return

    node_list.append(Node(counter, display_name=formula[0].replace('\\', '\\\\'), parent=node_list[parent_index]))
    index = len(node_list) - 1
    for i in range(1, len(formula)):
        anytree_format_tree(formula[i], index)


formula = parse_formula(formula_input.split(" "))
anytree_format_tree(formula, None)
DotExporter(node_list[0], nodeattrfunc=lambda node: 'label="{}"'.format(node.display_name)).to_picture(output_ast_file_name)

if len([x for x in formula_input.replace(')', '').replace('(', '').replace(',', '').split(" ") if x != '']) > len(
        node_list):
    log_error('Found trailing input near {} where not expected.'.format(' '.join(formula_input.split(' ')[(-1 * (len(
        [x for x in formula_input.replace(')', '').replace('(', '').replace(',', '').split(" ") if x != '']) - len(
        node_list))):])))

with open(output_grammar_file_name, 'w') as f:
    f.write("TERMINAL SYMBOLS")
    # Printing production rules
    f.write('\n'.join(terminal_symbol_list))
    f.write("\n\nNON-TERMINAL SYMBOLS")
    f.write('\n'.join(non_terminal_symbol_list))
    f.write("\n\nPRODUCTION RULES")
    maximum_left_size = max([len(production_rule[0]) for production_rule in production_list])
    for production_rule in production_list:
        f.write("\n{} -> {}".format(production_rule[0].ljust(maximum_left_size), production_rule[1]))
    f.write("\n\nSTART SYMBOL\nS")

log_success()
