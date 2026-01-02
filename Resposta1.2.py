import streamlit as st

st.title("Football Studio PRO")

if 'h' not in st.session_state:
    st.session_state.h = []
    st.session_state.bank = 200

bank = st.number_input("💰 Bankroll", value=st.session_state.bank)

# BOTÕES
col1, col2, col3 = st.columns(3)
if col1.button("🔴 BANK", use_container_width=True):
    st.session_state.h.append('🔴')
    st.rerun()
if col2.button("🔵 PLAYER", use_container_width=True):
    st.session_state.h.append('🔵')
    st.rerun()
if col3.button("🟡 TIE", use_container_width=True):
    st.session_state.h.append('🟡')
    st.rerun()

# HISTÓRICO EMOJIS ← RECENTE ESQUERDA
h = st.session_state.h[-15:][::-1]
if h:
    st.markdown("### 📊 **← RECENTE**")
    st.caption("   ".join(h))

# ANÁLISE PADRÕES
def analyze_patterns(hist):
    if len(hist) < 2:
        return {'bet': '⏳', 'amount': 0, 'pattern': 'WAIT'}
    
    # Recupera ordem original (mais recente no final)
    orig_hist = hist[::-1]
    last = orig_hist[-1]
    
    # STREAK
    streak = 1
    for i in range(1, min(10, len(orig_hist))):
        if orig_hist[-i-1] == last:
            streak += 1
        else:
            break
    
    # CHOPPY
    choppy = 0
    for i in range(1, min(8, len(orig_hist))):
        if orig_hist[-i] != orig_hist[-i-1]:
            choppy += 1
    
    # COCKROACH BBP/PPB
    cockroach = len(orig_hist) >= 3 and orig_hist[-3:] in [['🔴','🔴','🔵'], ['🔵','🔵','🔴']]
    
    amount = int(bank * 0.01)
    
    if streak >= 6:
        bet = '🔵' if last == '🔴' else '🔴'
        amount = int(bank * 0.02)
        return {'bet': bet, 'amount': amount, 'pattern': '🐲 DRAGON'}
    elif streak >= 4:
        bet = '🔵' if last == '🔴' else '🔴'
        amount = int(bank * 0.015)
        return {'bet': bet, 'amount': amount, 'pattern': f'🔥 STREAK {streak}'}
    elif cockroach:
        bet = '🔴'
        amount = int(bank * 0.008)
        return {'bet': bet, 'amount': amount, 'pattern': '🐛 COCKROACH'}
    elif choppy >= 5:
        bet = '🔵' if last == '🔴' else '🔴'
        amount = int(bank * 0.005)
        return {'bet': bet, 'amount': amount, 'pattern': f'🔄 CHOPPY {choppy}'}
    else:
        bet = '🔵' if last == '🔴' else '🔴'
        return {'bet': bet, 'amount': amount, 'pattern': '➡️ NORMAL'}

# SUGESTÃO PRINCIPAL
st.markdown("---")
st.markdown("### 🎯 **APOSTA AGORA**")

if st.session_state.h:
    analysis = analyze_patterns(h)
    
    col1, col2, col3 = st.columns([1,4,1])
    with col1:
        st.markdown(f"### **{analysis['bet']}**")
    with col2:
        st.markdown(f"### **R${analysis['amount']}**")
    with col3:
        st.success(f"**{analysis['pattern']}**")
    
    st.caption(f"Histórico: {len(st.session_state.h)} rodadas | Stake: {analysis['amount']/bank*100:.1f}%")
else:
    st.info("**Clique primeiro resultado**")

# STATS
if st.session_state.h:
    recent = st.session_state.h[-20:]
    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 BANK", recent.count('🔴'))
    col2.metric("🔵 PLAYER", recent.count('🔵'))
    col3.metric("🟡 TIE", recent.count('🟡'))

if st.button("🗑️ Clear", type="secondary"):
    st.session_state.h = []
    st.rerun()
