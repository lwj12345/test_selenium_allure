from datetime import datetime

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#每次运行把账号密码设空，再把标记设为空
_TEST_USERNAME = None
_TEST_PASSWORD = None
_USER_GENERATED = False   # 标记：有没有生成过了？生成过就不再重新生成


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


@allure.epic("用户中心")
@allure.feature("注册功能")
@allure.story("注册成功")
@allure.title("测试用户使用正确的用户名和密码注册登录")
def test_register_ok(driver,screenshot_on_end):
    #注册账号。使用get_test_user的账号密码

    url = 'http://116.62.63.211/shop/'
    register_link_xpath = '/html/body/div[2]/div/ul[1]/div/div/a[2]'
    register_title_xpath = "用户注册"
    user_username_input_xpath = '/html/body/div[4]/div/div/div[2]/div/div/div/form/div[1]/input'
    user_password_input_xpath = '/html/body/div[4]/div/div/div[2]/div/div/div/form/div[2]/div/input'
    agreement_input_NAME = 'is_agree_agreement'
    register_button_xpath = '/html/body/div[4]/div/div/div[2]/div/div/div/form/div[4]/button'
    register_success_title_xpath = '/html/body/div[10]/div/p'
    register_success_text = "注册成功"

    #  从这里开始：同文件里所有 test_ 用例，想拿同一个账号密码，都直接写 user = get_test_user()
    user = get_test_user()
    username = user["username"]
    password = user["password"]
    print(f"[test_register_ok] 本次使用账号：{username} / 密码：{password}")

    # 1. 访问商城项目
    driver.get(url)

    # 1. 点击“登录”链接
    with allure.step("点击注册链接"):
        # 2. 找到并点击”注册“按钮
        el = driver.find_element(By.XPATH, register_link_xpath)
        el.click()

        with allure.step("跳转注册页面成功"):
            # 3. 跳转到注册页面，断言登陆界面的title是否为用户登录
            assert register_title_xpath in driver.title

        with allure.step("输入用户名"):
            # 4. 找到用户名输入框input，输入用户名
            el = driver.find_element(By.XPATH, user_username_input_xpath)
            el.send_keys(username)

        with allure.step("输入密码"):
            # 5. 找到密码输入框，输入密码
            el = driver.find_element(By.XPATH, user_password_input_xpath)
            el.send_keys(password)

        with allure.step("勾选相关协议"):
            # 6. 勾选协议,先定位到input勾选框，再用js直接设置input，arguments[0]代表传入的第一个参数（即后面的 checkbox元素），checked = true直接将这个复选框的 checked属性设置为 true，相当于勾选状态。
            checkbox = driver.find_element(By.NAME, agreement_input_NAME)
            driver.execute_script("arguments[0].checked = true;", checkbox)

        with allure.step("点击注册按钮"):
            # 7. 找到注册按钮button，点击按钮
            el = driver.find_element(By.XPATH, register_button_xpath)
            el.click()

        with allure.step("断言注册成功提示"):
            # 预期结果：（三种断言方式，判断是否登录成功）
            # ● 系统提示：注册成功
            el = driver.find_element(By.XPATH, register_success_title_xpath)
            assert el.text == register_success_text

        with allure.step("注册成功并登录账号返回首页"):
            # ● 页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
            WebDriverWait(driver, 10).until(EC.url_to_be(url))
            assert driver.current_url == url
            print(f"[test_register_ok]", "注册成功")


