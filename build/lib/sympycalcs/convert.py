def param_value(params):
    """Converts the dictionary containing parameters with units to a unitless dictionary.

    Args:
        params (dict): Parameters with units

    Returns:
        dict: Parameters without units in base SI
    """
    from sympy.physics.units import convert_to, m, seconds, N
    parameter_plots = params.copy()

    for units in parameter_plots:
        SI_units = [m,N,seconds]
        if type(parameter_plots[units]) == float:
            parameter_plots[f'{units}'] = convert_to(parameter_plots[units],SI_units)
        else:
            parameter_plots[f'{units}'] = convert_to(parameter_plots[units],SI_units).args[0]

    return parameter_plots

def expr_value(expr, params=False, unit=False):
    from sympy.physics.units import convert_to
    
    if params != False:
        exp = expr.subs(params).simplify().evalf(3)
    
    if unit != False and params!=False:
        exp = convert_to(expr.subs(params).simplify().evalf(3), unit)

    return(exp)

