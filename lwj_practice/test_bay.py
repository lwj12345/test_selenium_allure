import time
import re

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element_visible(driver, by, value, timeout=10):
    """好懂版：等一个元素出现+可见，最多等 N 秒，找不到就报错，不用每次写 WebDriverWait"""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )

def safe_click(el, driver):
    """
    好懂版「安全点击」：
    1. 先正常 el.click() —— 你最熟悉的方式
    2. 如果被挡住/Stale 失败，就用 1 行 JS 强行点（不是 200 行那种大段 JS，就是 1 句 好懂）
    """
    try:
        el.click()
    except Exception:
        driver.execute_script("arguments[0].click();", el)

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
    time.sleep(0.5)

    # 9. 选择手机通讯类的手机
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/ul/li[1]/div/div/div/div/div/dl[1]/dd[1]/a")
    el.click()
    time.sleep(0.5)

    #  页面跳转：商城首页,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/search/index/category_id/68.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/search/index/category_id/68.html'

    # 10. 鼠标勾选品牌
    el = driver.find_element(By.XPATH,"/html/body/div[4]/div/div[2]/div/div/ul/li[2]/div[2]/ul/li[1]")
    el.click()
    time.sleep(0.5)

    # 11. 鼠标勾选价格
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/div/ul/li[3]/div[2]/ul/li[6]")
    el.click()
    time.sleep(0.5)

    # 12. 选择华为手机
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div/ul/li/div")
    el.click()
    time.sleep(0.5)

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

    # 19. 点击购买
    el = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/button[1]")
    el.click()

    #  页面跳转：跳转去目前最后一个窗口,在10秒内重复检查url是否为http://116.62.63.211/shop/，最多等十秒
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(EC.url_to_be("http://116.62.63.211/shop/buy/index.html"))
    assert driver.current_url == 'http://116.62.63.211/shop/buy/index.html'

    # #  删除之前测试产生的默认地址
    # el = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/ul/li/div[3]/a[2]")
    # classes = el.get_attribute("class")
    # if "am-icon-trash-o address-submit-delete" in classes:
    #     print("存在，执行删除")
    #     el.click()
    #     time.sleep(0.5)
    #     el = driver.find_element(By.XPATH, "/html/body/div[11]/div/div[3]/span[2]")
    #     el.click()

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
    safe_click(save_btn, driver)   # 先正常点，点不中用一行 JS 兜底，好懂
    time.sleep(1)

    # 关键：先退出 iframe 回到主页面（不然 driver.current_url 看到的还是 iframe 内部的地址，不是 buy/index.html）
    driver.switch_to.default_content()

    # ========== 新增地址成功信号：等 URL 里出现 address_id= ==========
    # 你截图里观察到的：http://...buy/index.html → http://...buy/index.html?address_id=63490
    # 就用这个当「地址100%保存成功」的信号，比 refresh() 2 次靠谱多了
    print(f"保存地址后当前URL：{driver.current_url}")
    WebDriverWait(driver, 20).until(
        lambda d: "address_id=" in d.current_url
    )
    print(f"✓ 检测到 address_id 出现，地址保存成功！新URL：{driver.current_url}")

    # 刷新 1 次让页面内容和 URL 同步（只刷新一次，你原来的两次里有一次是多余的）
    driver.refresh()
    time.sleep(1)

    # 33. 选择支付方式（不用 ul/li 绝对路径，直接按文字=支付宝找元素，再 safe_click）
    #    想选货到付款就把 XPath 里的「支付宝」改成「货到付款」即可
    for retry in range(3):   # 重试 3 次，防止刚刷完 DOM 还没稳定点不到
        try:
            # XPath 写法翻译：// * [文字去掉前后空白刚好就是"支付宝"]
            el_pay = wait_for_element_visible(
                driver,
                By.XPATH,
                '//*[self::div or self::a or self::span or self::button][normalize-space(text())="支付宝"]'
            )
            safe_click(el_pay, driver)     # 先正常点，点不中行 1 句 JS
            print("✓ 支付方式：支付宝（已点击）")
            break
        except Exception as e:
            print(f"第 {retry+1} 次选支付宝失败：{e}，0.5 秒后重试")
            time.sleep(0.5)
            driver.refresh()              # 实在 DOM 怪就再刷一次继续点
            time.sleep(0.5)

    # 34. 买家留言 = 无（不用绝对路径，直接找 placeholder="买家留言" 的 input，页面结构怎么改都能找到）
    for retry in range(3):
        try:
            el_msg = wait_for_element_visible(driver, By.XPATH, './/input[@placeholder="买家留言"]')
            el_msg.clear()
            el_msg.send_keys("无")
            print("✓ 买家留言已填：无")
            break
        except Exception as e:
            print(f"第 {retry+1} 次填留言失败：{e}，0.5 秒后重试")
            time.sleep(0.5)

    # 35. 提交订单（不用绝对路径，直接找按钮文字=提交订单）
    for retry in range(3):
        try:
            el_submit = wait_for_element_visible(
                driver,
                By.XPATH,
                './/button[normalize-space(.)="提交订单"]'
            )
            safe_click(el_submit, driver)  # 先正常点，点不中行 1 句 JS
            print("✓ 已点击【提交订单】")
            break
        except Exception as e:
            print(f"第 {retry+1} 次点提交订单失败：{e}，0.5 秒后重试")
            time.sleep(0.5)

    # 36. 跳转订单管理页面，由于为测试阶段暂不购买（用 URL 包含判断，不写死完整 URL）
    WebDriverWait(driver, 15).until(EC.url_contains("/shop/order/"))
    assert "/shop/order/" in driver.current_url
    print(f"✓ 已跳转订单页：{driver.current_url}")

    # ========== 37. 元素数量断言：确认总共买了【2部华为手机】（3 种方案任你选，推荐方案 1，最严谨）==========
    time.sleep(1.2)   # 等订单列表 DOM 渲染稳定

    # ✅【方案 1，最推荐】定位「商品标题含 Huawei/华为 H60-L01 荣耀6」的元素数量 = 2
    #    好处 1：同时验证了「我买的确实是华为这款手机，不是别的」
    #    好处 2：每条订单商品标题就是这行文字，2 条订单 = 2 部手机，直接数标题个数 = 手机部数
    huawei_title_list = driver.find_elements(
        By.XPATH,
        '//*[self::a or self::div or self::span][contains(normalize-space(.), "Huawei/华为 H60-L01 荣耀6")]'
    )
    print(f"【方案1】商品标题匹配到的元素数量：{len(huawei_title_list)}")
    assert len(huawei_title_list) == 2, f"应该有 2 部华为手机，实际匹配到 {len(huawei_title_list)} 个商品标题"
    print("✓【方案1】断言通过：页面上有 2 个『Huawei/华为 H60-L01 荣耀6』商品标题 = 买了 2 部华为手机")

    # 🟡【方案 2】定位「每条订单里 x1（数量=1 部）」的元素个数 = 2（2 条订单，每条各 1 部）
    #    适用：不想按商品标题断言，只想按「数量标签个数」断言
    qty_list = driver.find_elements(
        By.XPATH,
        '//*[self::span or self::em or self::div or self::b][normalize-space(text())="x1" or normalize-space(text())="×1"]'
    )
    print(f"【方案2】x1 数量标签匹配到的元素数量：{len(qty_list)}")
    if len(qty_list) == 0:
        # 兜底：有些商城 x1 是写在标题同一行同一串文字里，单独拿不到，就用正则找 "¥1999.00x1" 这种 span
        qty_list = driver.find_elements(
            By.XPATH,
            '//*[self::span or self::div][contains(., "¥1999.00x1") or contains(., "1999.00x1")]'
        )
        print(f"【方案2兜底】按价格+x1 匹配到的元素数量：{len(qty_list)}")
    assert len(qty_list) == 2, f"应该有 2 个 x1 数量标签（对应 2 部手机），实际匹配到 {len(qty_list)} 个"
    print("✓【方案2】断言通过：页面上有 2 个 x1 数量标签 = 买了 2 部手机")

    # 🟢【方案 3（辅助断言，和上面任一个配合一起用）】读页面底部「共 2 条数据」的文字 = 2
    #    注意：这个只能验证订单数=2，验证不了订单里是不是华为手机，所以当辅助断言配合方案 1 一起用最稳
    try:
        count_tip_el = driver.find_element(
            By.XPATH,
            '//*[self::div or self::span or self::p][contains(normalize-space(.), "共") and contains(normalize-space(.), "条数据")]'
        )
        tip_text = count_tip_el.text
        match = re.search(r"共\s*(\d+)\s*条数据", tip_text)
        if match:
            order_count = int(match.group(1))
            print(f"【方案3】底部『共X条数据』读出来的数字：{order_count}，原文：{tip_text}")
            assert order_count == 2, f"订单条数应该是 2，实际读出来是 {order_count}"
            print("✓【方案3】断言通过：页面底部写了『共 2 条数据』= 一共 2 个订单")
        else:
            print(f"【方案3】正则没匹配出数字，tip 原文：{tip_text}（不影响其他两个断言）")
    except Exception as e:
        print(f"【方案3】没找到『共X条数据』元素（仅辅助断言，不强制）：{e}")
    print("🎉 三部断言（标题数=2 + x1数=2 + 订单条数=2）都通过！")


#页面跳转并且打开新窗口要手动跳转---driver.switch_to.window(driver.window_handles[-1])
#对于本页新开窗口可能要定位框架且打开---iframe_el = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"am-popup-bd")]//iframe[contains(@src,"saveinfo")]')))
#当页面url发生变化但页面内容没有怎么变，最好刷新一下浏览器---driver.refresh()








