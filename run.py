import pytest
import os

RUN_ONLY_THIS_TEST_FILE = "tests/test_user_function_package.py"
pytest.main(["-s", "-v", "--alluredir", "./temps", RUN_ONLY_THIS_TEST_FILE])

os.system("allure generate ./temps -o ./reports --clean")#将./temps的内容转成可视化报告
