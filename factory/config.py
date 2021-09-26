"""
This configuration file can be used to change the Factory behavior and test some sub-strategies within the "promotion"
strategy applied on this simulation, for example, we can change the levels for each job, or setup different available
position in buyer, seller or assembler jobs.
"""

FOO_MINER = 'FOO_MINER'
BAR_MINER = 'BAR_MINER'
ASSEMBLER = 'ASSEMBLER'
SELLER = 'SELLER'
BUYER = 'BUYER'

MAX_LEVEL = {
    FOO_MINER: 10,
    BAR_MINER: 15,
    ASSEMBLER: 18,
    SELLER: 19,
    BUYER: 20,
}

MAX_JOBS = {
    BUYER: 1,
    SELLER: 2,
    ASSEMBLER: 5,
}
