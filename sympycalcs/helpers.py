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
    """
    result_eq = target_eq
    previous_result_eq = None
    
    while result_eq != previous_result_eq:
        previous_result_eq = result_eq
        for eq in substitution_eqs:
            if eq != target_eq:
                result_eq = result_eq.subs(eq.lhs, eq.rhs)
                
    return result_eq


def param_value(input_dict, base_units=None):
    """
    Convert a dictionary containing parameters with units to a unitless dictionary in base SI units.

    Args:
        input_dict (dict): Parameters with units.
        base_units (list of sympy.physics.units.*): List of base SI units. Defaults to [N, m, second].

    Returns:
        dict: Parameters without units in base SI units.

    Example:
    input_dict = {'mass': 5 * kg, 'distance': 3 * m, 'time': 2 * s}
    base_units = [N, m, s]

    result = param_value(input_dict, base_units)
    # Output: {'mass': 5, 'distance': 3, 'time': 2}
    """
    from sympy.physics.units import convert_to
    from sympy import Mul

    if base_units is None:
        base_units = [N, m, second]  # Default base SI units

    result_dict = {}

    for key, value in input_dict.items():
        converted_value = convert_to(value, base_units)

        if isinstance(converted_value, Mul):
            numeric_factor = converted_value.args[0]
        else:
            numeric_factor = converted_value

        result_dict[key] = numeric_factor

    return result_dict


def dict_render(params):
    """renders a dictionary containing the parameters

    Args:
        params (dict): Parameters for substitution
    """
    from sympy import Eq, Symbol
    symbols = list(params.keys())
    values = list(params.values())

    for i in range(0,len(symbols)):
        display(Eq(symbols[i], values[i]))   



def eq_pretty_units(equation, unit=None):
    """
    Format a SymPy equation with a specified unit and return it as a LaTeX string.
    
    Args:
        equation (sympy.Eq): The SymPy equation to format.
        unit (str): The unit string to append to the equation.
        equation_number (int): Optional equation number for LaTeX numbering.

    Returns:
        str: LaTeX-formatted equation with the specified unit.
    """
    if unit == None:
        units = latex(equation.rhs.subs(equation.rhs.args[0], 1))
    else:
        units = fr'\mathrm{{{unit}}}'
        
        
    formatted_equation_latex_sympy = latex(Eq(equation.lhs, equation.rhs.args[0]))
    formatted_equation_latex = (
        fr"\begin{{align}}{formatted_equation_latex_sympy} \, {units} \end{{align}}" 
    )
    return Latex(formatted_equation_latex)




def dict_to_table(d):
    """
    Creates a markdown table out of a dict with two rows and sorts the keys alphabetically.
    """
    from sympy import Eq, Symbol, latex
    from IPython.display import display, Markdown
    
    def eq_pretty_units(equation):
        """
        Format a SymPy equation with a specified unit and return it as a LaTeX string.

        Args:
            equation (sympy.Eq): The SymPy equation to format.

        Returns:
            str: LaTeX-formatted equation with the specified unit.
        """
        units = latex(equation.rhs.subs(equation.rhs.args[0], 1))

        formatted_equation_latex_sympy = latex(Eq(equation.lhs, equation.rhs.args[0]))
        formatted_equation_latex = (
            fr"${formatted_equation_latex_sympy} \, {units}$" 
        )
        return formatted_equation_latex

    sorted_items = sorted(d.items(), key=lambda item: str(item[0]))  # Schlüssel alphabetisch sortieren
    n = len(sorted_items)
    table = "|   |   |\n|---|---|\n"
    for i, (key, value) in enumerate(sorted_items):
        if isinstance(key, str):
            key_sym = Symbol(key)  # Benutzerdefiniertes Symbol aus der Zeichenkette erstellen
        else:
            key_sym = key  # Verwende den Schlüssel direkt, wenn es bereits ein Symbol ist
        
        # Call eq_pretty_units to format the equation with units
        formatted_equation = eq_pretty_units(Eq(key_sym, value))
        
        table += f"| {formatted_equation} "
        if i % 2 == 1:
            table += "|\n"
    if n % 2 == 1:
        table += "| |\n"
    display(Markdown(table))


def eq_display(*args):
    """
Simple display of an sympy equation for as many args as desired. First entry Eq1.lhs and second entry is Eq1.rhs, third entry creates Eq2.lhs and fourth entry Eq2.rhs and so on.
    """
    from sympy import sympify, Eq
    from IPython.display import display


    for i in range(0, len(args), 2):
        lhs = sympify(args[i]) if isinstance(args[i], str) else args[i]
        rhs = sympify(args[i+1]) if isinstance(args[i+1], str) else args[i+1]
        display(Eq(lhs,rhs))


def pdf_to_svg(dir, delete_original=False):
    import os
    import subprocess

    inkscape_path = r'C:\Program Files\Inkscape\bin\inkscape.exe'
    input_dir = dir
    output_dir = dir

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".svg")
            subprocess.run([inkscape_path, "--export-type=svg", "--pdf-poppler", "-l", f'--export-filename={output_file}', input_file])

            if delete_original:
                os.remove(input_file)




