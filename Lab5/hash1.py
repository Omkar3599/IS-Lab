def custom_hash(input_string):
    hash_value = 5381
    for char in input_string:
        # Multiply by 33 and add ASCII of character
        hash_value = (hash_value * 33) + ord(char)

        # Example bit mixing: XOR with shifted versions of itself
        hash_value ^= (hash_value << 5) & 0xFFFFFFFF
        hash_value ^= (hash_value >> 3)

        # Keep hash_value within 32 bits
        hash_value &= 0xFFFFFFFF

    return hash_value


# Example usage:
s = input("Enter string: ")
print(f"Hash of '{s}': {custom_hash(s):#010x}")
