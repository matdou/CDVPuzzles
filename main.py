### This script is used to capture screenshots of various puzzles and their solutions from the web.
### The screenshots are saved in a directory named "CDV_XX_jeux_avec_solution" where "XX" is the number of the group.
### The puzzles are captured from the following websites:
### - https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/loopy.html
### - https://www.e-sudoku.fr/sudoku-killer.php
### - https://www.e-sudoku.fr/jouer-sudoku-solo.php
### - https://www.e-sudoku.fr/sudoku-irregulier.php
### - https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unequal.html
### The screenshots are saved in png format and are named according to the puzzle type and difficulty level.
### The script uses the Selenium WebDriver to interact with the web pages and capture the screenshots.
### The script is designed to be run on a server or a local machine with a graphical environment and a web browser installed.
### The script can be run periodically to update the screenshots of the puzzles and their solutions.




# %%
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import base64
import os
import time

# %%
def click_if_present(driver, css_selector, timeout=10):
    """
    Clicks an element specified by the CSS selector if it is present and clickable.
    If the element is not present or not clickable within the timeout, the function silently ignores the error.
    
    :param driver: The WebDriver instance.
    :param css_selector: The CSS selector for the element to click.
    :param timeout: The maximum time to wait for the element to become clickable.
    """
    try:
        button = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        button.click()
    except TimeoutException:
        print(f"Element with selector '{css_selector}' not found or not clickable.")

def initialize_driver(headless=False):
    """Initialize and return a WebDriver instance with optional headless mode."""
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    window_handle = driver.current_window_handle
    return driver, window_handle

def ensure_directory_exists(path):
    """Ensure that a directory exists; if not, create it."""
    os.makedirs(path, exist_ok=True)

def has_canvas_stabilized(driver, canvas_xpath, interval=0.2, checks=2):
    """Check if the canvas has stabilized (no changes) over a few intervals."""
    last_data_url = None
    unchanged_checks = 0
    while unchanged_checks < checks:
        current_data_url = driver.execute_script(f"""
            var canvas = document.evaluate('{canvas_xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            return canvas.toDataURL();
        """)
        if current_data_url == last_data_url:
            unchanged_checks += 1
        else:
            unchanged_checks = 0
        last_data_url = current_data_url
        #print(f"Unchanged checks: {unchanged_checks}/{checks}")
        time.sleep(interval)
    return True

