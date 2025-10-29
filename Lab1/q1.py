def prepare_message(message):
    """Remove spaces and convert to uppercase"""
    return message.replace(" ", "").upper()


def additive_cipher(message, key, mode='encrypt'):
    result = []
    for char in prepare_message(message):
        if char.isalpha():
            if mode == 'encrypt':
                new_char = chr(((ord(char) - 65 + key) % 26) + 65)
            else:
                new_char = chr(((ord(char) - 65 - key) % 26) + 65)
            result.append(new_char)
    return ''.join(result)


def multiplicative_cipher(message, key, mode='encrypt'):
    result = []

    # Find modular inverse if decrypting
    mod_inverse = None
    if mode == 'decrypt':
        for i in range(26):
            if (key * i) % 26 == 1:
                mod_inverse = i
                break
        if mod_inverse is None:
            return "Error: Key must be coprime with 26 for decryption"

    for char in prepare_message(message):
        if char.isalpha():
            if mode == 'encrypt':
                new_char = chr(((ord(char) - 65) * key % 26) + 65)
            else:
                new_char = chr(((ord(char) - 65) * mod_inverse % 26) + 65)
            result.append(new_char)
    return ''.join(result)


def affine_cipher(message, a, b, mode='encrypt'):
    result = []

    # Find modular inverse if decrypting
    mod_inverse = None
    if mode == 'decrypt':
        for i in range(26):
            if (a * i) % 26 == 1:
                mod_inverse = i
                break
        if mod_inverse is None:
            return "Error: First key must be coprime with 26 for decryption"

    for char in prepare_message(message):
        if char.isalpha():
            if mode == 'encrypt':
                new_char = chr((((ord(char) - 65) * a + b) % 26) + 65)
            else:
                new_char = chr(((ord(char) - 65 - b) * mod_inverse % 26) + 65)
            result.append(new_char)
    return ''.join(result)


def main_menu():
    while True:
        print("\n=== Cipher Menu ===")
        print("1. Additive Cipher")
        print("2. Multiplicative Cipher")
        print("3. Affine Cipher")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '4':
            print("Exiting program...")
            break

        message = input("Enter your message: ")

        if choice == '1':
            key = int(input("Enter additive key (0-25): "))
            operation = input("Encrypt or Decrypt? (e/d): ").lower()
            if operation.startswith('e'):
                result = additive_cipher(message, key, 'encrypt')
                print(f"\nEncrypted Message: {result}")
            else:
                result = additive_cipher(message, key, 'decrypt')
                print(f"\nDecrypted Message: {result}")

        elif choice == '2':
            key = int(input("Enter multiplicative key (must be coprime with 26): "))
            operation = input("Encrypt or Decrypt? (e/d): ").lower()
            if operation.startswith('e'):
                result = multiplicative_cipher(message, key, 'encrypt')
                print(f"\nEncrypted Message: {result}")
            else:
                result = multiplicative_cipher(message, key, 'decrypt')
                print(f"\nDecrypted Message: {result}")

        elif choice == '3':
            a = int(input("Enter first affine key (must be coprime with 26): "))
            b = int(input("Enter second affine key (0-25): "))
            operation = input("Encrypt or Decrypt? (e/d): ").lower()
            if operation.startswith('e'):
                result = affine_cipher(message, a, b, 'encrypt')
                print(f"\nEncrypted Message: {result}")
            else:
                result = affine_cipher(message, a, b, 'decrypt')
                print(f"\nDecrypted Message: {result}")

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("=== Cryptography Ciphers Program ===")
    print("Your message will be automatically converted to uppercase and spaces removed")
    main_menu()
