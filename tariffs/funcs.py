from .models import TariffSettings
from main.models import Users, UserTariff
from datetime import date, timedelta
from dateutil.relativedelta import * 


def check_exist_user(telegram_id, secret_key):
    
    if Users.objects.filter(telegram_id = telegram_id, secret_key=secret_key).exists():
        db = Users.objects.get(telegram_id=telegram_id)
        if db.select != 'registration':
            return True
    return False


def get_all_tariffs():
    tariffs = TariffSettings.objects.filter()
    if len(tariffs) == 3:
        pass
    else:
        tariff_standart_db = TariffSettings(name="Стандарт", level=1, description="Тариф Стандарт", price="999")
        tariff_standart_db.save()
        tariff_extented_db = TariffSettings(name="Расширенный", level=2, description="Тариф Расширенный", price="1999")
        tariff_extented_db.save()
        tariff_pro_db = TariffSettings(name="PRO", level=3, description="Тариф PRO", price="2999")
        tariff_pro_db.save()
    tariffs = TariffSettings.objects.filter()
    return tariffs


def get_tariff_by_name(tariff_name):
    tariff = TariffSettings.objects.filter(name=tariff_name)
    if len(tariff) > 0:
        return TariffSettings.objects.get(name=tariff_name)
    else:
        return None


def get_user_balance(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    return int(db.balance)


def withdraw_from_user_balance(telegram_id, sum):
    db = Users.objects.get(telegram_id=telegram_id)
    db.balance = int(db.balance) - int(sum)
    db.save()


def check_possibility_of_set_tariff(telegram_id, tariff_name):
    tariff_db = get_tariff_by_name(tariff_name=tariff_name)
    if tariff_db != None:
        db = Users.objects.get(telegram_id=telegram_id)
        tariffs_db = UserTariff.objects.filter(user=db)
        for tariff in tariffs_db:
            split_date = tariff.runs_until.rsplit("-")
            today = date.today()
            dob = date(int(split_date[0]), int(split_date[1]), int(split_date[2])) 
            difference = relativedelta(today, dob)
            if int(tariff_db.level) >= int(tariff.tariff.level):
                if difference.days >= 0:
                    return False
            else:
                return False
        return True
    else:
        return False


def add_tariff(telegram_id, tariff_name):
    tariff_db = get_tariff_by_name(tariff_name=tariff_name)
    if tariff_db != None:
        db = Users.objects.get(telegram_id=telegram_id)
        new_tariff_db = UserTariff(user = db, tariff = tariff_db, runs_until=str(date.today() + timedelta(days=30)))
        new_tariff_db.save()