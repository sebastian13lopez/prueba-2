import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Crear el diagrama de Venn para tres conjuntos
plt.figure(figsize=(8, 8))
venn = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'))

# Paso 1: Sombrear la diferencia simétrica B Δ C
# Colorear las áreas de B y C que no están en la intersección
venn.get_patch_by_id('010').set_color('red')  # Solo B
venn.get_patch_by_id('010').set_alpha(0.7)

venn.get_patch_by_id('001').set_color('red')  # Solo C
venn.get_patch_by_id('001').set_alpha(0.7)

# Paso 2: Sombrear el complemento de A (A^c)
# Colorear el fondo azul donde no está A
for subset in ['010', '001', '011']:  # Partes de B y C fuera de A
    venn.get_patch_by_id(subset).set_color('blue')
    venn.get_patch_by_id(subset).set_alpha(0.3)

# Paso 3: Configurar transparencia y colores en las demás áreas para dejarlas sin sombrear
venn.get_patch_by_id('100').set_alpha(0)  # Solo A
venn.get_patch_by_id('110').set_alpha(0)  # A y B
venn.get_patch_by_id('101').set_alpha(0)  # A y C
venn.get_patch_by_id('111').set_alpha(0)  # A, B y C

# Configurar el título y mostrar el diagrama
plt.title("Diagrama de Venn para (B Δ C) y A^c")
plt.show()
