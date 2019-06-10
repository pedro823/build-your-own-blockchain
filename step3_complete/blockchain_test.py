from blockchain import Blockchain

bc = Blockchain(difficulty=4)

for i in range(10):
    bc.add_data(f'data #{i}')

for idx, block in enumerate(bc.blockchain):
    print(f'Block #{idx}: data={block.data} hash={block.hash} nonce={block.nonce}')

print(f'Blockchain.is_valid={bc.is_valid()}')