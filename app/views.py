from rest_framework import status, viewsets
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.models import User, Group, GroupMember, Bill, GroupBill, UserBill
from app.serializers import UserSerializer, GroupSerializer, GroupMemberSerializer, GroupBillSerializer, BillSerializer, \
    UserBillSerializer


def is_user_valid(phone_no):
    user = User.objects.filter(mobile=phone_no)
    return len(user) > 0


def get_user_bills(self, mobile):
    if not is_user_valid(mobile):
        return Response("Invalid User", status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(mobile=mobile)
    bills = UserBill.objects.filter(user_id=user.mobile)
    data = []
    for user_bill in bills:
        bill = Bill.objects.get(id=user_bill.bill_id.id)
        groupBill = GroupBill.objects.get(bill_id=bill.id)
        group = Group.objects.get(id=groupBill.gid.id)
        data.append({"group_name": group.gname, "bill_name": bill.name, "total_amount": bill.total_amount,
                     "user_amount": user_bill.amount})

    return JsonResponse(data, safe=False)


class UserController(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupController(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        if not is_user_valid(request.data["mobile"]):
            return Response("Invalid User", status=status.HTTP_400_BAD_REQUEST)
        data = {"gname": request.data["gname"]}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        group = Group.objects.filter(gname=data["gname"])
        data = {"gid": group[0].id, "user_id": request.data["mobile"]}
        group_member_serializer = GroupMemberSerializer(data=data)
        group_member_serializer.is_valid(raise_exception=True)
        group_member_serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BillController(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    def distribute_money(self, list_of_users, payee, bill_id, total_money):
        pay_amount = total_money / len(list_of_users)
        money_refund = total_money - pay_amount
        for user in list_of_users:
            amount = -pay_amount
            if user == payee.mobile:
                amount = money_refund
            data = {"bill_id": bill_id, "user_id": user, "amount": amount}
            user_bill_serializer = UserBillSerializer(data=data)
            user_bill_serializer.is_valid(raise_exception=True)
            user_bill_serializer.save()

    # users, payee, name, group, totalamount, creaters mobile number
    # only group user can create bill and add only group members
    def are_valid_group_members(self, users, group_id):
        for user in users:
            if len(GroupMember.objects.filter(user_id=user)) < 1:
                return False
        return True

    def create(self, request, *args, **kwargs):
        group = Group.objects.filter(gname=request.data["gname"])
        users = request.data["users"]
        users.extend([request.data["payee"], request.data["mobile"]])
        if not self.are_valid_group_members(users, group[0].id):
            return Response("Invalid User or User does not belong to group", status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        serializer = self.get_serializer(data={"name": data["name"], "payee": data["payee"],
                                               "total_amount": data["total_amount"]})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        bill = Bill.objects.filter(name=request.data["name"])
        self.distribute_money(request.data['users'], bill[0].payee, bill[0].id, bill[0].total_amount)
        data = {"gid": group[0].id, "bill_id": bill[0].id}
        group_bill_controller = GroupBillSerializer(data=data)
        group_bill_controller.is_valid(raise_exception=True)
        group_bill_controller.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupMemberController(viewsets.ModelViewSet):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer

    # add check for user
    # check for duplicate user in group
    def create(self, request, *args, **kwargs):
        if not is_user_valid(request.data["mobile"]):
            return Response("Invalid User", status=status.HTTP_400_BAD_REQUEST)
        group = Group.objects.filter(gname=request.data["gname"])
        data = {"gid": group[0].id, "user_id": request.data["mobile"]}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