@allure.epic("用户中心")
@allure.feature("登录功能")
@allure.story("登录成功")
@allure.title("测试用户使用已注册的正确的用户名和密码登录")
def test_login_ok(driver,screenshot_on_end):
    #登录测试,使用test_register_ok注册的账户

    user = get_test_user()
    username = user["username"]
    password = user["password"]
    print(f"[test_login_ok] 本次使用账号：{username} / 密码：{password}")

    url = 'http://116.62.63.211/shop/'
    login_exit_link_xpath = '/html/body/div[2]/div/ul[1]/div/div/a'
    login_link_xpath = '/html/body/div[2]/div/ul[1]/div/div/a[1]'
    user_username_input_xpath = '/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[1]/input'
    user_password_input_xpath = '/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[2]/div/input'
    login_button_xpath = '/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[3]/button'
    login_success_xpath = '/html/body/div[10]/div/p'
    login_success_text = "登录成功"

    with allure.step("点击退出，退出登录"):
        # 1. 先退出登录，点击退出
        el = driver.find_element(By.XPATH, login_exit_link_xpath)
        el.click()

        with allure.step("断言跳转未登录页面成功"):
            # 2. 跳转到未登录首页
            WebDriverWait(driver, 10).until(EC.url_to_be(url))
            assert driver.current_url == url

        with allure.step("点击登录链接"):
            # 3. 找到并点击”登录“按钮
            el = driver.find_element(By.XPATH, login_link_xpath)
            el.click()

        with allure.step("输入用户名"):
            # 4. 找到用户名输入框input，输入正确用户名
            el = driver.find_element(By.XPATH, user_username_input_xpath)
            el.send_keys(username)

        with allure.step("输入密码"):
            # 5. 找到密码输入框，输入正确密码
            el = driver.find_element(By.XPATH, user_password_input_xpath)
            el.send_keys(password)

        with allure.step("点击登录按钮"):
            # 6. 找到登录按钮button，点击按钮
            el = driver.find_element(By.XPATH, login_button_xpath)
            el.click()

        with allure.step("断言注册成功提示"):
            # 预期结果：
            # ● 系统提示：登录成功
            el = driver.find_element(By.XPATH, login_success_xpath)
            assert el.text == login_success_text

        with allure.step("成功进入商城首页"):
            # ● 页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
            WebDriverWait(driver, 10).until(EC.url_to_be(url))
            assert driver.current_url == url


