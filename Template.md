# Fashion Digest HTML Templates

> Template file for fashion-digest skill HTML generation
> 위치: /Users/jayden/Developer/fashion-research/Template.md

---

## 변수 정의 (Variables)

### 날짜 변수
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{DATE_ISO}}` | ISO 형식 날짜 | `2026-03-10` |
| `{{DATE_KR}}` | 한국어 날짜 | `2026년 3월 10일` |
| `{{DATE_EN}}` | 영어 날짜 | `March 10, 2026` |

### 기사 변수 (Article X: 1-10)
| 변수 | 설명 |
|------|------|
| `{{ARTICLE_X_TITLE}}` | 기사 제목 |
| `{{ARTICLE_X_URL}}` | 기사 URL |
| `{{ARTICLE_X_SOURCE}}` | 출처 (WWD, BoF 등) |
| `{{ARTICLE_X_DATE}}` | 발행일 |
| `{{ARTICLE_X_CATEGORY}}` | 카테고리 |
| `{{ARTICLE_X_SUMMARY_KR}}` | 한국어 요약 |
| `{{ARTICLE_X_INSIGHT_KR}}` | 한국어 시사점 |
| `{{ARTICLE_X_HIGHLIGHT_KR}}` | 한국어 흥미 포인트 |
| `{{ARTICLE_X_SUMMARY_EN}}` | 영어 요약 |
| `{{ARTICLE_X_INSIGHT_EN}}` | 영어 시사점 |
| `{{ARTICLE_X_HIGHLIGHT_EN}}` | 영어 흥미 포인트 |
| `{{ARTICLE_X_THUMB}}` | 썸네일 URL |
| `{{ARTICLE_X_FALLBACK}}` | 대체 이미지 URL |

### YouTube 변수 (YT X: 1-3)
| 변수 | 설명 |
|------|------|
| `{{YT_X_TITLE}}` | 영상 제목 |
| `{{YT_X_URL}}` | YouTube URL |
| `{{YT_X_VIDEO_ID}}` | 비디오 ID (v= 파라미터) |
| `{{YT_X_CHANNEL}}` | 채널명 |
| `{{YT_X_DATE}}` | 업로드 날짜 |
| `{{YT_X_CATEGORY}}` | 카테고리 |
| `{{YT_X_SUMMARY_KR}}` | 한국어 요약 |
| `{{YT_X_SUMMARY_EN}}` | 영어 요약 |

### Runway 변수 (RW X: 1-5)
| 변수 | 설명 |
|------|------|
| `{{RW_X_BRAND}}` | 브랜드명 |
| `{{RW_X_DESIGNER}}` | 디자이너명 |
| `{{RW_X_DATE}}` | 쇼 날짜 |
| `{{RW_X_VENUE}}` | 장소 |
| `{{RW_X_SUMMARY_KR}}` | 한국어 컬렉션 요약 |
| `{{RW_X_SUMMARY_EN}}` | 영어 컬렉션 요약 |
| `{{RW_X_CRITIC_KR}}` | 한국어 비평가 반응 |
| `{{RW_X_CRITIC_EN}}` | 영어 비평가 반응 |
| `{{RW_X_CRITIC_SOURCE}}` | 비평가 출처 (Vogue, WWD 등) |
| `{{RW_X_SOCIAL_KR}}` | 한국어 소셜 반응 |
| `{{RW_X_SOCIAL_EN}}` | 영어 소셜 반응 |
| `{{RW_X_THUMB}}` | 썸네일 URL |
| `{{RW_X_FALLBACK}}` | 대체 이미지 URL |

---

## PART 1: Web HTML Template

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fashion Digest — {{DATE_ISO}}</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
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
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: var(--bg-primary); color: var(--text-secondary); font-family: 'Inter', sans-serif; }
    header { text-align: center; padding: 80px 20px 60px; border-bottom: 1px solid var(--border); }
    header h1 { font-family: 'Playfair Display', serif; font-size: clamp(2.5rem, 6vw, 5rem); color: var(--text-primary); letter-spacing: 0.05em; }
    header .date { color: var(--accent-gold); font-size: 0.85rem; letter-spacing: 0.2em; text-transform: uppercase; margin-top: 12px; }
    header .subtitle { color: #666; font-size: 0.9rem; margin-top: 8px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 2px; padding: 2px; max-width: 1400px; margin: 40px auto; }
    .card { background: var(--bg-card); overflow: hidden; transition: transform 0.3s; }
    .card:hover { transform: translateY(-4px); }
    .card img { width: 100%; height: 220px; object-fit: cover; filter: brightness(0.85); }
    .card-body { padding: 24px; }
    .card-number { font-family: 'Playfair Display', serif; font-size: 0.8rem; color: var(--accent-gold); margin-bottom: 8px; }
    .card-meta { display: flex; gap: 12px; margin-bottom: 12px; font-size: 0.75rem; color: #888; letter-spacing: 0.1em; text-transform: uppercase; }
    .card-meta .source { color: var(--accent-gold); }
    .card h2 { font-family: 'Playfair Display', serif; font-size: 1.2rem; line-height: 1.5; color: var(--text-primary); margin-bottom: 16px; }
    .card h2 a { color: inherit; text-decoration: none; }
    .card h2 a:hover { color: var(--accent-gold); }
    .category { display: inline-block; font-size: 0.7rem; padding: 3px 10px; border: 1px solid rgba(201,169,110,0.2); color: var(--accent-gold); letter-spacing: 0.1em; margin-bottom: 14px; }
    .section-title { font-size: 0.7rem; color: #555; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 6px; }
    .summary { font-size: 0.88rem; line-height: 1.7; color: var(--text-muted); margin-bottom: 16px; }
    .insight { font-size: 0.85rem; line-height: 1.6; color: #999; border-left: 2px solid var(--accent-gold); padding-left: 12px; margin-bottom: 14px; }
    .highlight { font-size: 0.8rem; color: var(--accent-gold); font-style: italic; }
    .yt-section { max-width: 1400px; margin: 60px auto 40px; padding: 0 2px; }
    .yt-section-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: var(--text-primary); padding: 0 20px 20px; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
    .yt-section-title span { color: var(--accent-gold); }
    .yt-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px; }
    .yt-card { background: var(--bg-card); overflow: hidden; }
    .yt-card:hover .yt-thumb-wrap img { transform: scale(1.03); }
    .yt-thumb-wrap { position: relative; overflow: hidden; }
    .yt-thumb-wrap img { width: 100%; height: 200px; object-fit: cover; filter: brightness(0.8); transition: transform 0.4s; }
    .yt-play-badge { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 52px; height: 52px; background: rgba(255,0,0,0.85); border-radius: 50%; display: flex; align-items: center; justify-content: center; pointer-events: none; }
    .yt-play-badge::after { content: ''; border: 0 solid transparent; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left: 18px solid #fff; margin-left: 4px; }
    .yt-card-body { padding: 24px; }
    .yt-meta { display: flex; gap: 10px; font-size: 0.75rem; color: #888; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px; }
    .yt-meta .yt-channel { color: var(--accent-gold); }
    .yt-category { display: inline-block; font-size: 0.7rem; padding: 3px 10px; border: 1px solid rgba(255,107,107,0.4); color: var(--accent-yt); letter-spacing: 0.1em; margin-bottom: 14px; }
    .yt-card h3 { font-family: 'Playfair Display', serif; font-size: 1.1rem; line-height: 1.5; color: var(--text-primary); margin-bottom: 14px; }
    .yt-card h3 a { color: inherit; text-decoration: none; }
    .yt-card h3 a:hover { color: var(--accent-gold); }
    .yt-summary { font-size: 0.88rem; line-height: 1.7; color: var(--text-muted); }
    .runway-section { max-width: 1400px; margin: 60px auto 40px; padding: 0 2px; }
    .runway-section-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; color: var(--text-primary); padding: 0 20px 20px; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
    .runway-section-title span { color: var(--accent-gold); }
    .runway-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 2px; }
    .runway-card { background: var(--bg-card); overflow: hidden; transition: transform 0.3s; }
    .runway-card:hover { transform: translateY(-4px); }
    .runway-card img { width: 100%; height: 280px; object-fit: cover; filter: brightness(0.8); transition: filter 0.3s; }
    .runway-card:hover img { filter: brightness(1); }
    .runway-card-body { padding: 22px; }
    .runway-brand { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: var(--text-primary); margin-bottom: 4px; }
    .runway-meta { font-size: 0.75rem; color: #888; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px; }
    .runway-meta .rw-designer { color: var(--accent-gold); }
    .runway-summary { font-size: 0.88rem; line-height: 1.7; color: var(--text-muted); margin-bottom: 14px; }
    .runway-reactions { border-top: 1px solid #1e1e1e; padding-top: 14px; }
    .reaction-label { font-size: 0.7rem; color: #555; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 4px; }
    .critic-reaction { font-size: 0.85rem; line-height: 1.6; color: #999; border-left: 2px solid var(--accent-gold); padding-left: 10px; margin-bottom: 10px; }
    .social-reaction { font-size: 0.82rem; line-height: 1.6; color: #888; font-style: italic; }
    footer { text-align: center; padding: 40px; color: #333; font-size: 0.75rem; letter-spacing: 0.1em; }
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
```

