from scipy.stats import chi2_contingency, norm
import streamlit as st
from scipy.stats import chisquare
from scipy.stats import chi2_contingency
import numpy as np
import pandas as pd

tab1, tab2 = st.tabs(['Qui-quadrado 1', 'Qui-quadrado 2'])
with tab1:
    # Configuração da página do Streamlit
    st.title("Teste Qui-Quadrado para Proporções")
    st.write("""
    Este aplicativo calcula o teste qui-quadrado para verificar se há preferência por uma posição específica com base em suas observações. Além disso, ele identifica quais posições se destacam significativamente como preferidas.
    """)

    # Entrada dos dados
    st.header("Insira os dados")
    st.write("Digite as frequências observadas para cada posição abaixo:")

    # Caixas de entrada para as frequências observadas
    positions = st.text_input(
        "Exemplo: 15, 0, 2, 0, 1 (valores separados por vírgula)").strip()

    # Validação de entrada
    if positions:
        try:
            # Converte as entradas em uma lista de números
            observed = list(map(int, positions.split(",")))
            total_choices = sum(observed)
            num_positions = len(observed)

            # Frequências esperadas sob a hipótese nula (distribuição uniforme)
            expected = [total_choices / num_positions] * num_positions

            # Exibe os dados processados
            st.write(f"Frequências observadas: {observed}")
            st.write(f"Frequências esperadas (uniformes): {expected}")

            # Cálculo do teste qui-quadrado
            chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)

            # Resultados do teste
            st.subheader("Resultados do Teste Qui-Quadrado")
            st.write(f"Estatística qui-quadrado (χ²): {chi2_stat:.4f}")
            st.write(f"Valor-p: {p_value:.4e}")

            # Interpretação do valor-p
            alpha = 0.05  # Nível de significância
            if p_value < alpha:
                st.write(
                    "🚨 **Conclusão**: Existe evidência estatística para rejeitar a hipótese nula. "
                    "As escolhas não foram feitas de forma uniforme, indicando preferência por alguma posição."
                )
            else:
                st.write(
                    "✅ **Conclusão**: Não há evidência estatística para rejeitar a hipótese nula. "
                    "As escolhas podem ter sido feitas de forma uniforme."
                )

            # Cálculo dos resíduos padronizados
            st.subheader("Resíduos Padronizados por Posição")
            residuals = [(obs - exp) / np.sqrt(exp)
                         for obs, exp in zip(observed, expected)]
            # Valor crítico para 5% de significância (95% de confiança)
            critical_value = 1.96

            # Exibindo os resíduos e interpretando
            preferred_positions = []
            for i, res in enumerate(residuals):
                st.write(f"Posição {i + 1}: Resíduo padronizado = {res:.4f}")
                if res > critical_value:
                    st.write(
                        f"👉 **A posição {i + 1} é significativamente mais escolhida do que o esperado!**")
                    preferred_positions.append(i + 1)
                elif res < -critical_value:
                    st.write(
                        f"👉 **A posição {i + 1} é significativamente menos escolhida do que o esperado!**")

            # Conclusão geral sobre a posição preferida
            st.subheader("Conclusão sobre a Posição Preferida")
            if preferred_positions:
                st.write(f"📌 As seguintes posições foram identificadas como **preferidas**: {
                    ', '.join(map(str, preferred_positions))}")
            else:
                st.write(
                    "Nenhuma posição foi identificada como significativamente preferida ou menos preferida.")

        except ValueError:
            st.error("Por favor, insira valores inteiros separados por vírgula.")
    else:
        st.info("Aguardando entrada de dados...")

    # Mensagem final
    st.write("---")
    st.write("Desenvolvido com ❤️ usando Python e Streamlit.")
with tab2:
    import streamlit as st

# Configuração do título
st.title("Comparação de Proporções entre Posições com Análise Post-hoc")
st.write("""
Este aplicativo calcula o teste qui-quadrado para verificar se há diferença nas proporções de sucessos (premiações) entre posições independentes. 
Além disso, realiza uma análise post-hoc para identificar quais posições apresentam proporções significativamente diferentes.
""")

# Entrada dos dados
st.header("Insira os dados")
st.write("Digite os sucessos e os totais para cada posição:")

# Entrada de dados pelo usuário
data_input = st.text_area(
    "Exemplo (formato: sucessos, totais por linha):\n15,15\n58,59\n46,49\n30,31", height=150)

