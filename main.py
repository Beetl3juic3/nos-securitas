import streamlit as st

st.set_page_config(page_title="NOS Securitas - Auditoria e Venda", page_icon="🛡️", layout="centered")

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
    '</style>',
    unsafe_allow_html=True
)

# --- CABEÇALHO COM LOGO ---
import base64, os
_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
_logo_b64 = base64.b64encode(open(_logo_path, "rb").read()).decode()
_logo_html = f'<img src="data:image/png;base64,{_logo_b64}" width="220" style="display:block;margin:auto;" />'

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

# --- LISTAGEM DE DIVISÕES ---
if st.session_state.divisoes_instaladas:
    st.write("### 🏠 Plano de Instalação Atual:")
    for idx, div in enumerate(st.session_state.divisoes_instaladas):
        texto_janelas = f" — {div['num_janelas']} janela(s)/porta(s)" if div['tem_janelas'] else ""
        with st.expander(f"📍 {div['nome']} ({div['piso']}){texto_janelas}"):
            for eq, qtd in div["equipamentos_base"].items():
                st.write(f"- {qtd}x {eq}")

            if quer_modo_casa == "SIM (Quer segurança à noite por dentro)" and div["tem_janelas"]:
                qtd_base_cm = div["equipamentos_base"].get("Contacto Magnético", 0)
                if qtd_base_cm < div["num_janelas"]:
                    st.write(f"- {div['num_janelas'] - qtd_base_cm}x Contacto Magnético (Extra — Perímetro Noturno)")

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

# --- NOTAS ---
st.write("### 🚨 Notas Importantes de Engenharia:")
st.info("""
📐 Regras Técnicas de Instalação:
- Altura Recomendada: 2.10m a 2.40m.
- Proteção Solar: Evitar luz solar direta.
- Fixação Anti-Sabotagem Obrigatória: parafusos de tamper.
- Checklist Final: Ligar para a Central e validar comunicação.
""")

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
