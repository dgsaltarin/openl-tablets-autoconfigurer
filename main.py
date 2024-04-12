from selenium import webdriver
import unittest
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

class AutoCnfiguration(unittest.TestCase):

    @classmethod
    def test_SetupClass(cls):
        ## Setup chrome options
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        homedir = os.path.expanduser("~")
        webdriver_service = Service(f"/usr/local/bin/chromedriver")
        print(os.environ.get('RULE_ENGINE_URL'))

        # Choose Chrome Browser
        browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        browser.get(os.environ.get('RULE_ENGINE_URL'))
        browser.maximize_window()

        # start configuration
        browser.find_element(By.XPATH, '/html/body/div[2]/div/div/form/div[2]/input').click()

        # Enter webstudio working directory
        browser.find_element(By.XPATH, '//*[@id="j_idt13"]/div[2]/input').click()

        # Configure Design Repository
        type_list = browser.find_element(By.ID, 'j_idt14:j_idt23')
        select_type = Select(type_list)
        select_type.select_by_visible_text('AWS S3')
        browser.implicitly_wait(10)
        browser.find_element(By.NAME, 'j_idt14:j_idt82').click()
        browser.find_element(By.NAME, 'j_idt14:j_idt82').send_keys(os.environ.get('BUCKET_NAME'))
        region_list = browser.find_element(By.XPATH, '//*[@id="j_idt14:designParameters"]/table/tbody/tr[3]/td[2]/select')
        select_region = Select(region_list)
        select_region.select_by_visible_text('US East (N. Virginia)')
        browser.find_element(By.XPATH, '//*[@id="j_idt14:designParameters"]/table/tbody/tr[4]/td[2]/input').send_keys(os.environ.get('AWS_ACCESS_KEY_ID'))
        browser.find_element(By.XPATH, '//*[@id="j_idt14:designParameters"]/table/tbody/tr[5]/td[2]/input').send_keys(os.environ.get('AWS_SECRET_ACCESS_KEY'))
        browser.find_element(By.XPATH, '//*[@id="j_idt14:repositoryProps"]/div[3]/input[2]').click()

        # Configure User mode
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="step3Form:userMode:2"]'))).click()
        browser.find_element(By.XPATH, '//*[@id="step3Form:adAdminUsers"]').send_keys('dsaltarin,astefanov')
        browser.find_element(By.XPATH, '//*[@id="step3Form:dbUrl"]').clear()
        browser.find_element(By.XPATH, '//*[@id="step3Form:dbUrl"]').send_keys(os.environ.get('DB_URL'))
        browser.find_element(By.XPATH, '//*[@id="step3Form:dbUsername"]').send_keys(os.environ.get('DB_USERNAME'))
        browser.find_element(By.XPATH, '//*[@id="step3Form:dbPassword"]').send_keys(os.environ.get('DB_PASSWORD'))
        browser.find_element(By.XPATH, '//*[@id="finish-buttons"]/input[2]').click()
        browser.implicitly_wait(10)

        # Login
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginName"]'))).send_keys(os.environ.get('USERNAME'))
        browser.find_element(By.XPATH, '//*[@id="loginPassword"]').send_keys(os.environ.get('PASSWORD'))
        browser.find_element(By.XPATH, '//*[@id="loginSubmit"]').click()

        # configure deployment repository
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ll"]/a[3]'))).click()
        repository_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/ul/li[2]/a')
        browser.execute_script("arguments[0].click();", repository_button)
        #WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.NAME, 'systemSettingsForm:j_idt106'))).click()
        deployment_button = browser.find_element(By.ID, 'systemSettingsForm:j_idt106')
        browser.execute_script("arguments[0].click();", deployment_button)
        deployment_type_list = browser.find_element(By.ID, 'systemSettingsForm:j_idt656:0:j_idt661')
        select_deployment_type = Select(deployment_type_list)
        select_deployment_type.select_by_visible_text('AWS S3')
        browser.implicitly_wait(10)
        browser.find_element(By.NAME, 'systemSettingsForm:j_idt656:0:j_idt719').click()
        browser.find_element(By.NAME, 'systemSettingsForm:j_idt656:0:j_idt719').send_keys(os.environ.get('BUCKET_NAME'))
        deployment_region_list = browser.find_element(By.XPATH, '//*[@id="systemSettingsForm:j_idt656:0:productionParameters"]/table/tbody/tr[3]/td[2]/select')
        select_deployment_region = Select(deployment_region_list)
        select_deployment_region.select_by_visible_text('US East (N. Virginia)')
        browser.find_element(By.XPATH, '//*[@id="systemSettingsForm:j_idt656:0:productionParameters"]/table/tbody/tr[4]/td[2]/input').send_keys(os.environ.get('AWS_ACCESS_KEY_ID'))
        browser.find_element(By.XPATH, '//*[@id="systemSettingsForm:j_idt656:0:productionParameters"]/table/tbody/tr[5]/td[2]/input').send_keys(os.environ.get('AWS_SECRET_ACCESS_KEY'))
        browser.find_element(By.XPATH, '//*[@id="systemSettingsForm:j_idt922"]').click()

        browser.quit()

if __name__ == '__main__':
    unittest.main()
