.PHONY: help install run test clean

help:
	@echo "可用命令:"
	@echo "  install   安装依赖"
	@echo "  run       运行应用"
	@echo "  test      运行测试"
	@echo "  clean     清理缓存"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run:
	python run.py

test:
	pytest tests/ -v --cov=.

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
