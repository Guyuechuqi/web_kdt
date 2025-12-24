import logging
import pytest
from pytest_xlsx.file import XlsxItem
from selenium import webdriver

from keywords.web_keys import WebKeys

EXCLUDED_FIELDS = ["meta", "Step", "Description", "Action", "_BlankField"]

#pytest_xlsx_run_step 通常用于读取 XlsxItem（即 Excel 中的一行数据），解析其中的关键字（Keyword），并执行相应的操作
def pytest_xlsx_run_step(item: XlsxItem):
    step = item.current_step
    action_name = step.get("Action")

    logging.info(f"正在执行步骤: {action_name} | 数据: {step}")

    if not hasattr(item, 'web_keys'):
        driver = item.usefixtures.get("chrome") or item.usefixtures.get("login_chrome")
        if not driver:
            raise RuntimeError("无法获取浏览器驱动！")
        item.web_keys = WebKeys(driver)

    wk = item.web_keys

    if not hasattr(wk, action_name):
        error_msg = f"关键字类中未找到方法: {action_name}，请检查Excel拼写或代码封装。"
        logging.error(error_msg)
        raise AttributeError(error_msg)

    func_args = [v for k, v in step.items()
                   if k not in EXCLUDED_FIELDS and v is not None]

    try:
        getattr(wk, action_name)(*func_args)
    except Exception as e:
        logging.error(f"步骤 {action_name} 执行失败: {e}")
        raise e

    return True

@pytest.fixture(scope="function")
def chrome():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver

@pytest.fixture(scope="function")
def login_chrome():
    driver = webdriver.Chrome()
    driver.maximize_window()
    WebKeys(driver).execute_login()
    yield driver