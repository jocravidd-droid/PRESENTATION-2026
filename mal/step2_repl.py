"""MAKE A LISP IN PYTHON"""

import re

import tools  # MODULE containing the base functions for arithmetic and logical operations

environment = {}
stock = {
    '+': lambda cal: sum(cal),
    '*': tools.multiplication_function,
    '/': tools.division_function,
    '-': tools.subtraction_function,
    '<': tools.smallest,
    '>': tools.largest,
    '>=': tools.greater_or_equal,
    '<=': tools.less_or_equal,
}  # dictionary containing the operators and their associated functions


class ParenthesisError(Exception):  # error raised when there is a parenthesis problem
    def __init__(self, message="No parenthesis or unclosed parenthesis"):
        super().__init__(message)


def tokenize(string):  # tokenizes the expression into a list (str -> list)
    result = re.findall(r"[()]|[^\s()]+", string)
    return result


def read_form(tokens):  # handles nesting

    mapping = []

    index = 0
    while index < len(tokens):
        if tokens[index] == ')':
            index += 1
            return mapping, index
        elif tokens[index] == '(':
            if index == 0:
                index += 1
            else:
                sub_list, tokens_read = read_form(tokens[index:])
                mapping.append(sub_list)
                index += tokens_read
        else:
            if tokens[index].isdigit() or tokens[index].lstrip('-').isdigit():
                mapping.append(int(tokens[index]))
                index += 1
            else:
                try:
                    mapping.append(float(tokens[index]))
                    index += 1
                except ValueError:
                    mapping.append(tokens[index])
                    index += 1

    return mapping, index


def READ(info):  # starts the reading and tokenizing process, then returns the final list
    content = tokenize(info)
    if info[0] == '(' and info[-1] == ')':
        parsed_list, _token = read_form(content)
        return parsed_list
    if info[0] != '(' and info[-1] != ')':
        if info.isdigit() or info.lstrip('-').isdigit():
            return int(info)
        else:
            try:
                return float(info)
            except ValueError:
                return info
    elif (info[0] == '(' and info[-1] != ')') or (info[0] != '(' and info[-1] == ')'):
        raise ParenthesisError


def EVAL(expr, env=environment):  # evaluates the expression using the environment
    if not isinstance(expr, list):  # if the expression is not a list, return the variable's value from the environment
        if expr in env:
            return env[expr]
        elif expr in environment:
            return environment[expr]
        else:
            return expr
    if len(expr) == 0:  # if the expression is empty, raise an error
        raise IndexError('NO CONTENT')
    else:
        if expr[0] == 'let*':  # if the expression is a let*, create a local environment to store the variables
            local_env = {key: env[key] for key in env}  # copy the global environment into the local one
            index = 0
            while index < len(expr[1]):
                if isinstance(expr[1][index], str):
                    local_env[expr[1][index]] = EVAL(expr[1][index + 1], local_env)
                    index += 1
                else:
                    index += 1
            operator = EVAL(expr[2], local_env)

            try:
                return operator
            except KeyError:
                return "Unknown Operator"

        if expr[0] != 'def!':  # if the expression is not a definition, evaluate the operator and the arguments
            operator = expr[0]
            arguments = []

            for argument in expr[1:]:
                if isinstance(argument, list):
                    result = EVAL(argument, env)
                    arguments.append(result)
                elif argument in env:
                    arguments.append(env[argument])
                else:
                    arguments.append(argument)
            try:
                computation = stock[operator]
                result = computation(arguments)
                return result
            except KeyError:
                return "Unknown Operator"
        else:  # if the expression is a definition, store the variable in the environment

            total = []

            for check in expr[1:]:
                if isinstance(check, list):
                    result = EVAL(check, environment)
                    total.append(result)
                else:
                    total.append(check)

            letters = []

            for index, correction in enumerate(total):
                if isinstance(correction, str):
                    letters.append(correction)
                    if isinstance(total[index + 1], (int, float)):
                        environment[letters[index]] = total[index + 1]

            return environment[expr[1]]


def PRINT(info):  # returns the information as a string
    return info


def rep(info):  # RUNS THE READ, EVAL AND PRINT PROCESS
    a = READ(info)
    b = EVAL(a)
    c = PRINT(b)
    print(c)


if __name__ == '__main__':
    while True:
        try:
            cmd = input('user> ')  # asks the user to type an expression
            rep(cmd)
        except EOFError:  # if the user hits ctrl+D, quit the program
            print('EXIT')
            break