if data_input:
    try:
        # Processando os dados de entrada
        data_lines = data_input.strip().split("\n")
        data = [list(map(int, line.split(","))) for line in data_lines]

        # Preparando os dados
        df = pd.DataFrame(data, columns=["Sucessos", "Totais"])
        df["Insucessos"] = df["Totais"] - df["Sucessos"]

        # Exibindo a tabela de entrada
        st.subheader("Dados Inseridos:")
        st.write(df)

        # Tabela de contingência
        contingency_table = df[["Sucessos", "Insucessos"]].values

        # Cálculo do teste qui-quadrado
        chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

        # Resultados do teste
        st.subheader("Resultados do Teste Qui-Quadrado")
        st.write(f"Estatística qui-quadrado (χ²): {chi2_stat:.4f}")
        st.write(f"Graus de liberdade: {dof}")
        st.write(f"Valor-p: {p_value:.4e}")

        # Interpretação dos resultados
        alpha = 0.05  # Nível de significância
        if p_value < alpha:
            st.write(
                "🚨 **Conclusão**: Existe evidência estatística para rejeitar a hipótese nula. "
                "As proporções de sucessos (premiações) não são iguais entre as posições."
            )
        else:
            st.write(
                "✅ **Conclusão**: Não há evidência estatística para rejeitar a hipótese nula. "
                "As proporções de sucessos (premiações) podem ser iguais entre as posições."
            )

        # Exibindo os valores esperados
        st.subheader("Frequências Esperadas:")
        expected_df = pd.DataFrame(
            expected, columns=["Sucessos Esperados", "Insucessos Esperados"])
        st.write(expected_df)

        # Análise Post-hoc: Comparações por pares usando teste z para proporções
        st.subheader("Análise Post-hoc: Comparações por Pares")

        # Obtenção das proporções observadas
        proportions = df["Sucessos"] / df["Totais"]
        comparisons = []
        n_positions = len(df)

        # Comparação entre todos os pares de posições
        for i in range(n_positions):
            for j in range(i + 1, n_positions):
                # Sucessos e totais das duas posições
                succ_i, total_i = df.loc[i, "Sucessos"], df.loc[i, "Totais"]
                succ_j, total_j = df.loc[j, "Sucessos"], df.loc[j, "Totais"]

                # Proporções
                p_i, p_j = proportions[i], proportions[j]

                # Proporção combinada (pooling)
                pooled_p = (succ_i + succ_j) / (total_i + total_j)

                # Estatística z
                z = (p_i - p_j) / np.sqrt(pooled_p *
                                          (1 - pooled_p) * (1 / total_i + 1 / total_j))

                # Valor-p bilateral
                p_val = 2 * (1 - norm.cdf(abs(z)))

                # Armazenar resultado
                comparisons.append({
                    "Posição 1": i + 1,
                    "Posição 2": j + 1,
                    "Proporção 1": p_i,
                    "Proporção 2": p_j,
                    "Estatística z": z,
                    "Valor-p": p_val
                })

        # Correção de Bonferroni para múltiplas comparações
        comparisons_df = pd.DataFrame(comparisons)
        comparisons_df["Valor-p Ajustado (Bonferroni)"] = comparisons_df["Valor-p"] * len(
            comparisons_df)
        comparisons_df["Significativo (Ajustado)"] = comparisons_df["Valor-p Ajustado (Bonferroni)"] < alpha

        # Exibindo os resultados das comparações
        st.write(comparisons_df)

        # Conclusão sobre as posições mais premiadas
        st.subheader("Conclusão sobre as Posições mais Premiadas")
        sig_differences = comparisons_df[comparisons_df["Significativo (Ajustado)"]]
        if not sig_differences.empty:
            st.write(
                "As seguintes comparações apresentaram diferenças significativas nas proporções de premiação:")
            for _, row in sig_differences.iterrows():
                st.write(f"- **Posição {int(row['Posição 1'])}** (Proporção: {row['Proporção 1']:.4f}) é significativamente diferente de "
                         f"**Posição {int(row['Posição 2'])}** (Proporção: {row['Proporção 2']:.4f}).")
        else:
            st.write(
                "Nenhuma diferença significativa foi encontrada nas proporções de premiação após o ajuste de Bonferroni.")

    except Exception as e:
        st.error("Erro ao processar os dados. Verifique o formato da entrada.")
else:
    st.info("Aguardando entrada de dados...")

# Mensagem final
st.write("---")
st.write("Desenvolvido com ❤️ usando Python e Streamlit.")
