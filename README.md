# ONETJobs Education Scraper

یک اسکریپت پایتون برای استخراج خودکار اطلاعات رشته‌های تحصیلی از وب‌سایت [onetjobs.ir](https://onetjobs.ir/education).

داده‌های استخراج‌شده شامل نام رشته، مقطع، توضیحات و پیش‌نیازها در یک فایل Excel ذخیره می‌شوند.

## ⚙️ نحوه کار
- لیست رشته‌ها با Playwright و scroll خودکار بارگذاری می‌شود.
- کاربر باید **دستی** فیلترهای مقطع (کاردانی، کارشناسی، کارشناسی ارشد) را در صفحه اعمال کند و پس از لود کامل نتایج، در ترمینال `now` را تایپ کند.
- اسکریپت لینک‌ها را استخراج کرده و اطلاعات تک‌تک رشته‌ها را جمع‌آوری می‌کند.
- داده‌ها در فایل `onet_education_public_fields.xlsx` ذخیره می‌شوند (لینک‌های تکراری نادیده گرفته می‌شوند).

## 📦 پیش‌نیازها
- **Python 3.8+**
- **Playwright** به همراه مرورگر Chromium

### نصب
1. مخزن را کلون کنید:
   ```bash
   git clone https://github.com/MashHossaini/python-web-scraping-project.git
   cd python-web-scraping-project
   ```

2. کتابخانه‌های پایتون را نصب کنید:
   ```bash
   pip install -r requirements.txt
   ```

3. **مرورگر Chromium را برای Playwright نصب کنید**  
   (این مرحله ضروری است، چون Playwright بدون نصب مرورگر اجرا نمی‌شود):
   ```bash
   playwright install chromium
   ```

## 🚀 اجرا
```bash
python scraper.py
```
بعد از اجرا، پنجره مرورگر باز می‌شود. فیلترهای تحصیلی را اعمال کنید، منتظر بارگذاری کامل نتایج بمانید، سپس در ترمینال دستور `now` را تایپ کنید.

برای توقف اسکریپت می‌توانید `Ctrl+C` بزنید.

## 📂 خروجی
فایل `onet_education_public_fields.xlsx` با ستون‌های زیر ایجاد می‌شود:
- `field_name` → نام رشته
- `degree` → مقطع تحصیلی
- `share_link` → لینک صفحه رشته
- `description` → توضیحات رشته
- `prerequisites` → پیش‌نیازها (دیپلم‌های مورد نیاز)
- `updated_at` → زمان استخراج

## ⚠️ نکات اخلاقی و حقوقی
این پروژه **صرفاً برای اهداف آموزشی** و نمایش توانایی برنامه‌نویسی ساخته شده است. لطفاً به فایل `robots.txt` و قوانین وب‌سایت احترام بگذارید و از آن برای مقاصد غیرقانونی یا سوءاستفاده استفاده نکنید.

## 👤 نویسنده
- **نام کامل:** Masoomeh Hossaini
- **گیت‌هاب:** [@MashHossaini](https://github.com/MashHossaini)
- **لینکدین:** [Masoomeh Hosseini](https://linkedin.com/in/masoomeh-hosseini25)
