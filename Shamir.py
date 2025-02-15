import numpy as np
import galois
import random

class Shamir:
    """
    Choose a finite field Z_p with p is a prime number\n
    Create f = o[0] + o[1]*x^1 + ... + o[k-1]*x^(k-1)\n
    The secret is o[0] (s)\n
    The secret is splitted into s shares\n
    And k = min_shares is the minimum number of shared pieces need to recover the secret s
    """
    def __init__(self, prime, shares, min_shares, secret):
        self.p = prime
        self.s = shares
        self.k = min_shares
        self.GF = galois.GF(self.p)
        self.secret = secret
        self.f = random.sample(range(1, self.p), self.k-1)
        self.f = [self.secret] + self.f
        self.e = random.sample(range(1, self.p), self.s)

    def __generateSharesPairs(self, e):
        f_e = []
        for i in range(self.k):
            sum = 0
            for j in range(self.k):
                sum += self.f[j] * (e[i]**j)
            f_e.append(sum % self.p)
        return f_e
    
    def __vandermonde_matrix(self, e):
        V = []
        for e_i in e:
            row = []
            for i in range(self.k):
                row.append((e_i**i) % self.p)
            V.append(row)
        return V
    

    def computeSecret(self):
        index = random.sample(range(self.s), self.k)
        e_k = [self.e[i] for i in index]
        f_k = self.GF(self.__generateSharesPairs(e_k))
        V = self.GF(self.__vandermonde_matrix(e_k))
        V_inv = np.linalg.inv(V)
        o = np.dot(V_inv, f_k)
        return o[0]

s = Shamir(103, 10, 5, 3)
print(s.computeSecret() == 3)
