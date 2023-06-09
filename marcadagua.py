import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import fitz
import os, sys

def selecionar_documento():
    arquivo_selecionado = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if arquivo_selecionado:
        return arquivo_selecionado
    else:
        return None


def adicionar_marca_dagua():
    documento = selecionar_documento()
    if documento:
        texto = texto_marca_dagua.get("1.0", tk.END)  # Obtém o texto do widget Text

        pdf = fitz.open(documento)

        for pagina in pdf:
            bbox = pagina.bound()  # Retângulo que envolve a página
            largura_pagina = bbox.width  # Largura da página
            altura_pagina = bbox.height  # Altura da página
            margem_inferior = 0.5 * 72  # 0,5cm em pontos (1 ponto = 1/72 polegadas)
            margem_superior = altura_pagina - margem_inferior  # 0,5cm da borda superior
            margem_direita = largura_pagina - 0.1 * 72  # 0,1cm da borda direita

            fonte = "Helvetica"

            posicao_horizontal = margem_direita  # Posição horizontal na margem direita
            posicao_vertical = margem_superior  # Posição vertical na margem superior

            pagina.insert_text(fitz.Point(posicao_horizontal, posicao_vertical), texto,
                               fontsize=15, rotate=90, fontname=fonte, fill=(0.698, 0.698, 0.698))

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        pdf.save(output_path)
        pdf.close()

        messagebox.showinfo("Concluído", "A marca d'água foi adicionada com sucesso!")
    else:
        messagebox.showerror("Erro", "Nenhum documento selecionado.")


# Cria a interface gráfica usando Tkinter
window = tk.Tk()
window.title("Inserir marca d'água em um PDF")
window.geometry("600x400")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 600
window_height = 400
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.resizable(False, False)

# Cabeçalho
cabecalho = tk.Label(window, text="Inserir marca d'água em um PDF", font=("Helvetica", 18, "bold"))
cabecalho.pack(pady=20)

texto_marca_dagua = tk.Text(window, height=10, width=50, font=("Helvetica", 15))
texto_marca_dagua.pack(pady=5)

# Carregar a imagem do carimbo
image_path = os.path.join(os.path.dirname(__file__), "stample.png")
if os.path.exists(image_path):
    image_carimbo = Image.open(image_path)
    # Redimensionar a imagem para um tamanho adequado
    image_carimbo = image_carimbo.resize((30, 30))
    # Converter a imagem para o formato suportado pelo Tkinter
    icon_carimbo = ImageTk.PhotoImage(image_carimbo)

    btn_adicionar_marca_dagua = tk.Button(window, text="Adicionar Marca d'Água", font=("Helvetica", 15), command=adicionar_marca_dagua,
                                          compound=tk.LEFT, image=icon_carimbo)
    btn_adicionar_marca_dagua.pack(pady=10)
else:
    messagebox.showerror("Erro", "O arquivo 'stample.png' não foi encontrado.")

window.mainloop()
