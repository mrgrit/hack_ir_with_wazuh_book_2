param([string]$InputDoc, [string]$OutputPdf)
$ErrorActionPreference = 'Stop'
$wordRender = New-Object -ComObject Word.Application
$wordRender.Visible = $false
$wordRender.DisplayAlerts = 0
try {
  $renderDoc = $wordRender.Documents.Open($InputDoc,$false,$true)
  $renderDoc.ExportAsFixedFormat($OutputPdf,17)
  Write-Output ('Pages: ' + $renderDoc.ComputeStatistics(2))
  $renderDoc.Close(0)
} finally { $wordRender.Quit() }
