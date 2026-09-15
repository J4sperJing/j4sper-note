import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"
import { compareFolderNotes } from "./quartz/util/noteOrder"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "J4sper Notes",
    pageTitleSuffix: " · J4sper Notes",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "zh-CN",
    baseUrl: "j4sperjing.github.io/j4sper-note",
    ignorePatterns: ["private", "templates", ".obsidian", ".trash"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "local",
      cdnCaching: false,
      typography: {
        header: "PingFang SC",
        body: "PingFang SC",
        code: "SFMono-Regular",
      },
      colors: {
        lightMode: {
          light: "#faf9f6",
          lightgray: "#e5e6df",
          gray: "#81877f",
          darkgray: "#414a43",
          dark: "#203a2e",
          secondary: "#28654b",
          tertiary: "#497a61",
          highlight: "rgba(71, 116, 88, 0.09)",
          textHighlight: "#e5d5a588",
        },
        darkMode: {
          light: "#17211d",
          lightgray: "#334139",
          gray: "#98a39a",
          darkgray: "#c9d3cc",
          dark: "#ecf1e9",
          secondary: "#a1ccb0",
          tertiary: "#b6d8bc",
          highlight: "rgba(141, 184, 155, 0.12)",
          textHighlight: "#84784888",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage({ sort: compareFolderNotes }),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
