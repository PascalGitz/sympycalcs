from sympy.physics.units import convert_to, N,  m, second
from sympy import Mul, Eq, Symbol, latex, sympify
from IPython.display import display, Latex, Markdown
import os
import subprocess


def eq_subs(target_eq, *substitution_eqs):
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

    eq_1_subs = eq_subs(eq_1, eq_1, eq_2, eq_3)
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

    Args:
        params (dict): Parameters for substitution, where keys are symbols and values are numeric values.
        
    Example:
    params = {'a': 3, 'b': 5, 'c': 7}
    
    dict_render(params)
    # Displays:
    # a = 3
    # b = 5
    # c = 7
    """


    symbols = list(params.keys())
    values = list(params.values())

    for i in range(len(symbols)):
        display(Eq(Symbol(symbols[i]), values[i]))




def eq_pretty_units(equation, unit=None):
    """
    Format a SymPy equation with an optional specified unit and return it as a LaTeX string.

    Args:
        equation (sympy.Eq): The SymPy equation to format.
        unit (str, optional): The unit string to append to the equation. Default is None.

    Returns:
        str: LaTeX-formatted equation with the specified unit (if provided).

    Example:
    equation = Eq(a, b + c)
    
    # Without unit
    latex_equation = eq_pretty_units(equation)
    # Output: '\\begin{align}a = b + c\\end{align}'
    
    # With unit
    latex_equation = eq_pretty_units(equation, unit='m/s^2')
    # Output: '\\begin{align}a = b + c\\, \\mathrm{m/s^2}\\end{align}'
    """


    if unit is None:
        units = latex(equation.rhs.subs(equation.rhs.args[0], 1))
    else:
        units = fr'\mathrm{{{unit}}}'
        
    formatted_equation_latex_sympy = latex(Eq(equation.lhs, equation.rhs.args[0]))
    formatted_equation_latex = fr"\begin{{align}}{formatted_equation_latex_sympy} \, {units} \end{{align}}"
    
    return Latex(formatted_equation_latex)




def dict_to_table(d):
    """
    Create a markdown table from a dictionary with two rows and sort the keys alphabetically.

    Args:
        d (dict): Dictionary containing equations or values.

    Example:
    d = {'a': Eq(x, y), 'b': 42, 'c': Eq(z, w)}
    
    dict_to_table(d)
    # Displays a formatted markdown table of the dictionary entries.
    """

    
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




def eq_display(*args):
    """
    Simple display of a SymPy equation. Takes pairs of arguments where the first argument is the left-hand side (LHS)
    of the equation, and the second argument is the right-hand side (RHS).

    Args:
        *args: Variable-length argument list of LHS and RHS pairs for equations.

    Example:
    eq_display('x', '2*x + 3')
    # Displays the equation x = 2*x + 3.
    """


    for i in range(0, len(args), 2):
        lhs = sympify(args[i]) if isinstance(args[i], str) else args[i]
        rhs = sympify(args[i + 1]) if isinstance(args[i + 1], str) else args[i + 1]
        display(Eq(lhs, rhs))


def pdf_to_svg(input_dir, output_dir=None, delete_original=False, inkscape_path=None):
    """
    Convert PDF files in the specified directory to SVG format using Inkscape.

    Args:
        input_dir (str): The directory containing the PDF files to be converted.
        output_dir (str, optional): The directory where the SVG files will be saved.
            If None, SVG files will be saved in the same directory as the input PDF files.
        delete_original (bool, optional): Whether to delete the original PDF files after conversion. Default is False.
        inkscape_path (str, optional): The path to the Inkscape executable. If not provided, a default path is used.

    Example:
    pdf_to_svg('pdf_files', output_dir='svg_files', delete_original=True, inkscape_path='/path/to/inkscape')
    # Converts PDF files in 'pdf_files' directory to SVG format, saves in 'svg_files', and deletes the original PDFs.
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





