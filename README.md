# Tushare Skill

[Tushare Pro](https://tushare.pro) 金融数据获取 Skill，支持 220+ 个金融数据接口。

## 特性

- 🎯 **全面的数据覆盖** - 支持 220+ 个 Tushare API 接口
- 💬 **自然语言交互** - 直接用中文描述需求即可获取数据
- 📊 **丰富的数据类型** - 股票、财务、指数、宏观经济等
- 🚀 **开箱即用** - Claude Code Skill 即插即用
- 📚 **完整的接口文档** - 包含 220+ 个接口的详细文档
- ✨ **符合官方标准** - 遵循 Claude Code Skills 最佳实践

## 安装

### 1. 安装依赖
* 安装nodejs（如果需要skills管理本地包-npx命令）， https://nodejs.cn/download/
* 安装tushare， https://tushare.pro/document/1?doc_id=7


### 2. 配置 Token

到 [Tushare 官网](https://tushare.pro) 注册账号并获取 API token：

```bash
export TUSHARE_TOKEN="your_token_here"
```

### 3. 安装 Skill
可以通过下面几种个方法（任何一种都可以）：
* 将 tushare 目录复制到本地的 skills 目录：
* 通过skills，安装github上的源码包
```bash
npx skills add  https://github.com/waditu-tushare/skills.git --skill tushare
```

## 使用方法

安装后，在 Claude Code 中直接对话：

**获取股票数据**：
```
获取平安银行最近 30 天的股价数据
```

**财务分析**：
```
查看招商银行最近的财务报表，分析营收和净利润
```

**股票筛选**：
```
帮我查找所有银行股并分析最近表现
```

**指数数据**：
```
获取上证指数最近的行情数据
```

**宏观数据**：
```
查询最近一年的 GDP 和 CPI 数据
```

### 自动触发
Skill 会在以下情况自动激活：
- 用户请求股价、财务数据
- 查询指数、基金、期货、债券
- 获取宏观经济指标（GDP、CPI、利率等）

### 工具权限
- `Bash(python:*)`: 允许执行 Python 代码
- `Read`: 允许读取接口文档

## API 限制说明
[Tushare 官方文档](https://tushare.pro/document/1?doc_id=290)


**注意**: 本项目仅供学习和研究使用，请勿用于商业用途。使用时请遵守 Tushare 的使用条款。