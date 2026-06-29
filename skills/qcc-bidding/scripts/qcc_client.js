#!/usr/bin/env node
/**
 * 企查查 API 客户端 — 优先读 .env 文件，其次读系统环境变量。
 * 用法：
 *   node qcc_client.js <SERVER> <TOOL_NAME> <公司名>
 *   node qcc_client.js company get_company_registration_info "华为技术有限公司"
 */

const fs = require('fs');
const path = require('path');

const [server, tool, company] = process.argv.slice(2);

if (!server || !tool || !company) {
  console.error('用法: node qcc_client.js <SERVER> <TOOL_NAME> <公司名>');
  console.error('SERVER: company|risk|operation|ipr|executive|history');
  process.exit(1);
}

function getApiKey() {
  // 1. 系统环境变量
  if (process.env.QCC_API_KEY) return process.env.QCC_API_KEY;
  // 2. 脚本目录下的 .env 文件
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
  console.error('请任选一种方式设置:');
  console.error('  1. 编辑 ' + path.join(__dirname, '.env') + ' 填入 Key');
  console.error('  2. 或将 Key 告诉 Agent，Agent 自动写入 .env');
  console.error('获取 Key: https://agent.qcc.com');
  process.exit(1);
}

const url = `https://agent.qcc.com/mcp/${server}/stream`;

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`
  },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/call',
    params: { name: tool, arguments: { searchKey: company } }
  })
})
  .then(r => {
    if (!r.ok) throw new Error(`HTTP ${r.status}: ${r.statusText}`);
    return r.text();
  })
  .then(t => {
    const dataLine = t.split('\n').find(l => l.startsWith('data:'));
    if (!dataLine) throw new Error('No SSE data line found');
    const d = JSON.parse(dataLine.slice(6));
    const text = d?.result?.content?.[0]?.text;
    if (!text) throw new Error('API returned unexpected response format');
    const result = JSON.parse(text);
    console.log(JSON.stringify(result, null, 2));
  })
  .catch(e => {
    console.error('[ERROR]', e.message);
    process.exit(1);
  });
