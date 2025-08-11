class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        postfix = self._infix_to_postfix(tokens)
        return self._evaluate_postfix(postfix)

    def _infix_to_postfix(self, tokens):
        output = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  
            else:
                try:
                    output.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            output.append(operators.pop())

        return output

    def _evaluate_postfix(self, tokens):
        stack = []
        for token in tokens:
            if token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Not enough operands")
                operand2 = stack.pop()
                operand1 = stack.pop()
                result = self.operators[token](operand1, operand2)
                stack.append(result)
            else:
                stack.append(float(token))

        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return stack[0]