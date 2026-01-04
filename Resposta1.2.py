import streamlit as st
import pandas as pd

st.set_page_config(page_title="Football Flow Analyzer", layout="centered")

st.title("💰 Football – Análise por Soma de Pagamentos")
st.caption("Histórico visível • Fluxo financeiro • Anti-erro")

# ---- SESSION ----
if "dados" not in st.session_state:
    st.session_state.dados = []

# ---- INPUT ----
st.subheader("➕ Inserir rodada")

resultado = st.radio(
    "Resultado da rodada:",
    ["🔴 BANK", "🔵 PLAYER", "🟡 EMPATE"],
    horizontal=True
)

valor = st.number_input(
    "Valor pago (odd ou retorno):",
    min_value=0.0,
    step=0.01
)

if st.button("Adicionar rodada"):
    if valor > 0:
        cor = resultado.split()[0]
        st.session_state.dados.append({
            "Resultado": cor,
            "Valor": valor
        })
    else:
        st.warning("Informe um valor válido.")

# ---- HISTÓRICO ----
st.subheader("📜 Histórico de Rodadas")

if st.session_state.dados:
    df = pd.DataFrame(st.session_state.dados)
    st.dataframe(df, use_container_width=True)

    st.write("Visual:")
    st.write(" ".join(df["Resultado"].tolist()))
else:
    st.info("Nenhuma rodada registrada ainda.")

# ---- SOMA ----
soma_red = sum(d["Valor"] for d in st.session_state.dados if d["Resultado"] == "🔴")
soma_blue = sum(d["Valor"] for d in st.session_state.dados if d["Resultado"] == "🔵")
total = soma_red + soma_blue

st.subheader("📊 Soma Financeira")
st.write(f"🔴 BANK pago: **{soma_red:.2f}**")
st.write(f"🔵 PLAYER pago: **{soma_blue:.2f}**")

# ---- ANÁLISE ----
st.subheader("🧠 Análise de Fluxo")

def analisar():
    if len(st.session_state.dados) < 10:
        return "🟡 OBSERVAR", "Histórico insuficiente", 0

    if st.session_state.dados[-1]["Resultado"] == "🟡":
        return "🔴 PROIBIDO", "Empate recente (reset financeiro)", 0

    if total == 0:
        return "🟡 OBSERVAR", "Sem dados financeiros", 0

    diff = abs(soma_red - soma_blue) / total * 100

    if diff < 20:
        return "🟡 OBSERVAR", "Fluxo equilibrado", int(diff)

    if soma_red > soma_blue:
        return "🟢 ENTRAR 🔵", "BANK está caro (tende a compensar)", int(diff)
    else:
        return "🟢 ENTRAR 🔴", "PLAYER está caro (tende a compensar)", int(diff)

status, motivo, conf = analisar()

# ---- OUTPUT ----
st.markdown(f"### Status: {status}")
st.write(f"💡 Motivo: {motivo}")

if conf > 0:
    st.progress(conf / 100)
    st.write(f"📈 Pressão financeira: {conf}%")

st.divider()
st.caption("Sistema financeiro conservador • Não força entradas • Preserva banca")
