from typing import Optional


class BaseTest:
    config_filename: str = None
    project_name: str = "自动化测试"
    build_name: Optional[str] = None
    testplan_url: Optional[str] = None

    @classmethod
    def setup_class(cls):
        if cls.config_filename is None:
            raise ValueError("必须设置 config_filename 属性")

    @classmethod
    def teardown_class(cls):
        pass
