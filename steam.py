import json
import pprint
import sys
import steam.webauth as mwa
import steam.guard as g

#############################################
# Insert your Steam Account's username below
#############################################

steamUsername = "mySteamAccountUsername"

#############################################
# No need to edit anything else from here!
#############################################


# Instantiate and initialize the ValvePython/steam library's MobileWebAuth
user = mwa.MobileWebAuth('danilakadesnikov')
user.cli_login()


# Verify that the login worked, otherwise exits
if user.logged_on != True:
  sys.exit("Failed to log user in")


# Add SteamAuthenticator to your account
sa = g.SteamAuthenticator(backend=user)
sa.add() # SMS code will be send to the phone number registered in the Steam Account

print("2FA Secrets:")
pprint.pp(sa.secrets)

# Save the secrets to a file for safety
bkpFile = './2FA-secrets.json'
json.dump(sa.secrets, open(bkpFile, 'w'))
print(f"\n\nSecrets saved to {bkpFile}")
print("\n\nYou can now finish setting up Steam Guard Mobile Authenticator in your phone!")