from web3 import Web3
import time
# URL узла Infura
infura_url = "https://sepolia.infura.io/v3/28ac888234f74ad2af04eefb5ab49d00"

# Подключение к узлу
web3 = Web3(Web3.HTTPProvider(infura_url))

# Проверка подключения
if web3.is_connected():
    print("Подключение к Infura установлено!")
else:
    print("Не удалось подключиться к Infura.")


# Данные смарт-контракта
contract_address = "0x46dfd993Ec242D7fd209147eAB921F3EEB011E39"  # Укажите адрес контракта

abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "player",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "gameId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "bytes32",
				"name": "commitment",
				"type": "bytes32"
			}
		],
		"name": "CommitMade",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "creator",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "opponent",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "wager",
				"type": "uint256"
			}
		],
		"name": "GameCreated",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "winner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "loser",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "result",
				"type": "string"
			}
		],
		"name": "GameResult",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "player",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "gameId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "enum RockPaperScissors.Move",
				"name": "move",
				"type": "string"
			}
		],
		"name": "RevealMade",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "gameId",
				"type": "uint256"
			},
			{
				"internalType": "bytes32",
				"name": "commitment",
				"type": "bytes32"
			}
		],
		"name": "commitMove",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "opponent",
				"type": "address"
			}
		],
		"name": "createGame",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "gameCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "games",
		"outputs": [
			{
				"internalType": "address",
				"name": "player1",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "player2",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "wager",
				"type": "uint256"
			},
			{
				"internalType": "bytes32",
				"name": "player1Commit",
				"type": "bytes32"
			},
			{
				"internalType": "bytes32",
				"name": "player2Commit",
				"type": "bytes32"
			},
			{
				"internalType": "enum RockPaperScissors.Move",
				"name": "player1Move",
				"type": "string"
			},
			{
				"internalType": "enum RockPaperScissors.Move",
				"name": "player2Move",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isActive",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "gameId",
				"type": "uint256"
			},
			{
				"internalType": "enum RockPaperScissors.Move",
				"name": "move",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "salt",
				"type": "string"
			}
		],
		"name": "revealMove",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
# # Аккаунт и ключ
private_key = "11111"
account = "0x46dfd993Ec242D7fd209147eAB921F3EEB011E39"
account2="0x65B8fC12f0ea61186307D799532bc743DC939327"
private_key2 = "00000"

print(web3.eth.get_balance(account))

address = web3.to_checksum_address("0x11623afab6d8e71cfc45de74a1ec267fd758f872")
myContract = web3.eth.contract(address=address, abi=abi)
print(myContract)
print(f"Адрес контракта: {myContract.address}")
print("Доступные функции:")
for func_name in dir(myContract.functions):
	if not func_name.startswith("_"):
		print(f"  - {func_name}")

print("\nДоступные события:")
for event_name in dir(myContract.events):
    if not event_name.startswith("_"):  # Игнорируем приватные атрибуты
        print(f"  - {event_name}")

def set_bet_and_create_game(account, opponent,private_key):
    """
    Функция для задания ставки и создания игры с определенной ставкой.

    :param account: Адрес  аккаунта
    :param opponent: Адрес противника
    :param wager_amount: Сумма ставки (в эфире)
    """
    # Переводим сумму ставки в wei
    wager = web3.to_wei(0.00000002, 'ether')

    # Строим транзакцию для создания игры
    transaction = myContract.functions.createGame(opponent).build_transaction({
        'from': account,
        'value': wager,  # Передаем ставку в транзакцию
        'gas': 2000000,  # Газ для транзакции
        'gasPrice': web3.to_wei('10', 'gwei'),  # Цена газа
        'nonce': web3.eth.get_transaction_count(account),  # Получаем nonce для транзакции
    })

    # Подписываем транзакцию с приватным ключом
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Отправляем транзакцию
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

    # Ожидаем подтверждения транзакции
    print(f"Транзакция отправлена. Хэш транзакции: {tx_hash.hex()}")

    # Проверка статуса транзакции (опционально)
    try:
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Транзакция подтверждена. Статус: {tx_receipt['status']}")
    except Exception as e:
        print(f"Ошибка при ожидании подтверждения транзакции: {e}")



def commit_move(account, game_id, move_value, salt, private_key):
    # Генерация commitment с использованием keccak256
    # move_value - это значение хода, например, 0 для Камня, 1 для Бумаги, 2 для Ножниц
    move_and_salt = f"{move_value}{salt}"
    commitment = web3.keccak(Web3.to_bytes(text=move_and_salt))  # Генерация хэша

    # Строим транзакцию для вызова функции commitMove
    transaction = myContract.functions.commitMove(game_id, commitment).build_transaction({
        'from': account,
        'gas': 2000000,  # Газ
        'gasPrice': web3.to_wei('5', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account),  # Получаем nonce
    })

    # Подписываем транзакцию
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Отправляем транзакцию
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

    # Проверка статуса транзакции (опционально)
    try:
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Транзакция подтверждена. Статус: {tx_receipt['status']}")
    except Exception as e:
        print(f"Ошибка при ожидании подтверждения транзакции: {e}")

def get_game_count():
    # Вызываем функцию gameCount() контракта
    game_count = myContract.functions.gameCount().call()
    return game_count

def reveal_move(account, game_id, move_value, salt, private_key):
    """
    Раскрывает ход в смарт-контракте Rock-Paper-Scissors.
    
    :param account: Адрес игрока.
    :param game_id: ID игры.
    :param move_value: Ход игрока .
    :param salt: Соль, использованная для коммита.
    :param private_key: Приватный ключ для подписи транзакции.
    """

    # Строим транзакцию для вызова revealMove
    transaction = myContract.functions.revealMove(
        game_id,          # ID игры
        move_value,       # Ход 
        str(salt)         # Соль
    ).build_transaction({
        'from': account,
        'gas': 2000000,
        'gasPrice': web3.to_wei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(account),
    })

    # Подписываем транзакцию
    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    # Отправляем транзакцию
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)

    # Ожидаем подтверждения транзакции

    try:
		# Ожидание подтверждения транзакции
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt['status'] == 1:
            print(f"Ход успешно раскрыт! Хеш транзакции: {tx_hash.hex()}")
        else:
            print("Не удалось раскрыть ход. Проверьте контракт на наличие ошибок.")
    except Exception as e:
        print(f"Ошибка при ожидании подтверждения транзакции: {e}")



print(get_game_count())
set_bet_and_create_game(account2, account,private_key2)

commit_move(account, get_game_count(), move_value="Rock", salt=0, private_key=private_key )
commit_move(account2, get_game_count(), move_value="Rock", salt=0, private_key=private_key2 )

reveal_move(account, get_game_count(), move_value="Rock", salt=0, private_key=private_key2)
reveal_move(account2, get_game_count(), move_value="Rock", salt=0, private_key=private_key2)

