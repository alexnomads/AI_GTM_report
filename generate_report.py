#!/usr/bin/env python3
"""Generate HTML report for AI GTM hiring posts.

Reads raw JSON data from ai_gtm_posts_YYYY-MM-DD.json and generates:
1. Target role filtering (GTM, Head of Marketing, CMO, Customer Success, Product Marketing, etc.)
2. Tech stack keyword scoring (API, Automation, OpenClaw, Claude, N8N)
3. AI/ML startup indicators (AI Agent, AI SaaS, LLM)
4. Relevance badges in HTML output
5. Single consolidated results list with prioritization
"""
import json
import re
import os
from datetime import datetime

def get_latest_post_file():
    """Find latest post JSON file."""
    pattern = r'ai_gtm_posts_(\d{4}-\d{2}-\d{2})\.json'
    files = [f for f in os.listdir('.') if re.search(pattern, f)]
    
    if not files:
        print("[ERROR] No ai_gtm_posts_*.json found")
        return None
    
    latest_file = max(files, key=lambda f: datetime.strptime(re.search(pattern, f).group(1), '%Y-%m-%d'))
    with open(latest_file) as f:
        data = json.load(f)
    
    report_date = re.search(pattern, latest_file).group(1)
    return data, report_date

TARGET_ROLE_KEYWORDS = [
    r'\bhead\s+of\s+marketing\b',
    r'\bhead\s+of\s+growth\b',
    r'\b(gtm|go-to-market)\b',
    r'\bcmo\b',
    r'\bchief marketing officer\b',
    r'\bproduct\s+marketing\b',
    r'\b(customer\s+success)\b',
    r'\b(product\s+marketer)\b',
    r'\b(marketing\s+manager)\b',
    r'\b(head\s+of\s+community)\b',
]

TECH_KEYWORDS = [
    r'\b(openclaw|hermes|claude|n8n)\b',
    r'\b(automation)\b',
    r'\b(api)\b',
    r'\b(marketing\s+strategy)\b',
]

AI_STARTUP_KEYWORDS = [
    r'\b(ai\s+agent|ai\s+saaS|llm|machine learning)\b',
]

def score_relevance(text, job_title):
    """Score relevance based on tech stack mentions."""
    text_lower = text.lower()
    score = 0
    
    # Tech stack keywords boost relevance
    for kw in TECH_KEYWORDS:
        if re.search(kw, text_lower):
            score += 2
    
    # AI/ML startup indicators boost relevance
    for kw in AI_STARTUP_KEYWORDS:
        if re.search(kw, text_lower):
            score += 3
    
    # Target roles give base score
    if job_title and any(re.search(kw, job_title.lower()) for kw in TARGET_ROLE_KEYWORDS):
        score += 1
    
    return max(score, 0)

def is_target_role(text, job_title):
    """Check if this is a target role posting."""
    text_lower = text.lower()
    
    # Direct role match
    if job_title and any(re.search(kw, job_title.lower()) for kw in TARGET_ROLE_KEYWORDS):
        return True
    
    # Marketing context with tech stack
    marketing_context = any(kw.lower() in text_lower for kw in ['marketing', 'growth', 'product marketing', 'cmo'])
    has_tech = any(re.search(kw, text_lower) for kw in [r'\b(automation|api|openclaw)\b'])
    
    if marketing_context and has_tech:
        return True
    
    # Fallback: any hiring post with marketing context is valid
    if any(kw.lower() in text_lower for kw in ['marketing', 'growth']):
        return True
    
    return False

