# J4sper Notes

一个使用 Quartz 4 和 GitHub Pages 的中文 Markdown 笔记站点。

**网站：** https://j4sperjing.github.io/j4sper-note/

## 日常写作

- **网页上传**：打开 `content/notes`，选择 Add file → Upload files，上传 Markdown 后提交。
- **VS Code**：打开项目，编辑 `content` 中的文件，提交并推送到 `main`。
- **Obsidian**：将 `content` 文件夹打开为笔记库，写完后在 VS Code 提交并推送。

每次推送后，GitHub Actions 自动构建并发布。保存本地文件不等于发布。

详见 [写作与发布](content/guide/publishing.md) 和 [Obsidian 使用指南](content/guide/obsidian.md)。

## 目录

```text
content/
  index.md        # 首页介绍
  notes/          # 笔记，支持任意子目录
  assets/         # 图片和附件
  guide/          # 写作说明
quartz.config.ts  # 标题、域名、颜色
quartz.layout.ts  # 页面组件布局
quartz/styles/custom.scss  # 外观样式
.github/workflows/deploy.yml  # 自动发布
```

新笔记自动进入目录、搜索和首页最近更新，不需要手工修改导航。目录里的 `index.md` 用于描述该目录；首页 `content/index.md` 需要保留。

## 本地预览（可选）

需要 Node.js 22 或更高版本，以及 npm 10.9.2 或更高版本。

```sh
npm ci
npx quartz build --serve
```

打开命令输出的本地地址。日常网页上传和编辑 Markdown 不需要安装运行环境。

## GitHub Pages

仓库 Settings → Pages → Source 设为 **GitHub Actions**。默认分支为 `main`。工作流只使用 GitHub 自动提供的凭据，不需要自己添加部署令牌。

## 公开范围

仓库及网站公开。只有准备分享的内容才应提交；`draft: true` 仅让网页不显示，不能隐藏已提交的源码。`private/`、`.obsidian/`、`.trash/` 和 `.env` 已加入忽略规则。

本项目基于 [Quartz v4.5.2](https://github.com/jackyzha0/quartz/tree/v4.5.2)，保留原项目 MIT 许可证。`docs/` 为框架文档，不会作为笔记发布。

## 自定义笔记顺序

在 Markdown 顶部属性里添加 `order: 10`，数字越小越靠前。左侧目录和文件夹文章列表使用同一规则：有数字的条目优先；未填写的条目排在后面；数字相同或都未填写时，文件夹优先，再按标题自然排序。

```yaml
---
title: 基础知识
order: 10
---
```

建议使用 `10、20、30`，方便以后插入 `15`。留空或 `order: null` 表示不指定顺序，`order: 0` 则是有效编号。给文件夹排序时，把 `order` 写在该文件夹的 `index.md` 中。不同文件夹的子笔记分别排序。首页“最近更新”继续按日期排列。

此规则控制网站排序。Obsidian 文件列表和 VS Code 文件浏览器有各自的排序设置。

## 新笔记自动生成属性（本机）

项目提供一个独立于编辑器的本地监听程序，支持 Obsidian 和 VS Code。新建并保存 `content` 下的 `.md` 后，等待文件写入稳定，约 2–3 秒会自动插入以下属性：

```yaml
---
title: ""
description: ""
tags: []
date: 2026-09-15
draft: true
order: null
---
```

上面的日期只是示例；实际使用创建当天的本地日期。`title`、`description`、`tags` 和 `order` 留空。标题为空时，网站会使用文件名。发布前取消 `draft` 勾选或改为 `false`。

默认项保存在 `note-defaults.json`。首次启用时，现有笔记保持原样。已有属性的文件、通过 Git 拉取的已跟踪文件，以及 `private`、`templates`、`.obsidian`、`.trash` 里的文件都不会被补写。仅在编辑器中创建的未保存文档还不是磁盘文件，需要先保存。

在这台 Mac 的 `~/project/j4sper-note` 已配置登录后自动运行。首次克隆到另一台 Mac，或修改默认项后，可以在项目根目录运行：

```sh
/usr/bin/python3 scripts/install_note_defaults.py
```

运行状态和日志保存在忽略提交的 `.local/note-defaults/`。监听只修改本地文件，提交和推送由 Git 插件负责。

如需停用本机监听：

```sh
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.j4sper.note-defaults.plist"
```

Git 自动同步仅在 Obsidian 打开该笔记库、插件运行时工作。在 VS Code 写作时也可以保持这个 Obsidian 笔记库打开；或者用 VS Code 的源代码管理手动同步。
