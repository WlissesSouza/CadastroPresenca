from django import template

register = template.Library()

classes_padrao_erro = "borda-vermelha"


@register.filter
def add_class(field, css_class):
    """
    Adiciona minha classe CSS padrao para os formularios
    """
    existing_classes = field.field.widget.attrs.get("class", "")
    field.field.widget.attrs[
        "class"] = f"{existing_classes} {css_class} {classes_padrao_erro if field.errors else ""}".strip()
    return field


@register.filter(name="add_style")
def add_style(field, css_style):
    """Adiciona estilo inline ao campo de formulário."""
    return field.as_widget(attrs={"style": css_style})
