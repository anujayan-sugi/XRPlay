from xrpl.wallet import Wallet
# from xrpl.constants import CryptoAlgorithm
import xrpl
import json
import random
# from xrpl.wallet import Wallet
# test_wallet = Wallet.create()
# print(test_wallet.address) # Example: rGCkuB7PBr5tNy68tPEABEtcdno4hE6Y7f
# print(test_wallet.seed)


lottery_entrant1 = Wallet.from_seed(seed="sEd7AoY3CNp6nkpnHmfxeihbLF3Lp6D")
#Address: rxTkszMMqaQnwFPVBn19abZXvMwa89uFL
#Secret: sEd7AoY3CNp6nkpnHmfxeihbLF3Lp6D
lottery_entrant2 = Wallet.from_seed(seed="sEdV4ZekKRyxzUcqhH9jzaotTUUNzQo")
#Address: rpoCSH6PXYobGwtsC1MKSZjq3wT4TBy9BP
#Secret: sEdV4ZekKRyxzUcqhH9jzaotTUUNzQo
lottery_entrant3 = Wallet.from_seed(seed="sEdTUfUaiPGtJmSi2hsVeYEZDb2L4oQ")
#Address: rhGpbqwZ5a21Po6YsndWZo1MmPAN5ui6E7
#Secret: sEdTUfUaiPGtJmSi2hsVeYEZDb2L4oQ
lottery_address = Wallet.from_seed(seed="sEdSyVWcKUMK3cCtv3jD1pW6ZxAAUfT")
#Address: rwzEbnWrTJ8zq7u8H2ri1s6cYXTgmsnwhf
#Secret: sEdSyVWcKUMK3cCtv3jD1pW6ZxAAUfT

testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)
lottery_entrants = []
jackpot = 0
lottery_entry_amt = 10

def lottery_entry(lottery_entrant):
    #lottery entry costing 10 XRP
    global jackpot
    

    lottery_entry_payment = xrpl.models.transactions.Payment(
        account=lottery_entrant.address,
        amount=xrpl.utils.xrp_to_drops(lottery_entry_amt),
        destination=lottery_address.address,
    )


    signed_lottery_tx = xrpl.transaction.autofill_and_sign(
            lottery_entry_payment, client, lottery_entrant)
    max_ledger = signed_lottery_tx.last_ledger_sequence
    tx_id = signed_lottery_tx.get_hash()
    # print("Signed transaction:", signed_lottery_tx)
    # print("Transaction cost:", xrpl.utils.drops_to_xrp(signed_lottery_tx.fee), "XRP")
    # print("Transaction expires after ledger:", max_ledger)
    # print("Identifying hash:", tx_id)


    try:
        tx_response = xrpl.transaction.submit_and_wait(signed_lottery_tx, client)
        lottery_entrants.append(lottery_entrant)
        jackpot += lottery_entry_amt
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        exit(f"Submit failed: {e}")


# Check transaction results ----------------------------------------------------

    # print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    # print(f"Explorer link: https://testnet.xrpl.org/transactions/{tx_id}")
    metadata = tx_response.result.get("meta", {})
    # if metadata.get("TransactionResult"):
    #     # print("Result code:", metadata["TransactionResult"])
    # if metadata.get("delivered_amount"):
    #     # print("XRP delivered:", xrpl.utils.drops_to_xrp(
    #                 # metadata["delivered_amount"]))
# 
def pay_winner(lottery_winner):
    global jackpot 
    lottery_entry_payment = xrpl.models.transactions.Payment(
        account=lottery_address.address,
        # account=lottery_entrant.address,
        amount=xrpl.utils.xrp_to_drops(jackpot/1.1), 
        destination= lottery_winner.address,
    )


    signed_lottery_tx = xrpl.transaction.autofill_and_sign(
            lottery_entry_payment, client, lottery_address)
    max_ledger = signed_lottery_tx.last_ledger_sequence
    tx_id = signed_lottery_tx.get_hash()
    # print("Signed transaction:", signed_lottery_tx)
    # print("Transaction cost:", xrpl.utils.drops_to_xrp(signed_lottery_tx.fee), "XRP")
    # print("Transaction expires after ledger:", max_ledger)
    # print("Identifying hash:", tx_id)


    try:
        tx_response = xrpl.transaction.submit_and_wait(signed_lottery_tx, client)
        
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        exit(f"Submit failed: {e}")


# Check transaction results ----------------------------------------------------

    # print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    # print(f"Check your wallet transaction here: https://testnet.xrpl.org/transactions/{tx_id}")
    metadata = tx_response.result.get("meta", {})
    # if metadata.get("TransactionResult"):
    #     print("Result code:", metadata["TransactionResult"])
    # if metadata.get("delivered_amount"):
    #     print("XRP delivered:", xrpl.utils.drops_to_xrp(
    #                 metadata["delivered_amount"]))

def pick_winner():
    entrant_count = len(lottery_entrants)
    winner = random.randint(0,entrant_count-1)
    print(f"The winner is: entrant {winner + 1}")
    pay_winner(lottery_entrants[winner])


lottery_entry(lottery_entrant1)
lottery_entry(lottery_entrant2)
lottery_entry(lottery_entrant3)

pick_winner()


