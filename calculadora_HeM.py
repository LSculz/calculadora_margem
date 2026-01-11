import tkinter as tk
from tkinter import messagebox

# --- Lógica Exata enviada para Mensalista (aplicada a ambos) ---

def calcular_irrf(salario_bruto):
    if salario_bruto <= 2259.20:
        return 0.0
    elif salario_bruto <= 2826.65:
        return salario_bruto * 0.075 - 169.44
    elif salario_bruto <= 3751.05:
        return salario_bruto * 0.15 - 381.44
    elif salario_bruto <= 4664.68:
        return salario_bruto * 0.225 - 662.77
    else:
        return salario_bruto * 0.275 - 896.00

def calcular_inss(salario_bruto):
    # Tabela INSS enviada
    if salario_bruto <= 1518.00:
        return salario_bruto * 0.075
    elif salario_bruto <= 2793.88:
        return (1412.00 * 0.075) + ((salario_bruto - 1412.00) * 0.09)
    elif salario_bruto <= 4190.83:
        return (1412.00 * 0.075) + ((2661.01 - 1412.00) * 0.09) + ((salario_bruto - 2661.01) * 0.12)
    elif salario_bruto <= 8157.41:
        return (1412.00 * 0.075) + ((2661.01 - 1412.00) * 0.09) + ((4000.03 - 2661.01) * 0.12) + ((salario_bruto - 4000.03) * 0.14)
    else:
        return 908.85 # Teto fixo enviado

def calcular_margem(salario_bruto, emprestimo_ativo=0.0):
    desconto_irrf = calcular_irrf(salario_bruto)
    desconto_inss = calcular_inss(salario_bruto)
    salario_liquido = salario_bruto - desconto_irrf - desconto_inss
    
    margem_total = salario_liquido * 0.35 
    margem_cartao = salario_liquido * 0.05 
    margem_emprestimo = margem_total 
    margem_disponivel = max(margem_emprestimo - emprestimo_ativo, 0)

    return salario_liquido, desconto_irrf, desconto_inss, margem_total, margem_emprestimo, margem_cartao, margem_disponivel

# --- Lógica de Interface ---

def selecionar_mensalista():
    global modo_atual
    modo_atual = "mensalista"
    frame_horista.pack_forget()
    frame_mensalista.pack(pady=10)
    btn_mensalista.config(relief="sunken", bg="#b3e5fc")
    btn_horista.config(relief="raised", bg="#f0f0f0")

def selecionar_horista():
    global modo_atual
    modo_atual = "horista"
    frame_mensalista.pack_forget()
    frame_horista.pack(pady=10)
    btn_horista.config(relief="sunken", bg="#b3e5fc")
    btn_mensalista.config(relief="raised", bg="#f0f0f0")

def executar_calculo():
    try:
        # Define o Salário Bruto conforme o modo
        if modo_atual == "mensalista":
            salario_bruto = float(entry_salario.get().replace(",", "."))
        else:
            # No Horista, a base é a soma exclusiva destes campos
            m_liq = float(entry_menor_liq.get().replace(",", ".") or 0)
            h_norm = float(entry_h_normais.get().replace(",", ".") or 0)
            h_diur = float(entry_h_diurnas.get().replace(",", ".") or 0)
            h_notu = float(entry_h_noturnas.get().replace(",", ".") or 0)
            salario_bruto = m_liq + h_norm + h_diur + h_notu

        # Cálculo de contratos ativos
        total_contratos = 0.0
        for e in entradas_contratos:
            if e.get():
                total_contratos += float(e.get().replace(",", "."))

        # Executa a lógica matemática enviada
        sal_liq, desc_irrf, desc_inss, m_total, m_emp, m_card, m_disp = calcular_margem(salario_bruto, total_contratos)

        # Exibição do Resultado
        resultado_text.set(
            f"--- RESUMO {modo_atual.upper()} ---\n"
            f"Salário Bruto: R$ {salario_bruto:.2f}\n"
            f"Salário Líquido: R$ {sal_liq:.2f}\n"
            f"Desconto INSS: R$ {desc_inss:.2f}\n"
            f"Desconto IRRF: R$ {desc_irrf:.2f}\n\n"
            f"Margem Total (35%): R$ {m_total:.2f}\n"
            f"Margem Cartão (5%): R$ {m_card:.2f}\n"
            f"Empréstimos Ativos: R$ {total_contratos:.2f}\n"
            f"MARGEM DISPONÍVEL: R$ {m_disp:.2f}"
        )

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

def criar_campos_contratos():
    for widget in frame_lista_contratos.winfo_children():
        widget.destroy()
    entradas_contratos.clear()
    try:
        qtd = int(entry_qtd.get())
        if 0 <= qtd <= 9:
            for i in range(qtd):
                tk.Label(frame_lista_contratos, text=f"Contrato {i+1} (R$):").pack()
                e = tk.Entry(frame_lista_contratos)
                e.pack()
                entradas_contratos.append(e)
        else:
            messagebox.showerror("Erro", "Máximo de 9 contratos.")
    except ValueError:
        messagebox.showerror("Erro", "Insira um número inteiro para a quantidade.")

# --- Interface Principal ---

root = tk.Tk()
root.title("Calculadora de Margem Consignável")
root.geometry("450x800")

modo_atual = "mensalista"

# Botões de Perfil
tk.Label(root, text="Selecione o perfil do cliente:", font=("Arial", 9, "bold")).pack(pady=5)
frame_botoes = tk.Frame(root)
frame_botoes.pack()
btn_mensalista = tk.Button(frame_botoes, text="Mensalista", width=15, command=selecionar_mensalista)
btn_mensalista.pack(side="left", padx=5)
btn_horista = tk.Button(frame_botoes, text="Horista", width=15, command=selecionar_horista)
btn_horista.pack(side="left", padx=5)

# Container Mensalista
frame_mensalista = tk.Frame(root)
tk.Label(frame_mensalista, text="Salário Base / Bruto (R$):").pack()
entry_salario = tk.Entry(frame_mensalista)
entry_salario.pack()

# Container Horista (Apenas campos de horas e menor líquido)
frame_horista = tk.Frame(root)
tk.Label(frame_horista, text="Menor Líquido Holerite (R$):").pack()
entry_menor_liq = tk.Entry(frame_horista)
entry_menor_liq.pack()
tk.Label(frame_horista, text="Horas Normais (R$):").pack()
entry_h_normais = tk.Entry(frame_horista)
entry_h_normais.pack()
tk.Label(frame_horista, text="Horas Diurnas (R$):").pack()
entry_h_diurnas = tk.Entry(frame_horista)
entry_h_diurnas.pack()
tk.Label(frame_horista, text="Horas Noturnas (R$):").pack()
entry_h_noturnas = tk.Entry(frame_horista)
entry_h_noturnas.pack()

# Contratos (Comum)
tk.Label(root, text="\nQuantidade de contratos ativos (0-9):").pack()
entry_qtd = tk.Entry(root)
entry_qtd.pack()
tk.Button(root, text="Gerar campos de contratos", command=criar_campos_contratos).pack(pady=5)
frame_lista_contratos = tk.Frame(root)
frame_lista_contratos.pack()
entradas_contratos = []

# Resultado Final
tk.Button(root, text="Calcular Margem", bg="#1b5e20", fg="white", font=("Arial", 10, "bold"), command=executar_calculo).pack(pady=20)
resultado_text = tk.StringVar()
tk.Label(root, textvariable=resultado_text, justify="left", fg="blue", font=("Consolas", 10), bg="#f9f9f9", padx=10, pady=10).pack(pady=10)

selecionar_mensalista()
root.mainloop()