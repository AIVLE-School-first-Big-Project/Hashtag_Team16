from django.urls import path
from member.views import mypage, modify, user, login_custom, signup_custom, logout_custom, change_password, change_info
from member.views import RecoveryIdView, ajax_find_id_view , RecoveryPwView, ajax_find_pw_view, auth_confirm_view, auth_pw_reset_view, information
app_name = 'member'

urlpatterns = [
    path('', mypage, name='mypage'),
    path('modify/', modify, name='modify'),
    
    path('line/', user, name='line'),
    path('login/', login_custom, name='login_custom'),
    path('signup/', signup_custom, name='signup_custom'),
    path('logout/', logout_custom, name='logout_custom'),
    path('changepw/', change_password, name='change_password'),
    path('changeinfo/', change_info, name='change_info'),
    path('recovery/id/', RecoveryIdView.as_view(), name='recovery_id'),
    path('recovery/id/find/', ajax_find_id_view, name='ajax_id'),
    path('recovery/pw/', RecoveryPwView.as_view(), name='recovery_pw'),
    path('recovery/pw/find/', ajax_find_pw_view, name='ajax_pw'),
    path('recovery/pw/auth/', auth_confirm_view, name='recovery_auth'),
    path('recovery/pw/reset/', auth_pw_reset_view, name='recovery_pw_reset'),
    
    path('information/', information, name='information'),
]