---

## PART 2: Card Templates (for variable substitution)

### Article Card Template (Korean)
```html
<article class="card">
  <img src="{{ARTICLE_X_THUMB}}" alt="{{ARTICLE_X_TITLE}}" onerror="this.src='{{ARTICLE_X_FALLBACK}}'">
  <div class="card-body">
    <div class="card-number">No. 0{{X}}</div>
    <div class="card-meta">
      <span class="source">{{ARTICLE_X_SOURCE}}</span>
      <span>{{ARTICLE_X_DATE}}</span>
    </div>
    <span class="category">{{ARTICLE_X_CATEGORY}}</span>
    <h2><a href="{{ARTICLE_X_URL}}" target="_blank">{{ARTICLE_X_TITLE}}</a></h2>
    <div class="section-title">핵심 요약</div>
    <p class="summary">{{ARTICLE_X_SUMMARY_KR}}</p>
    <div class="section-title">시사점</div>
    <p class="insight">{{ARTICLE_X_INSIGHT_KR}}</p>
    <p class="highlight">✦ {{ARTICLE_X_HIGHLIGHT_KR}}</p>
  </div>
</article>
```

### YouTube Card Template
```html
<article class="yt-card">
  <div class="yt-thumb-wrap">
    <img src="https://img.youtube.com/vi/{{YT_X_VIDEO_ID}}/maxresdefault.jpg" alt="{{YT_X_TITLE}}">
    <a href="{{YT_X_URL}}" target="_blank"><div class="yt-play-badge"></div></a>
  </div>
  <div class="yt-card-body">
    <div class="yt-meta">
      <span class="yt-channel">{{YT_X_CHANNEL}}</span>
      <span>{{YT_X_DATE}}</span>
    </div>
    <span class="yt-category">{{YT_X_CATEGORY}}</span>
    <h3><a href="{{YT_X_URL}}" target="_blank">{{YT_X_TITLE}}</a></h3>
    <p class="yt-summary">{{YT_X_SUMMARY_KR}}</p>
  </div>
</article>
```

