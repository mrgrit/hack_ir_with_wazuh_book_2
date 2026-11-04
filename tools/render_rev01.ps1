param([string[]]$Stems=@())
$ErrorActionPreference='Stop'
$repoRoot=Split-Path -Parent $PSScriptRoot
$renderRoot=Join-Path $repoRoot 'build/REV01/render'
New-Item -ItemType Directory -Force -Path $renderRoot | Out-Null
if ($Stems.Count -eq 0) { $Stems=(1..13 | ForEach-Object {'chapter{0:d2}' -f $_})+@('appendix','references') }
Write-Output "Starting Word"
$renderWord=New-Object -ComObject Word.Application
$renderWord.Visible=$false
$renderWord.DisplayAlerts=0
$previousPrinter=$renderWord.ActivePrinter
$previousPrintBackground=$renderWord.Options.PrintBackground
try {
 $renderWord.ActivePrinter="Microsoft Print to PDF"
 $renderWord.Options.PrintBackground=$false
 foreach ($stem in $Stems) {
  $docFile=[IO.Path]::GetFullPath((Join-Path $repoRoot ('manuscript/REV01/volume02-'+$stem+'.docx')))
  $pdfFile=[IO.Path]::GetFullPath((Join-Path $renderRoot ($stem+'.pdf')))
  Write-Output ("Opening " + $stem)
  $renderDoc=$renderWord.Documents.Open($docFile,$false,$true)
  try {
   Write-Output ("Rendering " + $stem)
   # ExportAsFixedFormat performs pagination
   $renderDoc.ExportAsFixedFormat($pdfFile,17)
   Write-Output ($stem+': '+$renderDoc.ComputeStatistics(2)+' pages')
  } finally { $renderDoc.Close(0) }
 }
} finally {
 try {
  $renderWord.ActivePrinter=$previousPrinter
  $renderWord.Options.PrintBackground=$previousPrintBackground
 } finally { $renderWord.Quit() }
}
