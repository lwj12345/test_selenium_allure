from datetime import datetime

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#每次运行把账号密码设空，再把标记设为空
_TEST_USERNAME = None
_TEST_PASSWORD = None
_USER_GENERATED = False   # 标记：有没有生成过了？生成过就不再重新生成



def get_test_user():  #用于获取独特的账号与密码
     # 定义全局变量
    global _TEST_USERNAME, _TEST_PASSWORD, _USER_GENERATED
    if not _USER_GENERATED:
        # 第一次进来才生成：lwj + 时分秒
        username = "lwj" + datetime.now().strftime("%H%M%S")
        _TEST_USERNAME = username
        _TEST_PASSWORD = username
        _USER_GENERATED = True

    return {
        "username": _TEST_USERNAME,
        "password": _TEST_PASSWORD,
    }

def test_register_ok(driver):
    #注册账号。使用get_test_user的账号密码

    url = 'http://116.62.63.211/shop/'
    register_link_xpath = '/html/body/div[2]/div/ul[1]/div/div/a[2]'
    register_title = "用户注册"

    # 1. 访问商城项目
    driver.get(url)



    # 2. 找到并点击”注册“按钮
    el = driver.find_element(By.XPATH,register_link_xpath)
    el.click()

    # 3. 跳转到注册页面，断言登陆界面的title是否为用户登录
    assert register_title in driver.title

    #  从这里开始：同文件里所有 test_ 用例，想拿同一个账号密码，都直接写 user = get_test_user()
    user = get_test_user()
    username = user["username"]
    password = user["password"]
    print(f"[test_register_ok] 本次使用账号：{username} / 密码：{password}")

    # 4. 找到用户名输入框input，输入用户名
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div/div/form/div[1]/input")
    el.send_keys(username)

    # 5. 找到密码输入框，输入密码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div/div/form/div[2]/div/input")
    el.send_keys(password)

    # 6. 勾选协议,先定位到input勾选框，再用js直接设置input，arguments[0]代表传入的第一个参数（即后面的 checkbox元素），checked = true直接将这个复选框的 checked属性设置为 true，相当于勾选状态。
    checkbox = driver.find_element(By.NAME, "is_agree_agreement")
    driver.execute_script("arguments[0].checked = true;", checkbox)

    # 7. 找到注册按钮button，点击按钮
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[2]/div/div/div/form/div[4]/button")
    el.click()

    # 预期结果：（三种断言方式，判断是否登录成功）
    # ● 系统提示：注册成功
    el = driver.find_element(By.XPATH, "/html/body/div[10]/div/p")
    assert el.text == '注册成功'

    # ● 页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/"))
    assert driver.current_url == 'http://116.62.63.211/shop/'

    # ● 页面不再有登录按钮,有注册元素 列表el_list长度加一
    el_list = driver.find_elements(By.XPATH, '//*[text()="注册"]')
    assert len(el_list) == 0
    print(f"[test_register_ok]","注册成功")

def test_login_ok(driver):
    #登录测试,使用test_register_ok注册的账户
    user = get_test_user()
    username = user["username"]
    password = user["password"]
    print(f"[test_login_ok] 本次使用账号：{username} / 密码：{password}")

    # 1. 先退出登录，点击退出
    el = driver.find_element(By.XPATH, "/html/body/div[2]/div/ul[1]/div/div/a")
    el.click()

    # 3. 跳转到未登录首页
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/"))
    assert driver.current_url == 'http://116.62.63.211/shop/'

    # 2. 找到并点击”登录“按钮
    el = driver.find_element(By.XPATH, "/html/body/div[2]/div/ul[1]/div/div/a[1]")
    el.click()

    # 4. 找到用户名输入框input，输入正确用户名
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[1]/input")
    el.send_keys(username)

    # 5.    找到密码输入框，输入正确密码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[2]/div/input")
    el.send_keys(password)

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

