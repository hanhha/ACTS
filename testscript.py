# Supported: oneMin, fiveMin, thirtyMin, hour, day
script = [
    ['tick', 60],
    ['filter', 3],
    ['generate', 1, 'clk'],
    ['monitor', 'clk', 'BTC-ADA', 'oneMin', 'dat0'],
    ['notify','dat0', 'C', 'Test'],
]

#'BV': 99.44951468,
#'C': 5.223e-05,
#'H': 5.223e-05,
#'L': 5.067e-05,
#'O': 5.081e-05,
#'T': '2018-01-01T17:00:00',
#'V': 1933366.51921126}])
