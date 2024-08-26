import requests

# Set up the authorization and template details
access_token = "eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwAAkMlA4sXcSAgAANDsTiXG3EgCAJHARGQRmJtIuQ5UZS71Mq0VAAEAAAAYAAEAAAAFAAAADQAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkIgAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkMACAxlo24cXcSDcAjwPrez9MtESeuaWmpmPIgA.1DIN3QdBTwetKh8A4xzBXUwhaqWq3eg7hJ_hm5hshBmATH8SF_iTT__BHOAAb8kq3itMBKKp1IBenzYdaBQRMqnFLpNVZNIjaWt2i3bBTRarZLb-1CvCMS_igfRCUFnulStG9RZq6-RxtpGr7vxA3h2tsJCXgset_bJeQgUjZOY7FTLKLcKCpkQ1D9a6i1mHWJffYXx9TxALx7b7koEMVoh5muK7HUFCayRZqqchsac1hLrYPZvLXXlWZFcIsh-4g61pX9F1dRpsVgRb67iAGK5ka8BNkY4T9aqDyES8qMp4P3vYdmYVPiQVl85HOoq5u5_UcSBBrFkb1HHn3elrVg"  
account_id = "29035884"
template_id = "17cc51e1-5433-4576-98bb-7c60bde50bbd"
url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"

# Prompt for the number of recipients
num_recipients = int(input("Enter the number of recipients: "))

# Initialize the list to hold template roles
template_roles = []

# Collect information for each recipient
for i in range(num_recipients):
    print(f"Enter details for recipient {i+1}:")
    email = input("Enter email: ")
    name = input("Enter name: ")
    role_name = input("Enter role name (e.g., Recipient): ")
    
    # Create a template role dictionary and append to the list
    template_roles.append({
        "email": email,
        "name": name,
        "roleName": role_name,
        "clientUserId": "6444c091-9811-489b-b90e-54652ef532ad"  # This can be dynamic or static
    })

# Construct the payload
payload = {
    "templateId": template_id,
    "templateRoles": template_roles,
    "status": "sent"
}

# Set up the headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Send the envelope
response = requests.post(url, headers=headers, json=payload)

# Check the response
if response.status_code == 201:
    print("Envelope sent successfully!")
else:
    print(f"Failed to send envelope. Status code: {response.status_code}")
    print(f"Response: {response.json()}")
