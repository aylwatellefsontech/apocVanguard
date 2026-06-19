import { isValidElement } from 'react'

function flattenText(node) {
  if (typeof node === 'string' || typeof node === 'number') {
    return String(node)
  }
  if (Array.isArray(node)) {
    return node.map(flattenText).join('')
  }
  if (isValidElement(node)) {
    return flattenText(node.props.children)
  }
  return ''
}

export function parseHeadingId(children) {
  const raw = flattenText(children).trim()
  const match = raw.match(/^(.*?)\s*\{#([^}]+)\}\s*$/)
  if (!match) {
    return { id: undefined, title: children }
  }

  const titleText = match[1].trim()
  return {
    id: match[2],
    title: titleText || null,
  }
}

export function preprocessRulesMarkdown(source) {
  return source.replace(/\\([-.])/g, '$1')
}

export function createHeadingComponent(Tag) {
  return function RulesHeading({ children, ...props }) {
    const { id, title } = parseHeadingId(children)
    return (
      <Tag id={id} {...props}>
        {title ?? children}
      </Tag>
    )
  }
}
