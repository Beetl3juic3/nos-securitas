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
    '.card-divisao{border:1px solid #ddd;border-radius:12px;padding:14px;margin-bottom:10px;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,0.06)}'
    '.card-titulo{font-weight:700;color:#003366;font-size:1.05rem;margin-bottom:4px}'
    '.card-meta{color:#666;font-size:0.85rem;margin-bottom:8px}'
    '.badge-equip{display:inline-block;background:#E60000;color:#fff;padding:2px 8px;border-radius:12px;font-size:0.75rem;margin:2px}'
    '.badge-extra{display:inline-block;background:#003366;color:#fff;padding:2px 8px;border-radius:12px;font-size:0.75rem;margin:2px}'
    '.sugestao-box{background:#e8f4fd;border-left:4px solid #003366;padding:10px 14px;border-radius:4px;margin-top:8px}'
    '.check-item{padding:6px 0;border-bottom:1px solid #eee}'
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
    "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"
    "YgAAAABJRU5ErkJggg=="
)
_logo_html = f'<img src="data:image/png;base64,{_LOGO_B64}" width="220" style="display:block;margin:auto;" />'

st.markdown(_logo_html, unsafe_allow_html=True)
st.markdown(
    '<h2 style="text-align:center;margin-top:0.2rem;margin-bottom:0.2rem;">'
    'NOS Securitas</h2>',
    unsafe_allow_html=True
)
st.markdown(
    '<p style="text-align:center;color:#666;font-size:0.95rem;margin-top:0;">'
    'Auditoria e Orçamentação — Validação técnica em campo</p>',
    unsafe_allow_html=True
)
st.divider()

# --- DEMO RÁPIDO ---
col_demo, col_espaco = st.columns([1, 3])
with col_demo:
    if st.button("🚀 Carregar Demo (Casa T3 + Extras)", use_container_width=True):
        st.session_state.divisoes_instaladas = [
            {"nome": "Hall de Entrada / Recepção", "piso": "Rés-do-Chão / Alvo Fácil", "tem_janelas": True, "num_janelas": 2, "grande_envidracado": False, "alto_valor": False, "equipamentos_base": {"Sensor com Câmara": 1, "Contacto Magnético": 2}},
            {"nome": "Sala de Estar / Zona Comum", "piso": "Rés-do-Chão / Alvo Fácil", "tem_janelas": True, "num_janelas": 3, "grande_envidracado": True, "alto_valor": False, "equipamentos_base": {"Sensor PIR Normal": 1, "Contacto Magnético": 3, "Sensor Quebra de Vidros": 1}},
            {"nome": "Quarto / Suite", "piso": "Piso Intermédio", "tem_janelas": True, "num_janelas": 1, "grande_envidracado": False, "alto_valor": False, "equipamentos_base": {"Sensor PIR Normal": 1, "Contacto Magnético": 1}},
            {"nome": "Cozinha / Copa", "piso": "Rés-do-Chão / Alvo Fácil", "tem_janelas": True, "num_janelas": 2, "grande_envidracado": False, "alto_valor": True, "equipamentos_base": {"Sensor PIR Normal": 1, "Contacto Magnético": 2, "Sensor de Fumo/Temp": 1}},
            {"nome": "Varanda / Terraço", "piso": "Rés-do-Chão / Alvo Fácil", "tem_janelas": True, "num_janelas": 1, "grande_envidracado": True, "alto_valor": False, "equipamentos_base": {"Sensor Cortina": 1, "Sirene Exterior": 1}},
        ]
        st.session_state.alertas_finais = [
            "⚠️ Sala de Estar / Zona Comum: Afastar PIR da rota direta do fluxo de ar do AC/Lareira.",
            "🐾 Modo Pet: Configurar altura/lentes imunes a animais na divisão 'Varanda / Terraço'."
        ]
        st.toast("Demo carregada! Casa T3 com 5 divisões + extras.", icon="🚀")
        st.rerun()

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

