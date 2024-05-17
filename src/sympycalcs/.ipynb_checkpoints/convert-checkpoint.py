

def param_value(input_dict):
    """Converts the dictionary containing parameters with units to a unitless dictionary.

    Args:
        input_dict (dict): Parameters with units

    Returns:
        dict: Parameters without units in base SI
    """
    from sympy.physics.units import convert_to, m, second, N
    from sympy import Mul

    result_dict = {}
    base_units = [N,m,second]  # Beispielhafte Liste der SI-Basiseinheiten
    
    for key, value in input_dict.items():
        converted_value = convert_to(value, base_units)
        
        if isinstance(converted_value, Mul):
            numeric_factor = converted_value.args[0]
            unit_factor = Mul(*converted_value.args[1:])
        else:
            numeric_factor = converted_value
            unit_factor = 1
        
        result_dict[key] = numeric_factor
        
    return result_dict




def expr_value(expr, params=False, unit=False):
    from sympy.physics.units import convert_to
    
    if params != False:
        exp = expr.subs(params).simplify().evalf(3)
    
    if unit != False and params!=False:
        exp = convert_to(expr.subs(params).simplify().evalf(3), unit)

    return(exp)

