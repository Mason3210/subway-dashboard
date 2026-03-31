# 🚇 全球轨道交通安全看板

**Global Subway Safety Dashboard**

部署地址: https://your-name.gitee.io/subway-safety-dashboard

---

## 📱 部署到 Gitee Pages (免费，国内可直接访问)

### 方法一: 命令行部署

```bash
# 1. 安装 gitee-pages CLI (如未安装)
npm install -g gitee-pages

# 2. 进入项目目录
cd subway-safety-dashboard

# 3. 部署
gitee-pages deploy
```

### 方法二: 手动上传

1. 打开 https://gitee.com 并登录
2. 创建新仓库: `subway-safety-dashboard`
3. 上传 `index.html` 文件
4. 进入仓库 → 服务 → Gitee Pages
5. 点击 "启动" 按钮
6. 获取访问地址

---

## 📊 功能特性

- ✅ 中英文双语切换
- ✅ 港铁MTR风格专业设计
- ✅ 200+数据源监控
- ✅ 交互式图表
- ✅ 响应式布局 (支持手机/平板)

### 数据源 (200+)

| 类型 | 数量 |
|------|------|
| 地铁运营公司 | 52 |
| 政府交通部门 | 116 |
| 微信公众号 | 53 |
| 新浪微博 | 14 |
| 国际机构 | 5 |

---

## 🔄 更新数据

由于是静态页面，数据更新方式:

### 方式1: 修改index.html中的数据
直接编辑 `index.html` 文件中的 JavaScript 数据部分:

```javascript
updates: [
    { time: '2024-01-15', title: '新标题', source: '来源', type: '类型' },
    // 添加更多...
],
```

### 方式2: 定期重新部署
- 每周更新数据后重新上传 index.html
- 或使用自动化脚本生成新 index.html 后部署

---

## 📁 文件说明

```
subway-safety-dashboard/
├── index.html          # 静态看板页面 (直接部署此文件)
├── app.py              # Flask后端 (如需动态版本)
├── templates/          # Flask模板
├── static/             # 静态资源
├── data_sources_config.py  # 数据源配置
├── enhanced_scraper.py     # 网站爬虫
└── social_media_unified.py  # 社交媒体采集
```

---

## ☁️ 其他部署选项

| 平台 | 访问速度 | 说明 |
|------|---------|------|
| **Gitee Pages** | ⚡ 快 | ✅ 推荐，国内直访问 |
| GitHub Pages | ⚠️ 慢 | 需翻墙 |
| Vercel | ⚠️ 间歇 | 可能被墙 |
| Cloudflare Pages | ⚠️ 间歇 | 可能被墙 |

---

## 📞 后续支持

如需:
- 自动化数据更新
- 微信手动导入教程
- 添加更多数据源

请告知我继续开发。

---

**© 2024 全球轨道交通安全看板**
