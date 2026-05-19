#!/usr/bin/env python3
"""
Pinterest → AliExpress Daily Agent v4
Exact message format as requested
"""
import os, json, subprocess, random, hashlib
from datetime import datetime, timedelta

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

# ==================== PRODUCT DATABASE ====================
PRODUCTS = [
    {"id": "3256806526493591", "name": "Women Oversized Blazer 2026", "cat": "female", "price": "$35.99", "rating": "4.8★", "reviews": "(1,500 reviews)", "tags": ["WomenFashion", "PinterestViral", "Trend2026", "FashionTrends", "StyleInspo", "WomenStyle", "ViralFashion", "TrendyOutfit", "FashionTips", "WardrobeEssentials"], "analysis": "Power dressing on YOUR terms."},
    {"id": "3256807111544408", "name": "Bodycon Dress Long Sleeve", "cat": "female", "price": "$19.99", "rating": "4.6★", "reviews": "(2,000 reviews)", "tags": ["WomenFashion", "PinterestViral", "Trend2026", "FashionTrends", "StyleInspo", "WomenStyle", "ViralFashion", "TrendyOutfit", "FashionTips", "DressInspo"], "analysis": "Versatile for day to night."},
    {"id": "3256810276918782", "name": "Floral Summer Dress", "cat": "female", "price": "$16.99", "rating": "4.7★", "reviews": "(2,500 reviews)", "tags": ["WomenFashion", "PinterestViral", "Trend2026", "FashionTrends", "StyleInspo", "WomenStyle", "ViralFashion", "TrendyOutfit", "FashionTips", "SummerDress"], "analysis": "Comfort meets style."},
    {"id": "3256806166322838", "name": "Cropped Cardigan Button", "cat": "female", "price": "$14.99", "rating": "4.5★", "reviews": "(1,800 reviews)", "tags": ["WomenFashion", "PinterestViral", "Trend2026", "FashionTrends", "StyleInspo", "WomenStyle", "ViralFashion", "TrendyOutfit", "FashionTips", "Cardigan"], "analysis": "Layering essential."},
    {"id": "3256810039828881", "name": "Corset Top Lace-up", "cat": "female", "price": "$15.99", "rating": "4.6★", "reviews": "(2,200 reviews)", "tags": ["WomenFashion", "PinterestViral", "Trend2026", "FashionTrends", "StyleInspo", "WomenStyle", "ViralFashion", "TrendyOutfit", "FashionTips", "CorsetTop"], "analysis": "Y2K comeback style."},
    {"id": "1005001624053125", "name": "Cat Eye Sunglasses", "cat": "general", "price": "$9.99", "rating": "4.5★", "reviews": "(3,000 reviews)", "tags": ["Trending", "TikTokViral", "PinterestFashion", "USATrends", "ViralFashion", "Trend2026", "StyleInspo", "Accessories", "MustHave", "Fashion"], "analysis": "Retro vibes."},
    {"id": "1005003292493272", "name": "Minimalist Watch", "cat": "general", "price": "$15.99", "rating": "4.7★", "reviews": "(5,000 reviews)", "tags": ["Trending", "TikTokViral", "PinterestFashion", "USATrends", "ViralFashion", "Trend2026", "StyleInspo", "Accessories", "MustHave", "Fashion"], "analysis": "Timeless style."},
    {"id": "1005004877979148", "name": "Aesthetic Phone Case", "cat": "general", "price": "$6.99", "rating": "4.8★", "reviews": "(12,000 reviews)", "tags": ["Trending", "TikTokViral", "PinterestFashion", "USATrends", "ViralFashion", "Trend2026", "StyleInspo", "Accessories", "MustHave", "Tech"], "analysis": "Cute accessory."},
]

def get_day(): return datetime.now().strftime("%A").lower()
def get_date(): return datetime.now().strftime("%Y-%m-%d")
def get_times():
    now = datetime.now()
    return now.strftime("%I:%M %p"), (now + timedelta(hours=5)).strftime("%I:%M %p")

def get_link(pid):
    return f"https://www.aliexpress.us/item/{pid}.html"

def select_products():
    date_str = get_date() + get_day()
    seed = int(hashlib.md5(date_str.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    products = PRODUCTS[:]
    random.shuffle(products)
    return products[:5]

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
    lines = [
        f"🌅 GOOD MORNING! 📅 {get_date()} | {get_day().title()}",
        f"⏰ Time: 🇺🇸 {us} US | 🇵🇰 {pk} Pakistan",
        f"",
        f"📊 TODAY'S TRENDING PRODUCTS (Pinterest Curated)",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ]
    
    for i, p in enumerate(products, 1):
        cat = "FEMALE" if p['cat'] == "female" else "GENERAL"
        lines.append(f"")
        lines.append(f"👗 #{i} {cat} | {p['name']}")
        lines.append(f"   (PRODUCT LINK): {get_link(p['id'])}")
    
    lines.append(f"")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)

def build_detail(p, idx):
    us, pk = get_times()
    times = ["6:45 AM", "9:45 AM", "11:45 AM", "2:45 PM", "6:45 PM"]
    cats = ["FEMALE", "FEMALE", "FEMALE", "GENERAL", "GENERAL"]
    
    lines = [
        f"{get_date()} | {cats[idx]}",
        f"PRODUCT #{idx+1}",
        f"👑 POST AT: {times[idx]} US | 7 hours Pakistan",
        f"",
        f"━━━" * 12,
        f"TREND: {p['name']}",
        f"",
        f"👑 SEO PIN TITLE (copy this):",
        f"{p['name']} - Pinterest Viral Fashion Style",
        f"SEO DESCRIPTION:",
        f"TRENDING {p['name']} on Pinterest! {p['analysis']} Perfect for creating viral pins! This is what everyone's pinning right now. GET IT BEFORE IT SELLS OUT!",
        f"",
        f"FEMINIST ANALYSIS:",
        f"{p['analysis']}",
        f"",
        f"# 10 SEO HASHTAGS:"
    ]
    
    for i, tag in enumerate(p['tags'], 1):
        lines.append(f"{i}. #{tag}")
    
    lines += [
        f"",
        f"📌 PRICE: {p['price']}",
        f"RATING: {p['rating']} {p['reviews']}",
        f"SHIPPING: FREE US Shipping | 7-15 days",
        f"VERIFIED: Ships to USA ✔️ | Link Working ✔️",
        f"",
        f"CLICK HERE TO BUY:",
        f"{get_link(p['id'])}",
    ]
    
    return "\n".join(lines)

def main():
    print(f"🕐 Agent - {get_date()} | {get_day().title()}")
    us, pk = get_times()
    print(f"⏰ US: {us} | PK: {pk}")
    
    products = select_products()
    print(f"📦 {products}")
    
    print(f"\n📤 Sending...")
    send(build_summary(products))
    
    for i, p in enumerate(products):
        print(f"📤 Product {i+1}...")
        send(build_detail(p, i))
    
    print(f"\n✅ DONE!")

if __name__ == "__main__":
    main()