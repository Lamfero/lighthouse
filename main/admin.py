from django.contrib import admin
from main.models import Users, Orders, Service, UserSettings, ProfileViews, BankDetalis, DiplomsSertificats
from tariffs.models import TariffSettings
# Register your models here.


admin.site.register(Users)
admin.site.register(Orders)
admin.site.register(Service)
admin.site.register(UserSettings)
admin.site.register(ProfileViews)
admin.site.register(BankDetalis)
admin.site.register(DiplomsSertificats)
admin.site.register(TariffSettings)