import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def screenshot_on_end(driver):
    yield
    # 用例结束时截图
    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="UI截图",
            attachment_type=AttachmentType.PNG
        )
    except Exception as e:
        print(f"截图失败: {e}")


@allure.epic("用户中心")
@allure.feature("登录功能")
@allure.story("登录成功")
@allure.title("测试已注册用户使用正确的用户名和密码成功登录")
def test_login_success(driver, screenshot_on_end):
    """
    测试已注册用户能够使用正确的用户名和密码成功登录系统。
    """

    # 数据
    url = 'http://116.62.63.211/shop/'
    username = "kskbl12345"
    password = "lwj123456"
    # 定位
    login_link_xpath = '//a[text()="登录"]'
    username_input_xpath = '//input[@placeholder="请输入用户名/手机/邮箱"]'
    password_input_xpath = '//input[@placeholder="请输入登录密码"]'
    login_button_xpath = '//button[text()="登录"]'
    success_message_xpath = '//p[@class="prompt-msg"]'
    # 断言
    success_message_value = "登录成功"
    login_link_count = 0

    driver.get(url)

    # 1. 点击“登录”链接
    with allure.step("点击“登录”链接"):
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, login_link_xpath))
        )
        login_link.click()

        # 2. 输入用户名
        with allure.step("输入用户名"):
            username_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, username_input_xpath))
            )
            username_input.send_keys(username)

        # 3. 输入密码
        with allure.step("输入密码"):
            password_input = WebDriverWait(driver, 10).until(  # 从经验来看，用户名和密码一起出现，不需要重复进行显式等待
                EC.visibility_of_element_located((By.XPATH, password_input_xpath))
            )
            password_input.send_keys(password)

        # 4. 点击“登录”按钮
        with allure.step("点击“登录”按钮"):
            login_button = WebDriverWait(driver, 10).until(  # 从经验来看，用户名和密码一起出现，不需要重复进行显式等待
                EC.visibility_of_element_located((By.XPATH, login_button_xpath))
            )
            login_button.click()

        # 5. 断言登录成功提示
        with allure.step("断言登录成功提示"):
            success_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, success_message_xpath))
            )
            assert success_message.text == success_message_value

        # 6. 断言页面上不再有“登录”链接
        with allure.step("断言页面上不再有“登录”链接"):
            WebDriverWait(driver, 10).until(  
                EC.url_to_be(url)
            )
            assert len(driver.find_elements(By.XPATH, login_link_xpath)) == login_link_count



