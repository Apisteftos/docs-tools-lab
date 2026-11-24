# docs-tools-lab

Hands-on comparison of tools that turn **Markdown** into **handbooks, manuals and project
explanations** on Linux. Every tool has its own folder with a complete README (installation,
all terminal commands, the full configuration explained key by key, troubleshooting) and
numbered, ready-to-run examples.

The examples use a fictional company ("Example Company GmbH") and a placeholder logo.
They are not about code documentation (Doxygen and similar), only about written documents.

## The tools

| Tool | Folder | Best for | Output formats |
|------|--------|----------|----------------|
| **Pandoc** | [`pandoc-handbook`](pandoc-handbook) | One Markdown file to PDF, Word, HTML or ePub with a single command. Settings live inside the file | PDF, HTML, Word, ePub, many more |
| **Quarto** | [`quarto-handbook`](quarto-handbook) | Multi-chapter books and websites. Uses Pandoc inside and adds a project file, callouts and one command for all formats | HTML, PDF, ePub, Word |
| **Sphinx** | [`sphinx-handbook`](sphinx-handbook) | Large structured documentation with cross references, read through the MyST parser | HTML, PDF, ePub, Qt Help, text |
| **MkDocs Material** | [`mkdocs-handbook`](mkdocs-handbook) | A searchable handbook **website**. PDF only through the browser's print function | HTML (PDF via print page) |

## Which one should I use?

| I want ... | Use |
|------------|-----|
| One handbook as PDF with the least setup | Pandoc |
| The same file as PDF, Word, HTML and ePub | Pandoc |
| A book with chapters, a searchable website and a PDF from one project | Quarto |
| A big, long-lived documentation website with cross references | Sphinx |
| A good-looking internal website, PDF is secondary | MkDocs Material |

Notes from testing on Ubuntu 24.04:

- **Quarto** runs Pandoc inside, so a single-file handbook looks almost the same as with
  plain Pandoc. Quarto's PDF callout boxes need extra LaTeX packages (see its README).
- **MkDocs and Sphinx** are built around websites. Their PDF output works, but needs more
  effort than Pandoc or Quarto.
- **Material for MkDocs** is in maintenance mode. Its README explains the status and the
  successor.
- The Markdown syntax for notes and warnings differs between the tools, so a file written
  for one tool does not render identically in another. Plain Markdown (headings, lists,
  tables, pictures) works everywhere.

## Working with an AI assistant

The Markdown files are plain text, so an AI assistant such as Claude can write, restructure,
translate or update them. The build tools above then create the final files from the
Markdown. This keeps the source in Git and makes every output reproducible with one command.

## Requirements

- Ubuntu 24.04 (other Linux distributions work the same way)
- A terminal and a Markdown editor of your choice
- The tool-specific packages are listed in each folder's README

## How to use this repository

1. Open the folder of the tool you want to try.
2. Follow the **Installation** chapter of its README.
3. Run the build commands inside the example folder.
4. Replace the sample text and the placeholder logo (`images/logo.png`) with your own.

Generated files (PDF, HTML, Word, ePub and build folders) are listed in `.gitignore`,
because they can be rebuilt from the Markdown files.

## License

Copyright © 2026 **Konstantinos Angeloulis**

This project is licensed under the MIT License (see the [LICENSE](LICENSE) file).