from uuid import uuid4

from rest_framework import serializers

from api.encryption import encrypt_token
from users.models import APIUser
from wallet.models.invite import Invite


class APIUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIUser
        fields = ("token",)


class SignupSerializer(serializers.Serializer):
    """Create token and add user to the group."""

    invite_code = serializers.IntegerField(required=False)

    def create(self, validated_data):
        invite_code = validated_data.get("invite_code")
        token = str(uuid4())
        token_db = encrypt_token(token.encode())
        user = APIUser.objects.create(token=token_db)

        if invite_code:
            group_invite = Invite.objects.filter(invite_code=invite_code).first()
            if group_invite and not group_invite.is_expired:
                group = group_invite.group
                group.members.add(user)
                group_invite.delete()
        return user
