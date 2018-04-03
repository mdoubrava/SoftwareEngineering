"""The following Python implementation of Shamir's Secret Sharing is
released into the Public Domain under the terms of CC0 and OWFa:
https://creativecommons.org/publicdomain/zero/1.0/
http://www.openwebfoundation.org/legal/the-owf-1-0-agreements/owfa-1-0

See the bottom few lines for usage. Tested on Python 2 and 3.
"""
#
from __future__ import division
import random
import functools

_PRIME = 2**31 - 1  # this is the 8th Mersenne prime

_rint = functools.partial(random.SystemRandom().randint, 0)
sample = 777

def eval(polynomial, x, prime):
    '''evaluates polynomial (coefficient tuple) at x, used to generate a
    shamir pool in make_random_shares below.
    '''
    total = 0
    for coefficients in reversed(polynomial):
        total *= x
        total += coefficients
        total %= prime
    return total

def random_shares(threshold, shares, prime=_PRIME):
    '''
    Generates a random shamir pool, returns the secret and the share
    points.
    '''
    if threshold > shares:
        raise ValueError("The secret message is unrecoverable")
    polynomial = [_rint(prime) for i in range(threshold - 1)]
    polynomial = [sample] + polynomial
    points = [(i, eval(polynomial, i, prime))
              for i in range(1, shares + 1)]
    return polynomial[0], points


def _extended_gcd(a, b):
    '''
    division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    '''

    x = 0
    lastx = 1
    y = 1
    lasty = 0
    while b != 0:
        quotient = a // b
        a, b = b,  a%b
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastx, lasty


def _divmod(num, den, p):
    '''compute num / den modulo prime p

    To explain what this means, the return value will be such that
    the following is true: den * _divmod(num, den, p) % p == num
    '''
    inv, _ = _extended_gcd(den, p)
    return num * inv


def _lagrange_interpolate(x, x_s, y_s, p):
    '''
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order
    '''
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"

    def PI(vals):  # upper-case PI -- product of inputs
        total = 1
        for v in vals:
            total *= v
        return total

    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)  # list of x values
        cur = others.pop(i)  # get singular x value
        nums.append(PI(x - o for o in others))  # calculates Lagrange numerators
        dens.append(PI(cur - o for o in others))  # calculate Lagrange denominators

    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p) for i in range(k)])

    return (_divmod(num, den, p) + p) % p


def recover_secret(shares, prime=_PRIME):
    '''
    Recover the secret from share points
    (x,y points on the polynomial)
    '''
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, prime)


secret, shares = random_shares(threshold=3, shares=6)

print('secret and shares:', secret, shares)

print('secret recovered from minimum subset of shares', recover_secret(shares[:3]))
print('secret recovered from a different minimum subset of shares', recover_secret(shares[-3:]))
