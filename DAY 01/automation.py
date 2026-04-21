from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Replace these with your credentials
EMAIL = "tejashwinibmtejashwinibm@gmail.com"
PASSWORD = "Teju*123#"

SCHOLAR_URL = "https://scholar.parvam.in/student/login"

def start_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # keep browser visible so session stays until you cancel
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def try_find(driver, candidates, timeout=6):
    for by, val in candidates:
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, val)))
        except TimeoutException:
            continue
    raise NoSuchElementException("None of the candidate selectors matched.")

def main():
    driver = start_browser()
    driver.get(SCHOLAR_URL)

    # common selectors for email and password inputs (tries multiple options)
    email_selectors = [
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.NAME, "email"),
        (By.ID, "email"),
        (By.CSS_SELECTOR, "input[placeholder*='Email']"),
        (By.CSS_SELECTOR, "input[placeholder*='email']"),
        (By.CSS_SELECTOR, "input[type='text']"),
    ]
    password_selectors = [
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.NAME, "password"),
        (By.ID, "password"),
        (By.CSS_SELECTOR, "input[placeholder*='Password']"),
        (By.CSS_SELECTOR, "input[placeholder*='password']"),
    ]

    try:
        email_el = try_find(driver, email_selectors)
        password_el = try_find(driver, password_selectors)
    except NoSuchElementException:
        print("Could not find email/password fields automatically. Inspect the page and adjust selectors in the script.")
        print("Leaving browser open for manual login.")
        # keep browser open until user closes
        input("Press Enter to close browser and end session...")
        driver.quit()
        return

    # fill credentials (user must set EMAIL and PASSWORD above)
    email_el.clear()
    email_el.send_keys(EMAIL)
    password_el.clear()
    password_el.send_keys(PASSWORD)

    # try a few submit button selectors
    submit_selectors = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]"),
        (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in')]"),
        (By.XPATH, "//button[contains(., 'Submit')]"),
    ]

    submitted = False
    for by, val in submit_selectors:
        try:
            btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, val)))
            btn.click()
            submitted = True
            break
        except Exception:
            continue

    if not submitted:
        # fallback: press Enter on password field
        try:
            password_el.submit()
            submitted = True
        except Exception:
            pass

    # wait for some indication of dashboard / successful login
    try:
        # wait until URL or page contains 'dashboard' or a logout link appears
        WebDriverWait(driver, 15).until(
            lambda d: 'dashboard' in d.current_url.lower()
            or d.find_elements(By.XPATH, "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'logout')]")
            or d.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'dashboard')]")
        )
        print("Login appears successful. Browser will remain open until you cancel the session.")
    except TimeoutException:
        print("Login may have failed or took too long. Browser left open for inspection.")

    try:
        # keep session alive until user decides to close
        input("Press Enter to close browser and end session (or close the browser manually)...")
    except KeyboardInterrupt:
        pass
    finally:
        driver.quit()

if __name__ == "__main__":
    main()