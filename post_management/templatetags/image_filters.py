from django import template

register = template.Library()

@register.filter
def thumbnail_url(image_url):
    """
    Original image URL ko thumbnail URL me convert karega.
    Example:
    /media/upload/photo.jpg  ->  /media/upload/thumbnails/photo.jpg
    """
    if not image_url:
        return image_url

    # URL ko parts me tod do
    parts = str(image_url).split("/")
    filename = parts[-1]           # photo.jpg
    folder = "/".join(parts[:-1])  # /media/upload

    # Us folder ke andar thumbnails subfolder assume karo
    return f"{folder}/thumbnails/{filename}"