def m_cr():
    """Zeigt die Berechnung des Rissmoments für einen Rechteckquerschnitt.
    returns the calculations as a tuple.
    """
    ## Function import
    from sympy import symbols, Rational, Eq, Symbol
    from sympy.physics.units import convert_to, m
    import render as rend
    from IPython.display import display,Markdown

    ## define the Symbol outside of the function, otherwise it will get rendered as True
    h, f_ctm = symbols("h, f_ctm")

    
    display(Markdown("""
Berechnung des Rissmoments nach Skript **Karel Thoma Stahlbetonbau 2019**.\n
$t$ entspricht der Höhe des Zuggurts"""))

    t = h*Rational(1,3)
    k_t = 1/(1+Rational(1,2)*convert_to(t,m)/m)
    f_ctd=k_t*f_ctm
    m_cr = h**2 /6 * f_ctd

    rend.param_render(locals())
    
    return(t, k_t, f_ctd, m_cr)
