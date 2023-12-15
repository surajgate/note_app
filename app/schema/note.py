def noteEntity(item) -> dict:
    return {
        "id": str(item["id"]),
        "title": item["title"],
        "important": item["important"]
    }


def notesEntity(items) -> list:
    return [noteEntity(item) for item in items]
