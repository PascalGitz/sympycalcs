def subs_recursive(expression, substitution_dict, max_depth=None):
    """
    Substitutes an expression with a given dictionary as many times as the dict is long, or defined in max_depth.
    """
    if max_depth is None:
        max_depth = len(substitution_dict)

    if max_depth == 0:
        return expression

    new_expression = expression.subs(substitution_dict)
    if new_expression == expression:
        return new_expression

    return subs_recursive(new_expression, substitution_dict, max_depth - 1)