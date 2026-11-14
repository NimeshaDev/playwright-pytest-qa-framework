# Playwright + pytest QA Automation Framework

[![Tests](https://github.com/NimeshaDev/playwright-pytest-qa-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/NimeshaDev/playwright-pytest-qa-framework/actions)

UI, API and BDD test automation in Python, built with Playwright and pytest, using the Page Object Model. Every push runs the UI tests on Chromium, Firefox and WebKit in GitHub Actions and publishes an HTML test report.

## Tech stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Language |
| Playwright | Browser automation |
| pytest | Test runner and fixtures |
| pytest-bdd | Gherkin / BDD scenarios |
| pytest-playwright | Browser fixtures, cross-browser runs, failure screenshots and traces |
| pytest-html | HTML test reports |
| requests | API testing |
| Postman | Manual API exploration |
| GitHub Actions | CI pipeline |

## Project structure

```
.
├── .github/workflows/tests.yml   CI pipeline
├── conftest.py                   Shared fixtures (browser page, test data)
├── pytest.ini                    pytest and pytest-bdd settings
├── requirements.txt
├── data/test_data.json           Test users and URLs
├── features/login.feature        Gherkin scenarios
├── pages/                        Page Object Model classes
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── postman/                      Postman collection
└── tests/
    ├── api/test_users_api.py     REST API tests
    └── ui/
        ├── test_saucedemo_pom.py UI tests (POM)
        └── test_login_bdd.py     BDD step definitions
```

## Test coverage

**UI - saucedemo.com**
- Valid, invalid and locked-out user login
- Add product to cart
- Full flow: login, add to cart, verify cart

**API - jsonplaceholder.typicode.com**
- GET single user (200), user not found (404)
- POST create user (201)
- GET all users (200)

**BDD scenarios**
- Valid user can login
- Invalid user cannot login
- Locked user cannot login

## How to run

```bash
pip install -r requirements.txt
playwright install chromium
pytest                 # all tests
pytest tests/api       # API only
pytest tests/ui        # UI and BDD only
pytest tests/ui --browser firefox --headed   # watch it run in Firefox
pytest --html=reports/report.html --self-contained-html   # HTML report
```

## CI and test reports

GitHub Actions runs on every push and pull request:

- **API tests** once
- **UI and BDD tests** on Chromium, Firefox and WebKit in parallel
- On failure: a screenshot is embedded in the HTML report, and a Playwright trace is saved

**[View the latest test reports](https://nimeshadev.github.io/playwright-pytest-qa-framework/)** - published to GitHub Pages after every run on `master`.

<!-- REPORT_SCREENSHOT -->

## About

Built by Nimesha Herath - QA Engineer with 4+ years of experience, MSc in Information Systems and Computing (First Class Honours), ISTQB Foundation certified.

[LinkedIn](https://www.linkedin.com/in/nimeshadev) · [Portfolio](https://nimeshadev.github.io)
