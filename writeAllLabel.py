import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import config

#Log in to google account
print('Logging into account`')
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.keep.google.com')
time.sleep(1)
elem = driver.find_element_by_id('identifierId')
elem.send_keys(config.USR + Keys.ENTER)
time.sleep(1)
elem = driver.find_element_by_name('password')
elem.send_keys(config.PW + Keys.ENTER)

time.sleep(3)
all_labels = driver.find_elements_by_class_name('gb_mc')
label_text = [label.text.encode('utf-8') for label in all_labels]
label_text = label_text[2:len(label_text) - 8]

selected_label = ''
while selected_label not in label_text:
    print('Select label from the following:')
    print(label_text)
    selected_label = raw_input()
    
label_elem = [label for label in all_labels if label.text.encode('utf-8') == selected_label]
label_elem[0].click()

time.sleep(3)
driver.find_element_by_xpath('//*[@id="gb"]/div[2]/div[2]/div[3]/div[2]').click() #Switch from Grid to List view

#Scroll to bottom to load all notes
print('Loading all notes')
time.sleep(3)
lenOfPage = driver.execute_script("window.scrollTo(0,document.body.scrollHeight);"
                                + "var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);" 
                                    + "var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True

#Get text of every note
print('Getting note text')
divs = driver.find_elements_by_css_selector('div')
all_divs = []
for div in divs:
    if "notranslate" in div.get_attribute("class") and len(div.text.encode('utf-8')) > 0:
        all_divs.append(div)

del all_divs[0]
all_divs = [div for div in all_divs if div.text.encode('utf-8') != selected_label]
all_test = []
for div in all_divs:
    if 'CmABtb' in div.get_attribute('class') or 'r4nke' in div.get_attribute('class'):
        all_test.append('~!&^%!%' + div.text.encode('utf-8')) 
    else:
        all_test.append(div.text.encode('utf-8'))

#Write notes to a newly made google doc
print('Writing notes to new google doc')
driver.get('https://docs.google.com/document/create')
actions = ActionChains(driver)
for test in all_test:
    if '~!&^%!%' in test:
        actions.send_keys(test[7:])
        actions.send_keys(Keys.ENTER)
    else:
        actions.send_keys(test)
        actions.send_keys(Keys.ENTER + '------------------------------------' + Keys.ENTER)

actions.perform()


elem = driver.find_element_by_css_selector('#docs-title-widget > input')
elem.send_keys('Google Keep ' + selected_label + ' notes' + Keys.ENTER)

print('waiting')
time.sleep(5)

driver.quit()