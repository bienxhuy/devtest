# AI Agent Refactor Guide: DEVTEST Framework Architecture

## 🎯 System Context & Objective
You are an expert QA Automation Engineer and Python Developer. Your task is to refactor the `DEVTEST` repository from a tightly coupled structure into a scalable, modular mono-repo architecture. 

**The Goal:** Separate the generic "Framework Core" from the application-specific "Test Implementations" (UI/API) and prepare a dedicated space for "Performance Testing."

---

## 🚫 Strict Execution Rules
1. **Never Delete Silently:** Do not delete any existing logic. Move files to their new locations first.
2. **Update Imports Immediately:** Every time a file is moved, you MUST update the absolute/relative import statements in all dependent files.
3. **Core is Agnostic:** `core/` files MUST NOT contain any application-specific locators, credentials, or URLs.
4. **No Assertions in POM:** Ensure no `assert` statements exist in the `pages/` directory. Assertions belong only in the `ui/` test scripts.
5. **One Step at a Time:** Execute this guide phase-by-phase. Validate imports and run a test build before proceeding to the next phase.

---

## 🏗️ Target Architecture
This is the final state you are working towards. Use this as your map.

```text
DEVTEST/
├── core/                           
│   ├── __init__.py
│   ├── base_page.py                
│   ├── driver_factory.py           
│   ├── logs/                 
│   ├── postexec/                   
│   │   └── postexec_main.py        
│   └── utils/                      
├── tests_functional/               
│   ├── conftest.py                 
│   ├── test_data/                  
│   ├── pages/                      
│   │   ├── home_page/
│   │   └── login_page/
│   ├── ui/                         
│   │   └── test_auth/
│   └── api/                        
├── tests_performance/              
│   ├── locustfile.py               
│   └── load_data/                  
├── .env                            
├── pytest.ini                      
└── requirements.txt                
```

---

## 🚀 Execution Plan

### Phase 1: Directory Scaffolding
1. Create the root-level directories: `core/`, `tests_functional/`, and `tests_performance/`.
2. Inside `tests_functional/`, create subdirectories: `pages/`, `ui/`, `api/`, and `test_data/`.
3. Create empty `__init__.py` files in `core/`, `tests_functional/`, `tests_functional/pages/`, and `tests_functional/ui/` to ensure Python recognizes them as modules.

### Phase 2: Core Migration (The Engine)
1. **Move Logging & Utils:** Move `logger.py` and the `utils/` directory into `core/`.
2. **Move Post-Execution:** Move the `postexec/` folder into `core/`.
3. **Move Base Page:** Move `base_page.py` into `core/`.
   * *Validation:* Scan `base_page.py`. If it contains any application-specific locators (e.g., `self.driver.find_element(By.ID, 'my-app-login-btn')`), extract them before moving. `base_page.py` should only contain generic wrapper methods (e.g., `click_element(locator)`, `wait_for_visibility(locator)`).
4. **Create Driver Factory:** Create `core/driver_factory.py`. Draft a class that initializes Selenium WebDriver based on an environment variable (e.g., `BROWSER=chrome` or `BROWSER=headless`).
5. **Update Imports:** Search the entire project for `import logger`, `from utils...`, and `from base_page...` and update them to `from core.logger...`, `from core.utils...`, etc.

### Phase 3: Application Migration (The Tests)
1. **Move Page Objects:** Move existing POM folders (`home_page/`, `login_page/`, etc.) into `tests_functional/pages/`.
2. **Move Test Scripts:** Move existing test script folders (e.g., `test_auth/`) into `tests_functional/ui/`.
3. **Centralize Fixtures:** Create `tests_functional/conftest.py`. 
   * Move any existing driver initialization logic from individual test files into a `pytest` fixture here. 
   * The fixture should yield the driver from `core.driver_factory` and handle `driver.quit()` in teardown.
4. **Update Imports:** Ensure all files in `tests_functional/ui/` are correctly importing their respective pages from `tests_functional.pages.[page_name]`.

### Phase 4: Data Externalization
1. **Identify Hardcoded Data:** Scan files inside `tests_functional/ui/` and `tests_functional/pages/` for hardcoded usernames, passwords, URLs, and product IDs.
2. **Create Data Files:** Create `tests_functional/test_data/env_config.json` (or `.yaml`) to store this data.
3. **Refactor Tests:** Refactor the test scripts to read data from `env_config.json` rather than using hardcoded strings.

### Phase 5: Performance & Configuration Setup
1. **Scaffold Performance:** Create an empty `locustfile.py` inside `tests_performance/` with a basic boilerplate Locust class.
2. **Update Root Configs:** * Update `pytest.ini` to set the default `testpaths` to `tests_functional/ui`.
   * Ensure `requirements.txt` includes `pytest`, `selenium`, `pytest-html` (or `allure-pytest`), and `locust`.

---

## ✅ Completion Checklist
- [ ] Are `core/` and `tests_functional/` completely separated?
- [ ] Does `pytest` run successfully from the root directory without import errors?
- [ ] Is `base_page.py` completely free of app-specific locators?
- [ ] Are hardcoded credentials moved out of the test scripts?
