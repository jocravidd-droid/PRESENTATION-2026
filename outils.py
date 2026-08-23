def fonction_multiplication(cal):
    debut = cal[0]
    for number in cal[1:]:
        debut = debut * number
    return debut

def fonction_division(cal):
    debut = cal[0]
    try:
        for number in cal[1:]:
            debut = debut / number
    except ZeroDivisionError:
        return 'une division par zéro et impossible'
    return debut

def fonction_soustraction(cal):
    debut = cal[0]
    for number in cal[1:]:
        debut = debut - number
    return debut

def plus_petit(cal):
    debut = cal[0]
    for number in cal[1:]:
        debut = min(debut, number)
    return debut

def plus_grand(cal):
    debut = cal[0]
    for number in cal[1:]:
        debut = max(debut, number)
    return debut

def superieur_egal(cal):
    debut = cal[0]
    for number in cal[1:]:
        if number >= debut:  # noqa: PLR1730
            debut = number
    return debut

def inferieur_egal(cal):
    debut = cal[0]
    for number in cal[1:]:
        if number <= debut:  # noqa: PLR1730
            debut = number
    return debut

def egal(cal):
    boite = True
    debut = cal[0]
    for number in cal[1:]:
        if number != debut:
            boite = False
        else:
            continue
    return boite


if __name__ == '__main__':

    x = fonction_multiplication([2, 4, 5])
    print(x)

    x = fonction_division([100, 2, 5])
    print(x)

    x = fonction_soustraction([20, 5, 3])
    print(x)

    x = plus_petit([8, 3, 12, 1])
    print(x)

    x = plus_grand([8, 3, 12, 1])
    print(x)