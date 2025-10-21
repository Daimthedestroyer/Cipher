import random
import hashlib
import base91

def key_to_seed(key: str) -> int:
    hash_object = hashlib.sha256(key.encode('utf-8'))
    hex_digest = hash_object.hexdigest()
    seed = int(hex_digest, 16)
    return seed

def cipher(text, key):
    seed = key_to_seed(key)
    random.seed(seed)
    rnd = random.Random(seed)

    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅabcdefghijklmnopqrstuvwxyz!@#$%^&()}{.,+-*/="
    shuffled_alphabet = list(alphabet)
    random.shuffle(shuffled_alphabet)
    mapping = dict(zip(alphabet, shuffled_alphabet))

    result = []
    for l in text:
        if l == " ":
            result.append("~")
        elif l == "\n":
            result.append("|")
        else:
            result.append(mapping.get(l, l))
    
    first_sentence = ''.join(result)
    padding = (-len(first_sentence)) % 3
    first_sentence += "\u2400" * padding

    second_sentence = []
    for i in range(0, len(first_sentence), 3):
        second_sentence.append(first_sentence[i:i+3])
    
    rnd.shuffle(second_sentence)
    third_sentence = ''.join(second_sentence)
    third_sentence = third_sentence.encode("utf-8")

    final_sentence = base91.encode(third_sentence)
    return final_sentence

def decipher(encoded_text, key):
    seed = key_to_seed(key)
    random.seed(seed)
    rnd = random.Random(seed)

    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅabcdefghijklmnopqrstuvwxyz!@#$%^&()}{.,+-*/="
    shuffled_alphabet = list(alphabet)
    random.shuffle(shuffled_alphabet)
    inverse_mapping = dict(zip(shuffled_alphabet, alphabet))

    try:
        decoded_bytes = base91.decode(encoded_text)
        third_sentence = decoded_bytes.decode("utf-8")
    except Exception as e:
        raise ValueError(f"Decoding failed: {e}")

    second_sentence = []
    for i in range(0, len(third_sentence), 3):
        second_sentence.append(third_sentence[i:i+3])

    indices = list(range(len(second_sentence)))
    rnd.shuffle(indices)
    first_sentence_trigrams = [''] * len(second_sentence)
    for new_pos, old_pos in enumerate(indices):
        first_sentence_trigrams[old_pos] = second_sentence[new_pos]

    first_sentence = ''.join(first_sentence_trigrams)
    first_sentence = first_sentence.rstrip('\u2400')

    result = []
    for l in first_sentence:
        if l == "~":
            result.append(" ")
        elif l == "|":
            result.append("\n")
        else:
            result.append(inverse_mapping.get(l, l))

    return ''.join(result)