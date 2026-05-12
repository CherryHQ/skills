#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "rich",
# ]
# ///
"""
Invoice intake script for expense-reimbursement skill.

Handles all deterministic Lark Base operations:
  1. Get current user identity (open_id, name)
  2. Locate user's personal Base token from summary index
  3. Duplicate invoice number check
  4. Create Base record with correct millisecond timestamps
  5. Upload attachment to 发票凭证 field

Agent is responsible for: PDF/image parsing, expense type classification,
description generation. Pass parsed fields as CLI arguments.

Usage:
  uv run invoice_intake.py \
    --invoice-number "26112000001871925391" \
    --invoice-date "2026-05-11" \
    --amount 94 \
    --pretax-amount 93.07 \
    --tax 0.93 \
    --expense-type "餐饮" \
    --description "北京道久餐饮管理有限公司餐饮服务" \
    --file "./invoice.pdf"
"""

import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.logging import RichHandler

LOG_DIR = Path(".agents/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(console=Console(stderr=True)),
        logging.FileHandler(LOG_DIR / "invoice-intake.log"),
    ],
)
logger = logging.getLogger(__name__)

# Summary index config (from feishu-base.md)
INDEX_BASE_TOKEN = "JGzKb5SKSal9A3suMyRcxRepnLe"
INDEX_TABLE_ID = "tblavWeOwUGHQZhA"

VALID_EXPENSE_TYPES = {"差旅", "餐饮", "交通", "办公用品", "通讯", "培训", "招待", "其他"}


def lark(args: list[str]) -> dict:
    """Run a lark-cli command and return parsed JSON output."""
    cmd = ["lark-cli"] + args
    logger.debug("lark-cli %s", " ".join(args))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"lark-cli failed: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        # lark-cli sometimes returns table-formatted text; treat as opaque
        return {"raw": result.stdout}


