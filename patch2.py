with open('/home/ubuntu/nexorahub_dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("File size:", len(content))

# 7. Update HTML tab estrutura
old_html = '''  <!-- ESTRUTURA DE CUSTOS (Nexora Hub Mae) -->
  <div id="tab-estrutura" class="tab-content">'''

# Find the tab-estrutura section
idx_start = content.find('  <!-- ESTRUTURA DE CUSTOS (Nexora Hub M')
idx_end = content.find('\n  <!-- VISÃO GERAL EMPRESAS FILHAS -->', idx_start)
print(f"HTML section: {idx_start} to {idx_end}")

if idx_start > 0 and idx_end > 0:
    new_html_section = '''  <!-- ESTRUTURA DE CUSTOS (Nexora Hub Mae) -->
  <div id="tab-estrutura" class="tab-content">
    <div class="page-title">Estrutura de Custos — Nexora Hub <span class="saving" id="saving-estr">Salvando...</span></div>
    <div class="page-sub">Custos gerais de manutencao da empresa mae Nexora Hub. Periodo operacional: <strong>01/04/2025</strong> em diante.</div>

    <div class="caixa-block">
      <div class="caixa-input-wrap">
        <div class="caixa-label">Caixa Inicial do Grupo (R$)</div>
        <div class="caixa-desc">Saldo em 01/04/2025 (capital proprio)</div>
        <input class="caixa-inp" type="number" id="caixa-inicial" placeholder="Ex: 500000" oninput="saveEstrutura()" />
      </div>
      <div class="caixa-input-wrap">
        <div class="caixa-label">Inicio da Operacao</div>
        <div class="caixa-desc">Data de abertura do periodo</div>
        <div style="color:#fff;font-family:sans-serif;font-size:20px;font-weight:700;padding:10px 14px;background:rgba(255,255,255,0.08);border-radius:8px;border:1px solid rgba(30,111,255,0.4);">01/04/2025</div>
      </div>
      <div class="caixa-cards" id="caixa-cards"></div>
    </div>
    <div class="info-box">Caixa Atual = Caixa Inicial + Aportes Acumulados + Resultado Acumulado - Custos de Estrutura Acumulados (Abr-Dez)</div>

    <div class="section-title"><span>Aportes de Capital por Mes</span></div>
    <p style="color:#6B7280;font-size:12px;margin:-8px 0 10px;">Entradas de capital externo. Meses Jan/Fev/Mar = pre-operacao (bloqueados).</p>
    <div class="table-wrap" style="overflow-x:auto;margin-bottom:22px;">
      <table style="min-width:900px;">
        <thead><tr>
          <th>Tipo</th>
          <th style="color:rgba(255,255,255,0.4)">Jan</th><th style="color:rgba(255,255,255,0.4)">Fev</th><th style="color:rgba(255,255,255,0.4)">Mar</th>
          <th>Abr</th><th>Mai</th><th>Jun</th><th>Jul</th>
          <th>Ago</th><th>Set</th><th>Out</th><th>Nov</th><th>Dez</th>
          <th>Total</th>
        </tr></thead>
        <tbody id="aportes-table"></tbody>
      </table>
    </div>

    <div class="section-title"><span>Gestao de Custos Mes a Mes</span></div>
    <p style="color:#6B7280;font-size:12px;margin:-8px 0 12px;">Coluna <strong>Base</strong> = valor padrao. Preencha o mes para sobrescrever. Fundo amarelo = valor personalizado. Jan/Fev/Mar = bloqueados.</p>
    <div class="table-wrap" style="overflow-x:auto;margin-bottom:22px;">
      <table style="min-width:1200px;">
        <thead><tr>
          <th>Categoria</th>
          <th style="background:#1E3A5F;color:#7DD3FC;min-width:100px;">Base Mensal</th>
          <th style="background:#1a1a2e;color:rgba(255,255,255,0.3);">Jan</th>
          <th style="background:#1a1a2e;color:rgba(255,255,255,0.3);">Fev</th>
          <th style="background:#1a1a2e;color:rgba(255,255,255,0.3);">Mar</th>
          <th>Abr</th><th>Mai</th><th>Jun</th><th>Jul</th>
          <th>Ago</th><th>Set</th><th>Out</th><th>Nov</th><th>Dez</th>
          <th>Total Acum.</th>
        </tr></thead>
        <tbody id="custo-mensal-table"></tbody>
        <tfoot><tr id="custo-mensal-total"></tr></tfoot>
      </table>
    </div>

    <div class="two-col">
      <div>
        <div class="section-title"><span>Investimento Inicial</span></div>
        <p style="color:#6B7280;font-size:12px;margin:-8px 0 10px;">Gastos unicos de estruturacao (nao recorrentes).</p>
        <div class="table-wrap">
          <table><thead><tr><th>Categoria</th><th>Valor Gasto (R$)</th></tr></thead>
          <tbody id="inv-table"></tbody></table>
        </div>
        <div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:8px;padding:9px 14px;margin-top:10px;font-size:11px;color:#92400E;">
          O investimento inicial e apenas um registro historico e nao e deduzido automaticamente do caixa.
        </div>
      </div>
      <div>
        <div class="section-title"><span>Resumo Financeiro do Grupo</span></div>
        <div class="kpi-grid" id="estr-summary-cards"></div>
        <div style="background:#fff;border-radius:12px;border:1px solid #E5E7EB;padding:18px;margin-top:14px;">
          <div style="font-family:sans-serif;font-weight:700;font-size:13px;margin-bottom:12px;color:#111827;">Metas Globais</div>
          <div style="display:flex;flex-direction:column;gap:10px;">
            <div>
              <label style="font-size:11px;color:#6B7280;font-weight:600;display:block;margin-bottom:4px;">Runway Minimo (meses)</label>
              <input class="inp" type="number" id="meta-runway" value="6" oninput="saveEstrutura()" />
            </div>
            <div>
              <label style="font-size:11px;color:#6B7280;font-weight:600;display:block;margin-bottom:4px;">Margem Minima (ex: 0.15 = 15%)</label>
              <input class="inp" type="number" step="0.01" id="meta-margem" value="0.15" oninput="saveEstrutura()" />
            </div>
            <div>
              <label style="font-size:11px;color:#6B7280;font-weight:600;display:block;margin-bottom:4px;">Burn Rate Maximo (R$)</label>
              <input class="inp" type="number" id="meta-burnrate" value="0" oninput="saveEstrutura()" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
'''
    content = content[:idx_start] + new_html_section + content[idx_end:]
    print("7. HTML tab estrutura updated OK")
else:
    print("7. HTML section not found")

# 8. Replace renderEstrutura function
idx_rf = content.find("function renderEstrutura(totals) {")
idx_rf_end = content.find("\n// ─── VISÃO GERAL EMPRESAS FILHAS", idx_rf)
if idx_rf < 0:
    idx_rf_end = content.find("\n// ─── VISÃO GERAL", idx_rf)
print(f"renderEstrutura: {idx_rf} to {idx_rf_end}")

if idx_rf > 0 and idx_rf_end > 0:
    new_render = '''function renderEstrutura(totals) {
  const { caixaAtual, resultadoAcum, totalCusto, totalCustoAcum, totalInv, totalAportes } = totals;
  const ci = estrutura.caixa_inicial||0;
  const MONTHS_ALL = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
  const MONTHS_OP = ['Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];

  const ciEl = document.getElementById('caixa-inicial');
  if (ciEl && document.activeElement!==ciEl) ciEl.value = ci||'';

  const mt = estrutura.metas;
  const ri=document.getElementById('meta-runway'), mi=document.getElementById('meta-margem'), bi=document.getElementById('meta-burnrate');
  if(ri&&document.activeElement!==ri) ri.value=mt.runway||6;
  if(mi&&document.activeElement!==mi) mi.value=mt.margem||0.15;
  if(bi&&document.activeElement!==bi) bi.value=mt.burnRateMax||0;

  document.getElementById('caixa-cards').innerHTML = [
    {label:'Caixa Inicial (01/04)', val:fmt(ci), color:'#1E6FFF'},
    {label:'Aportes Acumulados', val:fmt(totalAportes), color:'#8B5CF6'},
    {label:'Resultado Acumulado', val:fmt(resultadoAcum), color:resultadoAcum>=0?'#10B981':'#EF4444'},
    {label:'Custos Estrutura Acum.', val:fmt(totalCustoAcum), color:'#F59E0B'},
    {label:'Caixa Atual Estimado', val:fmt(caixaAtual), color:caixaAtual>=0?'#10B981':'#EF4444'},
  ].map(({label,val,color})=>`
    <div class="caixa-mini" style="border-left:3px solid ${color}">
      <div class="caixa-mini-label">${label}</div>
      <div class="caixa-mini-val" style="color:${color}">${val}</div>
    </div>`).join('');

  // Tabela de aportes
  let aportesAccum = 0;
  document.getElementById('aportes-table').innerHTML =
    `<tr><td><strong>Aporte (R$)</strong></td>` +
    MONTHS_ALL.map(mm=>{
      const isOp = MONTHS_OP.includes(mm);
      const val = estrutura.aportes?.[mm]||'';
      return `<td style="padding:4px 6px;background:${isOp?'':'#F9FAFB'}">
        <input class="inp" type="number" value="${val}" style="width:80px;${isOp?'':'background:#F3F4F6;color:#9CA3AF;'}"
          ${isOp?`oninput="estrutura.aportes['${mm}']=parseFloat(this.value)||0;saveEstrutura()"`:' disabled'}
        /></td>`;
    }).join('') +
    `<td style="font-weight:700;color:#8B5CF6">${fmt(MONTHS_ALL.reduce((a,mm)=>a+(estrutura.aportes?.[mm]||0),0))}</td></tr>` +
    `<tr style="background:#F0FDF4"><td style="color:#059669;font-weight:600">Acumulado</td>` +
    MONTHS_ALL.map(mm=>{
      aportesAccum += (estrutura.aportes?.[mm]||0);
      const isOp = MONTHS_OP.includes(mm);
      return `<td style="color:${isOp?'#059669':'#9CA3AF'};font-weight:600">${fmt(aportesAccum)}</td>`;
    }).join('') +
    `<td></td></tr>`;

  // Tabela de custos mes a mes
  const custosRows = CUSTO_CATS.map((cat,rIdx)=>{
    const base = estrutura.custos_mensais[cat]||0;
    const totalAcumCat = MONTHS_OP.reduce((a,mm)=>a+getCustoMes(mm,cat),0);
    return `<tr style="background:${rIdx%2===0?'#FAFAFA':'#fff'}">
      <td style="font-weight:500">${cat}</td>
      <td style="padding:4px 8px;background:#EFF6FF;">
        <input class="inp" type="number" value="${base||''}" style="width:90px;background:#EFF6FF;"
          oninput="estrutura.custos_mensais['${cat}']=parseFloat(this.value)||0;saveEstrutura()" />
      </td>` +
      MONTHS_ALL.map(mm=>{
        const isOp = MONTHS_OP.includes(mm);
        const override = estrutura.custos_por_mes?.[mm]?.[cat];
        const hasOverride = override !== undefined && override !== null && override !== '';
        const displayVal = hasOverride ? override : '';
        return `<td style="padding:4px 6px;background:${!isOp?'#F3F4F6':(hasOverride?'#FFFBEB':'')}">
          <input class="inp" type="number" value="${displayVal}" placeholder="${isOp?base:''}"
            style="width:80px;${!isOp?'background:#F3F4F6;color:#9CA3AF;':(hasOverride?'background:#FFFBEB;border-color:#F59E0B;':'')}"
            ${isOp?`oninput="updateCustoMes('${mm}','${cat}',this.value)"`:' disabled'}
          /></td>`;
      }).join('') +
      `<td style="font-weight:700;color:#F59E0B">${fmt(totalAcumCat)}</td>
    </tr>`;
  }).join('');

  const totalBase = CUSTO_CATS.reduce((a,k)=>a+(estrutura.custos_mensais[k]||0),0);
  const totalPorMes = MONTHS_ALL.map(mm=>MONTHS_OP.includes(mm)?getTotalCustoMes(mm):0);
  const totalAcumGeral = totalPorMes.reduce((a,v)=>a+v,0);

  document.getElementById('custo-mensal-table').innerHTML = custosRows;
  document.getElementById('custo-mensal-total').innerHTML =
    `<td style="background:#0A1628;color:#fff;font-weight:700;padding:8px 12px;">TOTAL</td>` +
    `<td style="background:#1E3A5F;color:#7DD3FC;font-weight:700;padding:8px 12px;">${fmt(totalBase)}</td>` +
    MONTHS_ALL.map((mm,i)=>{
      const isOp = MONTHS_OP.includes(mm);
      const v = totalPorMes[i];
      return `<td style="background:${isOp?'#0A1628':'#1a1a2e'};color:${isOp?'#1E6FFF':'rgba(255,255,255,0.2)'};font-weight:700;padding:8px 12px;">${isOp?fmt(v):'\u2014'}</td>`;
    }).join('') +
    `<td style="background:#0A1628;color:#F59E0B;font-weight:700;padding:8px 12px;">${fmt(totalAcumGeral)}</td>`;

  document.getElementById('inv-table').innerHTML = INV_CATS.map((k,i)=>`
    <tr style="background:${i%2===0?'#FAFAFA':'#fff'}">
      <td>${k}</td>
      <td style="padding:5px 8px"><input class="inp" type="number" value="${estrutura.investimento[k]||''}"
        oninput="estrutura.investimento['${k}']=parseFloat(this.value)||0;saveEstrutura()" /></td>
    </tr>`).join('') +
    `<tr class="table-total"><td>TOTAL INVESTIDO</td><td>${fmt(totalInv)}</td></tr>`;

  const rwSemReceita = totalBase>0?`${fmtNum(ci/totalBase)} m`:'\u221e';
  document.getElementById('estr-summary-cards').innerHTML = [
    kpiCard('Caixa Inicial', fmt(ci), '01/04/2025', '#1E6FFF'),
    kpiCard('Aportes Acumulados', fmt(totalAportes), 'capital externo', '#8B5CF6'),
    kpiCard('Custo Base Mensal', fmt(totalBase), 'estrutura central', '#F59E0B'),
    kpiCard('Custo Acumulado', fmt(totalCustoAcum), 'Abr-Dez', '#EF4444'),
    kpiCard('Caixa Atual', fmt(caixaAtual), '', caixaAtual>=0?'#10B981':'#EF4444'),
    kpiCard('Runway', `${fmtNum(totals.runway)} m`, 'so custo fixo', '#1E6FFF'),
  ].join('');
}

function updateCustoMes(mes, cat, val) {
  if (!estrutura.custos_por_mes) estrutura.custos_por_mes = {};
  if (!estrutura.custos_por_mes[mes]) estrutura.custos_por_mes[mes] = {};
  if (val === '' || val === null || val === undefined) {
    delete estrutura.custos_por_mes[mes][cat];
  } else {
    estrutura.custos_por_mes[mes][cat] = parseFloat(val)||0;
  }
  saveEstrutura();
}
'''
    content = content[:idx_rf] + new_render + content[idx_rf_end:]
    print("8. renderEstrutura updated OK")
else:
    print("8. renderEstrutura section not found")

# 9. Update toast
old_toast = "toast('Nexora Hub v2.0 carregado"
if old_toast in content:
    idx_toast = content.find(old_toast)
    idx_toast_end = content.find("');", idx_toast) + 3
    content = content[:idx_toast] + "toast('Nexora Hub v3.0 — Periodo: 01/04/2025 | 11 empresas ativas!');" + content[idx_toast_end:]
    print("9. Toast updated OK")
else:
    print("9. Toast not found")

with open('/home/ubuntu/nexorahub_dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"File saved OK, size: {len(content)}")
