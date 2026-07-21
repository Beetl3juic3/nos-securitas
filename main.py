import streamlit as st

st.set_page_config(page_title="NOS Securitas - Auditoria e Venda", page_icon="🛡️", layout="centered")

st.title("🛡️ NOS Securitas: Auditoria, Upselling e Orçamento")
st.write("Compare o pacote vendido pelo comercial com a necessidade real do terreno.")

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
    "Sensor Cortina": 2.50,
    "Sensor de Quebra de Vidro": 2.00,
    "Sensor de Fumo/Temp": 3.00
}

# Divisões que têm sensor de movimento (PIR) por defeito
DIVISOES_COM_PIR = [
    "Sala de Estar / Zona Comum",
    "Quarto / Suite",
    "Escritório",
    "Arrecadação / Armazém",
    "Oficina / Zona Técnica",
    "Cave",
    "Garagem / Anexo",
    "Cozinha / Copa",
    "Varanda / Terraço",
]

# Instruções específicas de instalação por equipamento
INSTRUCOES_INSTALACAO = {
    "Sensor com Câmara":        "Montar no canto superior (2.0–2.5m), com campo visual a cobrir a porta/acesso principal.",
    "Sensor PIR Normal":        "Montar no canto da divisão a 2.0–2.2m de altura, em diagonal para cobrir toda a área. Evitar AC e janelas a apontar para o sensor.",
    "Sensor Cortina":           "Montar na parede, apontado para a janela/porta em linha reta (deteção em cortina vertical).",
    "Sensor de Quebra de Vidro":"Montar no teto ou parede próxima do vidro (raio de 6m). Testar após instalação.",
    "Sensor de Fumo/Temp":      "Montar no teto, no centro da divisão ou junto à zona de maior risco de fumo.",
    "Câmara de Vídeo Interior": "Posicionar no canto superior a cobrir a área de maior movimento. Verificar ângulo antes de fixar.",
    "Sirene Exterior":          "Fixar na fachada exterior a >2.5m de altura, visível da rua. Usar parafusos anti-sabotagem.",
    "Sirene Interior":          "Fixar no corredor ou hall central para maior cobertura sonora.",
    "Teclado Portátil Extra":   "Emparelhar com a central e testar temporização de entrada/saída.",
}

# --- 1. INICIALIZAÇÃO DA MEMÓRIA DA APP ---
if "divisoes_instaladas" not in st.session_state:
    st.session_state.divisoes_instaladas = []
if "alertas_finais" not in st.session_state:
    st.session_state.alertas_finais = []

# --- 2. PACOTE COMPLETO DO CONTRATO COMERCIAL ---
st.subheader("1. Equipamento do Contrato (Venda Comercial)")
st.caption("Insira as quantidades exatas de todos os dispositivos que constam na proposta do comercial:")

contrato_comercial = {}
col_a, col_b = st.columns(2)

with col_a:
    contrato_comercial["Sensor com Câmara"] = st.number_input("Sensores com Câmara incluídos:", min_value=0, value=1, step=1)
    contrato_comercial["Sensor PIR Normal"] = st.number_input("Sensores PIR normais incluídos:", min_value=0, value=1, step=1)
    contrato_comercial["Contacto Magnético"] = st.number_input("Contactos Magnéticos incluídos:", min_value=0, value=1, step=1)
    contrato_comercial["Sensor de Quebra de Vidro"] = st.number_input("Sensores Quebra de Vidro incluídos:", min_value=0, value=0, step=1)
    contrato_comercial["Sensor Cortina"] = st.number_input("Sensores Cortina incluídos:", min_value=0, value=0, step=1)

with col_b:
    contrato_comercial["Sirene Exterior"] = st.number_input("Sirenes Exteriores incluídas:", min_value=0, value=0, step=1)
    contrato_comercial["Sirene Interior"] = st.number_input("Sirenes Interiores incluídas:", min_value=0, value=0, step=1)
    contrato_comercial["Teclado Portátil Extra"] = st.number_input("Teclados Portáteis incluídos:", min_value=0, value=0, step=1)
    contrato_comercial["Câmara de Vídeo Interior"] = st.number_input("Câmaras de Vídeo Int. incluídas:", min_value=0, value=0, step=1)
    contrato_comercial["Sensor de Fumo/Temp"] = st.number_input("Sensores de Fumo incluídos:", min_value=0, value=0, step=1)

st.divider()

