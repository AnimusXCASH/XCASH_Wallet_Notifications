from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from colorama import init, Fore
from tools.fileHandlers import read_last_checked_block_data, store_last_updated_block_height
from pycoingecko import CoinGeckoAPI

gecko = CoinGeckoAPI()

init(autoreset=True)

class DepositMonitor():
    def __init__(self, xcash_wallet_rpc, pagers):
        self.wallet_rpc = xcash_wallet_rpc
        self.pagers = pagers

    async def deposits(self):
        try:
            usd = gecko.get_price(ids='x-cash', vs_currencies="usd")["x-cash"]["usd"]
        except Exception as e:
            print("Coingecko exception")
            usd = 0

        print(Fore.LIGHTBLUE_EX + f"[DEP] @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}... CHECKING")

        # Getting last check block 
        last_checked_block = read_last_checked_block_data()  # Get last processed block
        print(Fore.GREEN + f'Last processed block was {last_checked_block}')
        
        # Getting incoming transfer from last checked block
        block_txs = self.wallet_rpc.get_transfers(**{'in': True,
                                                            "min_height": last_checked_block,
                                                            "filter_by_height": True})


        # Checking if any results
        if block_txs["result"].get("in"):
            print(Fore.LIGHTCYAN_EX + f"[DEP] {len(block_txs['result']['in'])} New incoming transactions!!!")

            # Process every incoming transaction in block

            for t in block_txs["result"]["in"]:
                # Console
                print(Fore.LIGHTBLUE_EX + f'--------------------------------------------------\n'
                                            f'Time: {datetime.fromtimestamp(t["timestamp"])}\n'
                                            f'Height: {t["height"]}\n'
                                            f'Amount: {t["amount"]/(10**6):,.7f} XCASH\n'
                                            f'Fiat: ${(t["amount"]/(10**6)* usd):,.6f}\n'
                                            f'Payment ID: {t["payment_id"]}\n')
                
                # PushNotifier app
                message = f'[XCASH-IN] @ {datetime.fromtimestamp(t["timestamp"])}\nAmount: {t["amount"]/(10**6):,.7f} XCASH\nFiat: ${(t["amount"]/(10**6)* usd):,.6f}\nPayment ID: {t["payment_id"]}'
                message_disc = f'```Time: {datetime.fromtimestamp(t["timestamp"])}\nAmount: {t["amount"]/(10**6):,.7f} XCASH\nFiat: ${(t["amount"]/(10**6)* usd):,.6f}\nPayment ID: {t["payment_id"]}```'

                self.pagers.phone.phone_ping(text=message)
                self.pagers.discord.deposit_processed(text=message_disc)
            

            # Sending message on balance update
            balance = self.wallet_rpc.get_balance()
            balance_message = f'New Wallet Balance after processing:\n{balance["result"]["balance"]/(10**6)} XCASH\nFiat: ${(balance["result"]["balance"]/(10**6))*usd:,.6f}\n'
            self.pagers.phone.phone_ping(text=balance_message)
            self.pagers.discord.balance_status(text=f'```{balance["result"]["balance"]/(10**6):,.7f} XCASH\nFiat: ${(balance["result"]["balance"]/(10**6))*usd:,.6f}\n```')


            highest_block = max([x["height"] for x in block_txs["result"]["in"] ])
            if not store_last_updated_block_height(block_height=highest_block):
                print(Fore.LIGHTRED_EX + f'Could not update lastBlock.json to height {highest_block}...')
                raise
            
            print(Fore.LIGHTGREEN_EX + "[DEP] Finished processing all transfers... going to sleep!")
        else:
            print(Fore.LIGHTWHITE_EX + "[DEP] No new incoming payments....")



def start_deposit_monitor(timed_updater):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(timed_updater.deposits,
                      CronTrigger(minute='06, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 01'), misfire_grace_time=10,
                      max_instances=20)
    # scheduler.add_job(timed_updater.deposits,
    #                 CronTrigger(second='00'), misfire_grace_time=10,
    #                 max_instances=20)

    scheduler.start()
    print(Fore.LIGHTBLUE_EX + 'Deposit monitor...ACTIVATED')
    return scheduler
