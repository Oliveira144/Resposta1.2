import streamlit as st

st.title("🏆 Football Studio Elite")

if 'history' not in st.session_state:
    st.session_state.history = []
    st.session_state.bankroll = 200

bankroll = st.number_input("💰 Bankroll", value=st.session_state.bankroll)

# BOTÕES
col1, col2, col3 = st.columns([1,1,1])
if col1.button("🔴 **BANK**", use_container_width=True):
    st.session_state.history.append('BANK')
    st.rerun()
if col2.button("🔵 **PLAYER**", use_container_width=True):
    st.session_state.history.append('PLAYER')
    st.rerun()
if col3.button("🟡 **TIE**", use_container_width=True):
    st.session_state.history.append('TIE')
    st.rerun()

def analyze(history):
    if len(history) < 2:
        return {'streak': 0, 'choppy': 0, 'cockroach': False, 'suggestion': 'WAIT'}
    
    h = history[-12:]
    last = h[-1]
    
    # STREAK
    streak = 1
    for i in range(1, len(h)):
        if len(h) > i and h[-i-1] == last:
            streak += 1
        else:
            break
    
    # CHOPPY
    choppy = 0
    for i in range(1, min(8, len(h))):
        if h[-i] != h[-i-1]:
            choppy += 1
    
    # COCKROACH
    cockroach = len(h) >= 3 and h[-3:] in [['BANK', 'BANK', 'PLAYER'], ['PLAYER', 'PLAYER', 'BANK']]
    
    # SUGESTÃO
    bet_size = bankroll * 0.01
    if streak >= 6:
        opp = 'PLAYER' if last == 'BANK' else 'BANK'
        return {'streak': streak, 'suggestion': f"{opp} R${int(bet_size*2)}", 'dragon': True}
    elif streak >= 4:
        opp = 'PLAYER' if last == 'BANK' else 'BANK'
        return {'streak': streak, 'suggestion': f"{opp} R${int(bet_size*1.5)}"}
    elif cockroach:
        return {'cockroach': True, 'suggestion': f"BANK R${int(bet_size*0.8)}"}
    elif choppy >= 5:
        opp = 'PLAYER' if last == 'BANK' else 'BANK'
        return {'choppy': choppy, 'suggestion': f"{opp} R${int(bet_size*0.5)}"}
    else:
        opp = 'PLAYER' if last == 'BANK' else 'BANK'
        return {'suggestion': f"{opp} R${int(bet_size)}"}

# HISTÓRICO
if st.session_state.history:
    display_hist = st.session_state.history[-10:][::-1]
    st.markdown("### 📊 ← RECENTE")
    st.caption(" | ".join(display_hist))

# STATS
if st.session_state.history:
    h10 = st.session_state.history[-10:]
    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 BANK", h10.count('BANK'))
    col2.metric("🔵 PLAYER", h10.count('PLAYER'))
    col3.metric("🟡 TIE", h10.count('TIE'))

# SUGESTÃO PRINCIPAL
st.markdown("---")
st.markdown("### 🚀 **NEXT BET**")

if len(st.session_state.history) > 0:
    analysis = analyze(st.session_state.history)
    st.error(f"**{analysis['suggestion']}**")
    
    # PADRÕES
    if 'dragon' in analysis and analysis['dragon']:
        st.warning("🐲 **DRAGON DETECTED**")
    elif analysis.get('streak', 0) >= 4:
        st.info(f"🔥 **Big Road {analysis['streak']}**")
    elif analysis.get('choppy', 0) >= 5:
        st.info(f"🔄 **Choppy {analysis['choppy']}**")
    elif analysis.get('cockroach', False):
        st.success("🐛 **Cockroach**")

else:
    st.info("**Clique para começar**")

if st.button("🗑️ Reset"):
    st.session_state.history = []
    st.rerun()

st.caption("**Elite - Zero Errors**")
