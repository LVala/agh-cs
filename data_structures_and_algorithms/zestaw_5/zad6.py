def coin_change(coins, T):
    INF = float('inf') 

    min_coins = [INF] * (T + 1)

    min_coins[0] = 0

    for coin in coins:
        for i in range(T + 1):
            if i - coin >= 0:
                min_coins[i] = min(min_coins[i], min_coins[i - coin] + 1)

    if min_coins[T] != INF:
        return min_coins[T]
    else:
        return -1
