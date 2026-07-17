# qx-mcp — 启信宝企业数据 MCP 服务器

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-1.0%2B-orange)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**qx-mcp** 是一个基于 [MCP (Model Context Protocol)](https://modelcontextprotocol.io) 标准的服务器，将[启信宝开放平台](https://data.qixin.com)（上海生腾数据科技有限公司）170+ 企业工商/司法/知识产权/证券数据 API 封装为 MCP 工具，可供 AI 助手直接调用查询企业信息。

## ✨ 功能特性

- **173 个 MCP 工具**，覆盖企业工商、司法、经营、知识产权、证券等全维度
- **即装即用** — 安装后配置 appkey 即可通过 AI 助手自然语言查询
- **统一鉴权** — 自动处理 `appkey + timestamp + secret` 签名
- **全量覆盖** — 基础信息、股权穿透、关联关系、风险评分、特殊机构等

## 📋 覆盖数据范围

| 类别 | 工具数 | 说明 |
|:----|:------:|------|
| 基础工商信息 | 10 | 照面、简介、LOGO、三码、历史名称、资本背景、规模、行业分类、主体性质 |
| 股东/股权/投资 | 6 | 工商股东、对外投资、最优股比、参股控股、实际控制企业 |
| 关联关系 | 10 | 疑似关联方、关联企业、关联方认定、企业链图、企业间找关系(2家/10家/50家) |
| 股权穿透/族谱/受益人 | 9 | 三/六层族谱、十层股东穿透、十大受益人、实际控制人/受益人 |
| 人员信息 | 2 | 主要人员、董监高对外投资任职 |
| 变更/年报/社保 | 5 | 变更记录、工商年报、社保信息、股权变更、企业迁移 |
| 分支机构 | 2 | 分支机构查询、总公司核查 |
| 联系方式/年报网址 | 2 | 联系方式、年报网址 |
| 实时查询 | 2 | 实时工商信息(异步)、JOB 状态 |
| 验证类 | 4 | 企业二/三/四要素验证 |
| 公告 | 1 | 减资公告 |
| 风险/评分 | 3 | 启信分、工商风险扫描、关联信息汇总 |
| 特殊机构 | 6 | 律所、社会组织、香港企业、事业单位、医院、基金会 |
| 小微企业 | 3 | 小微企业信息、JOB 申请、详情数据 |
| 地理/周边 | 7 | 附近企业、周边统计、坐标、同电话、规上企业、新增企业 |
| 综合报告 | 1 | 企业基础工商信息报告 |

## 🚀 快速开始

### 前置条件

- Python 3.11+
- 启信宝开放平台 API 密钥（[申请地址](https://data.qixin.com)）

### 安装

```bash
# 通过 pip 安装
pip install qx-mcp

# 或从源码安装
git clone https://github.com/your-username/qx-mcp.git
cd qx-mcp
pip install -e .
```

### 配置

qx-mcp 从环境变量读取密钥，或直接编辑源码中的 `APPKEY` / `SECRET_KEY`：

```bash
export APPKEY="your-appkey"
export SECRET_KEY="your-secret-key"
```

### 启动

```bash
# STDIO 模式（默认，用于 Claude Desktop 等 MCP 客户端）
qx-mcp

# MCP 配置示例（用于 claude_desktop_config.json 或 .claude/mcp.json）
```

添加到 `.claude/mcp.json`：

```json
{
  "mcpServers": {
    "qx-mcp": {
      "command": "qx-mcp",
      "args": [],
      "env": {
        "APPKEY": "your-appkey",
        "SECRET_KEY": "your-secret-key"
      }
    }
  }
}
```

## 🔧 API 调用示例

所有接口接受企业全名 / 注册号 / 统一社会信用代码作为查询参数。

```python
# 查询工商照面
get_business_license(keyword="小米科技有限责任公司")

# 查询股东信息
get_shareholders(keyword="广州银行股份有限公司")

# 查询三层股权穿透
get_three_layer_shareholders(name="广州银行股份有限公司")

# 查询关联企业
get_related_enterprises(name="格力电器")

# 实际控制人
get_actual_controller(name="广州银行股份有限公司")
```

## 📂 项目结构

```
qx-mcp/
├── LICENSE
├── README.md
├── pyproject.toml
└── qx_mcp/
    └── __init__.py          # 所有工具定义及 MCP 服务器
```

## 🔒 数据来源

所有数据来源于 **启信宝开放平台**（[data.qixin.com](https://data.qixin.com)），由上海生腾数据科技有限公司提供。使用前需要在启信开放平台注册并获取 API 密钥。

## 📄 License

[MIT](LICENSE)

## ⚠️ 免责声明

本工具仅作为 API 的 MCP 封装层，不对数据的准确性、完整性或时效性作任何保证。数据仅供参考，不构成任何投资建议。实际调用需遵守启信宝开放平台的使用条款和计费规则。
