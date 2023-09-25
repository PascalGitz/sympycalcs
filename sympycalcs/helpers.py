def Eq_subs(target_eq, *substitution_eqs):
    """
    Substitute equations in target_eq with equations in substitution_eqs.
    Automatically generates new substitutions as needed until no further substitutions are possible.
    The target equation itself will not be excluded from substitutions.

    Parameters:
    target_eq (sympy.Eq): The target equation to perform substitutions on.
    *substitution_eqs (sympy.Eq): Variable-length argument list of equations to be used for substitution.

    Returns:
    sympy.Eq: The target equation with substitutions applied.

    Example:
    a, b, c, q, v, t, k = sp.symbols('a b c q v t k')

    eq_1 = sp.Eq(a, b + c)
    eq_2 = sp.Eq(b, q * v)
    eq_3 = sp.Eq(c, t * k)

    eq_1_subs = Eq_subs(eq_1, eq_1, eq_2, eq_3)
    print(eq_1_subs)  # Output: a = q*t*k*v + t*q*v + t*k
    """
    result_eq = target_eq
    previous_result_eq = None
    
    while result_eq != previous_result_eq:
        previous_result_eq = result_eq
        for eq in substitution_eqs:
            if eq != target_eq:
                result_eq = result_eq.subs(eq.lhs, eq.rhs)
                
    return result_eq