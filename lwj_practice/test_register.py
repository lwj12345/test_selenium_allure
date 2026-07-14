from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_register_ok(driver):
    #注册和自动登录测试
    # 1.    访问商城项目
    driver.get("http://116.62.63.211/shop/")

    # 2.    找到并点击”注册“按钮
    el = driver.find_element(By.XPATH, "/html/body/div[2]/div/ul[1]/div/div/a[2]")
    el.click()

    # 3.    跳转到注册页面，断言登陆界面的title是否为用户登录
    assert "用户注册" in driver.title

    # 使用lwj+实时时间来代替账号和密码
    username = "lwj" + datetime.now().strftime("%H%M%S")
    password = username

    # 4.    找到用户名输入框input，输入用户名
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div/div/form/div[1]/input")
    el.send_keys(username)

    # 5.    找到密码输入框，输入密码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div/div/form/div[2]/div/input")
    el.send_keys(password)

    # 6.    勾选协议,用js直接勾选，跳过鼠标模拟操作
    checkbox = driver.find_element(By.NAME, "is_agree_agreement")
    driver.execute_script("arguments[0].checked = true;", checkbox)

    # 7.    找到注册按钮button，点击按钮
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div/div/form/div[4]/button")
    el.click()

    # 预期结果：
    # ● 系统提示：注册成功
    el = driver.find_element(By.XPATH, "/html/body/div[10]/div/p")
    assert el.text == '注册成功'

    # ● 页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/"))
    assert driver.current_url == 'http://116.62.63.211/shop/'

    # ● 页面不再有登录按钮,有注册元素 列表el_list长度加一
    el_list = driver.find_elements(By.XPATH, '//*[text()="注册"]')
    assert len(el_list) == 0


def test_login_ok(driver):
    # 对整个loggong进行配置
    logging.basicConfig(level=logging.DEBUG)  # 在控制台输出日志内容，selenium自带的loggong日志功能

    #登录测试
    # 1.    访问商城项目
    driver.get("http://116.62.63.211/shop/")

    # 2.    找到并点击”登录“按钮
    el = driver.find_element(By.XPATH, "/html/body/div[2]/div/ul[1]/div/div/a[1]")
    el.click()

    # 3.    跳转到登录页面，断言登陆界面的title是否为用户登录
    assert "用户登录" in driver.title

    # 4.    找到用户名输入框input，输入正确用户名
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[1]/input")
    el.send_keys("kskbl12345")

    # 5.    找到密码输入框，输入正确密码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[2]/div/input")
    el.send_keys("kskbl12345")

    # 6.    找到登录按钮button，点击按钮
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[3]/button")
    el.click()

    # 预期结果：
    # ● 系统提示：登录成功
    el = driver.find_element(By.XPATH, "/html/body/div[10]/div/p")
    assert el.text == '登录成功'

    # ● 页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/"))
    assert driver.current_url == 'http://116.62.63.211/shop/'

    # ● 页面不再有登录按钮,有登录元素 列表el_list长度加一
    el_list = driver.find_elements(By.XPATH, '//*[text()="登录"]')
    assert len(el_list) == 0