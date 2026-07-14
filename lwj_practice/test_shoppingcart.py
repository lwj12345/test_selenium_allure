import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_ok(driver):
    #登录测试
    # 1. 访问商城项目
    driver.get("http://116.62.63.211/shop/")

    # 2. 找到并点击”登录“按钮
    el = driver.find_element(By.XPATH, "/html/body/div[2]/div/ul[1]/div/div/a[1]")
    el.click()

    # 3. 跳转到登录页面，断言登陆界面的title是否为用户登录
    assert "用户登录" in driver.title

    # 4. 找到用户名输入框input，输入正确用户名
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[1]/input")
    el.send_keys("kskbl12345")

    # 5. 找到密码输入框，输入正确密码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[2]/div/input")
    el.send_keys("kskbl12345")

    # 6. 找到登录按钮button，点击按钮
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[3]/button")
    el.click()

    #  系统提示：登录成功
    el = driver.find_element(By.XPATH, "/html/body/div[10]/div/p")
    assert el.text == '登录成功'

    #  页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/"))
    assert driver.current_url == 'http://116.62.63.211/shop/'

    #  页面不再有登录按钮,有登录元素 列表el_list长度加一
    el_list = driver.find_elements(By.XPATH, '//*[text()="登录"]')
    assert len(el_list) == 0

    # 8. 移动鼠标去数码办公类
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/ul/li[1]/a")
    actions = ActionChains(driver)  # 动作作用在这个浏览器中
    actions.move_to_element(el)
    actions.perform()

    # 9. 选择手机通讯类的手机
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/ul/li[1]/div/div/div/div/div/dl[1]/dd[1]/a")
    el.click()

    #  页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/search/index/category_id/68.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/search/index/category_id/68.html'

    # 10. 鼠标勾选品牌
    el = driver.find_element(By.XPATH,"/html/body/div[4]/div/div[2]/div/div/ul/li[2]/div[2]/ul/li[1]")
    el.click()

    # 11. 鼠标勾选价格
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/div/ul/li[3]/div[2]/ul/li[6]")
    el.click()

    # 12. 选择华为手机
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/ul/li/div")
    el.click()

    #  页面跳转：跳转去目前最后一个窗口,在10秒内重复检查url是否为http://116.62.63.211/shop/goods/index/id/4.html，最多等十秒
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/goods/index/id/4.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/goods/index/id/4.html'

    # 13. 只移动鼠标查看二维码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[2]/div/div[3]")
    actions = ActionChains(driver)  # 动作作用在这个浏览器中
    actions.move_to_element(el)
    actions.perform()

    # 14. 只移动鼠标查看手机放大图
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/div/img")
    actions = ActionChains(driver)  # 动作作用在这个浏览器中
    actions.move_to_element(el)
    actions.move_by_offset(66, 66)
    actions.perform()

    # 15. 移动鼠标查看手机平面图
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[1]/div/ul/li[2]/div/a/img")
    actions = ActionChains(driver)  # 动作作用在这个浏览器中
    actions.move_to_element(el)
    actions.perform()

    # 16. 添加数量
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[2]/dl/dd/div[2]/div[3]/form/div[1]/div[2]/dd/div/button[2]")
    el.click()
  
    # 17. 减少数量
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[2]/dl/dd/div[2]/div[3]/form/div[1]/div[2]/dd/div/button[1]")
    el.click()

    # 18. 直接输入购买数量1，arguments[0].value = '1'；
    # 将input的值改成1；arguments[0].dispatchEvent(new Event('change', { bubbles: true }));将修改的信号往上传输
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[2]/dl/dd/div[2]/div[3]/form/div[1]/div[2]/dd/div/input")
    driver.execute_script("arguments[0].value = '1'; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", el)

    # 19. 点击加入购物车
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/button[2]")
    el.click()








