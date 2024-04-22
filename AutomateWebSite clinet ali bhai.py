from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.common.keys import Keys
from time import sleep

username = 'Adultdeals'
password = 'monstA10'
REDUCED = 0.01
AMT = 19.95

# def updatePage(driver, price):


def updateListing(driver):
    isUpdated = False
    try:
        items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//form[@name="modifyform"]//tr')))
        for item in items:
            try:
                textEl = item.find_element(By.XPATH, "./td[3]").text.lower().strip()
                td4 = item.find_element(By.XPATH, "./td[4]")
                # If next competitor is adultdeals on the left price bar. Leave it
                if not re.findall(r".+?adultdeals$", textEl):
                    try:
                        inputPrice = item.find_element(By.XPATH, "./td[4]//input[@type='text']")
                        currAmt = td4.text.partition("$")[2].partition("New")[0].strip()
                        redTextPrice = textEl.partition("$")[2].partition(" ")[0].strip()
                        newPrice=None
                        try:
                            item.find_element(By.XPATH, "./td[3]//span[contains(@class,'text-danger')]")
                            # set newPrice to price in 3rd col, red text
                            newPrice=str(round(float(redTextPrice) - REDUCED, 2))
                        except:
                            pass
                        # Lowest we wanna go is 99c we do not go lower no matter what
                        if float(currAmt)<0.99:
                            # when our price is below 0.99 try and add it up to 0.99$
                            newPrice=str(0.99)
                        else:
                            try:
                                item.find_element(By.XPATH, "./td[4]//i[contains(@class,'text-danger')]")
                                if textEl.strip() == 'new':
                                    # If our price is Empty box try and add ours to be 19.95
                                    newPrice(str(AMT))
                                else:
                                    # if red tick, reduce price
                                    newPrice=str(round(float(currAmt) - REDUCED, 2))
                            except:
                                pass                            
                        if newPrice is not None:
                            inputPrice.clear()
                            inputPrice.send_keys(newPrice)
                            isUpdated = True
                            # newTabUrl = item.find_element(By.XPATH, "./td[2]/a[2]").get_attribute("href")
                            # driver.switch_to.new_window('tab')
                            # sleep(1)
                            # driver.get(newTabUrl)
                            # # driver.switch_to.window(driver.window_handles[1])
                            # form = driver.find_element(By.NAME, "addlistingform")
                            # form.find_element(By.NAME, "price").clear()
                            # form.find_element(By.NAME, "price").send_keys(newPrice)
                            # form.find_element(By.TAG_NAME, "button").click()
                            # WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//form[@name="modifyform"]')))
                            # driver.close()
                            # driver.switch_to.window(driver.window_handles[0])
                        
                    except Exception as err:
                        # print(err)
                        pass
                # if len(textEl) >= 2:
                #     if textEl[-1].strip().lower() != 'adultdeals':
                #         amount = round(float(textEl[0].split("$")[-1].strip()) - REDUCED, 2)
                #         print(textEl[-1].strip().lower(), amount)
                #         inputPrice = item.find_element(By.XPATH, "./td[4]//input[@type='text']")
                #         inputPrice.send_keys(amount)
                #         isUpdated = True
                # else:
                #     try:
                #         redTick = item.find_element(By.XPATH, "./td[4]//i[contains(@class,'text-danger')]")
                #         redText = item.find_element(By.XPATH, "./td[4]").text
                #         print("Red Tick")
                #         amount = round(float(redText.split()[0].split('$')[-1].strip()) - REDUCED, 2)
                #         inputPrice = item.find_element(By.XPATH, "./td[4]//input[@type='text']")
                #         inputPrice.send_keys(amount)
                #         isUpdated = True
                #     except:
                #         pass
            except Exception as e:
                print('Error: inner loop '+e)
                pass
        if isUpdated:
            updateBtn = driver.find_element(By.XPATH, '//input[@name="update_prices"]')
            updateBtn.click()
    except Exception as e1:
        print('Error: outer loop '+e1)
        pass
    try:
        next_page = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '//ul[@class="pager"]//a')))
        next_page.click()
        # print('bp')
    except Exception as e2:
        print('End of the list, going to 1st again...')
        raise Exception("end of list")

def startFunc():
    website = 'https://www.adultdvdmarketplace.com/'

    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("detach", True)
    # options.add_argument("--headless=new")

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("debuggerAddress",
    #                                        "localhost:1111")
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    # driver = Chrome(executable_path=driverPath, options=chrome_options)
    # driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.get(website)
    driver.maximize_window()

    try:
        adultForm = driver.find_element(By.XPATH, '//div[@id="bottom"]//a')
        adultForm.click()
    except Exception as e1:
        print('Error: //div[@id="bottom"]//a '+e1)
        pass

    try:
        # LOGIN
        loginForm = driver.find_elements(By.XPATH,
                                         '//div[@id="main-container-home"]//div[contains(@class,"form-group")]')
        userName = loginForm[0].find_element(By.XPATH, '//input[@name="username"]')
        userName.send_keys(username)
        passWord = loginForm[1].find_element(By.XPATH, '//input[@name="password"]')
        passWord.send_keys(password)
        submitBtn = loginForm[2].find_element(By.XPATH, './/button')
        submitBtn.click()
    except Exception as e2:
        print('Error: login form issue '+e2)
        pass

    try:
        # MANAGE LISTING
        manageListing = driver.find_element(By.XPATH,
                                            '//div[@id="main-container-home"]//div[@class="list-group"]/div[4]/div[4]/a')
        manageListing.click()
    except:
        pass

    return driver

def startFuncDebug():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress",
                                           "localhost:1111")
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    return driver

def init():
    driver = startFunc()
    # driver = startFuncDebug()
    while True:
        try:
            updateListing(driver)
        except:
            # going to 1st page
            driver.get('https://www.adultdvdmarketplace.com/xcart/adult_dvd/modify_listings.php')

init()