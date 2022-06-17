# XCASH_Wallet_Notifications


# About

Simple script which monitors your local XCASH wallet and notifies you on incoming transaction through one of the available systems. 

Integrated systems:
[x] Discord Webhook system (Not a bot)
[X] Push Notifiers to Android or Iphone through third party system (https://pushnotifier.de/)

Covnersions:
[x] USD Fiat conversions based on Coingecko

# How to set-up

## Git clone repo 

```bash
git clone https://github.com/AnimusXCASH/XCASH_Wallet_Notifications.git
```

## Install project requirements 
Note: You can create virtual environment and install requirements afterwards 

```bash
pip3 install requirements.txt
``` 
## Create  2 JSON File into main project directory

### Script settings file 

Name of file: systemSettings.json

```json
{
    "discord": {
      "active": false,  // Set to true and create webhook through Discord
      "deposits": "Discord Channel Webhook"},
    "pushNotifier": {
      "active": true,  // Set to true and register over https://pushnotifier.de/. 
      "username": "PUSH_NOTIFIER_USERNAME",
      "password": "PUSH_NOTIFIER_PASSWORD",
      "appName": "com.WHATEVRNAMEYOUWANT.app",
      "token": "TOKEN_FROM_SYSTEM"
    }
  }
    
  ```

### Last processed block tracking

ATTENTION: Set to block 934795 to not spam the system 
  ```json
  {
  "blockHeight":934795
  }
  ```


## Download CLI wallet and make activate RPC for wallet through: 
```bash

# On windos on local daemon
xcash-wallet-cli.exe --wallet-file NAME_OF_WALLET --password WALLET_PASSWORD

# On windows remote daemon (X-Payment-World delegate
xcash-wallet-cli.exe --daemon-address 95.216.6.115:18281 --wallet-file NAME_OF_WALLET --password WALLET_PASSWORD

# On Linux on local daemon
./xcash-wallet-rpc  --wallet-file NAME_OF_WALLET --password WALLET_PASSWORD

# On linux remote daemon
./xcash-wallet-rpc --daemon-address 95.216.6.115:18281 --wallet-file NAME_OF_WALLET --password WALLET_PASSWORD

```

## Run the script

  ```bash
  python3 main.py
  ```

# Support 

## Github 
Open up a github ticket 

## Discord X-Payment-Delegate Discord Server
[Invite Link](https://discord.gg/pj9JCmTeJc) (User @Animus)

# Tip Jar
- [x] Through X-Payment system on Discord to user `Animus#4608 (ID:360367188432912385)`

- [x] XCASH Wallet Address: `XCA1d9H82oZP1ytt8ULMVFa6GNaX1RWHz8EFpwFNDgDbCEkzvZGP384Qfz6DJxjsmU2ernSQguqKgLDVkm1VteVT4ZiPJiSEVN`
