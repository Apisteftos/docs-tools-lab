# MkDocs Handbook

Build a searchable handbook **website** from plain Markdown files with **MkDocs** and the
**Material** theme.

| Example | What it shows | Output |
|---------|---------------|--------|
| [`01_mkdocs_example`](01_mkdocs_example) | Company handbook with 5 pages, navigation, search, dark mode, notes and checklists, logo, and a print page | HTML site, PDF through the print page |

## Contents

1. [Installation](#1-installation)
2. [Build and preview](#2-build-and-preview)
3. [Create the PDF](#3-create-the-pdf)
4. [The complete mkdocs.yml](#4-the-complete-mkdocsyml)
5. [mkdocs.yml explained](#5-mkdocsyml-explained)
6. [Writing pages: Markdown features](#6-writing-pages-markdown-features)
7. [Customize](#7-customize)
8. [Status of Material for MkDocs and Zensical](#8-status-of-material-for-mkdocs-and-zensical)
9. [Troubleshooting](#9-troubleshooting)
10. [Optional .gitignore](#10-optional-gitignore)

> Run all commands **inside the example folder** (`cd 01_mkdocs_example`).

---

## 1. Installation

Tested on Ubuntu 24.04 with Python 3.

MkDocs is a Python program. Install it in a **virtual environment**, so that it does not
interfere with the system Python.

```bash
sudo apt install python3-venv

cd 01_mkdocs_example
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` contains:

```text
mkdocs>=1.6,<2
mkdocs-material>=9.5,<10
mkdocs-print-site-plugin>=2.6
```

| Line | Meaning |
|------|---------|
| `mkdocs>=1.6,<2` | The generator. Version 2 is a rewrite that breaks themes and plugins, so it is excluded |
| `mkdocs-material>=9.5,<10` | The Material theme |
| `mkdocs-print-site-plugin>=2.6` | Adds one page with the whole handbook, for printing to PDF |

Check the installation:

```bash
mkdocs --version        # mkdocs, version 1.6.x
```

Every time you open a new terminal, activate the environment again:

```bash
source .venv/bin/activate
```

Leave it with `deactivate`.

---

## 2. Build and preview

```bash
# Live preview: opens a local server, the page reloads when you save a file
mkdocs serve
# then open http://127.0.0.1:8000 in the browser

# Build the finished website into the folder site/
mkdocs build
```

| Command | Meaning |
|---------|---------|
| `mkdocs serve` | Local preview at `http://127.0.0.1:8000`. Stop it with `Ctrl+C` |
| `mkdocs build` | Writes the static website to `site/`. Copy this folder to any web server |
| `mkdocs build --clean` | Same, but deletes old files in `site/` first |
| `mkdocs build --strict` | Fails on warnings such as broken links. Good for checking before a release |

The `site/` folder works without a server: open `site/index.html` in the browser.

---

## 3. Create the PDF

MkDocs creates websites, not PDFs. This example uses the **print page**: the plugin
`print-site` builds one extra page that contains the whole handbook on a single page.

1. Run `mkdocs serve`.
2. Open `http://127.0.0.1:8000/print_page/` (menu entry "Company Handbook (print version)").
3. Press `Ctrl+P` in the browser and choose **Save as PDF**.
4. Set the paper size to A4 and enable *Background graphics*.

Alternative with Pandoc (see the `pandoc-handbook` folder): the pages are plain
Markdown, so Pandoc can convert them directly:

```bash
pandoc docs/index.md docs/working-together.md docs/engineering.md \
       docs/releases-and-support.md docs/onboarding.md \
       -o handbook.pdf --pdf-engine=xelatex -V papersize=a4 --toc
```

Special MkDocs syntax (`!!! note`, `??? info`) is not understood by Pandoc and appears
as plain text. For documents that must become a PDF, use Pandoc as the main tool.

---

## 4. The complete mkdocs.yml

```yaml
site_name: Company Handbook
site_description: How we work at Example Company
site_author: Example Company GmbH
copyright: Copyright &copy; 2026 Example Company GmbH

theme:
  name: material
  language: en
  logo: images/logo.png
  favicon: images/logo.png
  palette:
    - scheme: default
      primary: teal
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: teal
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.sections
    - navigation.top
    - search.suggest
    - content.code.copy

nav:
  - Home: index.md
  - Working together: working-together.md
  - Engineering: engineering.md
  - Releases and support: releases-and-support.md
  - Onboarding: onboarding.md

plugins:
  - search
  - print-site:
      add_to_navigation: true
      print_page_title: Company Handbook (print version)

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tasklist:
      custom_checkbox: true
```

Folder layout expected by this file:

```
01_mkdocs_example/
├── mkdocs.yml
├── requirements.txt
└── docs/
    ├── index.md
    ├── working-together.md
    ├── engineering.md
    ├── releases-and-support.md
    ├── onboarding.md
    └── images/
        ├── logo.png         (small square logo for the header)
        ├── logo-full.png    (wide logo used on the home page)
        └── process.png
```

All pages and pictures live in `docs/`. Paths in `mkdocs.yml` are relative to `docs/`.

---

## 5. mkdocs.yml explained

### 5.1 Site information

| Key | Meaning |
|-----|---------|
| `site_name` | Name shown in the header and the browser tab |
| `site_description` | Description for search engines |
| `site_author` | Author in the page metadata |
| `copyright` | Text in the footer. `&copy;` is the © sign |

### 5.2 Theme

| Key | Meaning |
|-----|---------|
| `theme: name: material` | Use the Material theme |
| `language: en` | Language of the interface (search box, buttons). `de` for German |
| `logo` | Logo in the header, relative to `docs/`. A small square PNG works best |
| `favicon` | Icon in the browser tab |
| `palette` | Two color schemes: `default` is light and `slate` is dark. The `toggle` entries create the sun/moon button |
| `primary: teal` | Color of the header. Many names are available, for example `indigo`, `blue`, `red` |

### 5.3 Theme features

| Feature | Meaning |
|---------|---------|
| `navigation.sections` | Groups of pages are shown as sections in the sidebar |
| `navigation.top` | "Back to top" button |
| `search.suggest` | Suggestions while typing in the search box |
| `content.code.copy` | Copy button on code blocks |

### 5.4 Navigation (`nav`)

```yaml
nav:
  - Home: index.md
  - Working together: working-together.md
```

The text before the colon is the menu title. The file name after it is the page.
The order here is the order in the menu. Without `nav`, MkDocs lists all files alphabetically.

Sub-menus:

```yaml
nav:
  - Home: index.md
  - Guides:
      - Setup: guides/setup.md
      - Usage: guides/usage.md
```

### 5.5 Plugins

| Plugin | Meaning |
|--------|---------|
| `search` | The built-in search. Keep it, because setting `plugins:` removes the default |
| `print-site` | Builds the print page with the whole handbook. `add_to_navigation: true` adds it to the menu |

### 5.6 Markdown extensions

| Extension | What it adds |
|-----------|--------------|
| `admonition` | Colored boxes: `!!! note`, `!!! tip`, `!!! warning` |
| `pymdownx.details` | Collapsible boxes: `??? info` |
| `attr_list` | Attributes on images and links, for example `{ width="260" }` |
| `md_in_html` | Markdown inside HTML blocks |
| `tables` | Tables with `|` |
| `toc: permalink: true` | A link symbol next to each heading |
| `pymdownx.superfences` | Better fenced code blocks |
| `pymdownx.tasklist` | Checklists `- [ ]` and `- [x]`, with `custom_checkbox` for a nicer look |

### 5.7 Rules for the YAML file

- Use **spaces**, never tabs. Indent with 2 spaces.
- Put a space after every colon: `primary: teal`.
- Dashes `-` start list items, and nested items must be indented consistently.
- A wrong indentation is the most common error. MkDocs reports the line number.

---

## 6. Writing pages: Markdown features

Each page starts with one `#` heading. Use `##` for sections. Besides normal Markdown, these
extensions work in this example:

```markdown
!!! note "Optional title"
    Indent the text of the box by four spaces.

!!! tip
    A tip box.

!!! warning
    A warning box.

??? info "Click to expand"
    Hidden text that opens on click.

- [x] Done item
- [ ] Open item

![Caption](images/process.png){ width="400" }
```

Links between pages use the file name: `[Engineering](engineering.md)`.

---

## 7. Customize

| I want to ... | Change |
|---------------|--------|
| Use my own logo | Replace `docs/images/logo.png` and `logo-full.png` with your files (same names) |
| Change the header color | `primary` in `palette`, for example `indigo` |
| Add a page | Create `docs/new-page.md` and add it under `nav` |
| Remove the dark mode button | Delete the second `palette` entry and the `toggle` of the first |
| Switch to German | `language: de` |
| Remove the print page | Delete the `print-site` entry under `plugins` |

Material shows the logo in the **top left** of the header. A logo on the right needs
custom CSS and is not part of this example.

---

## 8. Status of Material for MkDocs and Zensical

Material for MkDocs is in **maintenance mode**: no new features, only critical fixes. When
building, the installed version prints a notice that it reaches end of life on **May 5, 2027**,
and that **Zensical** is its successor from the same team. Zensical can read the same
`mkdocs.yml`.

The example works today. A quick test with Zensical on the same folder:

```bash
python3 -m venv .venv-zensical
source .venv-zensical/bin/activate
pip install zensical
zensical build
```

In a test run the site was built from the unchanged `mkdocs.yml`. Plugins that Zensical
does not support, such as `print-site`, may be ignored. Check the result in the browser.

To hide the MkDocs 2.0 notice while building, set `NO_MKDOCS_2_WARNING=1`:

```bash
NO_MKDOCS_2_WARNING=1 mkdocs build
```

---

## 9. Troubleshooting

| Problem | Solution |
|---------|----------|
| `mkdocs: command not found` | Activate the environment: `source .venv/bin/activate` |
| `The 'python3-venv' package is not installed` | `sudo apt install python3-venv` |
| `Config value 'theme': Unrecognised theme name: 'material'` | Run `pip install -r requirements.txt` inside the active environment |
| `Config value 'plugins': The "print-site" plugin is not installed` | Same: `pip install -r requirements.txt` |
| `A reference to 'xyz.md' is not found` | The file name in `nav` or in a link is wrong. Check spelling and folder |
| Picture is not shown | The path must be relative to the page, for example `images/process.png` for a page directly in `docs/` |
| YAML error with a line number | Check the indentation and the spaces after colons in `mkdocs.yml` |
| Port 8000 is already used | `mkdocs serve -a 127.0.0.1:8001` |

---

## 10. Optional .gitignore

```gitignore
# Generated website
site/

# Python environments
.venv/
.venv-zensical/
__pycache__/
```
