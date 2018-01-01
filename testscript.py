# Supported: oneMin, fiveMin, thirtyMin, hour, day
script = [
    ['tick', 60],
    ['filter', 3],
    ['generate', 1, 'clk'],
    ['monitor', 'clk', 'BTC-ADA', 'oneMin', 'dat0'],
    ['notify','dat0','Test'],
]
