import test from "node:test"
import assert from "node:assert/strict"
import { compareExplorerNotes, compareFolderNotes, normalizeNoteOrder } from "./noteOrder"
import type { QuartzPluginData } from "../plugins/vfile"
import type { FullSlug } from "./path"

const node = (title: string, order?: number, folder = false) => ({
  displayName: title,
  slug: title,
  isFolder: folder,
  data: { order },
})

test("explicit order, zero, folders, missing order and natural titles", () => {
  const items = [
    node("10 note"),
    node("2 note"),
    node("folder", undefined, true),
    node("early", 0),
    node("late", 20),
    node("folder-first", 10, true),
  ]
  assert.deepEqual(
    items.sort(compareExplorerNotes).map((n) => n.displayName),
    ["early", "folder-first", "late", "folder", "2 note", "10 note"],
  )
})

test("browser receives a self-contained serialized comparator", () => {
  const compare = new Function(`return (${compareExplorerNotes.toString()})`)()
  assert.equal(compare(node("Z", 1), node("A", 2)), -1)
  assert.equal(compare(node("A", Infinity), node("B", 1)), 1)
})

test("empty values are unranked and numeric strings are accepted", () => {
  for (const value of [undefined, null, "", "  ", "invalid", true, [], Infinity, NaN]) {
    assert.equal(normalizeNoteOrder(value), undefined)
  }
  assert.equal(normalizeNoteOrder("0"), 0)
  assert.equal(normalizeNoteOrder(" 15 "), 15)
  assert.equal(normalizeNoteOrder(1.5), 1.5)
})

test("folder list uses the same rank as the explorer", () => {
  const page = (title: string, order: unknown, slug: string) =>
    ({
      frontmatter: { title, order },
      slug: slug as FullSlug,
    }) as QuartzPluginData
  const pages = [
    page("A", undefined, "notes/a"),
    page("Z", 2, "notes/z"),
    page("Folder", 1, "notes/folder/index"),
  ]
  assert.deepEqual(
    pages.sort(compareFolderNotes).map((p) => p.frontmatter?.title),
    ["Folder", "Z", "A"],
  )
})