# --- INICIALIZAÇÃO DA MEMÓRIA DA APP (com demo rápida) ---
if "divisoes_instaladas" not in st.session_state:
    # Demo rápida: casa T3 completa com extras
    st.session_state.divisoes_instaladas = [
        {"nome": "Hall de Entrada / Recepção", "piso": "Rés-do-Chão / Alvo Fácil", "tem_janelas": True, "num_janelas": 2, "grande_envidracado": False, "alto_valor": False, "equipamentos_base": {"Sensor com Câmara": 1, "Contacto Magnético": 2}},
        {"nome": "Sala de Estar / Zona Comum", "piso": "Rés-do-Chão / Alvo Fácil", "tem_janelas": True, "num_janelas": 3, "grande_envidracado": True, "alto_valor": False, "equipamentos_base": {"Sensor PIR Normal": 1, "Contacto Magnético": 3, "Sensor Quebra de Vidros": 1}},
        {"nome": "Quarto / Suite", "piso": "Piso Intermédio", "tem_janelas": True, "num_janelas": 1, "grande_envidracado": False, "alto_valor": False, "equipamentos_base": {"Sensor PIR Normal": 1, "Contacto Magnético": 1}},
        {"nome": "Cozinha / Copa", "piso": "Rés-do-Chão / Alvo Fácil", "tem_janelas": True, "num_janelas": 2, "grande_envidracado": False, "alto_valor": True, "equipamentos_base": {"Sensor PIR Normal": 1, "Contacto Magnético": 2, "Sensor de Fumo/Temp": 1}},
        {"nome": "Varanda / Terraço", "piso": "Rés-do-Chão / Alvo Fácil", "tem_janelas": True, "num_janelas": 1, "grande_envidracado": True, "alto_valor": False, "equipamentos_base": {"Sensor Cortina": 1, "Sirene Exterior": 1}},
    ]
if "alertas_finais" not in st.session_state:
    st.session_state.alertas_finais = [
        "⚠️ Sala de Estar / Zona Comum: Afastar PIR da rota direta do fluxo de ar do AC/Lareira.",
        "🐾 Modo Pet: Configurar altura/lentes imunes a animais na divisão 'Varanda / Terraço'."
    ]
if "nome_cliente" not in st.session_state:
    st.session_state.nome_cliente = ""
if "historico_auditorias" not in st.session_state:
    st.session_state.historico_auditorias = []


def calcular_necessidades(divisoes, modo_noturno):
    """Calcula necessidades totais de equipamento."""
    necessidades = {key: 0 for key in PRECOS_MENSALIDADES.keys()}
    for div in divisoes:
        for eq, qtd in div["equipamentos_base"].items():
            if eq in necessidades:
                necessidades[eq] += qtd
        if modo_noturno == "SIM (Quer segurança à noite por dentro)" and div["tem_janelas"]:
            qtd_cm = div["equipamentos_base"].get("Contacto Magnético", 0)
            if qtd_cm < div["num_janelas"]:
                necessidades["Contacto Magnético"] += (div["num_janelas"] - qtd_cm)
    return necessidades


def calcular_faltas_e_extra(necessidades, stock_contrato):
    """Calcula faltas e custo extra mensal."""
    faltas = {}
    total = 0.0
    for disp, preco in PRECOS_MENSALIDADES.items():
        qtd_nec = necessidades.get(disp, 0)
        qtd_con = stock_contrato.get(disp, 0)
        faltas[disp] = max(0, qtd_nec - qtd_con)
        total += faltas[disp] * preco
    return faltas, total

# --- 1. EQUIPAMENTO DO CONTRATO (ABAS) ---
st.subheader("1. Equipamento do Contrato (Venda Comercial)")
st.caption("Introduza o material que já vem incluído na proposta do comercial:")

contrato_comercial = {}

tab_base, tab_extras = st.tabs(["🛡️ Equipamentos Base", "🔔 Acessórios / Extras"])

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
    quer_modo_casa = st.session_state.quer_modo_casa = st.radio(
        "Uso do Modo Parcial/Noite:",
        ["Não (Usa apenas o alarme Total quando sai)", "SIM (Quer segurança à noite por dentro)"]
    )

st.divider()

# --- 3. VISTORIA DINÂMICA ---
st.subheader("3. Mapeamento de Divisões e Riscos")

