# Fashion Digest Optimization Plan

> 병렬 처리와 템플릿 기반 아키텍처로 실행 속도 3배 향상

---

## 1. 병렬화 전략 (Parallelization Strategy)

### 1.1 Current Sequential Bottlenecks

현재 SKILL.md의 순차적 실행 문제점:
- Phase 3: 기사 10개 WebFetch → 순차 실행 시 10×2초 = 20초 소요
- Phase 5: og:image 10개 fetch → 추가 10×1초 = 10초 소요
- Phase 6: 영어 번역 → 한국어 완료 후에만 시작

### 1.2 Proposed Parallel Architecture

```
Phase 1: 병렬 검색 (12 sources) ─────────────────────────┐
                                                          ▼
Phase 2: 기사 선별 (10개) ────────────────────────────────┤
                                                          ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 3: 기사 분석 (10개 병렬 WebFetch)                │
│  ├─ Article 1 WebFetch ──┐                              │
│  ├─ Article 2 WebFetch ──┤                              │
│  ├─ Article 3 WebFetch ──┤  All in parallel             │
│  ├─ ... (7 more) ────────┤  (background=true)           │
│  └─ Article 10 WebFetch ─┘                              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 4: 데이터 추출 (병렬)                            │
│  ├─ YouTube 3개 metadata ──┬── Parallel ──┐            │
│  ├─ Runway 5개 data ───────┤              │            │
│  └─ og:image 10개 fetch ───┘              │            │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 5: 파일 생성 (병렬)                              │
│  ├─ Markdown 생성 ──────┐                                │
│  ├─ HTML Web 생성 ──────┼── Parallel (no dependencies)   │
│  ├─ HTML Email 생성 ────┤                                │
│  └─ English content ────┘                                │
└─────────────────────────────────────────────────────────┘
```

### 1.3 Implementation: Background Task Pattern

```typescript
// Phase 3: Article Analysis - All 10 in parallel
const articleTasks = selectedArticles.map((article, index) => 
  task({
    category: "quick",
    load_skills: [],
    run_in_background: true,  // 🔑 KEY: Parallel execution
    description: `Analyze article ${index + 1}`,
    prompt: `
      TASK: Fetch and analyze article content
      URL: ${article.url}
      REQUIRED OUTPUT:
      - summary: 3-4 lines Korean
      - implications: 2-3 lines Korean  
      - highlight: 1 line Korean
      
      MUST DO:
      - Use WebFetch to get full article content
      - Extract og:image URL
      - Return structured data only
      
      MUST NOT DO:
      - Do not save files
      - Do not generate HTML
    `
  })
);

// Collect all results
const articleResults = await Promise.all(
  articleTasks.map(t => background_output({ task_id: t.session_id, block: true }))
);
```

### 1.4 Critical Path Analysis

| Phase | Can Parallelize | Dependencies | Est. Time |
|-------|----------------|--------------|-----------|
| 1. Search (12 sources) | ✅ Already parallel | None | 3-5s |
| 2. Curation | ❌ Sequential | Phase 1 | 1s |
| 3. Article Analysis | ✅ 10 parallel | Phase 2 | 3-5s (was 20s) |
| 4. YouTube/Runway Fetch | ✅ 8 parallel | Phase 2 | 3-5s |
| 5. og:image Fetch | ✅ 10 parallel | Phase 3 | 2-3s (was 10s) |
| 6. File Generation | ✅ 3 parallel | Phase 3,4,5 | 1-2s |

**Total estimated time**: ~15s vs current ~60s (4x speedup)

---

## 2. Template.md Architecture

### 2.1 File Location
```
/Users/jayden/Developer/fashion-research/
├── Template.md                    # ← Main template file
├── output_md/
├── output_html/
└── output_email/
```

### 2.2 Template Structure

Template.md는 3개의 주요 섹션으로 구성:

