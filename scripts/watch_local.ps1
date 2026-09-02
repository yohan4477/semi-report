# 포트폴리오 워치 — 로컬 월간 갱신.
#
# 왜 로컬인가. 한국부동산원 R-ONE API 가 해외 IP 를 막는다 — GitHub 러너에서 두 번
# 돌려 두 번 다 연결이 끊기거나 타임아웃이었다(2026-09-02, run 33592254486). 그래서
# 받는 일은 한국에 있는 이 PC 가 하고, 알리는 일은 GitHub 워크플로(.github/workflows/
# watch.yml)가 _metrics 푸시에 반응해서 한다. 둘을 한 자리에 두면 둘 다 못 한다.
#
# 등록은 scripts/watch_local_register.ps1 이 한다(작업 스케줄러, 매달 20일 09:00,
# 놓치면 다음 켤 때). 손으로 돌릴 때는 저장소 어디서든 이 파일을 그냥 실행한다.
#
# 순서: 수치 받기 → 화면 재생성 → 워치 검사(FAIL 이면 커밋 안 함) → 바뀐 것만 커밋·푸시.
# 열쇠는 사용자 환경변수 REB_API_KEY 에 있다. 없으면 시작하지 않는다 — 열쇠 없이 돌면
# 앞 몇 건만 와서 값이 조용히 낡는다.

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$env:PYTHONIOENCODING = 'utf-8'
$log = Join-Path $repo 'insights\watch\_local.log'

function Say($s) {
    $line = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $s
    Write-Host $line
    Add-Content -Path $log -Value $line -Encoding utf8
}

if (-not $env:REB_API_KEY) {
    $u = [Environment]::GetEnvironmentVariable('REB_API_KEY', 'User')
    if ($u) { $env:REB_API_KEY = $u }
}
if (-not $env:REB_API_KEY) {
    Say '중단: REB_API_KEY 가 없다 — setx REB_API_KEY <값> 으로 심는다'
    exit 1
}

Say '시작'
git pull --ff-only --quiet
if ($LASTEXITCODE -ne 0) { Say '중단: git pull 실패'; exit 1 }

python insights/watch_fetch.py
if ($LASTEXITCODE -ne 0) { Say '중단: 수치 받기 실패 — _metrics 는 덮지 않았다'; exit 1 }

python scratchpad/gen_watch_page.py
if ($LASTEXITCODE -ne 0) { Say '중단: 화면 재생성 실패'; exit 1 }

$chk = python insights/check_watch.py 2>&1 | Out-String
if ($chk -notmatch 'FAIL 0') {
    Say '중단: check_watch FAIL — 커밋 안 함'
    Say $chk
    exit 1
}

$changed = git status --porcelain -- 'insights/watch/_metrics' '대시보드/포트폴리오 워치.html'
if (-not $changed) { Say '변화 없음'; exit 0 }

$today = Get-Date -Format 'yyyy-MM-dd'
git add -- 'insights/watch/_metrics' '대시보드/포트폴리오 워치.html'
git commit --quiet -m "chore(워치): 수치 갱신 — $today" -m "로컬 스케줄러(scripts/watch_local.ps1)가 받았다. 알림은 GitHub 워크플로가 이 푸시에 반응해 연다."
git push --quiet
if ($LASTEXITCODE -ne 0) { Say '중단: push 실패'; exit 1 }
Say "푸시 $(git rev-parse --short HEAD)"
