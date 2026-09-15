import { QuartzComponent, QuartzComponentConstructor } from "./types"
import { FullSlug, resolveRelative } from "../util/path"

export default (() => {
  const HomeIntro: QuartzComponent = ({ fileData }) => (
    <section class="home-intro" aria-label="欢迎来到 J4sper Notes">
      <div class="home-kicker">
        <span /> A GARDEN OF IDEAS
      </div>
      <h1>
        把零散想法，
        <br />
        <em>慢慢连成知识。</em>
      </h1>
      <p class="home-description">
        欢迎来到 J4sper 的数字花园。
        <br />
        在这里记录、思考，让每一条笔记都有迹可循。
      </p>
      <div class="home-actions">
        <a
          class="internal home-primary"
          href={resolveRelative(fileData.slug!, "notes/index" as FullSlug)}
        >
          开始阅读 <span aria-hidden="true">↗</span>
        </a>
        <a
          class="internal home-secondary"
          href={resolveRelative(fileData.slug!, "guide/index" as FullSlug)}
        >
          使用指南 <span aria-hidden="true">→</span>
        </a>
      </div>
      <div class="home-caption">NOTES / CONNECTIONS / DISCOVERIES</div>
    </section>
  )
  return HomeIntro
}) satisfies QuartzComponentConstructor
