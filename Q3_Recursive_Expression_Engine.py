"""Q3: Integer expression evaluator with variables, memoization and cycle detection."""
import re
import sys


class InvalidExpression(Exception):
    pass


class CycleDetected(Exception):
    pass


TOKEN_RE = re.compile(r"\s*(\d+|[A-Za-z_]\w*|[()+*-])")


class Parser:
    def __init__(self, text, resolve_name):
        self.tokens = []
        pos = 0
        while pos < len(text):
            match = TOKEN_RE.match(text, pos)
            if not match:
                if text[pos:].strip() == "":
                    break
                raise InvalidExpression
            self.tokens.append(match.group(1))
            pos = match.end()
        self.index = 0
        self.resolve_name = resolve_name

    def peek(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def take(self):
        token = self.peek()
        if token is not None:
            self.index += 1
        return token

    def parse(self):
        value = self.expression()
        if self.peek() is not None:
            raise InvalidExpression
        return value

    def expression(self):
        value = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def term(self):
        value = self.factor()
        while self.peek() == "*":
            self.take()
            value *= self.factor()
        return value

    def factor(self):
        token = self.take()
        if token is None:
            raise InvalidExpression
        if token.isdigit():
            return int(token)
        if token == "(":
            value = self.expression()
            if self.take() != ")":
                raise InvalidExpression
            return value
        if re.fullmatch(r"[A-Za-z_]\w*", token):
            return self.resolve_name(token)
        raise InvalidExpression


def main():
    try:
        v = int(sys.stdin.readline())
        if v < 1:
            raise ValueError
        definitions = {}
        for _ in range(v):
            line = sys.stdin.readline().strip()
            if "=" not in line:
                raise InvalidExpression
            name, expression = map(str.strip, line.split("=", 1))
            if not re.fullmatch(r"[A-Za-z_]\w*", name) or not expression:
                raise InvalidExpression
            definitions[name] = expression
        target = sys.stdin.readline().strip()
        if not target:
            raise InvalidExpression
    except (ValueError, InvalidExpression):
        print("INVALID")
        return

    memo = {}
    visiting = set()

    def resolve(name):
        if name not in definitions:
            raise InvalidExpression
        if name in memo:
            return memo[name]
        if name in visiting:
            raise CycleDetected
        visiting.add(name)
        value = Parser(definitions[name], resolve).parse()
        visiting.remove(name)
        memo[name] = value
        return value

    try:
        print(Parser(target, resolve).parse())
    except CycleDetected:
        print("CYCLE")
    except (InvalidExpression, RecursionError):
        print("INVALID")


if __name__ == "__main__":
    main()
