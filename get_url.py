import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


prefs = {
    'profile.default_content_setting_values': {
        'images': 2,   
        'javascript': 2,   
        'permissions.default.stylesheet': 2
    }
}

chrome_options = webdriver.ChromeOptions()                                             # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])       # 进行自动化伪装成 开发者模式
chrome_options.add_experimental_option('prefs', prefs)                                  # 禁止加载图片
chrome_options.add_experimental_option('useAutomationExtension', False)               # 开发者模式
chrome_options.add_argument("--headless")                                              # 为Chrome配置无头模式
chrome_options.add_argument('--disable-javascript')                                    # 禁用javascript
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-plugins')
chrome_options.add_argument('--disable--gpu')
chrome_options.add_argument('--disable-extensions')

with open('user_agent_pool.json','r') as f:
    user_agent_pool = json.load(f)
user_agent = random.choice(user_agent_pool)
chrome_options.add_argument('user-agent=%s'%user_agent)

PATH = '/Users/yangyijun/chromedriver-mac-x64/chromedriver'
driver = webdriver.Chrome(PATH,options=chrome_options) 
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
# driver.get("https://jiankang.baidu.com/widescreen/entitylist?tabType=1&navType=1")
# driver.get("https://jiankang.baidu.com/widescreen/entitylist?tabType=1&navType=2")
driver.get("https://jiankang.baidu.com/widescreen/entitylist?tabType=1&navType=3")

# Use the refined XPath to locate the elements
events_xpath = "//div[@id='entity']//div[contains(@class, '_3ekmQ')]//span[contains(@class, 'mQUou')]/span"

# Wait for the elements to be present in the DOM
events = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, events_xpath))
)
# Wait for the element to be clickable before clicking
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, events_xpath)))

# Click on each event element
for event_element in events:
    event_text = event_element.text
    event_element.click()

    links_xpath = "//div[@id='letter']//div[contains(@class, '_3jQHe')]//a"
    time.sleep(5)
    # Wait for the 'a' elements to be present in the DOM
    links = WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located((By.XPATH, links_xpath))
    )

    # Extract and print the href attribute and text of each 'a' element
    for link in links:
        href = link.get_attribute('href')
        text = link.text
        jsonob = {
            "class": event_text,
            "disease": text,
            "href": href

        }
        with open('class_dis_href_240202.jsonl', 'a') as f:
            json.dump(jsonob, f,ensure_ascii=False)
            f.write('\n')



