"""
Outils mathématiques pour GMBot (SymPy)
"""

import sympy as sp
from sympy import symbols, Eq, solve, simplify, expand, factor, diff, integrate, limit, series
from sympy.parsing.sympy_parser import parse_expr


def solve_equation(equation_str: str, variable: str = "x"):
    """Résout une équation"""
    x = symbols(variable)
    try:
        if "=" in equation_str:
            left, right = equation_str.split("=")
            eq = Eq(parse_expr(left.strip()), parse_expr(right.strip()))
        else:
            eq = Eq(parse_expr(equation_str), 0)
        solutions = solve(eq, x)
        return solutions
    except Exception as e:
        return f"Erreur de résolution : {e}"


def compute_derivative(expr_str: str, variable: str = "x", order: int = 1):
    """Calcule la dérivée"""
    x = symbols(variable)
    expr = parse_expr(expr_str)
    return diff(expr, x, order)


def compute_integral(expr_str: str, variable: str = "x", definite=False, bounds=None):
    """Calcule l'intégrale"""
    x = symbols(variable)
    expr = parse_expr(expr_str)
    if definite and bounds:
        return integrate(expr, (x, bounds[0], bounds[1]))
    return integrate(expr, x)


def simplify_expression(expr_str: str):
    """Simplifie une expression"""
    expr = parse_expr(expr_str)
    return simplify(expr)


if __name__ == "__main__":
    print(solve_equation("2*x + 3 = 7"))
    print(compute_derivative("x**3 + 2*x"))
    print(compute_integral("x**2 * exp(x)"))
