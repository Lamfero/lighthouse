from main.models import Users


def update_secret_key(telegram_id, secret_key):
    if Users.objects.filter(telegram_id=telegram_id).exists():
        user_db = Users.objects.get(telegram_id=telegram_id)
        user_db.secret_key = secret_key
        user_db.save()
        return True
    else:
        return False