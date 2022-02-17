# HeightComparator

This script will use the website hikaku-sitatter.com to create an image of a height comparison of you and your friends. The website only allows 10 people
to be added at a time, so this script automatically adds people 10, screenshots, removes, add 10 other people...etc, then edits all the screenshots together 
and crops the white spaces. Perfect if you want to compare heights with your discord friends, for instance.
- Example output:
![alt text](https://github.com/Ph03nixStyle/HeightComparator/blob/main/final.png?raw=true)
- Demonstration video
![here](https://www.youtube.com/watch?v=Ckssz3Wn4m4)


## Requirements:
```bash
pip install selenium
pip install Pillow
```
- If using Chrome: once Selenium is installed, download the version corresponding to your chrome version on https://chromedriver.chromium.org/downloads.
Then, put the chromedriver either in `PATH` or in the project directory. 
- If not using Chrome: You must change the first lines of code of the `main.py` file so that it uses your browser instead of Chrome.
You must install the webdriver for your browser (download location varies depending on browser) and put it on `PATH` or in the project directory.
(see Selenium doc, https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/).

## Launching the script:
Once selenium, Pillow and the webdriver are correctly setup, you may change the JSON file to put in it the people you want to compare.
Format:
```json
{
  "Person1": ["height in cm", "m/f"],
  "Person2": ["175", "m"]
}
```
Finally, save the json, and execute `main.py`:
```bash
python main.py
```