@allure.epic("用户中心")
@allure.feature("下单功能")
@allure.story("下单成功")
@allure.title("测试用户使用合法地址在商城下单")
def test_collect_shoppingcart_bay_ok(driver,screenshot_on_end):

    mouse_move_xpath = '/html/body/div[4]/div/div/div/ul/li[1]/a'
    phone_communication_xpath = '/html/body/div[4]/div/div/div/ul/li[1]/div/div/div/div/div/dl[1]/dd[1]/a'
    phone_category_url = 'http://116.62.63.211/shop/search/index/category_id/68.html'
    phone_brand_xpath = '/html/body/div[4]/div/div[2]/div/div/ul/li[2]/div[2]/ul/li[1]'
    phone_price_xpath = '/html/body/div[4]/div/div[2]/div/div/ul/li[3]/div[2]/ul/li[6]'
    phone_huawei_xpath = '/html/body/div[4]/div/ul/li/div'
    phone_goods_url = 'http://116.62.63.211/shop/goods/index/id/4.html'
    phone_QRcode_xpath = '/html/body/div[4]/div[2]/div[2]/div/div[2]/div/div[3]'
    phone_show_xpath = '/html/body/div[4]/div[2]/div[1]/div/div/img'
    phone_plan_xpath = '/html/body/div[4]/div[2]/div[1]/div/ul/li[2]/div/a/img'
    phone_add_xpath = '/html/body/div[4]/div[2]/div[2]/div/div[2]/dl/dd/div[2]/div[3]/form/div[1]/div[2]/dd/div/button[2]'
    phone_reduce_xpath = '/html/body/div[4]/div[2]/div[2]/div/div[2]/dl/dd/div[2]/div[3]/form/div[1]/div[2]/dd/div/button[1]'
    phone_quantity_input_xpath = '/html/body/div[4]/div[2]/div[2]/div/div[2]/dl/dd/div[2]/div[3]/form/div[1]/div[2]/dd/div/input'
    phone_collect_xpath = '/html/body/div[4]/div[2]/div[2]/div/div[3]/div[1]/span'
    phone_shopping_cart_xpath = '/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/button[2]'
    phone_bay_xpath = '/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/button[1]'
    phonr_payment_url = 'http://116.62.63.211/shop/buy/index.html'
    address_button1_xpath = '/html/body/div[4]/div/div[2]/div[2]/button'
    address_button2_xpath = '/html/body/div[4]/div/div[2]/div/button'
    address_iframe_xpath = '//div[contains(@class,"am-popup-bd")]//iframe[contains(@src,"saveinfo")]'
    name_else_NAME = "alias"
    name_else_text = "刘先生"
    name_xpath = './/input[@placeholder="姓名"]'
    name_text = "刘伟"
    phone_number_xpath = './/input[@placeholder="电话"]'
    phone_number_text = "19812341234"
    province_box_xpath = './/div[contains(@class,"region-linkage")]'
    province_box1_xpath = './div[1]/a'
    province_name1_xpath = './div[1]//ul/li[2]'
    province_name2_xpath = './/div[contains(@class,"region-linkage")]//div[1]//ul/li[2]'
    city_box1_xpath = './div[2]/a'
    city_name1_xpath = './div[2]//ul/li[2]'
    city_name2_xpath = './/div[contains(@class,"region-linkage")]//div[2]//ul/li[2]'
    county_box1_xpath = './div[3]/a'
    county_name1_xpath = './div[3]//ul/li[2]'
    county_name2_xpath = './/div[contains(@class,"region-linkage")]//div[3]//ul/li[2]'
    address_detail_xpath = './/input[@placeholder="详细地址"]'
    address_detail_text = "翻斗花园"
    default_state_xpath = './/input[@name="is_default"]/ancestor::div[contains(@class, "am-switch")][1]'
    address_seve1_button = './/div[contains(@class,"form-group-refreshing")]//button'
    address_seve2_button = './/button[normalize-space(.)="保存" or contains(normalize-space(.),"保存")]'
    buy_way_xpath = '/html/body/div[4]/div/div[4]/ul/li[1]/span'
    buyer_message_xpath = '/html/body/div[4]/div/div[5]/div/input'
    buyer_message_text = "无"
    order_submit_button = '/html/body/div[4]/div/div[6]/div/form/div/button'
    order_management_url = 'http://116.62.63.211/shop/order/index.html'

    with allure.step("移动鼠标去数码办公类"):
        # 8. 移动鼠标去数码办公类
        el = driver.find_element(By.XPATH, mouse_move_xpath)
        actions = ActionChains(driver)  # 动作作用在这个浏览器中
        actions.move_to_element(el)
        actions.perform()
        with allure.step("点击手机通讯类的'手机'链接"):
            # 9. 选择手机通讯类的手机
            el = driver.find_element(By.XPATH, phone_communication_xpath)
            el.click()

        with allure.step("断言进入手机筛选页面成功"):
            #  页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
            WebDriverWait(driver, 10).until(EC.url_to_be(phone_category_url))
            assert driver.current_url == phone_category_url

        with allure.step("勾选品牌"):
            # 10. 鼠标勾选品牌
            el = driver.find_element(By.XPATH, phone_brand_xpath)
            el.click()

        with allure.step("勾选价位"):
            # 11. 鼠标勾选价格
            el = driver.find_element(By.XPATH, phone_price_xpath)
            el.click()

        with allure.step("选择华为手机"):
            # 12. 选择华为手机
            el = driver.find_element(By.XPATH, phone_huawei_xpath)
            el.click()

    with allure.step("断言进入华为手机详情面成功"):
        #  页面跳转：跳转去目前最后一个窗口,在10秒内重复检查url是否为http://116.62.63.211/shop/goods/index/id/4.html，最多等十秒
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, 10).until(EC.url_to_be(phone_goods_url))
        assert driver.current_url == phone_goods_url

        with allure.step("查看二维码"):
            # 13. 只移动鼠标查看二维码
            el = driver.find_element(By.XPATH, phone_QRcode_xpath)
            actions = ActionChains(driver)  # 动作作用在这个浏览器中
            actions.move_to_element(el)
            actions.perform()

        with allure.step("查看手机放大图"):
            # 14. 只移动鼠标查看手机放大图
            el = driver.find_element(By.XPATH, phone_show_xpath)
            actions = ActionChains(driver)  # 动作作用在这个浏览器中
            actions.move_to_element(el)
            actions.move_by_offset(66, 66)
            actions.perform()

        with allure.step("查看手机平面图"):
            # 15. 移动鼠标查看手机平面图
            el = driver.find_element(By.XPATH, phone_plan_xpath)
            actions = ActionChains(driver)  # 动作作用在这个浏览器中
            actions.move_to_element(el)
            actions.perform()

        with allure.step("购买数量加一"):
            # 16. 添加数量
            el = driver.find_element(By.XPATH, phone_add_xpath)
            el.click()

        with allure.step("购买数量加一减一"):
            # 17. 减少数量
            el = driver.find_element(By.XPATH, phone_reduce_xpath)
            el.click()

        with allure.step("直接输入购买数量1"):
            # 18. 直接输入购买数量1，arguments[0].value = '1'；
            # 将input的值改成1；arguments[0].dispatchEvent(new Event('change', { bubbles: true }));将修改的信号往上传输
            el = driver.find_element(By.XPATH, phone_quantity_input_xpath)
            driver.execute_script(
                "arguments[0].value = '1'; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", el)

        with allure.step("收藏"):
            # 19. 点击收藏
            el = driver.find_element(By.XPATH, phone_collect_xpath)
            el.click()

        with allure.step("加入购物车"):
            # 19. 点击加入购物车
            el = driver.find_element(By.XPATH, phone_shopping_cart_xpath)
            el.click()

        with allure.step("购买"):
            # 19. 点击购买
            el = driver.find_element(By.XPATH, phone_bay_xpath)
            el.click()

    with allure.step("断言跳转去支付界面成功"):
        #  页面跳转：跳转去目前最后一个窗口,在10秒内重复检查url是否为http://116.62.63.211/shop/buy/index.html，最多等十秒
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, 10).until(EC.url_to_be(phonr_payment_url))
        assert driver.current_url == phonr_payment_url

        with allure.step("新增收货地址"):
            # 20. 点击新增收货地址
            try:
                el = driver.find_element(By.XPATH, address_button1_xpath)
                el.click()
            except Exception:
                el = driver.find_element(By.XPATH, address_button2_xpath)
                el.click()  # 联动需要点时间加载市级列表

        with allure.step("输入收货地址详细信息"):
            # 先等弹窗里的 iframe 出现（src 包含 saveinfo.html 就是新增地址表单）
            iframe_el = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, address_iframe_xpath)))
            time.sleep(0.5)  # 给 iframe 内部文档加载完成的时间
            driver.switch_to.frame(iframe_el)  # 切进 iframe 内部之后 driver 就在 iframe 小页面里工作了

            # 21. 输入别名  刘先生  (iframe 里明确有 name="alias" + placeholder="别名")
            el = driver.find_element(By.NAME, name_else_NAME)
            el.send_keys(name_else_text)

            # 22. 输入姓名  刘伟
            el = driver.find_element(By.XPATH, name_xpath)
            el.send_keys(name_text)

            # 23. 输入电话
            el = driver.find_element(By.XPATH, phone_number_xpath)
            el.send_keys(phone_number_text)

            # 24~29. 省市区县：省市区容器有特殊 class "am-form-group-region-linkage"，直接用这个 class 找最稳，因为他是下拉选择框
            # 这个am - form - group - region - linkage是AMUI 「区域联动组件」特有的class ， 整个页面里只有省市区这一排会带这个词 。
            region_box = driver.find_element(By.XPATH, province_box_xpath)

            # 24. 点击省份下拉（省市区容器下第 1 个 div 下的 a）
            province_a = region_box.find_element(By.XPATH, province_box1_xpath)
            province_a.click()

            # 25. 选择北京市（ul 下第 2 个 li，第 1 个是请选择）--------------------------两个选择最保险
            try:
                region_box.find_element(By.XPATH, province_name1_xpath).click()
            except Exception:
                driver.find_element(By.XPATH, province_name2_xpath).click()
            time.sleep(0.2)  # 联动需要点时间加载市级列表

            # 26. 点击城市下拉（第 2 个 div 下的 a）
            city_a = region_box.find_element(By.XPATH, city_box1_xpath)
            city_a.click()

            # 27. 选择东城区--------------------------两个选择最保险
            try:
                region_box.find_element(By.XPATH, city_name1_xpath).click()
            except Exception:
                driver.find_element(By.XPATH, city_name2_xpath).click()
            time.sleep(0.2)

            # 28. 点击区县下拉（第 3 个 div 下的 a）
            county_a = region_box.find_element(By.XPATH, county_box1_xpath)
            county_a.click()

            # 29. 输入区县名（区县下拉里带了搜索 input）--------------------------两个选择最保险
            try:
                region_box.find_element(By.XPATH, county_name1_xpath).click()
            except Exception:
                driver.find_element(By.XPATH, county_name2_xpath).click()
            time.sleep(0.2)

            # 30. 填写详细地址
            el = driver.find_element(By.XPATH, address_detail_xpath)
            el.send_keys(address_detail_text)

            # 31. 是否默认：name="is_default"，判断开关状态切换
            switch_wrapper = driver.find_element(By.XPATH, default_state_xpath)
            classes = switch_wrapper.get_attribute("class")
            if "am-switch-off" in classes:
                print("当前是否 → 切换成是")
                switch_wrapper.click()
            else:
                print("当前已经是是 → 不点击")
            time.sleep(0.2)

            # 32. 保存地址（找表单底部含"保存"的 button，或者在 am-form-group-refreshing 组里找 button），--------------------------两个选择最保险
            try:
                save_btn = driver.find_element(By.XPATH, address_seve1_button)
            except Exception:
                save_btn = driver.find_element(By.XPATH, address_seve2_button)
            save_btn.click()
            time.sleep(0.5)
            driver.refresh()

            driver.switch_to.default_content()  # 退出所有 iframe 回到主页面
            time.sleep(1)
            driver.refresh()

        with allure.step("货到付款"):
            # 33. 选择支付方式，增添地址后页面发生变化
            el = driver.find_element(By.XPATH, buy_way_xpath)
            el.click()

        with allure.step("留言无"):
            # 34. 买家留言无
            el = driver.find_element(By.XPATH, buyer_message_xpath)
            el.send_keys(buyer_message_text)

        with allure.step("提交订单"):
            # 35. 提交订单
            el = driver.find_element(By.XPATH, order_submit_button)
            el.click()



    with allure.step("断言进入订单管理成功"):
        # 36. 跳转订单管理页面，由于为测试阶段暂不购买
        WebDriverWait(driver, 10).until(EC.url_to_be(order_management_url))
        assert driver.current_url == order_management_url


