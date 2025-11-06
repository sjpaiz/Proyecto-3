from maquina_turing import MaquinaTuring

class FabricaMaquinasTuring:

    @staticmethod
    def crear_maquina1():
        #Máquina para (0+1)*00(0+1)* 
        return MaquinaTuring(
            estados=['q0', 'q1', 'q2', 'qa', 'qr'],
            alfabeto=['0', '1'],
            alfabeto_cinta=['0', '1', '_'],
            transiciones={
                ('q0', '0'): ('q1', '0', 'R'),
                ('q0', '1'): ('q0', '1', 'R'),
                ('q0', '_'): ('qr', '_', 'R'),
                
                ('q1', '0'): ('q2', '0', 'R'),
                ('q1', '1'): ('q0', '1', 'R'),
                ('q1', '_'): ('qr', '_', 'R'),
                
                ('q2', '0'): ('q2', '0', 'R'),
                ('q2', '1'): ('q2', '1', 'R'),
                ('q2', '_'): ('qa', '_', 'R'),
            },
            estado_inicial='q0',
            estado_aceptacion='qa',
            estado_rechazo='qr'
        )
    
    @staticmethod
    def crear_maquina2():
        #Máquina para (a|b)*abb 
        return MaquinaTuring(
            estados=['q0', 'q1', 'q2', 'q3', 'qa', 'qr'],
            alfabeto=['a', 'b'],
            alfabeto_cinta=['a', 'b', '_'],
            transiciones={
                ('q0', 'a'): ('q1', 'a', 'R'),
                ('q0', 'b'): ('q0', 'b', 'R'),
                ('q1', 'a'): ('q1', 'a', 'R'),
                ('q1', 'b'): ('q2', 'b', 'R'),
                ('q2', 'a'): ('q1', 'a', 'R'),
                ('q2', 'b'): ('q3', 'b', 'R'),
                ('q3', 'a'): ('q1', 'a', 'R'),
                ('q3', 'b'): ('q0', 'b', 'R'),
                ('q0', '_'): ('qa', '_', 'R'),
                ('q1', '_'): ('qr', '_', 'R'),
                ('q2', '_'): ('qr', '_', 'R'),
                ('q3', '_'): ('qa', '_', 'R'),
            },
            estado_inicial='q0',
            estado_aceptacion='qa',
            estado_rechazo='qr'
        )
    
    @staticmethod
    def crear_maquina3():
        #Máquina para 1(0+1)*1 
        return MaquinaTuring(
            estados=['q0', 'q1', 'q2', 'qa', 'qr'],
            alfabeto=['0', '1'],
            alfabeto_cinta=['0', '1', '_'],
            transiciones={
                ('q0', '1'): ('q1', '1', 'R'),
                ('q0', '0'): ('qr', '0', 'R'),
                ('q0', '_'): ('qr', '_', 'R'),
                
                ('q1', '0'): ('q1', '0', 'R'),
                ('q1', '1'): ('q1', '1', 'R'),
                ('q1', '_'): ('q2', '_', 'L'),
                
                ('q2', '0'): ('qr', '0', 'R'),
                ('q2', '1'): ('qa', '1', 'R'),
            },
            estado_inicial='q0',
            estado_aceptacion='qa',
            estado_rechazo='qr'
        )
    
    @staticmethod
    def crear_maquina4():
        #Máquina para (ab)* 
        return MaquinaTuring(
            estados=['q0', 'q1', 'qa', 'qr'],
            alfabeto=['a', 'b'],
            alfabeto_cinta=['a', 'b', '_'],
            transiciones={
                ('q0', 'a'): ('q1', 'a', 'R'),
                ('q0', '_'): ('qa', '_', 'R'),
                ('q1', 'b'): ('q0', 'b', 'R'),
                ('q1', 'a'): ('qr', 'a', 'R'),
                ('q1', '_'): ('qr', '_', 'R'),
            },
            estado_inicial='q0',
            estado_aceptacion='qa',
            estado_rechazo='qr'
        )
    
    @staticmethod
    def crear_maquina5():
        #Máquina para (0+1)*010(0+1)* 
        return MaquinaTuring(
            estados=['q0', 'q1', 'q2', 'q3', 'qa', 'qr'],
            alfabeto=['0', '1'],
            alfabeto_cinta=['0', '1', '_'],
            transiciones={
                ('q0', '0'): ('q1', '0', 'R'),
                ('q0', '1'): ('q0', '1', 'R'),
                ('q0', '_'): ('qr', '_', 'R'),
                
                ('q1', '0'): ('q1', '0', 'R'),
                ('q1', '1'): ('q2', '1', 'R'),
                ('q1', '_'): ('qr', '_', 'R'),
                
                ('q2', '0'): ('q3', '0', 'R'),
                ('q2', '1'): ('q0', '1', 'R'),
                ('q2', '_'): ('qr', '_', 'R'),
                
                ('q3', '0'): ('q3', '0', 'R'),
                ('q3', '1'): ('q3', '1', 'R'),
                ('q3', '_'): ('qa', '_', 'R'),
            },
            estado_inicial='q0',
            estado_aceptacion='qa',
            estado_rechazo='qr'
        )
    
    @staticmethod
    def obtener_maquina(opcion):
        maquinas = {
            '1': (FabricaMaquinasTuring.crear_maquina1, "(0+1)*00(0+1)*", "Contiene al menos dos 0's consecutivos"),
            '2': (FabricaMaquinasTuring.crear_maquina2, "(a|b)*abb", "Cadenas que terminan con 'abb'"),
            '3': (FabricaMaquinasTuring.crear_maquina3, "1(0+1)*1", "Empieza y termina con 1"),
            '4': (FabricaMaquinasTuring.crear_maquina4, "(ab)*", "Repeticiones de 'ab'"),
            '5': (FabricaMaquinasTuring.crear_maquina5, "(0+1)*010(0+1)*", "Contiene el patron '010'")
        }
        
        if opcion in maquinas:
            funcion, regex, descripcion = maquinas[opcion]
            return funcion(), regex, descripcion
        else:
            raise ValueError("Opcion de maquina no valida")