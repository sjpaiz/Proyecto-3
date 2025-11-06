class MaquinaTuring:
    def __init__(self, estados, alfabeto, alfabeto_cinta, transiciones, 
                 estado_inicial, estado_aceptacion, estado_rechazo, simbolo_blanco='_'):
        self.estados = estados
        self.alfabeto = alfabeto
        self.alfabeto_cinta = alfabeto_cinta
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado_aceptacion = estado_aceptacion
        self.estado_rechazo = estado_rechazo
        self.simbolo_blanco = simbolo_blanco
        self.reiniciar()

    def reiniciar(self):
        #Reinicia la máquina al estado inicial
        self.cinta = [self.simbolo_blanco]
        self.posicion_cabezal = 0
        self.estado_actual = self.estado_inicial
        self.pasos = 0
        self.historial = []

    def establecer_entrada(self, cadena_entrada):
        #Configura la cadena de entrada en la cinta
        self.reiniciar()
        
        # Validar que todos los caracteres estén en el alfabeto
        for caracter in cadena_entrada:
            if caracter not in self.alfabeto:
                raise ValueError(f"Carácter '{caracter}' no está en el alfabeto: {self.alfabeto}")
        
        # Configurar la cinta con la entrada
        self.cinta = list(cadena_entrada) + [self.simbolo_blanco]
        self._registrar_estado()

    def _registrar_estado(self):
        #Registra el estado actual 
        self.historial.append({
            'cinta': self.cinta.copy(),
            'posicion_cabezal': self.posicion_cabezal,
            'estado': self.estado_actual,
            'paso': self.pasos
        })

    def ejecutar_paso(self):
        if self.estado_actual in [self.estado_aceptacion, self.estado_rechazo]:
            return False

        # Obtener símbolo actual bajo el cabezal
        simbolo_actual = self.cinta[self.posicion_cabezal]
        
        # Buscar transición válida
        clave = (self.estado_actual, simbolo_actual)
        
        if clave in self.transiciones:
            nuevo_estado, escribir_simbolo, direccion = self.transiciones[clave]
            
            # 1. Escribir en la cinta
            self.cinta[self.posicion_cabezal] = escribir_simbolo
            
            # 2. Mover el cabezal
            if direccion == 'R':  # Derecha
                self.posicion_cabezal += 1
                # Extender cinta si es necesario
                if self.posicion_cabezal >= len(self.cinta):
                    self.cinta.append(self.simbolo_blanco)
            elif direccion == 'L':  # Izquierda
                self.posicion_cabezal -= 1
                # Extender cinta si es necesario
                if self.posicion_cabezal < 0:
                    self.cinta.insert(0, self.simbolo_blanco)
                    self.posicion_cabezal = 0
            
            # 3. Actualizar estado
            self.estado_actual = nuevo_estado
            self.pasos += 1
            
            self._registrar_estado()
            return True
        else:
            # No hay transición 
            self.estado_actual = self.estado_rechazo
            self._registrar_estado()
            return False

    def ejecutar_automatico(self):
        while self.ejecutar_paso():
            pass
        return self.estado_actual == self.estado_aceptacion

    def obtener_visualizacion_cinta(self):
        cinta_visual = ""
        for i, simbolo in enumerate(self.cinta):
            if i == self.posicion_cabezal:
                cinta_visual += f"[{simbolo}]"  # Cabezal en posición actual
            else:
                cinta_visual += f" {simbolo} "
        
        indicador_cabezal = " " * (self.posicion_cabezal * 3 + 1) + "↑"
        
        return cinta_visual, indicador_cabezal

    def es_aceptada(self):
        return self.estado_actual == self.estado_aceptacion

    def obtener_estado_actual(self):
        if self.estado_actual == self.estado_aceptacion:
            return "ACEPTADA"
        elif self.estado_actual == self.estado_rechazo:
            return "RECHAZADA"
        else:
            return f"Ejecutando - Estado: {self.estado_actual}"