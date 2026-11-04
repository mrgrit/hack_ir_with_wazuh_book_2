param()
$ErrorActionPreference='Stop'
$repoRoot=Split-Path -Parent $PSScriptRoot
$checked=@()
Push-Location -LiteralPath $repoRoot
try {
 $allowed=@('Test-Path','Get-Content','ConvertFrom-Json','Format-Table','Get-FileHash','Format-List','Where-Object','ForEach-Object','Select-Object')
 foreach($offlineId in @('CA-01','CA-02','CA-03','CA-04')) {
  $offlineText=Get-Content (Join-Path 'examples/rev01/appendix' ($offlineId+'.txt')) -Raw -Encoding UTF8
  $tokens=$null; $parseErrors=$null
  $ast=[System.Management.Automation.Language.Parser]::ParseInput($offlineText,[ref]$tokens,[ref]$parseErrors)
  if($parseErrors.Count){throw ('Parse error: '+$offlineId)}
  $calls=$ast.FindAll({param($n) $n -is [System.Management.Automation.Language.CommandAst]},$true)
  foreach($call in $calls){if($call.GetCommandName() -notin $allowed){throw 'Unexpected command'}}
  . ([scriptblock]::Create($offlineText)) | Out-Null
  if($offlineId -eq 'CA-03') {
   $login=@($case.records | Where-Object { $_.data.win.system.eventRecordID -eq '9115' })
   if($login.Count -ne 1 -or $login[0].rule.id -ne '60200' -or $login[0].data.win.eventdata.logonType -ne '8' -or $login[0].data.win.eventdata.processName -notlike '*sshd.exe') { throw 'Record 9115 mismatch' }
  }
  $checked+=$offlineId
  Write-Output ($offlineId+' local read: PASS')
 }
 $archives=$bundle.cases | Where-Object case -eq 'ch06-original-archives'
 $alerts=$bundle.cases | Where-Object case -eq 'ch06-original-alerts'
 if($archives.total.value -ne 6 -or $archives.returned -ne 6 -or $alerts.total.value -ne 0){throw 'Count mismatch'}
 $ids=@($archives.records | ForEach-Object {$_.system.eventRecordID} | Sort-Object)
 if(($ids -join ',') -ne '9407,9451,9454,9455,9461,9462'){throw 'Record mismatch'}
 foreach($entry in $manifest.files){
  $actual=(Get-FileHash (Join-Path 'examples/rev01/records' $entry.file) -Algorithm SHA256).Hash
  if($actual -ne $entry.sha256){throw 'Hash mismatch'}
 }
 Write-Output 'All provided record hashes and chapter06 expected values: PASS'
 $result=[ordered]@{scope='local saved files only';inputs=$checked;record9115='60200 / type 8 / sshd.exe';chapter06=[ordered]@{archives=6;alerts=0;recordIds=$ids};hashesChecked=@($manifest.files).Count;result='PASS'}
 $result | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath 'editorial/REV01/offline-check.json' -Encoding UTF8
}
finally { Pop-Location }
