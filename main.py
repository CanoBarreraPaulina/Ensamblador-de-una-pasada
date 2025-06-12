#1. inicio
#   a configurar la direccion de inicio (location counter)
#   b. prepara la tabla de simbolos (vacia)
#2. primera pasada
#   a. para cada linea de codigo:
#       i. si es una etiqueta, la guarda en la tabla de simbolos junto con su direccionn actual.
#       ii. si es una instruccion: la traduce a codigo maquina utilizando la tabla de simbolos en caso de ser necesario.
#       iii. si una directiva, ajusta el contador de ubicacion (location counter)
#   b. si se encuentra una referencia a una etiqueta no definida puede dejar un espacio en blanco y rellenarlo mas tarde ( y en la tabla de referencias pendientes.)
#3. generacion de salida
#   a. codigo objeto (en formato hexadecimal)
#   b. tabla de simbolos (para el enlazador)
#
# ----------------------    Programa sobre leer un archivo ensamblador
#-----------------------    Por:
#-----------------------        David muñoz Mendoza y Paulina Cano Barrera
import opcodes 
class EnsambladorIA32:
    def __init__(self):
        self.tabla_simbolos = {}
        self.referencias_pendientes = {} 
        self.codigo_hex = []
        self.instruccion = []
        
        self.contador_posicion = 0 # Location counter

    def ensamblar(self, archivo_entrada):
    #Metodo principal que realiza el ensamblado
        with open(archivo_entrada, 'r') as f:
            lineas = f.readlines()
            for linea in lineas:
                self.procesar_linea(linea)
                
        self.resolver_referencias_pendientes()
        self.generar_reportes()


    def procesar_linea(self, linea): 
        #Procesa una línea de código ensamblador
        cleaned_line = linea.strip() #Limpiar línea: quita espacios y comentarios
        for comentario in ('/', '#'):
            if comentario in cleaned_line:
                cleaned_line = cleaned_line.split(comentario)[0].strip()
        if not cleaned_line:
            return
        if cleaned_line.lower().startswith('org'): #Procesar directiva ORG
            partes = cleaned_line.split(None,1)
            if len(partes) > 1:
                direccion_str = partes[1]
                try:
                    direccion = int(direccion_str, 0)
                    self.contador_posicion = direccion
                except ValueError:
                    print(f"Error: Dirección inválida en ORG: {direccion_str}")
            return
        if ':' in cleaned_line:     #Procesar etiqueta si hay
            etiqueta, *code = cleaned_line.split(':', 1)
            etiqueta = etiqueta.strip()
            self.procesar_etiqueta(etiqueta)
            if code:
                linea_resto = code[0].strip()
                if linea_resto:
                    self.procesar_instruccion(linea_resto)
        else:
        #si no hay etiqueta, procesar la línea como instrucción directa
            self.procesar_instruccion(cleaned_line)
        return
        pass

    def procesar_etiqueta(self, etiqueta):
    #se detecta si la etiqueta es verdadera y si no esta duplicada
        if etiqueta:
            if etiqueta in self.tabla_simbolos:
                print(f"Error: Etiqueta duplicada '{etiqueta}'. Ignorando.")
            else:
                self.tabla_simbolos[etiqueta] = self.contador_posicion
            pass

    def procesar_instruccion(self, instruccion):
    #Procesa una instruccion y genera el codigo hex        
        instruccion = instruccion.lower().strip()
        partes = instruccion.split(None, 1)
        if not partes:
            return
        inst = partes[0].lower()
        operandos = [op.strip().lower() for op in partes[1].split(',')]
        if inst == 'mov':
            self.generar_mov(operandos)
        elif inst == 'add':
            self.generar_binaria(operandos, 'add')
        elif inst == 'sub':
            self.generar_binaria(operandos, 'sub')
        elif inst == 'cmp':
            self.generar_binaria(operandos, 'cmp')
        elif inst == 'jmp':
            if not operandos[0]:
                 print(f"Error: JMP requiere un operando de destino.")
                 return
            self.generar_salto_rel(operandos[0], 0xE9, 5)
        elif inst == 'je':
            if not operandos[0]:
                print(f"Error: JE requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x74, 2) 
            
        elif inst == 'jle':
            if not operandos[0]:
                print(f"Error: JLE requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x7E, 2)
            
        elif inst == 'jl':
            if not operandos[0]:
                print(f"Error: JL requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x7C, 2) 
            
        elif inst == 'jz':
            if not operandos[0]:
                print(f"Error: JX requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x74, 2)
        
        elif inst == 'jnz':
            if not operandos[0]:
                print(f"Error: JNZ requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x75, 2)
        elif inst == 'ja':
            if not operandos[0]:
                print(f"Error: JA requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x77, 2)
            
        elif inst == 'jae':
            if not operandos[0]:
                print(f"Error: JAE requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x73, 2)
        elif inst == 'jb':
            if not operandos[0]:
                print(f"Error: Jb requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x72, 2)    
        elif inst == 'jbe':
            if not operandos[0]:
                print(f"Error: JE requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x76, 2)  
        elif inst == 'jg':
            if not operandos[0]:
                print(f"Error: Jg requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x7F, 2)
        elif inst == 'jge':
            if not operandos[0]:
                print(f"Error: JGE requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x7D, 2)     
        elif inst == 'xor':
            self.generar_binaria(operandos, 'xor')
        elif inst == 'xchg':
            self.generar_xchg(operandos)
        elif inst == 'push':
            self.generar_push(operandos)
        elif inst == 'pop':
            self.generar_pop(operandos)
        elif inst == 'ret':
            self.generar_ret()
        elif inst == 'jb':
            if not operandos[0]:
                print(f"Error: JNE requiere un operando de destino.")
                return
            self.generar_salto_rel(operandos[0], 0x75, 2)
        elif inst == 'inc':
            self.generar_incdec(operandos, 'INC')
        elif inst == 'dec':
            self.generar_incdec(operandos, 'DEC')
        elif inst == 'mul':
            self.generar_mul(operandos)
        elif inst == 'imul':
            self.generar_imul(operandos)
        elif inst == 'div':
            self.generar_div(operandos)
        elif inst == 'idiv':
            self.generar_idiv(operandos)
        elif inst == 'call':
            if not operandos[0]:
                print(f"Error: call requiere un operando de destino.")
                return
            self.generar_call(operandos[0], 0xE8,2)
        else:
            print(f"Error: Instrucción '{inst}' no implementada o mal formada.")

    def generar_mov(self,partes):
        
            if len(partes) != 2:
                return
            op1, op2 = partes[0], partes[1]
            tamano = self.deducir_tamano_registro(op1)
            if tamano and op1 in opcodes.MOV_OPCODES[tamano]:
                opcode = int(opcodes.MOV_OPCODES[tamano][op1], 16)
                try:
                    valor = int(op2, 0)
                    self.codigo_hex.append(opcode)
                    if tamano == 8:
                        self.codigo_hex.append(valor & 0xFF)    
                    elif tamano == 32:
                        self.codigo_hex.append(valor & 0xFF)
                        self.codigo_hex.append((valor >> 8) & 0xFF)
                        self.codigo_hex.append((valor >> 16) & 0xFF)
                        self.codigo_hex.append((valor >> 24) & 0xFF)
                    self.contador_posicion += 1 + tamano // 8
                except ValueError:
                    print(f"Error: Valor inmediato no válido: {op2}")
                    pass
            if op1 in opcodes.REGISTROS_32_BIT and op2 in opcodes.REGISTROS_32_BIT :
                opcode = 0x89 # MOV r/m32, r32
                modrm = (0b11 << 6) | (opcodes.REGISTROS_32_BIT[op2] << 3) | opcodes.REGISTROS_32_BIT[op1]
                self.codigo_hex.extend([opcode, modrm])
                self.contador_posicion += 2
                return     
            if (op1.startswith('[') and op1.endswith(']')) or \
                (op2.startswith('[') and op2.endswith(']')):
                self.generar_mov_mem(op1, op2)
                return
    def generar_mov_mem(self, dest, res):
        #Genera el código para MOV con operandos de memoria (simplificado)
        if dest.startswith('[') and dest.endswith(']') and res == 'EAX':
            try:
                direccion = int(dest[1:-1], 0) #Extrae la dirección y convierte
                self.codigo_hex.append(0xA3) #opcode MOV mem32, EAX
                #Añadir dirección en little-endian
                for i in range(4):
                    self.codigo_hex.append((direccion >> (8 * i)) & 0xFF)
                self.contador_posicion += 5
                return
            except ValueError:
                print(f"Error: Dirección inválida en '{dest}' para MOV [dir], EAX")
                return
        # Formato: MOV EAX, [dir] (opcode A1)
        elif res.startswith('[') and res.endswith(']') and dest == 'EAX':
            try:
                direccion = int(res[1:-1], 0) # Extrae la dirección y convierte
                self.codigo_hex.append(0xA1) # opcode MOV EAX, mem32
          
                for i in range(4):
                    self.codigo_hex.append((direccion >> (8 * i)) & 0xFF)
                self.contador_posicion += 5
                return
            except ValueError:
                print(f"Error: Dirección inválida en '{res}' para MOV EAX, [dir]")
                return
        else:
            print(f"Error: MOV con memoria no soportada para los operandos: {dest}, {res}")
    def deducir_tamano_registro(self, registro):
        if registro in opcodes.MOV_OPCODES[8]:
            return 8
        elif registro in opcodes.MOV_OPCODES[16]:
            return 16    
        elif registro in opcodes.MOV_OPCODES[32]:
            return 32
        else:
            return None
    #Funcion para la realizacion de instrucciones matematicas como add y sub asi como xor y cmp
    def generar_binaria(self, operandos, operacion):
        if len(operandos) != 2:
            print(f"Error: {operacion} requiere 2 operandos.")
            return
        dest, src = operandos[0], operandos[1]
        opmap = {'add': 0x01, 'sub': 0x29, 'cmp': 0x39, 'xor': 0x31}
        immmap = {'add': 0b000, 'sub': 0b101, 'cmp': 0b111, 'xor': 0b110}
        if dest in opcodes.REGISTROS_32_BIT and src in opcodes.REGISTROS_32_BIT:
            opcode = opmap[operacion]
            modrm = (0b11 << 6) | \
                    (opcodes.REGISTROS_32_BIT[src] << 3) | \
                    opcodes.REGISTROS_32_BIT[dest]
            self.codigo_hex.extend([opcode, modrm])
            self.contador_posicion += 2
            return
        # Caso: REG, IMM (Ej: ADD EAX, 10h)
        if dest in opcodes.REGISTROS_32_BIT:
            try:
                valor = int(src, 0)
                opcode = 0x81 # Opcode base para ADD/SUB/CMP reg32, imm32
                reg_field = immmap[operacion] # Campo 'reg' en ModR/M

                modrm = (0b11 << 6) | \
                        (reg_field << 3) | \
                        opcodes.REGISTROS_32_BIT[dest]

                self.codigo_hex.extend([opcode, modrm])
                # Añadir valor inmediato en little-endian (4 bytes para 32-bit)
                for i in range(4):
                    self.codigo_hex.append((valor >> (8 * i)) & 0xFF)
                self.contador_posicion += 6 # 1 opcode + 1 modrm + 4 bytes inmediato
                return
            except ValueError:
                pass # No es un valor inmediato, fallar al siguiente caso
        print(f"Error: operandos inválidos para {operacion}: {dest}, {src}")

    def generar_call(self, etiqueta,code_base,largo_instruccion):
        # Caso 1: CALL a una etiqueta (llamada relativa)
        if etiqueta in self.tabla_simbolos:
            dir_etiqueta = self.tabla_simbolos[etiqueta]
            offset = dir_etiqueta - (self.contador_posicion + largo_instruccion)
            self.codigo_hex.append(code_base)
            for i in range(4):
                self.codigo_hex.append((offset >> (8 * i)) & 0xFF)
            self.contador_posicion += largo_instruccion
            return
        elif etiqueta in opcodes.REGISTROS_32_BIT:
            #CALL r/m32 (opcode FF /2)
            opcode = 0xFF
            modrm = (0b11 << 6) | (0b010 << 3) | opcodes.REGISTROS_32_BIT[etiqueta]
            self.codigo_hex.extend([opcode, modrm])
            self.contador_posicion += 2 
            return
        else:
            print(f"Advertencia: Etiqueta '{etiqueta}' no definida para CALL. Añadiendo a referencias pendientes.")
            #marcar posición y rellenar con ceros para el offset de 4 bytes
            self.referencias_pendientes.setdefault(etiqueta, []).append(self.contador_posicion)
            self.codigo_hex.append(0xE8)
            for _ in range(4): # Rellenar con 4 bytes de ceros
                self.codigo_hex.append(0x00)
            self.contador_posicion += 5
            return
            # print(f"Error: Operando '{target}' no válido o no soportado para CALL.")

    def generar_salto_rel(self, etiqueta, opcode_base, largo_instruccion): #Funciones para la solucion de los saltos 
        if etiqueta in self.tabla_simbolos:
            dir_etiqueta = self.tabla_simbolos[etiqueta]
            # Offset relativo: destino - (posición actual + longitud de la instrucción de salto)
            offset = dir_etiqueta - (self.contador_posicion + largo_instruccion)

            self.codigo_hex.append(opcode_base)
            if largo_instruccion == 2:
                #El offset de 8 bits debe estar en el rango -128 a 127
                if not (-128 <= offset <= 127):
                    print(f"Advertencia: Salto corto para '{etiqueta}' está fuera de rango. Puede fallar.")
                self.codigo_hex.append(offset & 0xFF)
            elif largo_instruccion == 5: # JMP rel32
                for i in range(4):
                    self.codigo_hex.append((offset >> (8 * i)) & 0xFF)
            self.contador_posicion += largo_instruccion
        else:
            #Si la etiqueta no está en la tabla de símbolos, es una referencia pendiente
            self.referencias_pendientes.setdefault(etiqueta, []).append(self.contador_posicion)
            self.codigo_hex.append(opcode_base)
            #Rellenar con ceros temporales
            for _ in range(largo_instruccion - 1):
                self.codigo_hex.append(0x00)
            self.contador_posicion += largo_instruccion

    def generar_incdec(self, operandos, operacion_tipo):
        if len(operandos) != 1:
            print(f"Error: {operacion_tipo} requiere 1 operando.")
            return
        reg = operandos[0]
        if reg not in opcodes.REGISTROS_32_BIT:
            print(f"Error: Registro '{reg}' no válido para {operacion_tipo}.")
            return
        #Opcodes directos para INC/DEC reg32 (40h + reg_encoding / 48h + reg_encoding)
        base_opcode = 0x40 if operacion_tipo == 'INC' else 0x48
        opcode = base_opcode + opcodes.REGISTROS_32_BIT[reg]
        self.codigo_hex.append(opcode)
        self.contador_posicion += 1

    def generar_mul(self, operandos):
        #multiplica EAX por el registro dado y guarda en EDX:EAX
        if len(operandos) != 1 or operandos[0] not in opcodes.REGISTROS_32_BIT:
            print("Error: MUL requiere 1 operando válido.")
            return
        reg = opcodes.REGISTROS_32_BIT[operandos[0]]
        self.codigo_hex.extend([0xF7, (0b11 << 6) | (0b100 << 3) | reg])
        self.contador_posicion += 2

    def generar_imul(self, operandos): 
        #permite 1, 2 o 3 operandos 
        n = len(operandos)
        if n not in (1, 2, 3):
            print("Error: IMUL admite 1, 2 o 3 operandos.")
            return
        try:
            if n == 1:
                reg = operandos[0]
                if reg in opcodes.REGISTROS_32_BIT:
                    self.codigo_hex.extend([0xF7, (0b11 << 6) | (0b101 << 3) | opcodes.REGISTROS_32_BIT[reg]])
                    self.contador_posicion += 2
                else:
                    raise ValueError("Registro inválido")
            elif n == 2:
                dest, src = operandos
                if dest in opcodes.REGISTROS_32_BIT and src in opcodes.REGISTROS_32_BIT:
                    modrm = (0b11 << 6) | (opcodes.REGISTROS_32_BIT[dest] << 3) | opcodes.REGISTROS_32_BIT[src]
                    self.codigo_hex.extend([0x0F, 0xAF, modrm])
                    self.contador_posicion += 3
                else:
                    raise ValueError("Registros inválidos")
            elif n == 3:
                dest, src, imm = operandos
                if dest not in opcodes.REGISTROS_32_BIT:
                    raise ValueError("Registro destino inválido")
                r_dest = opcodes.REGISTROS_32_BIT[dest]
                if src in opcodes.REGISTROS_32_BIT:
                    modrm = (0b11 << 6) | (r_dest) | (opcodes.REGISTROS_32_BIT[src] << 3)
                elif src.startswith('(') and src.endswith(')'):
                    base = src[1:-1]
                    if base not in opcodes.REGISTROS_32_BIT:
                        raise ValueError("Base de memoria inválida")
                    modrm = (0b00 << 6) | (r_dest) | (opcodes.REGISTROS_32_BIT[base] << 3)
                else:
                    raise ValueError("Segundo operando inválido")
                inmediato = int(imm, 0)
                if -128 <= inmediato <= 127:
                    self.codigo_hex.extend([0x6B, modrm, inmediato & 0xFF])
                    self.contador_posicion += 3
                else:
                    self.codigo_hex.extend([0x69, modrm])
                    self.codigo_hex.extend([(inmediato >> (8 * i)) & 0xFF for i in range(4)])
                    self.contador_posicion += 6
        except ValueError as e:
            print(f"Error en IMUL: {e}")

    def generar_div(self, operandos):
        #divide sin signo el valor en EDX:EAX entre reg
        if len(operandos) != 1 or operandos[0] not in opcodes.REGISTROS_32_BIT:
            print("Error: DIV requiere 1 operando válido.")
            return
        reg = opcodes.REGISTROS_32_BIT[operandos[0]]
        self.codigo_hex.extend([0xF7, (0b11 << 6) | (0b110 << 3) | reg])
        self.contador_posicion += 2

    def generar_idiv(self, operandos):
        #divide con signo el valor en EDX:EAX entre reg
        if len(operandos) != 1 or operandos[0] not in opcodes.REGISTROS_32_BIT:
            print("Error: IDIV requiere 1 operando válido.")
            return
        reg = opcodes.REGISTROS_32_BIT[operandos[0]]
        self.codigo_hex.extend([0xF7, (0b11 << 6) | (0b111 << 3) | reg])
        self.contador_posicion += 2
        
    def generar_xchg(self, operandos): 
        # Si ambos operandos son registros usa la instrucción XOR entre ellos
        # Si el segundo operando es un valor inmediato usa XOR con un valor constante
        if len(operandos) != 2:
            print("Error: XCHG requiere 2 operandos.")
            return
        op1, op2 = operandos
        reg = opcodes.REGISTROS_32_BIT

        if op1 == 'eax' and op2 in reg:
            self.codigo_hex.append(0x90 + reg[op2])
            self.contador_posicion += 1
            return
        if op2 == 'eax' and op1 in reg:
            self.codigo_hex.append(0x90 + reg[op1])
            self.contador_posicion += 1
            return
        if op1 in reg and op2 in reg:
            modrm = (0b11 << 6) | (reg[op1] << 3) | reg[op2]
            self.codigo_hex.extend([0x87, modrm])
            self.contador_posicion += 2
            return
        if op1.startswith('(') and op1.endswith(')') and op2 in reg:
            base = op1[1:-1]
            if base in reg:
                modrm = (0b00 << 6) | (reg[op2] << 3) | reg[base]
                self.codigo_hex.extend([0x87, modrm])
                self.contador_posicion += 2
                return
        if op2.startswith('(') and op2.endswith(')') and op1 in reg:
            base = op2[1:-1]
            if base in reg:
                modrm = (0b00 << 6) | (reg[op1] << 3) | reg[base]
                self.codigo_hex.extend([0x87, modrm])
                self.contador_posicion += 2
                return
        print(f"Error: Operandos inválidos para XCHG: {operandos}")

    def generar_push(self, operandos):
        #guarda el registro en la pila
        if len(operandos) != 1:
            print("Error: PUSH requiere 1 operando.")
            return
        reg = operandos[0]
        if reg in opcodes.REGISTROS_32_BIT:
            self.codigo_hex.append(0x50 + opcodes.REGISTROS_32_BIT[reg])
            self.contador_posicion += 1
        else:
            print(f"Error: PUSH inválido: {reg}")

    def generar_pop(self, operandos):
        #recupera de la pila al registro
        if len(operandos) != 1:
            print("Error: POP requiere 1 operando.")
            return
        reg = operandos[0]
        if reg in opcodes.REGISTROS_32_BIT:
            self.codigo_hex.append(0x58 + opcodes.REGISTROS_32_BIT[reg])
            self.contador_posicion += 1
        else:
            print(f"Error: POP inválido: {reg}")

    def generar_ret(self):
        #genera el opcode de RET (0xC3), que retorna de una subrutina
        self.codigo_hex.append(0xC3)
        self.contador_posicion += 1

    def resolver_referencias_pendientes(self):
    #Segunda pasada para resolver referencias pendientes
        for simbolo, direcciones in self.referencias_pendientes.items():
            if simbolo in self.tabla_simbolos:
                for dir in direcciones:
        # Calcular desplazamiento y parchear codigo
                    pass

    def generar_hex(self, archivo_salida):
    #genera archivo con el codigo maquina en hex
        with open(archivo_salida,'w') as f:
            for i,byte in enumerate(self.codigo_hex):
                if isinstance(byte, str):  
                    byte = int(byte, 16)          
                f.write(f"{byte:02X} ")

    def generar_reportes(self):
    #genera reportes de tablas de simbolos y referencias"""
        with open('simbolos.txt', 'w') as f:
            for simb, dir in self.tabla_simbolos.items():
                f.write(f"{simb}: {dir:04X}\n")
        with open('referencias.txt', 'w') as f:
            for simb, dirs in self.referencias_pendientes.items():
                f.write(f"{simb}: {',' .join(hex(d) for d in dirs)}\n")


 # Ejemplo de uso
if __name__ == "__main__":
    ensamblador = EnsambladorIA32()
    ensamblador.ensamblar('programa.asm')
    ensamblador.resolver_referencias_pendientes()
    ensamblador.generar_hex('programa.hexx')
    ensamblador.generar_reportes()