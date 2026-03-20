with open('/home/ubuntu/nexorahub_dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''// ─── ESTRUTURA ───────────────────────────────────────────────────────────────
function renderEstrutura(totals) {
  const { caixaAtual, resultadoAcum, totalCusto, totalInv } = totals;
  const ci = estrutura.caixa_inicial||0;

  const ciEl = document.getElementById('caixa-inicial');
  if (ciEl && document.activeElement!==ciEl) ciEl.value = ci||'';

  document.getElementById('caixa-cards').innerHTML = [
    {label:'Caixa Inicial', val:fmt(ci), color:'#1E6FFF'},
    {label:'Resultado Acumulado', val:fmt(resultadoAcum), color:resultadoAcum>=0?'#10B981':'#EF4444'},
    {label:'Custos Estrutura (ano)', val:fmt(totalCusto*12), color:'#F59E0B'},
    {label:'Caixa Atual Estimado', val:fmt(caixaAtual), color:caixaAtual>=0?'#10B981':'#EF4444'},
  ].map(({label,val,color})=>`
    <div class="caixa-mini" style="border-left:3px solid ${color}">
      <div class="caixa-mini-label">${label}</div>
      <div class="caixa-mini-val" style="color:${color}">${val}</div>
    </div>`).join('');

  document.getElementById('inv-table').innerHTML = INV_CATS.map((k,i)=>`
    <tr style="background:${i%2===0?'#FAFAFA':'#fff'}">
      <td>${k}</td>
      <td style="padding:5px 8px"><input class="inp" type="number" value="${estrutura.investimento[k]||''}"
        oninput="estrutura.investimento['${k}']=parseFloat(this.value)||0;saveEstrutura()" /></td>
    </tr>`).join('') +
    `<tr class="table-total"><td>TOTAL INVESTIDO</td><td>${fmt(totalInv)}</td></tr>`;

  document.getElementById('custo-table').innerHTML = CUSTO_CATS.map((k,i)=>`
    <tr style="background:${i%2===0?'#FAFAFA':'#fff'}">
      <td>${k}</td>
      <td style="padding:5px 8px"><input class="inp" type="number" value="${estrutura.custos_mensais[k]||''}"
        oninput="estrutura.custos_mensais['${k}']=parseFloat(this.value)||0;saveEstrutura()" /></td>
    </tr>`).join('') +
    `<tr class="table-total"><td>TOTAL MENSAL</td><td>${fmt(totalCusto)}</td></tr>`;

  const rwSemReceita = totalCusto>0?`${fmtNum(ci/totalCusto)} m`:'\u221e';
  document.getElementById('estr-summary-cards').innerHTML = [
    kpiCard('Custo Mensal', fmt(totalCusto), '', '#F59E0B'),
    kpiCard('Custo Anual', fmt(totalCusto*12), '', '#EF4444'),
    kpiCard('Runway s/ receita', rwSemReceita, 'só com custo fixo', '#1E6FFF'),
  ].join('');
}'''

new_func = '''// ─── ESTRUTURA ───────────────────────────────────────────────────────────────
function renderEstrutura(totals) {
  const { caixaAtual, resultadoAcum, totalCusto, totalCustoAcum, totalInv, totalAportes } = totals;
  const ci = estrutura.caixa_inicial||0;

  // Atualizar input caixa inicial
  const ciEl = document.getElementById('caixa-inicial');
  if (ciEl && document.activeElement!==ciEl) ciEl.value = ci||'';

  // Atualizar metas
  const m = estrutura.metas;
  const ri=document.getElementById('meta-runway'), mi=document.getElementById('meta-margem'), bi=document.getElementById('meta-burnrate');
  if(ri&&document.activeElement!==ri) ri.value=m.runway||6;
  if(mi&&document.activeElement!==mi) mi.value=m.margem||0.15;
  if(bi&&document.activeElement!==bi) bi.value=m.burnRateMax||0;

  // Cards de caixa
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

  // Tabela de aportes mensais
  const totalAportesAcum = MONTHS.reduce((a,mm)=>a+(estrutura.aportes?.[mm]||0),0);
  document.getElementById('aportes-table').innerHTML = `
    <tr>
      <td><strong>Aporte (R$)</strong></td>
      ${MONTHS.map(mm=>{
        const isOp = isMesOperacional(mm);
        const val = estrutura.aportes?.[mm]||'';
        return `<td style="padding:4px 6px;background:${isOp?'':'#F9FAFB'}">
          <input class="inp" type="number" value="${val}"
            style="width:90px;${isOp?'':'background:#F3F4F6;color:#9CA3AF;'}"
            ${isOp?`oninput="estrutura.aportes['${mm}']=parseFloat(this.value)||0;saveEstrutura()"`:' disabled'}
          /></td>`;
      }).join('')}
      <td style="font-weight:700;color:#8B5CF6">${fmt(totalAportesAcum)}</td>
    </tr>
    <tr style="background:#F0FDF4">
      <td style="color:#059669;font-weight:600">\ud83d\udcb9 Acumulado</td>
      ${MONTHS.reduce((acc,mm,i)=>{
        const soma = MONTHS.slice(0,i+1).reduce((s,x)=>s+(estrutura.aportes?.[x]||0),0);
        const isOp = isMesOperacional(mm);
        acc.push(`<td style="color:${isOp?'#059669':'#9CA3AF'};font-weight:600">${fmt(soma)}</td>`);
        return acc;
      },[]).join('')}
      <td></td>
    </tr>`;

  // Tabela de custos mes a mes
  const custosRows = CUSTO_CATS.map((cat,rIdx)=>{
    const base = estrutura.custos_mensais[cat]||0;
    const totalAcumCat = MONTHS_OPERACIONAIS.reduce((a,mm)=>a+getCustoMes(mm,cat),0);
    return `<tr style="background:${rIdx%2===0?'#FAFAFA':'#fff'}">
      <td style="font-weight:500">${cat}</td>
      <td style="padding:4px 8px;background:#EFF6FF;">
        <input class="inp" type="number" value="${base||''}" style="width:90px;background:#EFF6FF;"
          oninput="estrutura.custos_mensais['${cat}']=parseFloat(this.value)||0;saveEstrutura()" />
      </td>
      ${MONTHS.map(mm=>{
        const isOp = isMesOperacional(mm);
        const override = estrutura.custos_por_mes?.[mm]?.[cat];
        const hasOverride = override !== undefined && override !== null && override !== '';
        const displayVal = hasOverride ? override : '';
        return `<td style="padding:4px 6px;background:${!isOp?'#F3F4F6':(hasOverride?'#FFFBEB':'')}">
          <input class="inp" type="number" value="${displayVal}"
            placeholder="${isOp?base:''}"
            style="width:85px;${!isOp?'background:#F3F4F6;color:#9CA3AF;':(hasOverride?'background:#FFFBEB;border-color:#F59E0B;':'')}"
            ${isOp?`oninput="updateCustoMes('${mm}','${cat}',this.value)"`:' disabled'}
          /></td>`;
      }).join('')}
      <td style="font-weight:700;color:#F59E0B">${fmt(totalAcumCat)}</td>
    </tr>`;
  }).join('');

  // Linha de totais
  const totalBase = CUSTO_CATS.reduce((a,k)=>a+(estrutura.custos_mensais[k]||0),0);
  const totalPorMes = MONTHS.map(mm=>isMesOperacional(mm)?getTotalCustoMes(mm):0);
  const totalAcumGeral = totalPorMes.reduce((a,v)=>a+v,0);

  document.getElementById('custo-mensal-table').innerHTML = custosRows;
  document.getElementById('custo-mensal-total').innerHTML =
    `<td style="background:#0A1628;color:#fff;font-weight:700;padding:8px 12px;">TOTAL</td>` +
    `<td style="background:#1E3A5F;color:#7DD3FC;font-weight:700;padding:8px 12px;">${fmt(totalBase)}</td>` +
    MONTHS.map((mm,i)=>{
      const isOp = isMesOperacional(mm);
      const v = totalPorMes[i];
      return `<td style="background:${isOp?'#0A1628':'#1a1a2e'};color:${isOp?'#1E6FFF':'rgba(255,255,255,0.2)'};font-weight:700;padding:8px 12px;">${isOp?fmt(v):'\u2014'}</td>`;
    }).join('') +
    `<td style="background:#0A1628;color:#F59E0B;font-weight:700;padding:8px 12px;">${fmt(totalAcumGeral)}</td>`;

  // Investimento
  document.getElementById('inv-table').innerHTML = INV_CATS.map((k,i)=>`
    <tr style="background:${i%2===0?'#FAFAFA':'#fff'}">
      <td>${k}</td>
      <td style="padding:5px 8px"><input class="inp" type="number" value="${estrutura.investimento[k]||''}"
        oninput="estrutura.investimento['${k}']=parseFloat(this.value)||0;saveEstrutura()" /></td>
    </tr>`).join('') +
    `<tr class="table-total"><td>TOTAL INVESTIDO</td><td>${fmt(totalInv)}</td></tr>`;

  // Resumo financeiro
  const rwSemReceita = totalBase>0?`${fmtNum(ci/totalBase)} m`:'\u221e';
  document.getElementById('estr-summary-cards').innerHTML = [
    kpiCard('Caixa Inicial', fmt(ci), '01/04/2025', '#1E6FFF'),
    kpiCard('Aportes Acumulados', fmt(totalAportes), 'capital externo', '#8B5CF6'),
    kpiCard('Custo Base Mensal', fmt(totalBase), 'estrutura central', '#F59E0B'),
    kpiCard('Custo Acumulado', fmt(totalCustoAcum), 'Abr\u2192Dez', '#EF4444'),
    kpiCard('Caixa Atual', fmt(caixaAtual), '', caixaAtual>=0?'#10B981':'#EF4444'),
    kpiCard('Runway', `${fmtNum(totals.runway)} m`, 'só custo fixo', '#1E6FFF'),
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
}'''

if old_func in content:
    content = content.replace(old_func, new_func, 1)
    print("SUCCESS: replaced renderEstrutura")
else:
    print("ERROR: old_func not found")

with open('/home/ubuntu/nexorahub_dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("File written successfully")
