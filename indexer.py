from indexers.main import Worker

Worker("polygon-mainnet-usdt-tracker", "0xc2132D05D31c914a87C6611C10748AEb04B58e8F", "event", "recipient", {
    "recipient": '0xEAc7a8FE5B55Ade433Dd844420c8668b3FC56912'
}).cycle()
