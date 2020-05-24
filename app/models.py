from django.db import models


class User(models.Model):
    mobile = models.CharField(max_length=10, blank=False, unique=True, primary_key=True)
    name = models.CharField(max_length=50, blank=False)


class Group(models.Model):
    gname = models.CharField(max_length=50, blank=False, unique=True)


class GroupMember(models.Model):
    gid = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Bill(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    payee = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField()


class GroupBill(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    gid = models.ForeignKey(Group, on_delete=models.CASCADE)


class UserBill(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