### Runway Card Template (Korean)
```html
<article class="runway-card">
  <img src="{{RW_X_THUMB}}" alt="{{RW_X_BRAND}}" onerror="this.src='{{RW_X_FALLBACK}}'">
  <div class="runway-card-body">
    <div class="runway-brand">{{RW_X_BRAND}}</div>
    <div class="runway-meta">
      <span class="rw-designer">{{RW_X_DESIGNER}}</span> · {{RW_X_DATE}} · {{RW_X_VENUE}}
    </div>
    <p class="runway-summary">{{RW_X_SUMMARY_KR}}</p>
    <div class="runway-reactions">
      <div class="reaction-label">비평가 반응</div>
      <p class="critic-reaction">{{RW_X_CRITIC_KR}}</p>
      <div class="reaction-label">대중/소셜 반응</div>
      <p class="social-reaction">{{RW_X_SOCIAL_KR}}</p>
    </div>
  </div>
</article>
```

---

## PART 3: Email HTML Template

```html
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
        <p style="margin:0 0 20px;font-size:13px;color:#ff6b6b;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">▶ YouTube — 오늘의 패션 영상 3선</p>
{{KOREAN_YOUTUBE_CARDS}}
      </td></tr>
      
      <!-- Divider -->
      <tr><td style="padding:20px 0;"><hr style="border:none;border-top:1px solid #1a1a1a;"></td></tr>
      
      <!-- YouTube English -->
      <tr><td style="padding:8px 0;">
        <p style="margin:0 0 20px;font-size:13px;color:#ff6b6b;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">▶ YouTube — Today's Fashion Videos</p>
{{ENGLISH_YOUTUBE_CARDS}}
      </td></tr>
      
      <!-- Divider -->
      <tr><td style="padding:20px 0;"><hr style="border:none;border-top:1px solid #1a1a1a;"></td></tr>
      
      <!-- Runway Korean -->
      <tr><td style="padding:8px 0;">
        <p style="margin:0 0 20px;font-size:13px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">🏛 Runway — 이번 시즌 럭셔리 5선</p>
{{KOREAN_RUNWAY_CARDS}}
      </td></tr>
      
      <!-- Divider -->
      <tr><td style="padding:20px 0;"><hr style="border:none;border-top:1px solid #1a1a1a;"></td></tr>
      
      <!-- Runway English -->
      <tr><td style="padding:8px 0;">
        <p style="margin:0 0 20px;font-size:13px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">🏛 Runway — Season's Luxury Highlights</p>
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
```

