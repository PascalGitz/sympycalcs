def eq_render(variables):
    """Renders all the variables in the current cell in a sympy Equation

    Args:
        variables (locals() or globals()): needs to be the globals in the current Notebook. For that it has to be a function input.
    """
    import io
    from contextlib import redirect_stdout
    from sympy import Eq, Symbol

    offset=0

    ipy = get_ipython()
    out = io.StringIO()

    with redirect_stdout(out):
        ipy.run_line_magic("history", format(ipy.execution_count - offset))

    #process each line...
    x = out.getvalue().replace(" ", "").split("\n")
    x = [a.split("=")[0] for a in x if "=" in a] #all of the variables in the cell
    g = variables

    for k in x:
        if k in g:
            display(Eq(Symbol(k), g[k]))


def param_render(params):
    """renders a dictionary containing the parameters

    Args:
        params (dict): Parameters for substitution
    """
    from sympy import Eq, Symbol
    symbols = list(params.keys())
    values = list(params.values())

    for i in range(0,len(symbols)):
        display(Eq(Symbol(f'{symbols[i]}'), values[i]))   