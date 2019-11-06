import boto3
import json

config = {}

with open("config.json", "r") as f:
    config.update(json.load(f))

client = boto3.client(config['service'],
                      aws_access_key_id=config['accessKey'],
                      aws_secret_access_key=config['secretKey'])

invites = client.list_invitations(
    MaxResults=50,

)

accept_invites = client.accept_invitation(
    DetectorId=config['detectorID'],
    MasterId=invites["Invitations"][0]['AccountId'],
    InvitationId=invites["Invitations"][0]["InvitationId"]
)