#### Section 1: Variables Definition
```markdown
---
# Fashion Digest Template Variables
# 이 섹션은 실제 출력에 포함되지 않음
---

## Date Variables
- {{DATE_KR}}: "2026년 3월 10일"
- {{DATE_EN}}: "March 10, 2026"
- {{DATE_ISO}}: "2026-03-10"

## Article Variables (1-10)
- {{ARTICLE_1_TITLE}}, {{ARTICLE_1_URL}}, {{ARTICLE_1_SOURCE}}
- {{ARTICLE_1_DATE}}, {{ARTICLE_1_CATEGORY}}
- {{ARTICLE_1_SUMMARY_KR}}, {{ARTICLE_1_INSIGHT_KR}}, {{ARTICLE_1_HIGHLIGHT_KR}}
- {{ARTICLE_1_SUMMARY_EN}}, {{ARTICLE_1_INSIGHT_EN}}, {{ARTICLE_1_HIGHLIGHT_EN}}
- {{ARTICLE_1_THUMB}}, {{ARTICLE_1_FALLBACK}}

## YouTube Variables (1-3)
- {{YT_1_TITLE}}, {{YT_1_URL}}, {{YT_1_VIDEO_ID}}
- {{YT_1_CHANNEL}}, {{YT_1_DATE}}, {{YT_1_CATEGORY}}
- {{YT_1_SUMMARY_KR}}, {{YT_1_SUMMARY_EN}}
- {{YT_1_THUMB}} (auto: https://img.youtube.com/vi/{VIDEO_ID}/maxresdefault.jpg)

## Runway Variables (1-5)
- {{RW_1_BRAND}}, {{RW_1_DESIGNER}}, {{RW_1_DATE}}, {{RW_1_VENUE}}
- {{RW_1_SUMMARY_KR}}, {{RW_1_SUMMARY_EN}}
- {{RW_1_CRITIC_KR}}, {{RW_1_CRITIC_EN}}, {{RW_1_CRITIC_SOURCE}}
- {{RW_1_SOCIAL_KR}}, {{RW_1_SOCIAL_EN}}
- {{RW_1_THUMB}}, {{RW_1_FALLBACK}}
```

