import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import { QuartzComponent } from "./quartz/components/types"
import HomeIntro from "./quartz/components/HomeIntro"

const home = (component: QuartzComponent) =>
  Component.ConditionalRender({ component, condition: (page) => page.fileData.slug === "index" })
const article = (component: QuartzComponent) =>
  Component.ConditionalRender({ component, condition: (page) => page.fileData.slug !== "index" })

export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [
    home(
      Component.RecentNotes({
        title: "最近更新",
        limit: 5,
        showTags: true,
        filter: (page) =>
          page.slug !== "index" &&
          !page.slug?.endsWith("/index") &&
          !page.slug?.startsWith("guide/"),
      }),
    ),
  ],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/J4sperJing/j4sper-note",
      RSS: "https://j4sperjing.github.io/j4sper-note/index.xml",
    },
  }),
}

const left: PageLayout["left"] = [
  Component.PageTitle(),
  Component.MobileOnly(Component.Spacer()),
  Component.Flex({
    components: [
      { Component: Component.Search(), grow: true },
      { Component: Component.Darkmode() },
      { Component: Component.ReaderMode() },
    ],
  }),
  Component.Explorer({ folderClickBehavior: "link", folderDefaultState: "open" }),
]

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    home(HomeIntro()),
    article(Component.Breadcrumbs({ rootName: "首页" })),
    article(Component.ArticleTitle()),
    article(Component.ContentMeta()),
    article(Component.TagList()),
  ],
  left,
  right: [
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Graph(),
    article(Component.Backlinks()),
  ],
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs({ rootName: "首页" }), Component.ArticleTitle()],
  left,
  right: [],
}
