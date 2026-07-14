import pytest
from selenium import webdriver


@pytest.fixture(scope='session')
def driver():
    #让所有test遵循此函数的前后置
    d = webdriver.Chrome()
    d.maximize_window()
    d.implicitly_wait(2)  # 短的隐式等待

    yield d

    d.implicitly_wait(2)