# --- 3. CONFIGURAÇÃO DO CLIENTE ---
st.subheader("2. Perfil do Imóvel e Uso do Sistema")
col1, col2 = st.columns(2)
with col1:
    segmento = st.radio("Contrato:", ["Residencial", "Comercial / Empresa"])
    tem_animais = st.radio("Animais no Interior?", ["Não", "Sim (Até 20kg)", "Sim (Gatos/Cães Grandes)"])
with col2:
    quer_modo_casa = st.radio(
        "Quer armar o alarme à noite e andar livremente por dentro?",
        ["Não (Usa apenas o modo Total quando sai)", "SIM - Quer segurança perimetral para andar livre em casa"]
    )

st.divider()

# --- 4. VISTORIA DINÂMICA (MAPEAMENTO) ---
st.subheader("3. Adicionar Divisão & Análise de Risco")

opcoes_divisoes = [
    "Hall de Entrada / Receção",
    "Sala de Estar / Zona Comum",
    "Quarto / Suite",
    "Cozinha / Copa",
    "Varanda / Terraço",
    "Garagem / Anexo",
    "Cave",
    "Escritório",
    "Arrecadação / Armazém",
    "Oficina / Zona Técnica"
]

divisao_selecionada = st.selectbox("Selecione a divisão atual:", opcoes_divisoes)

piso_selecionado = st.radio(
    "Em que piso/nível fica esta divisão?",
    ["Rés-do-Chão (R/C) / Alvo Fácil", "Piso Intermédio (1º ao 5º Andar)", "Último Andar / Recuado (Risco de Telhado)"]
)

st.caption("Características do espaço:")
c1, c2 = st.columns(2)
with c1:
    tem_janelas = st.checkbox("Tem janelas/portas para o exterior?", value=True)

    num_janelas = 0
    if tem_janelas:
        num_janelas = st.number_input(
            f"Quantas janelas/portas para o exterior tem no/a {divisao_selecionada}?",
            min_value=1, value=1, step=1
        )

    tem_ac_calor = st.checkbox("Tem fontes de calor? (AC, Lareira, Motores)")
with c2:
    grande_envidracado = st.checkbox("Tem grandes vidros / Portas de correr?")
    alto_valor = st.checkbox("Zona de Alto Valor? (Cofre, Bastidor, Stock)")

if st.button("➕ Adicionar ao Plano de Instalação", type="secondary"):

    nova_divisao = {
        "nome": divisao_selecionada,
        "piso": piso_selecionado,
        "tem_janelas": tem_janelas,
        "num_janelas": num_janelas,
        "grande_envidracado": grande_envidracado,
        "alto_valor": alto_valor,
        "equipamentos_base": {}
    }

    if divisao_selecionada == "Hall de Entrada / Receção":
        nova_divisao["equipamentos_base"]["Sensor com Câmara"] = 1
        nova_divisao["equipamentos_base"]["Contacto Magnético"] = max(1, num_janelas)
        nova_divisao["equipamentos_base"]["Painel Touchscreen Principal"] = 1
    else:
        # PIR para todas as divisões habitáveis (inclui agora Cozinha e Varanda)
        if divisao_selecionada in DIVISOES_COM_PIR:
            nova_divisao["equipamentos_base"]["Sensor PIR Normal"] = 1

        # Contactos magnéticos para zonas de risco perimetral (RC, cobertura ou zonas críticas)
        piso_critico = piso_selecionado in ["Rés-do-Chão (R/C) / Alvo Fácil", "Último Andar / Recuado (Risco de Telhado)"]
        zona_critica = divisao_selecionada in ["Garagem / Anexo", "Cave", "Varanda / Terraço"]
        if tem_janelas and (piso_critico or zona_critica):
            nova_divisao["equipamentos_base"]["Contacto Magnético"] = num_janelas

    if grande_envidracado and piso_selecionado != "Piso Intermédio":
        nova_divisao["equipamentos_base"]["Sensor de Quebra de Vidro"] = num_janelas
        nova_divisao["equipamentos_base"]["Sensor Cortina"] = num_janelas

    if divisao_selecionada == "Cozinha / Copa":
        nova_divisao["equipamentos_base"]["Sensor de Fumo/Temp"] = 1

    if alto_valor:
        nova_divisao["equipamentos_base"]["Sirene Exterior"] = 1

    if tem_ac_calor:
        st.session_state.alertas_finais.append(
            f"⚠️ **{divisao_selecionada}:** Evitar montar o sensor PIR alinhado com fontes térmicas diretas."
        )
    if "Sim" in tem_animais:
        st.session_state.alertas_finais.append(
            f"🐾 **Modo Pet:** Regular altura e sensibilidade nas lentes PIR da divisão '{divisao_selecionada}'."
        )

    st.session_state.divisoes_instaladas.append(nova_divisao)
    st.toast(f"{divisao_selecionada} adicionada!", icon="🛡️")

