import re,base64

b64strregex = r'\'[A-Za-z0-9\+\/]*={0,2}\''
strregex    = r'\'.*?\''
arrayregex  = r'\[[A-Za-z0-9\[\]\/\\\'\,=+]+?\]'

def extract_arrays(f):
    """Takes javascript string argument"""
    arrays = re.findall(arrayregex,f)
    return arrays

def extract_strings(f):
    """Takes javascript string argument"""
    strings = re.findall(strregex,f)
    return strings


def extract_b64_arrays(f):
    arrays = extract_arrays(f)
    def b64_check(a):
        array = a[1:-1].split(",")
        if False not in map(lambda x: re.match(b64strregex, x) is not None and (len(x)-2) % 4 == 0, array):
            return True and len(array) > 1 # filter out dict references
        else:
            return False
    arrays = list(filter(b64_check, arrays))
    return arrays

def decrypt_b64_arrays(f):
    arrays = extract_b64_arrays(f)
    arrays = list(map(lambda x: list(map(lambda y: [y,base64.b64decode(y[1:-1])], x[1:-1].split(","))), arrays))
    return arrays

def replace_strings_code(f, arrays):
    for array in arrays:
        for i in array:
            f = f.replace(i[0][1:-1],i[1].decode())
    return f
    
# print(replace_strings_code(f,decrypt_b64_arrays(f))) where f is an exemplar obfuscated function. Testing code removed for copyright reasons.
