from sympy.physics.units import convert_to, N,  m, second
from sympy import Mul, Eq, Symbol, latex, sympify
from IPython.display import display, Latex, Markdown
from typing import Dict

import os
import subprocess


def eq_subs(target_eq, *substitution_eqs):
    """
    Substitute equations in target_eq with equations in substitution_eqs.
    
    Automatically generates new substitutions as needed until no further substitutions are possible.
    The target equation itself will not be excluded from substitutions.

    Parameters
    ----------
    target_eq : sympy.Eq
        The target equation to perform substitutions on.
    *substitution_eqs : variable-length arguments of sympy.Eq
        Equations to be used for substitution.

    Returns
    -------
    sympy.Eq
        The target equation with substitutions applied.

    Example
    -------
    a, b, c, q, v, t, k = symbols('a b c q v t k')

    eq_1 = Eq(a, b + c)
    eq_2 = Eq(b, q * v)
    eq_3 = Eq(c, t * k)

    eq_1_subs = eq_subs(eq_1, eq_1, eq_2, eq_3)

    Notes
    -----
    - This function iteratively applies substitutions to the target equation using the provided substitution equations.
    - It continues to generate new substitutions until no further substitutions are possible.
    - The target equation itself is not excluded from substitutions.
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

    Parameters
    ----------
    input_dict : dict
        Parameters with units.
    base_units : list of sympy.physics.units.*, optional
        List of base SI units. Defaults to [N, m, second].

    Returns
    -------
    dict
        Parameters without units in base SI units.

    Example
    -------
    >>> input_dict = {'mass': 5 * kg, 'distance': 3 * m, 'time': 2 * s}
    >>> base_units = [N, m, s]
    >>> result = param_value(input_dict, base_units)
    Output: {'mass': 5, 'distance': 3, 'time': 2}

    Notes
    -----
    - This function converts a dictionary of parameters with units to unitless values in base SI units.
    - It uses SymPy's `convert_to` function to perform unit conversions.
    - Default base SI units are [N, m, second], but you can specify custom units as needed.
    """
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
    """
    Render a dictionary containing parameter substitutions as SymPy equations.

    Parameters
    ----------
    params : dict
        Parameters for substitution, where keys are symbols and values are numeric values.
        
    Example
    -------
    >>> params = {'a': 3, 'b': 5, 'c': 7}
    >>> dict_render(params)
    Displays:
    a = 3
    b = 5
    c = 7

    Notes
    -----
    - This function converts a dictionary of parameter substitutions into SymPy equations.
    - The keys of the dictionary are treated as symbols, and the values are treated as their numeric values.
    """
    symbols = list(params.keys())
    values = list(params.values())

    for i in range(len(symbols)):
        display(Eq(Symbol(symbols[i]), values[i]))




def eq_pretty_units(equation, unit=None):
    """
    Format a SymPy equation with an optional specified unit and return it as a LaTeX string.

    Parameters
    ----------
    equation : sympy.Eq
        The SymPy equation to format.
    unit : str, optional
        The unit string to append to the equation. Default is `None`.

    Returns
    -------
    str
        LaTeX-formatted equation with the specified unit (if provided).

    Examples
    --------
    >>> equation = Eq(a, b + c)
    
    # Without unit
    >>> latex_equation = eq_pretty_units(equation)
    Output: '\\begin{align}a = b + c\\end{align}'
    
    # With unit
    >>> latex_equation = eq_pretty_units(equation, unit='m/s^2')
    Output: '\\begin{align}a = b + c\\, \\mathrm{m/s^2}\\end{align}'

    Notes
    -----
    - If no unit is provided, the function attempts to extract the unit from the right-hand side.
    - The returned LaTeX string is wrapped in the 'align' environment.
    """
    if unit is None:
        units = latex(equation.rhs.subs(equation.rhs.args[0], 1))
    else:
        units = fr'\mathrm{{{unit}}}'

    formatted_equation_latex_sympy = latex(Eq(equation.lhs, equation.rhs.args[0]))
    formatted_equation_latex = fr"\begin{{align}}{formatted_equation_latex_sympy} \, {units} \end{{align}}"
    
    return Latex(formatted_equation_latex)




