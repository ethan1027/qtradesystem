from typing import Literal


SideOfOrder = Literal['buy', 'sell', 'sell_short', 'buy_cover']
OrderType = Literal['market', 'limit', 'stop', 'stop_limit']
AccountType = Literal['live', 'paper']
BalanceType = Literal['cash', 'margin', 'day_margin']
