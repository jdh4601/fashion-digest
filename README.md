# Fashion Digest

글로벌 패션 업계 기사 10개 + YouTube 영상 3개 + Runway 컬렉션 5개를 매일 자동으로 수집·분석하여 **한국어 + 영어 바이링구얼 뉴스레터**로 Gmail 발송하는 자동화 시스템.

---

## 개요

| 항목 | 내용 |
|------|------|
| 수집 매체 | WWD, Business of Fashion, Vogue Business, Bloomberg, FT, YouTube |
| 분석 내용 | 핵심 요약 · 업계 시사점 · 흥미 포인트 (한국어 + 영어) |
| 출력물 | 마크다운 · 웹 HTML · 이메일 HTML |
| 발송 시각 | 매일 **오전 9시 KST** (macOS launchd) |
| 발송 방식 | Gmail SMTP + 앱 비밀번호 |

---

## 디렉토리 구조

```
fashion-research/
├── output_md/                      # 마크다운 출력 (한국어)
│   └── YYYY-MM-DD-fashion-digest.md
├── output_html/                    # 웹 뷰어용 HTML (매거진 스타일)
│   └── YYYY-MM-DD-fashion-digest.html
├── output_email/                   # 이메일 발송용 HTML (바이링구얼)
│   └── YYYY-MM-DD-fashion-digest-email.html
├── scripts/
│   ├── fashion-digest-daily.py    # 자동화 메인 스크립트
│   └── .env.example               # Gmail 인증 정보 템플릿
├── logs/                           # 실행 로그 (gitignore)
│   ├── fashion-digest.log
│   └── launchd.log
├── Template.md                     # HTML 템플릿 정의
├── OPTIMIZATION_PLAN.md            # 병렬화 및 최적화 계획
├── .gitignore
└── README.md
```

---

## 동작 방식

```
매일 09:00 KST
    ↓
macOS launchd
    ↓
python3 scripts/fashion-digest-daily.py
    ↓
claude -p "패션 기사 찾아줘"  ← Claude Code fashion-digest 스킬 실행
    ↓
[Phase 1] 12개 소스 병렬 검색 (WWD·BoF·Bloomberg 등)
[Phase 2] 콘텐츠 선별 (기사 10개 · YouTube 3개 · Runway 5개)
[Phase 3] 병렬 분석 (WebFetch)
[Phase 4] 마크다운 저장
[Phase 5] 웹 HTML 생성 (패션 매거진 디자인)
[Phase 6] 영어 버전 생성
[Phase 7] 이메일 HTML 생성 (inline CSS, 바이링구얼)
    ↓
Gmail SMTP → 받은편지함
```

---

## 설치 및 설정

### 1. 사전 요구사항

