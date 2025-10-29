def prepare_message(message):
    """Remove spaces and convert to uppercase"""
    return message.replace(" ", "").upper()


def vigenere_encrypt(message, keyword):
    encrypted = []
    keyword_repeated = (keyword * (len(message) // len(keyword) + 1))[:len(message)]
    for m_char, k_char in zip(prepare_message(message), keyword_repeated):
        if m_char.isalpha():
            shift = ord(k_char.upper()) - 65
            encrypted_char = chr(((ord(m_char) - 65 + shift) % 26) + 65)
            encrypted.append(encrypted_char)
    return ''.join(encrypted)


def vigenere_decrypt(ciphertext, keyword):
    decrypted = []
    keyword_repeated = (keyword * (len(ciphertext) // len(keyword) + 1))[:len(ciphertext)]
    for c_char, k_char in zip(ciphertext, keyword_repeated):
        if c_char.isalpha():
            shift = ord(k_char.upper()) - 65
            decrypted_char = chr(((ord(c_char) - 65 - shift) % 26) + 65)
            decrypted.append(decrypted_char)
    return ''.join(decrypted)


def autokey_encrypt(message, key):
    encrypted = []
    message_clean = prepare_message(message)
    key_stream = str(key) + message_clean[:-1]  # Autokey uses plaintext as subsequent keys
    for m_char, k_char in zip(message_clean, key_stream):
        shift = ord(k_char.upper()) - 65
        encrypted_char = chr(((ord(m_char) - 65 + shift) % 26) + 65)
        encrypted.append(encrypted_char)
    return ''.join(encrypted)


def autokey_decrypt(ciphertext, key):
    decrypted = []
    key_char = chr(key + 65)
    for c_char in ciphertext:
        decrypted_char = chr(((ord(c_char) - 65 - (ord(key_char) - 65)) % 26) + 65)
        decrypted.append(decrypted_char)
        key_char = decrypted_char  # Autokey uses decrypted text as subsequent keys
    return ''.join(decrypted)


def main():
    message = "the house is being sold tonight"
    vigenere_keyword = "dollars"
    autokey_key = 7  # 'H' (7th letter)

    while True:
        print("\n=== Cipher Menu ===")
        print("1. Vigenère Cipher")
        print("2. Autokey Cipher")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            print("\n[Vigenère Cipher]")
            encrypted = vigenere_encrypt(message, vigenere_keyword)
            decrypted = vigenere_decrypt(encrypted, vigenere_keyword)
            print(f"Original: {prepare_message(message)}")
            print(f"Encrypted: {encrypted}")
            print(f"Decrypted: {decrypted}")

        elif choice == '2':
            print("\n[Autokey Cipher]")
            encrypted = autokey_encrypt(message, autokey_key)
            decrypted = autokey_decrypt(encrypted, autokey_key)
            print(f"Original: {prepare_message(message)}")
            print(f"Encrypted: {encrypted}")
            print(f"Decrypted: {decrypted}")

        elif choice == '3':
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
