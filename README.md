# AI Support Diagnostic & Resolution Toolkit

A Python-based support engineering toolkit designed to diagnose API issues, validate configuration, classify common failures, generate troubleshooting recommendations, and create support reports.

This project demonstrates practical skills used in Technical Support, SaaS Support, API Support, and AI Support Engineering environments.

---

## Project Purpose

The purpose of this project is to simulate a real-world API troubleshooting workflow.

The toolkit can:

- Send requests to API endpoints
- Inspect HTTP responses
- Identify common API failures
- Provide troubleshooting recommendations
- Validate environment configuration
- Test multiple endpoints
- Generate diagnostic reports
- Create application logs for troubleshooting

The goal is to make API troubleshooting more structured and repeatable.

---

## Architecture

The project separates different support responsibilities into Python modules.

```text
Configuration
     ↓
API Request
     ↓
Diagnostics
     ↓
Error Classification
     ↓
Troubleshooting Recommendation
     ↓
Logging
     ↓
Report Generation
```

This modular structure makes the project easier to maintain, troubleshoot, and extend.

---

## Core Features

### API Diagnostics

Tests API endpoints and collects information such as:

- HTTP status code
- Response time
- Content type
- Request ID when available
- JSON response
- Connection errors
- Timeout errors

### HTTP Error Classification

The diagnostic engine identifies common HTTP responses such as:

```text
200 OK
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
429 Too Many Requests
500 Internal Server Error
```

### Troubleshooting Recommendations

The toolkit converts technical failures into useful support recommendations.

Example:

```text
HTTP 401 | Authentication failure

Recommendation:
Verify that the API credentials are configured correctly and have not expired.
```

### Environment Configuration Validation

The toolkit checks required environment variables such as:

```text
API_BASE_URL
API_TOKEN
ENVIRONMENT
REQUEST_TIMEOUT
```

Sensitive credentials are loaded through environment variables instead of being hardcoded into the Python source code.

### CSV-Based Endpoint Testing

Multiple API endpoints can be defined and tested through structured input, allowing repeatable diagnostic testing.

### Incident Report Generation

Diagnostic results can be exported into report files for later review and troubleshooting.

### Logging

The toolkit records important application and diagnostic events.

Sensitive information such as API tokens is never intentionally written to logs.

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-support-diagnostic-toolkit
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

The project uses environment variables for configuration.

A safe template is provided in:

```text
.env.example
```

Create your local `.env` file:

```bash
cp .env.example .env
```

Then configure the required values.

Example:

```env
API_BASE_URL=https://example.com/api
API_TOKEN=your_api_token_here
ENVIRONMENT=development
REQUEST_TIMEOUT=5
```

> Never commit real API keys, tokens, passwords, or other credentials to GitHub.

The `.env` file should remain excluded through `.gitignore`.

---

## How to Run

From the project root directory, activate the virtual environment if necessary:

```bash
source .venv/bin/activate
```

Then run the main application:

```bash
python src/main.py
```

Individual modules can also be tested during development when appropriate.

---

## Sample Output

Example diagnostic output:

```text
==================================================
API DIAGNOSTIC REPORT
==================================================

Endpoint: Product API
Method: GET
Status Code: 200
Content Type: application/json; charset=utf-8
Result: SUCCESS
```

Example failure:

```text
==================================================
API DIAGNOSTIC REPORT
==================================================

Status Code: 404
Result: FAILED

Diagnosis:
Requested resource was not found.

Recommendation:
Verify the endpoint URL and requested resource ID.
```

A sanitized example report is available at:

```text
examples/sample_report.txt
```

The real generated reports are excluded from Git tracking.

---

## Troubleshooting Capabilities

The toolkit is designed to help investigate common API and configuration problems including:

- Authentication failures
- Authorization failures
- Invalid endpoints
- Missing resources
- API rate limiting
- Server-side errors
- Request timeouts
- Connection failures
- Invalid environment configuration
- Missing environment variables
- Invalid timeout values
- Unexpected API responses

The diagnostic engine attempts to provide both the technical failure and a useful next troubleshooting step.

---

## Project Structure

```text
AI-support-diagnostic-toolkit/
│
├── src/
│   ├── main.py
│   ├── diagnostics.py
│   ├── config_checker.py
│   └── report_generator.py
│
├── reports/
│
├── examples/
│   └── sample_report.txt
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Additional modules may be added as the toolkit develops.

---

## Security Practices

This project follows basic credential-handling practices:

- API credentials are stored in environment variables
- `.env` is excluded from Git
- Secrets are not hardcoded into Python files
- API tokens are not intentionally written to logs or reports
- Public sample reports contain sanitized data only

---

## What I Learned

Building this project provided hands-on practice with:

- Python scripting
- REST API troubleshooting
- HTTP methods and status codes
- Python `requests`
- JSON response handling
- Exception handling
- Environment variables
- `.env` configuration
- API authentication concepts
- Logging
- File handling
- CSV processing
- Diagnostic report generation
- Git and GitHub
- `.gitignore`
- Modular Python project structure
- Troubleshooting API failures systematically

Most importantly, this project helped connect Python programming with practical support-engineering workflows rather than treating Python only as a programming exercise.

---

## Future Improvements

Potential future improvements include:

- Additional API authentication methods
- More detailed error classification
- Retry handling
- Improved log analysis
- Automated incident summaries
- Additional report formats
- Integration with real SaaS or AI APIs
- Expanded automated testing

---

## Project Status

Active development and continuous improvement.
