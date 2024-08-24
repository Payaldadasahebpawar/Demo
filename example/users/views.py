from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction as db_transaction
from .models import UserProfile, UserAccount
from .serializers import UserProfileSerializer, UserAccountSerializer

class RegisterView(APIView):   
    @db_transaction.atomic
    def post(self, request):
        # Deserialize the user profile data
        user_profile_serializer = UserProfileSerializer(data=request.data)
        
        # Extract account data from the request
        account_data = request.data.get('account')
        
        if user_profile_serializer.is_valid() and account_data:
            try:
                # Start a transaction
                with db_transaction.atomic():
                    # Save the user profile
                    user_profile = user_profile_serializer.save()
                    
                    # Deserialize the account data
                    user_account_serializer = UserAccountSerializer(data=account_data)
                    
                    if user_account_serializer.is_valid():
                        # Save the user account with the linked user profile
                        user_account_serializer.save(user_profile=user_profile)  # Pass the user_profile instance here
                        
                        # Commit the transaction
                        return Response({
                            'user_profile': user_profile_serializer.data,
                            'account': user_account_serializer.data
                        }, status=status.HTTP_201_CREATED)
                    else:
                        # If account data is invalid, raise an error to trigger a rollback
                        raise ValueError("Invalid account data")
            except ValueError as e:
                # Rollback the transaction on error
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
