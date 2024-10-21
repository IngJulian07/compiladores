import re
import matplotlib.pyplot as plt
import networkx as nx

# Definimos las expresiones regulares para los diferentes tipos de tokens
TOKEN_REGEX = [
    ('PALABRA CLAVE', r'\b(if|else|while|return)\b'),
    ('IDENTIFICADOR', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
    ('LITERALES', r'\b\d+(\.\d+)?\b'),
    ('OPERADORES LOGICOS', r'[+\-*/=<>!]+'),
    ('DELIMITADORES', r'[()\[\]{};,]'),
    ('TEXTO', r'"[^"]*"'),
    ('ESPACIO EN BLANCO', r'\s+'),
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
                if token_type != 'ESPACIO EN BLANCO':  # Ignoramos los espacios en blanco
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
    raiz = Nodo("expresión")  # Nodo raíz del árbol sintáctico
    pila_nodos = [raiz]  # Utilizamos una pila para construir el árbol ascendente
    actual = raiz

    for token in tokens:
        tipo, valor = token['type'], token['value']

        if tipo == 'PALABRA CLAVE':
            if valor in ['if', 'else', 'while']:
                nuevo_nodo = Nodo(f'{valor}')
                actual.agregar_hijo(nuevo_nodo)
                pila_nodos.append(actual)  # Guardamos el contexto actual
                actual = nuevo_nodo  # Cambiamos el contexto al nuevo nodo
            elif valor == 'return':
                nodo_return = Nodo(f"{valor}")
                actual.agregar_hijo(nodo_return)
        elif tipo == 'DELIMITADORES':
            if valor == '{':
                bloque = Nodo("bloque")
                actual.agregar_hijo(bloque)
                pila_nodos.append(actual)  # Guardamos el contexto actual
                actual = bloque  # Cambiamos el contexto al bloque
            elif valor == '}':
                actual = pila_nodos.pop()  # Volvemos al contexto anterior
            elif valor == '(':
                condicion = Nodo("condición")
                actual.agregar_hijo(condicion)
                pila_nodos.append(actual)  # Guardamos el contexto actual
                actual = condicion  # Cambiamos el contexto a la condición
            elif valor == ')':
                actual = pila_nodos.pop()  # Volvemos al contexto anterior
        elif tipo in ['IDENTIFICADOR', 'LITERALES', 'OPERADORES LOGICOS']:
            nodo = Nodo(f"{valor}")  # Solo mostramos el valor sin detalles extra
            actual.agregar_hijo(nodo)
        elif tipo == 'TEXTO':
            nodo_texto = Nodo(f"{valor}")
            actual.agregar_hijo(nodo_texto)

    return raiz

# Función para dibujar el árbol utilizando networkx y matplotlib
def dibujar_arbol(raiz):
    G = nx.DiGraph()
    labels = {}

    # Función recursiva para recorrer el árbol y agregar nodos al gráfico
    def agregar_nodos_aristas(nodo, padre=None, depth=0, pos_x=0, pos_y=0, horizontal_spacing=1.5):
        G.add_node(nodo)
        labels[nodo] = nodo.valor
        pos[nodo] = (pos_x, pos_y)  # Definir posición del nodo
        if padre:
            G.add_edge(padre, nodo)
        
        # Ajuste manual para distribuir horizontalmente los hijos
        num_hijos = len(nodo.hijos)
        if num_hijos > 0:
            # Espaciado horizontal entre hijos
            offset_x = -(num_hijos - 1) * horizontal_spacing / 2
            for i, hijo in enumerate(nodo.hijos):
                agregar_nodos_aristas(hijo, nodo, depth + 1, pos_x + offset_x + i * horizontal_spacing, pos_y - 1)

    pos = {}
    agregar_nodos_aristas(raiz)

    # Dibujar el árbol
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", arrows=False)
    plt.title("Árbol Sintáctico")
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    code = input("Introduce el código que deseas analizar: ")
    tokens = lexer(code)

    print("\nTokens obtenidos:")
    for token in tokens:
        print(token)

    print("\nÁrbol sintáctico ascendente:")
    arbol = generar_arbol_sintactico(tokens)
    print(arbol)  # Esto imprimirá el árbol usando __str__() del Nodo

    # Dibujar el árbol
    dibujar_arbol(arbol)
