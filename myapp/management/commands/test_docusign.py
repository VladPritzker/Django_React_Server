from django.core.management.base import BaseCommand
import requests
import json

class Command(BaseCommand):
    help = 'Test DocuSign PDF conversion and sending'

    def handle(self, *args, **kwargs):
        url = 'http://oyster-app-vhznt.ondigitalocean.app/docusign/send/'
        headers = {'Content-Type': 'application/json'}
        data = {
            "email": "recipient@example.com"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        self.stdout.write(self.style.SUCCESS(f'Response: {response.json()}'))
