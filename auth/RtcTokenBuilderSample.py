#! /usr/bin/python
# ! -*- coding: utf-8 -*-
from flask import Flask
import sys
import os
import time
from random import randint
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from auth.RtcTokenBuilder import RtcTokenBuilder,Role_Attendee
import uuid
import secret
appID = secret.appID
appCertificate = secret.appCert
expireTimeInSeconds = 3600
currentTimestamp = int(time.time())
privilegeExpiredTs = currentTimestamp + expireTimeInSeconds


def main():
    token = RtcTokenBuilder.buildTokenWithUid(appID, appCertificate, channelName, uid, Role_Attendee, privilegeExpiredTs)
    print("Token with int uid: {}".format(token))
    token = RtcTokenBuilder.buildTokenWithAccount(appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)
    print("Token with user account: {}".format(token))

def getTokenForUser(username,channelName):
    token = RtcTokenBuilder.buildTokenWithAccount(appID, appCertificate, channelName, username, Role_Attendee, privilegeExpiredTs)
    return token    

if __name__ == "__main__":
    main()
