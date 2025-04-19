import requests
from bs4 import BeautifulSoup
import urllib.parse
import argparse
import concurrent.futures
import re
import json
import os
import sys
import shutil
import subprocess

# ANSI Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Banner Display
def show_banner():
    if shutil.which("figlet"):
        subprocess.run(["figlet", "HTML INJECTOR"])
    else:
        print("HTML INJECTOR")
    print(f"{GREEN}Advanced HTML Injector with Crawler{RESET}")
    print(f"Created by: {GREEN}Varun Sulakhe{RESET}\n")

# Load Payloads
def load_payloads(file_path):
    if not file_path:
        print(f"{RED}❌ Error: No payload file provided.{RESET}")
        sys.exit(1)
    try:
        with open(file_path, "r") as f:
            payloads = [line.strip() for line in f.readlines() if line.strip()]
        if not payloads:
            print(f"{RED}❌ Error: Payload file is empty.{RESET}")
            sys.exit(1)
        return payloads
    except FileNotFoundError:
        print(f"{RED}❌ Error: Payload file '{file_path}' not found.{RESET}")
        sys.exit(1)

# Build Headers
def build_headers(custom_headers=None, cookie=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    if custom_headers:
        for h in custom_headers:
            if ':' in h:
                key, value = h.split(":", 1)
                headers[key.strip()] = value.strip()
    if cookie:
        headers["Cookie"] = cookie
    return headers

# Crawl Website
def crawl_website(base_url, max_urls=50, custom_headers=None, cookie=None):
    print(f"🔍 Advanced crawling started for {CYAN}{base_url}{RESET}...")
    headers = build_headers(custom_headers, cookie)

    visited = set()
    to_visit = {base_url}
    discovered_urls = set()

    static_extensions = (
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.pdf', '.doc', '.docx', '.xls',
        '.xlsx', '.zip', '.tar', '.gz', '.mp4', '.mp3', '.avi', '.woff', '.woff2',
        '.ttf', '.eot', '.ico', '.exe', '.bin', '.rar', '.7z'
    )

    while to_visit and len(discovered_urls) < max_urls:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url, headers=headers, timeout=5)
            if response.status_code != 200 or "text/html" not in response.headers.get("Content-Type", ""):
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            found_urls = set()

            for tag in soup.find_all(["a", "form", "script", "link"]):
                url = tag.get("href") or tag.get("src") or tag.get("action")
                if not url or url.startswith(("javascript:", "mailto:")):
                    continue

                full_url = urllib.parse.urljoin(current_url, url)
                parsed = urllib.parse.urlparse(full_url)

                if not parsed.scheme.startswith("http"):
                    continue
                if any(full_url.lower().endswith(ext) for ext in static_extensions):
                    continue
                if base_url in full_url:
                    found_urls.add(full_url.split("#")[0])

            for url in found_urls:
                if url not in visited and len(discovered_urls) < max_urls:
                    discovered_urls.add(url)
                    to_visit.add(url)

        except requests.RequestException as e:
            print(f"{RED}⚠️ Failed to crawl {current_url}: {e}{RESET}")
            continue

    print(f"{GREEN}✅ Advanced crawler found {len(discovered_urls)} URLs.{RESET}")
    return list(discovered_urls)

# Discover Parameters
def discover_parameters(url, custom_headers=None, cookie=None):
    print(f"🔍 Discovering parameters for {CYAN}{url}{RESET}...")
    headers = build_headers(custom_headers, cookie)
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        query_params = re.findall(r'[?&]([a-zA-Z0-9_]+)=', response.url)
        form_params = set()
        for form in soup.find_all("form"):
            for input_tag in form.find_all(["input", "select", "textarea"]):
                if input_tag.get("name"):
                    form_params.add(input_tag.get("name"))
        return list(set(query_params) | form_params)
    except requests.exceptions.RequestException:
        return []

