from selenium import webdriver
from selenium.webdriver.common.by import By
import html2text
from selenium.webdriver.chrome.options import Options

class StockScreenerScraper:
    def __init__(self, login_email=None, login_pass=None):
        self.options = Options()
        self.options.add_argument('--headless=new')
        self.driver = webdriver.Chrome(options=self.options)
        self.converter = html2text.HTML2Text()
        self.login_email = login_email
        self.login_pass = login_pass
        if (self.login_email is None or self.login_email == '') or (self.login_pass is None or self.login_pass == ''):
            pass
        else:
            self.login_screener()

    def login_screener(self):
        try:
            self.driver.get('https://www.screener.in')
            self.driver.find_element(By.XPATH, '/html/body/nav/div[2]/div/div/div/div[2]/div[2]/a[1]').click()
            email_field = self.driver.find_element(By.NAME, 'username')
            pass_field = self.driver.find_element(By.NAME, 'password')
            email_field.send_keys(self.login_email)
            pass_field.send_keys(self.login_pass)
            self.driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/form/button').click()

        except Exception as e:
            print(f"Error during login: {e}")
            raise

    def preprocess(self):
        self.remove_links()
        self.click_show_more()
        self.remove_elements()

    def remove_links(self):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        links = body.find_elements(By.TAG_NAME, 'a')
        for link in links:
            self.driver.execute_script("arguments[0].removeAttribute('href');", link)

    def click_show_more(self):
        try:
            self.driver.find_element(By.CLASS_NAME, 'show-more-button').click()
            self.driver.find_element(By.XPATH, '//*[@id="shareholding"]/div[1]/div[2]/div[1]/button[1]').click()
        except:
            pass

    # Remove Unwanted elements
    def remove_elements(self):
        remove_xpath = [
            '//*[@id="top"]/div[2]',
            '//*[@id="top"]/div[2]/div[2]/div',
            '//*[@id="top"]/div[1]/div/div[1]',
            '//*[@id="top"]/div[1]/div/div',
            '//*[@id="top"]/div[1]/form',
            '//*[@id="top"]/div[2]/div[1]/div[1]/div[3]',
            '//*[@id="top"]/div[2]/div[1]/div[2]',
            '//*[@id="top"]/div[2]/div[1]/div[1]/div[3]',
            '//*[@id="top"]/div[2]/div[1]/div[1]/button',
            '//*[@id="profit-loss"]/div[1]/div[1]/p',
            '//*[@id="profit-loss"]/div[1]/div[2]',
            '//*[@id="quarters"]/div[1]/div[1]/p',
            '//*[@id="quarters"]/div[1]/div[2]',
            '//*[@id="quarters"]/div[3]/table/tbody/tr[12]',
            '//*[@id="ratios"]/div[1]/div[1]/p',
            '//*[@id="shareholding"]/div[1]/div[2]',
            '//*[@id="shareholding"]/p',
            '//*[@id="yearly-shp"]',
            '//*[@id="peers"]/div[1]/div[2]',
            '//*[@id="peers"]/div[3]',
            '//*[@id="peers-table-placeholder"]/div[3]/table/tfoot',
            '//*[@id="balance-sheet"]/div[1]/div[2]',
            '//*[@id="balance-sheet"]/div[1]/div[1]/p',
            '//*[@id="cash-flow"]/div[1]/div[1]/p',
            '//*[@id="documents"]',
            '//*[@id="chart"]',
            '//*[@id="analysis"]'
        ]

        for xpath in remove_xpath:
            try:
                self.driver.execute_script("arguments[0].remove();", self.driver.find_element(By.XPATH, xpath))
            except:
                pass
    
    # Scrapes the Whole Page with Sector Page
    def get_full_data(self,ticker):
        try:
            self.ticker = ticker
            self.url = f'https://www.screener.in/company/{self.ticker}/consolidated/'
            self.driver.get(self.url)
            sector_url = self.driver.find_element(By.XPATH, '//*[@id="peers"]/div[1]/div[1]/p').find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
            self.preprocess()
            full_data = self.driver.find_element(By.XPATH, '/html/body/main')
            full_data_html = full_data.get_attribute('outerHTML')
            full_data_markdown = self.converter.handle(full_data_html)

            try:
                self.driver.get(sector_url)
                self.remove_links()
                self.driver.execute_script("arguments[0].remove();", self.driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]'))
                self.driver.execute_script("arguments[0].remove();", self.driver.find_element(By.XPATH, '/html/body/main/div[2]/div[4]'))
            except:
                pass

            sector_data = self.driver.find_element(By.XPATH, '/html/body/main/div[2]')
            sector_data_html = sector_data.get_attribute('outerHTML')
            sector_data_markdown = self.converter.handle(sector_data_html)
        except:
            pass

        return full_data_markdown,sector_data_markdown

    # Close Driver
    def close(self):
        self.driver.quit()