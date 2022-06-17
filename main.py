from xcash.rpc import XcashWalletRpc
import asyncio
from tools.fileHandlers import read_settings_data
from scheduledTaskers.depositMonitor import DepositMonitor,start_deposit_monitor
from tools.notifiersManager import NotifiersManager
from colorama import Fore, init

init(autoreset=True)

if __name__ == "__main__":

    # Load project settings 
    settings_file = read_settings_data()

    # Iitiate wallet RPC
    xcash_wallet_rpc = XcashWalletRpc(wallet_rpc_url = settings_file["rpcConnection"])
    
    try:
        # Get the balance from wallet
        balance = xcash_wallet_rpc.get_balance()
        print(Fore.GREEN + f'Current Wallet Balance: {balance["result"]["balance"]/(10**6):,.7f} XCASH')
    except Exception as e:
        print(Fore.LIGHTRED_EX + f'It looks like script can not access Wallet. Please re-check your Wallet-RPC connection.')
        raise
        
    # Activate notifiers
    notifiers = NotifiersManager(settings=settings_file)

    # Initiate deposit monitor
    deposit_monitor = DepositMonitor(xcash_wallet_rpc=xcash_wallet_rpc, pagers=notifiers)

    # Start monitoring script
    deposits = start_deposit_monitor(deposit_monitor)

    # Start async loop
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

