import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import os
import webcolors
def closest_colour(requested_colour):
    min_colours = {}
    for name in webcolors.names("css3"):
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def adicionar_preto_branco(img):
    largura, altura = img.size
    nova_img = Image.new("RGB", (largura + 2, altura + 1), "white")
    nova_img.paste(img, (0, 0))
    draw = ImageDraw.Draw(nova_img)
    draw.point((largura, altura), fill=(0, 0, 0))
    draw.point((largura + 1, altura), fill=(255, 255, 255))
    return nova_img

def reconstruir_imagem_rgb(img_quantized):
    palette = img_quantized.getpalette()
    pixels = np.array(img_quantized)
    rgb_array = np.zeros((pixels.shape[0], pixels.shape[1], 3), dtype=np.uint8)
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            idx = pixels[i, j]
            rgb_array[i, j] = palette[idx*3:idx*3+3]
    return rgb_array

def gerar_legenda(img_quantized):
    palette = img_quantized.getpalette()
    used_colors = sorted(set(img_quantized.getdata()))
    legenda = {}
    for i, color_index in enumerate(used_colors):
        r = palette[color_index * 3]
        g = palette[color_index * 3 + 1]
        b = palette[color_index * 3 + 2]
        legenda[f"Cor {i+1}"] = (r, g, b)
    return legenda

def salvar_imagem_temporaria(rgb_pixels, nome_arquivo="grafico_ponto_cruz.png"):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(rgb_pixels, interpolation='nearest', aspect='equal')
    ax.set_xticks(np.arange(-0.5, rgb_pixels.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rgb_pixels.shape[0], 1), minor=True)
    ax.grid(True, which='minor', color='gray', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(nome_arquivo, dpi=300)
    plt.close(fig)
    return nome_arquivo

def exibir_grafico(rgb_pixels):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(rgb_pixels, interpolation='nearest', aspect='equal')
    ax.set_xticks(np.arange(-0.5, rgb_pixels.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rgb_pixels.shape[0], 1), minor=True)
    ax.grid(True, which='minor', color='gray', linewidth=0.5)
    plt.tight_layout()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    plt.close(fig)
    return buf

def rgb_para_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*rgb)

def salvar_imagem_com_legenda(rgb_pixels, legenda, nome_arquivo="grafico_com_legenda.png"):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(rgb_pixels, interpolation='nearest', aspect='equal')
    ax.set_xticks(np.arange(-0.5, rgb_pixels.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rgb_pixels.shape[0], 1), minor=True)
    ax.grid(True, which='minor', color='gray', linewidth=0.5)

    # Monta texto da legenda usando closest_colour()
    legenda_texto = "\n".join(
        [f"{cor}: {closest_colour(rgb)} — RGB{rgb}" for cor, rgb in legenda.items()]
    )

    # Adiciona legenda ao lado direito
    fig.text(1.05, 0.5, legenda_texto, fontsize=10, va='center', ha='left', wrap=True)

    plt.tight_layout()
    fig.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return nome_arquivo

# Interface Streamlit
st.title("🧵 Gerador de Gráfico de Ponto Cruz")

uploaded_file = st.file_uploader("Selecione uma imagem", type=["jpg", "jpeg", "png"])
grid_x = st.slider("Quantidade de pontos no eixo X", 30, 150, 50)
grid_y = st.slider("Quantidade de pontos no eixo Y", 30, 150, 50)
num_colors = st.slider("Número de cores", 2, 50, 20)

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    img_small = img.resize((grid_x, grid_y), resample=Image.Resampling.NEAREST)
    img_small = adicionar_preto_branco(img_small)
    img_quantized = img_small.convert("P", palette=Image.Palette.ADAPTIVE, colors=num_colors)
    rgb_pixels = reconstruir_imagem_rgb(img_quantized)

    st.subheader("🖼️ Gráfico Gerado")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(rgb_pixels, interpolation='nearest', aspect='equal')
    ax.set_xticks(np.arange(-0.5, rgb_pixels.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rgb_pixels.shape[0], 1), minor=True)
    ax.grid(True, which='minor', color='gray', linewidth=0.5)
    st.pyplot(fig)


    st.subheader("📥 Baixar Gráfico como Imagem")
   # imagem_download=exibir_grafico(rgb_pixels)
    legenda = gerar_legenda(img_quantized)
    imagem_download = exibir_grafico(rgb_pixels)

    st.download_button(
    label="📥 Baixar Gráfico como Imagem",
    data=imagem_download.getvalue(),
    file_name="grafico_ponto_cruz.png",
    mime="image/png"
)
   
    caminho_imagem = salvar_imagem_com_legenda(rgb_pixels, legenda)
    with open(caminho_imagem, "rb") as file:
        st.download_button(
        label="📥 Baixar Gráfico com Legenda",
        data=file.read(),
        file_name="grafico_com_legenda.png",
        mime="image/png"
    )


    st.subheader("🎨 Legenda de Cores")
    legenda = gerar_legenda(img_quantized)
    for cor, rgb in legenda.items():
        nome = closest_colour(rgb)
        hex_cor = rgb_para_hex(rgb)
        st.markdown(f"**{cor}**: {nome.title()} — RGB{rgb}")
        st.color_picker(label="", value=hex_cor, key=cor)
        