# --- RECALCULAR NECESSIDADES DE CAMPO EM TEMPO REAL ---
necessidades_campo = {key: 0 for key in PRECOS_MENSALIDADES.keys()}

for div in st.session_state.divisoes_instaladas:
    for eq, qtd in div["equipamentos_base"].items():
        if eq in necessidades_campo:
            necessidades_campo[eq] += qtd

    # Modo Casa: janelas de pisos intermédios também precisam de CM perimetral
    if quer_modo_casa == "SIM - Quer segurança perimetral para andar livre em casa" and div["tem_janelas"]:
        qtd_ja_atribuida = div["equipamentos_base"].get("Contacto Magnético", 0)
        if qtd_ja_atribuida < div["num_janelas"]:
            necessidades_campo["Contacto Magnético"] += (div["num_janelas"] - qtd_ja_atribuida)

# --- LISTAGEM DE DIVISÕES ADICIONADAS ---
if st.session_state.divisoes_instaladas:
    st.write("### 🏠 Divisões Mapeadas:")
    for idx, div in enumerate(st.session_state.divisoes_instaladas):
        texto_janelas = f" — {div['num_janelas']} janela(s)" if div['tem_janelas'] and div['num_janelas'] > 0 else " — sem acesso exterior"
        with st.expander(f"📍 {div['nome']} — [{div['piso']}]{texto_janelas}", expanded=False):

            for eq, qtd in div["equipamentos_base"].items():
                st.write(f"- {qtd}x {eq}")

            modo_casa_ativo = quer_modo_casa == "SIM - Quer segurança perimetral para andar livre em casa" and div["tem_janelas"]
            qtd_base_cm = div["equipamentos_base"].get("Contacto Magnético", 0)
            if modo_casa_ativo and qtd_base_cm < div["num_janelas"]:
                extras_noite = div["num_janelas"] - qtd_base_cm
                st.write(f"- {extras_noite}x Contacto Magnético (Extra — Modo Parcial Noturno)")

            if st.button(f"🗑️ Remover", key=f"del_{idx}"):
                st.session_state.divisoes_instaladas.pop(idx)
                st.rerun()

st.divider()

# --- 5. COMPARAÇÃO DINÂMICA E ORÇAMENTAÇÃO ---
st.subheader("4. Balanço Técnico e Orçamento Extra")

