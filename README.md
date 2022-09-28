# NFT Deployer
This repo provides python scripts to ease NFT deployment on TON (The Open Network).

## Prerequisites

1. Install `Python3`
2. [Setup TON Development Environment](https://www.tonspace.co/develop/smart-contracts/environment/installation#build-from-source)
    - Make sure to include binaries in your `PATH` before moving ahead!

## Getting Started

1. Clone the repository
    ```sh
    git clone https://github.com/anomaly-guard/nft-deployer
    cd nft-deployer
    ```
2. Download necessary configs:
    ```sh
    mkdir tmp
    cd tmp
    wget https://ton-blockchain.github.io/global.config.json
    wget https://ton-blockchain.github.io/testnet-global.config.json
    cd ..
    ```

## Setting up the Wallet

Before moving on you should configure `config.json`. It configures `network`, `your private key`, `lite-client configs`, and `contract codes`.

> **Warning**
> At least test the flow one time with `testnet` before moving on to `mainnet`.

To begin your work with deploying, you need to setup your wallet for sending messages and paying for fees. This script currently supports `v3r2` wallets. If you don't have one, upon first execution, keys will be generated and you will be asked to save it.

1. Set your private key in `config.json` (If you want key generation, replace the value with `null`)
2. Run `deploy-wallet.py`
    ```sh
    python deploy-wallet.py
    ```
3. According to the account state, the script will notify you with the proper action for you to do.
4. You can use `@testgiver_ton_bot` to get testnet TONs.
5. You're done when you see a message like the following message:
    ```
    using existing key defined in config ...
    This account is already active and deployed ...
    Wallet Address: kQC/+HiWP5fgsu9fS7cECGCGON5PZAdKO7fHZ0JyJxV8t6Yj
    Balance: 1.46751 TON
    ```

## Deploying NFT Collection

1. Open `deploy-collection.py` and configure the parameters of `NFTCollection` to create your desired collection:
    ```python
    # ...
    collection = NftCollection()
    collection.init_data(
        owner=addr,
        royalty_factor=5,
        royalty_base=100,
        next_item_index=0,
        collection_content_url='https://raw.githubusercontent.com/ton-blockchain/token-contract/main/nft/web-example/my_collection.json',
        common_content_url='https://raw.githubusercontent.com/ton-blockchain/token-contract/main/nft/web-example/',
    )
    # ...
    ```
2. Save and run the deploy script, you will see a message like:
    ```sh
    ❯ python3 deploy-collection.py
    using existing key defined in config ...
    preparing to deploy nft collection contract ...
    NFT Collection address: kQCtSPsG5JlnAeviQAzc811k2X4aRbHm1OJmzUnpkNNoPgLJ
    Deploy message successfully sent to lite-servers!
    ```
3. Take note of NFT Collection address, we will use it in next section to deploy NFT Items.

## Deploy NFT Items

1. Edit `deploy-item.py` and replace the values with desired ones:
    ```python
    nft_collection_addr = "kQCtSPsG5JlnAeviQAzc811k2X4aRbHm1OJmzUnpkNNoPgLJ"
    msg_body = DeployNFTMessage(
        index=0,
        content_url="my_nft.json",
        amount=50000000,
        owner=addr,
    ).to_boc()
    ```
2. Save and run the deploy script, you will see a message like:
    ```sh
    ❯ python3 deploy-item.py
    using existing key defined in config ...
    Message successfully sent to lite-servers!
    ```
3. Your NFT is successfully deployed!

## Notes

1. The `0.05 TON` amount in messages are for covering the TON fees.
2. NFT Item url is not stored completely in NFT Item contract, the common part of url is saved in Collection contract and just the last part is saved in Item contract (To optimize fees).
3. You can use [tonscan](https://tonscan.org/) or its [testnet version](https://testnet.tonscan.org/) to check transactions status. (Enter address and check its transactions)
4. You can use [TON NFT Explorer](https://explorer.tonnft.tools/) or its [testnet version](https://testnet.explorer.tonnft.tools/) to check NFT contracts state.
5. You can customize the codes too, just point the `config.json`'s code path to modified contracts.