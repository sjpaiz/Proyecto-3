import tkinter as tk
from tkinter import ttk
import time
from fabrica_maquinas import FabricaMaquinasTuring

BG = "#f5ecf7"
CELL_BG = "#fceefc"
CELL_OUTLINE = "#caa0d7"
TEXT_COLOR = "#6c5b7b"
ACCENT = "#a987b5"

class InterfazTuring:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")
        self.root.geometry("850x600")
        self.root.config(bg=BG)

        self.maquina = None
        self.animando = False

        titulo = tk.Label(
            root, 
            text="Simulador de Máquina de Turing",
            font=("Century Gothic", 18, "bold"),
            bg=BG,
            fg=ACCENT
        )
        titulo.pack(pady=15)

        frame_maquina = tk.Frame(root, bg=BG)
        frame_maquina.pack(pady=5)

        tk.Label(frame_maquina, text="Seleccionar máquina:", 
                 font=("Poppins", 11), bg=BG, fg=TEXT_COLOR).pack(side="left", padx=5)

        self.combo_maquina = ttk.Combobox(
            frame_maquina, 
            values=[
                "1. (0+1)*00(0+1)* — Contiene dos 0 consecutivos",
                "2. (a|b)*abb — Termina con 'abb'",
                "3. 1(0+1)*1 — Empieza y termina con 1",
                "4. (ab)* — Repeticiones de 'ab'",
                "5. (0+1)*010(0+1)* — Contiene el patrón '010'"
            ],
            state="readonly", width=45, font=("Poppins", 10)
        )
        self.combo_maquina.pack(side="left", padx=5)
        self.combo_maquina.current(0)

        ttk.Button(frame_maquina, text="Cargar", command=self.cargar_maquina).pack(side="left", padx=8)

        # Entrada de cadena
        frame_cadena = tk.Frame(root, bg=BG)
        frame_cadena.pack(pady=10)

        tk.Label(frame_cadena, text="Cadena:", font=("Poppins", 11), bg=BG, fg=TEXT_COLOR).pack(side="left", padx=5)
        self.entry_cadena = ttk.Entry(frame_cadena, font=("Poppins", 11), width=25)
        self.entry_cadena.pack(side="left", padx=5)

        # Botones de controles
        frame_botones = tk.Frame(root, bg=BG)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Paso a Paso", command=self.ejecutar_paso).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botones, text="Automático", command=self.ejecutar_automatico).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botones, text="Reiniciar", command=self.reiniciar).grid(row=0, column=2, padx=5)

        # Visualización
        self.canvas = tk.Canvas(root, width=750, height=200, bg="#fdfaff", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.estado_label = tk.Label(root, text="Seleccione una máquina para comenzar.", 
                                     font=("Century Gothic", 12), bg=BG, fg=TEXT_COLOR)
        self.estado_label.pack(pady=10)

        # Flechas y cintas
        self.rects = []
        self.texts = []
        self.cell_width = 50
        self.cell_height = 50
        self.left_margin = 80
        self.arrow = None

    def cargar_maquina(self):
        opcion = self.combo_maquina.get().split(".")[0]
        self.maquina, _, _ = FabricaMaquinasTuring.obtener_maquina(opcion)
        cadena = self.entry_cadena.get().strip()
        try:
            self.maquina.establecer_entrada(cadena)
            self.dibujar_cinta()
            self.estado_label.config(text=f"Máquina cargada - Estado: {self.maquina.estado_actual}")
        except Exception as e:
            self.estado_label.config(text=f"Error: {e}")

    def dibujar_cinta(self):
        self.canvas.delete("all")
        self.rects.clear()
        self.texts.clear()
        self.arrow = None

        if not self.maquina:
            return
        
        cinta = self.maquina.cinta
        y_inicio = 90

        for i, simbolo in enumerate(cinta):
            x = self.left_margin + i * self.cell_width
            r = self.canvas.create_rectangle(x, y_inicio, x + self.cell_width, y_inicio + self.cell_height, 
                                             fill=CELL_BG, outline=CELL_OUTLINE, width=2)
            t = self.canvas.create_text(x + self.cell_width / 2, y_inicio + self.cell_height / 2, 
                                        text=simbolo, font=("Consolas", 16), fill=TEXT_COLOR)
            self.rects.append(r)
            self.texts.append(t)

        self._dibujar_flecha(self.maquina.posicion_cabezal)

    def _dibujar_flecha(self, pos):
        if self.arrow:
            for part in self.arrow:
                self.canvas.delete(part)
        if pos < 0 or pos >= len(self.rects):
            return
        coords = self.canvas.coords(self.rects[pos])
        x1, y1, x2, y2 = coords
        cx = (x1 + x2) / 2
        top = y1 - 20
        line = self.canvas.create_line(cx, top, cx, y1 - 2, fill=ACCENT, width=2)
        arrow_tip = self.canvas.create_polygon(cx - 6, y1 - 8, cx + 6, y1 - 8, cx, y1,
                                               fill=ACCENT, outline=ACCENT)
        self.arrow = (line, arrow_tip)

    def ejecutar_paso(self):
        if not self.maquina:
            self.estado_label.config(text="Primero debe cargar una máquina.")
            return
        
        seguir = self.maquina.ejecutar_paso()
        self.dibujar_cinta()
        if not seguir:
            self.estado_label.config(text=f"Cadena {self.maquina.obtener_estado_actual()}")
        else:
            self.estado_label.config(text=f"Paso: {self.maquina.pasos} | Estado: {self.maquina.estado_actual}")

    def ejecutar_automatico(self):
        if not self.maquina:
            self.estado_label.config(text="Primero debe cargar una máquina.")
            return
        if self.animando:
            return
        self.animando = True
        self._animar()

    def _animar(self):
        if not self.animando or self.maquina.estado_actual in [self.maquina.estado_aceptacion, self.maquina.estado_rechazo]:
            self.estado_label.config(text=f"Cadena {self.maquina.obtener_estado_actual()}")
            self.animando = False
            return
        self.maquina.ejecutar_paso()
        self.dibujar_cinta()
        self.estado_label.config(text=f"Paso: {self.maquina.pasos} | Estado: {self.maquina.estado_actual}")
        self.root.after(500, self._animar)

    def reiniciar(self):
        self.animando = False
        if self.maquina:
            self.maquina.reiniciar()
        self.dibujar_cinta()
        self.estado_label.config(text="Máquina reiniciada.")

# Ejecutar interfaz
root = tk.Tk()
app = InterfazTuring(root)
root.mainloop()