col_div1, col_div2 = st.columns(2)

with col_div1:
    opcoes_divisoes = [
        "Hall de Entrada / Recepção", "Sala de Estar / Zona Comum", "Quarto / Suite",
        "Cozinha / Copa", "Varanda / Terraço", "Garagem / Anexo", "Cave",
        "Escritório", "Arrecadação / Armazém", "Oficina / Zona Técnica"
    ]
    divisao_selecionada = st.selectbox("Divisão Atual:", opcoes_divisoes)

with col_div2:
    piso_selecionado = st.selectbox(
        "Nível/Piso:",
        ["Rés-do-Chão / Alvo Fácil", "Piso Intermédio", "Último Andar / Recuado"]
    )

st.write("Características do Espaço:")
c1, c2 = st.columns(2)

with c1:
    tem_janelas = st.checkbox("Tem janelas/portas para o exterior?", value=True)
    num_janelas = 1
    if tem_janelas:
        num_janelas = st.number_input("Quantidade de janelas/portas/acessos:", min_value=1, value=1, step=1)
    tem_ac_calor = st.checkbox("Fontes de calor diretas (AC/Lareira)")
    grande_envidracado = st.checkbox("Grandes vidros / Portas de correr")

with c2:
    alto_valor = st.checkbox("Zona de Alto Valor (Cofre/Bastidor/Stock)")
    st.write("---")
    quer_painel_opcional = st.checkbox("📱 Instalar Painel Principal nesta divisão")
    quer_cortina_opcional = st.checkbox("➕ Incluir Sensor Cortina")
    quer_quebra_vidros_opcional = st.checkbox("➕ Incluir Sensor Quebra de Vidros")
    quer_sirene_ext_opcional = st.checkbox("➕ Incluir Sirene Exterior")
    quer_fumo_opcional = st.checkbox("➕ Incluir Sensor de Fumo/Temp")

# --- SUGESTÕES INTELIGENTES ---
sugestoes = []
if tem_janelas and num_janelas >= 3:
    sugestoes.append("💡 Muitas janelas — considerar Sensor Cortina para proteção ampliada.")
if grande_envidracado:
    sugestoes.append("💡 Grandes vidros detectados — Sensor Quebra de Vidros recomendado.")
if tem_animais and "Sim" in tem_animais:
    sugestoes.append("💡 Animal no interior — usar PIR com lentes imunes a pets ou Sensor Cortina.")
if alto_valor:
    sugestoes.append("💡 Zona de Alto Valor — adicionar Câmara de Vídeo Interior ou Sensor com Câmara.")
if tem_ac_calor:
    sugestoes.append("💡 Fonte de calor — afastar PIR da rota do ar quente.")
if piso_selecionado == "Rés-do-Chão / Alvo Fácil" and tem_janelas:
    sugestoes.append("💡 Rés-do-Chão com janelas — Contacto Magnético obrigatório + considerar Sirene Exterior.")

