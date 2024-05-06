'''
Fecha: 06/05/2024

Integrantes:  - Juan David García Arce
              - Adrian Fernando Gaitán
              - Maximiliano Giraldo Ocampo

Tipo de busqueda: Heurística.
'''

#_________________________LIBRERÍAS_________________________#
import copy
import itertools
#_________________________ESTRUCTURA CSP_________________________#
class CSP:
    def __init__(self):
        self.Vars = {}  # Variables.
        self.Constraints={'Dif':[], 'SameDomain2': [], 'SameDomain3': [], 'NotRepeated': []}  # Restricciones.
        self.checkReductions = False # Booleano de verificación de reducciones.

    '''DOMINIOS DE LAS VARIABLES'''

    '''
    Estructura de los dominios de las variables:

            +---+---+---+---+---+---+---+---+---+---+
    Sudoku: | / | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
            +---+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+
            | A | *   *   * | *   *   * | *   *   * |
            | B | *   *   * | *   *   * | *   *   * |
            | C | *   *   * | *   *   * | *   *   * |
            +---+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+
            | D | *   *   * | *   *   * | *   *   * |
            | E | *   *   * | *   *   * | *   *   * |
            | F | *   *   * | *   *   * | *   *   * |
            +---+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+
            | G | *   *   * | *   *   * | *   *   * |
            | H | *   *   * | *   *   * | *   *   * |
            | I | *   *   * | *   *   * | *   *   * |
            +---+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+

            Genera la estructura de los dominios de variables para el tablero de Sudoku.

    '''

    def Vars_Doms(self):
        rows = set(range(1, 10))
        cols = 'ABCDEFGHI'
        self.Vars = {f"{c}{r}": rows.copy() for c in cols for r in rows}

    """
    Establece un valor específico en el diccionario de variables.

    Args:
        Name (str): El nombre de la variable para establecer el valor.
        Value (int): El valor a establecer para la variable.

    Returns:
        None
    """


    def setValueInVars(self,Name,Value):
        self.Vars[Name] = {Value}

    """
    Inicializa el tablero de Sudoku leyendo valores de un archivo y asignándolos a variables.

    Args:
        nameFile (str): El nombre del archivo que contiene los valores del tablero de Sudoku.

    Returns:
        None
    """

    def initBoard(self, nameFile):
        with open(nameFile, "r") as file:
            ListSudoku = "ABCDEFGHI"
            for r, c in itertools.product(range(1, 10), ListSudoku):
                cur = int(file.readline())
                if cur < 10:
                    self.setValueInVars(f"{c}{r}", cur)

    '''   RESTRICCIONES DE LAS VARIABLES

        - Itera sobre el rango de números de fila y columnas, creando una lista de variables para cada fila y añadiéndola al diccionario de restricciones bajo la clave dada.
    '''

    # Restricciones de las filas.
    def rowConstraints(self, consKey):
        colsIndex = "ABCDEFGHI"
        for i in range(1, 10):
            restrictionList = [str(j) + str(i) for j in colsIndex]
            self.Constraints[consKey].append(restrictionList)

    # Restricciones de las columnas.
    def colConstraints(self, consKey):
        colsIndex = "ABCDEFGHI"
        for i in colsIndex:
            restrictionList = [str(i) + str(j) for j in range(1, 10)]
            self.Constraints[consKey].append(restrictionList)

    # Restricciones de las ventanas.
    def regionConstraints(self, consKey, startRange, endRange):
        triplets = ["ABC", "DEF", "GHI"]
        for t in triplets:
            restrictionList = []
            for c in t:
                restrictionList.extend(str(c) + str(i) for i in range(startRange, endRange))
            self.Constraints[consKey].append(restrictionList)

    # Estructura de las restricciones.
    def constraintStructures(self, consKey):
        self.Constraints[consKey] = [] # Se inicializa la restricción.
        self.rowConstraints(consKey)
        self.colConstraints(consKey)
        startRange = [1, 4, 7]
        endRange = [4, 7, 10]
        for index in range(3):
            self.regionConstraints(consKey, int(startRange[index]), int(endRange[index]))

    '''
    Restricciones de diferencias:

      - Si el dominio de la variable es 1, se elimina el elemento de las demás variables.

      - Si el dominio es 2, se eliminan los elementos de las demás variables si los dominios son iguales.

      - Si el dominio es 3, se eliminan los elementos de las demás variables si los dominios son iguales.
    '''
    def dif(self, list_, index):
        for var in list_:
            if (self.numElement(var) == 1):
                element = self.Vars[var] 
                self.deleteElementInVar(var, list_, element.copy())
                self.deleteVarInConstraint('Dif', var, index)

    # Restricciones de dominios iguales de 2.
    def SameDomain2(self):
        for constraint in self.Constraints['SameDomain2']:
            for var_1 in constraint:
                if (self.numElement(var_1) == 2):
                    for var_2 in constraint:
                        if var_1 != var_2 and self.Vars[var_1] == self.Vars[var_2]:
                            lista_valores = list(self.Vars[var_1])
                            # Se obtienen los valores del dominio.
                            val_1 = lista_valores[0]
                            val_2 = lista_valores[1]
                            for valForDelete in constraint:
                                if valForDelete not in [var_1, var_2]:
                                    lenBefore = len(self.Vars[valForDelete])
                                    # Se eliminan los elementos del dominio.
                                    self.Vars[valForDelete].discard(val_1)
                                    self.Vars[valForDelete].discard(val_2)
                                    lenAfter = len(self.Vars[valForDelete])
                                    if(lenBefore > lenAfter):
                                        self.checkReductions = True

    # Restricciones de dominios iguales de 3.
    def SameDomain3(self):
        for constraint  in self.Constraints['SameDomain3']:
            for var_1 in constraint:
                if(self.numElement(var_1) == 3): # Si  el dominio de la variable es 3, se verifica si hay dominios iguales.
                    for var_2 in constraint:
                        if var_1 == var_2: # Si la variable es la misma, se pasa
                            pass
                        else:
                            if(self.Vars[var_1] == self.Vars[var_2]): # Si los dominios son iguales, se eliminan los elementos de las demás variables.
                                for var_3 in constraint:
                                    if(var_3 == var_1 or var_3 == var_2): 
                                        pass
                                    else:
                                        if(self.Vars[var_3] == self.Vars[var_1]): 
                                            lista = list(self.Vars[var_1]) # Se obtienen los valores del dominio.
                                            val_1 = lista[0]
                                            val_2 = lista[1]
                                            val_3 = lista[2]
                                            for valForDelete in constraint: # Se eliminan los elementos del dominio.
                                                if(valForDelete == var_1 or valForDelete == var_2 or valForDelete == var_3):
                                                    pass # Si la variable a eliminar es la misma, se pasa.
                                                else:
                                                    lenBefore = len(self.Vars[valForDelete]) # Se obtiene el tamaño del dominio antes de eliminar los elementos.
                                                    self.Vars[valForDelete].discard(val_1) 
                                                    self.Vars[valForDelete].discard(val_2)
                                                    self.Vars[valForDelete].discard(val_3)
                                                    lenAfter = len(self.Vars[valForDelete])
                                                    if(lenBefore > lenAfter): # Si el tamaño del dominio disminuyó, se actualiza la variable checkReductions.         
                                                            self.checkReductions = True # Se actualiza la variable checkReductions.

    # Restricciones de no repetidos.
    def NotRepeated(self):
        for constraint in self.Constraints['NotRepeated']:
            all_values = set()
            for var in constraint:
                all_values.update(self.Vars[var])
            for value in all_values:
                count = 0
                for var in constraint:
                    if value in self.Vars[var]:
                        count += 1
                        var_unic = var
                if count == 1 and self.numElement(var_unic) != 1:
                    # Si el valor se encuentra en un solo dominio, se actualiza el dominio de la variable.
                    self.Vars[var_unic] = {value}
                    self.checkReductions = True

    """
    Elimina un elemento del dominio de una variable en una lista dada, excepto la variable especificada.

    Args:
        var: La variable de la que se elimina el elemento.
        list_: La lista de variables para actualizar el dominio.
        element: El elemento a eliminar del dominio de las variables.

    Returns:
        None
    """
    def deleteElementInVar(self, var, list_, element):
        integer_element = int(element.pop())
        for c in list_:
            if c != var:
                self.Vars[c].discard(integer_element)
                self.checkReductions = True

    # Se elimina la variable de la restricción.
    def deleteVarInConstraint(self, constKey, var, i):
        lista = self.Constraints[constKey][i]
        lista.remove(var)

    """
    Devuelve la longitud del dominio de una variable.

    Args:
        key: La clave de la variable para determinar la longitud del dominio.

    Returns:
        int: La longitud del dominio de la variable.
    """
    def numElement(self, key):
        return len(self.Vars[key])

    """
    Procesa las restricciones para verificar la consistencia y aplicar operaciones específicas.

    Returns:
        bool: True si se realizaron reducciones durante el procesamiento de las restricciones, False en caso contrario.
    """
    def loopThroughConstraint(self):
        self.checkReductions = False
        for index in range(len(self.Constraints['Dif'])):
            self.dif(self.Constraints['Dif'][index], index)
            # Se verifica si el sudoku es consistente.
        self.SameDomain2()
        self.SameDomain3()
        self.NotRepeated()
        return self.checkReductions

    # Se verifica si el sudoku está resuelto.
    def is_solved(self):
        colsIndex = "ABCDEFGHI" # Columnas.
        return all(
            len(self.Vars[str(c) + str(i)]) == 1
            for c, i in itertools.product(colsIndex, range(1, 10))
        )

    # Se verifica si el sudoku es consistente.
    def localConsistent(self):
        colsIndex = "ABCDEFGHI"
        return all(
            len(self.Vars[str(c) + str(i)]) != 0
            for c, i in itertools.product(colsIndex, range(1, 10))
        )

    # Se copia el objeto.
    def copy(self):
        return copy.deepcopy(self)

    """
    Realiza el backtracking para resolver el rompecabezas de Sudoku.

    Args:
        sudoku: El rompecabezas de Sudoku a resolver.

    Returns:
        bool: True si se resuelve el rompecabezas, False en caso contrario.
    """
    def backTracking(self, sudoku):
        colsIndex = "ABCDEFGHI"
        break_outer_loop = False # Variable que nos indica si se realizó alguna eliminación en el dominio de las variables.
        for c in colsIndex:
            for i in range(1,10):
                if (len(self.Vars[str(c) + str(i)]) == 2):
                    lista = list(self.Vars[str(c) + str(i)])
                    element = lista[0]
                    self.Vars[str(c) + str(i)].discard(element)
                    break_outer_loop = True
                    break
            if break_outer_loop: # Se verifica si se realizó alguna eliminación en el dominio de las variables. 
                break

        if(break_outer_loop): # Se verifica si se realizó alguna eliminación en el dominio de las variables.
            while(self.loopThroughConstraint()):
                pass
            if (self.localConsistent() == False):
                sudoku.Vars[str(c) + str(i)] = {element} # Se actualiza la variable.
                return False
            else:
                return True

