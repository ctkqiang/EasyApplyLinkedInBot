# 领英自动投递机器人 🤖

一个自动化的领英职位申请工具，帮助你快速投递简历。

## ✨ 功能特点

- 🔍 支持多关键词职位搜索
- 📍 支持地区筛选
- 🚀 自动申请"快速申请"职位
- 📝 处理多步骤申请流程
- 💾 保存申请记录和搜索结果
- 🔐 安全的密码输入处理

## 🛠 环境要求

- Python 3.8+
- Firefox 浏览器
- Selenium WebDriver
- 有效的领英账号

## 📦 安装

1. 克隆仓库：
```bash
git clone https://github.com/ctkqiang/EasyApplyLinkedInBot.git

cd EasyApplyLinkedInBot
````

2. 安装依赖：

```bash
pip3 install -r requirements.txt
```

## 🚀 使用方法

1. 运行程序：

```bash
python src/run.py
```

2. 按提示输入：
   - LinkedIn 账号
   - LinkedIn 密码
   - 目标地区
   - 职位关键词将在程序中设置

## 📁 输出文件

程序会在 `export` 目录下生成两类 CSV 文件：

- `{keyword}_all_jobs_{timestamp}.csv`: 搜索到的所有职位
- `{keyword}_applied_jobs_{timestamp}.csv`: 成功申请的职位

## 🖥 运行输出示例

运行程序时，您将看到以下类型的输出：

```plaintext
🤖 初始化领英自动投递机器人
👤 账号: your.email@example.com
🔍 搜索关键词: flutter, python, 爬虫
📍 地区: 中国
✅ 浏览器启动成功
🔐 正在登录LinkedIn...
✅ LinkedIn登录成功

🚀 开始搜索职位...
📊 正在搜索关键词: flutter
🌐 访问搜索页面: https://www.linkedin.com/jobs/search/...
📑 找到 1483 个职位，共 60 页

📄 正在处理第 1/60 页
⏳ 已收集 25 个职位ID
...

📋 总计找到 1483 个不重复职位
🤖 开始自动申请流程...

💼 正在处理第 1/1483 个职位
✅ 成功申请职位 12345678

📊 统计信息:
   - 总职位数: 1483
   - 成功申请: 50
   - 失败数量: 1433

💾 正在保存申请记录...
✅ 已保存到: export/flutter_applied_jobs_20240224_175352.csv
```

### 📊 输出文件格式

1. 搜索结果文件 (`{keyword}_all_jobs_{timestamp}.csv`):

```csv
datetime,title,company,location,url,status
2024-02-24 17:53:52,Flutter开发工程师,科技有限公司,上海,https://www.linkedin.com/jobs/view/12345678,未申请
```

2. 申请记录文件 (`{keyword}_applied_jobs_{timestamp}.csv`):

```csv
datetime,title,description,url,country
2024-02-24 17:53:52,高级Flutter开发工程师,职位描述...,https://www.linkedin.com/jobs/view/12345678,中国
```


## ⚠️ 注意事项

- 请确保您的 LinkedIn 账号已完善个人信息和简历
- 建议适当调整程序运行间隔，避免触发 LinkedIn 的反爬虫机制
- 使用工具时请遵守 LinkedIn 的使用条款
- 建议在使用前先小范围测试

## 许可证

本项目采用 **木兰宽松许可证 (Mulan PSL)** 进行许可。  
有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

[![License: Mulan PSL v2](https://img.shields.io/badge/License-Mulan%20PSL%202-blue.svg)](http://license.coscl.org.cn/MulanPSL2)

## 🌟 开源项目赞助计划

### 用捐赠助力发展

感谢您使用本项目！您的支持是开源持续发展的核心动力。  
每一份捐赠都将直接用于：  
✅ 服务器与基础设施维护  
✅ 新功能开发与版本迭代  
✅ 文档优化与社区建设

点滴支持皆能汇聚成海，让我们共同打造更强大的开源工具！

---

### 🌐 全球捐赠通道

#### 国内用户

<div align="center" style="margin: 40px 0">

<div align="center">
<table>
<tr>
<td align="center" width="300">
<img src="https://github.com/ctkqiang/ctkqiang/blob/main/assets/IMG_9863.jpg?raw=true" width="200" />
<br />
<strong>🔵 支付宝</strong>
</td>
<td align="center" width="300">
<img src="https://github.com/ctkqiang/ctkqiang/blob/main/assets/IMG_9859.JPG?raw=true" width="200" />
<br />
<strong>🟢 微信支付</strong>
</td>
</tr>
</table>
</div>
</div>

#### 国际用户

<div align="center" style="margin: 40px 0">
  <a href="https://qr.alipay.com/fkx19369scgxdrkv8mxso92" target="_blank">
    <img src="https://img.shields.io/badge/Alipay-全球支付-00A1E9?style=flat-square&logo=alipay&logoColor=white&labelColor=008CD7">
  </a>
  
  <a href="https://ko-fi.com/F1F5VCZJU" target="_blank">
    <img src="https://img.shields.io/badge/Ko--fi-买杯咖啡-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white">
  </a>
  
  <a href="https://www.paypal.com/paypalme/ctkqiang" target="_blank">
    <img src="https://img.shields.io/badge/PayPal-安全支付-00457C?style=flat-square&logo=paypal&logoColor=white">
  </a>
  
  <a href="https://donate.stripe.com/00gg2nefu6TK1LqeUY" target="_blank">
    <img src="https://img.shields.io/badge/Stripe-企业级支付-626CD9?style=flat-square&logo=stripe&logoColor=white">
  </a>
</div>

---

### 📌 开发者社交图谱

#### 技术交流

<div align="center" style="margin: 20px 0">
  <a href="https://github.com/ctkqiang" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-开源仓库-181717?style=for-the-badge&logo=github">
  </a>
  
  <a href="https://stackoverflow.com/users/10758321/%e9%92%9f%e6%99%ba%e5%bc%ba" target="_blank">
    <img src="https://img.shields.io/badge/Stack_Overflow-技术问答-F58025?style=for-the-badge&logo=stackoverflow">
  </a>
  
  <a href="https://www.linkedin.com/in/ctkqiang/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-职业网络-0A66C2?style=for-the-badge&logo=linkedin">
  </a>
</div>

#### 社交互动

<div align="center" style="margin: 20px 0">
  <a href="https://www.instagram.com/ctkqiang" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-生活瞬间-E4405F?style=for-the-badge&logo=instagram">
  </a>
  
  <a href="https://twitch.tv/ctkqiang" target="_blank">
    <img src="https://img.shields.io/badge/Twitch-技术直播-9146FF?style=for-the-badge&logo=twitch">
  </a>
  
  <a href="https://github.com/ctkqiang/ctkqiang/blob/main/assets/IMG_9245.JPG?raw=true" target="_blank">
    <img src="https://img.shields.io/badge/微信公众号-钟智强-07C160?style=for-the-badge&logo=wechat">
  </a>
</div>

---

🙌 感谢您成为开源社区的重要一员！  
💬 捐赠后欢迎通过社交平台与我联系，您的名字将出现在项目致谢列表！
