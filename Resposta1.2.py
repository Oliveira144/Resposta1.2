import streamlit as st

st.title("Football Studio CONSERVADOR")

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

# HISTÓRICO ← RECENTE
h_display = st.session_state.h[-15:][::-1]
if h_display:
    st.markdown("### 📊 **← RECENTE**")
    st.caption("   ".join(h_display))

# ANÁLISE CONSERVADORA (SÓ ENTRA COM PADRÃO FORTE)
def analyze_conservative(hist):
    if len(hist) < 6:
        return {'bet': '⏳', 'amount': 0, 'pattern': '6+ rodadas', 'confidence': 0}
    
    # Ordem original (recente final)
    orig = hist[::-1]
    
    # 1. STREAK 5+ (40% setups)
    streak = 1
    last = orig[-1]
    for i in range(1, min(12, len(orig))):
        if orig[-i-1] == last:
            streak += 1
        else:
            break
    
    # 2. CHOPPY 6+ alternados
    choppy = sum(1 for i in range(1, min(10, len(orig))) if orig[-i] != orig[-i-1])
    
    # 3. COCKROACH exato BBP ou PPB
    cockroach = len(orig) >= 3 and orig[-3:] in [['🔴','🔴','🔵'], ['🔵','🔵','🔴']]
    
    # 4. TIE STREAK (2+ TIEs)
    tie_streak = sum(1 for i in range(min(4, len(orig))) if orig[-i] == '🟡')
    
    confidence = 0
    
    # PRIORIDADE 1: DRAGON 6+ (alta prob break)
    if streak >= 6:
        bet = '🔵' if last == '🔴' else '🔴'
        amount = int(bank * 0.02)
        confidence = 85
        return {'bet': bet, 'amount': amount, 'pattern': f'🐲 DRAGON {streak}', 'confidence': confidence}
    
    # PRIORIDADE 2: COCKROACH (padrão recorrente)
    elif cockroach:
        bet = '🔴'
        amount = int(bank * 0.01)
        confidence = 75
        return {'bet': bet, 'amount': amount, 'pattern': '🐛 COCKROACH', 'confidence': confidence}
    
    # PRIORIDADE 3: CHOPPY 7+ (alternado forte)
    elif choppy >= 7:
        bet = '🔵' if last == '🔴' else '🔴'
        amount = int(bank * 0.008)
        confidence = 70
        return {'bet': bet, 'amount': amount, 'pattern': f'🔄 CHOPPY {choppy}', 'confidence': confidence}
    
    # PRIORIDADE 4: TIE STREAK 3+
    elif tie_streak >= 3:
        bet = '🔴'  # BANK após TIEs
        amount = int(bank * 0.005)
        confidence = 65
        return {'bet': bet, 'amount': amount, 'pattern': f'🟡 TIEs {tie_streak}', 'confidence': confidence}
    
    else:
        return {'bet': '⏳', 'amount': 0, 'pattern': 'SEM SETUP', 'confidence': 0}

# SUGESTÃO CONSERVADORA
st.markdown("---")
st.markdown("### 🎯 **ANÁLISE**")

if len(st.session_state.h) >= 6:
    analysis = analyze_conservative(h_display)
    
    if analysis['confidence'] > 0:
        col1, col2, col3 = st.columns([2,3,2])
        with col1:
            st.markdown(f"### **{analysis['bet']}**")
        with col2:
            st.markdown(f"### **R${analysis['amount']}**")
        with col3:
            st.success(f"**{analysis['confidence']}%**")
        
        st.info(f"**{analysis['pattern']}**")
    else:
        st.markdown("### **⏳ AGUARDAR**")
        st.warning("**SEM PADRÃO FORTE** - Paciência")
        
else:
    st.info(f"**{6-len(st.session_state.h)} rodadas** para análise")

# STATS
if st.session_state.h:
    recent = st.session_state.h[-20:]
    col1, col2, col3 = st.columns(3)
    col1.metric("🔴", recent.count('🔴'))
    col2.metric("🔵", recent.count('🔵'))
    col3.metric("🟡", recent.count('🟡'))

if st.button("🗑️ Clear"):
    st.session_state.h = []
    st.rerun()

st.caption("**Conservador** - só entra setup forte 65%+")
