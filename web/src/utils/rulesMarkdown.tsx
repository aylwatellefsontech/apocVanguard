import { isValidElement, type JSX, type ReactNode } from 'react'
import type { RulesHeading } from '../types'

const HEADING_LINE = /^(#{1,6})\s+(.+)$/

function flattenText(node: ReactNode): string {
  if (typeof node === 'string' || typeof node === 'number') {
    return String(node)
  }
  if (Array.isArray(node)) {
    return node.map(flattenText).join('')
  }
  if (isValidElement(node)) {
    return flattenText((node.props as { children?: ReactNode }).children)
  }
  return ''
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
}

function uniqueId(base: string, usedIds: Set<string>): string {
  const root = base || 'section'
  if (!usedIds.has(root)) {
    usedIds.add(root)
    return root
  }

  let index = 2
  let candidate = `${root}-${index}`
  while (usedIds.has(candidate)) {
    index += 1
    candidate = `${root}-${index}`
  }
  usedIds.add(candidate)
  return candidate
}

export function parseHeadingLine(content: string): { title: string; id?: string } {
  const raw = content.trim()
  const match = raw.match(/^(.*?)\s*\{#([^}]+)\}\s*$/)
  if (!match) {
    return { title: raw, id: undefined }
  }

  return {
    title: match[1].trim(),
    id: match[2],
  }
}

export function parseHeadingId(children: ReactNode): { id?: string; title: ReactNode } {
  const { title, id } = parseHeadingLine(flattenText(children))
  if (!id) {
    return { id: undefined, title: children }
  }

  return {
    id,
    title: title || null,
  }
}

export function preprocessRulesMarkdown(source: string): string {
  const usedIds = new Set<string>()

  return source
    .replace(/\\([-.])/g, '$1')
    .replace(HEADING_LINE, (line, hashes: string, content: string) => {
      const { title, id } = parseHeadingLine(content)
      if (!title) {
        return line
      }

      const resolvedId = id ? uniqueId(id, usedIds) : uniqueId(slugify(title), usedIds)
      return `${hashes} ${title} {#${resolvedId}}`
    })
}

export function extractRulesHeadings(source: string): RulesHeading[] {
  const headings: RulesHeading[] = []

  for (const line of source.split('\n')) {
    const match = line.match(HEADING_LINE)
    if (!match) {
      continue
    }

    const level = match[1].length
    const { title, id } = parseHeadingLine(match[2])
    if (!title || !id) {
      continue
    }

    headings.push({ level, title, id })
  }

  return headings
}

export function createHeadingComponent(Tag: keyof JSX.IntrinsicElements) {
  return function RulesHeading({
    children,
    ...props
  }: {
    children?: ReactNode
    id?: string
    className?: string
  }) {
    const { id, title } = parseHeadingId(children)
    const Component = Tag
    return (
      <Component id={id} {...props}>
        {title ?? children}
      </Component>
    )
  }
}