def capture_and_save_canvas_as_image(driver, canvas_xpath, output_path, timeout=60):
    """Capture a canvas element specified by its XPath and save it as an image, ensuring it has fully loaded."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if has_canvas_stabilized(driver, canvas_xpath):
            image_data_base64 = driver.execute_script(f"""
                var canvas = document.evaluate('{canvas_xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                return canvas.toDataURL('image/png').substring(22);
            """)
            image_data = base64.b64decode(image_data_base64)
            with open(output_path, 'wb') as file:
                file.write(image_data)
            print(f"Canvas screenshot saved to {output_path}")
            return
        else:
            print("Waiting for canvas to stabilize...")
    print(f"Timed out waiting for the canvas to stabilize at {canvas_xpath}")


def click_element_if_present(driver, selector, by=By.CSS_SELECTOR):
    """Click on an element if it is present and clickable."""
    try:
        element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, selector))) # TODO choose a better timeout
        element.click()
    except TimeoutException:
        print(f"Element with selector '{selector}' not found or not clickable.")

def capture_and_save_table_as_image(driver, table_selector, image_path, timeout=20):
    """Capture a table element as an image without any preliminary actions."""
    table = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, table_selector)))
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    table.screenshot(image_path)
    print(f"Table screenshot saved to {image_path}")

def click(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, selector)))
        element.click()
    except TimeoutException:
        raise Exception(f"Element with selector '{selector}' not found or not clickable within {timeout} seconds.")

def switch_to_new_window(driver, timeout=10):
    """
    Automatically captures the current window handle and switches to a new window or tab that opens after this function is called.
    
    :param driver: The WebDriver instance.
    :param timeout: How long to wait for the new window to open before raising a TimeoutException.
    """
    current_handle = driver.current_window_handle  # Capture the current window handle
    
    # Wait for a new window or tab to appear
    WebDriverWait(driver, timeout).until(lambda d: len(d.window_handles) > 1 and d.current_window_handle == current_handle)
    
    # Identify the new window handle and switch to it
    for handle in driver.window_handles:
        if handle != current_handle:
            driver.switch_to.window(handle)
            break
    else:  # If no new window is found
        raise TimeoutException("A new window did not open.")
    
def switch_to_new_window(driver, main_window_handle):
    """Switch to a new window or tab that opens after this function is called."""
    new_window_handle = [handle for handle in driver.window_handles if handle != main_window_handle][0]
    driver.switch_to.window(new_window_handle)

def select_option_by_visible_text_css(driver, css_selector, text):
    """
    Selects an option from a <select> dropdown by visible text using a CSS selector.

    :param driver: The Selenium WebDriver instance.
    :param css_selector: The CSS selector of the <select> element.
    :param text: The visible text of the option you want to select.
    """
    # Find the <select> element using the CSS selector
    select_element = driver.find_element(By.CSS_SELECTOR, css_selector)

    # Create a Select object for the found <select> element
    select = Select(select_element)

    # Select the option by visible text
    select.select_by_visible_text(text)

def hover(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """
    Move the mouse cursor over an element specified by the selector, ensuring the element is visible and ready.
    
    :param driver: The Selenium WebDriver instance.
    :param selector: The selector for the element to hover over.
    :param by: The method used to locate the element (default is By.CSS_SELECTOR).
    :param timeout: Maximum time to wait for the element to be visible and ready for interaction.
    """
    # Wait for the element to be visible and ready
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, selector))
    )

    # Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

    # Perform the hover action
    ActionChains(driver).move_to_element(element).perform()

# %%
def capture_loopy(driver, path):
    driver.get('https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/loopy.html')
    capture_and_save_canvas_as_image(driver, "/html/body/main/div/canvas", path + 'loopy.png')
    click(driver, "#solve", By.CSS_SELECTOR)
    capture_and_save_canvas_as_image(driver, "/html/body/main/div/canvas", path + 'loopy_solution.png')

def capture_sudoku_killer(driver, path, main_window_handle):
    global FIRST_PASS
    driver.get('https://www.e-sudoku.fr/sudoku-killer.php')
    if FIRST_PASS:
        click_element_if_present(driver, ".fc-cta-consent")
        FIRST_PASS = False
    capture_and_save_table_as_image(driver, "table.tours", path + 'sudoku_killer.png')
    click(driver, "input.bouton:nth-child(6)")
    switch_to_new_window(driver, main_window_handle)
    capture_and_save_table_as_image(driver, ".tours", path + 'sudoku_killer_solution.png')
    driver.close()
    driver.switch_to.window(main_window_handle)

def capture_sudoku_solo(driver, path, difficulty="Moyen"):
    global FIRST_PASS
    driver.get("https://www.e-sudoku.fr/jouer-sudoku-solo.php")
    if FIRST_PASS:
        click_element_if_present(driver, ".fc-cta-consent")
        FIRST_PASS = False
    select_option_by_visible_text_css(driver, "#options > p:nth-child(3) > select", difficulty)
    capture_and_save_table_as_image(driver, "#grille > table", f'{path}sudoku_{difficulty.lower()}.png')
    click(driver, "#options > p:nth-child(3) > input:nth-child(1)")
    capture_and_save_table_as_image(driver, "#grille > table", f'{path}sudoku_{difficulty.lower()}_solution.png')

def capture_irregular_sudoku(driver, path, main_window_handle, difficulty="Moyen"):
    global FIRST_PASS
    driver.get("https://www.e-sudoku.fr/sudoku-irregulier.php")
    if FIRST_PASS:
        click_element_if_present(driver, ".fc-cta-consent")
        FIRST_PASS = False
    select_option_by_visible_text_css(driver, "#grille-sudoku > div.ecran > p > select", difficulty)
    capture_and_save_table_as_image(driver, "table.tours", f'{path}irregulier_{difficulty.lower()}.png')
    click(driver, "#grille-sudoku > div.ecran > input:nth-child(6)")
    switch_to_new_window(driver, main_window_handle)
    capture_and_save_table_as_image(driver, "body > div:nth-child(2) > table", f'{path}irregulier_{difficulty.lower()}_solution.png')
    driver.close()
    driver.switch_to.window(main_window_handle)

def capture_unequal_adjacent_puzzles(driver, path, puzzle_type, difficulty):
    driver.get("https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/unequal.html")
    hover(driver, "#gamemenu > ul:nth-child(1) > li:nth-child(2) > div:nth-child(1)")
    if puzzle_type == "unequal":
        label_index = 5 if difficulty == "Extreme" else 2
    else:  # "adjacent"
        label_index = 4 if difficulty == "Tricky" else 3
    click(driver, f"#gametype > li:nth-child({label_index}) > label:nth-child(1)")
    capture_and_save_canvas_as_image(driver, '//*[@id="puzzlecanvas"]', f'{path}{puzzle_type}_{difficulty.lower()}.png')
    click(driver, "#solve")
    capture_and_save_canvas_as_image(driver, '//*[@id="puzzlecanvas"]', f'{path}{puzzle_type}_{difficulty.lower()}_solution.png')


# %%
def main():
    path = './CDV_XX_jeux_avec_solution/'
    ensure_directory_exists(path)
    driver, main_window_handle = initialize_driver()
    
    global FIRST_PASS
    FIRST_PASS = True

    tasks = [
        (capture_loopy, (driver, path)),
        (capture_sudoku_killer, (driver, path, main_window_handle)),
        (capture_sudoku_solo, (driver, path, "Moyen")),
        (capture_sudoku_solo, (driver, path, "Difficile")),
        (capture_sudoku_solo, (driver, path, "Diabolique")),
        (capture_irregular_sudoku, (driver, path, main_window_handle, "Moyen")),
        (capture_unequal_adjacent_puzzles, (driver, path, "unequal", "Extreme")),
        (capture_unequal_adjacent_puzzles, (driver, path, "adjacent", "Tricky")),
    ]

    for task, args in tasks:
        try:
            task(*args)
        except Exception as e:
            print(f"Error occurred in {task.__name__}: {e}")

    driver.quit()

if __name__ == "__main__":
    main()



# %%
# TODO Add the following puzzles or change the source of the puzzles:
# https://www.puzzles.ca/word-search/
# https://puzzlygame.com/nonogram/?rows=25&columns=25
# https://fr.puzzle-light-up.com/?size=7
# https://fr.puzzle-light-up.com/?size=8
# https://fr.kakuroconquest.com/


