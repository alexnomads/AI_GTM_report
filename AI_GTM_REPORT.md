# 🤖 AI GTM Hiring Report - Daily Marketing & Growth Intelligence

## About

Daily curated hiring report for **AI/GTM/Marketing** roles in startups specializing in AI agents, AI SaaS, and automation tools.

## 🎯 Focus Areas

### Target Job Titles
- **GTM / Go-To-Market**
- **Head of Marketing**
- **Marketing Manager**
- **Customer Success**
- **Product Marketing / Product Marketer**
- **CMO / Chief Marketing Officer**
- **Head of Community**

### Tech Stack Keywords
Reports prioritize postings mentioning:
- **API** automation
- **OpenClaw / Hermes / Claude / N8N** tools
- **Marketing strategy** approaches

### Preferred Fundraising Stage
Startups that have raised:
- Seed, Series A, Series B, or Series C funding
- Specializing in **AI Agent** or **AI SaaS** products

## ⏰ Schedule

**Daily at 1:00 PM CET (Madrid time)** → 11:00 UTC

Reports are generated from the past 24 hours of hiring tweets.

## 📊 Live Report

View latest report: <https://alexnomads.github.io/AI_GTM_report/>

## 🔧 Pipeline

```
scraper_twitter_hiring.py → generate_report.py → update_index.py → GitHub Pages
```

- **Scraper**: Pulls hiring tweets from Twitter/X via Bird API (24h window)
- **Generator**: Filters for target roles and tech stack relevance
- **Index**: Dynamically updates archive with latest report link

## 📁 Repository Structure

```
AI_GTM_report/
├── scraper_twitter_hiring.py     # Twitter hiring tweet scraper
├── generate_report.py            # Filters & generates HTML report
├── update_index.py               # Updates index.html links
├── ai-gtm-report.yml             # GitHub Actions workflow
├── .github/
│   └── workflows/ai-gtm-report.yml
├── index.html                    # Main archive page
└── AI_GTM_REPORT.md              # This documentation
```

## 🚀 How to Run Locally

```bash
# 1. Install Twitter credentials (see .twitter_cookies.env)
# 2. Run scraper
python scraper_twitter_hiring.py days_ago=1

# 3. Generate filtered report
python generate_report.py

# 4. Update index
python update_index.py
```

## 📜 License

MIT - See LICENSE file for details