#_________________________SUDOKU_________________________#
sudoku = CSP() # Se crea el objeto CSP.
sudoku.Vars_Doms()
sudoku.initBoard("solve.txt") # Se inicializa el tablero de Sudoku.
sudoku.constraintStructures('Dif')
sudoku.constraintStructures('SameDomain2')
sudoku.constraintStructures('SameDomain3')
sudoku.constraintStructures('NotRepeated')

# Se resuelve el sudoku.
while(sudoku.is_solved() == False):
    while(sudoku.loopThroughConstraint()):
        pass
    if sudoku.is_solved() == False:
        test = sudoku.copy() # Se copia el objeto.
        if test.backTracking(sudoku) != False:
            sudoku = test # Se actualiza el sudoku.

#_________________________IMPRESIÓN DEL SUDOKU_________________________#
def print_sudoku(sudoku):
    colsIndex = "ABCDEFGHI" # Columnas

    print("SUDOKU RESUELTO: ")
    print("\t"+"+---"*10+"+")
    print("\t| / | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |")
    print("\t"+"+---"*10+"+")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("\t"+"+---"*10+"+")
        row_values = []
        for j in range(9):
            cell_value = sudoku.Vars[colsIndex[j] + str(i+1)].pop()
            row_values.append(str(cell_value))
            sudoku.Vars[colsIndex[j] + str(i+1)].add(cell_value)
        print("\t| " + colsIndex[i] + " | " + " | ".join(row_values) + " |")
    print("\t"+"+---"*10+"+")

print_sudoku(sudoku)
#_________________________FIN DEL PROGRAMA_________________________#