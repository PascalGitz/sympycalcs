import sympy
import numpy
from sympy.physics.units import convert_to, N,  m, second, degree, rad
from IPython.display import display, Markdown

from typing import Dict
import subprocess
import os





def eq_subs(target_eq, *substitution_eqs):
    """
    Substitute variables in the target equation using the provided substitution equations.

    Parameters:
    target_eq (sympy.Eq): The equation in which variables will be substituted.
    substitution_eqs (sympy.Eq): The equations representing the substitutions to be made.

    Returns:
    sympy.Eq: The target equation with variables substituted.

    Example:
    >>> from sympy import symbols, Eq
    >>> x, y, z = symbols('x y z')
    >>> eq1 = Eq(x + y, z)
    >>> eq2 = Eq(x, 2)
    >>> eq_subs(eq1, eq2)
    Eq(2 + y, z)
    """
    for eq in substitution_eqs:
        target_eq = target_eq.subs(eq.lhs, eq.rhs)           
    return target_eq

def display_eq(lhs:str = 'x', rhs = 20):
    display(sympy.Eq(sympy.Symbol(lhs), rhs))

def type_application(exprs, func):
    if isinstance(exprs,(numpy.ndarray)):  
        result = [] 

        for expr in exprs:
            result.append(func(expr))   

        return numpy.array(result).astype(float)
    
    if isinstance(exprs, (dict)):
        result_dict = {}

        for key, value in exprs.items():
            result_dict[key] = func(value)

        return result_dict

    if isinstance(exprs, (sympy.core.relational.Equality)):
        lhs = func(exprs.lhs)
        rhs = func(exprs.rhs)
        return sympy.Eq(lhs, rhs)
    
    else:
        return transformation(exprs)
    

def to_float(exprs, base_units=[m,N,second, rad]):
    """
    Converts expressions to their numerical float values.

    Args:
        exprs: The expression(s) to be converted to float.
        base_units: The base units to be used for conversion. Default is [m, N, second, degree].

    Returns:
        The numerical float value(s) of the input expression(s).

    Raises:
        None.

    Examples:
        >>> to_float(5*m)
        5.0
        >>> to_float([2*N, 3*m])
        array([2.0, 3.0])
        >>> to_float({'force': 10*N, 'length': 2*m})
        {'force': 10.0, 'length': 2.0}
    """

    def transformation(expr):
        if isinstance(expr, (sympy.core.mul.Mul, sympy.core.add.Add)):
            expr_si_base = convert_to(expr, base_units)            
            replacements = [(base_units[i], 1)for i in range(len(base_units))]                
            expr_numerical = float(expr_si_base.subs(replacements))                     
            return expr_numerical
        else:
            return expr
    type_application(exprs, transformation)
    


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

    

    sorted_items = sorted(d.items(), key=lambda item: str(item[0]))  # Sort keys alphabetically
    n = len(sorted_items)
    table = "|  Parameter  | \u200B  |\n|---|---|\n"    
    for i, (key, value) in enumerate(sorted_items):
        if isinstance(key, str):
            key_sym = sympy.Symbol(key)  # Create a custom symbol from the string
        else:
            key_sym = key  # Use the key directly if it's already a symbol

        # Call eq_pretty_units to format the equation with units
        formatted_equation = sympy.latex(sympy.Eq(key_sym, value))

        table += f"| ${formatted_equation}$ "
        if i % 2 == 1:
            table += "|\n"
    if n % 2 == 1:
        table += "| \u200B  |\n"
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