- macOS (launchd 사용)
- Python 3.11+
- [Claude Code](https://claude.ai/code) CLI 설치 및 로그인
- Gmail 계정 + 2단계 인증 활성화

### 2. Gmail 앱 비밀번호 발급

1. [Google 계정 보안](https://myaccount.google.com/security) → **2단계 인증** 활성화
2. 보안 → **앱 비밀번호** → 앱: 메일 / 기기: Mac → 생성
3. 표시된 16자리 코드 복사

### 3. 환경 변수 설정

```bash
cp scripts/.env.example scripts/.env
```

`scripts/.env` 파일 편집:

```env
GMAIL_USER=your@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

### 4. launchd 등록 (최초 1회)

`com.fashiondigest.daily.plist` 파일을 생성하여 `~/Library/LaunchAgents/`에 저장:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fashiondigest.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/Developer/fashion-research/scripts/fashion-digest-daily.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/Developer/fashion-research/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/Developer/fashion-research/logs/launchd-error.log</string>
</dict>
</plist>
```

> **참고**: `YOUR_USERNAME`을 본인의 macOS 사용자명으로 변경하세요.

등록 명령어:

```bash
launchctl load ~/Library/LaunchAgents/com.fashiondigest.daily.plist
```

---

## 수동 실행 (테스트)

```bash
cd /path/to/fashion-research
python3 scripts/fashion-digest-daily.py
```

실행 시 `logs/fashion-digest.log`에 진행 상황이 기록됩니다.

---

## launchd 관리

```bash
# 등록 확인
launchctl list | grep fashiondigest

# 일시 중지
launchctl unload ~/Library/LaunchAgents/com.fashiondigest.daily.plist

# 재등록
launchctl load ~/Library/LaunchAgents/com.fashiondigest.daily.plist

# 로그 확인
tail -f logs/fashion-digest.log
tail -f logs/launchd.log
```

---

## Claude Code 스킬

이 프로젝트는 `~/.claude/skills/fashion-digest/` 스킬을 사용합니다.

### 스킬 설치

```bash
mkdir -p ~/.claude/skills/fashion-digest
cp .claude/commands/fashion-digest.md ~/.claude/skills/fashion-digest/SKILL.md
```

### Claude Code에서 직접 실행

```
패션 기사 찾아줘
```

또는 프로젝트 루트에서:

```bash
claude -p "패션 기사 찾아줘" --dangerously-skip-permissions
```

---

## 콘텐츠 구성

### 기사 (10개)
글로벌 패션 미디어에서 선별된 최신 기사
- 핵심 요약 (한/영)
- 업계 시사점 (한/영)
- 흥미로운 포인트 (한/영)

### YouTube (3개)
패션 관련 영상 콘텐츠
- 영상 제목 및 채널 정보
- 영상 요약 (한/영)

### Runway (5개)
최신 런웨이 컬렉션 하이라이트
- 브랜드 및 디자이너 정보
- 컬렉션 요약 (한/영)
- 비평가 반응 (한/영)
- 소셜 미디어 반응 (한/영)

---

## 템플릿 시스템

`Template.md` 파일에 HTML 템플릿과 변수 정의가 포함되어 있습니다:

- **Web HTML**: 패션 매거진 스타일의 다크 테마
- **Email HTML**: inline CSS가 적용된 이메일용 템플릿
- **Card Templates**: 기사/YouTube/Runway 카드 템플릿

---

## 이메일 예시

```
제목: 👗 Fashion Digest — 2026년 03월 10일 (March 10, 2026)

🇰🇷 오늘의 패션 이슈 10선
  1. LVMH 매출 부진 지속 — 럭셔리 무조건 성장의 시대 종말
  2. 구찌·펜디 크리에이티브 디렉터 교체 — 90년대 이후 최대 개편
  ...

🌍 Today's Fashion Digest — English Edition
  1. LVMH Sales Struggle Continues — The Era of Unconditional Luxury Growth Is Over
  2. Gucci & Fendi Creative Director Shakeup — Largest Reshuffle Since the 90s
  ...

▶ YouTube — 오늘의 패션 영상 3선
  ...

🏛 Runway — 이번 시즌 럭셔리 5선
  ...
```

---

## 주의사항

- `scripts/.env`는 절대 커밋하지 마세요 (`.gitignore`에 포함됨)
- Mac이 꺼져 있으면 launchd가 실행되지 않습니다 (다음 날 자동 재개)
- 패션 매체 대부분이 페이월 → 기사 본문 fetch 실패 시 검색 결과 기반으로 분석
- Claude Code CLI가 PATH에 등록되어 있어야 합니다

---

## 최적화 및 개선

`OPTIMIZATION_PLAN.md` 파일에서 병렬 처리 및 성능 최적화 계획을 확인할 수 있습니다:

- 병렬 WebFetch로 실행 시간 단축 (목표: 4배 속도 향상)
- Template 기반 파일 생성
- Fallback 콘텐츠 처리

---

## 라이선스

개인 사용 목적으로 작성된 프로젝트입니다.
