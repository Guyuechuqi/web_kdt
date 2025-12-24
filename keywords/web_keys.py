from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.captcha_util import get_captcha
from common.yaml_util import read_config
from config.path import DATA_PATH


class WebKeys:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = read_config()["common"]["timeout"]

    def open_url(self, url):
        base_url = read_config()["common"]["base_url"]
        self.driver.get(base_url+url)
        self.driver.maximize_window()

    def get_element(self, method, value):
        locator = (getattr(By, method.upper()), value)
        from selenium.common import TimeoutException
        try:
            return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print(f"元素定位失败：{locator}")
            raise TimeoutException

    def input(self, method, value, text=None):
        element = self.get_element(method, value)
        if text is None:
            element.clear()
        else:
            element.send_keys(text)

    def click(self, method, value):
        self.get_element(method, value).click()

    def upload(self, method, value, file=None):
        file_path = str(DATA_PATH/file)
        self.get_element(method, value).send_keys(file_path)

    def input_captcha(self, method, value):
        captcha_value = get_captcha()
        self.get_element(method, value).send_keys(captcha_value)

    def screenshot(self, method, value, file):
        file_path = str(DATA_PATH/file)
        self.get_element(method, value).screenshot(file_path)

    def assert_text(self, method, value, expect_text):
        try:
            actual_text = self.get_element(method, value).text
            if actual_text.isdigit():
                expect_text = str(expect_text)
            assert expect_text in actual_text, f"断言失败：预期包含'{expect_text}'"
        except Exception as e:
            print(f"--> 断言异常: {e}")
            raise e

    def quit_browser(self):
        self.driver.quit()

    def execute_login(self):
        account, password = read_config()["fecshop"].values()
        self.open_url("/cn/customer/account/login")
        self.input("CSS_SELECTOR", "#phone", account)
        self.input("CSS_SELECTOR", "#password", password)
        self.click("CSS_SELECTOR", "#login-btn")
