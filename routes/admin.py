from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db
from models import Product, Category, Customer, Order

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
def dashboard():

    products = Product.query.order_by(Product.created_at.desc()).all()

    total_products = Product.query.count()
    active_products = Product.query.filter_by(is_active=True).count()
    featured_products = Product.query.filter_by(featured=True).count()

    total_stock = sum((p.stock or 0) for p in products)

    low_stock = Product.query.filter(
        Product.stock <= 3,
        Product.is_active == True
    ).order_by(Product.stock.asc()).all()

    orders = Order.query.order_by(Order.created_at.desc()).limit(8).all()

    total_orders = Order.query.count()

    revenue = db.session.query(
        db.func.coalesce(db.func.sum(Order.total_price), 0)
    ).scalar()

    customers = Customer.query.count()

    return render_template(
        "admin/dashboard.html",
        products=products,
        total_products=total_products,
        active_products=active_products,
        featured_products=featured_products,
        total_stock=total_stock,
        low_stock=low_stock,
        orders=orders,
        total_orders=total_orders,
        revenue=revenue,
        customers=customers
    )


# =========================
# PRODUCTS
# =========================

@admin_bp.route("/products/new", methods=["GET", "POST"])
def new_product():

    if request.method == "POST":

        product = Product(
            name=request.form.get("name"),
            slug=request.form.get("slug"),
            price=int(request.form.get("price") or 0),
            stock=int(request.form.get("stock") or 0),
            category=request.form.get("category"),
            description=request.form.get("description"),
            featured=request.form.get("featured") == "on",
            is_active=True
        )

        db.session.add(product)
        db.session.commit()

        flash("محصول با موفقیت اضافه شد.", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template("admin/product_form.html")


@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":

        product.name = request.form.get("name")
        product.slug = request.form.get("slug")
        product.price = int(request.form.get("price") or 0)
        product.stock = int(request.form.get("stock") or 0)
        product.category = request.form.get("category")
        product.description = request.form.get("description")
        product.featured = request.form.get("featured") == "on"

        db.session.commit()

        flash("محصول ویرایش شد.", "success")

        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/product_form.html",
        product=product
    )


@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):

    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    flash("محصول حذف شد.", "success")

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/products/<int:product_id>/toggle", methods=["POST"])
def toggle_product(product_id):

    product = Product.query.get_or_404(product_id)

    product.is_active = not product.is_active

    db.session.commit()

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/products/<int:product_id>/featured", methods=["POST"])
def toggle_featured(product_id):

    product = Product.query.get_or_404(product_id)

    product.featured = not product.featured

    db.session.commit()

    return redirect(url_for("admin.dashboard"))


# =========================
# ORDERS
# =========================

@admin_bp.route("/orders")
def orders():

    orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "admin/orders.html",
        orders=orders
    )


@admin_bp.route("/orders/<int:order_id>/status", methods=["POST"])
def order_status(order_id):

    order = Order.query.get_or_404(order_id)

    order.status = request.form.get("status")

    db.session.commit()

    return redirect(url_for("admin.orders"))


# =========================
# CUSTOMERS
# =========================

@admin_bp.route("/customers")
def customers():

    customers = Customer.query.order_by(
        Customer.created_at.desc()
    ).all()

    return render_template(
        "admin/customers.html",
        customers=customers
    )


# =========================
# CATEGORIES
# =========================

@admin_bp.route("/categories", methods=["GET", "POST"])
def categories():

    if request.method == "POST":

        name = request.form.get("name")
        slug = request.form.get("slug")

        if name and slug:

            category = Category(
                name=name,
                slug=slug
            )

            db.session.add(category)
            db.session.commit()

            flash("دسته‌بندی اضافه شد.", "success")

        return redirect(url_for("admin.categories"))

    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    return render_template(
        "admin/categories.html",
        categories=categories
    )


@admin_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
def delete_category(category_id):

    category = Category.query.get_or_404(category_id)

    db.session.delete(category)
    db.session.commit()

    return redirect(url_for("admin.categories"))
