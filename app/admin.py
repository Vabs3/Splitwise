from django.contrib import admin

# Register your models here.
from .models import UserBill, User, Bill, GroupMember, GroupBill, Group

admin.site.register(User)
admin.site.register(UserBill)
admin.site.register(Bill)
admin.site.register(Group)
admin.site.register(GroupBill)
admin.site.register(GroupMember)