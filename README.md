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

