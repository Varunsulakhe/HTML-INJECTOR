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

# ANSI Color Codes for Styling Output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Banner Display Function
def show_banner():
    if shutil.which("figlet"):
        subprocess.run(["figlet", "HTML INJECTOR"])
    else:
        print("HTML INJECTOR")
    print(f"{GREEN}Advanced HTML Injector with Crawler{RESET}")
    print(f"Created by: {GREEN}Varun Sulakhe{RESET}\n")

# Load HTML Injection Payloads from File
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

# Crawl Website to Discover Links
def crawl_website(base_url, max_urls=50):
    print(f"🔍 Crawling {CYAN}{base_url}{RESET} for links...")
    discovered_urls = set()
    urls_to_visit = {base_url}
    headers = {"User-Agent": "Mozilla/5.0"}

    while urls_to_visit and len(discovered_urls) < max_urls:
        url = urls_to_visit.pop()
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link.get("href")
                full_url = urllib.parse.urljoin(base_url, href)
                if full_url.startswith(base_url) and full_url not in discovered_urls:
                    discovered_urls.add(full_url)
                    urls_to_visit.add(full_url)
        except requests.exceptions.RequestException:
            continue
    print(f"{GREEN}✅ Found {len(discovered_urls)} URLs.{RESET}")
    return list(discovered_urls)

# Extract Parameters from URL and Forms
def discover_parameters(url):
    print(f"🔍 Discovering parameters for {CYAN}{url}{RESET}...")
    headers = {"User-Agent": "Mozilla/5.0"}
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

# Function to Test HTML Injection on Parameters
def test_html_injection(target_url, param, method="get", payloads=[], vulnerabilities=[]):
    headers = {"User-Agent": "Mozilla/5.0"}
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

# Scanning Function that Tests All Parameters on the Target
def scan_target(url, payloads, threads, vulnerabilities):
    params = discover_parameters(url)
    if not params:
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for param in params:
            executor.submit(test_html_injection, url, param, "get", payloads, vulnerabilities)
            executor.submit(test_html_injection, url, param, "post", payloads, vulnerabilities)

# Display All Found Vulnerabilities in a Table Format
def display_vulnerabilities(vulnerabilities):
    if not vulnerabilities:
        print(f"{GREEN}✅ No vulnerabilities detected.{RESET}")
        return

    print(f"\n{YELLOW}🚨 Vulnerabilities Found:{RESET}")
    print("=" * 80)
    print(f"{'URL':<50} {'Payload':<20} {'Method':<10} {'Type':<10}")
    print("=" * 80)

    for vuln in vulnerabilities:
        print(f"{vuln['url'][:48]:<50} {vuln['payload'][:18]:<20} {vuln['method']:<10} {vuln['type']:<10}")

    print("=" * 80)

# Main Function to Parse Arguments and Start the Scan
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Target URL", required=True)
    parser.add_argument("--crawl", action="store_true", help="Enable crawling")  # Fixed Argument Issue
    parser.add_argument("-p", "--payloads", help="Payload file", required=True)
    parser.add_argument("-t", "--threads", type=int, default=10, help="Threads")
    args = parser.parse_args()

    show_banner()
    payloads = load_payloads(args.payloads)

    targets = [args.url]
    if args.crawl:
        targets = crawl_website(args.url)

    vulnerabilities = []

    for target in targets:
        scan_target(target, payloads, args.threads, vulnerabilities)

    display_vulnerabilities(vulnerabilities)  # Display results instead of saving them

if __name__ == "__main__":
    main()