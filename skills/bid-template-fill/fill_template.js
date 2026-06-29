#!/usr/bin/env node
/**
 * DOCX 模板填充工具 v3
 * 跨平台支持：Windows/macOS/Linux，零外部依赖
 *
 * v3 改进：
 * - 日期替换不再硬编码年份，改为判断是否为当日
 * - 跨平台 ZIP 操作（Windows用PowerShell，Unix用unzip/zip）
 * - 添加输入校验和友好错误提示
 * - 占位符扫描支持三套格式
 */
import { readFileSync, writeFileSync, rmSync, readdirSync, statSync, existsSync, renameSync, mkdirSync } from "fs";
import { join, dirname, relative } from "path";
import { execSync } from "child_process";
import { platform, tmpdir } from "os";

// ==================== 参数校验 ====================
const templatePath = process.argv[2];
const outputPath = process.argv[3];
const dataPath = process.argv[4];

if (!templatePath || !outputPath) {
  console.log("用法: node fill_template.js <模板.docx> <输出.docx> [替换数据.json]");
  console.log();
  console.log("  模板.docx  - 含 _[占位符]_ 的脱敏DOCX模板");
  console.log("  输出.docx  - 生成的投标文件路径");
  console.log("  数据.json  - 键值对替换数据（可选）");
  process.exit(1);
}

if (!existsSync(templatePath)) {
  console.error(`[ERROR] 模板文件不存在: ${templatePath}`);
  process.exit(1);
}
if (dataPath && !existsSync(dataPath)) {
  console.error(`[ERROR] 数据文件不存在: ${dataPath}`);
  process.exit(1);
}

// ==================== 平台检测 ====================
const isWindows = platform() === "win32";
console.log(`  平台: ${platform()}`);

// ==================== 工具函数 ====================

