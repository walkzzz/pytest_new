from typing import List

import allure
from allure_commons.types import AttachmentType


class AllureHelper:
    """Allure报告辅助工具"""

    @staticmethod
    def add_attachment(name: str, content: str, attachment_type: AttachmentType = AttachmentType.TEXT):
        """添加附件"""
        allure.attach(content, name, attachment_type)

    @staticmethod
    def add_link(url: str, name: str = None, link_type: str = None):
        """添加链接"""
        if link_type == 'issue':
            allure.issue(url=url, name=name)
        elif link_type == 'tms':
            allure.tms(url=url, name=name)
        else:
            allure.link(url=url, name=name)

    @staticmethod
    def add_label(label_type: str, value: str):
        """添加标签"""
        allure.label(label_type, value)

    @staticmethod
    def add_severity(severity: str):
        """添加严重级别"""
        severity_map = {
            'blocker': allure.severity_level.BLOCKER,
            'critical': allure.severity_level.CRITICAL,
            'normal': allure.severity_level.NORMAL,
            'minor': allure.severity_level.MINOR,
            'trivial': allure.severity_level.TRIVIAL,
        }
        level = severity_map.get(severity.lower(), allure.severity_level.NORMAL)
        allure.severity(level)

    @staticmethod
    def add_test_case_info(
        title: str = None,
        description: str = None,
        severity: str = None,
        epic: str = None,
        feature: str = None,
        story: str = None,
        suite: str = None,
        layer: str = None,
        tags: List[str] = None,
    ):
        """添加测试用例信息"""
        if title:
            allure.title(title)
        if description:
            allure.description(description)
        if severity:
            AllureHelper.add_severity(severity)
        if epic:
            allure.epic(epic)
        if feature:
            allure.feature(feature)
        if story:
            allure.story(story)
        if suite:
            allure.suite(suite)
        if layer:
            allure.tag(layer)
        if tags:
            for tag in tags:
                allure.tag(tag)
