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

    # Class for equations with its parts
    class equation:
        def __init__(self, diction) -> None:
            self.dict = diction
            self.symbols = list(diction.keys())
            self.values = list(diction.values())
            pass


    raw = equation({k:g[k] for k in x if k in g})    
    subs = equation({g[k]:k for k in x if k in g})

    Eq_raws = []
    ## raw equations
    for i in range(0,len(raw.symbols)):
        Eq_raw = Eq(Symbol(f'{raw.symbols[i]}'), raw.values[i])
        Eq_raws.append(Eq_raw)

    ## Backsubsitution
    Eq_subs = []

    # for i in range(0,len(raw.symbols)):
    #     Eq_sub = Eq(Symbol(f'{raw.symbols[i]}'), raw.values[i]).subs(subs.dict)
    #     Eq_subs.append(Eq_sub)


    def remove_value(dict, value):
        for key in list(dict.keys()):
            if dict[key] == value:
                dict.pop(key)
                return key
        raise ValueError('value not found in dictionary')
    
    
    for j in range(0,len(raw.symbols)):
        for i in range(0,len(raw.symbols)):

            symbol_subs = list(dict([list(subs.dict.items())[i]]).values())[0]
            
            # print(symbol_subs, dict_subs)
            if Eq_raws[j].lhs != symbol_subs: 
                subs_dict = subs.dict.copy()
                remove_value(subs_dict, symbol_subs)

                Eq_sub = Eq_raws[j].subs(subs_dict)
                # print(Eq_sub)$

            if Eq_sub!=True:
                Eq_subs.append(Eq_sub)

    Eq_tot = list(dict.fromkeys(Eq_subs + Eq_raws))
    print(raw.dict, "\n",subs.dict)
    for Eqs in Eq_tot:
        display(Eqs)


    


import sympy as sp

a = sp.symbols("a")
b = sp.cos(a)
c = sp.sin(b)

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