"""Q7: Interactive calculator with distinct custom exceptions."""
import re


class FormulaError(Exception):
    pass


class InvalidFormatError(FormulaError):
    pass


class UnknownVariableError(FormulaError):
    pass


class DivisionByZeroError(FormulaError):
    pass


class UnsupportedOperatorError(FormulaError):
    pass


NUMBER = r"(?:\d+(?:\.\d*)?|\.\d+)"
OPERAND = rf"(?:{NUMBER}|[A-Za-z_]\w*)"
FORMULA_RE = re.compile(rf"^\s*({OPERAND})\s*([^\s])\s*({OPERAND})\s*$")
ASSIGNMENT_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*(.*?)\s*$")


def value_of(token, variables):
    if re.fullmatch(NUMBER, token):
        return float(token) if "." in token else int(token)
    if token in variables:
        return variables[token]
    raise UnknownVariableError(f"Unknown variable: {token}")


def calculate(left, operator, right):
    if operator not in {"+", "-", "*", "/", "%"}:
        raise UnsupportedOperatorError(f"Unsupported operator: {operator}")
    if operator in {"/", "%"} and right == 0:
        raise DivisionByZeroError("Division by zero")
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        return left / right
    return left % right


def main():
    variables = {}
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        if line.casefold() == "quit":
            break
        if not line:
            continue

        assignment = ASSIGNMENT_RE.fullmatch(line)
        if assignment:
            name, expression = assignment.groups()
            if re.fullmatch(NUMBER, expression):
                variables[name] = float(expression) if "." in expression else int(expression)
            else:
                print("InvalidFormatError: Assignments must contain a numeric value.")
            continue

        match = FORMULA_RE.fullmatch(line)
        if not match:
            print("InvalidFormatError: Expected operand operator operand.")
            continue

        left_token, operator, right_token = match.groups()
        try:
            left = value_of(left_token, variables)
            right = value_of(right_token, variables)
            result = calculate(left, operator, right)
            print(f"{result:g}" if isinstance(result, float) else result)
        except FormulaError as exc:
            print(f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
