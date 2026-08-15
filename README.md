Patient Record Blockchain — Technical Showcase
=============================================

This repository is a sanitized, technical showcase of a student project implementing a simple patient-record system backed by an on-chain Solidity contract and an educational Python blockchain demo.

Goals
- Demonstrate smart contract design for controlled record storage and transfer.
- Show a small, readable Python PoW blockchain used for teaching core concepts.
- Provide a reproducible, minimal setup that can be inspected without exposing secrets.

Key technologies
- **Solidity** (>=0.8.19) — contract in `contracts/PatientRecordContract.sol`
- **Python 3.8+** — demo and utilities in `src/`
- **web3.py** — interaction with Ethereum JSON-RPC providers
- **python-dotenv** — load local environment variables from an `.env` file
- **Alchemy / Infura** — RPC providers used during development; the environment template uses `ALCHEMY_URL` (see `.env.example`).

Repository layout
- `contracts/PatientRecordContract.sol` — Solidity contract implementing provider authorisation, record addition, and transfer logic.
- `src/interact.py` — sanitized helper showing how to connect and call view functions with `web3.py`.
- `src/blockchain.py` — educational Proof-of-Work blockchain implementation used for demonstration and unit tests.
- `notebooks/NOTES.md` — notes about development artifacts (sensitive notebooks excluded).
- `.env.example` — environment variable template you must copy to `.env` locally.

Security and sensitive data
- This repo intentionally excludes any secrets (RPC keys, private keys, exported transaction CSVs). The following guidelines were followed and should be followed when you run or extend this project:
	- Keep a local `.env` for secrets and add `.env` to `.gitignore` (the repo includes `.env.example`).
	- Never commit private keys or full RPC URLs containing API keys to version control.
	- Use `ALCHEMY_URL` or `INFURA_URL` (the example uses `ALCHEMY_URL`) for connecting to Sepolia or any testnet; store the full URL only in your local `.env`.

Environment variables (from `.env.example`)
- `ALCHEMY_URL` — Alchemy RPC endpoint (e.g. `https://eth-sepolia.g.alchemy.com/v2/<API_KEY>`) or set `INFURA_URL` if using Infura.
- `CONTRACT_ADDR` — deployed contract address (checksum form `0x...`).
- `OWNER_ADDR`, `OWNER_KEY` — deployer/owner address and private key (private key must remain local/private).
- `PROVIDER2_ADDR`, `PROVIDER2_KEY` — second provider account used for demonstration.

Setup and run (technical)
1. Create virtualenv and install dependencies (example):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install web3 python-dotenv
```

2. Copy `.env.example` to `.env` and populate the variables. Example `.env` values should only be used locally.

3. Deploy the contract (recommended workflow):
	- Compile and deploy using Remix or a local toolchain (Hardhat/Foundry).
	- If using Remix with Alchemy/Infura, configure the RPC endpoint in `.env` and unlock the deployer account in Remix or use a private key locally.
	- After deployment, set `CONTRACT_ADDR` in your local `.env`.

4. Interact locally using `web3.py` (view-only calls):

```powershell
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('RPC:', os.getenv('ALCHEMY_URL') or os.getenv('INFURA_URL'))"
python src/interact.py  # sanitized helper; replace ABI with local copy for full interactions
```

Testing and verification
- The Python demo contains unit tests in `src/blockchain.py` (testing `Block` and `Blockchain`). Run them with:

```powershell
python -m pytest src/blockchain.py -q
```

Notes derived from the submitted report
- The original assignment document informed the structure and rationale: a permissioned contract model (owner-authorised providers), event-based audit trail, and an educational Python implementation to illustrate blockchain primitives (hashing, PoW, genesis block, consensus). This README focuses on the technical reproduction steps rather than the academic report text.

Publishing guidance
- Before publishing to GitHub: verify `.env` and any CSV exports are not present. This repository already strips exported CSVs and local `.env` variants — keep them out of commits.

Next actions
- I can (A) create a `requirements.txt` for the Python parts, (B) prepare a minimal `deploy/` script showing Remix/Hardhat commands, or (C) commit and push this cleaned repo to a remote — tell me which you'd like next.
