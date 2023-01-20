from rest_framework import serializers
from .models import User, Holiday
from datetime import datetime


class UserCreateSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ["emp_name", "email", "password", "confirm_password"]

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                "Password and Confirm Password not match."
            )
        return attrs

    def create(self, validated_data):

        create_user = User()
        create_user.emp_name = validated_data["emp_name"]
        create_user.email = validated_data["email"]

        create_user.set_password(validated_data["password"])
        create_user.save()

        return validated_data


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):

        if attrs["email"] == "" or attrs["email"] == None:
            raise serializers.ValidationError("Email may not be blank.")

        if attrs["password"] == "" or attrs["password"] == None:
            raise serializers.ValidationError("Password may not be blank.")

        return attrs


class HolidayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ["title", "start_date", "end_date"]

    def validate(self, attrs):

        if "start_date" not in attrs and "end_date" not in attrs:
            raise serializers.ValidationError("Start Date and End Date is required.")

        if "start_date" not in attrs:
            raise serializers.ValidationError("Start Date is required.")

        if "end_date" not in attrs:
            raise serializers.ValidationError("End Date is required.")

        start_date = attrs["start_date"]
        end_date = attrs["end_date"]

        if start_date == None or start_date == "":
            raise serializers.ValidationError("This field is required.")

        if end_date == None or end_date == "":
            raise serializers.ValidationError("This field is required.")
        return attrs

    def create(self, validated_data):

        user = self.context["request"].user
        import random

        
        import random
        random_number = random.randint(0,16777215)
        hex_number = str(hex(random_number))
        hex_number ='#'+ hex_number[2:]


        print(hex_number)

        print(hex_number, "COLOUR...........")
        create_request = Holiday.objects.create(
            email=user,
            title=validated_data["title"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
            colour=hex_number,
        )

        create_request.save()

        return validated_data


class HolidayGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ["event_id", "title", "start_date", "end_date", "colour"]


class HolidayGetFilterSerializer(serializers.Serializer):
    title = serializers.CharField(allow_blank=True, allow_null=True)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

    def validate(self, attrs):

        start_date = attrs["start_date"]
        end_date = attrs["end_date"]

        if start_date > end_date:
            raise serializers.ValidationError("Start date is not bigger than End date.")

        return attrs


class DummyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ["event_id", "title", "start_date", "end_date"]
