import time
import json
from collections import OrderedDict
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def main():
    options = Options()
    options.add_argument("--kiosk")
    driver = webdriver.Chrome(options=options) # ----------------- Change if not using chrome
    # Go to the height comparator website
    driver.get('https://hikaku-sitatter.com/en/')
    # Gets the JSON data
    with open('height_list.json', 'r') as f:
        names_dict = json.load(f)

    # Execute all the functions needed for each page of 10 people in the JSON
    n = 0 # total amount of images
    for i in range(int(len(names_dict)/10 + 1)):
        init_and_reset_graph(driver)
        add_10_names_from_json(driver, i)
        take_screenshot(driver, i)
        n += 1

    concatenate_images(n)
    crop_white_spaces()
    driver.quit()


def init_and_reset_graph(driver):
    """Adds someone whose height is 190cm to set the graph at a good scale. Then deletes all the default people
    with random name and height generated by the website + that 190cm person."""
    # Fetches elements needed in the HTML source
    name_textbox = driver.find_element_by_id('name')
    height_textbox = driver.find_element_by_id('height')
    send_button = driver.find_element_by_class_name('addInput__btn')
    # Cross element needed to cleanup the people first
    btn_del = driver.find_elements_by_class_name('btn-del')

    # People cleanup
    for element in btn_del:
        try:
            # Javascript script needed to click on hidden cross element
            driver.execute_script("arguments[0].click();", element)
        except:
            continue
    
    # Adds 190 cm person
    name_textbox.send_keys("placeHolder")
    height_textbox.send_keys('190')
    send_button.click()
    time.sleep(0.5)

    # Then instantly removes the 190 person (cleanup again)
    btn_del = driver.find_element_by_class_name('btn-del')
    driver.execute_script("arguments[0].click();", btn_del)


def add_10_names_from_json(driver, page_number):
    """"Add 10 people to the website with correct name/height/gender, which is the limit."""
    # Find needed elements
    name_textbox = driver.find_element_by_id('name')
    height_textbox = driver.find_element_by_id('height')
    male_female_buttons = driver.find_elements_by_class_name('addInput-gender__label')
    send_button = driver.find_element_by_class_name('addInput__btn')

    # Loads JSON with names/height/gender, then add them into input fields and adds them one after another
    with open('height_list.json', 'r') as f:
        names_dict = json.load(f, object_pairs_hook=OrderedDict)

    # Add all the data into text fields then submits, for each person
    for index, (name, list_data) in enumerate(names_dict.items()):
        if index < 10 * page_number or index >= 10 * (page_number+1) :
            continue

        name_textbox.send_keys(name)
        height_textbox.send_keys(list_data[0])

        # Selects male or female
        if list_data[1] == 'm':
            male_female_buttons[0].click()
        else:
            male_female_buttons[1].click()
        send_button.click()
        time.sleep(0.1)
    time.sleep(0.5)


def take_screenshot(driver, page_number):
    """Takes a screenshot of the frame and saves it"""
    # Frame element that we need to screenshot
    frame = driver.find_element_by_class_name('view-scale')
    location = frame.location
    size = frame.size
    full_page_screenshot = driver.get_screenshot_as_png()
    print("Full page screenshot taken")
    im = Image.open(BytesIO(full_page_screenshot))

    left = location['x'] + 300
    top = location['y']
    right = location['x'] + size['width'] - 50
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))
    im.save(f'screenshot_{page_number}.png')


def concatenate_images(n):
    images = [Image.open(x) for x in [f"screenshot_{i}.png" for i in range(n)]]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save('final.png')


def _find_blank_cols(pixels, width, height):
    blank_line = [pixels[0, y] for y in range(height)]
    cols_found = []
    for x in range(width):
        col_x = [pixels[x, y] for y in range(height)]
        if col_x == blank_line:
            cols_found.append(x)
    return cols_found


def crop_white_spaces():
    im = Image.open("final.png")
    if im.mode != 'RGB':
        im = im.convert('RGB')
    pixels = im.load()
    width, height = im.size[0], im.size[1]

    cols_to_remove = _find_blank_cols(pixels, width, height)
    new_im = Image.new('RGB', (width - len(cols_to_remove), height))
    new_pixels = new_im.load()
    
    cols_removed = 0
    for x in range(im.size[0]):
        if x not in cols_to_remove:
            for y in range(new_im.size[1]):
                new_pixels[x - cols_removed, y] = pixels[x, y]
        else:
            cols_removed += 1
    
    new_im.save("final.png")


if __name__ == '__main__':
    # main()
    main()