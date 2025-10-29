def create_playfair_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    used = set()

    # Add key letters to matrix (no duplicates)
    for char in key:
        if char.isalpha() and char not in used:
            used.add(char)
            matrix.append(char)

    # Add remaining letters (combine I/J)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J excluded
    for char in alphabet:
        if char not in used:
            used.add(char)
            matrix.append(char)

    # Convert list into 5x5 matrix
    matrix_5x5 = [matrix[i*5:(i+1)*5] for i in range(5)]
    return matrix_5x5


def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None


def prepare_text(text):
    text = text.upper().replace('J', 'I')
    # Remove non-alpha characters
    text = ''.join(filter(str.isalpha, text))

    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = ''
        if i + 1 < len(text):
            b = text[i+1]
        else:
            b = 'X'  # Padding if last letter has no pair

        if a == b:
            # Insert 'X' between same letters
            result += a + 'X'
            i += 1
        else:
            result += a + b
            i += 2

    # If length is odd, pad with 'X'
    if len(result) % 2 != 0:
        result += 'X'

    return result


def encode_pair(matrix, a, b):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    if r1 == r2:
        # Same row: letter to the right (wrap around)
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        # Same column: letter below (wrap around)
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:
        # Rectangle: swap columns
        return matrix[r1][c2] + matrix[r2][c1]


def playfair_encrypt(key, plaintext):
    matrix = create_playfair_matrix(key)
    prepared_text = prepare_text(plaintext)

    ciphertext = ""
    for i in range(0, len(prepared_text), 2):
        a = prepared_text[i]
        b = prepared_text[i+1]
        ciphertext += encode_pair(matrix, a, b)

    return ciphertext


# Given values
key = "GUIDANCE"
plaintext = input("Enter plain text: ")

ciphertext = playfair_encrypt(key, plaintext)
print("Ciphertext:", ciphertext)
