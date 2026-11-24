# Configuration file for the Sphinx documentation builder.
# Documentation of all options: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = "Company Handbook"
author = "Example Company GmbH"
copyright = "2026, Example Company GmbH"
version = "1.0"
release = "1.0"
language = "en"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",          # read Markdown files
]
source_suffix = {".md": "markdown"}
root_doc = "index"
exclude_patterns = ["_build", ".venv", "README.md"]

# MyST (Markdown) extensions
myst_enable_extensions = [
    "colon_fence",          # ::: fences for notes and warnings
    "deflist",              # definition lists
    "tasklist",             # - [ ] and - [x] checklists
    "attrs_inline",         # image attributes: ![text](file.png){width=80%}
]
myst_heading_anchors = 3    # allow links to headings down to level 3

# -- HTML output -------------------------------------------------------------
html_theme = "furo"
html_title = "Company Handbook"
html_logo = "images/logo-full.png"

# -- ePub output -------------------------------------------------------------
epub_title = "Company Handbook"
epub_author = "Example Company GmbH"
epub_cover = ("images/logo-full.png", "")

# -- PDF output (LaTeX) ------------------------------------------------------
latex_engine = "xelatex"
latex_documents = [
    # (start file, output name, title, author, document class)
    ("index", "handbook.tex", "Company Handbook", "Example Company GmbH", "manual"),
]
latex_logo = "images/logo-full.png"      # logo on the title page
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "extraclassoptions": "openany,oneside",   # no blank pages between chapters
    "fontpkg": r"""
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
""",
    # logo in the top right of every page
    "preamble": r"""
\setlength{\headheight}{1.6cm}
\fancypagestyle{normal}{
  \fancyhf{}
  \fancyhead[L]{\small\textcolor{gray}{Company Handbook}}
  \fancyhead[R]{\includegraphics[height=1.0cm]{logo-full.png}}
  \fancyfoot[C]{\small\thepage}
  \renewcommand{\headrulewidth}{0.4pt}
}
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyhead[R]{\includegraphics[height=1.0cm]{logo-full.png}}
  \fancyfoot[C]{\small\thepage}
  \renewcommand{\headrulewidth}{0pt}
}
""",
    "sphinxsetup": "hmargin={2.5cm,2.5cm}, vmargin={3.2cm,2.5cm}, marginpar=0pt",
}
