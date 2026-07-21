import streamlit as st 

st.set_page_config(page_title="NOS Securitas - Auditoria e Venda", page_icon="🛡️", layout="centered") 

# --- REMOVE ENGENHARIA VISUAL DO STREAMLIT (RODA AZUL E MENUS) ---
st.markdown("""
<style>
/* Esconde a barra preta superior (Share, Star, Menus) */
div[data-testid="stHeader"] {
display: none !important;
}
/* Esconde o menu de opções original e rodapés antigos */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;} 

/* Esconde o botão 'Manage app' no canto inferior direito */
div[data-testid="stConnectionStatus"] {
display: none !important;
}
iframe[title="Manage app"] {
display: none !important;
} 

/* IMPEDE A EXIBIÇÃO DA TOOLBAR FLUTUANTE INFERIOR (Hosted with Streamlit / Created by) */
div[data-testid="stDeploymentLightbox"],
.stAppDeployButton,
[data-testid="stNotificationViewer"] {
display: none !important;
}
footer, .viewerBadge_container__1QSob, .styles_viewerBadge__3S15m {
display: none !important;
}
/* Alvo direto para o elemento flutuante do plano gratuito */
div[class*="viewerBadge"] {
display: none !important;
}
</style>
""", unsafe_allow_html=True) 

st.title("🛡️ NOS Securitas: Auditoria e Orçamentação")
st.write("Validação técnica em campo e cálculo de upgrades na mensalidade.") 

st.divider() 

# --- TABELA DE PREÇOS MENSAIS OFICIAIS ---
PRECOS_MENSALIDADES = {
"Sensor com Câmara": 3.50,
"Sensor PIR Normal": 2.00,
"Contacto Magnético": 1.50,
"Sirene Exterior": 6.00,
"Sirene Interior": 5.00,
"Teclado Portátil Extra": 2.50,
"Câmara de Vídeo Interior": 5.00,
"Sensor de Fumo/Temp": 3.00,
"Sensor Cortina": 2.50,
"Sensor Quebra de Vidros": 2.00
} 

# --- INICIALIZAÇÃO DA MEMÓRIA DA APP ---
if "divisoes_instaladas" not in st.session_state:
    st.session_state.divisoes_instaladas = []
if "alertas_finais" not in st.session_state:
    st.session_state.alertas_finais = [] 

# --- 1. EQUIPAMENTO DO CONTRATO (ABAS REORGANIZADAS) ---
st.subheader("1. Equipamento do Contrato (Venda Comercial)")
st.caption("Introduza o material que já vem incluído na proposta do comercial:") 

contrato_comercial = {} 

tab_base, tab_extras = st.tabs(["Equipamentos Base 🛡️", "Acessórios / Extras 🔔"]) 

with tab_base:
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        contrato_comercial["Sensor com Câmara"] = st.number_input("Sensores com Câmara:", min_value=0, value=1, step=1, key="cc")
        contrato_comercial["Sensor PIR Normal"] = st.number_input("Sensores PIR Normais:", min_value=0, value=1, step=1, key="pir")
        contrato_comercial["Contacto Magnético"] = st.number_input("Contactos Magnéticos:", min_value=0, value=1, step=1, key="cm")
    with col_b2:
        contrato_comercial["Painel Touchscreen Principal"] = st.number_input("Painel Touchscreen Principal:", min_value=0, value=1, step=1, key="pt")
        contrato_comercial["Placa Dissuasora"] = st.number_input("Placas Dissuasoras incluídas:", min_value=0, value=1, step=1, key="pd")
        contrato_comercial["Sensor Cortina"] = 0 

with tab_extras:
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        contrato_comercial["Sensor Quebra de Vidros"] = st.number_input("Quebra de Vidros no contrato:", min_value=0, value=0, step=1, key="qv")
        contrato_comercial["Sirene Exterior"] = st.number_input("Sirenes Exteriores:", min_value=0, value=0, step=1, key="se")
        contrato_comercial["Sirene Interior"] = st.number_input("Sirenes Interiores:", min_value=0, value=0, step=1, key="si")
    with col_e2:
        contrato_comercial["Câmara de Vídeo Interior"] = st.number_input("Câmaras de Vídeo Int.:", min_value=0, value=0, step=1, key="cam")
        contrato_comercial["Teclado Portátil Extra"] = st.number_input("Teclados Extra:", min_value=0, value=0, step=1, key="tec")
        contrato_comercial["Sensor de Fumo/Temp"] = st.number_input("Sensores de Fumo:", min_value=0, value=0, step=1, key="sf") 