# Test Injection
def test_html_injection(target_url, param, method="get", payloads=[], vulnerabilities=[], custom_headers=None, cookie=None):
    headers = build_headers(custom_headers, cookie)
    for payload in payloads:
        encoded_payload = urllib.parse.quote(payload)
        data = {param: payload}
        try:
            if method == "get":
                test_url = f"{target_url}?{param}={encoded_payload}"
                response = requests.get(test_url, headers=headers, timeout=5)
            else:
                test_url = target_url
                response = requests.post(test_url, data=data, headers=headers, timeout=5)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            if soup.find(string=re.compile(re.escape(payload))):
                print(f"{GREEN}✅ Reflected Injection Found: {test_url} | Payload: {payload}{RESET}")
                vulnerabilities.append({"url": test_url, "payload": payload, "method": method.upper(), "type": "Reflected", "location": "HTML Content"})
            elif payload in response.text:
                print(f"{GREEN}✅ Injection Found in Response: {test_url} | Payload: {payload}{RESET}")
                vulnerabilities.append({"url": test_url, "payload": payload, "method": method.upper(), "type": "Reflected", "location": "Raw HTML"})
        except requests.exceptions.RequestException:
            continue

# Scan Target
def scan_target(url, payloads, threads, vulnerabilities, custom_headers=None, cookie=None):
    params = discover_parameters(url, custom_headers, cookie)
    if not params:
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for param in params:
            executor.submit(test_html_injection, url, param, "get", payloads, vulnerabilities, custom_headers, cookie)
            executor.submit(test_html_injection, url, param, "post", payloads, vulnerabilities, custom_headers, cookie)

# Git Update Support
def update_script():
    print(f"{CYAN}🔄 Updating script from Git...{RESET}")
    try:
        subprocess.run(["git", "pull"], check=True)
        print(f"{GREEN}✅ Script updated successfully.{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}❌ Git update failed.{RESET}")
        sys.exit(1)

# Main Function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Target URL")
    parser.add_argument("-l", "--list", help="File containing list of target URLs")
    parser.add_argument("-p", "--payloads", help="Payload file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Threads")
    parser.add_argument("-o", "--output", help="Output file to save vulnerabilities in JSON")
    parser.add_argument("-H", "--header", action="append", help="Custom header (use multiple times)")
    parser.add_argument("--cookie", help="Cookie string")
    parser.add_argument("--crawl", action="store_true", help="Enable crawling")
    parser.add_argument("-u", "--update", action="store_true", help="Update the script via Git")
    args = parser.parse_args()

    if not args.update and not args.payloads:
        parser.error("the following arguments are required: -p/--payloads (unless using -u to update)")

    if args.update:
        update_script()
        sys.exit(0)

    show_banner()
    payloads = load_payloads(args.payloads)

    targets = []
    if args.url:
        targets.append(args.url)
    if args.list:
        try:
            with open(args.list, 'r') as f:
                targets.extend([line.strip() for line in f if line.strip()])
        except FileNotFoundError:
            print(f"{RED}❌ URL list file '{args.list}' not found.{RESET}")
            sys.exit(1)

    if args.crawl:
        new_targets = []
        for target_url in targets:
            new_targets.extend(crawl_website(target_url, custom_headers=args.header, cookie=args.cookie))
        targets = new_targets

    vulnerabilities = []
    for target in targets:
        scan_target(target, payloads, args.threads, vulnerabilities, args.header, args.cookie)

    # Display Vulnerabilities
def display_vulnerabilities(vulnerabilities):
    print(f"\n{CYAN}📋 Summary of Vulnerabilities:{RESET}")
    if not vulnerabilities:
        print(f"{YELLOW}❌ No HTML injection vulnerabilities found.{RESET}")
        return
    for vuln in vulnerabilities:
        print(f"{GREEN}✔️  URL: {vuln['url']}")
        print(f"   Method: {vuln['method']}")
        print(f"   Payload: {vuln['payload']}")
        print(f"   Location: {vuln['location']}")
        print(f"   Type: {vuln['type']}{RESET}\n")

if __name__ == "__main__":
    main()
