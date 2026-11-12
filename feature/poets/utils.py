def format_poet_list_item(poet, era_name: str, poem_count: int):
    """تنسيق الشاعر في القائمة العامة"""
    return {
        "id": poet.id,
        "name": poet.name,
        "era_name": era_name,
        "poem_count": poem_count 
    }

def format_poet_detail(poet, era_name: str, poem_count: int, top_meters: list):
    """تنسيق تفاصيل الشاعر مع إحصاءاته"""
    return {
        "id": poet.id,
        "name": poet.name,
        "era_name": era_name,
        "statistics": {
            "total_poems": poem_count,
            "favorite_meters": top_meters
        }
    }

def format_poet_poem_item(poem, meter_name:str):
    """تنسيق القصيدة عند عرضها في قائمة قصائد الشاعر"""
    return {
        "id": poem.id,
        "title": poem.title,
        "verse_count": poem.verse_count,
        "meter": meter_name,
        "url": poem.url,
    }