# LaTeX Bib File Capitalization Tool

This tool processes `.bib` files by wrapping capital letters in specified words or phrases with curly braces `{}` to ensure that the capital letters in these words are not automatically downcased when generating references in LaTeX.


## Features

- Automatically wraps capitalized letters in specified words or phrases with `{}` to preserve capitalization in LaTeX.
- Supports both all-uppercase and title-case words.
- Allows customization through a separate file containing the words or phrases that need capitalization preservation.
- Processes only the `title` fields of the `.bib` entries.
- The modified content is written to a new `.bib` file with `_modified` appended to its filename.


## Requirements

- Python 3.x

## Quick Test

You can quickly run the script with:

```bash
python converter.py
```

This will process the default `.bib` file (`test.bib`) and the default formatted words file (`formatted_words.txt`), then generate a new `.bib` file (`test_modified.bib`).


## Command-Line Arguments

- `-b`, `--bib`: Path to the input `.bib` file. Default is `test.bib`.
- `-w`, `--words`: Path to the file containing formatted words or phrases. Default is `formatted_words.txt`.

```bash
python converter.py -b your_bib_file.bib -w formatted_words.txt
```

### Customizing `formatted_words.txt`

The `formatted_words.txt` file contains words or phrases for capitalization preservation. You can customize it to suit your own needs. The version included in the repository is just an example/template and can be modified as needed.