---

## PART 4: Email Card Templates (Inline CSS)

### Email Article Card (Korean)
```html
<table width="560" cellpadding="0" cellspacing="0" style="margin:0 auto 24px;background:#111111;border-radius:4px;overflow:hidden;">
  <tr><td>
    <img src="{{ARTICLE_X_THUMB}}" width="560" height="200" style="display:block;width:100%;height:200px;object-fit:cover;" alt="{{ARTICLE_X_TITLE}}" onerror="this.src='{{ARTICLE_X_FALLBACK}}'">
  </td></tr>
  <tr><td style="padding:20px 24px;">
    <p style="margin:0 0 6px;font-size:11px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">{{ARTICLE_X_SOURCE}} · {{ARTICLE_X_DATE}}</p>
    <span style="display:inline-block;margin:0 0 10px;padding:2px 8px;border:1px solid #c9a96e44;color:#c9a96e;font-size:10px;letter-spacing:1px;font-family:Arial,sans-serif;">{{ARTICLE_X_CATEGORY}}</span>
    <h3 style="margin:0 0 14px;font-size:17px;line-height:1.5;color:#ffffff;font-family:Georgia,serif;">
      <a href="{{ARTICLE_X_URL}}" style="color:#ffffff;text-decoration:none;">{{ARTICLE_X_TITLE}}</a>
    </h3>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">핵심 요약</p>
    <p style="margin:0 0 14px;font-size:14px;line-height:1.7;color:#bbbbbb;font-family:Arial,sans-serif;">{{ARTICLE_X_SUMMARY_KR}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">시사점</p>
    <p style="margin:0 0 12px;font-size:13px;line-height:1.6;color:#999999;padding-left:10px;border-left:2px solid #c9a96e;font-family:Arial,sans-serif;">{{ARTICLE_X_INSIGHT_KR}}</p>
    <p style="margin:0;font-size:12px;color:#c9a96e;font-style:italic;font-family:Georgia,serif;">✦ {{ARTICLE_X_HIGHLIGHT_KR}}</p>
  </td></tr>
</table>
```

### Email Article Card (English)
```html
<table width="560" cellpadding="0" cellspacing="0" style="margin:0 auto 24px;background:#111111;border-radius:4px;overflow:hidden;">
  <tr><td>
    <img src="{{ARTICLE_X_THUMB}}" width="560" height="200" style="display:block;width:100%;height:200px;object-fit:cover;" alt="{{ARTICLE_X_TITLE}}" onerror="this.src='{{ARTICLE_X_FALLBACK}}'">
  </td></tr>
  <tr><td style="padding:20px 24px;">
    <p style="margin:0 0 6px;font-size:11px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">{{ARTICLE_X_SOURCE}} · {{ARTICLE_X_DATE}}</p>
    <span style="display:inline-block;margin:0 0 10px;padding:2px 8px;border:1px solid #c9a96e44;color:#c9a96e;font-size:10px;letter-spacing:1px;font-family:Arial,sans-serif;">{{ARTICLE_X_CATEGORY}}</span>
    <h3 style="margin:0 0 14px;font-size:17px;line-height:1.5;color:#ffffff;font-family:Georgia,serif;">
      <a href="{{ARTICLE_X_URL}}" style="color:#ffffff;text-decoration:none;">{{ARTICLE_X_TITLE}}</a>
    </h3>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">Summary</p>
    <p style="margin:0 0 14px;font-size:14px;line-height:1.7;color:#bbbbbb;font-family:Arial,sans-serif;">{{ARTICLE_X_SUMMARY_EN}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">Implications</p>
    <p style="margin:0 0 12px;font-size:13px;line-height:1.6;color:#999999;padding-left:10px;border-left:2px solid #c9a96e;font-family:Arial,sans-serif;">{{ARTICLE_X_INSIGHT_EN}}</p>
    <p style="margin:0;font-size:12px;color:#c9a96e;font-style:italic;font-family:Georgia,serif;">✦ {{ARTICLE_X_HIGHLIGHT_EN}}</p>
  </td></tr>
</table>
```

