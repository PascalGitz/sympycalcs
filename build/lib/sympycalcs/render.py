def eq_render(variables):
    """Renders all the variables in the current cell in a sympy Equation

    Args:
        variables (locals() or globals()): needs to be the globals in the current Notebook. For that it has to be a function input.
    """
    import io
    from contextlib import redirect_stdout
    from sympy import Eq, Symbol, sympify

    offset=0

    ipy = get_ipython()
    out = io.StringIO()

    with redirect_stdout(out):
        ipy.run_line_magic("history", format(ipy.execution_count - offset))

    #process each line...
    x = out.getvalue().replace(" ", "").split("\n")
    Eq_raw_rhs = [a.split("=")[1] for a in x if "=" in a]
    Eq_raw_lhs = [a.split("=")[0] for a in x if "=" in a]
    
    Eq_raws = []
    for i in range(0,len(Eq_raw_rhs)):
        Eq_raw = Eq(Symbol(Eq_raw_lhs[i]), sympify(Eq_raw_rhs[i]))
        Eq_raws.append(Eq_raw)

    x = [a.split("=")[0] for a in x if "=" in a] #all of the variables in the cell

    g = variables

    # Class for equations with its parts
    class equation:
        def __init__(self, diction) -> None:
            self.dict = diction
            self.symbols = list(diction.keys())
            self.values = list(diction.values())
            pass


    subs = equation({k:g[k] for k in x if k in g})    

    Eq_subs = []
    ## raw equations
    for i in range(0,len(subs.symbols)):
        Eq_sub = Eq(Symbol(f'{subs.symbols[i]}'), subs.values[i])
        Eq_subs.append(Eq_sub)

    Eq_tot =[]   
    for i in range(0,len(Eq_raws)):
        Eq_tot.append(Eq_raws[i])
        Eq_tot.append(Eq_subs[i])

    Eq_tot = list(dict.fromkeys(Eq_tot))
    # print(Eq_tot)
    for Eq in Eq_tot:
        display(Eq)



def dict_render(params):
    """renders a dictionary containing the parameters

    Args:
        params (dict): Parameters for substitution
    """
    from sympy import Eq, Symbol
    symbols = list(params.keys())
    values = list(params.values())

    for i in range(0,len(symbols)):
        display(Eq(Symbol(f'{symbols[i]}'), values[i]))   