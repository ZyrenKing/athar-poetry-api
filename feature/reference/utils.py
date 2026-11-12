def format_reference_item(item):
    """تنسيق بيانات المرجع ليكون نظيفاً (id و name فقط)"""
    return {
        "id": item.id,
        "name": item.name
    }