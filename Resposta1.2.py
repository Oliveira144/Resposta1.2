import streamlit as st
from collections import Counter

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================
st.set_page_config(page_title="🧠 Football Studio IA", layout="centered")

st.title("🎴 Football Studio – IA Avançada")
st.caption("18 padrões reais | Probabilidade | Manipulação | Sem forçar entrada")

# =============================
# CONFIG
# =============================
MAX_HIST = 60
MIN_READ = 5

# =============================
# ESTADO
# =============================
if "hist" not in st.session_state:
    st.session_state.hist = []

# =============================
# INPUT DE RESULTADOS
# =============================
st.subheader("➕ Inserir Resultado")
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🔴 Player"):
        st.session_state.hist.append("🔴")
with c2:
    if st.button("🔵 Banker"):
        st.session_state.hist.append("🔵")
with c3:
    if st.button("🟡 Empate"):
        st.session_state.hist.append("🟡")
with c4:
    if st.button("❌ Apagar"):
        if st.session_state.hist:
            st.session_state.hist.pop()

st.session_state.hist = st.session_state.hist[-MAX_HIST:]

# =============================
# HISTÓRICO VISUAL
# =============================
st.subheader("📜 Histórico (mais recente → antigo)")
linhas = [st.session_state.hist[i:i+9] for i in range(0, len(st.session_state.hist), 9)]
for linha in linhas[::-1]:
    st.write(" ".join(linha[::-1]))

# =============================
# FUNÇÕES AUXILIARES
# =============================
def ult(n):
    return st.session_state.hist[-n:] if len(st.session_state.hist) >= n else []

def alternado(seq):
    return len(seq) >= 4 and all(seq[i] != seq[i+1] for i in range(len(seq)-1))

def repeticao(n):
    return len(st.session_state.hist) >= n and len(set(st.session_state.hist[-n:])) == 1

def contagem():
    return Counter(st.session_state.hist[-10:])

# =============================
# MOTOR DOS 18 PADRÕES
# =============================
st.subheader("🧠 Leitura Avançada")

sugestao = "❌ NÃO ENTRAR"
padrao = "Nenhum padrão válido"
prob = 0
manip = 9

h = st.session_state.hist

if len(h) >= MIN_READ:
    u4 = ult(4)
    u5 = ult(5)
    u6 = ult(6)
    u7 = ult(7)

    # 1 Alternado Simples
    if alternado(u4):
        sugestao = "➡️ OPOSTO do último"
        padrao = "Alternado Simples"
        prob = 68
        manip = 3

    # 2 Duplo (2x1)
    elif len(u6) == 6 and u6[-4] == u6[-3] and u6[-2] != u6[-1]:
        sugestao = f"➡️ {u6[-1]}"
        padrao = "Duplo (2x1)"
        prob = 65
        manip = 4

    # 3 Triplo
    elif repeticao(3):
        sugestao = f"➡️ {h[-1]}"
        padrao = "Triplo"
        prob = 62
        manip = 4

    # 4 Escadinha
    elif len(u6) == 6 and u6[0]==u6[1] and u6[2]==u6[3] and u6[4]!=u6[3]:
        sugestao = "⚠️ Aguardar"
        padrao = "Escadinha"
        prob = 50
        manip = 6

    # 5 Empate Âncora
    elif "🟡" in u4:
        sugestao = "➡️ Seguir cor anterior ao empate"
        padrao = "Empate Âncora"
        prob = 64
        manip = 4

    # 6 Empate de Corte
    elif h[-1] == "🟡" and len(set(h[-4:-1])) == 1:
        sugestao = "❌ NÃO ENTRAR"
        padrao = "Empate de Corte"
        prob = 0
        manip = 8

    # 7 Empate Isolado
    elif h[-1] == "🟡":
        sugestao = "⚠️ Ignorar empate"
        padrao = "Empate Isolado"
        prob = 45
        manip = 6

    # 8 Repetição Curta
    elif repeticao(2):
        sugestao = f"➡️ Manter {h[-1]}"
        padrao = "Repetição Curta"
        prob = 63
        manip = 4

    # 9 Repetição Longa
    elif repeticao(5):
        sugestao = "⚠️ Quebra próxima"
        padrao = "Repetição Longa"
        prob = 40
        manip = 7

    # 10 Falsa Quebra
    elif len(h) >= 3 and h[-3] == h[-1] and h[-2] != h[-1]:
        sugestao = f"➡️ Voltar {h[-1]}"
        padrao = "Falsa Quebra"
        prob = 66
        manip = 5

    # 11 Falso Alternado
    elif alternado(h[-5:-1]) and h[-1] == h[-2]:
        sugestao = f"➡️ {h[-1]}"
        padrao = "Falso Alternado"
        prob = 67
        manip = 5

    # 12 Espelhado
    elif len(u6) == 6 and u6[:3] == u6[3:][::-1]:
        sugestao = "❌ NÃO ENTRAR"
        padrao = "Espelhado"
        prob = 0
        manip = 8

    # 13 Atraso de Quebra
    elif repeticao(2) and h[-3] != h[-1]:
        sugestao = "⚠️ Aguardar confirmação"
        padrao = "Atraso de Quebra"
        prob = 48
        manip = 6

    # 14 Saturação
    elif contagem().most_common(1)[0][1] >= 7:
        sugestao = "❌ NÃO ENTRAR"
        padrao = "Saturação de Mercado"
        prob = 0
        manip = 9

    # 15 Surf
    elif u7.count("🔴") == u7.count("🔵"):
        sugestao = "➡️ Seguir onda"
        padrao = "Surf"
        prob = 61
        manip = 5

    # 16 Ciclo
    elif len(set(u6)) == 2:
        sugestao = "⚠️ Ciclo encerrando"
        padrao = "Ciclo"
        prob = 52
        manip = 6

    # 17 Colapso de Probabilidade
    else:
        u3 = ult(3)
        if "🟡" in u3:
            sugestao = "❌ NÃO ENTRAR"
            padrao = "Colapso de Probabilidade"
            prob = 0
            manip = 9
        else:
            # 18 Fantasma
            sugestao = "❌ NÃO ENTRAR"
            padrao = "Padrão Fantasma"
            prob = 0
            manip = 9

# =============================
# RESULTADO FINAL
# =============================
st.markdown("---")
st.subheader("📊 Resultado da IA")

st.markdown(f"""
### 🎯 Sugestão: **{sugestao}**
- 🧠 Padrão detectado: **{padrao}**
- 📊 Probabilidade estimada: **{prob}%**
- 🤖 Nível de manipulação: **{manip}/9**
""")

if manip >= 7:
    st.error("🚫 Entrada bloqueada – manipulação alta")
elif prob >= 60:
    st.success("✅ Entrada possível com gestão")
else:
    st.warning("⚠️ Zona neutra – apenas observar")

# =============================
# REGRA DE OURO
# =============================
st.markdown("""
---
### 🧠 REGRA ABSOLUTA
> **Se o padrão precisa ser forçado, ele já acabou.**
""")
