def pdf_to_svg(dir, delete_original=False):
    import os
    import subprocess

    inkscape_path = r'C:\Program Files\Inkscape\bin\inkscape.exe'
    input_dir = dir
    output_dir = dir

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".svg")
            subprocess.run([inkscape_path, "--export-type=svg", "--pdf-poppler", "-l", f'--export-filename={output_file}', input_file])

            if delete_original:
                os.remove(input_file)

