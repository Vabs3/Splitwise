from django.urls import path

from rest_framework.routers import DefaultRouter

from app import views
from app.views import UserController, GroupController, BillController, GroupMemberController

router = DefaultRouter()
router.register('user', UserController, basename='user')
router.register('group', GroupController, basename='group')
router.register('bill', BillController, basename='bill')
router.register('groupMember', GroupMemberController, basename='groupMember')

urlpatterns = [
    path('userBills/<str:mobile>/', views.get_user_bills, name='user_bills')
]

urlpatterns += router.urls