if sugestoes:
    st.markdown('<div class="sugestao-box"><strong>🧠 Sugestões Automáticas de Engenharia:</strong><br>' +
                '<br>'.join(sugestoes) + '</div>', unsafe_allow_html=True)

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

    if divisao_selecionada == "Hall de Entrada / Recepção":
        nova_divisao["equipamentos_base"]["Sensor com Câmara"] = 1
        nova_divisao["equipamentos_base"]["Contacto Magnético"] = 1
        if num_janelas > 1:
            nova_divisao["equipamentos_base"]["Contacto Magnético"] += (num_janelas - 1)
    else:
        lista_pircam = ["Sala de Estar / Zona Comum", "Escritório", "Arrecadação / Armazém",
                        "Oficina / Zona Técnica", "Cave", "Quarto / Suite", "Garagem / Anexo"]
        if divisao_selecionada in lista_pircam:
            nova_divisao["equipamentos_base"]["Sensor PIR Normal"] = 1

        if tem_janelas and (piso_selecionado in ["Rés-do-Chão / Alvo Fácil", "Último Andar / Recuado"]
                            or divisao_selecionada in ["Garagem / Anexo", "Cave", "Cozinha / Copa"]):
            nova_divisao["equipamentos_base"]["Contacto Magnético"] = num_janelas

    if quer_painel_opcional:
        nova_divisao["equipamentos_base"]["Painel Touchscreen Principal"] = 1

    if quer_cortina_opcional:
        nova_divisao["equipamentos_base"]["Sensor Cortina"] = 1
    if quer_quebra_vidros_opcional:
        nova_divisao["equipamentos_base"]["Sensor Quebra de Vidros"] = 1
    if quer_sirene_ext_opcional:
        nova_divisao["equipamentos_base"]["Sirene Exterior"] = 1
    if quer_fumo_opcional:
        nova_divisao["equipamentos_base"]["Sensor de Fumo/Temp"] = 1

    if tem_ac_calor:
        st.session_state.alertas_finais.append(
            f"⚠️ {divisao_selecionada}: Afastar PIR da rota direta do fluxo de ar do AC/Lareira."
        )
    if "Sim" in tem_animais:
        st.session_state.alertas_finais.append(
            f"🐾 Modo Pet: Configurar altura/lentes imunes a animais na divisão '{divisao_selecionada}'."
        )

    st.session_state.divisoes_instaladas.append(nova_divisao)
    st.toast(f"{divisao_selecionada} adicionada com sucesso!", icon="🛡️")