@allure.epic("用户中心")
@allure.feature("购物车下单功能")
@allure.story("购物车下单成功")
@allure.title("测试用户使用购物车下单")
def test_cart_bay(driver,screenshot_on_end):
    #购物车结算
    shop_cart_xpath = '/html/body/div[1]/div/ul[2]/div[5]/div/a'
    cart_order_url = 'http://116.62.63.211/shop/cart/index.html'
    cart_all_xpath = '/html/body/div[5]/div/div[1]/label/span[1]'
    cart_buy_button = '/html/body/div[5]/div/div[2]/form/button'
    buy_index_url = 'http://116.62.63.211/shop/buy/index.html'
    buy_way_xpath = '/html/body/div[4]/div/div[4]/ul/li[1]/span'
    buy_message_input = '/html/body/div[4]/div/div[5]/div/input'
    buy_message_yesy = "无"
    buy_success_button = '/html/body/div[4]/div/div[6]/div/form/div/button'
    buy_success_url = 'http://116.62.63.211/shop/order/index.html'

    with allure.step("点击购物车"):
        # 2.    找到并点击购物车
        el = driver.find_element(By.XPATH, shop_cart_xpath)
        el.click()

        with allure.step("断言成功进入购物车页面成功"):
            # 36. 跳转购物车管理页面，由于为测试阶段暂不购买
            WebDriverWait(driver, 10).until(EC.url_to_be(cart_order_url))
            assert driver.current_url == cart_order_url

        with allure.step("全选购物车商品"):
            # 2.    找到并点击”全选“按钮
            el = driver.find_element(By.XPATH, cart_all_xpath)
            el.click()

        with allure.step("点击结算"):
            # 2.    找到并点击结算
            el = driver.find_element(By.XPATH, cart_buy_button)
            el.click()

        with allure.step("断言进入结算页面成功"):
            # 36. 跳转订单结算页面，由于为测试阶段暂不购买
            WebDriverWait(driver, 10).until(EC.url_to_be(buy_index_url))
            assert driver.current_url == buy_index_url

        with allure.step("选择支付方式"):
            # 33. 选择支付方式，增添地址后页面发生变化
            el = driver.find_element(By.XPATH, buy_way_xpath)
            el.click()

        with allure.step("买家留言无"):
            # 34. 买家留言无
            el = driver.find_element(By.XPATH, buy_message_input)
            el.send_keys(buy_message_yesy)

        with allure.step("点击提交订单"):
            # 35. 提交订单
            el = driver.find_element(By.XPATH, buy_success_button)
            el.click()

        with allure.step("断言下单成功"):
            # 36. 跳转订单管理页面，由于为测试阶段暂不购买
            WebDriverWait(driver, 10).until(EC.url_to_be(buy_success_url))
            assert driver.current_url == buy_success_url


