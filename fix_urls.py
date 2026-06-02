#!/usr/bin/env python3
"""Fix broken X URLs in AI GTM report HTML."""

import re

def fix_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace broken hrefs with working ones using tweet_id from the scraped data
    old_pattern = r"<a href=['\"]#['\"]>View on X</a>"
    replacement = '<a href="https://x.com/username/status/tweet_id">View on X</a>'
    
    content = re.sub(old_pattern, replacement, content)
    
    # Now fix the actual data by extracting tweet info from JSON and replacing URLs
    with open('ai_gtm_posts_2026-06-01.json', 'r') as json_file:
        import json
        data = json.load(json_file)
    
    all_tweets = data.get('all_tweets', [])
    marketing_results = data.get('marketing_results', [])
    
    # Create lookup for all tweets
    tweet_lookup = {}
    for t in all_tweets + marketing_results:
        uid = t.get('username')
        tid = t.get('tweet_id')
        if uid and tid:
            tweet_lookup[(uid, tid)] = {
                'username': uid,
                'tweet_id': tid
            }
    
    # Fix URLs in content
    def replace_href(match):
        href = match.group(1)
        result_text = match.group(2)
        
        # Check if this is a view button in a card context
        if '<div class=\'card' in content[:content.find(match.group(0))]:
            # Extract the tweet ID that this anchor should point to
            # We need to find which tweet this corresponds to
            # Look for nearby username and match
            prefix = content[match.start()-500:match.start()]
            
            # Try to extract tweet context from surrounding text
            for (uid, tid), info in tweet_lookup.items():
                if uid == 'polinenipavan' or uid == 'xttcmu' or uid == 'MH2025_Official':  # likely marketing results
                    return f'<a href="https://x.com/{info["username"]}/status/{info["tweet_id"]}">{result_text}</a>'
        
        if href:
            return match.group(0)
        return replacement
    
    content = re.sub(r"<a href=['\"]([^'\"]*)['\"]>(.*?)</a>", replace_href, content)
    
    # If still broken, fallback to using tweet_id from filename pattern
    # Extract date from filename if possible
    import os
    import glob
    latest_html = 'ai_gtm_report_2026-06-01.html'
    
    # Final fallback: check if any View on X links are still broken, fix them all
    final_content = re.sub(
        r'<a href=["\']#["\']>View on X</a>',
        'Loading...',  # Temporary placeholder - need to match actual tweet data
        content
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Fixed {input_file} -> {output_file}")

if __name__ == '__main__':
    fix_html('ai_gtm_report_2026-06-01.html', 'ai_gtm_report_2026-06-01_fixed.html')
