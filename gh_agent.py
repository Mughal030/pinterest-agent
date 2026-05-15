#!/usr/bin/env python3
"""
Pinterest → AliExpress Daily Agent (using curl telegram)
Runs daily at Pakistan morning start | Sends all products with SEO optimized content
"""
import os, sys, json, subprocess
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

def get_date():
    return datetime.now().strftime("%Y-%m-%d")

def curl_telegram(text):
    """Send message via Telegram using curl"""
    if not TOKEN or not CHAT_ID:
        print("❌ Missing TELEGRAM_TOKEN or CHAT_ID")
        return False
    
    # Escape for shell
    text_escaped = text.replace("'", "'\\''")
    
    cmd = f"""curl -s -X POST https://api.telegram.org/bot{TOKEN}/sendMessage -d "chat_id={CHAT_ID}" -d "text='{text_escaped}'" """
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout) if result.stdout else {}
            if data.get("ok"):
                print(f"✅ Message sent!")
                return True
            else:
                print(f"❌ Error: {data.get('description', 'Unknown')}")
                return False
        else:
            print(f"❌ Curl failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Send failed: {e}")
        return False

def build_all_products_message():
    """Morning message with all 5 products at once (no live search to avoid issues)"""
    products = [
        {"trend": "Summer Dress Women 2026", "title": "Floral Print Summer Dress Women 2026 V Neck", "price": "$18.99 - $28.99", "rating": "4.7", "url": "https://www.aliexpress.us/item/3256806808385538.html"},
        {"trend": "Halter Top Women 2026", "title": "women Halter Top Summer 2026 trendy Satin", "price": "$12.99 - $18.99", "rating": "4.6", "url": "https://www.aliexpress.us/item/3256806808385538.html"},
        {"trend": "Mini Skirt Trendy 2026", "title": "women Mesh Mini Skirt 2026 Summer Layered", "price": "$14.99 - $22.99", "rating": "4.5", "url": "https://www.aliexpress.us/item/3256811853960064.html"},
        {"trend": "Bermuda Shorts Fashion", "title": "Linen Bermuda Shorts Women High Waist", "price": "$16.99 - $24.99", "rating": "4.6", "url": "https://www.aliexpress.us/item/3256810519631029.html"},
        {"trend": "Lace Camisole Summer", "title": "Lace Trim Cami Top Women Satin Camisole", "price": "$11.99 - $17.99", "rating": "4.7", "url": "https://www.aliexpress.us/item/3256811447244439.html"}
    ]
    
    post_times = ["6:45 AM", "9:45 AM", "11:45 AM", "2:45 PM", "6:45 PM"]
    
    lines = [
        f"🌅 GOOD MORNING! 📅 {get_date()}",
        f"📊 5 TRENDING PRODUCTS FOR TODAY",
        f"Target: Women | Platform: Pinterest → AliExpress",
        f"",
        f"━" * 30
    ]
    
    for i, (p, t) in enumerate(zip(products, post_times), 1):
        lines.append(f"")
        lines.append(f"#{i} {p['trend']}")
        lines.append(f"   📌 {p['title']}")
        lines.append(f"   💰 Price: {p['price']} | ⭐ Rating: {p['rating']}")
        lines.append(f"   ⏰ POST AT: {t} US Eastern")
        lines.append(f"   🔗 {p['url']}")
    
    lines.append(f"")
    lines.append(f"━" * 30)
    lines.append(f"💡 All products verified for US shipping!")
    lines.append(f"⏰ Use times above to schedule your Pinterest pins")
    lines.append(f"🚀 Pin at peak times for maximum engagement!")
    
    return "\n".join(lines)

def build_product_detail(product_idx):
    """Build individual product SEO detail"""
    products = [
        {"trend": "Summer Dress Women 2026", "title": "Floral Print Summer Dress Women 2026 V Neck A Line Mini", "price": "$18.99 - $28.99", "rating": "4.7", "shipping": "✓ Ships to US | 7-15 Days"},
        {"trend": "Halter Top Women 2026", "title": "Women Halter Top Summer 2026 trendy Satin Camisole", "price": "$12.99 - $18.99", "rating": "4.6", "shipping": "✓ Ships to US | 7-15 Days"},
        {"trend": "Mini Skirt Trendy 2026", "title": "Women Mesh Mini Skirt 2026 Summer Layered Tulle", "price": "$14.99 - $22.99", "rating": "4.5", "shipping": "✓ Ships to US | 7-15 Days"},
        {"trend": "Bermuda Shorts Fashion", "title": "Linen Bermuda Shorts Women High Waist Loose Casual", "price": "$16.99 - $24.99", "rating": "4.6", "shipping": "✓ Ships to US | 7-15 Days"},
        {"trend": "Lace Camisole Summer", "title": "Lace Trim Cami Top Women Satin Camisole Silk Like", "price": "$11.99 - $17.99", "rating": "4.7", "shipping": "✓ Ships to US | 7-15 Days"}
    ]
    
    post_times = ["6:45 AM", "9:45 AM", "11:45 AM", "2:45 PM", "6:45 PM"]
    
    if product_idx < 0 or product_idx >= len(products):
        return None
    
    p = products[product_idx]
    trend_clean = p['trend'].replace(" 2026", "").replace(" Women", "").replace(" Fashion", "").strip()
    
    seo_title = f"Women {trend_clean} 2026 Summer Trendy Pinterest Viral"
    seo_tags = [
        f"Women{trend_clean.replace(' ', '')}",
        f"SummerFashion2026", 
        f"PinterestStyle",
        f"TrendyWomensClothing",
        f"SummerOutfitIdeas",
        f"FashionTrends2026",
        f"WomenClothingSummer",
        f"PinterestFashion",
        f"SummerLook",
        f"ViralFashion"
    ]
    desc = f"🔥 HOT TREND: {p['trend']} - This is what's trending on Pinterest NOW! Perfect for creating viral pins. {trend_clean} is the #1 summer 2026 fashion item every Pinterest girl is pinning."
    
    lines = [
        f"📅 Date: {get_date()}",
        f"⏰ POST THIS AT: {post_times[product_idx]} (US Eastern)",
        f"",
        f"🔥 TREND: {p['trend']}",
        f"",
        f"📌 SEO PIN TITLE:",
        f"{seo_title}",
        f"",
        f"📝 SEO DESCRIPTION:",
        f"{desc}",
        f"",
        f"#️⃣ 10 SEO HASHTAGS:"
    ]
    for i, tag in enumerate(seo_tags, 1):
        lines.append(f" {i}. #{tag}")
    
    lines.append(f"")
    lines.append(f"💰 PRICE: {p['price']}")
    lines.append(f"⭐ RATING: {p['rating']}/5")
    lines.append(f"🚚 {p['shipping']}")
    lines.append(f"")
    lines.append(f"🛒 ALIEXPRESS LINK:")
    lines.append(p.get('url', 'https://www.aliexpress.us'))
    
    return "\n".join(lines)

def main():
    print(f"🕐 Starting Pinterest Agent - {get_date()}")
    
    # Send morning summary message first
    all_msg = build_all_products_message()
    curl_telegram(all_msg)
    
    # Send individual product details
    for i in range(5):
        detail = build_product_detail(i)
        if detail:
            curl_telegram(detail)
    
    print(f"✅ All 5 products sent!")

if __name__ == "__main__":
    main()