import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    """Executes the different functions of the file"""
    # Initiates the webdriver
    options = Options()
    driver = webdriver.Chrome(options=options)
    # Go to the height comparator website
    driver.get('https://hikaku-sitatter.com/en/')
    # Execute all the functions needed
    delete_default_people(driver)
    add_10_names_from_json(driver)
    take_screenshot(driver)
    time.sleep(5)
    driver.quit()

def delete_default_people(driver):
    """Deletes the two default people with random name and height generated by the website."""
    # Cross element needed to delete the people
    btn_del = driver.find_elements_by_class_name('btn-del')
    for element in btn_del:
        # Javascript script needed to click on hidden cross element
        driver.execute_script("arguments[0].click();", element)



def add_10_names_from_json(driver):
    """"Add 10 people to the website with correct name/height/gender, which is the limit."""
    # Find needed elements
    name_textbox = driver.find_element_by_id('name')
    height_textbox = driver.find_element_by_id('height')
    send_button = driver.find_element_by_class_name('addInput__btn')
    # Loads JSON with names/height/gender, then add them into input fields and adds them one after another
    with open('liste_taille.json', 'r') as f:
        names_dict = json.load(f)
        # Add all the data into text fields then submits, for each person
        for name, height in names_dict.items():
            name_textbox.send_keys(name)
            height_textbox.send_keys(height)
            send_button.click()
            time.sleep(1)

def take_screenshot(driver):
    """Takes a screenshot of the frame and saves it"""
    # Frame element that we need to screenshot
    frame = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div[2]')


if __name__ == '__main__':
    main()