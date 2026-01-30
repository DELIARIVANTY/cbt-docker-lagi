from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def is_selected(teacher_id, assigned_id):
    """Check if teacher is selected for this class"""
    if assigned_id is None:
        return False
    return teacher_id == assigned_id
