# Pandoc Handbook

Examples for turning Markdown files into handbooks and manuals with **Pandoc**.
Both examples use only plain Markdown files, pictures and terminal commands.

| Example | What it shows | Output |
|---------|---------------|--------|
| [`01_pandoc_example`](01_pandoc_example) | Small test document with embedded pictures, converted to many formats | PDF, HTML, Word, ePub |
| [`02_pandoc_example`](02_pandoc_example) | Company handbook with logo in the page header, table of contents and numbered chapters. All settings live inside the Markdown file | PDF (A4) |

## Contents

1. [Installation](#1-installation)
2. [Example 01: one file, many formats](#2-example-01-one-file-many-formats)
3. [Example 02: company handbook as PDF](#3-example-02-company-handbook-as-pdf)
4. [YAML metadata block explained](#4-yaml-metadata-block-explained)
5. [The LaTeX header explained](#5-the-latex-header-explained)
6. [Command line options and their YAML equivalents](#6-command-line-options-and-their-yaml-equivalents)
7. [Fonts](#7-fonts)
8. [Troubleshooting](#8-troubleshooting)
9. [Optional .gitignore](#9-optional-gitignore)

> Run all commands **inside the example folder** (for example `cd 01_pandoc_example`).
> Pictures are referenced with relative paths such as `images/logo.png`.

---

## 1. Installation

Tested on Ubuntu 24.04.

### 1.1 Pandoc

Download the `.deb` file (for example `pandoc-3.14-1-amd64.deb`) from the
[Pandoc releases page](https://github.com/jgm/pandoc/releases) and install it:

```bash
cd ~/Downloads
sudo apt install ./pandoc-3.14-1-amd64.deb
```

Keep the `./` in front of the file name. It tells `apt` to install a local file.
Ubuntu's own repository only provides an older version (3.1.x), so the `.deb` is the better choice.

### 1.2 LaTeX engine (needed for PDF only)

Pandoc creates PDFs through LaTeX. Install XeLaTeX and the packages used here:

```bash
sudo apt install texlive-xetex texlive-latex-recommended
```

### 1.3 Fonts

Example 02 uses **DejaVu Serif** and **DejaVu Sans Mono**. They are installed on
most Ubuntu systems. If not:

```bash
sudo apt install fonts-dejavu
```

### 1.4 Check the installation

```bash
pandoc --version                      # first line: pandoc 3.x
xelatex --version                     # prints the XeTeX version
fc-list | grep -i "DejaVu Serif"      # prints at least one line
```

---

## 2. Example 01: one file, many formats

Folder: `01_pandoc_example`. The source is `handbook.md`. It contains headings, a table,
a code block, a quote, lists, a definition list and three pictures.

### 2.1 YAML block of the file

```yaml
---
title: "Sample Project Handbook"
author: "Example Author"
date: "2026-11-24"
lang: en
---
```

Only title, author, date and language are set here. The rest (table of contents,
paper size, ...) is given on the command line, so you can see the difference to example 02.

### 2.2 Build commands

```bash
cd 01_pandoc_example

# HTML: a single file, pictures are embedded
pandoc handbook.md -o handbook.html --standalone --embed-resources

# Word
pandoc handbook.md -o handbook.docx

# ePub
pandoc handbook.md -o handbook.epub

# PDF (default settings, US Letter)
pandoc handbook.md -o handbook.pdf --pdf-engine=xelatex
```

### 2.3 Variants (PDF)

```bash
# A4 paper
pandoc handbook.md -o handbook2.pdf --pdf-engine=xelatex -V papersize=a4

# A4, table of contents, numbered chapters, own fonts and margins
pandoc handbook.md -o handbook3.pdf --pdf-engine=xelatex \
  --toc --number-sections \
  -V papersize=a4 -V geometry:margin=2.5cm \
  -V mainfont="DejaVu Serif" -V monofont="DejaVu Sans Mono"
```

The backslash `\` at the end of a line continues the command on the next line.

### 2.4 What to check

- All three pictures appear in every format.
- The table is rendered correctly.
- The `{width=...}` picture sizes are applied. Some editors ignore them in the preview, but Pandoc applies them in the output.
- The checkbox list may look plain in Word. This is a known limit.

---

## 3. Example 02: company handbook as PDF

Folder: `02_pandoc_example`. All settings are inside `handbook.md`, so the build is one command.

### 3.1 Build

```bash
cd 02_pandoc_example
pandoc handbook.md -o handbook.pdf --pdf-engine=xelatex
```

The result is an A4 PDF with the company logo at the top right of every page,
a table of contents, numbered chapters and page numbers in the footer.

### 3.2 The complete YAML block

This block must be at the very top of `handbook.md`, starting on line 1:

```yaml
---
title: "Company Handbook"
subtitle: "How we work at Example Company"
author: "Example Company GmbH"
date: "November 2026"
lang: en
toc: true
toc-depth: 2
numbersections: true
papersize: a4
geometry: [margin=2.5cm, top=3cm, headheight=1.3cm]
mainfont: "DejaVu Serif"
monofont: "DejaVu Sans Mono"
colorlinks: true
linestretch: 1.15
header-includes: |
  \usepackage{fancyhdr}
  \usepackage{graphicx}
  \fancypagestyle{plain}{%
    \fancyhf{}
    \fancyhead[L]{\small\textcolor{gray}{Company Handbook}}
    \fancyhead[R]{\includegraphics[height=1.0cm]{images/logo.png}}
    \fancyfoot[C]{\small\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
  }
  \pagestyle{plain}
---
```

After the second `---` the normal Markdown text starts:

```markdown
# Welcome

Welcome to **Example Company**. ...

![Standard workflow for every project](images/process.png){width=95%}
```

### 3.3 Change something

| I want to ... | Change |
|---------------|--------|
| Use my own logo | Replace `images/logo.png` with your file (same name) |
| Make the logo bigger | `height=1.0cm` in `\includegraphics`, and raise `headheight` and `top` in `geometry` |
| Change the header text | The text in `\fancyhead[L]{...}` |
| Remove the table of contents | `toc: false` |
| Use US Letter | `papersize: letter` |
| Change the fonts | `mainfont` and `monofont`, see [Fonts](#7-fonts) |

---

## 4. YAML metadata block explained

The block between the two `---` lines is read by Pandoc as settings. It is not part of the text.

### 4.1 Document information

| Key | Meaning |
|-----|---------|
| `title` | Title on the first page |
| `subtitle` | Line below the title |
| `author` | Author or company |
| `date` | Date on the title page. Any text is allowed |
| `lang` | Language, for hyphenation and names like "Contents". `en`, `de`, ... |

### 4.2 Structure

| Key | Meaning |
|-----|---------|
| `toc: true` | Adds a table of contents |
| `toc-depth: 2` | Lists headings down to level 2 (`#` and `##`) |
| `numbersections: true` | Numbers the headings: 1, 1.1, 2, ... |

### 4.3 Page layout

| Key | Meaning |
|-----|---------|
| `papersize: a4` | Paper size. Others: `letter`, `a5` |
| `geometry: [...]` | Page margins. `margin=2.5cm` on all sides, `top=3cm` more space at the top, `headheight=1.3cm` room for the logo |
| `linestretch: 1.15` | Line spacing. 1 is tight, 1.5 is airy |

### 4.4 Fonts and links

| Key | Meaning |
|-----|---------|
| `mainfont` | Font of the body text |
| `monofont` | Font of code |
| `colorlinks: true` | Colored links instead of boxes around them |

### 4.5 Raw LaTeX: `header-includes`

```yaml
header-includes: |
  \usepackage{fancyhdr}
  ...
```

The `|` means that everything indented below is one block of plain text. Pandoc
inserts it into the LaTeX file before building the PDF. It only affects the PDF.

### 4.6 Rules for the YAML block

- It must start on **line 1** with `---`. Nothing before it, not even an empty line.
- It must end with `---` (or `...`).
- Use **spaces**, never tabs.
- Put a space after the colon: `toc: true`.
- Lines below `header-includes: |` must be indented consistently (two spaces here).
- Text with special characters such as `:` goes in quotes: `title: "Handbook: Part 1"`.

If the block is wrong, Pandoc prints it as normal text, and you will see the `---` lines on page 1 of the PDF.

---

## 5. The LaTeX header explained

```latex
\usepackage{fancyhdr}
\usepackage{graphicx}
\fancypagestyle{plain}{%
  \fancyhf{}
  \fancyhead[L]{\small\textcolor{gray}{Company Handbook}}
  \fancyhead[R]{\includegraphics[height=1.0cm]{images/logo.png}}
  \fancyfoot[C]{\small\thepage}
  \renewcommand{\headrulewidth}{0.4pt}
}
\pagestyle{plain}
```

| Line | Meaning |
|------|---------|
| `\usepackage{fancyhdr}` | Loads a package for custom headers and footers |
| `\usepackage{graphicx}` | Loads a package for including pictures |
| `\fancypagestyle{plain}{...}` | Redefines the page style named `plain`, which LaTeX uses on every page |
| `\fancyhf{}` | Clears the default header and footer |
| `\fancyhead[L]{...}` | Header, left: grey text "Company Handbook" |
| `\fancyhead[R]{...}` | Header, right: the logo, 1 cm high |
| `\fancyfoot[C]{...}` | Footer, center: the page number |
| `\renewcommand{\headrulewidth}{0.4pt}` | Thin line below the header |
| `\pagestyle{plain}` | Applies the style to the whole document |

`L`, `C` and `R` mean left, center and right.

---

## 6. Command line options and their YAML equivalents

Every setting can be given on the command line (example 01) or in the YAML block (example 02).
The YAML way keeps the build command short and the settings next to the text.

| Command line | YAML |
|--------------|------|
| `--toc` | `toc: true` |
| `--toc-depth=2` | `toc-depth: 2` |
| `--number-sections` | `numbersections: true` |
| `-V papersize=a4` | `papersize: a4` |
| `-V geometry:margin=2.5cm` | `geometry: [margin=2.5cm]` |
| `-V mainfont="DejaVu Serif"` | `mainfont: "DejaVu Serif"` |
| `-V monofont="DejaVu Sans Mono"` | `monofont: "DejaVu Sans Mono"` |
| `-V colorlinks=true` | `colorlinks: true` |
| `-V linestretch=1.15` | `linestretch: 1.15` |
| `--include-in-header=header.tex` | `header-includes: \|` and the LaTeX below it |
| `--pdf-engine=xelatex` | Stays on the command line |

For HTML, Word and ePub the same title, author and date are used. The LaTeX settings
(`papersize`, `geometry`, fonts, `header-includes`) only affect the PDF.

---

## 7. Fonts

XeLaTeX finds fonts **by name**, so the font must be installed on the computer.

```bash
fc-list : family | sort -u               # all installed fonts
fc-list :spacing=100 family | sort -u    # monospace fonts only (for monofont)
```

Common choices on Ubuntu:

| Type | Fonts |
|------|-------|
| Serif (`mainfont`) | DejaVu Serif, Liberation Serif, FreeSerif |
| Sans (`mainfont`) | DejaVu Sans, Liberation Sans, Ubuntu, Noto Sans |
| Monospace (`monofont`) | DejaVu Sans Mono, Liberation Mono, Ubuntu Mono |

With `texlive-fonts-recommended` installed you also get TeX Gyre Pagella, TeX Gyre Termes and TeX Gyre Heros.

---

## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `xelatex not found` | `sudo apt install texlive-xetex` |
| `fancyhdr.sty not found` | `sudo apt install texlive-latex-recommended` |
| `The font "..." cannot be found` | The name in `mainfont` or `monofont` is wrong or the font is missing. Check with `fc-list` |
| `File 'images/logo.png' not found` | Run the command inside the example folder and check the file name |
| The `---` block shows up in the PDF text | The file must start with `---` on line 1, with nothing before it |
| `Missing character` warning | The font has no glyph for that character (for example an emoji). Remove it or use another font |
| Warning about `\headheight` | Increase `headheight` in `geometry`, for example `headheight=1.5cm` |
| Logo is cut off or overlaps the text | Raise `top` and `headheight` in `geometry`, or reduce the logo `height` |

---

## 9. Optional `.gitignore`

Generated files can be rebuilt, so they do not have to be in Git.

```gitignore
# LaTeX leftovers
*.aux
*.log
*.toc
*.out
*.xdv
*.fls
*.fdb_latexmk
*.synctex.gz

# Generated output
*.pdf
*.epub
*.html

# Keep the finished examples
!01_pandoc_example/*.pdf
!02_pandoc_example/*.pdf
```

Do not ignore `*.docx` or `*.html` globally if you later add template files such as
`reference.docx`, because the build needs them.