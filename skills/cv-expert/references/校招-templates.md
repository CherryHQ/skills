# 校招量化模板 & 输出策略

## 核心原则

校招候选人（应届生/实习）通常没有商业 KPI。
但"量化"不等于"商业数字"——学术与项目场景有大量可用的替代指标。
助手的任务是帮用户找到已有的可量化信息，而不是凭空编造数字。

---

## 替代量化框架（四类）

### 类型 1：数据规模
适用于：数据分析、ML、ETL、数据库项目

提问模板：
- "你的数据集大概有多少条记录？（哪怕数量级：千条/万条/百万条）"
- "你处理的文件/表格大概多大？（MB/GB 级别即可）"
- "你的模型用了多少个特征？"

转化示例：
- 无数字版：`Processed customer transaction data`
- 有数量级：`Processed ~50,000 customer transaction records` ⚠️ Estimate（待确认量级）
- 有精确数：`Processed 48,312 customer transaction records` ✅ Fact

---

### 类型 2：效率提升
适用于：自动化、脚本、流程优化项目

提问模板：
- "这个脚本/工具替代了哪些手工操作？大概节省了多少时间？"
- "没有这个工具前，同样的工作需要多久？有了之后呢？"
- "你的自动化替代了几个手工步骤？"

转化示例：
- 无数字版：`Automated report generation process`
- 有估算：`Automated weekly report generation, reducing manual effort from ~3 hours to 15 minutes` ⚠️ Estimate（待确认时间）
- 用步骤数：`Automated 5 manual steps in the data cleaning pipeline` ✅ Fact（如可数）

---

### 类型 3：质量提升
适用于：ML 模型、数据清洗、测试、质检项目

提问模板：
- "你的模型/方法最终达到了多少准确率/F1分数/AUC？"
- "改进前后的准确率对比是多少？"
- "你发现并修复了多少个数据质量问题？"

转化示例：
- 无数字版：`Improved model accuracy through feature engineering`
- 有对比：`Improved XGBoost model accuracy from 82% to 94% via feature engineering and hyperparameter tuning` ✅ Fact（验证项目报告）
- 有相对值：`Reduced null value rate in dataset from ~15% to < 1%` ⚠️ Estimate

---

### 类型 4：交付与规模
适用于：软件工程、产品开发、团队协作项目

提问模板：
- "你独立完成了多少个功能/模块？"
- "这个项目最终有多少人用到了你的成果？（组内/班级/比赛参与者）"
- "项目进行了几轮迭代？最终上线/提交了吗？"
- "你的代码/报告有没有被复用？被复用了几次？"

转化示例：
- 无数字版：`Contributed to a team project on NLP`
- 有团队规模：`Co-developed NLP pipeline with a 4-person team, delivering 3 model iterations over 8 weeks` ✅ Fact
- 有复用：`Reusable preprocessing module adopted by 2 other team projects` ✅ Fact（如确认）

---

## 校招场景特殊量化来源

| 信息来源 | 可量化内容 | 示例 |
|---------|-----------|------|
| 竞赛证书 | 排名、参赛人数、奖项等级 | "Top 15% of 500 teams in National Data Science Competition" |
| 课程项目 | 数据集大小、准确率、同学评分 | "Achieved 91% accuracy on test set (class average: 78%)" |
| 毕业设计 | 实验规模、章节数、被引用次数 | "Thesis reviewed by 3 faculty advisors; selected for department showcase" |
| 社团/组织 | 成员规模、活动次数、参与人数 | "Organized 5 workshops for 200+ participants as VP of Data Club" |
| 实习绩效 | 完成任务数、导师反馈评级 | "Received 'Exceeds Expectations' on mid-term intern review" |

---

## 对话提问最佳实践

### 提问顺序（校招）
1. 先问具体的数字/事实（数据规模、结果、规模）
2. 再问可以估算的信息（时间、比例）
3. 最后才问学历/专业相关（只有在 Dimension 1 中有严重风险信号时才问）

### 给用户的快速选择选项示例（避免开放式问题阻塞）

针对数据规模：
```
你的项目数据集大概是哪个量级？（选一个最接近的）
A) 几百条（< 1K）
B) 几千条（1K-10K）
C) 几万条（10K-100K）
D) 更大（> 100K 或 GB级）
E) 不确定/没有实际数据
```

针对效率：
```
你的自动化脚本节省了多少时间？（估算即可）
A) 每次节省 < 30 分钟
B) 每次节省 1-3 小时
C) 每周节省 > 3 小时
D) 说不清楚
```

---

## SAFE / BOOSTED 输出策略详解

### SAFE（默认）

**用于：** 谨慎型用户；不确定数据准确性；求稳

**正文规则：**
- 只写入 `FACT ✅` 内容
- `ESTIMATE ⚠️` → 仅以 Word 批注呈现，正文不改动
- `NEED_CONFIRM ❓` → 仅以 Word 批注呈现

**文件名：** `<原文件名>_optimized_safe.docx`

**批注示例（SAFE 模式 ESTIMATE）：**
```
⚠️ 建议优化 (未写入正文): 考虑加入"Processed ~50K records"以量化数据规模。
依据：用户提到数据集是"几万条"。请在确认准确数字后手动修改正文。
```

---

### BOOSTED（需要明确开启）

**用于：** 对数字有把握且愿意承担估算标注的用户

**正文规则：**
- `FACT ✅` → 直接写入正文
- `ESTIMATE ⚠️` → 每条在 Phase 4 Q&A 中逐一确认：
  - 用户说 "y/确认" → 写入正文 + 批注注明 ⚠️ Estimate
  - 用户说 "n/否" → 降级为 comment_only

**文件名：** `<原文件名>_optimized_boosted.docx`

**Q&A 提示格式（BOOSTED）：**
```
📝 我计划在正文中加入以下估算内容：

  "Processed ~50,000 customer transaction records"

依据：你提到数据集是"几万条"，50,000 是合理的中位估算。

✅ 确认写入正文 (y) / ❌ 仅加批注 (n)：
```

---

## 绝对禁止（校招模式）

无论 SAFE 还是 BOOSTED：

1. **不得** 捏造公司名称、项目名称、奖项名称
2. **不得** 发明不存在的实习经历或在职经历
3. **不得** 修改毕业学校、专业名称、GPA
4. **不得** 在用户明确表示"不确定/没有这个数据"后仍将该数字写入正文
5. **不得** 将 `NEED_CONFIRM` 项目写入正文（只允许批注）
6. **不得** 给估算数据加 ✅ Fact 标签

---

## 潜力信号增强（校招加分项）

当硬性量化不足时，以下"软性潜力信号"可在叙述中合理强化（无需用户额外数据）：

| 信号类型 | 重构方式 |
|---------|---------|
| 快速学习 | "Independently learned [tool] within [timeframe] to complete [project]" |
| 主动驱动 | "Self-initiated [project/improvement] to solve [problem]" |
| 跨学科应用 | "Applied [domain knowledge from X] to solve [problem in Y]" |
| 导师认可 | "Selected by faculty advisor for [recognition/showcase]" |
| 团队贡献 | "Led [specific component] of team project, responsible for [deliverable]" |

以上重构均需基于用户已有经历的真实描述，不可无中生有。