### Email YouTube Card (Korean)
```html
<table width="560" cellpadding="0" cellspacing="0" style="margin:0 auto 20px;background:#111111;border-radius:4px;overflow:hidden;">
  <tr><td>
    <a href="{{YT_X_URL}}" style="display:block;">
      <img src="https://img.youtube.com/vi/{{YT_X_VIDEO_ID}}/maxresdefault.jpg" width="560" height="210" style="display:block;width:100%;height:210px;object-fit:cover;" alt="{{YT_X_TITLE}}">
    </a>
  </td></tr>
  <tr><td style="padding:4px 20px 4px;background:#1a0000;">
    <p style="margin:0;font-size:10px;color:#ff6b6b;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">▶ YouTube</p>
  </td></tr>
  <tr><td style="padding:12px 20px 20px;background:#111111;">
    <p style="margin:0 0 6px;font-size:11px;color:#c9a96e;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">{{YT_X_CHANNEL}} · {{YT_X_DATE}}</p>
    <span style="display:inline-block;margin:0 0 10px;padding:2px 8px;border:1px solid rgba(255,107,107,0.4);color:#ff6b6b;font-size:10px;letter-spacing:1px;font-family:Arial,sans-serif;">{{YT_X_CATEGORY}}</span>
    <h3 style="margin:0 0 12px;font-size:16px;line-height:1.5;color:#ffffff;font-family:Georgia,serif;">
      <a href="{{YT_X_URL}}" style="color:#ffffff;text-decoration:none;">{{YT_X_TITLE}}</a>
    </h3>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">영상 요약</p>
    <p style="margin:0;font-size:14px;line-height:1.7;color:#bbbbbb;font-family:Arial,sans-serif;">{{YT_X_SUMMARY_KR}}</p>
  </td></tr>
</table>
```

### Email YouTube Card (English)
```html
<table width="560" cellpadding="0" cellspacing="0" style="margin:0 auto 20px;background:#111111;border-radius:4px;overflow:hidden;">
  <tr><td>
    <a href="{{YT_X_URL}}" style="display:block;">
      <img src="https://img.youtube.com/vi/{{YT_X_VIDEO_ID}}/maxresdefault.jpg" width="560" height="210" style="display:block;width:100%;height:210px;object-fit:cover;" alt="{{YT_X_TITLE}}">
    </a>
  </td></tr>
  <tr><td style="padding:4px 20px 4px;background:#1a0000;">
    <p style="margin:0;font-size:10px;color:#ff6b6b;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">▶ YouTube</p>
  </td></tr>
  <tr><td style="padding:12px 20px 20px;background:#111111;">
    <p style="margin:0 0 6px;font-size:11px;color:#c9a96e;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">{{YT_X_CHANNEL}} · {{YT_X_DATE}}</p>
    <span style="display:inline-block;margin:0 0 10px;padding:2px 8px;border:1px solid rgba(255,107,107,0.4);color:#ff6b6b;font-size:10px;letter-spacing:1px;font-family:Arial,sans-serif;">{{YT_X_CATEGORY}}</span>
    <h3 style="margin:0 0 12px;font-size:16px;line-height:1.5;color:#ffffff;font-family:Georgia,serif;">
      <a href="{{YT_X_URL}}" style="color:#ffffff;text-decoration:none;">{{YT_X_TITLE}}</a>
    </h3>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">Video Summary</p>
    <p style="margin:0;font-size:14px;line-height:1.7;color:#bbbbbb;font-family:Arial,sans-serif;">{{YT_X_SUMMARY_EN}}</p>
  </td></tr>
</table>
```

