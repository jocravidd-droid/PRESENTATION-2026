def multiplication_function(cal):
    start = cal[0]
    for number in cal[1:]:
        start = start * number
    return start


def division_function(cal):
    start = cal[0]
    try:
        for number in cal[1:]:
            start = start / number
    except ZeroDivisionError:
        return 'a division by zero is impossible'
    return start


def subtraction_function(cal):
    start = cal[0]
    for number in cal[1:]:
        start = start - number
    return start


def smallest(cal):
    start = cal[0]
    for number in cal[1:]:
        start = min(start, number)
    return start


def largest(cal):
    start = cal[0]
    for number in cal[1:]:
        start = max(start, number)
    return start


def greater_or_equal(cal):
    start = cal[0]
    for number in cal[1:]:
        if number >= start:  # noqa: PLR1730
            start = number
    return start


def less_or_equal(cal):
    start = cal[0]
    for number in cal[1:]:
        if number <= start:  # noqa: PLR1730
            start = number
    return start


def equal(cal):
    box = True
    start = cal[0]
    for number in cal[1:]:
        if number != start:
            box = False
        else:
            continue
    return box


if __name__ == '__main__':
    x = multiplication_function([2, 4, 5])
    print(x)
    x = division_function([100, 2, 5])
    print(x)
    x = subtraction_function([20, 5, 3])
    print(x)
    x = smallest([8, 3, 12, 1])
    print(x)
    x = largest([8, 3, 12, 1])
    print(x)
