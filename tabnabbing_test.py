from playwright.sync_api import sync_playwright
import sys
import argparse
import os

# Add colorama for colored terminal output
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    # If colorama is not installed, define dummy Fore and Style
    class Dummy:
        def __getattr__(self, name): return ''
    Fore = Style = Dummy()

def check_tabnabbing(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Visiting: {url}")
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=15000)
        except Exception as e:
            print(f"  Error loading {url}: {e}")
            browser.close()
            return {'url': url, 'error': str(e), 'checked': 0, 'issues': []}

        links = page.query_selector_all('a[target="_blank"]')
        checked = len(links)
        issues = []
        for link in links:
            rel = (link.get_attribute('rel') or '').lower()
            missing = []
            if 'noopener' not in rel:
                missing.append('noopener')
            if 'noreferrer' not in rel:
                missing.append('noreferrer')
            if missing:
                issues.append({
                    'href': link.get_attribute('href'),
                    'missing': missing,
                    'outer_html': link.evaluate('e => e.outerHTML')
                })

        browser.close()
        return {'url': url, 'checked': checked, 'issues': issues}

def format_result(result, use_color=False):
    def c(text, color):
        return f"{color}{text}{Style.RESET_ALL}" if use_color else text

    output = []
    output.append(c(f"URL: {result['url']}", Fore.CYAN))
    if 'error' in result:
        output.append(c(f"  Error: {result['error']}\n", Fore.RED))
        return "\n".join(output)
    output.append(c(f"  Checked {result['checked']} links with target=\"_blank\".", Fore.YELLOW))
    if result['issues']:
        output.append(c(f"  Tabnabbing risks found ({len(result['issues'])}):", Fore.RED))
        for i, issue in enumerate(result['issues'], 1):
            output.append(c(f"    [{i}] {issue['href']} - Missing: {', '.join(issue['missing'])}", Fore.MAGENTA))
            output.append(c(f"        Element: {issue['outer_html']}", Fore.LIGHTBLACK_EX))
    else:
        output.append(c("  ✅ No tabnabbing risks found. All links are safe!", Fore.GREEN))
    output.append("")
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Check for tabnabbing risks in URLs.")
    parser.add_argument("input", help="A URL or a .txt file with URLs (one per line)")
    parser.add_argument("-o", "--output", help="Output filename (if not supplied, only prints to terminal)")
    parser.add_argument("-d", "--directory", default=".", help="Output directory (default: current directory, only used if --output is set)")
    args = parser.parse_args()

    # Determine if input is a file or a single URL
    if os.path.isfile(args.input) and args.input.endswith('.txt'):
        with open(args.input, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    else:
        urls = [args.input]

    results = []
    for url in urls:
        result = check_tabnabbing(url)
        results.append(result)

    # Print results to terminal with color
    for result in results:
        print(format_result(result, use_color=True))

    # Optionally write to file (without color)
    if args.output:
        output_path = os.path.join(args.directory, args.output)
        os.makedirs(args.directory, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(format_result(result, use_color=False))
                f.write("\n")
        print(f"\nScan complete. Results written to: {output_path}")
    else:
        print("\nScan complete.")

if __name__ == "__main__":
    main()