"""MAKE A LISP IN PYTHON"""

import re

import outils # MODULE contenant les fonctions de base pour les opérations arithmétiques et logiques

environnement = {}
stock = {'+': lambda cal: sum(cal), '*': outils.fonction_multiplication, '/': outils.fonction_division, '-': outils.fonction_soustraction, '<': outils.plus_petit, '>': outils.plus_grand, '>=': outils.superieur_egal, '<=': outils.inferieur_egal} # dictionnaire contenant les opérateurs et les fonctions associées

class ParentheseError(Exception): # erreur levée lorsqu'il y a un problème de parenthèses
    def __init__(self, message = "Aucune Paranthese ou Paranthese Ouvert"):
        super().__init__(message)

def tokenize(chaine): # tokenize l'expression en list (passe de str a list)
    result = re.findall(r"[()]|[^\s()]+", chaine)
    return result

def read_form(tokens): # gere les embriquation

    mappage = []

    index = 0
    while index < len(tokens):
        if tokens[index] == ')':
            index += 1
            return mappage, index
        elif tokens[index] == '(':
            if index == 0:
                index += 1
            else:
                sous_liste, tokens_lus = read_form(tokens[index:])
                mappage.append(sous_liste)
                index += tokens_lus
        else:
            if tokens[index].isdigit() or tokens[index].lstrip('-').isdigit():  
                mappage.append(int(tokens[index]))
                index += 1
            else:
                try:
                    mappage.append(float(tokens[index]))
                    index += 1
                except ValueError:
                    mappage.append(tokens[index])
                    index += 1
    
    return mappage, index

def READ(info): # lance le processus de lecture et de tokenisation, puis retourne la liste finale
    contenu = tokenize(info)
    if info[0] == '(' and info[-1] == ')':
        liste, _token = read_form(contenu)
        return liste
    if info[0] != '(' and info[-1] != ')':
        if info.isdigit() or info.lstrip('-').isdigit():
            return int(info)
        else:
            try:
                return float(info)
            except ValueError:
                return info
    elif (info[0] == '(' and info[-1] != ')') or (info[0] != '(' and info[-1] == ')'):
        raise ParentheseError
    
        
def EVAL(expr, env = environnement): # evaluer l'expression en fonction de l'environnement
    if not isinstance(expr, list): # si l'expression n'est pas une liste, on retourne la valeur de la variable dans l'environnement
        if expr in env:
            return env[expr]
        elif expr in environnement:
            return environnement[expr]
        else:
            return expr
    if len(expr)== 0: # si l'expression est vide, on retourne une erreur
        raise IndexError('AUCUN CONTENU')
    else:
        if expr[0] == 'let*': # si l'expression est un let*, on crée un environnement local pour stocker les variables
            env_local = {cle: env[cle] for cle in env} # on copie l'environnement global dans l'environnement local
            index = 0
            while index < len(expr[1]):
                if isinstance(expr[1][index], str):
                    env_local[expr[1][index]] = EVAL(expr[1][index + 1], env_local)
                    index += 1
                else:
                    index += 1
            operateur = EVAL(expr[2], env_local)

            try:
                return operateur
            except KeyError:
                return "Operateur Inconnu"
                    
                
        if expr[0] != 'def!': # si l'expression n'est pas une définition, on évalue l'opérateur et les arguments
            operateur = expr[0]
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
                calcul = stock[operateur]
                result = calcul(arguments)
                return result
            except KeyError:
                return "Operateur Inconnu"
        else: # si l'expression est une définition, on stocke la variable dans l'environnement

            somme = []

            for verif in expr[1:]:
                if isinstance(verif, list):
                    result = EVAL(verif, environnement)
                    somme.append(result)
                else:
                    somme.append(verif)

            lettre = []

            for index, correction in enumerate(somme):
                if isinstance(correction, str):
                    lettre.append(correction)
                    if isinstance(somme[index + 1], (int, float)):
                        environnement[lettre[index]] = somme[index + 1]

            return environnement[expr[1]]
        
def PRINT(info): # retourne l'information sous forme de string
    return info

def rep(info): # LANCE LE PROCESSUS DE LECTURE, EVALUATION ET AFFICHAGE
    a = READ(info)
    b = EVAL(a)
    c = PRINT(b)
    print(c)
    with open('output.txt', 'a') as f: # on écrit le résultat dans un fichier output.txt pour garder une trace des résultats
        f.write(f'sortie [{info}]:{str(c)}' + '\n')

if __name__ == '__main__':
    while True:
        try:
            cmd = input('user> ') # demande à l'utilisateur de saisir une expression
            rep(cmd)
        except EOFError: # si l'utilisateur fait un ctrl+D, on quitte le programme
            print('EXIT')
            break