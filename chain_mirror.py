"""
Chain Mirror: инструмент для клонирования состояния адреса — UTXO, баланс, история.
"""

import requests
import argparse

def get_address_info(address):
    url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("❌ Ошибка получения адреса.")
    data = r.json()["data"][address]
    return {
        "balance": data["address"]["balance"],
        "transactions": data["transactions"],
        "utxos": data["utxo"]
    }

def summarize_info(info):
    print(f"💰 Баланс: {info['balance']} сатоши")
    print(f"🔁 Кол-во транзакций: {len(info['transactions'])}")
    print(f"📦 UTXO:")
    for utxo in info['utxos']:
        print(f"  - {utxo['transaction_hash']}:{utxo['index']} — {utxo['value']} сатоши")

def simulate_script(info):
    print("\n⚙️ Скрипт воспроизведения:")
    for utxo in info['utxos']:
        print(f"add_input('{utxo['transaction_hash']}', {utxo['index']})  # {utxo['value']} сатоши")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chain Mirror — отражение адреса.")
    parser.add_argument("address", help="Bitcoin-адрес")
    args = parser.parse_args()
    info = get_address_info(args.address)
    summarize_info(info)
    simulate_script(info)
