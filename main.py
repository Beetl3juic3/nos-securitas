import streamlit as st

st.set_page_config(page_title="NOS Securitas - Auditoria e Venda", page_icon="🛡️", layout="centered")

# --- TEMA NOS + UTILIDADES ---
if "tema_escuro" not in st.session_state:
    st.session_state.tema_escuro = False

NOS_VERMELHO = "#E60000"
NOS_AZUL = "#003366"
NOS_CINZA = "#F5F5F5"

st.markdown(
    '<style>'
    'div[data-testid="stHeader"]{display:none!important}'
    '#MainMenu{visibility:hidden}'
    'footer{visibility:hidden}'
    'header{visibility:hidden}'
    'div[data-testid="stConnectionStatus"]{display:none!important}'
    'iframe[title="Manage app"]{display:none!important}'
    'div[data-testid="stDeploymentLightbox"],.stAppDeployButton,[data-testid="stNotificationViewer"]{display:none!important}'
    'div[class*="viewerBadge"]{display:none!important}'
    '.card-divisao{border:1px solid rgba(128,128,128,0.25);border-radius:12px;padding:14px;margin-bottom:10px;background:rgba(128,128,128,0.06);box-shadow:0 2px 6px rgba(0,0,0,0.06)}'
    '.card-titulo{font-weight:700;color:#003366;font-size:1.05rem;margin-bottom:4px}'
    '.card-meta{color:#888;font-size:0.85rem;margin-bottom:8px}'
    '.badge-equip{display:inline-block;background:#E60000;color:#fff;padding:2px 8px;border-radius:12px;font-size:0.75rem;margin:2px}'
    '.badge-extra{display:inline-block;background:#003366;color:#fff;padding:2px 8px;border-radius:12px;font-size:0.75rem;margin:2px}'
    '.sugestao-box{background:rgba(0,51,102,0.12);border-left:4px solid #003366;padding:10px 14px;border-radius:4px;margin-top:8px}'
    '.check-item{padding:6px 0;border-bottom:1px solid rgba(128,128,128,0.2)}'
    '.check-done{text-decoration:line-through;color:#888}'
    '</style>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div style="text-align:right;margin-bottom:-10px;">'
    f'<span style="font-size:0.8rem;color:#666;">Tema: </span>'
    f'<a href="?" target="_self" style="text-decoration:none;font-size:0.85rem;">'
    f'{"🌙 Escuro" if not st.session_state.tema_escuro else "☀️ Claro"}</a>'
    f'</div>',
    unsafe_allow_html=True
)

# --- CABEÇALHO COM LOGO ---
_LOGO_B64 = (
