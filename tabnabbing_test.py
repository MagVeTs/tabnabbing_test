from playwright.sync_api import sync_playwright
import sys

def check_tabnabbing(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Visiting: {url}")
        page.goto(url, wait_until='domcontentloaded')

        links = page.query_selector_all('a[target="_blank"]')
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

        print(f"\nChecked {len(links)} links with target=\"_blank\".")
        if issues:
            print(f"\nTabnabbing risks found ({len(issues)}):")
            for i, issue in enumerate(issues, 1):
                print(f"[{i}] {issue['href']} - Missing: {', '.join(issue['missing'])}")
                print(f"    Element: {issue['outer_html']}")
        else:
            print("\n✅ No tabnabbing risks found. All links are safe!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tabnabbing_poc.py <URL>")
        sys.exit(1)
    check_tabnabbing(sys.argv[1])
