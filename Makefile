.PHONY: help lint test typecheck coverage clean install install-dev test-unit test-mock test-all testmon format pre-commit ci quality report

help:
	@echo "可用命令:"
	@echo "  make install       - 安装生产依赖"
	@echo "  make install-dev   - 安装开发依赖"
	@echo "  make test          - 运行所有测试"
	@echo "  make test-unit     - 运行单元测试"
	@echo "  make test-mock     - 运行 Mock 测试"
	@echo "  make test-all      - 运行全部测试（含覆盖率）"
	@echo "  make lint          - 运行代码检查"
	@echo "  make format        - 格式化代码"
	@echo "  make typecheck     - 运行类型检查"
	@echo "  make clean         - 清理临时文件"
	@echo "  make pre-commit    - 运行 pre-commit 检查"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/ -v --tb=short

test-unit:
	python -m pytest tests/unit/ -v --tb=short

test-mock:
	python -m pytest tests/mock/ -v --tb=short

test-all:
	python -m pytest tests/ -v --tb=short --cov=src --cov-report=html --cov-report=term-missing --cov-report=xml

testmon:
	python -m pytest tests/ --testmon -v

test-parallel:
	python -m pytest tests/ -n auto --dist loadgroup

lint:
	flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics || true
	ruff check src/ tests/ || true

format:
	black src/ tests/ scripts/ --config pyproject.toml
	isort src/ tests/ scripts/ --profile black
	ruff check src/ tests/ --fix

typecheck:
	mypy src/ --config-file pyproject.toml --ignore-missing-imports

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf .pytest_cache/ .coverage htmlcov/ coverage.xml 2>/dev/null || true
	rm -rf reports/ allure-results/ allure-report/ 2>/dev/null || true
	rm -rf .ruff_cache/ .mypy_cache/ 2>/dev/null || true

pre-commit:
	pre-commit run --all-files

quality: lint format typecheck
	@echo "代码质量检查完成!"

ci: lint test-all
	@echo "CI 检查完成!"

report:
	python -m pytest tests/ -v --html=reports/report.html --self-contained-html