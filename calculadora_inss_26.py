import tkinter as tk
from tkinter import messagebox


def calcular_inss(salario_base):
    """Calcula o INSS 2026 com base no Salário Base (Bruto)"""
    teto_inss = 8475.55
    # O cálculo nunca ultrapassa o teto
    base = min(salario_base, teto_inss)

    if base <= 1621.00:
        return base * 0.075
    elif base <= 2902.84:
        return (base * 0.09) - 23.66
    elif base <= 4354.27:
        return (base * 0.12) - 110.75
    else:
        return (base * 0.14) - 197.83

def calcular_irrf(salario_base_irrf):
    """Calcula o IRRF 2026 sobre a base (Salário Base - INSS)"""
    if salario_base_irrf <= 2259.20:
        return 0.0
    elif salario_base_irrf <= 2826.65:
        return (salario_base_irrf * 0.075) - 169.44
    elif salario_base_irrf <= 3751.05:
        return (salario_base_irrf * 0.15) - 381.44
    elif salario_base_irrf <= 4664.68:
        return (salario_base_irrf * 0.225) - 662.77
    else:
        return (salario_base_irrf * 0.275) - 896.00

def executar_calculo():
    try:
        # 1. Entrada única: Salário Base
        salario_base = float(entry_salario.get().replace(",", "."))
        
        # 2. Cálculos automáticos em cadeia
        valor_inss = calcular_inss(salario_base)
        base_irrf = salario_base - valor_inss # O IRRF incide após o INSS
        valor_irrf = calcular_irrf(base_irrf)
        
        salario_liquido = salario_base - valor_inss - valor_irrf
        
        # 3. Cálculo das margens (35% empréstimo e 5% cartão)
        margem_consignavel = salario_liquido * 0.35
        margem_cartao = salario_liquido * 0.05
        
        # Se houver empréstimos ativos informados, subtraímos da margem de 35%
        total_emprestimos = 0.0
        for e in entradas_contratos:
            if e.get():
                total_emprestimos += float(e.get().replace(",", "."))
        
        margem_disponivel = max(margem_consignavel - total_emprestimos, 0)

        # 4. Exibição dos resultados
        resultado_text.set(
            f"--- RESUMO DE FOLHA (2026) ---\n"
            f"Salário Base: R$ {salario_base:.2f}\n"
            f"Desconto INSS: R$ {valor_inss:.2f}\n"
            f"Desconto IRRF: R$ {valor_irrf:.2f}\n"
            f"Salário Líquido: R$ {salario_liquido:.2f}\n\n"
            f"--- MARGENS DISPONÍVEIS ---\n"
            f"Margem Empréstimo (35%): R$ {margem_consignavel:.2f}\n"
            f"Margem Cartão (5%): R$ {margem_cartao:.2f}\n"
            f"Utilizado em Contratos: R$ {total_emprestimos:.2f}\n"
            f"DISPONÍVEL REAL: R$ {margem_disponivel:.2f}"
        )

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor válido para o Salário Base.")

def criar_campos_contratos():
    for e in entradas_contratos:
        e.destroy()
    entradas_contratos.clear()

    try:
        qtd = int(entry_qtd.get())
        if qtd < 0 or qtd > 9:
            messagebox.showerror("Erro", "Número de contratos deve ser entre 0 e 9.")
            return
        for i in range(qtd):
            tk.Label(frame_contratos, text=f"Contrato {i+1} (R$):").pack()
            e = tk.Entry(frame_contratos)
            e.pack()
            entradas_contratos.append(e)
    except ValueError:
        messagebox.showerror("Erro", "Digite um número inteiro para a quantidade de contratos.")

# ----- Interface -----
root = tk.Tk()
root.title("Calculadora de Margem Consignável")
root.geometry("400x600")

tk.Label(root, text="Salário base (R$):").pack()
entry_salario = tk.Entry(root)
entry_salario.pack()

tk.Label(root, text="Quantidade de contratos ativos (0-9):").pack()
entry_qtd = tk.Entry(root)
entry_qtd.pack()

tk.Button(root, text="Gerar campos", command=criar_campos_contratos).pack()

frame_contratos = tk.Frame(root)
frame_contratos.pack()

entradas_contratos = []

tk.Button(root, text="Calcular Margem", command=executar_calculo).pack(pady=10)

resultado_text = tk.StringVar()
tk.Label(root, textvariable=resultado_text, justify="left", fg="blue").pack(pady=10)

root.mainloop()
