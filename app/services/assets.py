from flask_assets import Bundle, Filter
from webassets.filter import get_filter
import re


class ConcatFilter(Filter):
    """
    Filter that merges files, placing a semicolon between them.
    Fixes issues caused by missing semicolons at end of JS assets, for example
    with last statement of jquery.pjax.js.
    """

    def concat(self, out, hunks, **kw):
        out.write(";".join([h.data() for h, info in hunks]))


bs_icons = (
    get_filter(
        "cssrewrite",
        replace=lambda url: re.sub(
            r"./fonts/",
            "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/fonts/",
            url,
        ),
    ),
)


css_main = Bundle(
    "https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700,300italic,400italic,600italic",
    "https://fonts.googleapis.com/css?family=Roboto+Mono:400,300,700",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
    Bundle(
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.min.css",
        filters=bs_icons,
    ),
    "https://rawcdn.githack.com/darkterminal/tagin/6fa2863c13aa1841f33cf6dcbbf266c92fbf5412/dist/css/tagin.min.css",
    "https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css",
    output="css/main.css",
)

js_main = Bundle(
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js",
    # "https://rawcdn.githack.com/darkterminal/tagin/6fa2863c13aa1841f33cf6dcbbf266c92fbf5412/dist/js/tagin.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js",
    "https://cdn.jsdelivr.net/momentjs/latest/moment.min.js",
    "https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/floatthead/2.2.4/jquery.floatThead.min.js",
    output="js/main.js",
)

js_custom = Bundle(
    "../app/ressources/js/custom.js", filters="rjsmin", output="js/custom.js"
)
css_custom = Bundle(
    "../app/ressources/css/custom.css", filters="cssmin", output="css/custom.css"
)
