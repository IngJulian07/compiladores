
import re
from enum import Enum

# Enum para los tipos de tokens
class TokenType(Enum):
    PALABRA_CLAVE = 'PALABRA CLAVE'
    IDENTIFICADOR = 'IDENTIFICADOR'
    LITERALES = 'LITERALES'
    OPERADORES_LOGICOS = 'OPERADORES LOGICOS'
    DELIMITADORES = 'DELIMITADORES'
    TEXTO = 'TEXTO'
    ESPACIO_EN_BLANCO = 'ESPACIO EN BLANCO'
    CARACTER_DESCONOCIDO = 'CARACTER DESCONOCIDO'

# Compilamos las expresiones regulares una sola vez para mejorar rendimiento
TOKEN_REGEX = [
    (TokenType.PALABRA_CLAVE, re.compile(r'\b(if|else|while|return)\b')),
    (TokenType.IDENTIFICADOR, re.compile(r'\b[a-zA-Z_][a-zA-Z_0-9]*\b')),
    (TokenType.LITERALES, re.compile(r'\b\d+(\.\d+)?\b')),
    (TokenType.OPERADORES_LOGICOS, re.compile(r'[+\-\*/=<>!]+')),
    (TokenType.DELIMITADORES, re.compile(r'[()\[\]{};,]')),
    (TokenType.TEXTO, re.compile(r'"[^"]*"')),
    (TokenType.ESPACIO_EN_BLANCO, re.compile(r'\s+')),
    (TokenType.CARACTER_DESCONOCIDO, re.compile(r'.'))
]

# Función para el analizador léxico
def lexer(code):
    tokens = []
    index = 0
    while index < len(code):
        match = None
        for token_type, pattern in TOKEN_REGEX:
            match = pattern.match(code, index)
            if match:
                if token_type != TokenType.ESPACIO_EN_BLANCO:  # Ignoramos los espacios en blanco
                    token = {
                        'type': token_type.value,  # Aquí usamos .value para obtener el valor del Enum
                        'value': match.group(0),
                        'position': index
                    }
                    tokens.append(token)
                index = match.end(0)
                break
        if not match:
            raise RuntimeError(f'Error léxico en el índice {index}, carácter desconocido: {code[index]}')
    return tokens

# Clase Nodo para representar los elementos del árbol sintáctico
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)

    def __str__(self, nivel=0):
        ret = "\t" * nivel + f"{self.valor}\n"
        for hijo in self.hijos:
            ret += hijo.__str__(nivel + 1)
        return ret

    def __repr__(self):
        return f'{self.valor}'

# Función para generar un árbol sintáctico ascendente
def generar_arbol_sintactico(tokens):
    raiz = Nodo("expresión")
    pila_nodos = [raiz]
    actual = raiz

    for token in tokens:
        tipo, valor = token['type'], token['value']

        if tipo == 'PALABRA CLAVE':
            if valor in ['if', 'else', 'while']:
                nuevo_nodo = Nodo(f'{valor}')
                actual.agregar_hijo(nuevo_nodo)
                pila_nodos.append(actual)
                actual = nuevo_nodo
            elif valor == 'return':
                nodo_return = Nodo(f"{valor}")
                actual.agregar_hijo(nodo_return)
        elif tipo == 'DELIMITADORES':
            if valor == '(':
                condicion = Nodo("condición")  # Nuevo nodo para la condición
                actual.agregar_hijo(condicion)
                pila_nodos.append(actual)
                actual = condicion  # Cambiamos el contexto al nodo de condición
            elif valor == ')':
                actual = pila_nodos.pop()  # Volvemos al contexto anterior
            elif valor == '{':
                bloque = Nodo("bloque")
                actual.agregar_hijo(bloque)
                pila_nodos.append(actual)
                actual = bloque
            elif valor == '}':
                actual = pila_nodos.pop()
        elif tipo in ['IDENTIFICADOR', 'LITERALES', 'OPERADORES LOGICOS']:
            nodo = Nodo(f"{valor}")
            actual.agregar_hijo(nodo)

    return raiz


# Ejemplo de uso dinámico
if __name__ == "__main__":
    code = input("Introduce el código que deseas analizar: ")  # Entrada dinámica
    tokens = lexer(code)

    print("\nTokens obtenidos:")
    for token in tokens:
        print(token)

    print("\nÁrbol sintáctico ascendente:")
    arbol = generar_arbol_sintactico(tokens)
    print(arbol)


