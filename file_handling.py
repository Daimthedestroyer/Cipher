from ciphering import cipher, decipher

def write_to_file(path, new_content):
    with open(path, "w") as f:
        f.write(new_content)

def open_file(path):
    with open(path) as f:
        return f.read()
    
def test_path(path):
    try:
        with open(path):
            return True
    except FileNotFoundError:
        return False

def handle_file(path, key, mode):
    with open(path) as f:
        content = f.read()

    if mode == "cipher":
        return cipher(content, key)
    
    elif mode == "decipher":
        return decipher(content, key)
    
    else:
        raise Exception("mode not specified")