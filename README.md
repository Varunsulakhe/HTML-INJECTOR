# HTML Injector - Automated HTML Injection Scanner

## Overview
**HTML Injector** is an advanced security tool that scans websites for HTML injection vulnerabilities. It crawls web pages, extracts parameters, and attempts various HTML injection payloads to detect potential security flaws.

## Features
✅ Crawls websites to discover links, forms, and script sources
✅ Extracts GET and POST parameters from URLs and HTML forms
✅ Tests each parameter for HTML injection vulnerabilities (reflected)
✅ Supports multi-threading for fast concurrent testing
✅ Displays results in real-time and saves structured JSON output
✅ Supports custom headers and cookies for authenticated scanning
✅ Allows Git-based script self-update with --update flag
✅ Command-line interface with flexible argument support
✅ Handles multiple targets via file input or crawler discovery

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/HTML-INJECTOR.git
cd HTML-INJECTOR
```

### 2. Install Dependencies
Ensure you have Python installed, then install the required dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage
### Adjusting Threads for Faster Scans 
```bash
python3 HTML_Injection.py --url "http://example.com" -p html-injection-payload.txt -t 20 --crawl
```

## Example Payloads
Sample payloads to test for HTML injection:
```
<body><h1>HTML html</h1></body>
Html<br>line breaks<br>injection
<button type="button">Click Me!</button>
<canvas id="myCanvas">draw htmli</canvas>
<caption>Html</caption>
```

## Notes
- Use this tool for ethical security testing only.
- Ensure you have permission before testing any website.

## License
This project is licensed under the MIT License.

## Author
Developed by **Varun Sulakhe** 🚀

