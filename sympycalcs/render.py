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





