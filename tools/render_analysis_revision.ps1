param([string[]]$Stems = @())
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$renderRoot = Join-Path $repoRoot 'build/analysis-revision/render'
New-Item -ItemType Directory -Force -Path $renderRoot | Out-Null
if ($Stems.Count -eq 0) { $Stems = (1..13 | ForEach-Object { 'chapter{0:d2}' -f $_ }) + @('appendix') }
$renderWord = New-Object -ComObject Word.Application
$renderWord.Visible = $false
$renderWord.DisplayAlerts = 0
try {
 foreach ($stem in $Stems) {
  $docFile = Join-Path $repoRoot ('manuscript/volume02-' + $stem + '.docx')
  $pdfFile = Join-Path $renderRoot ($stem + '.pdf')
  $renderDoc = $renderWord.Documents.Open($docFile,$false,$true)
  try {
   $renderDoc.ExportAsFixedFormat($pdfFile,17)
   Write-Output ($stem + ': ' + $renderDoc.ComputeStatistics(2) + ' pages')
  } finally { $renderDoc.Close(0) }
 }
} finally { $renderWord.Quit() }
