# sympycalcs

I'm using sympy to create human readable and especially reproducable calculations exlusively in the output. My workflow consists of creating Jupyter-Notebooks that get converted via [Quarto](https://quarto.org/) into PDFs.
To increase implementation speed and convenience I created sympycalcs. 

## Algebra_with_sympy

My package is highly influenced by [Algebra_with_sympy](https://github.com/gutow/Algebra_with_Sympy). I straight away copied the Equation class, which is the core of sympycalcs.
As I'm working solely in Jupyter-Notebooks I skipped the parts that focus on different environments, in contrast to [gutows](https://github.com/gutow) approach, which in my opinion keeps my package more lightweight.

## Additional features
While working with basic sympy I struggled to the generated expressions in a convenient way.
-  For that I added some display functions (in Markdown tables or latex equations)
-  Function that converts my parameters into SI-units and then removes the units. This helps for generating plots.
-  Useful for my workflow was to convert PDFs to SVG, as i drew pictures in a CAD software, that was only capable of exporting PDFs efficiently. In notebooks it is prefered to work with svg.
- the Beton module is only in testing phase, since I'm looking a way to predefine heavily used calculations in structural engineering.

