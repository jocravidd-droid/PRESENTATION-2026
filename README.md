# MAL — Make A Lisp in Python

A minimal Lisp interpreter written in Python. It reads an S-expression typed by the user, parses it into a nested Python list, evaluates it, and prints the result — the classic READ / EVAL / PRINT loop.

---

## Project layout

| File | Role |
|------|------|
| `mal.py` | Interpreter: tokenizer, parser, evaluator, REPL |
| `tools.py` | Arithmetic and comparison functions used by the evaluator |

`mal.py` imports `tools`, so both files must sit in the same directory.

---

## Requirements

- Python 3.8 or newer
- No external dependencies (standard library only: `re`)

---

## Running the REPL

```bash
python mal.py
```

You get a prompt:

```
user> (+ 1 2 3)
6
user> (* 2 (+ 3 4))
14
user> 
```

Press `Ctrl+D` to quit (the program prints `EXIT` and stops).

---

## Syntax supported

### Atoms

| Input | Result |
|-------|--------|
| `42` | integer `42` |
| `-7` | integer `-7` |
| `3.5` | float `3.5` |
| `hello` | the symbol `hello` — its value if defined, otherwise the symbol itself |

### Calls

An expression is a parenthesized list whose first element is an operator and whose remaining elements are the arguments:

```
(operator arg1 arg2 ...)
```

Arguments may themselves be lists — nesting is evaluated inside-out.

```
user> (- 20 5 3)
12
user> (/ 100 2 5)
10.0
user> (* 2 (- 10 4) 3)
36
```

---

## Built-in operators

All operators are variadic: they fold over the argument list from left to right.

| Operator | Function called | Behaviour |
|----------|-----------------|-----------|
| `+` | `sum` | Sum of all arguments |
| `-` | `tools.subtraction_function` | First argument minus each of the following |
| `*` | `tools.multiplication_function` | Product of all arguments |
| `/` | `tools.division_function` | First argument divided by each of the following |
| `<` | `tools.smallest` | Smallest value in the list |
| `>` | `tools.largest` | Largest value in the list |
| `<=` | `tools.less_or_equal` | Last value that is `<=` the running value |
| `>=` | `tools.greater_or_equal` | Last value that is `>=` the running value |

Division by zero does not crash — it returns the string `a division by zero is impossible`.

An unknown operator returns the string `Unknown Operator`.

---

## Special forms

### `def!` — define a global variable

```
(def! name value)
```

Stores `value` in the global `environment` dictionary and returns it.

```
user> (def! a 6)
6
user> (+ a 4)
10
user> (def! b (* a 2))
12
user> (+ a b)
18
```

The value may be a nested expression; it is evaluated before being stored.

### `let*` — define local bindings

```
(let* (name1 value1 name2 value2 ...) body)
```

Creates a copy of the current environment, adds the bindings to that copy, evaluates `body` inside it, and returns the result. The bindings are **not** visible after the `let*` ends.

```
user> (let* (c 2) c)
2
user> (let* (c 2 d (* c 3)) (+ c d))
8
```

Bindings are read as a flat list of pairs — `(c 2 d 3)`, not `((c 2) (d 3))`.

---

## How it works

```
input string
    |
 tokenize()      splits on parentheses and whitespace -> list of tokens
    |
 read_form()     builds the nested list, converts numeric tokens to int/float
    |
 READ()          entry point; validates the outer parentheses
    |
 EVAL()          resolves symbols, applies special forms, calls the operator
    |
 PRINT()         returns the value
    |
  print
```

### `tokenize(string)`

Uses the regex `[()]|[^\s()]+`: every parenthesis becomes its own token, and any run of non-space, non-parenthesis characters becomes one token.

```python
tokenize("(+ 1 (* 2 3))")
# ['(', '+', '1', '(', '*', '2', '3', ')', ')']
```

### `read_form(tokens)`

Walks the token list and returns `(nested_list, tokens_consumed)`.

- `(` at position 0 is the opening of the current list and is simply skipped.
- `(` anywhere else starts a sub-list: the function calls itself on the remaining tokens and appends the result.
- `)` closes the current list and returns.
- Anything else is converted to `int`, then `float`, and left as a string if both fail.

The second return value (`tokens_consumed`) is what lets the caller jump past the sub-list it just parsed.

### `READ(info)`

Tokenizes, then dispatches on the first and last character of the raw input:

- starts with `(` and ends with `)` -> parse as a list
- neither -> parse as a single atom
- only one of the two -> raise `ParenthesisError`

### `EVAL(expr, env=environment)`

- Not a list -> looked up in `env`, then in the global `environment`; returned as-is if absent.
- Empty list -> `IndexError('NO CONTENT')`.
- First element `let*` -> local-binding branch described above.
- First element `def!` -> definition branch, writes to the global `environment`.
- Anything else -> evaluate each argument (recursively for sub-lists), look the operator up in `stock`, and call it with the argument list.

### `PRINT(info)` and `rep(info)`

`PRINT` currently returns its input unchanged — it is the hook where a proper Lisp-style printer would go. `rep` chains the three stages and prints the result.

---

## Errors

| Situation | Behaviour |
|-----------|-----------|
| Unbalanced outer parentheses | raises `ParenthesisError` |
| Empty list `()` | raises `IndexError: NO CONTENT` |
| Unknown operator | returns `"Unknown Operator"` |
| Division by zero | returns `"a division by zero is impossible"` |
| `Ctrl+D` | prints `EXIT`, exits the loop |

`ParenthesisError` is a custom exception with the default message `No parenthesis or unclosed parenthesis`.

---

## Known limitations

These are current behaviours of the code, worth knowing before extending it:

1. **Comparison operators return numbers, not booleans.** `(< 8 3 12)` returns `3`, the smallest value — not `True`/`False`. A real Lisp would return a boolean.
2. **`=` is not wired up.** `tools.equal` exists but is missing from the `stock` dictionary, so `(= 1 1)` returns `"Unknown Operator"`.
3. **Empty input crashes.** Pressing Enter on a blank line makes `READ` index `info[0]` on an empty string and raise `IndexError`.
4. **Parenthesis checking is shallow.** Only the first and last character are inspected, so `(+ 1 (* 2 3)` is not caught by `ParenthesisError`.
5. **`def!` with several names in one call is unreliable** — the index used to write into `environment` is the position in the full argument list, not in the list of names.
6. **No user-defined functions.** There is no `fn*` form yet, so the operator set is fixed to the contents of `stock`.
7. **No string type.** Anything that is not numeric is treated as a symbol.

---

## Extending it

To add an operator:

1. Write the function in `tools.py`. It must take a single argument: the list of already-evaluated arguments.
2. Register it in `stock` in `mal.py` under the symbol you want.

```python
# tools.py
def modulo_function(cal):
    start = cal[0]
    for number in cal[1:]:
        start = start % number
    return start
```

```python
# mal.py
stock = {
    ...
    '%': tools.modulo_function,
}
```

No change to `EVAL` is needed — it looks operators up in `stock` by name.