#### Section 2: Web HTML Template
```html
<!-- TEMPLATE: WEB_HTML -->
<!-- FILE: {{DATE_ISO}}-fashion-digest.html -->

<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fashion Digest — {{DATE_ISO}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    /* CSS Variables for theming */
    :root {
      --bg-primary: #0a0a0a;
      --bg-card: #111;
      --text-primary: #fff;
      --text-secondary: #e8e8e8;
      --text-muted: #bbb;
      --accent-gold: #c9a96e;
      --accent-yt: #ff6b6b;
      --border: #2a2a2a;
    }
    
    /* Base styles */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      background: var(--bg-primary); 
      color: var(--text-secondary); 
      font-family: 'Inter', sans-serif; 
    }
    
    /* Header */
    header { 
      text-align: center; 
      padding: 80px 20px 60px; 
      border-bottom: 1px solid var(--border); 
    }
    header h1 { 
      font-family: 'Playfair Display', serif; 
      font-size: clamp(2.5rem, 6vw, 5rem); 
      color: var(--text-primary); 
      letter-spacing: 0.05em; 
    }
    header .date { 
      color: var(--accent-gold); 
      font-size: 0.85rem; 
      letter-spacing: 0.2em; 
      text-transform: uppercase; 
      margin-top: 12px; 
    }
    
    /* Grid */
    .grid { 
      display: grid; 
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); 
      gap: 2px; 
      padding: 2px; 
      max-width: 1400px; 
      margin: 40px auto; 
    }
    
    /* Card */
    .card { 
      background: var(--bg-card); 
      overflow: hidden; 
      transition: transform 0.3s; 
    }
    .card:hover { transform: translateY(-4px); }
    .card img { 
      width: 100%; 
      height: 220px; 
      object-fit: cover; 
      filter: brightness(0.85); 
    }
    .card-body { padding: 24px; }
    .card-number { 
      font-family: 'Playfair Display', serif; 
      font-size: 0.8rem; 
      color: var(--accent-gold); 
      margin-bottom: 8px; 
    }
    .card-meta { 
      display: flex; 
      gap: 12px; 
      margin-bottom: 12px; 
      font-size: 0.75rem; 
      color: #888; 
      letter-spacing: 0.1em; 
      text-transform: uppercase; 
    }
    .card-meta .source { color: var(--accent-gold); }
    .card h2 { 
      font-family: 'Playfair Display', serif; 
      font-size: 1.2rem; 
      line-height: 1.5; 
      color: var(--text-primary); 
      margin-bottom: 16px; 
    }
    .card h2 a { color: inherit; text-decoration: none; }
    .card h2 a:hover { color: var(--accent-gold); }
    .category { 
      display: inline-block; 
      font-size: 0.7rem; 
      padding: 3px 10px; 
      border: 1px solid rgba(201,169,110,0.2); 
      color: var(--accent-gold); 
      letter-spacing: 0.1em; 
      margin-bottom: 14px; 
    }
    .section-title { 
      font-size: 0.7rem; 
      color: #555; 
      letter-spacing: 0.15em; 
      text-transform: uppercase; 
      margin-bottom: 6px; 
    }
    .summary { 
      font-size: 0.88rem; 
      line-height: 1.7; 
      color: var(--text-muted); 
      margin-bottom: 16px; 
    }
    .insight { 
      font-size: 0.85rem; 
      line-height: 1.6; 
      color: #999; 
      border-left: 2px solid var(--accent-gold); 
      padding-left: 12px; 
      margin-bottom: 14px; 
    }
    .highlight { 
      font-size: 0.8rem; 
      color: var(--accent-gold); 
      font-style: italic; 
    }
    
    /* YouTube Section */
    .yt-section { 
      max-width: 1400px; 
      margin: 60px auto 40px; 
      padding: 0 2px; 
    }
    .yt-section-title { 
      font-family: 'Playfair Display', serif; 
      font-size: 1.8rem; 
      color: var(--text-primary); 
      padding: 0 20px 20px; 
      border-bottom: 1px solid var(--border); 
      margin-bottom: 32px; 
    }
    .yt-section-title span { color: var(--accent-gold); }
    .yt-grid { 
      display: grid; 
      grid-template-columns: repeat(3, 1fr); 
      gap: 2px; 
    }
    .yt-card { background: var(--bg-card); overflow: hidden; }
    .yt-card:hover .yt-thumb-wrap img { transform: scale(1.03); }
    .yt-thumb-wrap { position: relative; overflow: hidden; }
    .yt-thumb-wrap img { 
      width: 100%; 
      height: 200px; 
      object-fit: cover; 
      filter: brightness(0.8); 
      transition: transform 0.4s; 
    }
    .yt-play-badge { 
      position: absolute; 
      top: 50%; 
      left: 50%; 
      transform: translate(-50%, -50%); 
      width: 52px; 
      height: 52px; 
      background: rgba(255,0,0,0.85); 
      border-radius: 50%; 
      display: flex; 
      align-items: center; 
      justify-content: center; 
      pointer-events: none; 
    }
    .yt-play-badge::after { 
      content: ''; 
      border: 0 solid transparent; 
      border-top: 10px solid transparent; 
      border-bottom: 10px solid transparent; 
      border-left: 18px solid #fff; 
      margin-left: 4px; 
    }
    .yt-card-body { padding: 24px; }
    .yt-meta { 
      display: flex; 
      gap: 10px; 
      font-size: 0.75rem; 
      color: #888; 
      letter-spacing: 0.1em; 
      text-transform: uppercase; 
      margin-bottom: 10px; 
    }
    .yt-meta .yt-channel { color: var(--accent-gold); }
    .yt-category { 
      display: inline-block; 
      font-size: 0.7rem; 
      padding: 3px 10px; 
      border: 1px solid rgba(255,107,107,0.4); 
      color: var(--accent-yt); 
      letter-spacing: 0.1em; 
      margin-bottom: 14px; 
    }
    .yt-card h3 { 
      font-family: 'Playfair Display', serif; 
      font-size: 1.1rem; 
      line-height: 1.5; 
      color: var(--text-primary); 
      margin-bottom: 14px; 
    }
    .yt-card h3 a { color: inherit; text-decoration: none; }
    .yt-card h3 a:hover { color: var(--accent-gold); }
    .yt-summary { 
      font-size: 0.88rem; 
      line-height: 1.7; 
      color: var(--text-muted); 
    }
    
    /* Runway Section */
    .runway-section { 
      max-width: 1400px; 
      margin: 60px auto 40px; 
      padding: 0 2px; 
    }
    .runway-section-title { 
      font-family: 'Playfair Display', serif; 
      font-size: 1.8rem; 
      color: var(--text-primary); 
      padding: 0 20px 20px; 
      border-bottom: 1px solid var(--border); 
      margin-bottom: 32px; 
    }
    .runway-section-title span { color: var(--accent-gold); }
    .runway-grid { 
      display: grid; 
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); 
      gap: 2px; 
    }
    .runway-card { 
      background: var(--bg-card); 
      overflow: hidden; 
      transition: transform 0.3s; 
    }
    .runway-card:hover { transform: translateY(-4px); }
    .runway-card img { 
      width: 100%; 
      height: 280px; 
      object-fit: cover; 
      filter: brightness(0.8); 
      transition: filter 0.3s; 
    }
    .runway-card:hover img { filter: brightness(1); }
    .runway-card-body { padding: 22px; }
    .runway-brand { 
      font-family: 'Playfair Display', serif; 
      font-size: 1.2rem; 
      color: var(--text-primary); 
      margin-bottom: 4px; 
    }
    .runway-meta { 
      font-size: 0.75rem; 
      color: #888; 
      letter-spacing: 0.1em; 
      text-transform: uppercase; 
      margin-bottom: 12px; 
    }
    .runway-meta .rw-designer { color: var(--accent-gold); }
    .runway-summary { 
      font-size: 0.88rem; 
      line-height: 1.7; 
      color: var(--text-muted); 
      margin-bottom: 14px; 
    }
    .runway-reactions { 
      border-top: 1px solid #1e1e1e; 
      padding-top: 14px; 
    }
    .reaction-label { 
      font-size: 0.7rem; 
      color: #555; 
      letter-spacing: 0.15em; 
      text-transform: uppercase; 
      margin-bottom: 4px; 
    }
    .critic-reaction { 
      font-size: 0.85rem; 
      line-height: 1.6; 
      color: #999; 
      border-left: 2px solid var(--accent-gold); 
      padding-left: 10px; 
      margin-bottom: 10px; 
    }
    .social-reaction { 
      font-size: 0.82rem; 
      line-height: 1.6; 
      color: #888; 
      font-style: italic; 
    }
    
    /* Footer */
    footer { 
      text-align: center; 
      padding: 40px; 
      color: #333; 
      font-size: 0.75rem; 
      letter-spacing: 0.1em; 
    }
  </style>
</head>
<body>
  <header>
    <div class="date">{{DATE_KR}}</div>
    <h1>Fashion Digest</h1>
    <div class="subtitle">오늘의 글로벌 패션 이슈 10선</div>
  </header>

  <main class="grid">
    {{ARTICLE_CARDS}}
  </main>

  <section class="yt-section">
    <h2 class="yt-section-title">YouTube — <span>오늘의 패션 영상 3선</span></h2>
    <div class="yt-grid">
      {{YOUTUBE_CARDS}}
    </div>
  </section>

  <section class="runway-section">
    <h2 class="runway-section-title">Runway — <span>이번 시즌 럭셔리 5선</span></h2>
    <div class="runway-grid">
      {{RUNWAY_CARDS}}
    </div>
  </section>

  <footer>Generated by fashion-digest skill · {{DATE_ISO}}</footer>
</body>
</html>

<!-- CARD TEMPLATES -->

<!-- Article Card Template -->
{{ARTICLE_CARD_TEMPLATE}}
<article class="card">
  <img src="{{THUMB}}" alt="{{TITLE}}" onerror="this.src='{{FALLBACK}}'">
  <div class="card-body">
    <div class="card-number">No. {{NUMBER}}</div>
    <div class="card-meta">
      <span class="source">{{SOURCE}}</span>
      <span>{{DATE}}</span>
    </div>
    <span class="category">{{CATEGORY}}</span>
    <h2><a href="{{URL}}" target="_blank">{{TITLE}}</a></h2>
    <div class="section-title">핵심 요약</div>
    <p class="summary">{{SUMMARY}}</p>
    <div class="section-title">시사점</div>
    <p class="insight">{{INSIGHT}}</p>
    <p class="highlight">✦ {{HIGHLIGHT}}</p>
  </div>
</article>
{{/ARTICLE_CARD_TEMPLATE}}

<!-- YouTube Card Template -->
{{YOUTUBE_CARD_TEMPLATE}}
<article class="yt-card">
  <div class="yt-thumb-wrap">
    <img src="https://img.youtube.com/vi/{{VIDEO_ID}}/maxresdefault.jpg" alt="{{TITLE}}">
    <a href="{{URL}}" target="_blank"><div class="yt-play-badge"></div></a>
  </div>
  <div class="yt-card-body">
    <div class="yt-meta">
      <span class="yt-channel">{{CHANNEL}}</span>
      <span>{{DATE}}</span>
    </div>
    <span class="yt-category">{{CATEGORY}}</span>
    <h3><a href="{{URL}}" target="_blank">{{TITLE}}</a></h3>
    <p class="yt-summary">{{SUMMARY}}</p>
  </div>
</article>
{{/YOUTUBE_CARD_TEMPLATE}}

<!-- Runway Card Template -->
{{RUNWAY_CARD_TEMPLATE}}
<article class="runway-card">
  <img src="{{THUMB}}" alt="{{BRAND}}" onerror="this.src='{{FALLBACK}}'">
  <div class="runway-card-body">
    <div class="runway-brand">{{BRAND}}</div>
    <div class="runway-meta">
      <span class="rw-designer">{{DESIGNER}}</span> &nbsp;·&nbsp; {{DATE}} &nbsp;·&nbsp; {{VENUE}}
    </div>
    <p class="runway-summary">{{SUMMARY}}</p>
    <div class="runway-reactions">
      <div class="reaction-label">비평가 반응</div>
      <p class="critic-reaction">{{CRITIC}}</p>
      <div class="reaction-label">대중/소셜 반응</div>
      <p class="social-reaction">{{SOCIAL}}</p>
    </div>
  </div>
</article>
{{/RUNWAY_CARD_TEMPLATE}}
```

