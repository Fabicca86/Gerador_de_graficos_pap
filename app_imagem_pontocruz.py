import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

def adicionar_preto_branco(img):
    # Cria uma nova imagem com espaço extra
    largura, altura = img.size
    nova_img = Image.new("RGB", (largura + 2, altura + 1), "white")
    nova_img.paste(img, (0, 0))

    # Adiciona um pixel preto e um branco no canto inferior direito
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

def salvar_grafico(pixels, grid_size, num_colors):
    plt.figure(figsize=(8, 8))
    plt.imshow(pixels, interpolation='nearest')
    plt.grid(True, color='gray', linewidth=0.5)
    plt.xticks(range(pixels.shape[1]))
    plt.yticks(range(pixels.shape[0]))
    plt.gca().invert_yaxis()
    plt.title(f"Gráfico de Ponto Cruz ({grid_size}x{grid_size}, {num_colors} cores)")

    # Salvar como imagem
    nome_arquivo = f"grafico_ponto_cruz_{grid_size}x{grid_size}_{num_colors}cores.png"
    plt.savefig(nome_arquivo, dpi=300)
    print(f"Gráfico salvo como: {nome_arquivo}")

def process_image(image_path, grid_size, num_colors):
    img = Image.open(image_path).convert("RGB") 
   # img_small = img.resize((grid_size, grid_size), Image.Resampling.NEAREST)
    img_small = img.resize((grid_size, grid_size), resample=Image.Resampling.NEAREST)
    img_small = adicionar_preto_branco(img_small)
   # img_quantized = img_small.convert("P", palette=Image.Palette.ADAPTIVE, colors=num_colors)
    pixels = np.array(img_small)#(img_quantized)

    plt.figure(figsize=(8, 8))
    plt.imshow(pixels, interpolation='none', aspect='equal')
    plt.xticks(np.arange(-0.5, pixels.shape[1], 1), [])
    plt.yticks(np.arange(-0.5, pixels.shape[0], 1), []) 
    plt.gca().set_xticks(np.arange(-0.5, pixels.shape[1], 1), minor=True)
    plt.gca().set_yticks(np.arange(-0.5, pixels.shape[0], 1), minor=True)
    #plt.gca().grid(which='minor', color='gray', linewidth=0.5)
    plt.grid(True, color='gray', linewidth=0.5)
   # plt.xticks(range(pixels.shape[1],1))
   # plt.yticks(range(pixels.shape[0],1))
   # plt.gca().invert_yaxis()
    plt.title(f"Gráfico de Ponto Cruz ({grid_size}x{grid_size}, {num_colors} cores)")
    plt.show()
    salvar_grafico(pixels, grid_size, num_colors)
    gerar_legenda(img_small)#(img_quantized)

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        process_image(file_path, grid_slider.get(), color_slider.get())

# Interface
root = tk.Tk()
root.title("Gerador de Gráfico de Ponto Cruz")

tk.Label(root, text="Tamanho da Grade (pontos)").pack()
grid_slider = tk.Scale(root, from_=30, to=150, orient=tk.HORIZONTAL)
grid_slider.set(50)
grid_slider.pack()

tk.Label(root, text="Número de Cores").pack()
color_slider = tk.Scale(root, from_=2, to=50, orient=tk.HORIZONTAL)
color_slider.set(20)
color_slider.pack()

tk.Button(root, text="Selecionar Imagem", command=select_image).pack(pady=10)

root.mainloop()