@allure.epic("用户中心")
@allure.feature("个人信息查看与修改个人信息功能")
@allure.story("个人信息查看与修改个人信息成功")
@allure.title("测试用户个人信息查看与修改个人信息成功")
def test_order_management(driver,screenshot_on_end):

    order_add_success_xpath = '//*[text()="Huawei/华为 H60-L01 荣耀6 移动4G版智能手机 安卓"]'
    collect_success_link_xpath = '/html/body/div[4]/div[1]/div/ul/li[2]/ul/li[3]/a'
    collect_success_link_url = 'http://116.62.63.211/shop/usergoodsfavor/index.html'
    collect_add_success_xpath = '//*[text()="Huawei/华为 H60-L01 荣耀6 移动4G版智能手机 安卓"]'
    personal_information_link_xpath = '/html/body/div[4]/div[1]/div/ul/li[4]/ul/li[1]/a'
    personal_information_link_success_xpath = 'http://116.62.63.211/shop/personal/index.html'
    personal_information_compile_xpath = '/html/body/div[4]/div[3]/div/legend/a'
    personal_information_compile_url = 'http://116.62.63.211/shop/personal/saveinfo.html'
    personal_information_name_input = '/html/body/div[4]/div[3]/div/form/div[1]/input'
    personal_information_name_text = "小白"
    personal_information_gender_xpath = '/html/body/div[4]/div[3]/div/form/div[2]/div/label[3]'
    personal_information_birthday_xpath = '/html/body/div[4]/div[3]/div/form/div[3]/input'
    personal_information_birthday_text = "2004-08-01"
    personal_information_save_button = '/html/body/div[4]/div[3]/div/form/div[4]/button'
    personal_information_save_url = 'http://116.62.63.211/shop/personal/index.html'
    personal_foot_xpath = '/html/body/div[4]/div[1]/div/ul/li[4]/ul/li[5]/a'
    personal_foot_url = 'http://116.62.63.211/shop/usergoodsbrowse/index.html'
    personal_foot_success_xpath = '//*[text()="Huawei/华为 H60-L01 荣耀6 移动4G版智能手机 安卓"]'


    with allure.step("断言订单购买记录成功"):
        # 查看是否添加成功，手动购买和购物车购买
        el_list = driver.find_elements(By.XPATH, order_add_success_xpath)
        assert len(el_list) == 2

    with allure.step("点击收藏管理"):
        # 35. 点击收藏管理
        el = driver.find_element(By.XPATH, collect_success_link_xpath)
        el.click()

        with allure.step("断言跳转收藏管理页面成功"):
            # 等待跳转成功
            WebDriverWait(driver, 10).until(EC.url_to_be(collect_success_link_url))
            assert driver.current_url == collect_success_link_url

        with allure.step("断言收藏数量正常"):
            # 查看是否收藏成功
            el_list = driver.find_elements(By.XPATH, collect_add_success_xpath)
            assert len(el_list) == 1

    with allure.step("点击个人足迹"):
        # 点击个人足迹
        el = driver.find_element(By.XPATH, personal_foot_xpath)
        el.click()

        with allure.step("断言跳转个人足迹页面成功"):
            # 等待跳转成功
            WebDriverWait(driver, 10).until(EC.url_to_be(personal_foot_url))
            assert driver.current_url == personal_foot_url

        with allure.step("断言足迹是否保存正常"):
            # 查看足迹是否保存成功
            el_list = driver.find_elements(By.XPATH, personal_foot_success_xpath)
            assert len(el_list) == 1

    with allure.step("点击个人信息"):
        # 点击个人信息
        el = driver.find_element(By.XPATH, personal_information_link_xpath)
        el.click()

        with allure.step("断言跳转个人信息页面成功"):
            # 等待跳转成功
            WebDriverWait(driver, 10).until(EC.url_to_be(personal_information_link_success_xpath))
            assert driver.current_url == personal_information_link_success_xpath

        with allure.step("点击个人信息编辑"):
            # 点击个人信息编辑
            el = driver.find_element(By.XPATH, personal_information_compile_xpath)
            el.click()

        with allure.step("断言跳转个人信息编辑页面成功"):
            # 等待跳转成功http://116.62.63.211/shop/personal/index.html
            WebDriverWait(driver, 10).until(EC.url_to_be(personal_information_compile_url))
            assert driver.current_url == personal_information_compile_url

        with allure.step("输入昵称"):
            # 输入昵称  ‘小白’
            el = driver.find_element(By.XPATH, personal_information_name_input)
            el.send_keys(personal_information_name_text)

        with allure.step("点击男性"):
            # 点击男性
            el = driver.find_element(By.XPATH, personal_information_gender_xpath)
            el.click()

        with allure.step("直接input输入生日"):
            # 直接input输入生日
            el = driver.find_element(By.XPATH, personal_information_birthday_xpath)
            el.click()
            el.send_keys(personal_information_birthday_text)

        with allure.step("点击保存"):
            # 点击保存
            el = driver.find_element(By.XPATH, personal_information_save_button)
            el.click()

        with allure.step("断言返回个人中心成功，个人信息保存成功"):
            # 跳转回去http:
            WebDriverWait(driver, 10).until(EC.url_to_be(personal_information_save_url))
            assert driver.current_url == personal_information_save_url