#### Section 3: Email HTML Template
```html
<!-- TEMPLATE: EMAIL_HTML -->
<!-- FILE: {{DATE_ISO}}-fashion-digest-email.html -->

<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fashion Digest — {{DATE_ISO}}</title>
</head>
<body style="margin:0;padding:0;background:#0a0a0a;">
<table width="100%" cellpadding="0" cellspacing="0">
  <tr><td align="center" style="padding:40px 20px;">
    <table width="600" cellpadding="0" cellspacing="0">
      
      <!-- Header -->
      <tr><td style="text-align:center;padding:40px 0 30px;border-bottom:1px solid #2a2a2a;">
        <p style="margin:0 0 8px;font-size:11px;color:#c9a96e;letter-spacing:3px;text-transform:uppercase;font-family:Arial,sans-serif;">{{DATE_KR}}</p>
        <h1 style="margin:0;font-size:36px;color:#ffffff;font-family:Georgia,serif;letter-spacing:3px;">Fashion Digest</h1>
      </td></tr>
      
      <!-- Korean Section -->
      <tr><td style="padding:32px 0 8px;">
        <p style="margin:0 0 24px;font-size:13px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">🇰🇷 오늘의 패션 이슈 10선</p>
        {{KOREAN_ARTICLE_CARDS}}
      </td></tr>
      
      <!-- Divider -->
      <tr><td style="padding:20px 0;">
        <hr style="border:none;border-top:1px solid #2a2a2a;">
      </td></tr>
      
      <!-- English Section -->
      <tr><td style="padding:8px 0;">
        <p style="margin:0 0 24px;font-size:13px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">🌍 Today's Fashion Digest — English Edition</p>
        {{ENGLISH_ARTICLE_CARDS}}
      </td></tr>
      
      <!-- Divider -->
      <tr><td style="padding:20px 0;"><hr style="border:none;border-top:1px solid #2a2a2a;"></td></tr>
      
      <!-- YouTube Korean -->
      <tr><td style="padding:8px 0;">
        <p style="margin:0 0 20px;font-size:13px;color:#ff6b6b;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">&#9654; YouTube — 오늘의 패션 영상 3선</p>
        {{KOREAN_YOUTUBE_CARDS}}
      </td></tr>
      
      <!-- Divider -->
      <tr><td style="padding:20px 0;"><hr style="border:none;border-top:1px solid #1a1a1a;"></td></tr>
      
      <!-- YouTube English -->
      <tr><td style="padding:8px 0;">
        <p style="margin:0 0 20px;font-size:13px;color:#ff6b6b;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">&#9654; YouTube — Today's Fashion Videos</p>
        {{ENGLISH_YOUTUBE_CARDS}}
      </td></tr>
      
      <!-- Divider -->
      <tr><td style="padding:20px 0;"><hr style="border:none;border-top:1px solid #1a1a1a;"></td></tr>
      
      <!-- Runway Korean -->
      <tr><td style="padding:8px 0;">
        <p style="margin:0 0 20px;font-size:13px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">&#127963; Runway &#8212; 이번 시즌 럭셔리 5선</p>
        {{KOREAN_RUNWAY_CARDS}}
      </td></tr>
      
      <!-- Divider -->
      <tr><td style="padding:20px 0;"><hr style="border:none;border-top:1px solid #1a1a1a;"></td></tr>
      
      <!-- Runway English -->
      <tr><td style="padding:8px 0;">
        <p style="margin:0 0 20px;font-size:13px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">&#127963; Runway &#8212; Season's Luxury Highlights</p>
        {{ENGLISH_RUNWAY_CARDS}}
      </td></tr>
      
      <!-- Footer -->
      <tr><td style="text-align:center;padding:32px 0;border-top:1px solid #1a1a1a;">
        <p style="margin:0;font-size:11px;color:#333333;font-family:Arial,sans-serif;">Generated by fashion-digest skill · {{DATE_ISO}}</p>
      </td></tr>
      
    </table>
  </td></tr>
</table>
</body>
</html>

<!-- Email Card Templates (Inline CSS) -->
{{EMAIL_ARTICLE_CARD_TEMPLATE_KR}}
<table width="560" cellpadding="0" cellspacing="0" style="margin:0 auto 24px;background:#111111;border-radius:4px;overflow:hidden;">
  <tr><td>
    <img src="{{THUMB}}" width="560" height="200" style="display:block;width:100%;height:200px;object-fit:cover;" alt="{{TITLE}}" onerror="this.src='{{FALLBACK}}'">
  </td></tr>
  <tr><td style="padding:20px 24px;">
    <p style="margin:0 0 6px;font-size:11px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">{{SOURCE}} · {{DATE}}</p>
    <span style="display:inline-block;margin:0 0 10px;padding:2px 8px;border:1px solid #c9a96e44;color:#c9a96e;font-size:10px;letter-spacing:1px;font-family:Arial,sans-serif;">{{CATEGORY}}</span>
    <h3 style="margin:0 0 14px;font-size:17px;line-height:1.5;color:#ffffff;font-family:Georgia,serif;">
      <a href="{{URL}}" style="color:#ffffff;text-decoration:none;">{{TITLE}}</a>
    </h3>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">핵심 요약</p>
    <p style="margin:0 0 14px;font-size:14px;line-height:1.7;color:#bbbbbb;font-family:Arial,sans-serif;">{{SUMMARY}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">시사점</p>
    <p style="margin:0 0 12px;font-size:13px;line-height:1.6;color:#999999;padding-left:10px;border-left:2px solid #c9a96e;font-family:Arial,sans-serif;">{{INSIGHT}}</p>
    <p style="margin:0;font-size:12px;color:#c9a96e;font-style:italic;font-family:Georgia,serif;">✦ {{HIGHLIGHT}}</p>
  </td></tr>
</table>
{{/EMAIL_ARTICLE_CARD_TEMPLATE_KR}}

{{EMAIL_YOUTUBE_CARD_TEMPLATE_KR}}
<table width="560" cellpadding="0" cellspacing="0" style="margin:0 auto 20px;background:#111111;border-radius:4px;overflow:hidden;">
  <tr><td>
    <a href="{{URL}}" style="display:block;">
      <img src="https://img.youtube.com/vi/{{VIDEO_ID}}/maxresdefault.jpg" width="560" height="210" style="display:block;width:100%;height:210px;object-fit:cover;" alt="{{TITLE}}">
    </a>
  </td></tr>
  <tr><td style="padding:4px 20px 4px;background:#1a0000;">
    <p style="margin:0;font-size:10px;color:#ff6b6b;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">&#9654; YouTube</p>
  </td></tr>
  <tr><td style="padding:12px 20px 20px;background:#111111;">
    <p style="margin:0 0 6px;font-size:11px;color:#c9a96e;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">{{CHANNEL}} · {{DATE}}</p>
    <span style="display:inline-block;margin:0 0 10px;padding:2px 8px;border:1px solid rgba(255,107,107,0.4);color:#ff6b6b;font-size:10px;letter-spacing:1px;font-family:Arial,sans-serif;">{{CATEGORY}}</span>
    <h3 style="margin:0 0 12px;font-size:16px;line-height:1.5;color:#ffffff;font-family:Georgia,serif;">
      <a href="{{URL}}" style="color:#ffffff;text-decoration:none;">{{TITLE}}</a>
    </h3>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">영상 요약</p>
    <p style="margin:0;font-size:14px;line-height:1.7;color:#bbbbbb;font-family:Arial,sans-serif;">{{SUMMARY}}</p>
  </td></tr>
</table>
{{/EMAIL_YOUTUBE_CARD_TEMPLATE_KR}}

{{EMAIL_RUNWAY_CARD_TEMPLATE_KR}}
<table width="560" cellpadding="0" cellspacing="0" style="margin:0 auto 20px;background:#111111;border-radius:4px;overflow:hidden;">
  <tr><td>
    <img src="{{THUMB}}" width="560" height="240" style="display:block;width:100%;height:240px;object-fit:cover;" alt="{{BRAND}}" onerror="this.src='{{FALLBACK}}'">
  </td></tr>
  <tr><td style="padding:4px 20px;background:#0d0d1a;">
    <p style="margin:0;font-size:10px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">&#127963; RUNWAY</p>
  </td></tr>
  <tr><td style="padding:14px 20px 20px;background:#111111;">
    <h3 style="margin:0 0 4px;font-size:19px;color:#ffffff;font-family:Georgia,serif;">{{BRAND}}</h3>
    <p style="margin:0 0 12px;font-size:11px;color:#c9a96e;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">{{DESIGNER}} · {{DATE}} · {{VENUE}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">컬렉션 요약</p>
    <p style="margin:0 0 14px;font-size:14px;line-height:1.7;color:#bbbbbb;font-family:Arial,sans-serif;">{{SUMMARY}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">비평가 반응</p>
    <p style="margin:0 0 12px;font-size:13px;line-height:1.6;color:#999999;padding-left:10px;border-left:2px solid #c9a96e;font-family:Arial,sans-serif;">{{CRITIC}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">대중/소셜 반응</p>
    <p style="margin:0;font-size:13px;line-height:1.6;color:#888888;font-style:italic;font-family:Georgia,serif;">{{SOCIAL}}</p>
  </td></tr>
</table>
{{/EMAIL_RUNWAY_CARD_TEMPLATE_KR}}
```

