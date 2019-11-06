import boto3
import smtplib
import os
from jinja2 import Template
import json

accounts_to_email = {}
config = {}

with open("config.json", "r") as f:
    config.update(json.load(f))

client = boto3.client(config['service'],
                      aws_access_key_id=config['accessKey'],
                      aws_secret_access_key=config['secretKey'])

response = client.list_members(
    DetectorId=config['detectorID'],
    MaxResults=50,
    OnlyAssociated='False'
)

for accounts in response['Members']:
    if accounts['RelationshipStatus'] == 'Invited':
        accounts_to_email.update({accounts['AccountId']:accounts['Email']})
    # print(accounts['RelationshipStatus'])
print(accounts_to_email)


def generate_email(accountnumber, accountemail, senderemail):
    subject = "Guard Duty Trial Reminder"

    with open(os.path.join('templates', 'reminder_email.template')) as email_file:
        email_template = Template(email_file.read())
        email_variables = {
            'accountNumber': accountnumber,
            'to_email': accountemail,
            'from_email': senderemail,
            'subject': subject
        }
    return email_template.render(email_variables)


for email_account in accounts_to_email:
    email_body = generate_email(email_account, accounts_to_email[email_account], config['fromEmail'])
    server_ssl = smtplib.SMTP_SSL('smtp-relay.gmail.com', 465)
    server_ssl.ehlo()
    server_ssl.sendmail(config['fromEmail'], accounts_to_email[email_account], email_body)
    server_ssl.close()