st.divider() 

# --- 2. PERFIL DO IMÓVEL ---
st.subheader("2. Perfil do Imóvel e Uso do Sistema")
col1, col2 = st.columns(2) 

with col1:
    segmento = st.radio("Segmento do Contrato:", ["Residencial", "Comercial / Empresa"], horizontal=True) 
    tipo_imovel = "Moradia"
    if segmento == "Residencial":
        tipo_imovel = st.radio("Tipo de Imóvel:", ["Moradia", "Apartamento"], horizontal=True) 
    tem_animais = st.radio("Animais no Interior?", ["Não", "Sim (Até 20kg)", "Sim (Gatos/Cães Grandes)"], horizontal=True) 

with col2:
    quer_modo_casa = st.radio(
        "Uso do Modo Parcial/Noite (Perímetro ativo com cliente dentro casa):",
        ["Não (Usa apenas o alarme Total quando sai)", "SIM (Quer total liberdade e segurança à noite por dentro)"]
    ) 

st.divider() 

# --- 3. VISTORIA DINÂMICA ---
st.subheader("3. Mapeamento de Divisões e Riscos") 

col_div1, col_div2 = st.columns(2) 

with col_div1:
    opcoes_divisoes = [
        "Hall de Entrada / Receção", "Sala de Estar / Zona Comum", "Quarto / Suite",
        "Cozinha / Copa", "Varanda / Terraço", "Garagem / Anexo", "Cave",
        "Escritório", "Arrecadação / Armazém", "Oficina / Zona Técnica"
    ]
    divisao_selecionada = st.selectbox("Divisão Atual:", opcoes_divisoes) 

with col_div2:
    piso_selecionado = st.selectbox(
        "Nível/Piso da Divisão:",
        ["Rés-do-Chão (R/C) / Alvo Fácil", "Piso Intermédio (1º ao 5º Andar)", "Último Andar / Recuado (Risco de Telhado)"]
    ) 

st.write("Características e Opcionais do Espaço:")
c1, c2 = st.columns(2) 

with c1:
    tem_janelas = st.checkbox("Tem janelas/portas para o exterior?", value=True)
    num_janelas = 1
    if tem_janelas:
        num_janelas = st.number_input("Quantidade de janelas/acessos:", min_value=1, value=1, step=1) 
    tem_ac_calor = st.checkbox("Fontes de calor diretas (AC/Lareira)")
    grande_envidracado = st.checkbox("Grandes vidros / Portas de correr") 

with c2:
    alto_valor = st.checkbox("Zona de Alto Valor (Cofre/Bastidor/Stock)")
    st.write("---")
    # NOVA OPÇÃO: Forçar Painel em qualquer divisão
    quer_painel_opcional = st.checkbox("📱 Instalar Painel Principal nesta divisão")
    quer_cortina_opcional = st.checkbox("➕ Incluir Sensor Cortina Exterior")
    quer_quebra_vidros_opcional = st.checkbox("➕ Incluir Sensor Quebra de Vidros")
    quer_sirene_ext_opcional = st.checkbox("➕ Incluir Sirene Exterior")
    quer_fumo_opcional = st.checkbox("➕ Incluir Sensor de Fumo/Temp")