def dict_to_table(d: Dict):
    """
    Create a Markdown table from a dictionary, with sorted keys in alphabetical order.

    Parameters
    ----------
    d : dict
        Dictionary containing equations or values.

    Example
    -------
    >>> d = {'a': Eq(x, y), 'b': 42, 'c': Eq(z, w)}
    >>> dict_to_table(d)
    Displays a formatted Markdown table of the dictionary entries.

    Notes
    -----
    - This function formats equations with specified units using LaTeX.
    - The keys are sorted alphabetically for consistent table order.
    """

    def eq_pretty_units(equation):
        """
        Format a SymPy equation with a specified unit and return it as a LaTeX string.

        Parameters
        ----------
        equation : sympy.Eq
            The SymPy equation to format.

        Returns
        -------
        str
            LaTeX-formatted equation with the specified unit.
        """
        if equation.rhs.args:
            units = latex(equation.rhs.subs(equation.rhs.args[0], 1))
            equation_rhs = equation.rhs.args[0]
        else:
            units = ""
            equation_rhs = equation.rhs
        

        formatted_equation_latex_sympy = latex(Eq(equation.lhs, equation_rhs))
        formatted_equation_latex = fr"${formatted_equation_latex_sympy} \, {units}$"
        return formatted_equation_latex

    sorted_items = sorted(d.items(), key=lambda item: str(item[0]))  # Sort keys alphabetically
    n = len(sorted_items)
    table = "|   |   |\n|---|---|\n"
    for i, (key, value) in enumerate(sorted_items):
        if isinstance(key, str):
            key_sym = Symbol(key)  # Create a custom symbol from the string
        else:
            key_sym = key  # Use the key directly if it's already a symbol

        # Call eq_pretty_units to format the equation with units
        formatted_equation = eq_pretty_units(Eq(key_sym, value))

        table += f"| {formatted_equation} "
        if i % 2 == 1:
            table += "|\n"
    if n % 2 == 1:
        table += "| |\n"
    display(Markdown(table))





def pdf_to_svg(input_dir, output_dir=None, delete_original=False, inkscape_path=None):
    """
    Convert PDF files in the specified directory to SVG format using Inkscape.

    Parameters
    ----------
    input_dir : str
        The directory containing the PDF files to be converted.
    output_dir : str, optional
        The directory where the SVG files will be saved. If not specified, SVG files
        will be saved in the same directory as the input PDF files.
    delete_original : bool, optional
        Whether to delete the original PDF files after conversion. Default is `False`.
    inkscape_path : str, optional
        The path to the Inkscape executable. If not provided, a default path is used.

    Examples
    --------
    >>> pdf_to_svg('pdf_files', output_dir='svg_files', delete_original=True, inkscape_path='/path/to/inkscape')
    
    Converts PDF files in 'pdf_files' directory to SVG format.
    
    - Saves the resulting SVG files in 'svg_files'.
    - Deletes the original PDF files if `delete_original` is set to `True`.
    - Requires Inkscape installed at the specified `inkscape_path` or a default path.

    Notes
    -----
    - Make sure to specify the correct path to the Inkscape executable.
    - The `--pdf-poppler` option in Inkscape is used for PDF conversion.

    """
    if inkscape_path is None:
        # Default Inkscape executable path (update this to your Inkscape installation path)
        inkscape_path = r'C:\Program Files\Inkscape\bin\inkscape.exe'

    if output_dir is None:
        output_dir = input_dir

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".svg")
            
            subprocess.run([inkscape_path, "--export-type=svg", "--pdf-poppler", "-l", f'--export-filename={output_file}', input_file])

            if delete_original:
                os.remove(input_file)







