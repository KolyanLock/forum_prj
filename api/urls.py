from django.urls import path, include
from rest_framework import routers

# from api.views import CheckboxViewSet

# router = routers.DefaultRouter()
# router.register('api', CheckboxViewSet)
from api import views

urlpatterns = [
    # path('', include(router.urls)),
    path('checkbox_list', views.checkbox_list, name='checkbox_list'),
    path('checkbox_list/<int:pk>', views.checkbox, name='checkbox'),
    path('checkbox_create', views.checkbox_create, name='checkbox_create'),
    path('checkbox_update/<int:pk>', views.checkbox_update, name='checkbox_create'),
    path('checkbox_delete/<int:pk>', views.checkbox_delete, name='checkbox_create'),
    path('user_list', views.UserList.as_view(), name='user_list'),
    path('user_list/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
]