function xmlEscape(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function isWordDocumentXML(relativePath) {
  const norm = relativePath.replace(/\\/g, "/");
  return norm.startsWith("word/") && norm.endsWith(".xml");
}

function todayChinese() {
  const d = new Date();
  return `${d.getFullYear()} 年 ${String(d.getMonth() + 1).padStart(2, "0")} 月 ${String(d.getDate()).padStart(2, "0")} 日`;
}

// ==================== ZIP 操作 ====================

function unzipDocx(docxPath, destDir) {
  mkdirSync(destDir, { recursive: true });
  if (isWindows) {
    const safeSrc = docxPath.replace(/'/g, "''");
    const safeDst = destDir.replace(/'/g, "''");
    execSync(
      `powershell -NoProfile -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('${safeSrc}', '${safeDst}')"`,
      { stdio: "pipe", encoding: "utf-8", maxBuffer: 100 * 1024 * 1024 }
    );
  } else {
    execSync(`unzip -o "${docxPath}" -d "${destDir}"`, {
      stdio: "pipe", encoding: "utf-8", maxBuffer: 100 * 1024 * 1024
    });
  }
}

function zipDocx(sourceDir, outputPath) {
  const absSource = sourceDir;
  const absOutput = outputPath;
  if (isWindows) {
    const psScript = [
      `$source = '${absSource.replace(/'/g, "''")}'`,
      `$output = '${absOutput.replace(/'/g, "''")}'`,
      `Add-Type -AssemblyName System.IO.Compression.FileSystem`,
      `$zip = [System.IO.Compression.ZipFile]::Open($output, 'Create')`,
      `try {`,
      `  $allFiles = Get-ChildItem -Path $source -File -Recurse`,
      `  $ct = Get-ChildItem -Path $source -Filter '[Content_Types].xml' | Select-Object -First 1`,
      `  if ($ct) {`,
      `    $entry = $zip.CreateEntry('[Content_Types].xml')`,
      `    $bytes = [System.IO.File]::ReadAllBytes($ct.FullName)`,
      `    $stream = $entry.Open()`,
      `    $stream.Write($bytes, 0, $bytes.Length)`,
      `    $stream.Close()`,
      `  }`,
      `  foreach ($f in $allFiles) {`,
      `    if ($f.Name -eq '[Content_Types].xml') { continue }`,
      `    $relPath = $f.FullName.Substring($source.Length + 1) -replace '\\\\', '/'`,
      `    $entry = $zip.CreateEntry($relPath)`,
      `    $bytes = [System.IO.File]::ReadAllBytes($f.FullName)`,
      `    $stream = $entry.Open()`,
      `    $stream.Write($bytes, 0, $bytes.Length)`,
      `    $stream.Close()`,
      `  }`,
      `} finally {`,
      `  $zip.Dispose()`,
      `}`,
    ].join("\n");
    const ps1Path = join(tmpdir(), `pack_docx_${Date.now()}.ps1`);
    writeFileSync(ps1Path, psScript, "utf-8");
    try {
      execSync(`powershell -NoProfile -ExecutionPolicy Bypass -File "${ps1Path}"`, {
        stdio: "pipe", encoding: "utf-8", maxBuffer: 100 * 1024 * 1024
      });
    } finally {
      rmSync(ps1Path, { force: true });
    }
  } else {
    const cwd = process.cwd();
    process.chdir(absSource);
    try {
      execSync(`zip -r "${absOutput}" .`, {
        stdio: "pipe", encoding: "utf-8", maxBuffer: 100 * 1024 * 1024
      });
    } finally {
      process.chdir(cwd);
    }
  }
}

// ==================== 日期替换 ====================

const DATE_PATTERN = /(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日/g;

function replaceDatesInText(text) {
  const today = todayChinese();
  const todayCompact = today.replace(/\s+/g, "");
  return text.replace(DATE_PATTERN, (match, y, m, d) => {
    const year = parseInt(y, 10);
    const month = parseInt(m, 10);
    const day = parseInt(d, 10);
    const now = new Date();
    if (year === now.getFullYear() && month === now.getMonth() + 1 && day === now.getDate()) {
      return match;
    }
    return today;
  });
}

// ==================== DOCX XML感知替换 ====================

function docxAwareReplace(xml, replacements) {
  let totalOccurrences = 0;
  let datesReplaced = 0;

  const result = xml.replace(/<w:p\b[\s\S]*?<\/w:p>/g, (paragraph) => {
    const segments = [];
    const tRegex = /<w:t([^>]*)>([\s\S]*?)<\/w:t>/g;
    let m;
    while ((m = tRegex.exec(paragraph)) !== null) {
      segments.push({ attrs: m[1], text: m[2] });
    }
    if (segments.length === 0) return paragraph;

    let merged = segments.map((s) => s.text).join("");
    let paraChanged = false;

    // 阶段一：整日期正则替换（优先处理）
    const beforeDate = merged;
    merged = replaceDatesInText(merged);
    if (merged !== beforeDate) {
      paraChanged = true;
      datesReplaced++;
    }

    // 阶段二：占位符替换
    const sorted = Object.entries(replacements).sort((a, b) => b[0].length - a[0].length);
    for (const [key, value] of sorted) {
      if (!merged.includes(key)) continue;
      const escaped = xmlEscape(value);
      const count = merged.split(key).length - 1;
      merged = merged.split(key).join(escaped);
      totalOccurrences += count;
      paraChanged = true;
    }

    if (!paraChanged) return paragraph;

    let rebuilt = paragraph;
    let isFirst = true;
    rebuilt = rebuilt.replace(
      /<w:t([^>]*)>([\s\S]*?)<\/w:t>/g,
      (full, attrs) => {
        if (isFirst) {
          isFirst = false;
          const spaceAttr = attrs.includes("xml:space") ? attrs : attrs + ' xml:space="preserve"';
          return `<w:t${spaceAttr}>${merged}</w:t>`;
        }
        return `<w:t${attrs}></w:t>`;
      }
    );
    return rebuilt;
  });

  return { content: result, occurrences: totalOccurrences, dates: datesReplaced };
}

// ==================== 主流程 ====================

let replacements = {};
if (dataPath) {
  let raw = readFileSync(dataPath, "utf-8");
  if (raw.charCodeAt(0) === 0xfeff) raw = raw.slice(1);
  try {
    replacements = JSON.parse(raw);
  } catch (e) {
    console.error(`[ERROR] JSON 解析失败: ${e.message}`);
    process.exit(1);
  }
  console.log(`  加载 ${Object.keys(replacements).length} 个替换键`);
}

const outputDir = dirname(outputPath);
if (outputDir && !existsSync(outputDir)) {
  mkdirSync(outputDir, { recursive: true });
}

const tmpDir = join(outputDir, ".tmpl_" + Date.now());
const placeholderPatterns = [
  /_[^\s]+_/g,
  /\[[^\]]+]/g,
  /（[^）]+）/g
];
let exitCode = 0;

try {
  // 步骤1：解包
  console.log("📦 解包模板...");
  unzipDocx(templatePath, tmpDir);

  // 步骤2：替换
  console.log("🔍 替换占位符...");
  let totalFiles = 0;
  let totalOccurrences = 0;

  function processDir(dir) {
    for (const entry of readdirSync(dir)) {
      const full = join(dir, entry);
      if (statSync(full).isDirectory()) { processDir(full); continue; }
      if (!entry.endsWith(".xml") && !entry.endsWith(".rels")) continue;

      const rel = relative(tmpDir, full);
      let content = readFileSync(full, "utf-8");
      let fileChanged = 0;

      if (isWordDocumentXML(rel)) {
        const r = docxAwareReplace(content, replacements);
        if (r.occurrences > 0 || r.dates > 0) {
          content = r.content;
          fileChanged = r.occurrences + r.dates;
        }
      } else {
        const sorted = Object.entries(replacements).sort((a, b) => b[0].length - a[0].length);
        for (const [key, value] of sorted) {
          const escapedValue = xmlEscape(value);
          const before = content.split(key).length;
          content = content.split(key).join(escapedValue);
          const after = content.split(key).length;
          if (before !== after) fileChanged++;
        }
      }

      if (fileChanged > 0) {
        writeFileSync(full, content, "utf-8");
        console.log(`  ✓ ${rel} (${fileChanged} 处)`);
        totalFiles++;
        totalOccurrences += fileChanged;
      }
    }
  }

  processDir(tmpDir);
  console.log(`  共修改 ${totalFiles} 个文件，替换 ${totalOccurrences} 处`);

  // 步骤3：遗漏检查（三套占位符格式）
  const unfilled = new Set();
  function scanDir(dir) {
    for (const entry of readdirSync(dir)) {
      const full = join(dir, entry);
      if (statSync(full).isDirectory()) { scanDir(full); continue; }
      if (!entry.endsWith(".xml") && !entry.endsWith(".rels")) continue;
      const content = readFileSync(full, "utf-8");
      for (const pattern of placeholderPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          for (const p of matches) {
            if (p.startsWith("[Content") || p.startsWith("[ISO")) continue;
            unfilled.add(p);
          }
        }
      }
    }
  }
  scanDir(tmpDir);

  if (unfilled.size > 0) {
    console.log(`\n⚠️  发现 ${unfilled.size} 个未填充的占位符：`);
    const sorted = [...unfilled].sort();
    for (const p of sorted.slice(0, 20)) {
      console.log(`  ◇ ${p}`);
    }
    if (sorted.length > 20) {
      console.log(`  ... 还有 ${sorted.length - 20} 个`);
    }
    console.log("  请检查数据文件是否包含对应键。");
  }

  // 步骤4：打包
  console.log("\n📦 打包输出...");
  const zipPath = outputPath.replace(/\.docx$/i, ".zip");
  zipDocx(tmpDir, zipPath);

  if (existsSync(zipPath)) {
    if (existsSync(outputPath)) rmSync(outputPath, { force: true });
    renameSync(zipPath, outputPath);
    console.log(`✅ ${outputPath}`);
    if (unfilled.size === 0) {
      console.log("   所有占位符已填充完毕。");
    }
  } else {
    console.error("❌ 打包失败，未生成输出文件");
    exitCode = 1;
  }
} catch (err) {
  console.error(`\n❌ 错误: ${err.message}`);
  if (err.stderr) console.error(err.stderr.toString());
  exitCode = 1;
} finally {
  if (existsSync(tmpDir)) {
    try { rmSync(tmpDir, { recursive: true, force: true }); } catch {}
  }
}

process.exit(exitCode);