def test_collect_shoppingcart_bay_ok(driver):

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

    # 19. 点击收藏
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div[1]/span")
    el.click()

    # 19. 点击加入购物车
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/button[2]")
    el.click()

    # 19. 点击购买
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/button[1]")
    el.click()

    #  页面跳转：跳转去目前最后一个窗口,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/buy/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/buy/index.html'

    # 20. 点击新增收货地址
    try:
        el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/button")
        el.click()
    except Exception:
        el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/button")
        el.click()  # 联动需要点时间加载市级列表

    # 先等弹窗里的 iframe 出现（src 包含 saveinfo.html 就是新增地址表单）
    iframe_el = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"am-popup-bd")]//iframe[contains(@src,"saveinfo")]')))
    time.sleep(0.5)  # 给 iframe 内部文档加载完成的时间
    driver.switch_to.frame(iframe_el)   # 切进 iframe 内部之后 driver 就在 iframe 小页面里工作了

    # 21. 输入别名  刘先生  (iframe 里明确有 name="alias" + placeholder="别名")
    el = driver.find_element(By.NAME, "alias")
    el.send_keys("刘先生")

    # 22. 输入姓名  刘伟
    el = driver.find_element(By.XPATH, './/input[@placeholder="姓名"]')
    el.send_keys("刘伟")

    # 23. 输入电话
    el = driver.find_element(By.XPATH, './/input[@placeholder="电话"]')
    el.send_keys("19812341234")

    # 24~29. 省市区县：省市区容器有特殊 class "am-form-group-region-linkage"，直接用这个 class 找最稳，因为他是下拉选择框
    # 这个am - form - group - region - linkage是AMUI 「区域联动组件」特有的class ， 整个页面里只有省市区这一排会带这个词 。
    region_box = driver.find_element(By.XPATH, './/div[contains(@class,"region-linkage")]')

    # 24. 点击省份下拉（省市区容器下第 1 个 div 下的 a）
    province_a = region_box.find_element(By.XPATH, './div[1]/a')
    province_a.click()

    # 25. 选择北京市（ul 下第 2 个 li，第 1 个是请选择）--------------------------两个选择最保险
    try:
        region_box.find_element(By.XPATH, './div[1]//ul/li[2]').click()
    except Exception:
        driver.find_element(By.XPATH, './/div[contains(@class,"region-linkage")]//div[1]//ul/li[2]').click()
    time.sleep(0.2)  # 联动需要点时间加载市级列表

    # 26. 点击城市下拉（第 2 个 div 下的 a）
    city_a = region_box.find_element(By.XPATH, './div[2]/a')
    city_a.click()

    # 27. 选择东城区--------------------------两个选择最保险
    try:
        region_box.find_element(By.XPATH, './div[2]//ul/li[2]').click()
    except Exception:
        driver.find_element(By.XPATH, './/div[contains(@class,"region-linkage")]//div[2]//ul/li[2]').click()
    time.sleep(0.2)

    # 28. 点击区县下拉（第 3 个 div 下的 a）
    county_a = region_box.find_element(By.XPATH, './div[3]/a')
    county_a.click()

    # 29. 输入区县名（区县下拉里带了搜索 input）--------------------------两个选择最保险
    try:
        region_box.find_element(By.XPATH, './div[3]//ul/li[2]').click()
    except Exception:
        driver.find_element(By.XPATH, './/div[contains(@class,"region-linkage")]//div[3]//ul/li[2]').click()
    time.sleep(0.2)

    # 30. 填写详细地址
    el = driver.find_element(By.XPATH, './/input[@placeholder="详细地址"]')
    el.send_keys("翻斗花园")

    # 31. 是否默认：name="is_default"，判断开关状态切换
    switch_wrapper = driver.find_element(By.XPATH,'.//input[@name="is_default"]/ancestor::div[contains(@class, "am-switch")][1]')
    classes = switch_wrapper.get_attribute("class")
    if "am-switch-off" in classes:
        print("当前是否 → 切换成是")
        switch_wrapper.click()
    else:
        print("当前已经是是 → 不点击")
    time.sleep(0.2)

    # 32. 保存地址（找表单底部含"保存"的 button，或者在 am-form-group-refreshing 组里找 button），--------------------------两个选择最保险
    try:
        save_btn = driver.find_element(By.XPATH, './/div[contains(@class,"form-group-refreshing")]//button')
    except Exception:
        save_btn = driver.find_element(By.XPATH, './/button[normalize-space(.)="保存" or contains(normalize-space(.),"保存")]')
    save_btn.click()
    time.sleep(0.5)
    driver.refresh()

    driver.switch_to.default_content()  # 退出所有 iframe 回到主页面
    time.sleep(1)
    driver.refresh()

    # 33. 选择支付方式，增添地址后页面发生变化
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[4]/ul/li[1]/span")
    el.click()

    # 34. 买家留言无
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[5]/div/input")
    el.send_keys("无")

    # 35. 提交订单
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[6]/div/form/div/button")
    el.click()

    # 36. 跳转订单管理页面，由于为测试阶段暂不购买
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/order/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/order/index.html'

