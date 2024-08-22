import requests

# Set up the authorization and template details
access_token = "eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwAAk1fvucLcSAgAANN6_fzC3EgCAJHARGQRmJtIuQ5UZS71Mq0VAAEAAAAYAAEAAAAFAAAADQAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkIgAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkMACAS7bVucLcSDcAjwPrez9MtESeuaWmpmPIgA.kJFg4TLQLK9hKaXNO2EvDo0wARNaIwiQ9mdqHmd7gUvfe85oU2opWIq0ljB2Oab2lFM45LiOeL3CaJK0iSL0Ja-yH7JLCWPLGur-3eu_3yO6xgqZpp5x2cMCC6iXlJmApsSu904LiTnWukd9v8sADGuYZ9iaT8yvxWK_OE7hXLKOilFHwrrPs98DpiiWIHfJiqLHVGiaqvZ9Tw51_ofNQO5C2XBG0prG12DxHQUduguUnFgiF7I7ezgLaregxwtgOZqQAsVJ-L8wBG1cAWSlL74-s53TaWyFgBoXbjggWwjnIj03USR6fYreMTljPqE-v96SER6cJ9Y6O2AkeyOCGw"  # Replace with your actual access token
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