### Email Runway Card (Korean)
```html
<table width="560" cellpadding="0" cellspacing="0" style="margin:0 auto 20px;background:#111111;border-radius:4px;overflow:hidden;">
  <tr><td>
    <img src="{{RW_X_THUMB}}" width="560" height="240" style="display:block;width:100%;height:240px;object-fit:cover;" alt="{{RW_X_BRAND}}" onerror="this.src='{{RW_X_FALLBACK}}'">
  </td></tr>
  <tr><td style="padding:4px 20px;background:#0d0d1a;">
    <p style="margin:0;font-size:10px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">🏛 RUNWAY</p>
  </td></tr>
  <tr><td style="padding:14px 20px 20px;background:#111111;">
    <h3 style="margin:0 0 4px;font-size:19px;color:#ffffff;font-family:Georgia,serif;">{{RW_X_BRAND}}</h3>
    <p style="margin:0 0 12px;font-size:11px;color:#c9a96e;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">{{RW_X_DESIGNER}} · {{RW_X_DATE}} · {{RW_X_VENUE}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">컬렉션 요약</p>
    <p style="margin:0 0 14px;font-size:14px;line-height:1.7;color:#bbbbbb;font-family:Arial,sans-serif;">{{RW_X_SUMMARY_KR}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">비평가 반응</p>
    <p style="margin:0 0 12px;font-size:13px;line-height:1.6;color:#999999;padding-left:10px;border-left:2px solid #c9a96e;font-family:Arial,sans-serif;">{{RW_X_CRITIC_KR}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">대중/소셜 반응</p>
    <p style="margin:0;font-size:13px;line-height:1.6;color:#888888;font-style:italic;font-family:Georgia,serif;">{{RW_X_SOCIAL_KR}}</p>
  </td></tr>
</table>
```

### Email Runway Card (English)
```html
<table width="560" cellpadding="0" cellspacing="0" style="margin:0 auto 20px;background:#111111;border-radius:4px;overflow:hidden;">
  <tr><td>
    <img src="{{RW_X_THUMB}}" width="560" height="240" style="display:block;width:100%;height:240px;object-fit:cover;" alt="{{RW_X_BRAND}}" onerror="this.src='{{RW_X_FALLBACK}}'">
  </td></tr>
  <tr><td style="padding:4px 20px;background:#0d0d1a;">
    <p style="margin:0;font-size:10px;color:#c9a96e;letter-spacing:2px;text-transform:uppercase;font-family:Arial,sans-serif;">🏛 RUNWAY</p>
  </td></tr>
  <tr><td style="padding:14px 20px 20px;background:#111111;">
    <h3 style="margin:0 0 4px;font-size:19px;color:#ffffff;font-family:Georgia,serif;">{{RW_X_BRAND}}</h3>
    <p style="margin:0 0 12px;font-size:11px;color:#c9a96e;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">{{RW_X_DESIGNER}} · {{RW_X_DATE}} · {{RW_X_VENUE}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">Collection Summary</p>
    <p style="margin:0 0 14px;font-size:14px;line-height:1.7;color:#bbbbbb;font-family:Arial,sans-serif;">{{RW_X_SUMMARY_EN}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">Critic Reaction</p>
    <p style="margin:0 0 12px;font-size:13px;line-height:1.6;color:#999999;padding-left:10px;border-left:2px solid #c9a96e;font-family:Arial,sans-serif;">{{RW_X_CRITIC_EN}}</p>
    <p style="margin:0 0 4px;font-size:10px;color:#555555;letter-spacing:1.5px;text-transform:uppercase;font-family:Arial,sans-serif;">Social Reaction</p>
    <p style="margin:0;font-size:13px;line-height:1.6;color:#888888;font-style:italic;font-family:Georgia,serif;">{{RW_X_SOCIAL_EN}}</p>
  </td></tr>
</table>
```

---

## Fallback 이미지 URLs

카테고리별 기본 이미지 (og:image 추출 실패 시 사용):

```json
{
  "fallbacks": {
    "브랜드전략": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
    "럭셔리": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800",
    "테크/AI": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800",
    "지속가능성": "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?w=800",
    "유통/리테일": "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=800",
    "스트리트": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800",
    "시장동향": "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=800",
    "runway": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800"
  }
}
```

---

## 사용법

### 1. 템플릿 로드
```javascript
const template = readFile('/Users/jayden/Developer/fashion-research/Template.md');
const webTemplate = extractPart(template, 'PART 1: Web HTML Template');
```

### 2. 변수 대체
```javascript
// 카드 생성
const articleCards = articles.map((a, i) => {
  let card = articleCardTemplate;
  card = card.replace(/{{ARTICLE_X_TITLE}}/g, a.title);
  card = card.replace(/{{ARTICLE_X_URL}}/g, a.url);
  // ... 나머지 변수
  return card;
}).join('\n');

// 메인 템플릿에 삽입
let html = webTemplate
  .replace('{{ARTICLE_CARDS}}', articleCards)
  .replace('{{DATE_ISO}}', dateISO)
  .replace('{{DATE_KR}}', dateKR);
```

### 3. 파일 저장
```javascript
writeFile(`output/${dateISO}-fashion-digest.html`, html);
```