# --- LISTAGEM DE DIVISÕES (CARDS VISUAIS) ---
if st.session_state.divisoes_instaladas:
    st.write("### 🏠 Plano de Instalação Atual:")
    for idx, div in enumerate(st.session_state.divisoes_instaladas):
        texto_janelas = f" | {div['num_janelas']} janela(s)/porta(s)" if div['tem_janelas'] else " | Sem acessos exteriores"
        alertas_div = []
        if div.get("alto_valor"):
            alertas_div.append("🔒 Alto Valor")
        if div.get("grande_envidracado"):
            alertas_div.append("🖼️ Grandes Vidros")
        alertas_html = " | ".join(alertas_div) if alertas_div else ""

        badges = ""
        for eq, qtd in div["equipamentos_base"].items():
            tipo = "badge-extra" if eq in ["Sensor Cortina", "Sensor Quebra de Vidros", "Sirene Exterior", "Sensor de Fumo/Temp", "Câmara de Vídeo Interior", "Teclado Portátil Extra"] else "badge-equip"
            badges += f'<span class="{tipo}">{qtd}x {eq}</span>'

        modo_extra = ""
        if quer_modo_casa == "SIM (Quer segurança à noite por dentro)" and div["tem_janelas"]:
            qtd_base_cm = div["equipamentos_base"].get("Contacto Magnético", 0)
            if qtd_base_cm < div["num_janelas"]:
                extra_cm = div["num_janelas"] - qtd_base_cm
                modo_extra = f'<span class="badge-extra">{extra_cm}x Contacto Magnético (🌙 Noturno)</span>'

        card_html = f"""
        <div class="card-divisao">
            <div class="card-titulo">📍 {div['nome']}</div>
            <div class="card-meta">{div['piso']}{texto_janelas}{' | ' + alertas_html if alertas_html else ''}</div>
            <div>{badges}{modo_extra}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        if st.button("🗑️ Remover", key=f"del_{idx}", type="primary"):
            st.session_state.divisoes_instaladas.pop(idx)
            st.rerun()

st.divider()

# --- DASHBOARD EM TEMPO REAL ---
if st.session_state.divisoes_instaladas:
    st.subheader("📊 Resumo da Auditoria")

    necessidades_live = calcular_necessidades(st.session_state.divisoes_instaladas, quer_modo_casa)
    faltas_live, total_live = calcular_faltas_e_extra(necessidades_live, contrato_comercial)

    c1, c2, c3, c4 = st.columns([1, 1, 1, 1.2])
    with c1:
        st.metric("Divisões Mapeadas", len(st.session_state.divisoes_instaladas))
    with c2:
        st.metric("Custo Extra Mensal", f"+{total_live:.2f} €")
    with c3:
        extras_count = sum(1 for q in faltas_live.values() if q > 0)
        st.metric("Tipos de Extras", extras_count)
    with c4:
        st.write("")
        st.write("")
        if st.button("🔄 Limpar Tudo", use_container_width=True):
            st.session_state.divisoes_instaladas = []
            st.session_state.alertas_finais = []
            st.session_state.nome_cliente = ""
            st.rerun()

    stock_excedido = []
    for disp, qtd_falta in faltas_live.items():
        if qtd_falta > 0:
            stock_excedido.append(f"{disp}: precisa de {necessidades_live[disp]}, contrato tem {contrato_comercial.get(disp, 0)}")

    if stock_excedido:
        st.warning("⚠️ Stock do Contrato Insuficiente:\n" + "\n".join(f"- {s}" for s in stock_excedido))

    st.divider()

# --- 4. BALANÇO TÉCNICO ---
st.subheader("4. Análise de Custos e Upgrade de Mensalidade")

if st.session_state.divisoes_instaladas:
    necessidades_campo = {key: 0 for key in PRECOS_MENSALIDADES.keys()}

    for div in st.session_state.divisoes_instaladas:
        for eq, qtd in div["equipamentos_base"].items():
            if eq in necessidades_campo:
                necessidades_campo[eq] += qtd

        if quer_modo_casa == "SIM (Quer segurança à noite por dentro)" and div["tem_janelas"]:
            qtd_ja = div["equipamentos_base"].get("Contacto Magnético", 0)
            if qtd_ja < div["num_janelas"]:
                necessidades_campo["Contacto Magnético"] += (div["num_janelas"] - qtd_ja)

    faltas_faturar = {}
    total_mensal_extra = 0.0

    for dispositivo, preco in PRECOS_MENSALIDADES.items():
        qtd_nec = necessidades_campo[dispositivo]
        qtd_con = contrato_comercial.get(dispositivo, 0)
        faltas_faturar[dispositivo] = max(0, qtd_nec - qtd_con)

    col_orc1, col_orc2 = st.columns([2, 1])

    with col_orc1:
        st.write("Dispositivos adicionais necessários:")
        tem_upgrade = False
        for disp, qtd in faltas_faturar.items():
            if qtd > 0:
                custo = qtd * PRECOS_MENSALIDADES[disp]
                st.write(f"- {qtd}x {disp} (+ {custo:.2f}€/mês)")
                total_mensal_extra += custo
                tem_upgrade = True

        if not tem_upgrade:
            st.success("✔️ O pacote comercial cobre todos os riscos levantados no terreno!")

    with col_orc2:
        st.metric("Total Extra", f"+{total_mensal_extra:.2f} €")

    st.divider()

    # --- ROTEIRO ---
    st.subheader("📍 Roteiro Técnico de Instalação")
    stock = contrato_comercial.copy()

    if stock.get("Placa Dissuasora", 0) > 0:
        st.success(f"🏷️ Colar Placas Dissuasoras: Fixar a(s) {stock['Placa Dissuasora']} placa(s) em pontos bem visíveis do exterior (Portões/Acessos).")

    for div in st.session_state.divisoes_instaladas:
        st.write(f"🏢 {div['nome']}:")

        equipamentos_rota = div["equipamentos_base"].copy()

        if quer_modo_casa == "SIM (Quer segurança à noite por dentro)" and div["tem_janelas"]:
            qtd_cm = equipamentos_rota.get("Contacto Magnético", 0)
            if qtd_cm < div["num_janelas"]:
                equipamentos_rota["Contacto Magnético"] = div["num_janelas"]

        for eq, qtd_req in equipamentos_rota.items():
            if eq == "Painel Touchscreen Principal":
                if stock.get("Painel Touchscreen Principal", 0) > 0:
                    st.success("📱 Fixar Painel Principal → Instalar nos furos de sabotagem (Incluído).")
                    stock["Painel Touchscreen Principal"] -= 1
                else:
                    st.warning("➕ Fixar Painel Principal → Falta no Contrato!")
                continue

            qtd_base = div["equipamentos_base"].get(eq, 0)
            for i in range(qtd_req):
                if i < qtd_base:
                    if stock.get(eq, 0) > 0:
                        st.caption(f"✔️ Instalar 1x {eq} (Incluído)")
                        stock[eq] -= 1
                    else:
                        st.info(f"➕ Instalar 1x {eq} (Extra a Faturar)")
                else:
                    st.info(f"➕ Instalar 1x {eq} (Extra — Perímetro Noturno)")

    st.divider()

    # --- COMPARADOR DE PACOTES ---
    st.subheader("📊 Comparador de Pacotes")
    pacotes = {
        "Base (Contrato)": {k: contrato_comercial.get(k, 0) for k in PRECOS_MENSALIDADES.keys()},
        "Necessário (Campo)": necessidades_campo,
        "Extra a Faturar": faltas_faturar,
    }
    comp_cols = st.columns(3)
    for i, (nome, dados) in enumerate(pacotes.items()):
        with comp_cols[i]:
            total_p = sum(dados.values())
            st.markdown(f"**{nome}**")
            st.markdown(f'<div style="font-size:1.4rem;font-weight:700;color:{NOS_AZUL if i==1 else NOS_VERMELHO if i==2 else "#333"};">{total_p} equip.</div>', unsafe_allow_html=True)
            for d, q in dados.items():
                if q > 0:
                    st.caption(f"{q}x {d}")

    st.divider()

    # --- FECHO ---
    st.subheader("5. Fecho de Venda")
    decisao = st.radio(
        "Acordo Comercial:",
        ["A aguardar simulação...", "Aceitou os extras na mensalidade", "Recusou e assume os riscos"],
        horizontal=True
    )

    if "Aceitou" in decisao:
        st.success(f"🎉 Contrato Atualizado! Upgrade validado de +{total_mensal_extra:.2f}€/mês.")
    elif "Recusou" in decisao:
        st.error("⚠️ Proposta recusada. Instalar apenas material base.")

# --- NOTAS + CHECKLIST INTERATIVO ---
st.write("### 🚨 Regras Técnicas de Instalação")
st.info("""
📐 Regras Técnicas de Instalação:
- Altura Recomendada: 2.10m a 2.40m.
- Proteção Solar: Evitar luz solar direta.
- Fixação Anti-Sabotagem Obrigatória: parafusos de tamper.
""")

st.subheader("✅ Checklist Final de Instalação")
if "checklist" not in st.session_state:
    st.session_state.checklist = {
        "painel_fixado": False,
        "sensores_testados": False,
        "contactos_alinhados": False,
        "sirene_funcional": False,
        "comunicacao_central": False,
        "cliente_treinado": False,
    }

check_items = [
    ("painel_fixado", "📱 Painel principal fixado com parafusos de tamper"),
    ("sensores_testados", "🔍 Todos os sensores testados e com cobertura verificada"),
    ("contactos_alinhados", "🪟 Contactos magnéticos alinhados e com gap < 5mm"),
    ("sirene_funcional", "🚨 Sirene testada e audível no exterior"),
    ("comunicacao_central", "📞 Comunicação com a Central validada"),
    ("cliente_treinado", "👥 Cliente treinado no uso da app/painel"),
]

progresso = sum(1 for v in st.session_state.checklist.values() if v)
total_checks = len(st.session_state.checklist)
st.progress(progresso / total_checks, text=f"{progresso}/{total_checks} tarefas concluídas")

for key, label in check_items:
    st.session_state.checklist[key] = st.checkbox(label, value=st.session_state.checklist[key])

if progresso == total_checks:
    st.success("🎯 Checklist completo! Instalação pronta para ativação.")

if st.session_state.alertas_finais:
    st.write("Alertas específicos detetados:")
    for alerta in list(set(st.session_state.alertas_finais)):
        st.warning(alerta)

if st.button("🔄 Reiniciar Auditoria / Limpar Tudo", use_container_width=True):
    st.session_state.divisoes_instaladas = []
    st.session_state.alertas_finais = []
    st.session_state.nome_cliente = ""
    st.rerun()

if not st.session_state.divisoes_instaladas:
    st.info("Mapeie as divisões no Passo 3 para gerar o relatório.")
