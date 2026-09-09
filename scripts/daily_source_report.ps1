# 매일 아침 소스별 미처리 신규를 세어 목록 장을 갱신하고 카카오톡으로 보낸다.
# 작업 스케줄러가 부른다. 로그는 scratchpad/daily_source_report.log.
$ErrorActionPreference = 'Continue'
$repo = 'C:\Users\y\semianalysis'
Set-Location $repo
$env:PYTHONIOENCODING = 'utf-8'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$log = Join-Path $repo 'scratchpad\daily_source_report.log'
"=== $(Get-Date -Format 'yyyy-MM-dd HH:mm')" | Out-File $log -Append -Encoding utf8

git pull --rebase --autostash --quiet 2>&1 | Out-File $log -Append -Encoding utf8

python scripts\count_new.py --kakao 2>&1 | Out-File $log -Append -Encoding utf8

# 목록 장이 바뀌었을 때만 올린다 — 폰에서 열리는 것은 GitHub Pages 쪽이다
git add '대시보드/소스 신규.html' 2>&1 | Out-File $log -Append -Encoding utf8
$staged = git diff --cached --name-only
if ($staged) {
  git commit -m "chore(소스 신규): 아침 갱신 $(Get-Date -Format 'yyyy-MM-dd')" 2>&1 | Out-File $log -Append -Encoding utf8
  git push origin main 2>&1 | Out-File $log -Append -Encoding utf8
} else {
  "변경 없음" | Out-File $log -Append -Encoding utf8
}
