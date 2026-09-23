from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "lunashid-admin-secret-2026"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/shop/")
def shop():
    return render_template("shop.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/favorites/")
def favorites():
    return render_template("empty.html", title="علاقه‌مندی‌ها", icon="♡", message="هنوز محصولی به علاقه‌مندی‌ها اضافه نشده است.")

@app.route("/cart/")
def cart():
    return render_template("empty.html", title="سبد خرید", icon="□", message="سبد خرید شما هنوز خالی است.")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/customer/")
def customer():
    return render_template("customer.html")

@app.route("/admin/")
def admin():
    return render_template("admin/dashboard.html")

@app.route("/admin/<section>/")
def admin_section(section):
    sections = {
        "products": "مدیریت محصولات",
        "add-product": "افزودن محصول",
        "categories": "دسته‌بندی‌ها",
        "orders": "سفارش‌ها",
        "order-details": "جزئیات سفارش",
        "customers": "مشتریان",
        "users": "مدیریت کاربران",
        "favorites": "علاقه‌مندی‌ها",
        "carts": "سبدهای خرید",
        "inventory": "موجودی انبار",
        "pricing": "قیمت‌گذاری",
        "discounts": "تخفیف‌ها",
        "coupons": "کدهای تخفیف",
        "payments": "پرداخت‌ها",
        "transactions": "تراکنش‌ها",
        "shipping": "ارسال و تحویل",
        "media": "مدیریت تصاویر",
        "gallery": "گالری",
        "reviews": "نظرات مشتریان",
        "messages": "پیام‌ها",
        "notifications": "اعلان‌ها",
        "homepage": "صفحه اصلی",
        "hero": "بنر و Hero",
        "about": "درباره لونا شید",
        "faq": "سؤالات متداول",
        "blog": "وبلاگ",
        "analytics": "آمار و گزارش‌ها",
        "settings": "تنظیمات سایت",
        "security": "امنیت و لاگ فعالیت‌ها"
    }

    title = sections.get(section, "بخش مدیریت")
    return render_template(
        "admin/section.html",
        title=title,
        section=section
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
