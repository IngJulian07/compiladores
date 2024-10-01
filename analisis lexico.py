import re

# Definimos las expresiones regulares para los diferentes tipos de tokens
TOKEN_REGEX = [
    ('PALABRA CLAVE ', r'\b(if|else|while|return)\b'),
    ('IDENTIFICADOR ', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('LITERALES', r'\b\d+(\.\d+)?\b'),
    ('OPERADORES LOGICOS', r'[+\-*/=<>!]+'),
    ('DELIMITADORES', r'[()\[\]{};,]'),
    ('TEXTO', r'"[^"]*"'),
    ('ESPACIO EN BLANCO ', r'\s+'),
    ('CARACTERES DESCONOCIDOS', r'.')
]

# Función para el analizador léxico
def lexer(code):
    tokens = []
    index = 0
    while index < len(code):
        match = None
        for token_type, pattern in TOKEN_REGEX:
            regex = re.compile(pattern)
            match = regex.match(code, index)
            if match:
                if token_type != 'WHITESPACE':  # Ignoramos los espacios en blanco
                    token = {
                        'type': token_type,
                        'value': match.group(0),
                        'position': index
                    }
                    tokens.append(token)
                index = match.end(0)
                break
        if not match:
            raise RuntimeError(f'Error léxico en el índice {index}')
    return tokens

# Ejemplo de uso
if __name__ == "__main__":
    code = input("")
    tokens = lexer(code)
    for token in tokens:
        print(token)