def to_ms_timestamp(date_str: str) -> int:
    """Convert YYYY-MM-DD to millisecond Unix timestamp (Base requires ms, not seconds)."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(dt.timestamp()) * 1000


def get_current_user() -> tuple[str, str]:
    """Return (open_id, name) for the authenticated Lark user."""
    data = lark(["api", "GET", "/open-apis/authen/v1/user_info"])
    if data.get("code") != 0:
        raise RuntimeError(f"Failed to get user info: {data}")
    user = data["data"]
    return user["open_id"], user["name"]


def find_personal_base(user_name: str) -> str:
    """Look up user's personal Base token from summary index table."""
    # lark-cli returns table-formatted text for +record-list without --json; use --json flag
    result = subprocess.run(
        ["lark-cli", "base", "+record-list",
         "--base-token", INDEX_BASE_TOKEN,
         "--table-id", INDEX_TABLE_ID,
         "--limit", "100",
         "--format", "json"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to read index table: {result.stderr.strip()}")

    try:
        records = json.loads(result.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Unexpected index table output: {result.stdout[:200]}")

    outer = records.get("data", {})
    # lark-cli --format json returns data.data (rows), data.fields (column names)
    rows = outer.get("data", [])
    fields_list = outer.get("fields", [])
    if rows and fields_list:
        try:
            name_idx = fields_list.index("姓名")
            token_idx = fields_list.index("Base Token")
        except ValueError:
            raise RuntimeError(f"Expected columns '姓名' and 'Base Token' not found: {fields_list}")
        for row in rows:
            if row[name_idx] == user_name:
                token = row[token_idx]
                if token:
                    return token
    else:
        # Fallback: nested items/records structure
        items = outer.get("items", outer.get("records", []))
        for item in items:
            item_fields = item.get("fields", {})
            name_val = item_fields.get("姓名", "")
            if isinstance(name_val, list):
                name_val = name_val[0].get("text", "") if name_val else ""
            if name_val == user_name:
                token = item_fields.get("Base Token", "")
                if isinstance(token, list):
                    token = token[0].get("text", "") if token else ""
                if token:
                    return token
    raise RuntimeError(f"No personal Base found for user '{user_name}' in summary index")


def get_table_id(base_token: str) -> str:
    """Return the first (and expected only) table ID from a personal Base."""
    result = subprocess.run(
        ["lark-cli", "base", "+table-list", "--base-token", base_token],
        capture_output=True, text=True,
    )
    data = json.loads(result.stdout)
    tables = data.get("data", {}).get("tables", [])
    if not tables:
        raise RuntimeError(f"No tables found in Base {base_token}")
    return tables[0]["id"]


def get_attachment_field_id(base_token: str, table_id: str, field_name: str = "发票凭证") -> str:
    """Look up the field_id for the attachment field by name."""
    result = subprocess.run(
        ["lark-cli", "base", "+field-list", "--base-token", base_token, "--table-id", table_id],
        capture_output=True, text=True,
    )
    data = json.loads(result.stdout)
    for field in data.get("data", {}).get("fields", []):
        if field.get("name") == field_name:
            return field["id"]
    raise RuntimeError(f"Attachment field '{field_name}' not found in table {table_id}")


def check_duplicate(base_token: str, table_id: str, invoice_number: str) -> bool:
    """Return True if invoice_number already exists in the Base table."""
    result = subprocess.run(
        ["lark-cli", "base", "+record-list",
         "--base-token", base_token,
         "--table-id", table_id,
         "--limit", "500"],
        capture_output=True, text=True,
    )
    return invoice_number in result.stdout


def create_record(
    base_token: str,
    table_id: str,
    open_id: str,
    invoice_number: str,
    invoice_date: str,
    apply_date: str,
    amount: float,
    pretax_amount: float,
    tax: float,
    expense_type: str,
    description: str,
    department: str,
) -> str:
    """Create a record and return the record_id."""
    fields = {
        "申请人": [{"id": open_id, "type": "open_id"}],
        "报销类型": expense_type,
        "审批状态": "待审批",
        "发生日期": to_ms_timestamp(invoice_date),
        "申请日期": to_ms_timestamp(apply_date),
        "报销金额": amount,
        "不含税金额": pretax_amount,
        "税额": tax,
        "发票号码": invoice_number,
        "事由说明": description,
    }
    if department:
        fields["归属部门"] = department

    payload = json.dumps({"fields": fields})
    result = subprocess.run(
        ["lark-cli", "api", "POST",
         f"/open-apis/bitable/v1/apps/{base_token}/tables/{table_id}/records",
         "--data", payload],
        capture_output=True, text=True,
    )
    data = json.loads(result.stdout)
    if data.get("code") != 0:
        raise RuntimeError(f"Failed to create record: {data}")
    return data["data"]["record"]["id"]


def upload_attachment(base_token: str, table_id: str, record_id: str, file_path: str) -> None:
    """Upload invoice file to 发票凭证 attachment field."""
    field_id = get_attachment_field_id(base_token, table_id)
    result = subprocess.run(
        ["lark-cli", "base", "+record-upload-attachment",
         "--file", file_path,
         "--base-token", base_token,
         "--table-id", table_id,
         "--record-id", record_id,
         "--field-id", field_id],
        capture_output=True, text=True,
    )
    data = json.loads(result.stdout)
    if not data.get("ok"):
        raise RuntimeError(f"Attachment upload failed: {data}")


@click.command()
@click.option("--invoice-number", required=True, help="发票号码")
@click.option("--invoice-date", required=True, help="开票日期 YYYY-MM-DD")
@click.option("--amount", required=True, type=float, help="价税合计（报销金额）")
@click.option("--pretax-amount", required=True, type=float, help="不含税金额")
@click.option("--tax", default=0.0, type=float, help="税额（默认0）")
@click.option("--expense-type", required=True,
              type=click.Choice(sorted(VALID_EXPENSE_TYPES)), help="报销类型")
@click.option("--description", required=True, help="事由说明")
@click.option("--file", "file_path", default="", help="发票文件路径（相对于当前目录）")
@click.option("--department", default="", help="归属部门（可选）")
@click.option("--apply-date", default="", help="申请日期 YYYY-MM-DD（默认今天）")
@click.option("--dry-run", is_flag=True, help="解析和校验，但不写入 Base")
def main(
    invoice_number: str,
    invoice_date: str,
    amount: float,
    pretax_amount: float,
    tax: float,
    expense_type: str,
    description: str,
    file_path: str,
    department: str,
    apply_date: str,
    dry_run: bool,
) -> None:
    apply_date = apply_date or datetime.today().strftime("%Y-%m-%d")

    if file_path and not Path(file_path).exists():
        logger.error("File not found: %s", file_path)
        sys.exit(1)

    # Step 1: Get user identity
    logger.info("Getting current user identity...")
    open_id, user_name = get_current_user()
    logger.info("User: %s (%s)", user_name, open_id)

    # Step 2: Locate personal Base
    logger.info("Looking up personal Base for '%s'...", user_name)
    base_token = find_personal_base(user_name)
    logger.info("Personal Base token: %s", base_token)

    table_id = get_table_id(base_token)
    logger.info("Table ID: %s", table_id)

    # Step 3: Duplicate check
    logger.info("Checking for duplicate invoice number '%s'...", invoice_number)
    if check_duplicate(base_token, table_id, invoice_number):
        logger.error("❌ Duplicate invoice number detected: %s — aborting.", invoice_number)
        sys.exit(2)
    logger.info("No duplicate found.")

    if dry_run:
        logger.info("[DRY RUN] Would write record: %s | %s | ¥%.2f | %s",
                    invoice_number, expense_type, amount, invoice_date)
        return

    # Step 4: Create record
    logger.info("Creating Base record...")
    record_id = create_record(
        base_token, table_id, open_id,
        invoice_number, invoice_date, apply_date,
        amount, pretax_amount, tax,
        expense_type, description, department,
    )
    logger.info("Record created: %s", record_id)

    # Step 5: Upload attachment
    if file_path:
        logger.info("Uploading attachment: %s", file_path)
        upload_attachment(base_token, table_id, record_id, file_path)
        logger.info("Attachment uploaded.")
    else:
        logger.warning("No file provided — skipping attachment upload.")

    click.echo(json.dumps({
        "status": "ok",
        "record_id": record_id,
        "base_token": base_token,
        "table_id": table_id,
        "invoice_number": invoice_number,
        "amount": amount,
    }))


if __name__ == "__main__":
    main()
