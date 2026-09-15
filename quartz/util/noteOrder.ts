import type { QuartzPluginData } from "../plugins/vfile"
import { isFolderPath } from "./path"

export function normalizeNoteOrder(value: unknown): number | undefined {
  if (typeof value !== "number" && typeof value !== "string") return undefined
  if (typeof value === "string" && value.trim() === "") return undefined
  const order = Number(value)
  return Number.isFinite(order) ? order : undefined
}

type OrderedNode = {
  data?: { order?: number } | null
  isFolder: boolean
  displayName: string
  slug: string
}

// Explorer serializes this function for the browser; keep it free of external references.
export function compareExplorerNotes(a: OrderedNode, b: OrderedNode): number {
  const aValue = a.data?.order
  const bValue = b.data?.order
  const aOrder = typeof aValue === "number" && Number.isFinite(aValue) ? aValue : Infinity
  const bOrder = typeof bValue === "number" && Number.isFinite(bValue) ? bValue : Infinity
  if (aOrder !== bOrder) return aOrder < bOrder ? -1 : 1
  if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
  return (
    a.displayName.localeCompare(b.displayName, "zh-CN", { numeric: true, sensitivity: "base" }) ||
    a.slug.localeCompare(b.slug, "zh-CN", { numeric: true })
  )
}

export function compareFolderNotes(a: QuartzPluginData, b: QuartzPluginData): number {
  const entry = (page: QuartzPluginData): OrderedNode => ({
    data: { order: normalizeNoteOrder(page.frontmatter?.order) },
    isFolder: isFolderPath(page.slug ?? ""),
    displayName: page.frontmatter?.title ?? "",
    slug: page.slug ?? "",
  })
  return compareExplorerNotes(entry(a), entry(b))
}
