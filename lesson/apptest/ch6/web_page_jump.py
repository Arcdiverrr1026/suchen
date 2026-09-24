import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "http://xczx2-portal.itheima.net/"


class TestWebPageJump(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(BASE_URL)

    def test_web_page_jump(self):
        expect_one = "最新"
        expect_two = "获取验证码"

        # 1. 点击“课程”
        self.driver.find_element(By.ID, "course-page").click()
        time.sleep(2)

        # 2. 获取课程页面中的“最新”文本，并断言
        newest = self.driver.find_element(By.LINK_TEXT, "最新").text
        self.assertEqual(expect_one, newest)
        print("课程页面跳转成功")

        # 3. 点击“注册”
        self.driver.find_element(By.LINK_TEXT, "注册").click()
        time.sleep(2)

        # 4. 获取注册页面中的“获取验证码”文本，并断言
        verification_code = self.driver.find_element(
            By.XPATH,
            "/html/body/div/div/div[4]/form/div[2]/div/div/div[2]/button/span"
        ).text
        self.assertEqual(expect_two, verification_code)
        print("注册页面跳转成功")

        # 5. 返回首页
        self.driver.get(BASE_URL)
        time.sleep(2)
        print("返回首页面跳转成功")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()