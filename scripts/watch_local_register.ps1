# 포트폴리오 워치 — 로컬 월간 갱신을 작업 스케줄러에 건다.
#
# 매달 20일 09:00 에 scripts/watch_local.ps1 을 돌린다. 부동산원 월간 통계가 보름께 나온다.
# 그 시각에 PC 가 꺼져 있으면 다음 켤 때 바로 돈다(StartWhenAvailable). 배터리여도 돈다.
# 다시 실행하면 같은 이름의 작업을 덮어쓴다. 풀려면:
#   schtasks /Delete /TN "포트폴리오 워치 갱신" /F
#
# 만드는 건 schtasks 다 — PowerShell 5.1 의 New-ScheduledTaskTrigger 에는 월 단위가 없다.
# 놓쳤을 때 도는 설정은 만든 뒤 Set-ScheduledTask 로 얹는다.

$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot 'watch_local.ps1'
$name = '포트폴리오 워치 갱신'
$cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \`"$script\`""

schtasks /Create /TN $name /SC MONTHLY /D 20 /ST 09:00 /TR $cmd /F | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'schtasks /Create 실패' }

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30)
Set-ScheduledTask -TaskName $name -Settings $settings | Out-Null

$t = Get-ScheduledTask -TaskName $name
"등록됨: {0} · 상태 {1} · 다음 실행 {2}" -f $t.TaskName, $t.State, (Get-ScheduledTaskInfo -TaskName $name).NextRunTime
