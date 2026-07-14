from datetime import time

from selenium import webdriver

from selenium.webdriver.common.by import By

import logging

#对整个loggong进行配置
logging.basicConfig(level=logging.DEBUG)  #在控制台输出日志内容，selenium自带的loggong日志功能

#启动浏览器
driver = webdriver.Chrome()

#控制浏览器
driver.get("http://116.62.63.211/shop/user/logininfo.html")

#元素对象
el = driver.find_element("name",'accounts')
el.send_keys("1231231231")

#截图
# driver.get_screenshot_as_file("page.png")

# 1.  窗口最大化
time.sleep(5)
driver.maximize_window()
print('窗口已经最大化')

# 2. 指定窗口大小
time.sleep(5)
driver.set_window_size(110,2000)
print('窗口改为指定的大小')

# 3. 最小化
time.sleep(5)
driver.minimize_window()
print('窗口已经最小化')

# 1. 跳转
time.sleep(3)
driver.get("http://116.62.63.211/shop/")

# 2. 刷新
time.sleep(3)
driver.refresh()  # URL不变，但是内容更新

# 3.后退（回退到之前的URL）
time.sleep(3)
driver.back()  # 退到空白页面

# 4.前进（撤销一次回退）
time.sleep(3)
driver.forward()  # 重新进入项目

# 获取信息：
print('标题：', driver.title)
print('URL：', driver.current_url)
print('网页内容（HTML）', driver.page_source)
# print('网页内容（PNG）', driver.get_screenshot_as_file("page.png"))
print('cookies', driver.get_cookies())

#XPATH定位
el = driver.find_element(By.XPATH, "/html/body/div[2]/div/ul[1]/div/div/a[2]")
print(el)

#//*  定位任意节点任意标签，[text()="登录"]  元素文本为登录的
el_list = driver.find_elements(By.XPATH, '//*[text()="登录"]')

#强制等待
time.sleep(5)

#隐式等待
driver.implicitly_wait(5)

#显示等待，在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
# WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/"))
# assert driver.current_url == 'http://116.62.63.211/shop/'

#单击鼠标
el.click()

#键盘输入
el.send_keys()

from selenium.webdriver.common.keys import Keys
#ctrl+a
el.send_keys(Keys.CONTROL + "a")

#清空输入框
el.clear()

#获取元素文本  <a href="http://116.62.63.211/shop/user/logininfo.html">登录</a>
data = el.text
print(data)  # 登录

#获取元素属性
data = el.get_attribute("href")
print(data)  # http://116.62.63.211/shop/user/logininfo.html

#获取元素标记
tag_name = el.tag_name
print(tag_name)  # a

#鼠标操作
# actions = ActionChains(driver) # 动作作用在这个浏览器中
# actions.move_to_element(el)：移动到指定元素（不点击）
# actions.move_by_offset(el)：移动到相对位置
# actions.click(el)：左键单击
# actions.context_click(el)：右键单击
# actions.double_click(el)：左键双击
# actions.click_and_hold(el)：按住不妨
# actions.release(el)：释放鼠标
# actions.drag_and_drop(el)：拖拽（a元素拖动到b元素上面）
# actions.perform()  # 执行动作----------------------------------------------没有它鼠标动作不执行

#键盘操作
# send_keys：输入内容
# key_down：按住不妨
# key_up：松开按键

#ctrl+a
# actions.key_down(Keys.CONTROL)          # 按住 Ctrl
# actions.key_down('a')

# pause：暂停，以秒为单位，在动作链中加了强制等待
# reset_actions：清除已编排动作。 效果等同于实例化一个新的动作链
# perform：执行已编排动作

#有跳转时要手动
print('当前的所有窗口',driver.window_handles) # 列表
driver.switch_to.window(driver.window_handles[-1])  # 切换到最后一个窗口

#切进去了一定要切出来
# user_driver.switch_to.frame(frame)
# user_driver.switch_to.default_content() # 退出所有框架

#关闭浏览器
driver.quit()