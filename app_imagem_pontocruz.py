import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        grid_x = grid_slider_x.get()
        grid_y = grid_slider_y.get()
        num_colors = color_slider.get()
        process_image(file_path, grid_x, grid_y, num_colors)
       
        #process_image(file_path, grid_slider.get(), color_slider.get())

def adicionar_preto_branco(img):
    largura, altura = img.size
    nova_img = Image.new("RGB", (largura + 2, altura + 1), "white")
    nova_img.paste(img, (0, 0))
    draw = ImageDraw.Draw(nova_img)
    draw.point((largura, altura), fill=(0, 0, 0))       # Preto
    draw.point((largura + 1, altura), fill=(255, 255, 255))  # Branco
    return nova_img

def gerar_legenda(img_quantized):
    palette = img_quantized.getpalette()
    used_colors = sorted(set(img_quantized.getdata()))
    legenda = {}
    for i, color_index in enumerate(used_colors):
        r = palette[color_index * 3]
        g = palette[color_index * 3 + 1]
        b = palette[color_index * 3 + 2]
        legenda[f"Cor {i+1}"] = (r, g, b)
    print("\n🧵 Legenda de Cores Utilizadas:")
    for cor, rgb in legenda.items():
        print(f"{cor}: RGB{rgb}")

def salvar_grafico(rgb_pixels, grid_x, grid_y, num_colors):
    altura, largura = rgb_pixels.shape[:2]
    plt.figure(figsize=(8, 8))
    plt.imshow(rgb_pixels, interpolation='nearest', aspect='equal')
    plt.xticks(range(largura))
    plt.yticks(range(altura))
    plt.gca().set_xticks(np.arange(-0.5, largura, 1), minor=True)
    plt.gca().set_yticks(np.arange(-0.5, altura, 1), minor=True)
    plt.grid(True, which='minor', color='gray', linewidth=0.5)
   # plt.gca().invert_yaxis()
    plt.title(f"Gráfico de Ponto Cruz ({grid_x}x{grid_y}, {num_colors} cores)")
    nome_arquivo = f"grafico_ponto_cruz_{grid_x}x{grid_y}_{num_colors}cores.png"
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300)
    plt.close()
    print(f"Gráfico salvo como: {nome_arquivo}")

def reconstruir_imagem_rgb(img_quantized):
    palette = img_quantized.getpalette()
    pixels = np.array(img_quantized)
    rgb_array = np.zeros((pixels.shape[0], pixels.shape[1], 3), dtype=np.uint8)
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            idx = pixels[i, j]
            rgb_array[i, j] = palette[idx*3:idx*3+3]
    return rgb_array

def exibir_grafico_com_grid(rgb_pixels, grid_x, grid_y, num_colors):
    plt.clf()
    plt.close('all')

    altura, largura = rgb_pixels.shape[:2]

    plt.figure(figsize=(8, 8))
    plt.imshow(rgb_pixels, interpolation='nearest', aspect='equal')

    # Ticks para cada ponto da grade
    plt.xticks(range(largura))
    plt.yticks(range(altura))

    # Grid menor para marcar os quadradinhos
    plt.gca().set_xticks(np.arange(-0.5, largura, 1), minor=True)
    plt.gca().set_yticks(np.arange(-0.5, altura, 1), minor=True)
    plt.grid(True, which='minor', color='gray', linewidth=0.5)

    plt.title(f"Gráfico de Ponto Cruz ({grid_x}x{grid_y}, {num_colors} cores)")
    plt.tight_layout()
    plt.show()

def process_image(image_path, grid_x, grid_y, num_colors):
    img = Image.open(image_path).convert("RGB")
    img = img.rotate(270, expand=True)
    img_small = img.resize(( grid_x, grid_y), resample=Image.Resampling.NEAREST)
    img_small = adicionar_preto_branco(img_small)

    # Quantiza a imagem
    img_quantized = img_small.convert("P", palette=Image.Palette.ADAPTIVE, colors=num_colors)

    # Reconstrói com cores reais
    rgb_pixels = reconstruir_imagem_rgb(img_quantized)

    # Exibe o gráfico
    #plt.figure(figsize=(8, 8))
    #plt.imshow(rgb_pixels, interpolation='nearest', aspect='equal')
    #plt.xticks(np.arange(-0.5, rgb_pixels.shape[1], 1), [])
    #plt.yticks(np.arange(-0.5, rgb_pixels.shape[0], 1), [])
    #plt.gca().set_xticks(np.arange(-0.5, rgb_pixels.shape[1], 1), minor=True)
    #plt.gca().set_yticks(np.arange(-0.5, rgb_pixels.shape[0], 1), minor=True)
    #plt.grid(True, color='gray', linewidth=0.5)
    #plt.title(f"Gráfico de Ponto Cruz ({grid_size}x{grid_size}, {num_colors} cores)")
    #plt.show()
    exibir_grafico_com_grid(rgb_pixels, grid_x, grid_y, num_colors)
    salvar_grafico(rgb_pixels, grid_x, grid_y, num_colors)
    gerar_legenda(img_quantized)

# Interface
root = tk.Tk()
root.title("Gerador de Gráfico de Ponto Cruz")

'''tk.Label(root, text="Tamanho da Grade (pontos)").pack()
grid_slider = tk.Scale(root, from_=30, to=150, orient=tk.HORIZONTAL)
grid_slider.set(50)
grid_slider.pack()'''

tk.Label(root, text="Quantidade de pixels - Horizontal").pack()
grid_slider_x = tk.Scale(root, from_=30, to=300, orient=tk.HORIZONTAL)
grid_slider_x.set(50)
grid_slider_x.pack()

tk.Label(root, text="Quantidade pixels - Vertical").pack()
grid_slider_y = tk.Scale(root, from_=30, to=300, orient=tk.HORIZONTAL)
grid_slider_y.set(50)
grid_slider_y.pack()


tk.Label(root, text="Número de Cores").pack()
color_slider = tk.Scale(root, from_=2, to=50, orient=tk.HORIZONTAL)
color_slider.set(20)
color_slider.pack()

tk.Button(root, text="Selecionar Imagem", command=select_image).pack(pady=10)

root.mainloop()

""" ESTA FUNCAO FUNCIONA MAS IGNORA A PALETA DE CORES
def process_image(image_path, grid_size, num_colors):
    img = Image.open(image_path).convert("RGB")
    img_small = img.resize((grid_size, grid_size), resample=Image.Resampling.NEAREST)
    img_small = adicionar_preto_branco(img_small)
    pixels = np.array(img_small)

    plt.figure(figsize=(8, 8))
    plt.imshow(pixels, interpolation='none', aspect='equal')
    plt.xticks(np.arange(-0.5, pixels.shape[1], 1), [])
    plt.yticks(np.arange(-0.5, pixels.shape[0], 1), []) 
    plt.gca().set_xticks(np.arange(-0.5, pixels.shape[1], 1), minor=True)
    plt.gca().set_yticks(np.arange(-0.5, pixels.shape[0], 1), minor=True)
    plt.grid(True, color='gray', linewidth=0.5)
    plt.title(f"Gráfico de Ponto Cruz ({grid_size}x{grid_size}, {num_colors} cores)")
    plt.show()
    salvar_grafico(pixels, grid_size, num_colors)
    gerar_legenda(img_small)
    """
