import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "http://xczx2-portal.itheima.net/"
USERNAME = os.getenv("XCZX_USERNAME")
PASSWORD = os.getenv("XCZX_PASSWORD")


class TestLoginAndLogout(unittest.TestCase):

    def setUp(self):
        if not USERNAME or not PASSWORD:
            self.skipTest("请设置 XCZX_USERNAME 和 XCZX_PASSWORD 后运行登录测试")
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(BASE_URL)

    def test_login_and_logout(self):
        driver = self.driver
        expect = USERNAME

        driver.find_element(By.LINK_TEXT, "登录").click()

        username = driver.find_element(
            By.XPATH,
            "/html/body/div/div/div[3]/form/div[1]/div/div/input"
        )
        username.clear()
        username.send_keys(USERNAME)

        password = driver.find_element(
            By.XPATH,
            "/html/body/div/div/div[3]/form/div[2]/div/div/input"
        )
        password.clear()
        password.send_keys(PASSWORD)

        driver.find_element(By.CLASS_NAME, "el-button--primary").click()
        time.sleep(2)

        account = driver.find_element(By.CLASS_NAME, "dropbtn").text
        self.assertEqual(expect, account)

        driver.find_element(By.LINK_TEXT, "个人中心").click()
        time.sleep(2)

        driver.find_element(By.CLASS_NAME, "glyphicon-log-out").click()
        print("成功退出学成在线教育平台")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
