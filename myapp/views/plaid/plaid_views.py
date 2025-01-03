from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .plaid_client import plaid_client
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.country_code import CountryCode
from django.conf import settings
from plaid.model.products import Products
from myapp.models import PlaidItem, TrackedAccount
from django.views.decorators.http import require_POST
# from myapp.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

import json
import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Set up logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])  # This allows any user to access the view
def create_link_token(request):
    try:
        data = request.data
        user_id = data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
        
        # Fetch the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        logger.info(f"Creating link token for client_user_id: {user_id}")

        # Create the link token request
        request_data = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=str(user_id)),
            client_name="Pritzker Finance",
            products=[Products("transactions")],
            country_codes=[CountryCode("US")],
            language="en",
            webhook="https://oyster-app-vhznt.ondigitalocean.app/plaid/webhook/"
        )

        # Send the request to Plaid
        response = plaid_client.link_token_create(request_data)
        link_token = response.link_token

        # Log and return the link token
        logger.info(f"Link token generated: {link_token}")
        return Response({'link_token': link_token})

    except Exception as e:
        logger.error(f"Error creating link token: {str(e)}")
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])  # This allows any user to access the view
def get_access_token(request):
    try:
        data = request.data  # Use DRF's request.data
        public_token = data.get('public_token')
        user_id = data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
        
        # Fetch the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        logger.info(f"Received public token: {public_token} for user_id: {user_id}")

        # Exchange public token for access token
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)

        # Extract access token and item ID
        access_token = exchange_response.access_token
        item_id = exchange_response.item_id
        logger.info(f"Access token: {access_token}, Item ID: {item_id}")

        # Update the PlaidItem for the user
        plaid_item, created = PlaidItem.objects.get_or_create(user=user)
        if plaid_item.item_id != item_id:
            plaid_item.previous_item_id = plaid_item.item_id
            plaid_item.item_id = item_id
            plaid_item.cursor = None  # Reset the cursor when item_id changes
        plaid_item.access_token = access_token
        plaid_item.save()

        return Response({'message': 'Access token obtained successfully.', 'access_token': access_token})
    except Exception as e:
        logger.error(f"Error getting access token: {str(e)}", exc_info=True)
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])  # This allows any user to access the view
def get_account_data(request):
    try:
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
        
        # Fetch the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        plaid_item = PlaidItem.objects.filter(user=user).last()
        if not plaid_item:
            return Response({'error': 'PlaidItem not found'}, status=404)
        access_token = plaid_item.access_token
        if not access_token:
            return Response({'error': 'Access token missing'}, status=400)
        
        # Use the utility function
        accounts = get_account_data_util(access_token)
        if accounts is None:
            return Response({'error': 'Failed to get account data'}, status=500)
        
        # Convert accounts to dictionary format
        accounts_data = [account.to_dict() for account in accounts]
        return Response({'accounts': accounts_data})
    except Exception as e:
        logger.error(f"Error getting account data: {str(e)}", exc_info=True)
        return Response({'error': str(e)}, status=500)

def get_account_data_util(access_token):
    try:
        # Fetch account data from Plaid using the access token
        request_data = AccountsGetRequest(access_token=access_token)
        response = plaid_client.accounts_get(request_data)
        # Return the account data
        return response.accounts
    except Exception as e:
        logger.error(f"Error getting account data: {str(e)}")
        return None

@api_view(['POST'])
@permission_classes([AllowAny])  # This allows any user to access the view
def save_selected_accounts(request):
    try:
        data = request.data  # Use DRF's request.data to handle JSON data
        user_id = data.get('user_id')
        selected_account_ids = data.get('account_ids', [])

        if not user_id:
            return Response({'error': 'user_id is required'}, status=400)
        
        # Fetch the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        # Assuming you have the latest PlaidItem
        plaid_item = PlaidItem.objects.filter(user=user).last()
        if not plaid_item:
            return Response({'error': 'PlaidItem not found'}, status=404)

        # Fetch account data to get account info
        access_token = plaid_item.access_token
        accounts = get_account_data_util(access_token)
        if accounts is None:
            return Response({'error': 'Failed to retrieve accounts.'}, status=500)

        account_id_to_info = {
            account.account_id: {
                'name': account.name,
                'mask': account.mask
            }
            for account in accounts
        }

        # Clear existing tracked accounts
        TrackedAccount.objects.filter(user=user).delete()

        # Save selected accounts
        for account_id in selected_account_ids:
            account_info = account_id_to_info.get(account_id, {})
            TrackedAccount.objects.create(
                user=user,
                account_id=account_id,
                account_name=account_info.get('name', ''),
                account_mask=account_info.get('mask', ''),
                item=plaid_item
            )

        return Response({'message': 'Selected accounts saved successfully.'})
    except Exception as e:
        logger.error(f"Error saving selected accounts: {str(e)}", exc_info=True)
        return Response({'error': str(e)}, status=500)