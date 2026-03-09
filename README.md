# Fashion Digest

글로벌 패션 업계 기사 10개를 매일 자동으로 수집·분석하여 **한국어 + 영어 바이링구얼 뉴스레터**로 Gmail 발송하는 자동화 시스템.

---

## 개요

| 항목 | 내용 |
|------|------|
| 수집 매체 | WWD, Business of Fashion, Vogue Business, Bloomberg, FT |
| 분석 내용 | 핵심 요약 · 업계 시사점 · 흥미 포인트 (한국어 + 영어) |
| 출력물 | 마크다운 · 웹 HTML · 이메일 HTML |
| 발송 시각 | 매일 **오전 9시 KST** (macOS launchd) |
| 발송 방식 | Gmail SMTP + 앱 비밀번호 |

---

## 디렉토리 구조

```
fashion-research/
├── fashion-research/               # 생성된 다이제스트 파일 저장
│   ├── YYYY-MM-DD-fashion-digest.md           # 마크다운 (한국어)
│   ├── YYYY-MM-DD-fashion-digest.html         # 웹 뷰어용 HTML (매거진풍)
│   └── YYYY-MM-DD-fashion-digest-email.html   # 이메일 발송용 HTML (바이링구얼)
├── scripts/
│   ├── fashion-digest-daily.py    # 자동화 메인 스크립트
│   └── .env.example               # Gmail 인증 정보 템플릿
├── logs/                           # 실행 로그 (gitignore)
│   ├── fashion-digest.log
│   └── launchd-error.log
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
[Phase 1] 6개 소스 병렬 검색 (WWD·BoF·Bloomberg 등)
[Phase 2] 기사 10개 선별 (최신성·다양성·흥미도)
[Phase 3] 각 기사 분석 (요약·시사점·흥미 포인트)
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

```bash
cp com.fashiondigest.daily.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.fashiondigest.daily.plist
```

> **참고**: plist 파일의 경로(`/Users/jayden/...`)를 본인 사용자명으로 수정 후 등록하세요.

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
```

---

## Claude Code 스킬

이 프로젝트는 `~/.claude/skills/fashion-digest/` 스킬을 사용합니다.
Claude Code 세션에서 직접 실행하려면:

```
패션 기사 찾아줘
```

---

## 이메일 예시

```
제목: 👗 Fashion Digest — 2026년 03월 09일 (March 09, 2026)

🇰🇷 오늘의 패션 이슈 10선
  1. LVMH 매출 부진 지속 — 럭셔리 무조건 성장의 시대 종말
  2. 구찌·펜디 크리에이티브 디렉터 교체 — 90년대 이후 최대 개편
  ...

🌍 Today's Fashion Digest — English Edition
  1. LVMH Sales Struggle Continues — The Era of Unconditional Luxury Growth Is Over
  2. Gucci & Fendi Creative Director Shakeup — Largest Reshuffle Since the 90s
  ...
```

---

## 주의사항

- `scripts/.env`는 절대 커밋하지 마세요 (`.gitignore`에 포함됨)
- Mac이 꺼져 있으면 launchd가 실행되지 않습니다 (다음 날 자동 재개)
- 패션 매체 대부분이 페이월 → 기사 본문 fetch 실패 시 검색 결과 기반으로 분석
