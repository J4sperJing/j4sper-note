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
