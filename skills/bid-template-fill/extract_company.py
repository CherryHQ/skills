#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公司信息提取器 - 从公司内部信息DOCX提取结构化数据，输出为company.json格式
用法：
  python extract_company.py <公司信息.docx> [-o company.json]
  python extract_company.py <公司信息.docx> --print  # 打印到标准输出
"""
import json, re, sys, os
from pathlib import Path

def extract_company_info(docx_path):
    """从公司信息DOCX提取结构化数据，返回dict"""
    try:
        from docx import Document
    except ImportError:
        print("[ERROR] 需要 python-docx。请运行: pip install python-docx", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(docx_path):
        print(f"[ERROR] 文件不存在: {docx_path}", file=sys.stderr)
        sys.exit(1)

    doc = Document(docx_path)

    # 收集所有段落文本和表格文本
    all_texts = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            all_texts.append(text)

    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            all_texts.append('\t'.join(cells))

    full_text = '\n'.join(all_texts)

    # 字段提取规则：按冒号分隔的键值对
    field_pattern = re.compile(
        r'^(.*?)[：:]\s*(.+?)$', re.MULTILINE
    )

    raw_fields = {}
    for m in field_pattern.finditer(full_text):
        key = m.group(1).strip()
        value = m.group(2).strip()
        # 过滤明显不是数据的行（标题、章节等）
        if len(key) > 20 or key in ('一', '二', '三', '四', '五', '六', '七', '八', '附'):
            continue
        if not value or value in ('—', '-'):
            continue
        raw_fields[key] = value

    # 映射到模板key
    COMPANY_FULL = raw_fields.get('公司全称', '')
    COMPANY_SHORT = raw_fields.get('公司简称', '')
    LEGAL_PERSON = raw_fields.get('法定代表人', '')
    AUTH_REP = raw_fields.get('授权代表', '')
    ADDRESS = raw_fields.get('注册地址', '')
    ZIPCODE = raw_fields.get('邮政编码', '')
    BANK = raw_fields.get('开户银行全称', '') or raw_fields.get('开户银行名称', '')
    ACCOUNT = raw_fields.get('银行账号', '')
    PHONE = raw_fields.get('联系电话', '') or raw_fields.get('办公电话', '')
    MOBILE = raw_fields.get('手机号码', '') or raw_fields.get('手机', '')
    FAX = raw_fields.get('传真号码', '') or raw_fields.get('传真', '')
    CONTACT = raw_fields.get('联系人姓名', '') or raw_fields.get('项目联系人', '')

    result = {}

    # 公司全称/简称
    if COMPANY_FULL:
        result['XX重工股份有限公司'] = COMPANY_FULL
        result['XX重工集团有限公司'] = COMPANY_FULL
        result['XX集团有限公司'] = COMPANY_FULL
    if COMPANY_SHORT:
        result['XX重工'] = COMPANY_SHORT
        result['XX集团'] = COMPANY_SHORT

    # 法人/授权代表
    if LEGAL_PERSON:
        result['金红萍'] = LEGAL_PERSON
        result['王红梅'] = LEGAL_PERSON
    if AUTH_REP:
        result['沈小芳'] = AUTH_REP
        result['李小明'] = AUTH_REP

    # 地址/联系方式
    if ADDRESS:
        result['[公司地址]'] = ADDRESS
    if ZIPCODE:
        result['[邮编已脱敏]'] = ZIPCODE
    if BANK:
        result['[开户银行名称]'] = BANK
    if ACCOUNT:
        result['[银行账号]'] = ACCOUNT
    if PHONE:
        result['[电话已脱敏]'] = PHONE
    if MOBILE:
        result['[手机已脱敏]'] = MOBILE
    if FAX:
        result['[传真已脱敏]'] = FAX

    # 附加信息（供参考）
    extra = {}
    if CONTACT:
        extra['联系人'] = CONTACT
    credit_code = raw_fields.get('统一社会信用代码', '')
    if credit_code:
        extra['统一社会信用代码'] = credit_code

    return {'fill_data': result, 'extra': extra, 'raw': raw_fields}


def main():
    if len(sys.argv) < 2:
        print("用法: python extract_company.py <公司信息.docx> [选项]")
        print()
        print("选项:")
        print("  -o <文件>    输出为JSON文件")
        print("  --print      打印到标准输出（默认）")
        print()
        print("示例:")
        print("  python extract_company.py 公司信息.docx -o company.json")
        print("  python extract_company.py 公司信息.docx --print")
        sys.exit(1)

    docx_path = sys.argv[1]
    output_path = None
    print_mode = True

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '-o' and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            print_mode = False
            i += 2
        elif sys.argv[i] == '--print':
            print_mode = True
            i += 1
        else:
            i += 1

    data = extract_company_info(docx_path)

    if output_path:
        # 保存为company.json格式
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data['fill_data'], f, ensure_ascii=False, indent=2)
        print(f"[OK] 已提取 {len(data['fill_data'])} 个映射键 → {output_path}")
        if data['extra']:
            print(f"  附加信息: {json.dumps(data['extra'], ensure_ascii=False)}")
    else:
        print("=" * 50)
        print("  公司信息提取结果")
        print("=" * 50)
        print()
        print("--- 模板填充映射（可直接用作company.json）---")
        print(json.dumps(data['fill_data'], ensure_ascii=False, indent=2))
        if data['extra']:
            print()
            print("--- 附加参考信息 ---")
            print(json.dumps(data['extra'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
