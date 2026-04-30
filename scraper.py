import asyncio
import random
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

EXCEL_FILE = "onet_education_public_fields.xlsx"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# -------------------------------------------------------
# Load existing links
# -------------------------------------------------------
def load_existing_links():
    if not Path(EXCEL_FILE).exists():
        return set()
    try:
        df = pd.read_excel(EXCEL_FILE)
        if "share_link" in df.columns:
            return set(df["share_link"].dropna().astype(str).tolist())
    except:
        pass
    return set()

# -------------------------------------------------------
# Save records
# -------------------------------------------------------
def save_append(records):
    if not records:
        return
    df_new = pd.DataFrame(records)
    if Path(EXCEL_FILE).exists():
        df_old = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_excel(EXCEL_FILE, index=False)
    logging.info(f"ذخیره شد: {len(records)} رکورد جدید")

# -------------------------------------------------------
# Human scroll
# -------------------------------------------------------
async def human_scroll(page):
    for _ in range(20):
        await page.mouse.wheel(0, random.randint(900, 1500))
        await asyncio.sleep(random.uniform(1.5, 3))

# -------------------------------------------------------
# Extract links from list page
# -------------------------------------------------------
async def extract_links(page):
    links = set()
    for a in await page.query_selector_all("a"):
        href = await a.get_attribute("href") or ""
        if "/education/" in href and href.count("/") >= 2:
            full = "https://onetjobs.ir" + href if href.startswith("/") else "https://onetjobs.ir/" + href
            links.add(full)
    return list(links)

# -------------------------------------------------------
# Extract details — نسخه فوق‌العاده دقیق و تست‌شده ۲۰۲۵
# -------------------------------------------------------
async def extract_details(page, url):
    await page.goto(url, wait_until="networkidle", timeout=90000)
    await asyncio.sleep(4)

    record = {
        "field_name": "",
        "degree": "",
        "share_link": url,
        "description": "",
        "prerequisites": "",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # ۱. نام رشته
    try:
        record["field_name"] = await page.locator("h1").inner_text(timeout=10000)
        record["field_name"] = record["field_name"].strip()
    except:
        record["field_name"] = "نامشخص"

    # ۲. مقطع — دقیق‌ترین selector ممکن
    try:
        degree = await page.locator("dt:-soup-contains('مقطع') + dd").inner_text(timeout=8000)
        record["degree"] = degree.strip()
    except:
        try:
            degree = await page.locator("text=مقطع >> xpath=../following-sibling::*").first.inner_text(timeout=5000)
            record["degree"] = degree.strip()
        except:
            record["degree"] = "نامشخص"

    # ۳. توضیحات رشته — بخش اصلی معرفی
    try:
        desc = await page.locator("div.prose, section.prose, div[class*='prose'], div[data-slot='description']").first.inner_text(timeout=10000)
        if len(desc) > 50:
            record["description"] = desc.strip()
    except:
        try:
            paragraphs = await page.locator("main p, article p, div.relative p").all_inner_texts()
            clean = [p.strip() for p in paragraphs if len(p.strip()) > 30 and "رأی" not in p and "اشتراک" not in p]
            record["description"] = " ".join(clean[:8])
        except:
            record["description"] = ""

    # ۴. پیش‌نیازها — دقیق و بدون خطا
    prereqs = []
    try:
        cards = await page.locator("div.grid >> div.bg-white, div.rounded-xl, div.rounded-lg, div.border").all()
        for card in cards:
            text = await card.inner_text(timeout=4000)
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            if len(lines) >= 2 and "دیپلم" in lines[1]:
                branch = lines[0].replace("دیپلم", "").strip()
                if branch:
                    prereqs.append(branch)
        record["prerequisites"] = " | ".join(prereqs) if prereqs else "همه رشته‌ها"
    except:
        record["prerequisites"] = "نامشخص"

    logging.info(f"✓ {record['field_name']} | {record['degree']} | {record['prerequisites']}")
    return record

# -------------------------------------------------------
# Wait for user
# -------------------------------------------------------
async def wait_for_user_ready():
    print("\n" + "="*70)
    logging.info("فیلتر رو دستی بزن (کاردانی + کارشناسی + کارشناسی ارشد)")
    logging.info("وقتی نتایج کامل لود شد، در ترمینال تایپ کن: now")
    print("="*70)
    while True:
        if input(">> ").strip().strip().lower() == "now":
            logging.info("ادامه...")
            await asyncio.sleep(2)
            break

# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
async def main():
    existing = load_existing_links()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        context = await browser.new_context(viewport=None)
        page = await context.new_page()

        await page.goto("https://onetjobs.ir/education", wait_until="networkidle")
        await wait_for_user_ready()

        while True:
            await human_scroll(page)
            links = await extract_links(page)
            new = [l for l in links if l not in existing]

            logging.info(f"جدید: {len(new)} از {len(links)}")

            for url in new:
                data = await extract_details(page, url)
                if data:
                    save_append([data])  # ذخیره فوری
                    existing.add(url)

            await page.goto("https://onetjobs.ir/education", wait_until="networkidle")
            await wait_for_user_ready()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nتوقف دستی")