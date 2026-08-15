# 贡献指南

感谢你对论坛 V5 项目的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告 Bug
1. 检查是否已经存在相同的问题
2. 使用 Bug Report 模板
3. 提供详细的复现步骤

### 提交代码
1. Fork 本仓库
2. 创建你的功能分支
3. 提交你的更改
4. 推送到分支
5. 创建 Pull Request

## 代码规范

### Python
- 遵循 PEP 8
- 使用 Black 格式化
- 使用 Flake8 检查

### Commit 规范
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

## 测试

```bash
pytest tests/ -v --cov=.
