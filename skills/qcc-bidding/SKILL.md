---
name: qcc-bidding
description: "企业招投标全维度尽调——Node.js fetch 直连企查查 API。覆盖企业工商、司法风险、经营罗盘、知识产权、董监高、历史存档 6 大 Server 共 69 个招投标核心工具。当用户说「查招投标」「查公司」「尽调XX公司」「评估供应商」「找投标机会」时必须使用。"
---

# 企查查招投标尽调

> 调用链：`node -e fetch()` → `agent.qcc.com/mcp/<server>/stream` → JSON 数据。每次独立调用，不依赖 MCP 代理。


## ⚠️ 首次使用：申请 API Key

本 Skill 不含内置 Key，首次使用必须申请自己的：

1. 访问 **[https://agent.qcc.com](https://agent.qcc.com)** 注册账号
2. 登录后点击「免费注册拿 API Key」获取 Key（免费赠送 500 积分）
3. 在本文件中**全局搜索 YOUR_API_KEY**，**全部替换**为你的 API Key
4. 保存文件，即可使用

> 每个 Key 独立计费，**请勿将含 Key 的 Skill 文件分享给他人**。Key 过期后重新申请并替换即可。

---## API 端点

| Server | 端点 | 工具数 | 用途 |
|--------|------|--------|------|
| 企业工商 | `agent.qcc.com/mcp/company/stream` | 16 | 注册信息、股东、实控人、财务、年报 |
| 司法风险 | `agent.qcc.com/mcp/risk/stream` | 36 | 失信、被执行、裁判文书、行政处罚、欠税 |
| 经营罗盘 | `agent.qcc.com/mcp/operation/stream` | 35 | 招投标、资质、信用、纳税、舆情、荣誉 |
| 知识产权 | `agent.qcc.com/mcp/ipr/stream` | 18 | 商标、专利、软著、企业标准 |
| 董监高 | `agent.qcc.com/mcp/executive/stream` | 43 | 董监高任职、关联企业、风险扫描 |
| 历史存档 | `agent.qcc.com/mcp/history/stream` | 3 | 历史工商/股东/失信（需企业认证） |

---

## 命令格式

场景中每条命令的格式为 `Server Tool "公司名"`，执行时替换到下面模板中：

| 命令中的字段 | 替换到模板 |
|-------------|-----------|
| `company` / `risk` / `operation` / `ipr` / `executive` / `history` | `SERVER` |
| `get_xxx` | `TOOL_NAME` |
| `"公司全称"` | `COMPANY_NAME` |

## 通用调用模板

```bash
node -e "
const KEY='COMPANY_NAME';
fetch('https://agent.qcc.com/mcp/SERVER/stream',{
  method:'POST',
  headers:{
    'Content-Type':'application/json',
    'Authorization':'Bearer YOUR_API_KEY'
  },
  body:JSON.stringify({
    jsonrpc:'2.0',id:1,method:'tools/call',
    params:{name:'TOOL_NAME',arguments:{searchKey:KEY}}
  })
}).then(r=>r.text()).then(t=>{
  const d=JSON.parse(t.split('\n').find(l=>l.startsWith('data:')).slice(6));
  console.log(JSON.stringify(JSON.parse(d.result.content[0].text),null,2));
}).catch(e=>console.error(e.message))
"
```

## 招投标 & 财务数据的格式化模板

以下两个工具输出量大，用专用格式化替代通用 JSON dump：

**招投标**（替换模板 `.then(t=>{...})` 部分）：
```js
.then(t=>{
  const d=JSON.parse(t.split('\n').find(l=>l.startsWith('data:')).slice(6));
  const r2=JSON.parse(d.result.content[0].text);
  console.log('## '+r2.摘要);
  r2.招投标信息.slice(0,15).forEach(b=>
    console.log('| '+b.发布日期+' | '+b.中标金额+' | '+(b.中标单位||[]).join('/')+' | '+b.项目名称.substring(0,60)+' |')
  );
})
```

**财务数据**（替换模板 `.then(t=>{...})` 部分）：
```js
.then(t=>{
  const d=JSON.parse(t.split('\n').find(l=>l.startsWith('data:')).slice(6));
  const r2=JSON.parse(d.result.content[0].text);
  (r2.财务数据信息||[]).forEach(f=>{
    const m=f.指标详情&&f.指标详情.主要财务指标;
    if(m) console.log(f.报告期,'营收:'+m.营业总收入,'利润:'+m.利润总额,'资产:'+m.总资产);
    const a=f.指标详情&&f.指标详情.分析数据;
    if(a) console.log('  净利率:'+a.盈利能力.净利率+'%','负债率:'+a.偿还能力.资产负债率+'%','营收增速:'+a.成长能力.营业收入同比+'%');
  });
})
```

> **原则**：能用表格/字段提取的就用专用格式化；其余工具走通用 JSON dump 即可。

---

## 招投标尽调工具集（按维度分组）

### 工商基础 (company)
| 工具 | 招投标用途 |
|------|-----------|
| `get_company_by_query` | 模糊搜索锁定公司全称 |
| `get_company_registration_info` | 工商注册：名称/代码/法人/资本/成立/状态/地址 |
| `get_company_profile` | 企业概况摘要 |
| `get_actual_controller` | 实际控制人穿透 |
| `get_beneficial_owners` | 最终受益人（UBO） |
| `get_shareholder_info` | 股东出资结构 |
| `get_key_personnel` | 主要人员 |
| `get_external_investments` | 对外投资 |
| `get_branches` | 分支机构 |
| `get_change_records` | 工商变更记录 |
| `get_annual_reports` | 企业年报 |
| `get_financial_data` | 财务数据：营收/利润/资产/净利率/负债率/增速 |
| `verify_company_accuracy` | 核验工商信息准确性 |

### 风险扫描 (risk)
| 工具 | 招投标用途 |
|------|-----------|
| `get_company_risk_scan` | **一键综合风险扫描**（投标前必查） |
| `get_dishonest_info` | 失信被执行人 |
| `get_high_consumption_restriction` | 限制高消费 |
| `get_business_exception` | 经营异常 |
| `get_serious_violation` | 严重违法失信 |
| `get_administrative_penalty` | 行政处罚 |
| `get_tax_violation` | 税收违法 |
| `get_tax_arrears_notice` | 欠税公告 |
| `get_default_info` | 违约事项/票据违约 |
| `get_judicial_documents` | 裁判文书 |
| `get_court_notice` | 开庭公告 |
| `get_equity_freeze` | 股权冻结 |
| `get_stock_pledge_info` | 股权质押 |
| `get_equity_pledge_info` | 股权出质 |
| `get_terminated_cases` | 终本案件 |
| `get_case_filing_info` | 立案信息 |
| `get_environmental_penalty` | 环保处罚 |

### 一票否决类风险 (risk)
| 工具 | 招投标用途 |
|------|-----------|
| `get_bankruptcy_reorganization` | **破产重整**（投标资格一票否决） |
| `get_guarantee_info` | **对外担保**（或有负债风险） |
| `get_chattel_mortgage_info` | **动产抵押**（资产受限） |
| `get_judicial_auction` | 司法拍卖 |
| `get_exit_restriction` | 限制出境 |
| `get_valuation_inquiry` | 评估询价 |

### 经营实力 (operation)
| 工具 | 招投标用途 |
|------|-----------|
| `get_bidding_info` | **招投标记录**（累计/中标/项目明细） |
| `get_qualifications` | **资质证书**（ISO/CMMI/行业资质） |
| `get_credit_evaluation` | 信用评价 |
| `get_taxpayer_qualification` | 纳税信用等级 |
| `get_honor_info` | 荣誉信息/获奖 |
| `get_government_announcement` | 政府公告（招投标相关） |
| `get_government_interview` | 政府约谈（风险信号） |
| `get_news_sentiment` | 新闻舆情 |
| `get_administrative_license` | 行政许可 |
| `get_ranking_list_info` | 行业排名 |
| `get_recruitment_info` | 招聘信息（经营活跃度） |

### 投标机会 (operation)
| 工具 | 招投标用途 |
|------|-----------|
| `get_land_grant_info` | **土地出让**（工程建设标来源） |
| `get_land_transfer_info` | 土地转让 |
| `get_property_rights_transaction` | **产权交易**（国有资产标来源） |
| `get_asset_auction` | 资产拍卖 |
| `get_financing_records` | 融资记录（企业扩张信号） |
| `get_company_announcement` | 企业公告 |

### 知识产权 (ipr)
| 工具 | 招投标用途 |
|------|-----------|
| `get_trademark_info` | 商标 |
| `get_patent_info` | 专利 |
| `get_international_patent` | 国际专利 |
| `get_software_copyright_info` | 软件著作权 |
| `get_copyright_work_info` | 作品著作权 |
| `get_standard_info` | **企业标准**（投标加分项） |
| `get_ipr_pledge` | 知识产权质押 |

### 董监高 (executive)
| 工具 | 招投标用途 |
|------|-----------|
| `get_executive_risk_scan` | **董监高综合风险扫描** |
| `get_executive_positions` | 董监高任职 |
| `get_executive_related_companies` | 关联企业 |
| `get_executive_controlled_companies` | 控制企业 |
| `get_executive_dishonest` | 董监高失信 |
| `get_executive_high_consumption_ban` | 董监高限高 |
| `get_executive_historical_dishonest` | 董监高历史失信 |

### 历史追溯 (history)
| 工具 | 招投标用途 |
|------|-----------|
| `get_historical_company_info` | 历史工商（洗白核查） |
| `get_historical_shareholder_info` | 历史股东 |
| `get_historical_dishonest_info` | 历史失信 |

> **注意**：history Server 需企业认证。未认证时跳过历史维度，不影响主流程。

---

## 场景一：快速查公司

先模糊搜索锁定全称 → 再并行查工商+失信+招投标：

```
步骤1：company get_company_by_query "关键词"
步骤2（并行）：
  company get_company_registration_info "全称"
  risk get_dishonest_info "全称"
  operation get_bidding_info "全称"
```

输出：**企业概览** + **风险速览** + **招投标 TOP 5**（`get_bidding_info` 用专用格式化）。

---

## 场景二：供应商全面尽调（核心场景）

用户说「尽调 XX 公司」，**分 4 批并行执行**：

### 第 1 批：基础画像 (4 条)
```
company get_company_registration_info "全称"
company get_actual_controller "全称"
company get_shareholder_info "全称"
company get_company_profile "全称"
```

### 第 2 批：一键风险 + 一票否决 (5 条)
```
risk get_company_risk_scan "全称"
risk get_bankruptcy_reorganization "全称"
risk get_guarantee_info "全称"
risk get_chattel_mortgage_info "全称"
executive get_executive_risk_scan "全称"
```

### 第 3 批：经营实力 (5 条)
```
operation get_bidding_info "全称"
operation get_qualifications "全称"
operation get_credit_evaluation "全称"
operation get_taxpayer_qualification "全称"
company get_financial_data "全称"
```

### 第 4 批：深度维度 (5 条·按需)
```
operation get_news_sentiment "全称"
operation get_honor_info "全称"
ipr get_patent_info "全称"
ipr get_standard_info "全称"
executive get_executive_related_companies "全称"
```

### 汇总报告结构

```
## 供应商尽调报告：XX 公司

### 一、企业画像
- 工商信息、实控人、股东结构

### 二、风险评级（A/B/C/D）
- 综合风险扫描结果
- 失信/被执行/违约/限高/经营异常/欠税/行政处罚
- 破产重整/对外担保/动产抵押（一票否决项）
- 董监高风险

### 三、经营实力
- 招投标 TOP 10（日期/金额/项目/中标单位）
- 资质证书清单
- 信用评价 / 纳税等级 / 行业排名
- 财务 3 年对比（营收/利润/资产/净利率/负债率）

### 四、加分项
- 荣誉/获奖、企业标准、专利/软著

### 五、关联关系
- 董监高关联企业

### 六、综合结论
- 风险评级 + 是否建议合作 + 关注事项
```

---

## 场景三：招投标专项

```
operation get_bidding_info "全称"        # 招投标历史（专用格式化）
operation get_qualifications "全称"      # 资质证书
operation get_honor_info "全称"          # 获奖荣誉
ipr get_standard_info "全称"             # 企业标准
company get_financial_data "全称"        # 财务实力（专用格式化）
```

---

## 场景四：关联关系穿透

```
company get_actual_controller "全称"
company get_shareholder_info "全称"
executive get_executive_positions "全称"
executive get_executive_controlled_companies "全称"
executive get_executive_related_companies "全称"
```

---

## 场景五：投标合规核查

重点关注招标文件中的禁止性条款：

```
risk get_company_risk_scan "全称"               # 综合风险
risk get_bankruptcy_reorganization "全称"       # 破产重整（一票否决）
risk get_serious_violation "全称"               # 严重违法（一票否决）
risk get_dishonest_info "全称"                  # 失信（一票否决）
risk get_tax_arrears_notice "全称"              # 欠税
risk get_high_consumption_restriction "全称"    # 限高
risk get_guarantee_info "全称"                  # 对外担保
risk get_chattel_mortgage_info "全称"           # 动产抵押
operation get_government_interview "全称"       # 政府约谈
```

---

## 场景六：投标机会发现

用户说「找标」「有什么可投的」时，从经营罗盘中挖掘机会：

```
operation get_land_grant_info "地区或关键词"               # 土地出让（工程标）
operation get_property_rights_transaction "地区或关键词"   # 产权交易（国资标）
operation get_asset_auction "地区或关键词"                 # 资产拍卖
operation get_government_announcement "关键词"             # 政府公告
operation get_company_announcement "关键词"                # 企业公告
```

> `searchKey` 可以填地区名（如"苏州"）、行业关键词（如"市政工程"）或留空。