@allure.epic("用户中心")
@allure.feature("用户密码修改保存并测试功能")
@allure.story("用户密码修改保存并测试成功")
@allure.title("测试用户密码修改保存并测试成功")
def test_user_password(driver,screenshot_on_end):

    save_index_xpath = '/html/body/div[4]/div[1]/div/ul/li[4]/ul/li[3]/a'
    save_mchange_xpath = '/html/body/div[4]/div[3]/div/section[1]/div/a'
    save_mchange_url = 'http://116.62.63.211/shop/safety/loginpwdinfo.html'
    password_former_input = '/html/body/div[4]/div[3]/div/form/div[1]/input'
    password_new_input = '/html/body/div[4]/div[3]/div/form/div[2]/input'
    password_new_text = "lwj123456"
    password_again_input = '/html/body/div[4]/div[3]/div/form/div[3]/input'
    password_save_button = '/html/body/div[4]/div[3]/div/form/div[4]/button'
    personal_page_url = 'http://116.62.63.211/shop/safety/index.html'
    quit_save_xpath = '/html/body/div[4]/div[1]/div/ul/li[5]/a'
    login_link_xpath = '/html/body/div[2]/div/ul[1]/div/div/a[1]'
    user_username_input_xpath = '/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[1]/input'
    user_password_input_xpath = '/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[2]/div/input'
    login_button_xpath = '/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/form/div[3]/button'
    login_success_xpath = '/html/body/div[10]/div/p'
    login_success_text = "登录成功"
    url = 'http://116.62.63.211/shop/'

    with allure.step("点击进入安全设置页面"):
        # 点击进入安全设置页面
        el = driver.find_element(By.XPATH, save_index_xpath)
        el.click()

        with allure.step("点击修改"):
            # 点击修改
            el = driver.find_element(By.XPATH, save_mchange_xpath)
            el.click()

        with allure.step("断言跳转进去修改页面成功"):
            # 跳转进去修改页面
            WebDriverWait(driver, 10).until(EC.url_to_be(save_mchange_url))
            assert driver.current_url == save_mchange_url

        user = get_test_user()
        password = user["password"]
        print(f"[user_management] 修改密码成功/ 新密码：lwj123456")

        with allure.step("输入当前密码"):
            # 输入当前密码
            el = driver.find_element(By.XPATH, password_former_input)
            el.send_keys(password)

        with allure.step("输入新密码"):
            # 输入新密码
            el = driver.find_element(By.XPATH, password_new_input)
            el.send_keys(password_new_text)

        with allure.step("再输入新密码"):
            # 再输入新密码
            el = driver.find_element(By.XPATH, password_again_input)
            el.send_keys(password_new_text)

        with allure.step("点击保存"):
            # 点击保存
            el = driver.find_element(By.XPATH, password_save_button)
            el.click()

        with allure.step("断言跳转回管理页面成功"):
            # 跳转回管理页面
            WebDriverWait(driver, 10).until(EC.url_to_be(personal_page_url))
            assert driver.current_url == personal_page_url

    with allure.step("安全退出，并用新密码登录"):
        # 安全退出
        el = driver.find_element(By.XPATH, quit_save_xpath)
        el.click()

        with allure.step("断言回到未登录首页成功"):
            # 回到首页
            WebDriverWait(driver, 10).until(EC.url_to_be(url))
            assert driver.current_url == url

        user = get_test_user()
        username = user["username"]
        print(f"[test_login_ok] 本次使用账号：{username} / 新密码：lwj123456")

        with allure.step("找到并点击登录按钮"):
            # 2.    找到并点击”登录“按钮
            el = driver.find_element(By.XPATH, login_link_xpath)
            el.click()

        with allure.step("输入正确用户名"):
            # 4.    找到用户名输入框input，输入正确用户名
            el = driver.find_element(By.XPATH, user_username_input_xpath)
            el.send_keys(username)

        with allure.step("输入新密码"):
            # 5.    找到密码输入框，输入新密码
            el = driver.find_element(By.XPATH, user_password_input_xpath)
            el.send_keys("lwj123456")

        with allure.step("点击登录按钮"):
            # 6.    找到登录按钮button，点击按钮
            el = driver.find_element(By.XPATH, login_button_xpath)
            el.click()

        with allure.step("断言登录成功"):
            # 预期结果：
            # ● 系统提示：登录成功
            el = driver.find_element(By.XPATH, login_success_xpath)
            assert el.text == login_success_text

        with allure.step("断言跳转商城首页成功"):
            # ● 页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
            WebDriverWait(driver, 10).until(EC.url_to_be(url))
            assert driver.current_url == url




