if st.session_state.divisoes_instaladas:
    faltas_faturar = {}
    total_mensal_extra = 0.0

    for dispositivo, preco in PRECOS_MENSALIDADES.items():
        quantidade_necessaria = necessidades_campo[dispositivo]
        quantidade_no_contrato = contrato_comercial[dispositivo]
        if quantidade_necessaria > quantidade_no_contrato:
            faltas_faturar[dispositivo] = quantidade_necessaria - quantidade_no_contrato
        else:
            faltas_faturar[dispositivo] = 0

    st.write("#### 💸 Impacto na Mensalidade (Upgrade em Campo):")

    tem_algum_upgrade = False
    for disp, qtd in faltas_faturar.items():
        if qtd > 0:
            custo_item = qtd * PRECOS_MENSALIDADES[disp]
            st.write(f"- **{qtd}x {disp}:** + {custo_item:.2f}€/mês")
            total_mensal_extra += custo_item
            tem_algum_upgrade = True

    if not tem_algum_upgrade:
        st.success("✔️ O pacote comercial cobre perfeitamente todas as necessidades do terreno! Custo extra: 0.00€")
    else:
        st.subheader(f"💵 Total Extra a Somar na Fatura: + {total_mensal_extra:.2f}€ / mês")

    st.divider()

    # --- ROTEIRO TÉCNICO DE INSTALAÇÃO ---
    st.subheader("📍 Roteiro Técnico de Instalação")
    st.write("Guia prático dispositivo a dispositivo:")

    stock = contrato_comercial.copy()

    def instalar(equipamento, divisao_nome, nota_extra=""):
        """Imprime linha de instalação: verde se coberto pelo contrato, azul se extra."""
        instrucao = INSTRUCOES_INSTALACAO.get(equipamento, "Posicionar conforme auditoria técnica.")
        if nota_extra:
            instrucao = nota_extra
        if stock.get(equipamento, 0) > 0:
            st.success(f"✅ **{equipamento}** — {instrucao} *(Incluído no contrato)*")
            stock[equipamento] -= 1
        else:
            st.info(f"➕ **{equipamento} (EXTRA — cobrar +{PRECOS_MENSALIDADES.get(equipamento, 0):.2f}€/mês)** — {instrucao}")

    for div in st.session_state.divisoes_instaladas:
        acesso_label = f"{div['num_janelas']} janela(s)/acesso(s)" if div["tem_janelas"] and div["num_janelas"] > 0 else "sem acesso exterior"
        st.markdown(f"---\n**🏠 {div['nome']}** *(piso: {div['piso'].split('/')[0].strip()} — {acesso_label})*")

        # Painel principal
        if "Painel Touchscreen Principal" in div["equipamentos_base"]:
            st.success("📱 **Painel Touchscreen Principal** — Fixar na parede junto à porta de entrada com parafusos de sabotagem. *(Incluído no contrato)*")

        # Sensor com Câmara
        if "Sensor com Câmara" in div["equipamentos_base"]:
            for _ in range(div["equipamentos_base"]["Sensor com Câmara"]):
                instalar("Sensor com Câmara", div["nome"])

        # Sensor PIR Normal
        if "Sensor PIR Normal" in div["equipamentos_base"]:
            for _ in range(div["equipamentos_base"]["Sensor PIR Normal"]):
                instalar("Sensor PIR Normal", div["nome"])

        # Sensor de Quebra de Vidro
        if "Sensor de Quebra de Vidro" in div["equipamentos_base"]:
            for _ in range(div["equipamentos_base"]["Sensor de Quebra de Vidro"]):
                instalar("Sensor de Quebra de Vidro", div["nome"])

        # Sensor Cortina
        if "Sensor Cortina" in div["equipamentos_base"]:
            for _ in range(div["equipamentos_base"]["Sensor Cortina"]):
                instalar("Sensor Cortina", div["nome"])

        # Sensor de Fumo/Temp
        if "Sensor de Fumo/Temp" in div["equipamentos_base"]:
            instalar("Sensor de Fumo/Temp", div["nome"])

        # Sirene Exterior
        if "Sirene Exterior" in div["equipamentos_base"]:
            instalar("Sirene Exterior", div["nome"])

        # ---- Contactos Magnéticos (janela a janela) ----
        qtd_cm_base = div["equipamentos_base"].get("Contacto Magnético", 0)
        modo_casa_ativo = quer_modo_casa == "SIM - Quer segurança perimetral para andar livre em casa" and div["tem_janelas"]
        total_cm_div = qtd_cm_base
        if modo_casa_ativo and qtd_cm_base < div["num_janelas"]:
            total_cm_div = div["num_janelas"]

        for i in range(1, total_cm_div + 1):
            eh_modo_casa_extra = (i > qtd_cm_base)
            if div["nome"] == "Hall de Entrada / Receção" and i == 1:
                nota = "Montar na porta principal de entrada (controla temporização de entrada/saída)."
            elif eh_modo_casa_extra:
                nota = f"Janela nº{i} — necessário para activar o Modo Parcial Noturno (perímetro protegido com cliente dentro de casa)."
            else:
                nota = f"Janela/acesso nº{i} — montar na caixilharia da porta ou janela."
            instalar("Contacto Magnético", div["nome"], nota)

    st.divider()

    # --- FECHO DE VENDA ---
    st.subheader("5. Fecho de Venda")
    decisao = st.radio(
        "O cliente aceitou o ajuste da mensalidade para os extras?",
        ["A aguardar decisão...", "SIM - Cliente aceitou o valor mensal e quer instalar tudo", "NÃO - Cliente recusou o valor mensal e assume os riscos"]
    )

    if decisao == "SIM - Cliente aceitou o valor mensal e quer instalar tudo":
        st.success(f"🎉 **Venda Fechada!** Adicionado com sucesso: +{total_mensal_extra:.2f}€/mês.")
    elif decisao == "NÃO - Cliente recusou o valor mensal e assume os riscos":
        st.error("⚠️ **Aviso de Obra:** Instale apenas os itens assinalados com ✅ 'Incluído no contrato'.")

    if st.session_state.alertas_finais:
        st.write("### 🚨 Prevenção de Falsos Alarmes:")
        for alerta in list(set(st.session_state.alertas_finais)):
            st.warning(alerta)

    st.divider()
    if st.button("🔄 Nova Instalação / Limpar"):
        st.session_state.divisoes_instaladas = []
        st.session_state.alertas_finais = []
        st.rerun()
else:
    st.info("Insira o pacote comercial completo no Passo 1 e adicione as divisões para gerar o relatório em tempo real.")
