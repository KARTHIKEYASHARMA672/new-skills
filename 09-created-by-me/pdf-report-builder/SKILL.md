---
name: pdf-report-builder
description: Use when a report/summary/receipt must be delivered as a professional PDF on Windows - builds styled HTML, renders PDF via msedge headless --print-to-pdf (no internet, no paid tooling), verifies page count and content, and places the file with a matching .png cover if wanted. Includes Word COM fallback and an HTML template with typography, tables and checkboxes.
---

# PDF Report Builder (Windows-native)

## The proven loop
1. Write `report.html` (target location, e.g. deliverable folder).
2. Find Edge: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` (fallback: `Program Files` variant).
3. Render:
   & "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="<abs path>.pdf" "file:///<abs path>.html"
   Note: --print-to-pdf needs ABSOLUTE paths. Open file:// URLs, not network drive letters directly.
4. Verify: @(Get-Item "<pdf>.pdf").Length -gt 10000 (a tiny file means the render fell back to error text), and optionally count pages by fetching pdf bytes and counting '/Type /Page' occurrences, or peek page 1 via --print-to-pdf of page-range HTML.

## HTML template (copy into report.html)
Baseline CSS that always renders cleanly through Edge:
- body { font-family: 'Segoe UI', Arial; color:#1a1a2e; margin:0; }
- .cover: full-page colored header block (title, date, subtitle), margin:0 0 24px
- section { padding:24px; } h2 { border-bottom:2px solid #4f46e5; padding-bottom:6px; }
- table { width:100%; border-collapse:collapse; } th{ background:#4f46e5;color:#fff } td{border-bottom:1px solid #e0e0e0; padding:8px}
- .badge { background:#fff;border:1px solid #cbd5e1;border-radius:999px;padding:2px 10px; font:12px } li{margin:6px 0}
- Use checklist: <li>✅ / ⚠ / ❌ prefix - prints fine in most PDF engines.
- Page breaks: <div style="page-break-before:always"></div> between major sections.

## Data flow into the report
- Pull REAL numbers from the source of truth (folder listing, log files, test output). Never hand-type counts - compute then interpolate with -f into the HTML.

## Word fallback (no Edge)
PowerShell COM: New-Object -ComObject Word.Application, open an .html or .docx, call SaveAs2([path], 17) (wdFormatPDF=17). Works without Edge; slower; needs MS Word installed.

## Anti-patterns
- Relative paths in --print-to-pdf → silently no output.
- Quoting: use single-quoted PS strings around paths with spaces inside & invocation.
- Report without verification = not delivered. Show page count + file size in the receipt.
