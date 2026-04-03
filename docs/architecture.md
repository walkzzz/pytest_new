# 项目架构

## 目录结构

```
pytest_new_opt/
├── src/                    # 核心源码
│   ├── core/               # 核心基类
│   │   ├── base_page.py    # 页面基类（POM）
│   │   └── base_test.py    # 测试基类
│   ├── pywinauto/          # pywinauto 封装
│   ├── pytest_runner/      # 测试运行器
│   ├── config/             # 配置管理
│   ├── utils/              # 工具类
│   └── exceptions.py       # 自定义异常
├── tests/                  # 测试用例
│   ├── locators/           # 元素定位器
│   └── configs/            # 环境配置
├── data/                   # 测试数据
├── docs/                   # 文档
├── scripts/                # 辅助脚本
└── logs/                   # 日志目录
```

## 模块说明

### src/core

核心基类模块，提供页面对象模型（POM）和测试基类。

### src/pywinauto

pywinauto 驱动封装，包含控件、操作执行器、断言等。

### src/pytest_runner

测试运行器，负责解析配置、执行测试步骤、生成报告。

### src/config

配置管理，包含 YAML 解析、环境配置加载。

### src/utils

通用工具，包含等待、重试、日志、配置等工具。

## 设计模式

### POM (Page Object Model)

页面对象模型，将每个页面封装为独立类，元素定位器与业务逻辑分离。

### 数据驱动

测试数据与配置分离，支持多环境切换。

### 关键字驱动

通过 YAML 配置定义测试步骤，实现测试用例与代码解耦。