def generate_html(data, report_date):
    """Generate HTML report from raw data."""
    
    # Filter and score tweets
    results = []
    all_tweets = data.get('all_tweets', []) or []
    
    for tweet in all_tweets:
        text = tweet.get('text', '')
        job_title = tweet.get('job_title', '')
        
        # Check if target role
        if is_target_role(text, job_title):
            score = score_relevance(text, job_title)
            
            # Determine badge
            if score >= 4:
                badge_type = 'tech'
            else:
                badge_type = None
            
            results.append({
                **tweet,
                'relevance_score': score,
                'badge_type': badge_type,
            })
    
    # Sort by relevance score (highest first)
    results.sort(key=lambda x: (-x['relevance_score'], -x['relevance_score']))
    
    # Count by type
    marketing_count = len([r for r in results if 'marketing' in r.get('text', '').lower()])
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI GTM Hiring Report - {date}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box }}
body {{ font-family:-apple-system,sans-serif; background:#0a0a0a; color:#e0e0e0; padding:20px }}
.container {{ max-width:900px; margin:0 auto }}
.header {{ 
  background:linear-gradient(135deg,#1a1a2e,#16213e); 
  padding:30px; 
  border-radius:12px; 
  margin-bottom:20px 
}}
.header h1 {{ font-size:28px; color:#00d4aa; margin-bottom:10px }}
.header p {{ color:#888; font-size:14px }}
.stats {{ display:flex; gap:20px; margin-top:20px }}
.stat {{ 
  background:rgba(0,212,170,0.1); 
  padding:15px 20px; 
  border-radius:8px; 
  flex:1; 
  text-align:center 
}}
.stat-num {{ font-size:24px; font-weight:bold; color:#00d4aa }}
.stat-label {{ font-size:12px; color:#888; margin-top:5px }}
.latest-report {{ 
  margin-bottom:30px; 
  padding:20px; 
  background:#0f0f0f; 
  border:2px solid #00d4aa; 
  border-radius:8px; 
  text-align:center 
}}
.latest-report a {{ 
  display:inline-block; 
  background:#00d4aa; 
  color:#0a0a0a; 
  font-weight:bold; 
  padding:15px 25px; 
  text-decoration:none; 
  border-radius:6px; 
  margin-bottom:15px 
}}
.latest-report span {{ font-size:14px; color:#888 }}
.report-list {{ margin:30px 0 }}
.card {{ 
  background:#1a1a1a; 
  border:1px solid #333; 
  border-radius:8px; 
  padding:15px; 
  margin-bottom:10px 
}}
.card-header {{ display:flex; align-items:center; gap:8px; margin-bottom:8px }}
.card-handle {{ font-weight:bold; color:#00d4aa }}
.card-title {{ font-size:16px; margin-bottom:5px }}
.card-text {{ color:#ccc; font-size:14px; line-height:1.5; margin-bottom:10px }}
.card-meta {{ display:flex; gap:15px; font-size:12px; color:#666 }}
.card-meta a {{ color:#00d4aa; text-decoration:none }}
.badge {{ 
  display:inline-block; 
  padding:4px 8px; 
  border-radius:4px; 
  font-size:12px; 
  margin-left:8px 
}}
.badge-tech {{ background:#17a2b8; color:white }}
.badge-ai {{ background:#6f42c1; color:white }}
.footer {{ text-align:center; margin-top:40px; color:#555; font-size:12px }}
</style>
</head>
<body>
<div class='container'>
<div class='header'>
<h1>AI GTM Hiring Report - {date}</h1>
<p>Daily hiring intelligence for AI startups • GTM, Marketing, Customer Success, Product Marketing, and more</p>
<div class='stats'>
<div class='stat'><div class='stat-num'>{days}</div><div class='stat-label'>Days Covered</div></div>
<div class='stat'><div class='stat-num'>{count}</div><div class='stat-label'>Marketing Posts</div></div>
<div class='stat'><div class='stat-num'>{total}</div><div class='stat-label'>Total Jobs</div></div>
</div>
</div>

<h2>Latest Report — {date}</h2>
<a href="ai_gtm_report_{date}.html" style='display:inline-block;background:#00d4aa;border:1px solid #00d4aa;color:#00d4aa;font-weight:bold;padding:15px;margin-bottom:20px;text-decoration:none'>📄 View Latest Report ({date})</a>

<div class='latest-report'><span>This report showcases hiring opportunities in AI GTM/Marketing roles with tech stack signals.</span></div>

<div class='report-list'>
{cards}
</div>

<div class='footer'>Generated by AI GTM Report Pipeline • Powered by Twitter Bird API</div>
</div>
</body>
</html>"""
    
    # Generate job cards HTML
    cards_html = ""
    for r in results:
        text = r.get('text', '')[:300].replace('\n', ' ')
        company = r.get('company', '')
        job_title = r.get('job_title', '') or ''
        badge_type = r.get('badge_type')
        
        badges = ""
        if badge_type == 'tech':
            badges = '<span class="badge badge-tech">🔬 Tech Stack Match</span>'
        elif badge_type == 'ai':
            badges = '<span class="badge badge-ai">🤖 AI Startup Signal</span>'
        
        card_html = f"""<div class='card'>
<div class='card-header'><span class='card-handle'>@{r.get('username', '')}</span></div>
<div class='card-title'>{company} {job_title}</div>
<div class='card-text'>{text}</div>
<div class='card-meta'><a href='{r.get("twitter_url", "#")}'>View on X</a>{badges}</div>
</div>"""
        cards_html += card_html
    
    html_content = html_template.format(
        date=report_date,
        days='1',
        count=marketing_count,
        total=len(results),
        cards=cards_html,
    )
    
    # Generate HTML report file
    output_file = f'ai_gtm_report_{report_date}.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[OK] Generated HTML report: {output_file}")
    print(f"   - Marketing-focused jobs: {marketing_count}")
    print(f"   - Total target roles found: {len(results)}")
    
    return True

def update_index(data, report_date):
    """Update index.html to point to latest report."""
    index_file = 'index.html'
    
    if not os.path.exists(index_file):
        # Create default index
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>AI GTM Hiring Report</title>
<style>body{{font-family:sans-serif;background:#111;color:#e0e0e0;padding:50px;text-align:center}}
h1{{color:#00d4aa;font-size:32px;margin-bottom:10px}}p{{color:#888;font-size:16px;margin-bottom:30px}}
a{{display:inline-block;background:#00d4aa;color:#0a0a0a;padding:20px 30px;text-decoration:none;border-radius:8px;font-weight:bold;margin-bottom:20px;font-size:18px}}</style>
</head>
<body><h1>AI GTM Hiring Report</h1><p>Daily hiring intelligence for AI startups • GTM, Marketing, Customer Success</p>
<a href="ai_gtm_report_{report_date}.html" style='display:inline-block;background:#00d4aa;color:#0a0a0a;padding:20px 30px;text-decoration:none;border-radius:8px;font-weight:bold;margin-bottom:20px;font-size:18px'>📄 View Latest Report ({report_date})</a>
<p style='color:#666;font-size:14px;'>Updates automatically at 1pm CET (11 UTC) daily • GitHub Actions Workflow</p>
</body>
</html>""")
        print(f"[OK] Created default index.html pointing to {report_date} report")
        return True
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update latest report link
    content = re.sub(
        r'(href="ai_gtm_report_\d{4}-\d{2}-\d{2}\.html".*?)<a',
        f'\\1 href="ai_gtm_report_{report_date}.html", style=\'display:inline-block;background:#00d4aa;color:#0a0a0a;padding:20px 30px;text-decoration:none;border-radius:8px;font-weight:bold;margin-bottom:20px;font-size:18px;\'><',
        content,
        flags=re.IGNORECASE
    )
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] Updated index.html to point to latest report ({report_date})")
    return True

if __name__ == "__main__":
    data, report_date = get_latest_post_file()
    
    if not data:
        print("[ERROR] No raw tweet data found. Run scraper_twitter_hiring.py first.")
        exit(1)
    
    print("=" * 60)
    print("[GENERATOR] AI GTM Report Generator")
    print("=" * 60)
    
    # Generate HTML report
    if generate_html(data, report_date):
        # Update index
        update_index(data, report_date)
        
        print("\n" + "=" * 60)
        print("[OK] AI GTM Report Generation Complete!")
        print("=" * 60)
        print(f"[OK] Report URL: https://alexnomads.github.io/AI_GTM_report/")
    else:
        print("\n[ERROR] Report generation failed")