### 2.4 Variable Substitution Logic

```typescript
// Template processing flow
interface TemplateData {
  // Date
  DATE_ISO: string;
  DATE_KR: string;
  DATE_EN: string;
  
  // Articles array
  articles: ArticleData[];
  
  // YouTube array
  youtube: YouTubeData[];
  
  // Runway array
  runway: RunwayData[];
}

// Step 1: Generate card HTML for each item
const articleCardsKR = articles.map((a, i) => 
  generateArticleCard(a, i + 1, 'kr')
).join('\n');

const articleCardsEN = articles.map((a, i) => 
  generateArticleCard(a, i + 1, 'en')
).join('\n');

// Step 2: Replace placeholders in template
let html = template
  .replace(/{{DATE_ISO}}/g, dateISO)
  .replace(/{{DATE_KR}}/g, dateKR)
  .replace(/{{ARTICLE_CARDS}}/g, articleCardsKR)
  .replace(/{{YOUTUBE_CARDS}}/g, youtubeCards)
  .replace(/{{RUNWAY_CARDS}}/g, runwayCards);

// Step 3: Write to file
writeFile(`output_html/${dateISO}-fashion-digest.html`, html);
```

---

## 3. Optimized Workflow (Step-by-Step)

### Phase 1: Search (No Change)
```
┌─────────────────────────────────────────────────────┐
│  12 Parallel WebSearch calls                        │
│  (Already parallel in current skill)               │
└─────────────────────────────────────────────────────┘
```

