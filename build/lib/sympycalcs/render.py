def eq_render(variables, parameters=False, raw_input = True, units=False, sub_input=True):
    
    
    
    """Reads variables in current cell. Displays them as sympy equations.

    Args:
        variables (dict): locals() or globals(). Containing left- and righthandside of the Equation.
        parameters (dict): Substitute all the equations with the given Parameters.
        raw_input (bool, optional): If True an attempt is made of rendering the unsubstituted input via simpify. 
        Parts that cannot be sympified will not get displayed! Defaults to False.
        units (list): An attempt is made of converting the numeric value to the given units. Each index of the list corresponds to a variable in the cell.
    """
    
    #Functionimport
    import io
    from contextlib import redirect_stdout
    from sympy import Eq, Symbol, sympify

    offset=0
    local_vars = variables
    ipy = get_ipython()
    out = io.StringIO()

    with redirect_stdout(out):
        ipy.run_line_magic("history", format(ipy.execution_count - offset))


    
    # Class for equations with its parts
    class equation:
        def __init__(self, diction) -> None:
            self.dict = diction
            self.symbols = list(diction.keys())
            self.values = list(diction.values())
            pass


    #process each line...
    each_line = out.getvalue().replace(" ", "").split("\n")
    
    # save the the variable name and input as a string for left and righthandside
    Eq_raw_rhs = [a.split("=")[1].replace("sp.", "").replace("u.","") for a in each_line if "=" in a]
    Eq_raw_lhs = [a.split("=")[0] for a in each_line if "=" in a]

    #Create normal Equation 
    subs = equation({k:local_vars[k] for k in Eq_raw_lhs if k in local_vars})    




    # Add all Equations to a list and iterate trough it. It guarantees that the order of the Equations is correct.
    Eq_tot =[]   

    for i in range(0,len(subs.symbols)):

        # Raw input Equations with sympify
        if raw_input != False:
            try:
                Eq_raws = []
                for j in range(0,len(Eq_raw_rhs)):
                    Eq_raw = Eq(Symbol(Eq_raw_lhs[j]), sympify(Eq_raw_rhs[j]))
                    Eq_raws.append(Eq_raw)
            except:
                pass
            Eq_tot.append(Eq_raws[i])
        

        # Normal Equation with Variablename and its substitution
        if sub_input != False:
            Eq_subs = []
            for j in range(0,len(subs.symbols)):
                Eq_sub = Eq(Symbol(f'{subs.symbols[j]}'), subs.values[j])
                Eq_subs.append(Eq_sub)
            Eq_tot.append(Eq_subs[i])
        
        # Equation with substituted Parameters
        if parameters!=False:
            from sympy.physics.units import convert_to
            Eq_params = []
            for j in range(0,len(subs.symbols)):
                    Eq_param = Eq(Symbol(f'{subs.symbols[j]}'), subs.values[j]).subs(parameters).simplify().evalf(3)
                    try:
                        Eq_params.append(convert_to(Eq_param, units[j]))
                    except:
                        Eq_params.append(Eq_param)
        
            Eq_tot.append(Eq_params[i])

            
    
    ## Removing duplicates
    Eq_tot = list(dict.fromkeys(Eq_tot))

    ## Display the Each Equation
    for Eq in Eq_tot:
        display(Eq)
    

    if parameters!=False:
        Eq_params_rhs =[]
        for Eq in Eq_params:
            Eq_params_rhs.append(Eq.rhs)
        if len(Eq_params_rhs)>1:
            Eq_params_rhs = tuple(Eq_params_rhs)
        else:
            Eq_params_rhs = Eq_params_rhs[0]


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




def eq_display(*args):

    from sympy import sympify, Eq

    from IPython.display import display
    for i in range(0, len(args), 2):
        lhs = sympify(args[i]) if isinstance(args[i], str) else args[i]
        rhs = sympify(args[i+1]) if isinstance(args[i+1], str) else args[i+1]
        display(Eq(lhs,rhs))