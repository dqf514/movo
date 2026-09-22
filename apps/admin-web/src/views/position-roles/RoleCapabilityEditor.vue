<script setup lang="ts">
import { t } from '@/composables/i18n';
import { computed } from 'vue';
import type { AgentCapabilityKey, PositionRoleDraft } from '@/api/positionRoles';

const props = defineProps<{
  modelValue: PositionRoleDraft;
  disabled?: boolean;
}>();
const emit = defineEmits<{ 'update:modelValue': [value: PositionRoleDraft] }>();

const draft = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
});

const capabilityOptions: Array<{ key: AgentCapabilityKey; label: string; description: string }> = [
  { key: 'content_generation', label: t('内容生成'), description: t('文章、报告、方案等专业内容生产') },
  { key: 'image_generation', label: t('图片生成'), description: t('直接生成图片或为内容任务生成配图') },
  { key: 'code_generation', label: t('代码生成'), description: t('Code Agent、项目、文件、终端与 Git 操作') },
  { key: 'browser_automation', label: t('浏览器自动运行'), description: t('允许 Agent 操作本地浏览器完成网页任务') },
  { key: 'internal_knowledge', label: t('内部知识检索'), description: t('在既有知识权限范围内检索企业资料') },
];
const impactPreview = computed(() => {
  const enabled = capabilityOptions.filter(item => draft.value.capabilities[item.key]).map(item => item.label);
  return enabled.length ? enabled.join(t('列表分隔符')) : t('普通问答');
});

function setCapability(key: AgentCapabilityKey, enabled: boolean) {
  draft.value = { ...draft.value, capabilities: { ...draft.value.capabilities, [key]: enabled } };
}
</script>

<template>
  <div class="capability-editor">
    <section>
      <h3>{{ t('Agent 能力') }}</h3>
      <p class="section-help">{{ t('员工端入口与运行时调用将同时遵守这些设置。') }}</p>
      <div class="capability-grid">
        <button
          v-for="item in capabilityOptions"
          :key="item.key"
          type="button"
          class="capability-card"
          :class="{ active: draft.capabilities[item.key] }"
          :disabled="disabled"
          @click="setCapability(item.key, !draft.capabilities[item.key])"
        >
          <span class="capability-card__copy"><strong>{{ item.label }}</strong><small>{{ item.description }}</small></span>
          <n-switch :value="draft.capabilities[item.key]" :disabled="disabled" @update:value="setCapability(item.key, $event)" @click.stop />
        </button>
      </div>
    </section>

    <n-alert type="info" :bordered="false">
      <strong>{{ t('员工端影响预览：') }}</strong>{{ impactPreview }}
      <div class="resource-note">{{ t('具体 Skill、MCP 与工具的使用对象，请在对应资源中配置。') }}</div>
    </n-alert>
  </div>
</template>

<style scoped>
.capability-editor { display: grid; gap: 4px; }
h3 { margin: 0 0 6px; color: #172033; font-size: 15px; }
.section-help { margin: 0 0 14px; color: #667085; font-size: 13px; }
.capability-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.capability-card { min-height: 76px; display: flex; align-items: center; justify-content: space-between; gap: 16px; border: 1px solid #e4e7ec; border-radius: 10px; background: #fff; padding: 14px; text-align: left; cursor: pointer; transition: border-color .2s, background-color .2s; }
.capability-card:hover { border-color: #9bbcff; }
.capability-card.active { border-color: #7aa2ff; background: #f6f9ff; }
.capability-card__copy { display: grid; gap: 5px; }
.capability-card small { color: #667085; line-height: 1.45; }
section :deep(.n-select) { margin-top: 12px; }
.resource-note { margin-top: 5px; color: #667085; font-size: 12px; }
@media (max-width: 760px) { .capability-grid { grid-template-columns: 1fr; } }
</style>
