import type { LabelMap } from '../messages'

export const modelAccessMessages: Record<string, LabelMap> = {
  '企业版': { 'zh-CN': '企业版', 'en-US': 'Enterprise' },
  '模型使用权限': { 'zh-CN': '模型使用权限', 'en-US': 'Model Access' },
  '只有命中适用对象的员工才能看到并调用该模型。': { 'zh-CN': '只有命中适用对象的员工才能看到并调用该模型。', 'en-US': 'Only employees matching the audience can see and use this model.' },
  '请选择企业全员或至少一个适用对象': { 'zh-CN': '请选择企业全员或至少一个适用对象', 'en-US': 'Select all employees or at least one audience target' },
  '模型已保存，但使用权限保存失败': { 'zh-CN': '模型已保存，但使用权限保存失败', 'en-US': 'The model was saved, but its access policy could not be saved' },
}
