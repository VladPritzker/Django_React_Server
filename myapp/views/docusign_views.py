import requests
from django.conf import settings

def send_form_via_docusign(template_id, recipient_email, recipient_name):
    access_token = "eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwAAgkukrrjcSAgAAMJusvG43EgCALlaeBAx3T9DhTXhXpK7bj8VAAEAAAAYAAEAAAAFAAAADQAkAAAAOTYzOGE4MzItM2Q4ZC00YzczLWI4YzQtMDMyM2ZmM2FhMWE3IgAkAAAAOTYzOGE4MzItM2Q4ZC00YzczLWI4YzQtMDMyM2ZmM2FhMWE3MACAnI6LrbjcSDcAMxu6Wx9oqUW5mw1_hUCyPw.CTRc71LwZHMCWm9C_2k6Yq9njLvemCrr0YqEqLFkCofeoL9E9ILFha0AbVcG3Gu16O2qUjH8irGOV38YFj6eCkVCuUeLKpEpH868gakv1Cu0HFBJ1cj2LVsLx6yE1U9p5vX-FQpLIG1H0oZjigo6p8U1i7YbtV0m1UO88kgXPS76E_O-HjX-CH3-MxS72JRbl8zEzVl_0svpZc5rJsG1NaPaZe54lxDqE0InuSDJA9HnOR1r3l7HmgWgTdSe-5K-xODH3W9ad63JySzo_ohcRrm1SjYRE7ndaxrKwhdGIDQimu9laalsVXiiGiALfQtB0-1qxWIOVCTCNuirkSNttw"
    account_id = settings.DOCUSIGN_ACCOUNT_ID  # Ensure this is set in your settings.py
    base_uri = settings.DOCUSIGN_ACCOUNT_BASE_URI  # Ensure this is set in your settings.py

    template_id = "5aafa122-3553-46b7-9e54-e9d7c83e6d91"
    recipient_email = "pritzkervlad@gmail.com"
    recipient_name = "Vlad Buzhor"

    url = f"{base_uri}/v2.1/accounts/{account_id}/envelopes"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "templateId": template_id,
        "emailSubject": "Please fill out and sign the form",
        "templateRoles": [
            {
                "email": recipient_email,
                "name": recipient_name,
                "roleName": "Signer",  # Role defined in the template
                "routingOrder": "1"
            }
        ],
        "status": "sent"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Form sent successfully")
    else:
        print(f"Failed to send form: {response.text}")