### Phase 2: Curation & Selection
```
┌─────────────────────────────────────────────────────┐
│  Select: 10 articles + 3 YouTube + 5 Runway        │
│  (Sequential - requires human-like judgment)       │
└─────────────────────────────────────────────────────┘
```

### Phase 3: Parallel Content Fetching
```
┌────────────────────────────────────────────────────────────┐
│  PARALLEL BATCH A: Article Content (10 concurrent)         │
│  ├─ task_01: WebFetch Article 1 → Extract summary         │
│  ├─ task_02: WebFetch Article 2 → Extract summary         │
│  ├─ ...                                                   │
│  └─ task_10: WebFetch Article 10 → Extract summary        │
│                                                            │
│  PARALLEL BATCH B: YouTube Metadata (3 concurrent)         │
│  ├─ task_yt1: WebFetch YouTube 1 → Extract metadata       │
│  ├─ task_yt2: WebFetch YouTube 2 → Extract metadata       │
│  └─ task_yt3: WebFetch YouTube 3 → Extract metadata       │
│                                                            │
│  PARALLEL BATCH C: Runway Data (5 concurrent)              │
│  ├─ task_rw1: WebFetch Runway 1 → Extract review          │
│  ├─ task_rw2: WebFetch Runway 2 → Extract review          │
│  ├─ ...                                                   │
│  └─ task_rw5: WebFetch Runway 5 → Extract review          │
└────────────────────────────────────────────────────────────┘
```

