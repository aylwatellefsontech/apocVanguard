/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly DATASOURCE?: string
  readonly VITE_DATASOURCE?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare module '*.md?raw' {
  const content: string
  export default content
}