def test_cart_bay(driver):
    #购物车结算
    # 2.    找到并点击”登录“按钮/html/body/div[5]/div/div[1]/label/span[1]
    el = driver.find_element(By.XPATH, "/html/body/div[1]/div/ul[2]/div[5]/div/a")
    el.click()

    # 36. 跳转订单管理页面，由于为测试阶段暂不购买
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/cart/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/cart/index.html'

    # 2.    找到并点击”全选“按钮
    el = driver.find_element(By.XPATH, "/html/body/div[5]/div/div[1]/label/span[1]")
    el.click()

    # 2.    找到并点击结算
    el = driver.find_element(By.XPATH, "/html/body/div[5]/div/div[2]/form/button")
    el.click()

    # 36. 跳转订单结算页面，由于为测试阶段暂不购买
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/buy/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/buy/index.html'

    # 33. 选择支付方式，增添地址后页面发生变化
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[4]/ul/li[1]/span")
    el.click()

    # 34. 买家留言无
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[5]/div/input")
    el.send_keys("无")

    # 35. 提交订单
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[6]/div/form/div/button")
    el.click()

    # 36. 跳转订单管理页面，由于为测试阶段暂不购买
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/order/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/order/index.html'

def test_order_management(driver):

    #查看是否添加成功，手动购买和购物车购买
    el_list = driver.find_elements(By.XPATH, '//*[text()="Huawei/华为 H60-L01 荣耀6 移动4G版智能手机 安卓"]')
    assert len(el_list) == 2

    # 35. 点击收藏管理
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/ul/li[2]/ul/li[3]/a")
    el.click()

    # 等待跳转成功
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/usergoodsfavor/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/usergoodsfavor/index.html'

    # 查看是否收藏成功
    el_list = driver.find_elements(By.XPATH, '//*[text()="Huawei/华为 H60-L01 荣耀6 移动4G版智能手机 安卓"]')
    assert len(el_list) == 1

    #点击个人信息
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/ul/li[4]/ul/li[1]/a")
    el.click()

    # 等待跳转成功
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/personal/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/personal/index.html'

    # 点击个人信息编辑
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/legend/a")
    el.click()

    # 等待跳转成功http://116.62.63.211/shop/personal/index.html
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/personal/saveinfo.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/personal/saveinfo.html'

    #输入昵称  ‘小白’
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/form/div[1]/input")
    el.send_keys("小白")

    #点击男性
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/form/div[2]/div/label[3]")
    el.click()

    #直接input输入生日
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/form/div[3]/input")
    el.click()
    el.send_keys("2004-08-01")

    #点击保存
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/form/div[4]/button")
    el.click()

    #跳转回去http:
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/personal/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/personal/index.html'

    # 点击个人足迹
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/ul/li[4]/ul/li[5]/a")
    el.click()

    # 等待跳转成功
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/usergoodsbrowse/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/usergoodsbrowse/index.html'

    # 查看足迹是否保存成功
    el_list = driver.find_elements(By.XPATH, '//*[text()="Huawei/华为 H60-L01 荣耀6 移动4G版智能手机 安卓"]')
    assert len(el_list) == 1

def test_user_password(driver):

    #点击进入安全设置页面
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/ul/li[4]/ul/li[3]/a")
    el.click()

    #点击修改
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/section[1]/div/a")
    el.click()

    # 跳转进去修改页面
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/safety/loginpwdinfo.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/safety/loginpwdinfo.html'

    user = get_test_user()
    password = user["password"]
    print(f"[user_management] 修改密码成功/ 新密码：lwj123456")

    #输入当前密码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/form/div[1]/input")
    el.send_keys(password)

    #输入新密码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/form/div[2]/input")
    el.send_keys("lwj123456")

    # 再输入新密码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/form/div[3]/input")
    el.send_keys("lwj123456")

    #点击保存
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/form/div[4]/button")
    el.click()

    #跳转回管理页面
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/safety/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/safety/index.html'

    #安全退出
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/ul/li[5]/a")
    el.click()

    #回到首页
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/"))
    assert driver.current_url == 'http://116.62.63.211/shop/'

    user = get_test_user()
    username = user["username"]
    print(f"[test_login_ok] 本次使用账号：{username} / 新密码：lwj123456")

    # 2.    找到并点击”登录“按钮
    el = driver.find_element(By.XPATH, "/html/body/div[2]/div/ul[1]/div/div/a[1]")
    el.click()

    # 4.    找到用户名输入框input，输入正确用户名
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[1]/input")
    el.send_keys(username)

    # 5.    找到密码输入框，输入正确密码
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[2]/div/input")
    el.send_keys("lwj123456")

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















