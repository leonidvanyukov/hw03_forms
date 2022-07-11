from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    currentyear = datetime.now().year
    return {
        'year': currentyear
    }
