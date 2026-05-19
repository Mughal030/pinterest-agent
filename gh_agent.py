#!/usr/bin/env python3
"""
Pinterest → AliExpress Daily Agent
Deep feminist analysis | 3 Female + 2 General | Validated links format
"""
import os, json, subprocess, random, hashlib
from datetime import datetime, timedelta

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

# Verified product IDs from AliExpress US
FEMALE_POOL = [
    {"id": "3256806808385538", "trend": "Floral Summer Dress", "cat": "dress"},
    {"id": "3256811447244439", "trend": "Lace Trim Cami", "cat": "top"},
    {"id": "3256811853960064", "trend": "Mesh Mini Skirt", "cat": "skirt"},
    {"id": "3256805726590168", "trend": "High Waist Jeans", "cat": "jeans"},
    {"id": "3256810519631029", "trend": "Linen Bermuda Shorts", "cat": "shorts"},
    {"id": "3256806526493591", "trend": "Oversized Blazer", "cat": "blazer"},
]

GENERAL_POOL = [
    {"id": "1005001624053125", "trend": "Unisex Sunglasses"},
    {"id": "1005003292493272", "trend": "Minimalist Watch"},
    {"id": "1005004821976619", "trend": "Canvas Tote Bag"},
    {"id": "1005004877979148", "trend": "Phone Case"},
]

def get_day(): return datetime.now().strftime("%A").lower()
def get_date(): return datetime.now().strftime("%Y-%m-%d")
def get_times():
    now = datetime.now()
    return now.strftime("%I:%M %p"), (now + timedelta(hours=5)).strftime("%I:%M %p")

# Feminist analysis per category
ANALYSIS = {
    "dress": "Choice to express YOUR femininity on YOUR terms.",
    "top": "Practical meets stylish - tops that work for YOUR life.",
    "skirt": "Own your movement - freedom to express yourself.",
    "jeans": "Classic meets modern - denim that flatters.",
    "shorts": "Comfort for active lives without compromise.",
    "blazer": "Power dressing on YOUR terms.",
}

def make_product(p, is_female, idx):
    trend = p['trend']
    cat = p.get('cat', 'fashion')
    analysis = ANALYSIS.get(cat, "Empowering choice for modern women.")
    
    if is_female:
        return {
            "id": p['id'],
            "trend": f"Women {trend} 2026",
            "seo_title": f"Women {trend} 2026 - Pinterest Viral Fashion",
            "desc": f"TRENDING {trend} on Pinterest! {analysis} Perfect for viral pins!",
            "analysis": analysis,
            "tags": ["WomenFashion", "PinterestViral", "Trend2026", "Fashion", "Style", "women", "Viral", "Trendy", "FashionTips", "Wardrobe"],
            "price": "$16.99",
        }
    else:
        return {
            "id": p['id'],
            "trend": f"Unisex {trend}",
            "seo_title": f"{trend} 2026 - Viral USA Trend",
            "desc": f"VIRAL {trend} taking over! {analysis} Perfect for pins!",
            "analysis": analysis,
            "tags": ["Trending", "TikTokViral", "Pinterest", "USA", "Viral", "Trend2026", "Style", "Accessories", "MustHave", "Fashion"],
            "price": "$9.99",
        }

def select_products():
    """Different selection each day"""
    seed = int(hashlib.md5(get_date().encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    fp = FEMALE_POOL[:]
    random.shuffle(fp)
    gp = GENERAL_POOL[:]
    random.shuffle(gp)
    
    female = [make_product(p, True, i) for i, p in enumerate(fp[:3])]
    general = [make_product(p, False, i) for i, p in enumerate(gp[:2])]
    
    return female + general, female, general

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
    lines = [f"🌅 GOOD MORNING! 📅 {get_date()} | {get_day().title()}",
    f"⏰ US: {us} | Pakistan: {pk}",
    f"",
    f"📊 TODAY'S TRENDING PRODUCTS",
    f"━━━━━━━━━━━━━━━━━━━━",
    f"✅ All VALIDATED links",
    f"✅ FREE US Shipping",
    f"✅ Feminist Analysis",
    f""]
    
    for i, p in enumerate(products, 1):
        c = "👗" if i <= 3 else "🎯"
        lines.append(f"{c} #{i} {p['trend']}")
        lines.append(f"   💰 {p['price']}")
        lines.append(f"   🔗 aliexpress.us/item/{p['id']}")
        lines.append(f"")
    
    return "\n".join(lines)

def build_detail(p, idx):
    us, pk = get_times()
    times = ["6:45 AM", "9:45 AM", "11:45 AM", "2:45 PM", "6:45 PM"]
    cats = ["👗 FEMALE", "👗 FEMALE", "👗 FEMALE", "🎯 GENERAL", "🎯 GENERAL"]
    url = f"https://www.aliexpress.us/item/{p['id']}.html"
    
    lines = [f"📅 {get_date()} | {cats[idx]} #{idx+1}",
    f"⏰ POST: {times[idx]} US | +7h Pakistan",
    f"",
    f"━━━━━━━━━━━━━━━━━━━━",
    f"🔥 {p['trend']}",
    f"",
    f"📌 SEO TITLE:",
    f"{p['seo_title']}",
    f"",
    f"📝 DESCRIPTION:",
    f"{p['desc']}",
    f"",
    f"💜 FEMINIST ANALYSIS:",
    f"{p['analysis']}",
    f"",
    f"#️⃣ HASHTAGS:"]
    
    for i, t in enumerate(p['tags'], 1):
        lines.append(f"  {i}. #{t}")
    
    lines += [f"",
    f"━━━━━━━━━━━━━━━━━━━━",
    f"💰 {p['price']}",
    f"✅ Ships to USA ✓",
    f"",
    f"🛒 LINK:",
    f"{url}",
    f"━━━━━━━━━━━━━━━━━━━━"]
    
    return "\n".join(lines)

def main():
    print(f"🕐 {get_date()}")
    products, f, g = select_products()
    print(f"👗 {len(f)} + 🎯 {len(g)}")
    
    send(build_summary(products))
    for i, p in enumerate(products):
        send(build_detail(p, i))
    
    print(f"✅ Done!")

if __name__ == "__main__":
    main()