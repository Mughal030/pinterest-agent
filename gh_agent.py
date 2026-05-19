#!/usr/bin/env python3
"""
Pinterest → AliExpress Agent v9
Using search links (more reliable)
"""
import os, json, subprocess, random, hashlib
from datetime import datetime, timedelta

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

FEMALE_PRODUCTS = [
    {"id": "1005005654900370", "name": "Oversized Hoodie Women", "price": "$19.99", "rating": "4.6★", "reviews": "(4,100 reviews)", "tags": ["WomenFashion", "PinterestViral", "Trend2026", "FashionTrends", "StyleInspo", "WomenStyle", "ViralFashion", "TrendyOutfit", "FashionTips", "Hoodie"], "analysis": "Comfortable chic."},
    {"id": "1005005451745185", "name": "Women Blazer Oversized", "price": "$32.99", "rating": "4.7★", "reviews": "(1,800 reviews)", "tags": ["WomenFashion", "PinterestViral", "Trend2026", "FashionTrends", "StyleInspo", "WomenStyle", "ViralFashion", "TrendyOutfit", "FashionTips", "Blazer"], "analysis": "Power dressing on YOUR terms."},
    {"id": "1005005210018416", "name": "High Waist Jeans Women", "price": "$24.99", "rating": "4.7★", "reviews": "(5,200 reviews)", "tags": ["WomenFashion", "PinterestViral", "Trend2026", "FashionTrends", "StyleInspo", "WomenStyle", "ViralFashion", "TrendyOutfit", "FashionTips", "Jeans"], "analysis": "Classic meets modern."},
]

GENERAL_PRODUCTS = [
    {"id": "1005004160570834", "name": "Canvas Tote Bag", "price": "$8.99", "rating": "4.6★", "reviews": "(7,800 reviews)", "tags": ["Trending", "TikTokViral", "PinterestFashion", "USATrends", "ViralFashion", "Trend2026", "StyleInspo", "Accessories", "MustHave", "Bag"], "analysis": "Everyday essential."},
    {"id": "1005005909802537", "name": "Phone Case Cute", "price": "$5.99", "rating": "4.8★", "reviews": "(15,000 reviews)", "tags": ["Trending", "TikTokViral", "PinterestFashion", "USATrends", "ViralFashion", "Trend2026", "StyleInspo", "Accessories", "MustHave", "PhoneCase"], "analysis": "Cute accessory."},
]

def get_day(): return datetime.now().strftime("%A").lower()
def get_date(): return datetime.now().strftime("%Y-%m-%d")
def get_times():
    now = datetime.now()
    return now.strftime("%I:%M %p"), (now + timedelta(hours=5)).strftime("%I:%M %p")

# Direct product link with US shipping parameter
def get_link(p):
    pid = p["id"]
    return f"https://www.aliexpress.com/item/{pid}.html?gatewayAdapt=glo2usa"

def get_product_url(pid):
    return f"https://www.aliexpress.com/item/{pid}.html?gatewayAdapt=glo2usa"

def select_products():
    date_str = get_date() + get_day()
    seed = int(hashlib.md5(date_str.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    female = FEMALE_PRODUCTS[:]
    general = GENERAL_PRODUCTS[:]
    random.shuffle(female)
    random.shuffle(general)
    return female[:3] + general[:2]

def send(text):
    if not TOKEN: return False
    t = text.replace("'", "'\\''").replace("\n", "\\n")
    cmd = f"""curl -s -X POST https://api.telegram.org/bot{TOKEN}/sendMessage -d "chat_id={CHAT_ID}" -d "text={t}" """
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=25)
        j = json.loads(r.stdout) if r.stdout else {}
        return j.get("ok", False)
    except: return False

def build_summary(products):
    us, pk = get_times()
    lines = [f"🌅 GOOD MORNING! 📅 {get_date()} | {get_day().title()}", f"⏰ Time: 🇺🇸 {us} US | 🇵🇰 {pk} Pakistan", f"🌍 GLOBAL SHIPPING AVAILABLE", f"", f"📊 TODAY'S TRENDING PRODUCTS", f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
    for i, p in enumerate(products, 1):
        cat = "FEMALE" if i <= 3 else "GENERAL"
        lines.append(f"👗 #{i} {cat} | {p['name']}")
        lines.append(f"🛒 {get_link(p)}")
    return "\n".join(lines)

def build_detail(p, idx):
    us, pk = get_times()
    times = ["6:45 AM", "9:45 AM", "11:45 AM", "2:45 PM", "6:45 PM"]
    cats = ["FEMALE", "FEMALE", "FEMALE", "GENERAL", "GENERAL"]
    lines = [f"{get_date()} | {cats[idx]}", f"PRODUCT #{idx+1}", f"👑 POST AT: {times[idx]} US | 7 hours Pakistan", f"", f"━━━"*12, f"TREND: {p['name']}", f"", f"👑 SEO PIN TITLE:", f"{p['name']} - Pinterest Viral Fashion Style", f"SEO DESCRIPTION:", f"TRENDING {p['name']} on Pinterest! {p['analysis']} Perfect for viral pins!", f"", f"FEMINIST ANALYSIS:", f"{p['analysis']}", f"", f"# 10 SEO HASHTAGS:"]
    for i, tag in enumerate(p['tags'], 1): lines.append(f"{i}. #{tag}")
    lines += [f"", f"📌 PRICE: {p['price']}", f"RATING: {p['rating']} {p['reviews']}", f"SHIPPING: FREE US Shipping", f"🌍 GLOBAL SHIPPING ✓", f"", f"🛒 CLICK TO BUY:", f"{get_link(p)}"]
    return "\n".join(lines)

def main():
    print(f"🕐 Agent - {get_date()} | {get_day().title()}")
    products = select_products()
    print(f"📦 {[p['name'] for p in products]}")
    print(f"\n📤 Sending...")
    send(build_summary(products))
    for i, p in enumerate(products):
        print(f"📤 Product {i+1}...")
        send(build_detail(p, i))
    print(f"\n✅ DONE!")

if __name__ == "__main__":
    main()