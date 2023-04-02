def eq_render(variables, parameters=False):
    """Reads all Variables in the current cell. Then displays them as an sympy equation with it's lefthandside as the variable name,
    and the righthandside of the input without substitution. The righthandside is converted via Sympify which does not handle all inputs!
    It then displays the Equation with it's substitution. If the parameters are given, it also displays the Equation with substituted parameters. 


    Args:
        variables (dict): locals() has to be put in!
        parameters (dict, optional): A dictionary containing all the parameters for the subsitution. Defaults to False.

    Returns:
        list: List of Equations with substituted parameters.
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
    
    try:
        Eq_raw_rhs = [a.split("=")[1].replace("sp.", "").replace("u.","") for a in x if "=" in a]
        Eq_raw_lhs = [a.split("=")[0] for a in x if "=" in a]
        
        Eq_raws = []
        for i in range(0,len(Eq_raw_rhs)):
            Eq_raw = Eq(Symbol(Eq_raw_lhs[i]), sympify(Eq_raw_rhs[i]))
            Eq_raws.append(Eq_raw)
    except:
        pass

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

    ## raw equations
    Eq_subs = []
    for i in range(0,len(subs.symbols)):
        Eq_sub = Eq(Symbol(f'{subs.symbols[i]}'), subs.values[i])
        Eq_subs.append(Eq_sub)
    
    #substitution with parameters
    Eq_params = []
    for i in range(0,len(subs.symbols)):
        if parameters!=False:
            Eq_param = Eq(Symbol(f'{subs.symbols[i]}'), subs.values[i]).subs(parameters).simplify().evalf(3)
            Eq_params.append(Eq_param)


    Eq_tot =[]   
    for i in range(0,len(Eq_subs)):
        Eq_tot.append(Eq_raws[i])
        Eq_tot.append(Eq_subs[i])
        if parameters!=False:
            Eq_tot.append(Eq_params[i])


    Eq_tot = list(dict.fromkeys(Eq_tot))
    for Eq in Eq_tot:
        display(Eq)

    #return
    Eq_params_rhs = []
    for Eq in Eq_params:
        Eq_params_rhs.append(Eq.rhs)

    if parameters!= False:
        return Eq_params_rhs



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