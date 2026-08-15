"""
Sanitized interaction helper for the PatientRecordContract.

This file shows how to connect and call view functions. Transactional
examples that would require private keys are intentionally omitted or
left as placeholders to avoid exposing secrets in the public repo.
"""

import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

CONTRACT_ABI = json.loads("""
[ ... ABI redacted for brevity in README copy - include full ABI when running locally ]
""")

def connect():
    infura_url    = os.getenv("ALCHEMY_URL") or os.getenv("INFURA_URL")
    contract_addr = os.getenv("CONTRACT_ADDR")

    if not infura_url or not contract_addr:
        raise EnvironmentError("ALCHEMY_URL/INFURA_URL and CONTRACT_ADDR must be set in .env")

    w3 = Web3(Web3.HTTPProvider(infura_url))
    if not w3.is_connected():
        raise ConnectionError("Could not connect to RPC provider. Check ALchemy/Infura URL.")

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(contract_addr),
        abi=CONTRACT_ABI
    )
    return w3, contract

def get_record(contract, record_id:int):
    return contract.functions.getRecord(record_id).call()

def get_total_records(contract):
    return contract.functions.totalRecords().call()

if __name__ == "__main__":
    print("This file is a sanitized helper. To run live interactions, fill .env from .env.example and use a local, private copy of this script that includes your ABI and keys.")