if st.button("➕ Adicionar Divisão ao Plano", type="primary", use_container_width=True):
    nova_divisao = {
        "nome": divisao_selecionada,
        "piso": piso_selecionado,
        "tem_janelas": tem_janelas,
        "num_janelas": num_janelas,
        "grande_envidracado": grande_envidracado,
        "alto_valor": alto_valor,
        "equipamentos_base": {}
    } 

    # LÓGICA DO PAINEL ATUALIZADA
    if divisao_selecionada == "Hall de Entrada / Receção" or quer_painel_opcional:
        nova_divisao["equipamentos_base"]["Painel Touchscreen Principal"] = 1
        if divisao_selecionada == "Hall de Entrada / Receção":
            nova_divisao["equipamentos_base"]["Sensor com Câmara"] = 1
            nova_divisao["equipamentos_base"]["Contacto Magnético"] = 1
            if num_janelas > 1:
                nova_divisao["equipamentos_base"]["Contacto Magnético"] += (num_janelas - 1)
    else:
        lista_pircam = ["Sala de Estar / Zona Comum", "Escritório", "Arrecadação / Armazém", "Oficina / Zona Técnica", "Cave", "Quarto / Suite", "Garagem / Anexo"]
        if divisao_selecionada in lista_pircam and contrato_comercial.get("Sensor com Câmara", 0) == 0:
            nova_divisao["equipamentos_base"]["Sensor PIR Normal"] = 1 

    if tem_janelas and (piso_selecionado in ["Rés-do-Chão (R/C) / Alvo Fácil", "Último Andar / Recuado (Risco de Telhado)"] or divisao_selecionada in ["Garagem / Anexo", "Cave"]):
        nova_divisao["equipamentos_base"]["Contacto Magnético"] = num_janelas 

    if divisao_selecionada == "Cozinha / Copa":
        nova_divisao["equipamentos_base"]["Sensor de Fumo/Temp"] = 1 

    if quer_cortina_opcional:
        nova_divisao["equipamentos_base"]["Sensor Cortina"] = 1
    if quer_quebra_vidros_opcional:
        nova_divisao["equipamentos_base"]["Sensor Quebra de Vidros"] = 1
    if quer_sirene_ext_opcional:
        nova_divisao["equipamentos_base"]["Sirene Exterior"] = 1
    if quer_fumo_opcional:
        nova_divisao["equipamentos_base"]["Sensor de Fumo/Temp"] = 1

    if tem_ac_calor:
        st.session_state.alertas_finais.append(f"⚠️ {divisao_selecionada}: Afastar PIR da rota direta do fluxo de ar do AC/Lareira.")
    if "Sim" in tem_animais:
        st.session_state.alertas_finais.append(f"🐾 Modo Pet: Configurar altura/lentes imunes a animais na divisão '{divisao_selecionada}'.") 

    st.session_state.divisoes_instaladas.append(nova_divisao)
    st.toast(f"{divisao_selecionada} adicionada com sucesso!", icon="🛡️") 

# --- LISTAGEM DE DIVISÕES MAPEADAS ---
if st.session_state.divisoes_instaladas:
    st.write("### 🏠 Plano de Instalação Atual:")
    for idx, div in enumerate(st.session_state.divisoes_instaladas):
        texto_janelas = f" — {div['num_janelas']} janela(s)" if div['tem_janelas'] else ""
        with st.expander(f"📍 {div['nome']} ({div['piso']}){texto_janelas}"):
            for eq, qtd in div["equipamentos_base"].items():
                st.write(f"- {qtd}x {eq}") 

        if quer_modo_casa == "SIM (Quer total liberdade e segurança à noite por dentro)" and div["tem_janelas"]:
            qtd_base_cm = div["equipamentos_base"].get("Contacto Magnético", 0)
            if qtd_base_cm < div["num_janelas"]:
                st.write(f"- {div['num_janelas'] - qtd_base_cm}x Contacto Magnético (Extra para Perímetro Noturno)") 

        if st.button("🗑️ Remover Divisão", key=f"del_{idx}", type="primary"):
            st.session_state.divisoes_instaladas.pop(idx)
            st.rerun() 

st.divider() 

# --- 4. BALANÇO TÉCNICO E ORÇAMENTO EXTRA ---
st.subheader("4. Análise de Custos e Upgrade de Mensalidade") 

