from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

# Connect to the Polkadot network
substrate = SubstrateInterface(
    url="ws://127.0.0.1:9944",
    ss58_format=0,
    type_registry_preset='polkadot'
)

# Load sender's keypair
sender_keypair = Keypair.create_from_mnemonic("symbol multiply black maze blade share slot split jelly tank unaware pottery")

# Define recipient address and amount to send (in Plancks, where 1 DOT = 10^10 Plancks)
recipient_address = "5FumiHZXSoJApjES7qZ5pWAJpU54G1Y8p4jCwp4hbWFYjA7d"
amount = 0 * 10**10  # 1 DOT

# Create a call to transfer funds
call = substrate.compose_call(
    call_module='Balances',
    call_function='transfer',
    call_params={
        'dest': recipient_address,
        'value': amount
    }
)

# Create the extrinsic
extrinsic = substrate.create_signed_extrinsic(call=call, keypair=sender_keypair)

# Send the extrinsic
try:
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    print(f"Extrinsic '{receipt.extrinsic_hash}' sent and included in block '{receipt.block_hash}'")
except SubstrateRequestException as e:
    print(f"Failed to send extrinsic: {e}")