# 📊 Calculadora de Margem Consignável - INSS 2026

Esta é uma aplicação desktop desenvolvida em **Python** utilizando a biblioteca **Tkinter**. O objetivo é facilitar o cálculo do salário líquido e a verificação automática da margem consignável disponível para empréstimos e cartões, utilizando as tabelas fiscais atualizadas de **2026**.

## 🚀 Funcionalidades

- **Cálculo Automático de INSS (2026):** Aplica as alíquotas progressivas sobre o salário bruto.
- **Cálculo de IRRF (2026):** Calcula o Imposto de Renda Retido na Fonte após a dedução do INSS.
- **Margem Consignável (35%):** Calcula o valor máximo permitido para parcelas de empréstimos.
- **Margem de Cartão (5%):** Calcula a margem específica para RMC/Cartão Consignado.
- **Gestão de Contratos:** Permite inserir empréstimos já ativos para calcular a margem livre real.

## 🛠️ Regras de Cálculo Aplicadas

O sistema segue rigorosamente a ordem de descontos obrigatórios para chegar à base de cálculo das margens:

1. **Salário Base (Bruto)** $\rightarrow$ Entrada do usuário.
2. **Desconto INSS** $\rightarrow$ Aplicado conforme faixas progressivas (Teto: R$ 8.475,55).
3. **Base IRRF** $\rightarrow$ `Salário Bruto - Desconto INSS`.
4. **Salário Líquido** $\rightarrow$ `Base IRRF - Desconto IRRF`.
5. **Margens** $\rightarrow$ Calculadas sobre o Salário Líquido final.

## 📅 Tabelas de Referência (Janeiro/2026)

### INSS
| Salário de Contribuição | Alíquota | Parcela a Deduzir |
| :--- | :--- | :--- |
| Até R$ 1.621,00 | 7,5% | R$ 0,00 |
| De R$ 1.621,01 até R$ 2.902,84 | 9,0% | R$ 23,66 |
| De R$ 2.902,85 até R$ 4.354,27 | 12,0% | R$ 110,75 |
| De R$ 4.354,28 até R$ 8.475,55 | 14,0% | R$ 197,83 |

### IRRF
| Base de Cálculo | Alíquota | Parcela a Deduzir |
| :--- | :--- | :--- |
| Até R$ 2.259,20 | Isento | R$ 0,00 |
| De R$ 2.259,21 até R$ 2.826,65 | 7,5% | R$ 169,44 |
| De R$ 2.826,66 até R$ 3.751,05 | 15,0% | R$ 381,44 |
| De R$ 3.751,06 até R$ 4.664,68 | 22,5% | R$ 662,77 |
| Acima de R$ 4.664,68 | 27,5% | R$ 896,00 |

## 💻 Como usar

1.  **Pré-requisitos:** Ter o Python 3.x instalado.
2.  **Instalação:** Não requer bibliotecas externas (usa `tkinter` nativo).
3.  **Execução:**
    ```bash
    python seu_arquivo.py
    ```
4.  **Uso:** - Insira o Salário Bruto.
    - Informe a quantidade de contratos de empréstimo que já possui.
    - Clique em "Calcular" para obter o resumo detalhado.

---
> **Nota:** Este projeto tem fins informativos e de auxílio ao cálculo. Os valores podem variar conforme regras específicas de cada convênio ou órgão pagador.
