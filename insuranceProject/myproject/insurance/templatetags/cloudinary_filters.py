from django import template

register = template.Library()


@register.filter
def optimize_cloudinary(url):
    if not url or "cloudinary" not in url:
        return url
    return url.replace('/upload', '/upload/f_auto,q_auto,w_1200/')