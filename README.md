# tabnabbing_test
A Python script for checking websites for href links that are vulnerable to tabnabbing.

## A Tabnabbing Risk Checker

This Python script scans one or more web pages for [tabnabbing](https://owasp.org/www-community/attacks/Reverse_Tabnabbing) risks by checking all `<a target="_blank">` links and reporting those missing `rel="noopener noreferrer"`.

## Features

- Accepts a single URL or a `.txt` file with multiple URLs (one per line).
- Reports how many links with `target="_blank"` were checked and how many are vulnerable.
- Outputs results to the terminal by default.
- Optionally writes results to a file in a specified directory.

## Colored Terminal Output

This script uses [colorama](https://pypi.org/project/colorama/) to provide colored output in the terminal, making results easier to read:

- **Cyan:** URL being checked
- **Yellow:** Number of links checked
- **Red:** Errors and tabnabbing risks found
- **Magenta:** Details of each risky link
- **Light gray:** HTML of the risky link
- **Green:** Success message when no risks are found

**Note:** Colors are only shown in the terminal. Output files are always plain text.

### Additional Requirement

To enable colored output, you need to install `colorama`:

```sh
pip install colorama
```

If `colorama` is not installed, the script will still run but without colored output.

## Requirements

- Python 3.7+
- [Playwright Python](https://playwright.dev/python/)
- colorama (optional; for colorizing terminal output)

## Installation

1. Install Playwright and its browser binaries:
    ```sh
    pip install playwright
    playwright install
    ```

2. Save `tabnabbing_test.py` to your project directory.

## Usage

### Scan a Single URL

```sh
python3 tabnabbing_test.py https://example.com
```

### Scan Multiple URLs from a File

Create a `urls.txt` file with one URL per line:

```
https://example.com
https://another-site.com
```

Then run:

```sh
python3 tabnabbing_test.py urls.txt
```

### Output to a File

Add the `-o` or `--output` argument to specify an output filename.  
Use `-d` or `--directory` to specify the output directory (default is current directory):

```sh
python3 tabnabbing_test.py urls.txt -o results.txt -d ./reports
```

## Output

- By default, results are printed to the terminal.
- If `-o` is supplied, results are also written to the specified file.

Example output for each URL:

```
URL: https://example.com
  Checked 5 links with target="_blank".
  Tabnabbing risks found (2):
    [1] https://bad.com - Missing: noopener, noreferrer
        Element: <a href="https://bad.com" target="_blank">Bad Link</a>
    [2] https://another.com - Missing: noreferrer
        Element: <a href="https://another.com" target="_blank" rel="noopener">Another Link</a>
```

If no risks are found:

```
  ✅ No tabnabbing risks found. All links are safe!
```

## License

MIT License
