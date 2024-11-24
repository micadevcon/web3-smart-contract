import time
from web3 import Web3
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
private_key = "111111"
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

def listen_for_events(contract, event_name, timeout=4):
    """
    Функция для прослушивания событий смарт-контракта в течение заданного времени.

    :param contract: объект контракта Web3.
    :param event_name: имя события для отслеживания.
    :param timeout: время (в секундах) для прослушивания событий.
    """
    # Создаем фильтр для события
    event_filter = getattr(contract.events, event_name).create_filter(from_block='latest', argument_filters={})
    print(f"Ожидание событий {event_name}...")

    start_time = time.time()

    try:
        while True:
            # Получаем новые события
            for event in event_filter.get_new_entries():
                print(f"Новое событие {event_name}!")
                print(f"Аргументы события: {event['args']}")

            # Таймер ограничивает выполнение
            if time.time() - start_time > timeout:
                print("Таймер завершён.")
                break

            # Небольшая пауза
            time.sleep(5)
    except KeyboardInterrupt:
        print("Прослушивание завершено.")

def listen_for_game_result(contract, timeout=4):
    """
    Функция для прослушивания событий GameResult смарт-контракта в течение заданного времени.

    :param contract: объект контракта Web3.
    :param timeout: время (в секундах) для прослушивания событий.
    """
    # Создаем фильтр для события GameResult
    event_filter = contract.events.GameResult.create_filter(from_block='latest')
    print("Ожидание событий GameResult...")

    start_time = time.time()

    try:
        while True:
            # Получаем новые события
            for event in event_filter.get_new_entries():
                print("Новое событие GameResult!")
                print(f"Победитель: {event['args']['winner']}")
                print(f"Проигравший: {event['args']['loser']}")
                print(f"Результат: {event['args']['result']}")

            # Таймер ограничивает выполнение
            if time.time() - start_time > timeout:
                print("Таймер завершён.")
                break

            # Небольшая пауза
            time.sleep(5)
    except KeyboardInterrupt:
        print("Прослушивание завершено.")

listen_for_events(myContract, "GameCreated", timeout=4)
listen_for_game_result(myContract, timeout=4)


	