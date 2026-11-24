# Sphinx Handbook

Build a handbook from Markdown files with **Sphinx** and the **MyST** parser. One source
creates HTML, PDF, ePub, Qt Help and plain text.

| Example | What it shows | Output |
|---------|---------------|--------|
| [`01_sphinx_example`](01_sphinx_example) | Company handbook with 6 pages, chapters, notes, checklists and a logo in the page header | HTML, PDF (A4), ePub, Qt Help, text |

## Contents

1. [Installation](#1-installation)
2. [Build commands](#2-build-commands)
3. [Folder layout](#3-folder-layout)
4. [The complete conf.py](#4-the-complete-confpy)
5. [conf.py explained](#5-confpy-explained)
6. [Writing pages: MyST Markdown](#6-writing-pages-myst-markdown)
7. [Customize](#7-customize)
8. [Troubleshooting](#8-troubleshooting)
9. [Optional .gitignore](#9-optional-gitignore)

> Run all commands **inside the example folder** (`cd 01_sphinx_example`).

---

## 1. Installation

Tested on Ubuntu 24.04 with Python 3 (Sphinx 9.2, MyST-Parser 5.2, Furo 2025.12).

### 1.1 Python packages

Sphinx is a Python program. Install it in a **virtual environment**:

```bash
sudo apt install python3-venv

cd 01_sphinx_example
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt`:

```text
sphinx>=7.2
myst-parser>=2.0
furo>=2024.1
```

| Package | Meaning |
|---------|---------|
| `sphinx` | The generator |
| `myst-parser` | Lets Sphinx read Markdown files (`.md`) |
| `furo` | A clean HTML theme with search and dark mode |

Check it:

```bash
sphinx-build --version
```

Activate the environment again in every new terminal: `source .venv/bin/activate`.

### 1.2 For PDF output

Sphinx creates the PDF through LaTeX:

```bash
sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended \
                 latexmk make fonts-dejavu
```

### 1.3 For Qt Help (optional)

Sphinx writes the Qt Help project files without extra tools. To compile them into a
`.qch` file you need Qt's help generator:

```bash
sudo apt install qttools5-dev-tools
```

---

## 2. Build commands

The general form is `sphinx-build -M <format> <source folder> <build folder>`.
Here the source folder is `.` and the build folder is `_build`.

| Command | Result |
|---------|--------|
| `sphinx-build -M html . _build` | Website in `_build/html/` (open `index.html`) |
| `sphinx-build -M latexpdf . _build` | PDF in `_build/latex/handbook.pdf` |
| `sphinx-build -M epub . _build` | ePub in `_build/epub/CompanyHandbook.epub` |
| `sphinx-build -M qthelp . _build` | Qt Help project in `_build/qthelp/` |
| `sphinx-build -M text . _build` | Plain text files in `_build/text/` |

All formats at once:

```bash
for f in html latexpdf epub qthelp text; do sphinx-build -M $f . _build; done
```

Compile the Qt Help project to a `.qch` file (needs `qhelpgenerator`, see 1.3):

```bash
cd _build/qthelp
qhelpgenerator CompanyHandbook.qhp -o CompanyHandbook.qch
```

Useful options:

| Option | Meaning |
|--------|---------|
| `-W` | Treat warnings as errors. Good for checking before a release |
| `-q` | Quiet, shows only warnings and errors |
| `-E` | Rebuild everything from scratch (ignore the cache) |

Delete old results with `rm -rf _build`.

---

## 3. Folder layout

```
01_sphinx_example/
├── conf.py                  settings (Python file)
├── requirements.txt
├── index.md                 start page with the table of contents
├── welcome.md
├── working-together.md
├── engineering.md
├── releases-and-support.md
├── onboarding.md
└── images/
    ├── logo-full.png        wide logo (HTML sidebar, PDF, ePub cover)
    ├── logo.png             small square logo
    └── process.png
```

The order of the chapters is set by the `toctree` block in `index.md`:

````markdown
```{toctree}
:maxdepth: 2
:caption: Contents

welcome
working-together
engineering
releases-and-support
onboarding
```
````

Each name is a file without the `.md` ending. The order here is the order in the menu,
in the PDF and in the ePub. A page that is not listed produces a warning.

---

## 4. The complete conf.py

```python
# Configuration file for the Sphinx documentation builder.

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
```

---

## 5. conf.py explained

`conf.py` is a normal Python file. Text after `#` is a comment, and strings are in quotes.

### 5.1 Project information

| Setting | Meaning |
|---------|---------|
| `project` | Name of the handbook (title in HTML and PDF) |
| `author` | Author or company |
| `copyright` | Copyright line in the footer |
| `version`, `release` | Version number, shown on the title page. `version` must not be empty for ePub |
| `language` | Language of generated texts such as "Search" or "Contents" |

### 5.2 General configuration

| Setting | Meaning |
|---------|---------|
| `extensions` | List of extensions. `myst_parser` is needed to read Markdown |
| `source_suffix` | Which file endings are sources, and in which syntax |
| `root_doc` | The start file (without ending). It contains the `toctree` |
| `exclude_patterns` | Files and folders that Sphinx must ignore, for example `_build` and this README |

### 5.3 MyST extensions

| Extension | What it adds |
|-----------|--------------|
| `colon_fence` | Boxes with `:::{note}`, `:::{tip}`, `:::{warning}` |
| `deflist` | Definition lists (term, then `: definition`) |
| `tasklist` | Checklists `- [ ]` and `- [x]` |
| `attrs_inline` | Image attributes such as `{width=80%}` |
| `myst_heading_anchors = 3` | Headings down to level 3 can be linked |

### 5.4 HTML, ePub

| Setting | Meaning |
|---------|---------|
| `html_theme = "furo"` | The theme. The classic alternative is `"sphinx_rtd_theme"` (extra package) |
| `html_title` | Title in the sidebar and the browser tab |
| `html_logo` | Logo at the top of the sidebar |
| `epub_title`, `epub_author` | Metadata of the ePub |
| `epub_cover` | Cover image: `(file, template)`. An empty template string uses the default |

### 5.5 PDF (LaTeX)

| Setting | Meaning |
|---------|---------|
| `latex_engine = "xelatex"` | Use XeLaTeX, which supports system fonts |
| `latex_documents` | One entry per PDF: start file, output name, title, author and document class. `manual` has chapters, `howto` is a short article |
| `latex_logo` | Logo on the title page |
| `papersize`, `pointsize` | A4 paper and 11 pt text |
| `extraclassoptions` | `openany,oneside` removes empty pages between chapters |
| `fontpkg` | Fonts. Must be installed, see `fc-list` |
| `preamble` | Raw LaTeX added before the document. Here it defines the page header with the logo (see below) |
| `sphinxsetup` | Sphinx layout options. `hmargin` and `vmargin` are the side and the top and bottom margins |

The LaTeX in `preamble` works as follows:

| Line | Meaning |
|------|---------|
| `\setlength{\headheight}{1.6cm}` | Reserves room for the logo in the header |
| `\fancypagestyle{normal}{...}` | Redefines the style of normal pages |
| `\fancypagestyle{plain}{...}` | Redefines the style of chapter start pages |
| `\fancyhf{}` | Clears the default header and footer |
| `\fancyhead[L]` / `[R]` | Header left (text) and right (logo) |
| `\fancyfoot[C]` | Footer center (page number) |
| `\renewcommand{\headrulewidth}{...}` | Thickness of the line under the header |

The picture name in LaTeX is the file name only (`logo-full.png`), because Sphinx copies
the images into the LaTeX build folder.

---

## 6. Writing pages: MyST Markdown

Each page starts with one `#` heading. Use `##` and `###` for sections. Besides standard
Markdown these work:

````markdown
:::{note}
A note box.
:::

:::{tip}
A tip box.
:::

:::{warning}
A warning box.
:::

:::{admonition} Own title
A box with a title of your choice.
:::

- [x] Done item
- [ ] Open item

Term
: Definition of the term.

![Caption](images/process.png){width=80%}

[Link to another page](engineering.md)
````

Content only for one output format:

````markdown
```{only} html
This text appears only in the website.
```
````

Use `latex` instead of `html` for PDF-only content.

---

## 7. Customize

| I want to ... | Change |
|---------------|--------|
| Use my own logo | Replace `images/logo-full.png` (same name) |
| Add a page | Create `new-page.md` and add its name to the `toctree` in `index.md` |
| Change the header text in the PDF | The text in `\fancyhead[L]{...}` in `conf.py` |
| Remove the logo from the PDF header | Delete the `\fancyhead[R]` lines |
| Use US Letter | `"papersize": "letterpaper"` |
| Change the fonts | The three lines in `fontpkg` |
| Short article instead of book | Document class `"howto"` in `latex_documents` |
| Switch to German | `language = "de"` |

---

## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `sphinx-build: command not found` | Activate the environment: `source .venv/bin/activate` |
| `Extension error: Could not import extension myst_parser` | `pip install -r requirements.txt` in the active environment |
| `latexmk: command not found` or `make: command not found` | `sudo apt install latexmk make` |
| `The font "DejaVu Serif" cannot be found` | `sudo apt install fonts-dejavu`, or change the names in `fontpkg` |
| `document isn't included in any toctree` | Add the file name to the `toctree` in `index.md`, or add it to `exclude_patterns` |
| `conf value "version" should not be empty for EPUB3` | Set `version = "1.0"` in `conf.py` |
| Picture missing in the PDF | Use a PNG or PDF file. Check the path relative to the page |
| Blank pages in the PDF | Keep `"extraclassoptions": "openany,oneside"` |
| Old content in the output | Delete `_build` and build again |
| Warning `unknown mimetype ... .doctrees` | Use `sphinx-build -M ...` as shown here, which keeps the cache outside the output |

If the PDF fails, the reason is in `_build/latex/handbook.log`. Search it for `!`.

---

## 9. Optional .gitignore

```gitignore
# Generated output
_build/

# Python environments
.venv/
__pycache__/
```
