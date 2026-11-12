# poems/utils.py

def format_poem_list_item(poem, poet_name, meter_name, era_name, topics_dict):
    """تنسيق القصيدة في القائمة (بدون أبيات)"""
    
    # ترجمة الـ topic_ids إلى أسماء
    topic_names = [topics_dict.get(t_id, "غير معروف") for t_id in poem.topic_ids]
    
    return {
        "id": poem.id,
        "title": poem.title,
        "verse_count": poem.verse_count,
        "poet_name": poet_name,
        "meter_name": meter_name,
        "era_name": era_name or "غير محدد",
        "topics": topic_names,
        "url": poem.url,
    }

def format_poem_detail(poem, poet, era_name, meter, topics):
    """
    تنسيق القصيدة عند عرض تفاصيلها (GET /poems/{id})
    """
    return {
        "id": poem.id,
        "title": poem.title,
        "poet": {
            "id": poet.id,
            "name": poet.name,
            "era_name": era_name
        },
        "meter": {
            "id": meter.id,
            "name": meter.name
        },
        "topics": [{"id": t.id, "name": t.name} for t in topics],
        "verse_count": poem.verse_count,
        "verses": poem.verses,
        "url": poem.url
    }