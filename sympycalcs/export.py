import os

def convert_notebook(notebook_path, output_format="tex", cell_input = True, open=True, standalone=False):
    
    # Define paths for input and output files
    base_path, notebook_name = os.path.split(notebook_path)
    notebook_name_without_ext = os.path.splitext(notebook_name)[0]
    md_path = os.path.join(base_path, notebook_name_without_ext + ".md")
    output_path = os.path.join(base_path, notebook_name_without_ext + "." + output_format)

    if output_format == "tex":
        output_format = "latex"


    # Convert notebook to markdown using nbconvert
    if cell_input==False:
        os.system(f"jupyter nbconvert {notebook_path} --to markdown --no-input ")
    else:
        os.system(f"jupyter nbconvert {notebook_path} --to markdown")


    # Convert markdown to desired output format using Pandoc
    os.system(f"pandoc --listings -f markdown -t {output_format} {md_path} -o {output_path} -F pandoc-crossref --citeproc")
    if standalone==True and output_format != 'docx':
        os.system(f"pandoc --listings -f markdown -t {output_format} {md_path} -s -o {output_path}  -F pandoc-crossref --citeproc")

    # Remove intermediate markdown file
    os.remove(md_path)
    if open ==True:
        os.startfile(output_path)


