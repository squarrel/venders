def count_change(amount):
    result = {
        '100': 0,
        '50': 0,
        '20': 0,
        '10': 0,
        '5': 0
    }

    for coin in result:
        result[coin] = amount // int(coin)
        amount = amount % int(coin)

    return result, amount
