import type { LabelMap } from '../messages'

export const resourceAccessMessages: Record<string, LabelMap> = {
  '使用权限': { 'zh-CN': '使用权限', 'en-US': 'Access' },
  '{name} · 使用权限': { 'zh-CN': '{name} · 使用权限', 'en-US': '{name} · Access' },
  'Skill 使用权限': { 'zh-CN': 'Skill 使用权限', 'en-US': 'Skill Access' },
  'MCP / 工具使用权限': { 'zh-CN': 'MCP / 工具使用权限', 'en-US': 'MCP / Tool Access' },
  '只有命中适用对象的员工才能看到并使用该 Skill。': { 'zh-CN': '只有命中适用对象的员工才能看到并使用该 Skill。', 'en-US': 'Only employees matching the audience can see and use this Skill.' },
  'MCP 服务下发现的工具默认继承该服务的适用对象。': { 'zh-CN': 'MCP 服务下发现的工具默认继承该服务的适用对象。', 'en-US': 'Tools discovered from an MCP server inherit the server audience by default.' },
  '保存使用权限': { 'zh-CN': '保存使用权限', 'en-US': 'Save Access' },
  '使用权限已保存': { 'zh-CN': '使用权限已保存', 'en-US': 'Access policy saved' },
  '加载使用权限失败': { 'zh-CN': '加载使用权限失败', 'en-US': 'Failed to load access policy' },
  '保存使用权限失败': { 'zh-CN': '保存使用权限失败', 'en-US': 'Failed to save access policy' },
  '具体 Skill、MCP 与工具的使用对象，请在对应资源中配置。': { 'zh-CN': '具体 Skill、MCP 与工具的使用对象，请在对应资源中配置。', 'en-US': 'Configure the audience for each Skill, MCP server, or tool on that resource.' },
}
