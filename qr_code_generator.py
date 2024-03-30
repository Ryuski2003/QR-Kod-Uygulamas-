import string, random

initial_code = "2439_"
initial_code_length = len(initial_code)
codelength = 12

def randomize():
        characters = string.ascii_uppercase + string.digits
        randcode = ''.join(random.choice(characters) for i in range(codelength - initial_code_length))  #random part of code will be generated
        code = initial_code + randcode  #initial part + random part
        return code
        