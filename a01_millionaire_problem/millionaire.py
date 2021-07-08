import random


def print_banner():
    banner = '''This project is inspired by a youtube video:
    姚期智百万富翁问题：大数据时代，如何保护个人隐私？
    URL: https://youtu.be/dOTwAzXrkyQ
    '''
    print(banner)


def debug(msg: str):
    assert isinstance(msg, str)
    print(f'DEBUG: {msg}')


'''
Theory: https://www.di-mgt.com.au/rsa_theory.html
The RSA cryptosyste

Key generation
1. Choose two distinct primes p and q of approximately equal size so that their 
    product n=pq is of the required bit length.
2. Compute ϕ(n)=(p−1)(q−1).
3. Choose a public exponent e, 1<e<ϕ(n), which is coprime to ϕ(n), that is, gcd(e,ϕ(n))=1.
4. Compute a private exponent d that satisfies the congruence ed≡1(modϕ(n)).
5. Make the public key (n,e) available to others. Keep the private values d, p, q, and ϕ(n) secret.

RSA Encryption scheme
Encryption rule: ciphertext, c= RsaPublic(m)=(m^e) mod n, where 1<m<n−1.
Decryption rule: plaintext, m= RsaPrivate(c)=(c^d) mod n.
Inverse transformation: m = RsaPrivate(RsaPublic(m)).

RSA Signature scheme
Signing: signature, s = RsaPrivate(m)=(m^d) mod n, where 1<m<n−1.
Verification: check, v = RsaPublic(s)=(s^e) mod n.
Inverse transformation: m = RsaPublic(RsaPrivate(m))
'''

'''
Real life implementation: https://pycryptodome.readthedocs.io/en/latest/src/examples.html
def generate_key_pairs():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt(message, public_key) -> str:
    data = str(message).encode("utf-8")
    recipient_key = RSA.import_key(public_key)  # RSA.import_key(open("receiver.pem").read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    encrypted_data = [x for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
    return encrypted_data
'''

'''
Toy implementation: https://www.pythonpool.com/rsa-encryption-python/

RSA Encryption Implementation Without Using Library in Python
How does RSA algorith work?
Let us learn the mechanism behind RSA algorithm :

How to generate Public Key for encryption:
Take two prime numbers such as 7 and 11.
multiply the prime numbers and assign them to a variable. n= 7*11=77
Assume a small exponent e which will lie between 1 to phi(n)= 6*10 = 60. Let us assume e=43, d=7
Now, we are ready with our public key(n = 77 and e = 43) .
private key(n = 77, d = 7)

Encryption:
c = (m^e) mod n = (m ** 43) % 77
Decryption:
m = (c^d) mod n = (c ** 7) % 77

'''


def generate_key_pairs():
    p = 11
    q = 7
    n = p * q
    e = 43
    d = 7
    private_key = (n, d)
    public_key = (n, e)
    return private_key, public_key


def encrypt(m, public_key):
    n, e = public_key
    c = (m ** e) % n
    return c


def decrypt(c, private_key):
    n, d = private_key
    m = (c ** d) % n
    return m


def get_integer_in_range(low, high) -> int:
    return random.randint(low, high)


def get_large_integer() -> int:
    ans = get_integer_in_range(53, 53)
    debug(f'large integer value is {ans}')
    return ans


def main():
    print_banner()

    # Step 0: millionaire A and B gets their money, respectively
    money_low, money_high = 1, 10
    money_range = money_high - money_low + 1
    i = get_integer_in_range(money_low, money_high)  # millionaire A's_money
    debug(f'i = {i}, millionaire A has {i} million dollars')
    j = get_integer_in_range(money_low, money_high)  # millionaire B's money
    debug(f'j = {j}, millionaire B has {j} million dollars')

    # Step 1: millionaire A generates a key pair, i.e., a public key and
    # a private key, and shares only the public key with public, including
    # millionaire B
    private_key, public_key = generate_key_pairs()
    debug(f'public_key={public_key}; private_key={private_key}')
    print(f'A send to B: {public_key}')

    # Step 2.1: millionaire B privately finds a large integer and shares
    # it with nobody.
    x = get_large_integer()  # millionaire B's private large integer
    debug(f'x = {x}')

    # Step 2.2: millionaire B encrypts the large integer
    k = encrypt(x, public_key)  # k is encrypted x, so E(x) = k, D(k) = x
    debug(f'k = E(x) = {k}')

    # Step 2.3: millionaire B generates a number m = k - j + 1 and send to
    # millionaire A
    m = k - j + money_low
    debug(f'm = k - j + {money_low} = {m}')
    print(f'B send to A: {m}')

    # Step 3.1 millionaire A generates a sequence y where y_u = k - j + u for
    # u in an inclusive range [money_low, money_high]
    y = [m + u for u in range(money_range)]
    debug(f'y = {y}')

    # Step 3.2 millionaire A decrypt each member of y
    z = [decrypt(y[u], private_key) for u in range(money_range)]
    debug(f'before mod operation: z = {z}')

    # Step 3.3 and then mod with a large prime number
    large_prime_number = 17  # or 1111111111111111111  # or use 4999 :)
    z = [zu % large_prime_number for zu in z]
    debug(f'after mod operation:  z = {z}')

    # Step 3.4 millionaire A add 1 to all boxes in inclusive range
    # [i+1, money_high], and then send the sequence back to millionaire B
    for index in range(i - money_low + 1, money_range):
        z[index] += 1
    debug(f'after "+1" operation: z = {z}')
    print(f'A send to B: {z}')

    # Step 4 millionaire B get z and only look at his own box,
    # and figure out if it was added by 1
    expected_number_in_box = x % large_prime_number
    debug(f'expected number in box is {x} % {large_prime_number} = {expected_number_in_box}')
    actual_number_in_box = z[j - money_low]
    debug(f'actual number in box is z[{j} - {money_low}] = {actual_number_in_box}')
    if expected_number_in_box == actual_number_in_box:
        print(f"B's money is less than or equal to A's money")
    else:
        print(f"B's money is greater than A's money")


if __name__ == "__main__":
    main()
