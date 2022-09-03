from nturl2path import url2pathname
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.view_user_profile_by_telegram_id_by_owner, name="profile"),
    path("<int:telegram_id_for_view>", views.view_user_profile_by_telegram_id_from_outside, name="view_profie_from_outside")
]