if st.session_state.divisoes_instaladas:
    necessidades_campo = {key: 0 for key in PRECOS_MENSALIDADES.keys()} 

    for div in st.session_state.divisoes_instaladas:
        for eq, qtd in div["equipamentos_base"].items():
            if eq in necessidades_campo:
                necessidades_campo[eq] += qtd 

        if quer_modo_casa == "SIM (Quer total liberdade e segurança à noite por dentro)" and div["tem_janelas"]:
            qtd_ja_atribuida = div["equipamentos_base"].get("Contacto Magnético", 0)
            if qtd_ja_atribuida < div["num_janelas"]:
                necessidades_campo["Contacto Magnético"] += (div["num_janelas"] - qtd_ja_atribuida) 

    faltas_faturar = {}
    total_mensal_extra = 0.0 

    for dispositivo, preco in PRECOS_MENSALIDADES.items():
        qtd_necessaria = necessidades_campo[dispositivo]
        qtd_contrato = contrato_comercial.get(dispositivo, 0)
        faltas_faturar[dispositivo] = max(0, qtd_necessaria - qtd_contrato) 

    col_orç1, col_orç2 = st.columns([2, 1]) 

    with col_orç1:
        st.write("Dispositivos adicionais necessários:")
        tem_algum_upgrade = False
        for disp, qtd in faltas_faturar.items():
            if qtd > 0:
                custo_item = qtd * PRECOS_MENSALIDADES[disp]
                st.write(f"- {qtd}x {disp} (+ {custo_item:.2f}€/mês)")
                total_mensal_extra += custo_item
                tem_algum_upgrade = True 

        if not tem_algum_upgrade:
            st.success("✔️ O pacote comercial cobre a totalidade dos riscos levantados no terreno!") 

    with col_orç2:
        st.metric("Total Extra", f"+{total_mensal_extra:.2f} €") 

    st.divider() 

    # --- ROTEIRO PRÁTICO DE INSTALAÇÃO ---
    st.subheader("📍 Roteiro Técnico de Instalação")
    stock_disponivel = contrato_comercial.copy() 

    if stock_disponivel.get("Placa Dissuasora", 0) > 0:
        st.success(f"🏷️ Colar Placas Dissuasoras: Fixar a(s) {stock_disponivel['Placa Dissuasora']} placa(s) em pontos bem visíveis do exterior (Portões/Acessos).") 

    for div in st.session_state.divisoes_instaladas:
        st.write(f"🏢 {div['nome']}:") 

        for eq, qtd_req in div["equipamentos_base"].items():
            if eq == "Painel Touchscreen Principal":
                if stock_disponivel.get("Painel Touchscreen Principal", 0) > 0:
                    st.success("📱 Fixar Painel Principal -> Instalar com parafusos de sabotagem (Obrigatório).")
                    stock_disponivel["Painel Touchscreen Principal"] -= 1
                else:
                    st.warning("➕ Fixar Painel Principal -> Falta no Contrato!")
                continue

            for _ in range(qtd_req):
                if stock_disponivel.get(eq, 0) > 0:
                    st.caption(f"✔️ Instalar 1x {eq} (Incluído)")
                    stock_disponivel[eq] -= 1
                else:
                    st.info(f"➕ Instalar 1x {eq} (Extra a Faturar)") 

    st.divider() 

    # --- FECHO DE VENDA ---
    st.subheader("5. Fecho de Venda")
    decisao = st.radio("Acordo Comercial com o Cliente:", ["A aguardar simulação...", "Aceitou os extras na mensalidade", "Recusou e assume os riscos de segurança"], horizontal=True) 

    if "Aceitou" in decisao:
        st.success(f"🎉 Contrato Atualizado! Upgrade validado de +{total_mensal_extra:.2f}€/mês.")
    elif "Recusou" in decisao:
        st.error("⚠️ Aviso de Responsabilidade: Proposta recusada. Instalar apenas material base.") 

    # --- SEÇÃO: NOTAS IMPORTANTES DE ENGENHARIA ---
    st.write("### 🚨 Notas Importantes de Engenharia:") 

    st.info("""
    📐 Regras Técnicas de Instalação de Sensores (PIR / PIR-CAM):
    - Altura Recomendada: 2.10m a 2.40m.
    - Proteção Solar: Evitar luz solar direta.

    ⚙️ Fixação Anti-Sabotagem Obrigatória:
    - Utilizar sempre os parafusos de tamper.

    📋 Checklist Final:
    - Ligar para a Central e validar comunicação.
    - Preencher Folha de Ocorrências assinada.
    """) 

    if st.session_state.alertas_finais:
        st.write("Alertas específicos detetados na vistoria:")
        for alerta in list(set(st.session_state.alertas_finais)):
            st.warning(alerta) 

    if st.button("🔄 Reiniciar Auditoria / Limpar Tudo", use_container_width=True):
        st.session_state.divisoes_instaladas = []
        st.session_state.alertas_finais = []
        st.rerun()
else:
    st.info("Mapeie as divisões no Passo 3 para gerar o relatório.")