### Phase 4: Parallel Image Fetching
```
┌────────────────────────────────────────────────────────────┐
│  PARALLEL: Thumbnail Extraction (10 concurrent)            │
│  ├─ WebFetch Article 1 URL → Extract og:image             │
│  ├─ WebFetch Article 2 URL → Extract og:image             │
│  ├─ ...                                                   │
│  └─ WebFetch Article 10 URL → Extract og:image            │
│                                                            │
│  (Runway images extracted in Phase 3C)                    │
└────────────────────────────────────────────────────────────┘
```

### Phase 5: Parallel File Generation
```
┌────────────────────────────────────────────────────────────┐
│  PARALLEL: Generate Output Files (3 concurrent)            │
│  ├─ task_md: Generate Markdown (Korean only)              │
│  ├─ task_html: Generate Web HTML (Korean only)            │
│  ├─ task_html_en: Generate Web HTML with English          │
│  └─ task_email: Generate Email HTML (Bilingual)           │
│                                                            │
│  Note: English content is translation, not new fetch      │
└────────────────────────────────────────────────────────────┘
```

---

## 4. File Organization

### 4.1 Output Directory Structure

```
/Users/jayden/Developer/fashion-research/
├── Template.md                              # HTML templates
├── fashion-digest.config.json              # Configuration
├── output/
│   ├── 2026-03-10-fashion-digest.md
│   ├── 2026-03-10-fashion-digest.html
│   └── 2026-03-10-fashion-digest-email.html
├── output_md/                               # Legacy (deprecate)
├── output_html/                             # Legacy (deprecate)
└── output_email/                            # Legacy (deprecate)
```

### 4.2 Recommended New Structure

