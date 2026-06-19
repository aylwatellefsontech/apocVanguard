export function isApiDatasource(): boolean {
  return import.meta.env.DATASOURCE === 'api'
}
