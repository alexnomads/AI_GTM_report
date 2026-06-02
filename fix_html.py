#!/usr/bin/env python3
import json
import re

# Load scraped data
with open('ai_gtm_posts_2026-06-01.json', 'r') as f:
    data = json.load(f)

all_tweets = data.get('all_tweets', []) + data.get('marketing_results', [])

# Create lookup: username -> list of (tweet_id, full_text)
username_lookup = {}
for t in all_tweets:
    uid = t.get('username')
    tid = t.get('tweet_id')
    text = t.get('text', '')
    if uid and tid and uid not in username_lookup:
        username_lookup[uid] = []
    if uid and tid:
        username_lookup[uid].append((tid, text))

# Load current HTML
with open('ai_gtm_report_2026-06-01.html', 'r') as f:
    html = f.read()

# For each card, fix its View on X link
def fix_card(match):
    card_html = match.group(0)
    
    # Extract username from @username in card-header
    handle_match = re.search(r"@(\w+)", card_html)
    if not handle_match:
        return card_html
    
    username = handle_match.group(1)
    
    # Find matching tweets for this user
    if username in username_lookup:
        tweets = username_lookup[username]
        # Get first tweet for this user (the one in this card)
        if tweets:
            tid, _ = tweets[0]
            url = f"https://x.com/{username}/status/{tid}"
        else:
            url = "#"
    else:
        url = "#"
    
    return re.sub(r'<a href="#">View on X</a>', f'<a href="{url}">View on X</a>', card_html)

fixed_html = re.sub(r'<div class=\'card\'>(.*?)</div>', fix_card, html, flags=re.DOTALL)

# Save fixed HTML
with open('ai_gtm_report_2026-06-01.html', 'w') as f:
    f.write(fixed_html)

print("Fixed all View on X links in HTML")
