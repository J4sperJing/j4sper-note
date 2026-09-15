---
title: 写作与发布
description: 三种方式更新笔记，提交后自动生成网站。
---

## 方式一：在 GitHub 网页上传

1. 打开 [仓库中的笔记目录](https://github.com/J4sperJing/j4sper-note/tree/main/content/notes)。
2. 点击 **Add file → Upload files**，上传 `.md` 和对应图片。
3. 点击 **Commit changes** 保存到 `main` 分支。
4. 在仓库的 **Actions** 页面等待 **Deploy notes to GitHub Pages** 出现绿色对勾，再刷新网站。通常需要几分钟，实际以任务状态为准。

新的 Markdown 文件会自动加入目录、搜索和对应文件夹列表，不需要手动配置菜单。放在其他 `content` 子目录的笔记也会自动出现。

## 方式二：在 VS Code 中写

1. 用 VS Code 打开本地 `j4sper-note` 项目文件夹。
2. 在 `content/notes` 新建或修改 `.md` 文件。
3. 保存文件，在左侧 **源代码管理** 中检查更改。
4. 输入提交说明，点击 **提交**，然后 **同步更改**（或 **推送**）。

**保存文件只会更新本地。推送到 GitHub 后，才会更新网站。**

如果你刚在 GitHub 网页修改过内容，先在 VS Code 拉取更新，再继续本地写作。

## 文章格式

纯 Markdown 可以直接发布。推荐在顶部增加标题、日期和标签：

```markdown
---
title: 我的第一篇笔记
date: 2026-09-15
tags:
  - 学习
---

从这里开始写正文。

## 一个小标题

这是一个段落。
```

文件名可以使用中文。为了让链接易读且稳定，也可以用小写英文和连字符，例如 `reading-notes.md`。标题可以保持中文；以后改文件名会改变文章网址。

## 图片与附件

图片建议放在 `content/assets`。如果文章位于 `content/notes`：

```markdown
![图片说明](../assets/example.png)
```

在 Obsidian 中也可以写 `![[example.png]]`，并把图片一同提交。只有外部图床链接不需要上传本地图片。

## 草稿与公开范围

这个站点和仓库都是公开的；提交到仓库的文件及其历史记录可以被他人查看。请把本项目作为专门的公开笔记库。

添加 `draft: true` 可以暂时不在网页展示，但文件一旦提交到公开仓库，源码仍然公开。未准备公开的笔记不要提交。

`private` 文件夹、Obsidian 设置和本地回收站已排除在常规提交之外。不要用强制添加的方式提交它们。

## 首页和外观

- 首页介绍：编辑 `content/index.md`。
- 笔记目录：添加、重命名或整理 `content` 下的文件夹。
- 站点名称与主题颜色：编辑 `quartz.config.ts`。
- 新笔记会自动进入首页的“最近更新”；`guide` 中的说明文章不会进入该列表。

## 更新没有出现时

先看 [Actions 发布记录](https://github.com/J4sperJing/j4sper-note/actions)。如果显示红色叉号，打开任务查看原因；如果发布成功但页面仍旧，强制刷新或稍等缓存更新。构建失败时，上一次成功发布的网站会继续提供访问。
