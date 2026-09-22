<script setup lang="ts">
import { t } from '@/composables/i18n';
import { computed, ref, watch } from 'vue';
import { useMessage } from 'naive-ui';
import {
  createCapabilityOverride,
  listCapabilityOverrides,
  revokeCapabilityOverride,
  type AgentCapabilityKey,
  type CapabilityOverride,
} from '@/api/positionRoles';
import { formatAdminDateTime } from '@/composables/adminTimezone';

const props = defineProps<{ show: boolean; userId: string; userName: string }>();
const emit = defineEmits<{ (event: 'update:show', value: boolean): void }>();
const message = useMessage();
const loading = ref(false);
const saving = ref(false);
const overrides = ref<CapabilityOverride[]>([]);
const expiresAt = ref<number | null>(Date.now() + 7 * 24 * 60 * 60 * 1000);
const reason = ref('');
const allowCapabilities = ref<AgentCapabilityKey[]>([]);
const denyCapabilities = ref<AgentCapabilityKey[]>([]);

const capabilityOptions = [
  { label: t('内容生成'), value: 'content_generation' },
  { label: t('图片生成'), value: 'image_generation' },
  { label: t('代码生成'), value: 'code_generation' },
  { label: t('浏览器自动运行'), value: 'browser_automation' },
  { label: t('内部知识检索'), value: 'internal_knowledge' },
];
const hasChange = computed(() => allowCapabilities.value.length + denyCapabilities.value.length > 0);

function resetDraft() {
  allowCapabilities.value = [];
  denyCapabilities.value = [];
  expiresAt.value = Date.now() + 7 * 24 * 60 * 60 * 1000;
  reason.value = '';
}

async function load() {
  if (!props.userId) return;
  loading.value = true;
  try {
    overrides.value = await listCapabilityOverrides(props.userId);
  } finally { loading.value = false; }
}

async function save() {
  if (!hasChange.value) return message.warning(t('请选择至少一项临时授权或限制'));
  if (!expiresAt.value || expiresAt.value <= Date.now()) return message.warning(t('请选择未来的失效时间'));
  if (!reason.value.trim()) return message.warning(t('请填写授权原因'));
  saving.value = true;
  try {
    await createCapabilityOverride(props.userId, {
      allowCapabilities: allowCapabilities.value,
      denyCapabilities: denyCapabilities.value,
      effectiveAt: new Date().toISOString(),
      expiresAt: new Date(expiresAt.value).toISOString(),
      reason: reason.value.trim(),
    });
    message.success(t('临时授权已生效'));
    resetDraft();
    await load();
  } catch (error: any) { message.error(error?.response?.data?.detail || error?.message || t('授权失败')); }
  finally { saving.value = false; }
}

async function revoke(row: CapabilityOverride) {
  try {
    await revokeCapabilityOverride(row.id);
    message.success(t('临时授权已撤销'));
    await load();
  } catch (error: any) { message.error(error?.response?.data?.detail || error?.message || t('撤销失败')); }
}

watch(() => props.show, (visible) => { if (visible) void load(); });
</script>

<template>
  <n-modal :show="show" preset="card" :title="t('{name} · 临时能力授权', { name: userName })" style="width: 720px" @update:show="(value: boolean) => emit('update:show', value)">
    <n-spin :show="loading">
      <n-alert type="info" :bordered="false">{{ t('岗位角色仍是长期权限基线；这里仅用于有明确原因和失效时间的临时例外。') }}</n-alert>
      <n-form label-placement="top" class="override-form">
        <n-grid :cols="2" :x-gap="14">
          <n-grid-item><n-form-item :label="t('临时增加能力')"><n-select v-model:value="allowCapabilities" multiple :options="capabilityOptions.filter(item => !denyCapabilities.includes(item.value as AgentCapabilityKey))" /></n-form-item></n-grid-item>
          <n-grid-item><n-form-item :label="t('临时限制能力')"><n-select v-model:value="denyCapabilities" multiple :options="capabilityOptions.filter(item => !allowCapabilities.includes(item.value as AgentCapabilityKey))" /></n-form-item></n-grid-item>
        </n-grid>
        <n-grid :cols="2" :x-gap="14">
          <n-grid-item><n-form-item :label="t('失效时间')" required><n-date-picker v-model:value="expiresAt" type="datetime" clearable style="width:100%" /></n-form-item></n-grid-item>
          <n-grid-item><n-form-item :label="t('授权原因')" required><n-input v-model:value="reason" maxlength="1000" show-count /></n-form-item></n-grid-item>
        </n-grid>
        <n-space justify="end"><n-button type="primary" :loading="saving" @click="save">{{ t('创建临时授权') }}</n-button></n-space>
      </n-form>
      <n-divider>{{ t('授权记录') }}</n-divider>
      <n-empty v-if="!overrides.length" :description="t('暂无临时授权')" />
      <div v-else class="override-list">
        <div v-for="row in overrides" :key="row.id" class="override-row">
          <div><strong>{{ row.reason }}</strong><small>{{ t('{time} 创建', { time: formatAdminDateTime(row.createdAt, '-') }) }} · {{ row.expiresAt ? t('{time} 失效', { time: formatAdminDateTime(row.expiresAt, '-') }) : t('长期有效') }}</small></div>
          <n-tag :type="row.status === 'active' ? 'success' : 'default'" :bordered="false">{{ row.status === 'active' ? t('生效中') : (row.status === 'expired' ? t('已到期') : t('已撤销')) }}</n-tag>
          <n-button v-if="row.status === 'active'" text type="error" @click="revoke(row)">{{ t('撤销') }}</n-button>
        </div>
      </div>
    </n-spin>
  </n-modal>
</template>

<style scoped>
.override-form { margin-top: 18px; }
.override-list { display: grid; gap: 8px; }
.override-row { display: grid; grid-template-columns: minmax(0, 1fr) auto auto; align-items: center; gap: 12px; padding: 12px; border: 1px solid #e5e7eb; border-radius: 10px; }
.override-row div { display: grid; gap: 4px; }
.override-row small { color: #667085; }
</style>
