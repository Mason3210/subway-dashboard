# 部署到 GitHub Pages 的简易方法

## 前提
你需要一个 GitHub 账号

## 步骤 1: 创建 GitHub 仓库

1. 打开 https://github.com/new
2. 仓库名称填写: `subway-dashboard`
3. 选择 **Public**
4. 点击 "Create repository"

## 步骤 2: 上传文件

创建仓库后，GitHub 会显示命令，按照下面操作：

```bash
cd C:\subway-safety-dashboard
git remote add origin https://github.com/YOUR_USERNAME/subway-dashboard.git
git push -u origin master
```

## 步骤 3: 启动 GitHub Pages

1. 仓库页面 → Settings → Pages
2. Source 选择 "main branch"
3. 保存后会显示网址

---

或者更简单：
1. 直接把 index.html 文件拖到 GitHub 仓库页面上传
2. 然后在 Settings → Pages 启动
