#!/usr/bin/env node
/**
 * 招投标信息格式化 — 调用 get_bidding_info 并按表格输出
 * 用法：
 *   node qcc_bidding_fmt.js <公司名>
 */

const fs = require('fs');
const path = require('path');

const company = process.argv[2];
if (!company) {
  console.error('用法: node qcc_bidding_fmt.js <公司名>');
  process.exit(1);
}

function getApiKey() {
  if (process.env.QCC_API_KEY) return process.env.QCC_API_KEY;
  const envPath = path.join(__dirname, '.env');
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, 'utf-8');
    const m = content.match(/^QCC_API_KEY=(.+)$/m);
    if (m && m[1]) {
      const val = m[1].trim();
      if (val && val !== 'your_key_here') return val;
    }
  }
  return null;
}

const apiKey = getApiKey();
if (!apiKey) {
  console.error('[ERROR] 未找到 QCC_API_KEY');
  console.error('请将 Key 告诉 Agent 让其写入 .env，或手动编辑 .env 文件');
  console.error('获取 Key: https://agent.qcc.com');
  process.exit(1);
}

fetch('https://agent.qcc.com/mcp/operation/stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`
  },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/call',
    params: { name: 'get_bidding_info', arguments: { searchKey: company } }
  })
})
  .then(r => {
    if (!r.ok) throw new Error(`HTTP ${r.status}: ${r.statusText}`);
    return r.text();
  })
  .then(t => {
    const dataLine = t.split('\n').find(l => l.startsWith('data:'));
    if (!dataLine) throw new Error('No SSE data line');
    const d = JSON.parse(dataLine.slice(6));
    const r2 = JSON.parse(d.result.content[0].text);
    console.log('## ' + r2.摘要);
    (r2.招投标信息 || []).slice(0, 15).forEach(b =>
      console.log('| ' + b.发布日期 + ' | ' + b.中标金额 + ' | ' + (b.中标单位 || []).join('/') + ' | ' + (b.项目名称 || '').substring(0, 60) + ' |')
    );
  })
  .catch(e => console.error('[ERROR]', e.message));
