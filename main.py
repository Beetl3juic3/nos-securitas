
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
    faltas_live, total_live = calcular_faltas_e_extra(necessidades_live, st.session_state.contrato_comercial)

    # Calcular diferença com/sin modo noite
    necessidades_sem_noite = calcular_necessidades(st.session_state.divisoes_instaladas, "Não (Usa apenas o alarme Total quando sai)")
    faltas_sem_noite, total_sem_noite = calcular_faltas_e_extra(necessidades_sem_noite, st.session_state.contrato_comercial)
    diff_noite = total_live - total_sem_noite

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

    # Comparador de modo noite
    if diff_noite > 0:
        st.markdown(
            f'<div style="background:rgba(230,0,0,0.08);border-left:4px solid #E60000;padding:10px 14px;border-radius:4px;margin-top:8px;">'
            f'<strong>🌙 Impacto do Modo Noite:</strong> O modo noturno adiciona <strong>{diff_noite:.2f} €/mês</strong> extra '
            f'(sem modo noite: +{total_sem_noite:.2f} €, com modo noite: +{total_live:.2f} €). '
            f'Pode mostrar esta diferença ao cliente para decidir.</div>',
            unsafe_allow_html=True
        )
    elif diff_noite == 0 and quer_modo_casa == "SIM (Quer segurança à noite por dentro)":
        st.markdown(
            f'<div style="background:rgba(0,51,102,0.08);border-left:4px solid #003366;padding:10px 14px;border-radius:4px;margin-top:8px;">'
            f'<strong>🌙 Impacto do Modo Noite:</strong> Sem custo extra. O modo noturno não acrescenta equipamentos adicionais para esta configuração.</div>',
            unsafe_allow_html=True
        )

    stock_excedido = []
    for disp, qtd_falta in faltas_live.items():
        if qtd_falta > 0:
            stock_excedido.append(f"{disp}: precisa de {necessidades_live[disp]}, contrato tem {st.session_state.contrato_comercial.get(disp, 0)}")

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
        qtd_con = st.session_state.contrato_comercial.get(dispositivo, 0)
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
    stock = st.session_state.contrato_comercial.copy()

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

# --- NOTAS + CHECKLIST INTERATIVO ---
st.write("### 🚨 Regras Técnicas de Instalação")
st.info("""
📐 Regras Técnicas de Instalação:
- Altura Recomendada: 2.10m a 2.40m.
- Proteção Solar: Evitar luz solar direta.
- Fixação Anti-Sabotagem Obrigatória: parafusos de tamper.
""")

st.subheader("✅ Checklist Final de Instalação")
st.markdown(
    "- 📱 Painel principal fixado com parafusos de tamper<br>"
    "- 🔍 Todos os sensores testados e com cobertura verificada<br>"
    "- 🪟 Contactos magnéticos alinhados e com gap < 5mm<br>"
    "- 📞 Comunicação com a Central validada<br>"
    "- 👥 Cliente treinado no uso da app/painel",
    unsafe_allow_html=True
)

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
