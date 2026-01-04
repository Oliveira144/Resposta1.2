import streamlit as st

st.set_page_config(page_title="Football Flow Analyzer", layout="centered")

st.title("💰 Football – Análise por Soma de Pagamentos")
st.caption("Leitura financeira • Fluxo de pagamento • Anti-padrão")

# ---- SESSION ----
if "dados" not in st.session_state:
    st.session_state.dados = []

# ---- INPUT ----
st.subheader("Inserir rodada")

c1, c2, c3 = st.columns(3)
resultado = None

if c1.button("🔴 BANK"):
    resultado = "🔴"
if c2.button("🔵 PLAYER"):
    resultado = "🔵"
if c3.button("🟡 EMPATE"):
    resultado = "🟡"

valor = st.number_input("Valor pago nesta rodada (ex: 1.95)", min_value=0.0, step=0.01)

if resultado and valor > 0:
    st.session_state.dados.append((resultado, valor))
    st.session_state.dados = st.session_state.dados[-40:]

# ---- HISTÓRICO ----
st.subheader("📜 Histórico de Pagamentos")
for r, v in st.session_state.dados[::-1]:
    st.write(f"{r} → {v}")

# ---- SOMA ----
soma_red = sum(v for r, v in st.session_state.dados if r == "🔴")
soma_blue = sum(v for r, v in st.session_state.dados if r == "🔵")

total = soma_red + soma_blue

st.subheader("📊 Soma Financeira")
st.write(f"🔴 Total pago BANK: **{soma_red:.2f}**")
st.write(f"🔵 Total pago PLAYER: **{soma_blue:.2f}**")

# ---- ANÁLISE ----
st.subheader("🧠 Análise de Fluxo")

def analisar_fluxo(hist):
    if len(hist) < 10:
        return "🟡 OBSERVAR", "Histórico financeiro insuficiente", 0

    if hist[-1][0] == "🟡":
        return "🔴 PROIBIDO", "Empate recente (reset financeiro)", 0

    if total == 0:
        return "🟡 OBSERVAR", "Sem dados financeiros", 0

    diff = abs(soma_red - soma_blue) / total * 100

    if diff < 20:
        return "🟡 OBSERVAR", "Pagamento equilibrado (sem pressão)", int(diff)

    if soma_red > soma_blue:
        return "🟢 ENTRAR 🔵", "BANK caro (cassino tende a compensar)", int(diff)

    else:
        return "🟢 ENTRAR 🔴", "PLAYER caro (cassino tende a compensar)", int(diff)

status, motivo, conf = analisar_fluxo(st.session_state.dados)

# ---- OUTPUT ----
st.markdown(f"### Status: {status}")
st.write(f"💡 Motivo: {motivo}")

if conf > 0:
    st.progress(conf / 100)
    st.write(f"📈 Pressão financeira: {conf}%")

st.divider()
st.caption("⚠️ Sistema baseado em fluxo de pagamento. Não força entradas. Proteção máxima de banca.")
