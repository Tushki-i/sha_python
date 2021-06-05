# Basic functions
# For a list of inputs: returns the mod 2**w of the sum.
def add(nums: list, w: int) -> int:
    return sum(nums) % 2**w

# For inputs a, b, c: returns the parity of a, b, c.
def xor(a: int, b: int, c: int) -> int:
    return a ^ b ^ c

# Returns x rotated left by n positions. w determines length.
def rotl(x: int, n: int, w: int) -> int:
    return (x << n) | (x >> w - n)

# For inputs a, b, c: the output is the majority of the bits.
#   majority(0, 0, 1) = 0
def majority(a: int, b: int, c: int) -> int:
    return (a & b) | (a & c) | (b & c)

# For inputs a, b, c: a determines whether b or c is selected.
#   choice(0, 0, 1) =  1
def choice(a: int, b: int, c: int) -> int:
    return (~a & c) | (a & b)

# Processing
# Adds n 0s before a string.
def fill(x: str, n: int) -> str:
    return '0' * (n - len(x)) + x

# Pads the message into 512/1024 length block with the last 64/128 bits reserved for message size.
#   For message m: m + '1' + len(m) where len(pad(m)) == 512n or 1024n.
def pad(x: str, block: int) -> str:
    return x + '1' + '0' * ((block - 1 - len(x) % block) - block//8) + fill(bin(len(x))[2:], block//8)

# Splits m into len(m)/length words.
def split_words(m: str, length: int) -> list:
    words = []
    num_words = len(m)//length
    for n in range(0, num_words):
        words.append(m[n * length : (n + 1) * length])

    return words

# Splits an array of words into a 2-dimensional array of blocks and words
def split_blocks(words: list, size: int) -> list:
    return [words[i : i + size] for i in range(0, len(words), size)]
    
# Encodes a string into UTF-8
def binary_val(string: str) -> str:
    bin_val = ""
    byte_list = bytearray(string, 'utf-8')

    for byte in byte_list:
        b = bin(byte)[2:]
        bin_val += fill(b, len(b) + 8 - (len(b) % 8))
    
    return bin_val

# Specialized
# Adds the elements of two lists at each respective index
def bilist_sum(a: list, b: list, w: int) -> list:
    c = []
    for i in range(0, max(len(a), len(b))):
        c.append(add([a[i], b[i]], w))
    return c

# Converts a list of integers into a hex string with specific padding
def hex_list(l: list, n: int) -> str:
    s = ""
    for val in l:
        s += fill(hex(val)[2:], n)
    return s

# Hashing algorithms
def sha1(message: str):
    # Declare Constants
    K_BLOCK_LENGTH = 512
    K_WORD_LENGTH = 32
    K_SCHEDULE_LENGTH = 80

    # Set Constants
    k = [1518500249, 1859775393, 2400959708, 3395469782]
    h = [1732584193, 4023233417, 2562383102, 271733878, 3285377520]

    # Separate Blocks
    blocks = split_blocks([int(word, 2) for word in split_words(pad(binary_val(message), K_BLOCK_LENGTH), K_WORD_LENGTH)], 16)

    # For each block compress
    for block in blocks:
        # Expand word schedule
        for t in range(16, K_SCHEDULE_LENGTH):
            block.append(rotl(block[t - 3] ^ block[t - 8] ^ block[t - 14] ^ block[t - 16], 1, K_WORD_LENGTH) % 2**K_WORD_LENGTH)

        i = h.copy() # Save initial hashes

        # Compress
        for t in range(0, K_SCHEDULE_LENGTH):
            # Generate f(a, b, c) and K
            if 0 <= t <= 19:
                f = choice(h[1], h[2], h[3])
                k_w = k[0]
            elif 20 <= t <= 39:
                f = xor(h[1], h[2], h[3])
                k_w = k[1]
            elif 40 <= t <= 59:
                f = majority(h[1], h[2], h[3])
                k_w = k[2]
            elif 59 <= t <= 79:
                f = xor(h[1], h[2], h[3])
                k_w = k[3]
            
            # Compress
            t = add([rotl(h[0], 5, K_WORD_LENGTH), f, k_w, block[t], h[4]], K_WORD_LENGTH)
            h[1] = rotl(h[1], 30, K_WORD_LENGTH)
            h.pop()
            h.insert(0, t)

        # Add initial hashes to new hashes.
        h = bilist_sum(h, i, K_WORD_LENGTH)

    # Convert list of hashes to hex string
    return hex_list(h, 8)