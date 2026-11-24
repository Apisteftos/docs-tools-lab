# Quarto Handbook

Build a handbook **book** from Markdown files with **Quarto**. Quarto uses Pandoc inside
and adds a project file, chapters, a searchable website, callout boxes and one command
for all output formats.

| Example | What it shows | Output |
|---------|---------------|--------|
| [`01_quarto_example`](01_quarto_example) | Company handbook with 5 chapters, notes, checklists and a logo in the page header | HTML website, PDF (A4), ePub, Word |

## Contents

1. [Installation](#1-installation)
2. [Build commands](#2-build-commands)
3. [Folder layout](#3-folder-layout)
4. [The complete _quarto.yml](#4-the-complete-_quartoyml)
5. [_quarto.yml explained](#5-_quartoyml-explained)
6. [Writing pages](#6-writing-pages)
7. [Customize](#7-customize)
8. [Typst instead of LaTeX](#8-typst-instead-of-latex)
9. [Troubleshooting](#9-troubleshooting)
10. [Optional .gitignore](#10-optional-gitignore)

> Run all commands **inside the example folder** (`cd 01_quarto_example`).

---

## 1. Installation

Tested on Ubuntu 24.04 with Quarto 1.11.

### 1.1 Quarto

Download the `.deb` file (for example `quarto-1.11.9-linux-amd64.deb`) from the
[Quarto releases page](https://github.com/quarto-dev/quarto-cli/releases) and install it:

```bash
cd ~/Downloads
sudo apt install ./quarto-1.11.9-linux-amd64.deb
```

Quarto brings its own Pandoc, so your separately installed Pandoc is not used.

Check the installation. This also shows which tools Quarto found:

```bash
quarto --version
quarto check
```

### 1.2 LaTeX engine (for PDF)

```bash
sudo apt install texlive-xetex texlive-latex-recommended texlive-latex-extra \
                 texlive-fonts-recommended texlive-fonts-extra fonts-dejavu
```

`texlive-fonts-extra` is large (several hundred MB), but Quarto's callout boxes need one
package from it (`fontawesome5`). Without it the PDF build stops with the error
`File 'fontawesome5.sty' not found`.

Alternative: let Quarto manage its own small LaTeX installation instead of the system one:

```bash
quarto install tinytex
```

TinyTeX downloads missing LaTeX packages automatically. After installing it, the
fonts must still be on the system (`fonts-dejavu`).

---

## 2. Build commands

| Command | Result |
|---------|--------|
| `quarto render` | Builds **all** formats from `_quarto.yml` into `_output/` |
| `quarto render --to html` | Only the website |
| `quarto render --to pdf` | Only the PDF |
| `quarto render --to epub` | Only the ePub |
| `quarto render --to docx` | Only the Word file |
| `quarto preview` | Live preview in the browser. Reloads when you save a file |

Results in `_output/`:

```
_output/
├── index.html, working-together.html, ...   website (open index.html)
├── Company-Handbook.pdf
├── Company-Handbook.epub
└── Company-Handbook.docx
```

> In a test, a single-format render (`--to pdf`) replaced the other files in `_output/`.
> Use plain `quarto render` when you want all formats together.

---

## 3. Folder layout

```
01_quarto_example/
├── _quarto.yml                project and format settings
├── index.md                   first chapter ("Welcome")
├── working-together.md
├── engineering.md
├── releases-and-support.md
├── onboarding.md
└── images/
    ├── logo-full.png          wide logo (sidebar, PDF header, ePub cover)
    ├── logo.png               small square logo
    └── process.png
```

Quarto accepts plain `.md` files, as used here, and `.qmd` files (Quarto Markdown, which
can also run code). The chapter order comes from the `chapters` list in `_quarto.yml`.

---

## 4. The complete _quarto.yml

```yaml
project:
  type: book
  output-dir: _output

lang: en
date-format: "MMMM YYYY"

book:
  title: "Company Handbook"
  subtitle: "How we work at Example Company"
  author: "Example Company GmbH"
  date: "November 2026"
  search: true
  sidebar:
    logo: images/logo-full.png
  chapters:
    - index.md
    - working-together.md
    - engineering.md
    - releases-and-support.md
    - onboarding.md

format:
  html:
    theme: cosmo
    toc: true
    toc-depth: 2
    number-sections: true
  pdf:
    documentclass: scrbook
    pdf-engine: xelatex
    papersize: a4
    classoption: [oneside, openany]
    geometry: [margin=2.5cm, top=3.2cm, headheight=1.6cm]
    mainfont: "DejaVu Serif"
    sansfont: "DejaVu Sans"
    monofont: "DejaVu Sans Mono"
    colorlinks: true
    callout-icon: false
    toc: true
    toc-depth: 2
    number-sections: true
    include-in-header:
      text: |
        \usepackage{scrlayer-scrpage}
        \clearpairofpagestyles
        \renewcommand*{\chapterpagestyle}{scrheadings}
        \pagestyle{scrheadings}
        \ohead{\includegraphics[height=1.0cm]{images/logo-full.png}}
        \ihead{\small\textcolor{gray}{Company Handbook}}
        \cfoot{\small\pagemark}
        \setkomafont{pageheadfoot}{\normalfont}
  epub:
    cover-image: images/logo-full.png
    toc: true
  docx:
    toc: true
    number-sections: true
```

---

## 5. _quarto.yml explained

### 5.1 Project

| Key | Meaning |
|-----|---------|
| `project: type: book` | A book with chapters, one navigation and one PDF. Other types: `website`, `default` |
| `output-dir: _output` | Folder for all results |
| `lang: en` | Language of generated texts such as "Table of contents" |
| `date-format` | Display format of the date. Without it Quarto turns "November 2026" into `2026-11-01` in the PDF |

### 5.2 Book

| Key | Meaning |
|-----|---------|
| `title`, `subtitle`, `author`, `date` | Title page and metadata |
| `search: true` | Search box in the website |
| `sidebar: logo` | Logo at the top of the website sidebar |
| `chapters` | The files in reading order. The first one is the start page |

### 5.3 HTML

| Key | Meaning |
|-----|---------|
| `theme: cosmo` | Bootstrap theme. Others: `flatly`, `journal`, `lumen`, ... |
| `toc`, `toc-depth` | Table of contents on the right, down to the given level |
| `number-sections` | Numbered headings |

### 5.4 PDF

| Key | Meaning |
|-----|---------|
| `documentclass: scrbook` | The KOMA-Script book class |
| `pdf-engine: xelatex` | Engine that supports system fonts |
| `papersize: a4` | Paper size |
| `classoption: [oneside, openany]` | One-sided layout and no blank pages before chapters |
| `geometry` | Margins. `headheight` leaves room for the logo |
| `mainfont`, `sansfont`, `monofont` | Fonts for text, headings and code |
| `colorlinks` | Colored links |
| `callout-icon: false` | No icons in the note boxes |
| `include-in-header` | Raw LaTeX added to the preamble, see below |

The LaTeX header:

| Line | Meaning |
|------|---------|
| `\usepackage{scrlayer-scrpage}` | KOMA package for headers and footers |
| `\clearpairofpagestyles` | Clears the default header and footer |
| `\renewcommand*{\chapterpagestyle}{scrheadings}` | Chapter start pages get the same header |
| `\pagestyle{scrheadings}` | Applies the style to all pages |
| `\ohead{...}` | Header, outer side (right): the logo |
| `\ihead{...}` | Header, inner side (left): grey text |
| `\cfoot{...}` | Footer, center: page number |
| `\setkomafont{pageheadfoot}{\normalfont}` | Header and footer use normal weight |

### 5.5 ePub and Word

| Key | Meaning |
|-----|---------|
| `epub: cover-image` | Cover picture of the ePub |
| `docx: toc, number-sections` | Table of contents and numbered headings in Word |

### 5.6 Rules for the YAML file

- Use **spaces**, never tabs. Indent with 2 spaces.
- Put a space after every colon: `toc: true`.
- Text with special characters goes in quotes.
- List items start with a dash `-`, or use square brackets: `[oneside, openany]`.

---

## 6. Writing pages

Each page starts with one `#` heading. Use `##` and `###` for sections. The first chapter
uses `# Welcome {.unnumbered}` so that it gets no number.

Besides standard Markdown (Pandoc flavor), Quarto adds callouts:

```markdown
::: {.callout-note}
A note box.
:::

::: {.callout-tip}
A tip box.
:::

::: {.callout-warning}
A warning box.
:::

::: {.callout-note}
## Own title
A box with a title.
:::

::: {.callout-note collapse="true"}
## Click to expand
Hidden text.
:::
```

Other useful syntax:

```markdown
- [x] Done item
- [ ] Open item

![Caption](images/process.png){width=80%}

Term
:   Definition of the term.
```

The files stay readable Markdown. Pandoc itself shows the callout syntax as a normal
block of text, because callouts are a Quarto feature.

---

## 7. Customize

| I want to ... | Change |
|---------------|--------|
| Use my own logo | Replace `images/logo-full.png` (same name) |
| Add a chapter | Create `new-chapter.md` and add it to `chapters` |
| Change the header text in the PDF | The text in `\ihead{...}` |
| Remove the logo from the PDF header | Delete the `\ohead{...}` line |
| Change the website colors | `theme: flatly` (or another theme) |
| Use US Letter | `papersize: letter` |
| Change the fonts | `mainfont`, `sansfont`, `monofont` |
| Turn off numbering | `number-sections: false` |
| Remove a format | Delete its block under `format:` |

---

## 8. Typst instead of LaTeX

Quarto can also create PDFs with **Typst**, which is built in. It needs no LaTeX and no
extra fonts package. To try it, replace the `pdf:` block with:

```yaml
  typst:
    papersize: a4
    toc: true
    number-sections: true
```

and run `quarto render --to typst`. In a test with this book, the PDF was built quickly,
but the book layout of this Quarto version did not take over my margin, font and
header settings (the logo header did not appear). That is why this example uses LaTeX for the PDF.

---

## 9. Troubleshooting

| Problem | Solution |
|---------|----------|
| `quarto: command not found` | Install the `.deb` file, see 1.1 |
| `File 'fontawesome5.sty' not found` | `sudo apt install texlive-fonts-extra`, or `quarto install tinytex` |
| `xelatex not found` | `sudo apt install texlive-xetex` |
| `scrlayer-scrpage.sty not found` | `sudo apt install texlive-latex-recommended` |
| `The font "..." cannot be found` | Install the font or change the name. Check with `fc-list` |
| PDF error: read `index.log` | The log in the project folder names the missing file or package |
| Date shows as `2026-11-01` | Set `date-format: "MMMM YYYY"` at the top level |
| Only one format in `_output/` | Use `quarto render` without `--to` |
| Logo missing on chapter start pages | Keep `\renewcommand*{\chapterpagestyle}{scrheadings}` |
| Picture not found | Paths are relative to the page, for example `images/process.png` |
| Old content in the website | Delete `_output` and `.quarto`, then render again |

---

## 10. Optional .gitignore

```gitignore
# Generated output
_output/
.quarto/
*_files/

# LaTeX leftovers
*.log
*.aux
```
