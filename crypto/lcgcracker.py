#   Tool for cracking linear congruential generators
#     Appropriate input in assumed so not much error handling
#       - function logic ripped from https://tailcall.net/posts/cracking-rngs-lcgs/

from Crypto.Util.number import inverse, GCD
from functools import reduce

def cracklcg(states, modulus = None, multiplier = None):
    
    # Minimum requirements
    if not isinstance(states, list) or len(states) < 3 or not all(isinstance(x, int) for x in states):
        raise ValueError("states must be a list of at least 3 integers.")
    if modulus is not None and not isinstance(modulus, int):
        raise ValueError("modulus must be an integer.")
    if multiplier is not None and not isinstance(multiplier, int):
        raise ValueError("multiplier must be an integer.")
  
  
    #Case with only states
    if modulus is None and multiplier is None :
        diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
        zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
        modulus = abs(reduce(GCD, zeroes))
        multiplier = (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus
        increment = (states[1] - states[0]*multiplier) % modulus
        return modulus, multiplier, increment
    
    #Case with states and modulus
    elif modulus is not None and multiplier is None:
        multiplier = (states[2] - states[1]) * inverse(states[1] - states[0], modulus) % modulus
        increment = (states[1] - states[0]*multiplier) % modulus
        return modulus, multiplier, increment
        
    #Case with states, modulus, and increment
    elif modulus is not None and multiplier is not None:
        increment = (states[1] - states[0]*multiplier) % modulus
        return modulus, multiplier, increment
    
    else: 
        raise ValueError("Unexpected input.")
