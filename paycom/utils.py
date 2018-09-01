import time


def sum2coins(amount):
    return amount * 100


def coin2sums(amount):
    return amount / 100


def time_now_in_ms():
    return int(time.time() * 1000)
