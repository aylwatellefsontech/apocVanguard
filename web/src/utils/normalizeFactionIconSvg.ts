const BLACK_COLOR =
  /(?:rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)|#(?:000000|000)|black)/i

function replaceBlackColors(svg: string): string {
  return svg
    .replace(/fill:\s*(?:rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)|#(?:000000|000)|black)/gi, 'fill: currentColor')
    .replace(/stroke:\s*(?:rgb\(\s*0\s*,\s*0\s*,\s*0\s*\)|#(?:000000|000)|black)/gi, 'stroke: currentColor')
    .replace(/\bfill="(?:#(?:000000|000)|black)"/gi, 'fill="currentColor"')
    .replace(/\bstroke="(?:#(?:000000|000)|black)"/gi, 'stroke="currentColor"')
}

function hasExplicitFill(style: string, fillAttr: string | undefined): boolean {
  if (fillAttr) {
    return true
  }

  return /(?:^|;)\s*fill\s*:/.test(style)
}

function fillIsNone(style: string, fillAttr: string | undefined): boolean {
  if (fillAttr && /^none$/i.test(fillAttr)) {
    return true
  }

  return /(?:^|;)\s*fill\s*:\s*none\b/i.test(style)
}

function defaultFillForTag(tag: string): string {
  if (tag === 'line' || tag === 'polyline' || tag === 'ellipse') {
    return 'fill: none'
  }

  return 'fill: currentColor'
}

function isFillOnlyLayer(style: string): boolean {
  return /(?:^|;)\s*stroke-width:\s*0(?:px)?\b/i.test(style)
}

function ensureStyleProperty(style: string, property: string, value: string): string {
  const pattern = new RegExp(`(^|;\\s*)${property}\\s*:[^;]*`, 'i')
  if (pattern.test(style)) {
    return style.replace(pattern, `$1${property}: ${value}`)
  }

  return style ? `${property}: ${value}; ${style}` : `${property}: ${value}`
}

function normalizeShapeAttributes(tag: string, attrs: string): string {
  const fillAttrMatch = attrs.match(/\bfill="([^"]*)"/i)
  const fillAttr = fillAttrMatch?.[1]
  const styleMatch = attrs.match(/\bstyle="([^"]*)"/i)
  let style = styleMatch?.[1] ?? ''

  if (!hasExplicitFill(style, fillAttr) && !fillIsNone(style, fillAttr)) {
    const defaultFill = defaultFillForTag(tag)
    style = style ? `${defaultFill}; ${style}` : defaultFill
  }

  if (
    (tag === 'path' || tag === 'polygon') &&
    isFillOnlyLayer(style) &&
    !fillIsNone(style, fillAttr)
  ) {
    style = ensureStyleProperty(style, 'fill', 'currentColor')
    style = ensureStyleProperty(style, 'stroke', 'none')
  }

  if (fillAttr && BLACK_COLOR.test(fillAttr)) {
    attrs = attrs.replace(fillAttrMatch![0], 'fill="currentColor"')
  }

  if (styleMatch) {
    return attrs.replace(styleMatch[0], `style="${style}"`)
  }

  if (style) {
    return `${attrs} style="${style}"`
  }

  return attrs
}

export function normalizeFactionIconSvg(svg: string): string {
  let result = replaceBlackColors(svg)

  result = result.replace(
    /<(path|polygon|ellipse|polyline|line|rect)(\s[^>]*?)>/gi,
    (_, tag, attrs) => `<${tag}${normalizeShapeAttributes(tag.toLowerCase(), attrs)}>`,
  )

  return result
}
