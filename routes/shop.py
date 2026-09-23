from flask import Blueprint, render_template
from models import Product


shop_bp = Blueprint(
    "shop",
    __name__,
    url_prefix="/shop"
)


@shop_bp.route("/")
def shop():

    products = (
        Product.query
        .filter_by(is_active=True)
        .order_by(Product.created_at.desc())
        .all()
    )

    return render_template(
        "shop.html",
        products=products
    )


@shop_bp.route("/<slug>")
def product_detail(slug):

    product = (
        Product.query
        .filter_by(
            slug=slug,
            is_active=True
        )
        .first_or_404()
    )

    return render_template(
        "product.html",
        product=product
    )
