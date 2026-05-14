from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import time

# =====================================================
# START BROWSER
# =====================================================

def start_browser():

    options = webdriver.ChromeOptions()

    # HIDE AUTOMATION FLAGS
    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    service = Service(
        ChromeDriverManager().install()
    )

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    driver.maximize_window()

    return driver

# =====================================================
# SEARCH DUCKDUCKGO
# =====================================================

def search_web(driver, query):

    print(f"\nSearching: {query}")

    driver.get(
        "https://duckduckgo.com"
    )

    wait = WebDriverWait(driver, 10)

    search_box = wait.until(

        EC.presence_of_element_located(
            (By.NAME, "q")
        )
    )

    search_box.send_keys(query)

    search_box.send_keys(Keys.RETURN)

    time.sleep(3)

# =====================================================
# EXTRACT TITLES
# =====================================================

def extract_titles(driver):

    print("\nExtracting search results...\n")

    results = driver.find_elements(
        By.TAG_NAME,
        "h2"
    )

    count = 0

    for result in results:

        text = result.text.strip()

        if text != "":

            count += 1

            print(f"{count}. {text}")

    if count == 0:

        print("No results found.")

# =====================================================
# CLOSE BROWSER
# =====================================================

def close_browser(driver):

    driver.quit()