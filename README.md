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

仓库及网站公开。只有准备分享的内容才应提交；`draft: true` 仅让网页不显示，不能隐藏已提交的源码。`private/`、`.trash/` 和 `.env` 已加入忽略规则；`.obsidian/` 仅同步下文列出的插件配置和属性类型。

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

## 新笔记自动生成属性（编辑器扩展）

模板和配置跟随这个仓库同步，不需要系统后台服务。

### Obsidian

1. 将 `content` 文件夹打开为笔记库。
2. 安装并启用社区插件 **Git** 和 **Templater**。
3. 在 **设置 → Templater → File creation** 中打开 **Trigger Templater on new file creation**。

模板目录、匹配规则和属性类型已经配置。Templater 新版本将自动触发开关保存在当前设备，每台新设备需要手动打开一次。Templater 2.25.0 要求 Obsidian 1.13.0 或更新版本。

Git 配置为每 10 分钟自动提交并推送，启动时拉取、每 10 分钟拉取。插件必须在 Obsidian 中运行；关闭该笔记库后不会自动同步。账号授权由本机 Git 单独管理。

### VS Code

1. 打开外层 `j4sper-note` 项目根目录。
2. 安装推荐扩展 [Auto Snippet](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.auto-snippet)。
3. 在资源管理器里于 `content` 下新建一个 `.md` 并打开，属性会自动插入并保存。

规则也适用于打开一个空的 Markdown 文件。已有正文不会被覆盖；如果先在未命名文档中写了内容再保存，可使用 **Insert Snippet → J4sper new note** 手动插入属性。

VS Code 的模板功能不依赖 Obsidian。提交与推送可在 VS Code 源代码管理中操作；如果希望沿用 Obsidian Git 自动同步，保持 Obsidian 打开同一 `content` 笔记库即可。

### 默认属性

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

日期按新建时的本地日期生成，上面只是示例。`title` 为空时，网站使用文件名。`order` 留空表示不指定顺序。`draft` 默认 `true`，发布前取消勾选或改为 `false`。自动提交到公开仓库的草稿源码仍然公开。

Obsidian 模板位于 `content/templates/new-note.md`；VS Code 模板位于 `.vscode/j4sper-note.code-snippets`。模板、插件设置和属性类型一起同步；插件程序、凭据和个人窗口布局保持本地。
