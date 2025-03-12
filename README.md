# HTML Injector - Automated HTML Injection Scanner

## Overview
**HTML Injector** is an advanced security tool that scans websites for HTML injection vulnerabilities. It crawls web pages, extracts parameters, and attempts various HTML injection payloads to detect potential security flaws.

## Features
- ✅ Crawls websites to discover links and input fields
- ✅ Extracts GET and POST parameters
- ✅ Tests for HTML injection vulnerabilities
- ✅ Supports multi-threading for faster scanning
- ✅ Outputs results in a structured format

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/html-injector.git
cd html-injector
```

### 2. Install Dependencies
Ensure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
### Basic Scan
```bash
python html_injector.py --url "http://example.com" -p injection-payload.txts.txt
```

### Enable Crawling
```bash
python html_injector.py --url "http://example.com" --crawl -p injection-payload.txts.txt
```

### Adjusting Threads for Faster Scans
```bash
python html_injector.py --url "http://example.com" -p html- injection-payload.txt -t 20
```

## Example Payloads
Sample payloads to test for HTML injection:
```
<script>alert('Injected!')</script>
<img src=x onerror=alert('Injected!')>
<b>Injected Text</b>
```

## Notes
- Use this tool for ethical security testing only.
- Ensure you have permission before testing any website.

## License
This project is licensed under the MIT License.

## Author
Developed by **Varun Sulakhe** 🚀