```
/Users/jayden/Developer/fashion-research/
├── templates/
│   ├── Template.md                          # Main template
│   ├── partials/
│   │   ├── article-card.html
│   │   ├── youtube-card.html
│   │   └── runway-card.html
│   └── email/
│       └── email-template.html
├── output/
│   └── 2026-03-10/
│       ├── fashion-digest.md
│       ├── fashion-digest.html
│       └── fashion-digest-email.html
└── config.json
```

### 4.3 Fallback Image Configuration

```json
{
  "fallbacks": {
    "brand": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
    "luxury": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800",
    "tech": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800",
    "sustainability": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800",
    "retail": "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=800",
    "street": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800",
    "market": "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=800"
  }
}
```

---

## 5. Error Handling Strategy

### 5.1 Parallel Fetch Error Pattern

```typescript
// Each parallel task returns Result type
interface FetchResult<T> {
  success: boolean;
  data?: T;
  error?: string;
  fallback?: T;  // Pre-computed fallback
}

// Article fetch with fallback
async function fetchArticle(url: string): Promise<FetchResult<ArticleData>> {
  try {
    const content = await WebFetch(url);
    return {
      success: true,
      data: extractArticleData(content)
    };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      fallback: createFallbackFromSnippet(url)  // Use search snippet
    };
  }
}

// Collect all results - don't fail on individual errors
const results = await Promise.allSettled(articleTasks);
const articles = results.map(r => 
  r.status === 'fulfilled' && r.value.success 
    ? r.value.data 
    : r.value.fallback
).filter(Boolean);  // Remove nulls

// Ensure minimum article count
if (articles.length < 10) {
  // Fill remaining slots with search snippet summaries
  const fillers = await getSnippetSummaries(10 - articles.length);
  articles.push(...fillers);
}
```

### 5.2 Error Recovery Levels

| Level | Trigger | Action |
|-------|---------|--------|
| L1 | WebFetch timeout (5s) | Retry once with shorter timeout |
| L2 | Retry failed | Use search snippet summary |
| L3 | No snippet available | Use generic category description |
| L4 | Critical failure (<5 articles) | Alert user, partial output |

### 5.3 Partial Output Strategy

```typescript
// Always generate output even with failures
if (articles.length >= 5) {
  // Generate with available content
  generateOutput({ 
    articles: articles.slice(0, 10),  // Use what we have
    warnings: [`Only ${articles.length} articles fetched successfully`]
  });
} else {
  // Critical failure - require user intervention
  throw new Error('Insufficient data: < 5 articles');
}
```

---

## 6. Implementation Checklist

### 6.1 Phase 1: Template Creation
- [ ] Create `/templates/Template.md` with all variables
- [ ] Extract card templates to separate partials
- [ ] Define variable naming convention
- [ ] Test template substitution with sample data

### 6.2 Phase 2: Parallel Fetch Implementation
- [ ] Implement background task pattern for articles
- [ ] Implement background task pattern for YouTube
- [ ] Implement background task pattern for runway
- [ ] Add result collection and error handling

### 6.3 Phase 3: File Generation
- [ ] Implement template engine (simple replace)
- [ ] Generate all 3 output files in parallel
- [ ] Add fallback image handling
- [ ] Validate HTML output

### 6.4 Phase 4: Testing & Validation
- [ ] Test with 10 concurrent fetches
- [ ] Measure execution time vs old implementation
- [ ] Test error scenarios (failed fetches)
- [ ] Verify all 3 output files render correctly

---

## 7. Performance Comparison

| Phase | Current (Sequential) | Optimized (Parallel) | Speedup |
|-------|---------------------|---------------------|---------|
| Search | 3-5s | 3-5s | 1x |
| Article Analysis | 20s (10×2s) | 3-5s | 4-6x |
| YouTube/Runway | 10s (8×1.2s) | 2-3s | 3-4x |
| Image Fetch | 10s (10×1s) | 2-3s | 3-4x |
| File Generation | 3s (sequential) | 1-2s | 1.5x |
| **Total** | **~46s** | **~12s** | **4x** |

---

## 8. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Rate limiting on parallel fetches | Add 100ms delay between batch starts; use 5 concurrent max |
| Memory overhead from parallel tasks | Stream results; don't hold all in memory |
| Template maintenance | Version templates; validate on skill load |
| Partial fetch failures | Always use fallback content; never fail entirely |

---

## Summary

This optimization plan achieves **4x speedup** through:

1. **Template-based generation**: Pre-defined HTML structures eliminate generation time
2. **Aggressive parallelization**: All independent WebFetches run concurrently
3. **Smart error handling**: Fallbacks ensure partial success is still useful
4. **Modular architecture**: Templates separate from logic for maintainability

**Next Step**: Implement Phase 1 (Template Creation) and Phase 2 (Parallel Fetch) first for immediate performance gains.
