import { useState, useEffect, useCallback } from "react";

const API = "/api/v1";

const http = {
  get: (p) => fetch(`${API}${p}`).then(r => r.json()),
  post: (p, b) => fetch(`${API}${p}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(b) }).then(r => r.json()),
  patch: (p, b) => fetch(`${API}${p}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(b) }).then(r => r.json()),
  del: (p) => fetch(`${API}${p}`, { method: "DELETE" }),
  upload: (p, file) => { const fd = new FormData(); fd.append("file", file); return fetch(`${API}${p}`, { method: "POST", body: fd }).then(r => r.json()); },
};

const T = {
  bg: "#0f172a", bgCard: "#1e293b", bgInput: "#0f172a",
  border: "#334155", borderLight: "#475569",
  text: "#f1f5f9", textS: "#94a3b8", textM: "#64748b",
  blue: "#3b82f6", blueD: "#1d4ed8", blueL: "#1e3a5f",
  green: "#22c55e", greenD: "#15803d", greenL: "#14532d",
  red: "#ef4444", redD: "#b91c1c", redL: "#450a0a",
  amber: "#f59e0b", amberD: "#b45309", amberL: "#451a03",
  purple: "#a855f7", purpleL: "#3b0764",
  cyan: "#06b6d4", cyanL: "#083344",
  accent: "#3b82f6",
};

const s = {
  card: { background: T.bgCard, border: `1px solid ${T.border}`, borderRadius: 12, padding: "1.25rem" },
  inp: { background: T.bgInput, border: `1px solid ${T.border}`, borderRadius: 8, padding: "9px 12px", fontSize: 14, color: T.text, width: "100%", boxSizing: "border-box", outline: "none", fontFamily: "inherit" },
  th: { padding: "10px 14px", textAlign: "left", fontSize: 12, fontWeight: 600, color: T.textM, background: T.bg, borderBottom: `1px solid ${T.border}`, letterSpacing: "0.05em", textTransform: "uppercase" },
  td: { padding: "11px 14px", borderBottom: `1px solid ${T.border}`, fontSize: 14, color: T.text },
  label: { fontSize: 12, color: T.textS, fontWeight: 500, display: "block", marginBottom: 5, letterSpacing: "0.04em", textTransform: "uppercase" },
};

function Btn({ children, onClick, v = "ghost", sm, disabled, full, style = {} }) {
  const vs = {
    ghost: { background: "transparent", color: T.text, border: `1px solid ${T.border}` },
    primary: { background: T.blue, color: "#fff", border: `1px solid ${T.blueD}` },
    success: { background: T.greenL, color: T.green, border: `1px solid ${T.greenD}` },
    danger: { background: T.redL, color: T.red, border: `1px solid ${T.redD}` },
    amber: { background: T.amberL, color: T.amber, border: `1px solid ${T.amberD}` },
  };
  return (
    <button onClick={onClick} disabled={disabled}
      style={{ ...(vs[v] || vs.ghost), padding: sm ? "5px 12px" : "9px 18px", borderRadius: 8, fontSize: sm ? 12 : 14, cursor: disabled ? "not-allowed" : "pointer", display: "inline-flex", alignItems: "center", gap: 7, fontFamily: "inherit", fontWeight: 500, opacity: disabled ? 0.45 : 1, width: full ? "100%" : "auto", justifyContent: full ? "center" : "flex-start", transition: "opacity 0.15s", ...style }}>
      {children}
    </button>
  );
}

function Badge({ children, color = "blue" }) {
  const m = {
    blue: [T.blueL, T.blue], green: [T.greenL, T.green],
    red: [T.redL, T.red], amber: [T.amberL, T.amber],
    purple: [T.purpleL, T.purple], cyan: [T.cyanL, T.cyan],
  };
  const [bg, fg] = m[color] || m.blue;
  return <span style={{ background: bg, color: fg, fontSize: 11, fontWeight: 700, padding: "3px 9px", borderRadius: 99, letterSpacing: "0.04em" }}>{children}</span>;
}

function Stat({ label, value, color = T.blue, sub }) {
  return (
    <div style={{ ...s.card, padding: "1rem" }}>
      <p style={{ margin: "0 0 6px", fontSize: 11, color: T.textM, fontWeight: 600, letterSpacing: "0.07em", textTransform: "uppercase" }}>{label}</p>
      <p style={{ margin: 0, fontSize: 28, fontWeight: 700, color, lineHeight: 1 }}>{value}</p>
      {sub && <p style={{ margin: "6px 0 0", fontSize: 12, color: T.textS }}>{sub}</p>}
    </div>
  );
}

function Modal({ title, onClose, children, width = 520 }) {
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.65)", zIndex: 1000, display: "flex", alignItems: "center", justifyContent: "center", padding: "1rem" }}
      onClick={e => e.target === e.currentTarget && onClose()}>
      <div style={{ ...s.card, width, maxHeight: "88vh", overflowY: "auto", boxShadow: "0 25px 80px rgba(0,0,0,0.6)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.25rem", paddingBottom: "1rem", borderBottom: `1px solid ${T.border}` }}>
          <h2 style={{ margin: 0, fontSize: 17, fontWeight: 700, color: T.text }}>{title}</h2>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", color: T.textS, fontSize: 22, lineHeight: 1, padding: 0 }}>×</button>
        </div>
        {children}
      </div>
    </div>
  );
}

function Confirm({ msg, onOk, onCancel }) {
  return (
    <Modal title="Confirmar ação" onClose={onCancel} width={400}>
      <p style={{ color: T.textS, marginBottom: "1.5rem", lineHeight: 1.7, fontSize: 14 }}>{msg}</p>
      <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
        <Btn onClick={onCancel}>Cancelar</Btn>
        <Btn v="danger" onClick={onOk}>Confirmar</Btn>
      </div>
    </Modal>
  );
}

function Toast({ message, type, onClose }) {
  useEffect(() => { const t = setTimeout(onClose, 3500); return () => clearTimeout(t); }, [onClose]);
  const m = { success: [T.greenL, T.green], error: [T.redL, T.red], info: [T.blueL, T.blue] };
  const [bg, fg] = m[type] || m.info;
  return (
    <div style={{ position: "fixed", bottom: 24, right: 24, background: bg, color: fg, border: `1px solid ${fg}`, borderRadius: 10, padding: "13px 18px", fontSize: 14, fontWeight: 600, zIndex: 9999, maxWidth: 380, boxShadow: "0 8px 32px rgba(0,0,0,0.4)", display: "flex", alignItems: "center", gap: 10 }}>
      {type === "success" ? "✓" : type === "error" ? "✕" : "ℹ"} {message}
    </div>
  );
}

function Field({ label, children, half }) {
  return (
    <div style={{ marginBottom: "1rem", gridColumn: half ? "span 1" : "span 2" }}>
      <label style={s.label}>{label}</label>
      {children}
    </div>
  );
}

function Inp(props) { return <input style={{ ...s.inp, ...(props.style || {}) }} {...props} />; }
function Sel({ children, ...props }) { return <select style={{ ...s.inp, ...(props.style || {}) }} {...props}>{children}</select>; }

function BarChart({ data, xKey, yKey, color = T.blue }) {
  if (!data?.length) return <p style={{ color: T.textM, fontSize: 13, margin: "1rem 0 0" }}>Sem dados para exibir.</p>;
  const max = Math.max(...data.map(d => d[yKey]), 1);
  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: 5, height: 130, marginTop: "1.25rem", paddingBottom: 22, position: "relative" }}>
      {data.map((d, i) => (
        <div key={i} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", height: "100%", justifyContent: "flex-end", gap: 4 }}>
          <span style={{ fontSize: 10, color: T.textS, fontWeight: 600 }}>{d[yKey]}</span>
          <div style={{ width: "100%", background: color, borderRadius: "4px 4px 0 0", height: `${Math.max((d[yKey] / max) * 100, 3)}%`, opacity: 0.8 }} />
          <span style={{ fontSize: 9, color: T.textM, position: "absolute", bottom: 0, maxWidth: 50, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", textAlign: "center" }}>{d[xKey]}</span>
        </div>
      ))}
    </div>
  );
}

// ── DASHBOARD ────────────────────────────────────────────────────────────────
function Dashboard({ setores, funcionarios }) {
  const ativos = funcionarios.filter(f => f.ativo).length;
  const inativos = funcionarios.length - ativos;
  return (
    <div>
      <div style={{ marginBottom: "1.75rem" }}>
        <h1 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 700, color: T.text }}>Dashboard</h1>
        <p style={{ margin: 0, fontSize: 14, color: T.textS }}>Visão geral do sistema de RH</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: "1.5rem" }}>
        <Stat label="Setores" value={setores.length} color={T.blue} />
        <Stat label="Funcionários ativos" value={ativos} color={T.green} />
        <Stat label="Inativos" value={inativos} color={T.red} />
        <Stat label="Total" value={funcionarios.length} color={T.purple} />
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: 16 }}>
        <div style={s.card}>
          <p style={{ margin: "0 0 1.25rem", fontSize: 14, fontWeight: 600, color: T.text }}>Distribuição por setor</p>
          {setores.length === 0
            ? <p style={{ color: T.textM, fontSize: 13 }}>Nenhum setor cadastrado ainda.</p>
            : setores.map(sec => {
              const cnt = funcionarios.filter(f => f.setor_id === sec.id && f.ativo).length;
              const pct = ativos > 0 ? Math.round((cnt / ativos) * 100) : 0;
              return (
                <div key={sec.id} style={{ marginBottom: 14 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                    <span style={{ fontSize: 13, color: T.text, fontWeight: 500 }}>{sec.nome}</span>
                    <span style={{ fontSize: 12, color: T.textS }}>{cnt} · {pct}%</span>
                  </div>
                  <div style={{ height: 5, background: T.border, borderRadius: 99 }}>
                    <div style={{ height: "100%", width: `${pct}%`, background: T.blue, borderRadius: 99, transition: "width 0.5s" }} />
                  </div>
                </div>
              );
            })
          }
        </div>
        <div style={s.card}>
          <p style={{ margin: "0 0 1.25rem", fontSize: 14, fontWeight: 600, color: T.text }}>Status</p>
          {[
            { label: "Ativos", val: ativos, color: T.green },
            { label: "Inativos", val: inativos, color: T.red },
          ].map(it => (
            <div key={it.label} style={{ display: "flex", alignItems: "center", gap: 12, padding: "13px 0", borderBottom: `1px solid ${T.border}` }}>
              <div style={{ width: 8, height: 8, borderRadius: 2, background: it.color, flexShrink: 0 }} />
              <span style={{ fontSize: 14, flex: 1, color: T.textS }}>{it.label}</span>
              <span style={{ fontWeight: 700, fontSize: 20, color: it.color }}>{it.val}</span>
              <span style={{ fontSize: 12, color: T.textM, minWidth: 36, textAlign: "right" }}>
                {funcionarios.length > 0 ? Math.round((it.val / funcionarios.length) * 100) : 0}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── SETORES ──────────────────────────────────────────────────────────────────
function Setores({ setores, onRefresh, toast }) {
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState({ nome: "", descricao: "" });
  const [loading, setLoading] = useState(false);

  const criar = async () => {
    setLoading(true);
    try {
      const res = await http.post("/setores/", form);
      if (res.id) { toast("Setor criado com sucesso!", "success"); onRefresh(); setModal(false); setForm({ nome: "", descricao: "" }); }
      else toast(res.detail || "Erro ao criar setor.", "error");
    } catch { toast("Erro de conexão.", "error"); }
    setLoading(false);
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1.75rem" }}>
        <div>
          <h1 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 700, color: T.text }}>Setores</h1>
          <p style={{ margin: 0, fontSize: 14, color: T.textS }}>{setores.length} setor{setores.length !== 1 ? "es" : ""} cadastrado{setores.length !== 1 ? "s" : ""}</p>
        </div>
        <Btn v="primary" onClick={() => setModal(true)}>
          <i className="ti ti-plus" aria-hidden="true" /> Novo setor
        </Btn>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 14 }}>
        {setores.map(sec => (
          <div key={sec.id} style={{ ...s.card, display: "flex", flexDirection: "column", gap: 12 }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div style={{ width: 42, height: 42, borderRadius: 10, background: T.blueL, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <i className="ti ti-building" style={{ fontSize: 20, color: T.blue }} aria-hidden="true" />
              </div>
              <Badge color={sec.ativo ? "green" : "red"}>{sec.ativo ? "Ativo" : "Inativo"}</Badge>
            </div>
            <div>
              <p style={{ margin: "0 0 4px", fontWeight: 700, fontSize: 16, color: T.text }}>#{sec.id} · {sec.nome}</p>
              <p style={{ margin: 0, fontSize: 13, color: T.textS }}>{sec.descricao || "Sem descrição"}</p>
            </div>
          </div>
        ))}
        {setores.length === 0 && (
          <div style={{ ...s.card, gridColumn: "1 / -1", textAlign: "center", padding: "3rem" }}>
            <i className="ti ti-building-off" style={{ fontSize: 40, color: T.textM, display: "block", marginBottom: 12 }} aria-hidden="true" />
            <p style={{ color: T.textS, margin: 0 }}>Nenhum setor cadastrado ainda.</p>
          </div>
        )}
      </div>

      {modal && (
        <Modal title="Novo setor" onClose={() => setModal(false)}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0 14px" }}>
            <Field label="Nome *" half={false}>
              <Inp value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))} placeholder="Ex: Tecnologia da Informação" autoFocus />
            </Field>
            <Field label="Descrição" half={false}>
              <textarea value={form.descricao} onChange={e => setForm(f => ({ ...f, descricao: e.target.value }))} rows={3} style={{ ...s.inp, resize: "vertical" }} placeholder="Descrição opcional..." />
            </Field>
          </div>
          <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 8 }}>
            <Btn onClick={() => setModal(false)}>Cancelar</Btn>
            <Btn v="primary" onClick={criar} disabled={loading || !form.nome.trim()}>{loading ? "Salvando..." : "Criar setor"}</Btn>
          </div>
        </Modal>
      )}
    </div>
  );
}

// ── FUNCIONÁRIOS ─────────────────────────────────────────────────────────────
function Funcionarios({ setores, funcionarios, onRefresh, toast }) {
  const [modal, setModal] = useState(null);
  const [confirm, setConfirm] = useState(null);
  const [fs, setFs] = useState("");
  const [fa, setFa] = useState("true");
  const [loading, setLoading] = useState(false);
  const ef = { nome: "", email: "", setor_id: "", cargo: "", data_admissao: "", horario_esperado_entrada: "08:00", horario_esperado_saida: "17:00" };
  const [form, setForm] = useState(ef);

  const abrirCriar = () => { setForm(ef); setModal("criar"); };
  const abrirEditar = (f) => {
    setForm({ nome: f.nome, email: f.email, setor_id: String(f.setor_id), cargo: f.cargo || "", data_admissao: f.data_admissao, horario_esperado_entrada: f.horario_esperado_entrada?.slice(0, 5) || "08:00", horario_esperado_saida: f.horario_esperado_saida?.slice(0, 5) || "17:00" });
    setModal(f);
  };

  const salvar = async () => {
    setLoading(true);
    try {
      if (modal === "criar") {
        const res = await http.post("/funcionarios/", { ...form, setor_id: parseInt(form.setor_id) });
        if (res.id) { toast("Funcionário criado!", "success"); onRefresh(); setModal(null); }
        else toast(res.detail || "Erro ao criar.", "error");
      } else {
        const body = {};
        if (form.nome !== modal.nome) body.nome = form.nome;
        if (form.cargo !== (modal.cargo || "")) body.cargo = form.cargo;
        if (parseInt(form.setor_id) !== modal.setor_id) body.setor_id = parseInt(form.setor_id);
        if (form.horario_esperado_entrada !== modal.horario_esperado_entrada?.slice(0, 5)) body.horario_esperado_entrada = form.horario_esperado_entrada;
        if (form.horario_esperado_saida !== modal.horario_esperado_saida?.slice(0, 5)) body.horario_esperado_saida = form.horario_esperado_saida;
        const res = await http.patch(`/funcionarios/${modal.id}`, body);
        if (res.id) { toast("Funcionário atualizado!", "success"); onRefresh(); setModal(null); }
        else toast(res.detail || "Erro ao atualizar.", "error");
      }
    } catch { toast("Erro de conexão.", "error"); }
    setLoading(false);
  };

  const desativar = async (id) => {
    try {
      await http.del(`/funcionarios/${id}`);
      toast("Funcionário desativado com sucesso.", "success"); onRefresh();
    } catch { toast("Erro ao desativar.", "error"); }
    setConfirm(null);
  };

  const nomeSetor = (id) => setores.find(sec => sec.id === id)?.nome || "—";

  const lista = funcionarios.filter(f => {
    if (fs && f.setor_id !== parseInt(fs)) return false;
    if (fa === "true" && !f.ativo) return false;
    if (fa === "false" && f.ativo) return false;
    return true;
  });

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "1.75rem" }}>
        <div>
          <h1 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 700, color: T.text }}>Funcionários</h1>
          <p style={{ margin: 0, fontSize: 14, color: T.textS }}>{lista.length} resultado{lista.length !== 1 ? "s" : ""}</p>
        </div>
        <Btn v="primary" onClick={abrirCriar}>
          <i className="ti ti-user-plus" aria-hidden="true" /> Novo funcionário
        </Btn>
      </div>

      <div style={{ display: "flex", gap: 10, marginBottom: "1.25rem" }}>
        <Sel value={fs} onChange={e => setFs(e.target.value)} style={{ width: 200 }}>
          <option value="">Todos os setores</option>
          {setores.map(sec => <option key={sec.id} value={sec.id}>{sec.nome}</option>)}
        </Sel>
        <Sel value={fa} onChange={e => setFa(e.target.value)} style={{ width: 140 }}>
          <option value="true">Ativos</option>
          <option value="false">Inativos</option>
          <option value="">Todos</option>
        </Sel>
      </div>

      <div style={{ ...s.card, padding: 0, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>{["#", "Nome", "E-mail", "Cargo", "Setor", "Admissão", "Horários", "Status", "Ações"].map((h, i) => <th key={i} style={s.th}>{h}</th>)}</tr>
          </thead>
          <tbody>
            {lista.map(f => (
              <tr key={f.id}
                style={{ transition: "background 0.1s" }}
                onMouseEnter={e => e.currentTarget.style.background = "rgba(255,255,255,0.03)"}
                onMouseLeave={e => e.currentTarget.style.background = ""}>
                <td style={{ ...s.td, color: T.textM, fontFamily: "monospace", fontSize: 12 }}>{f.id}</td>
                <td style={{ ...s.td, fontWeight: 600 }}>{f.nome}</td>
                <td style={{ ...s.td, color: T.textS, fontSize: 13 }}>{f.email}</td>
                <td style={{ ...s.td, color: T.textS }}>{f.cargo || <span style={{ color: T.textM }}>—</span>}</td>
                <td style={s.td}>{nomeSetor(f.setor_id)}</td>
                <td style={{ ...s.td, color: T.textS, fontSize: 13 }}>{f.data_admissao}</td>
                <td style={{ ...s.td, fontSize: 12, color: T.textS, fontFamily: "monospace" }}>{f.horario_esperado_entrada?.slice(0, 5)} — {f.horario_esperado_saida?.slice(0, 5)}</td>
                <td style={s.td}><Badge color={f.ativo ? "green" : "red"}>{f.ativo ? "Ativo" : "Inativo"}</Badge></td>
                <td style={s.td}>
                  <div style={{ display: "flex", gap: 6 }}>
                    <Btn sm onClick={() => abrirEditar(f)}>
                      <i className="ti ti-edit" aria-hidden="true" /> Editar
                    </Btn>
                    {f.ativo && (
                      <Btn sm v="danger" onClick={() => setConfirm(f)}>
                        <i className="ti ti-user-off" aria-hidden="true" /> Desativar
                      </Btn>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {lista.length === 0 && (
              <tr><td colSpan={9} style={{ ...s.td, textAlign: "center", padding: "3rem", color: T.textM }}>Nenhum funcionário encontrado.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {confirm && (
        <Confirm
          msg={`Deseja desativar "${confirm.nome}"? O histórico de ponto será preservado e ele pode ser reativado futuramente.`}
          onOk={() => desativar(confirm.id)}
          onCancel={() => setConfirm(null)}
        />
      )}

      {modal && (
        <Modal title={modal === "criar" ? "Novo funcionário" : `Editar · ${modal.nome}`} onClose={() => setModal(null)} width={580}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0 16px" }}>
            <Field label="Nome completo *" half>
              <Inp value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))} placeholder="Nome completo" />
            </Field>
            <Field label="E-mail *" half>
              <Inp type="email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} placeholder="email@empresa.com" disabled={modal !== "criar"} style={modal !== "criar" ? { opacity: 0.5 } : {}} />
            </Field>
            <Field label="Cargo" half>
              <Inp value={form.cargo} onChange={e => setForm(f => ({ ...f, cargo: e.target.value }))} placeholder="Ex: Analista de RH" />
            </Field>
            <Field label="Setor *" half>
              <Sel value={form.setor_id} onChange={e => setForm(f => ({ ...f, setor_id: e.target.value }))}>
                <option value="">Selecione um setor...</option>
                {setores.map(sec => <option key={sec.id} value={sec.id}>{sec.nome}</option>)}
              </Sel>
            </Field>
            <Field label="Data de admissão *" half>
              <Inp type="date" value={form.data_admissao} onChange={e => setForm(f => ({ ...f, data_admissao: e.target.value }))} disabled={modal !== "criar"} style={modal !== "criar" ? { opacity: 0.5 } : {}} />
            </Field>
            <div style={{ marginBottom: "1rem" }} />
            <Field label="Entrada esperada" half>
              <Inp type="time" value={form.horario_esperado_entrada} onChange={e => setForm(f => ({ ...f, horario_esperado_entrada: e.target.value }))} />
            </Field>
            <Field label="Saída esperada" half>
              <Inp type="time" value={form.horario_esperado_saida} onChange={e => setForm(f => ({ ...f, horario_esperado_saida: e.target.value }))} />
            </Field>
          </div>
          <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", paddingTop: "0.75rem", borderTop: `1px solid ${T.border}` }}>
            <Btn onClick={() => setModal(null)}>Cancelar</Btn>
            <Btn v="primary" onClick={salvar} disabled={loading || !form.nome.trim() || !form.setor_id}>
              {loading ? "Salvando..." : modal === "criar" ? "Criar funcionário" : "Salvar alterações"}
            </Btn>
          </div>
        </Modal>
      )}
    </div>
  );
}

// ── PONTO ────────────────────────────────────────────────────────────────────
function Ponto({ toast }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [drag, setDrag] = useState(false);

  const processar = async () => {
    if (!file) return;
    setLoading(true); setResultado(null);
    try {
      const res = await http.upload("/ponto/upload", file);
      setResultado(res);
      if (res.status === "concluido") toast(`${res.total_registros} registros processados!`, "success");
      else toast("Erro ao processar o CSV.", "error");
    } catch { toast("Erro de conexão.", "error"); }
    setLoading(false);
  };

  const onDrop = (e) => {
    e.preventDefault(); setDrag(false);
    const f = e.dataTransfer.files[0];
    if (f?.name.endsWith(".csv")) setFile(f);
    else toast("Apenas arquivos .csv são aceitos.", "error");
  };

  return (
    <div>
      <div style={{ marginBottom: "1.75rem" }}>
        <h1 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 700, color: T.text }}>Upload de ponto</h1>
        <p style={{ margin: 0, fontSize: 14, color: T.textS }}>Importe o arquivo CSV com os registros de entrada e saída</p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: "1.5rem" }}>
        <div style={s.card}>
          <p style={{ margin: "0 0 10px", fontSize: 13, fontWeight: 600, color: T.textS, letterSpacing: "0.05em", textTransform: "uppercase" }}>Formato do arquivo</p>
          <pre style={{ margin: 0, background: T.bg, padding: "12px 14px", borderRadius: 8, fontSize: 12, color: T.text, overflow: "auto", border: `1px solid ${T.border}`, lineHeight: 1.7 }}>
{`funcionario_id,nome,setor,data,hora_entrada,hora_saida
001,Ana Silva,TI,2026-05-01,08:05,17:10
002,Carlos Mendes,Financeiro,2026-05-01,09:20,18:00`}
          </pre>
        </div>
        <div style={s.card}>
          <p style={{ margin: "0 0 10px", fontSize: 13, fontWeight: 600, color: T.textS, letterSpacing: "0.05em", textTransform: "uppercase" }}>Regras de validação</p>
          {[
            "Data no formato YYYY-MM-DD",
            "Horários no formato HH:MM",
            "Funcionário deve existir no cadastro",
            "Campos em branco = falta no dia",
          ].map((r, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "7px 0", borderBottom: i < 3 ? `1px solid ${T.border}` : "none" }}>
              <i className="ti ti-check" style={{ fontSize: 14, color: T.green, flexShrink: 0 }} aria-hidden="true" />
              <span style={{ fontSize: 13, color: T.textS }}>{r}</span>
            </div>
          ))}
        </div>
      </div>

      <div
        onDragOver={e => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={onDrop}
        onClick={() => document.getElementById("csv-input").click()}
        style={{ border: `2px dashed ${drag ? T.blue : T.border}`, borderRadius: 14, padding: "3rem", textAlign: "center", marginBottom: "1rem", background: drag ? T.blueL : "rgba(255,255,255,0.02)", transition: "all 0.2s", cursor: "pointer" }}
      >
        <i className="ti ti-upload" style={{ fontSize: 44, color: drag ? T.blue : T.textM, display: "block", marginBottom: "1rem" }} aria-hidden="true" />
        <p style={{ margin: "0 0 6px", fontWeight: 700, fontSize: 16, color: T.text }}>Arraste o arquivo CSV aqui</p>
        <p style={{ margin: 0, fontSize: 13, color: T.textS }}>ou clique para selecionar do computador</p>
        <input type="file" accept=".csv" onChange={e => setFile(e.target.files[0])} style={{ display: "none" }} id="csv-input" />
      </div>

      {file && (
        <div style={{ ...s.card, marginBottom: "1rem" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{ width: 44, height: 44, background: T.blueL, borderRadius: 10, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
              <i className="ti ti-file-spreadsheet" style={{ fontSize: 22, color: T.blue }} aria-hidden="true" />
            </div>
            <div style={{ flex: 1 }}>
              <p style={{ margin: 0, fontWeight: 700, fontSize: 15, color: T.text }}>{file.name}</p>
              <p style={{ margin: 0, fontSize: 12, color: T.textM }}>{(file.size / 1024).toFixed(1)} KB · CSV</p>
            </div>
            <Btn v="primary" onClick={processar} disabled={loading}>
              <i className="ti ti-player-play" aria-hidden="true" />
              {loading ? "Processando..." : "Processar CSV"}
            </Btn>
            <Btn onClick={() => { setFile(null); setResultado(null); }}>
              <i className="ti ti-x" aria-hidden="true" />
            </Btn>
          </div>
        </div>
      )}

      {loading && (
        <div style={{ ...s.card, textAlign: "center", padding: "2rem" }}>
          <p style={{ color: T.textS, margin: 0 }}>Processando registros...</p>
        </div>
      )}

      {resultado && !loading && (
        <div style={s.card}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: "1.25rem", paddingBottom: "1rem", borderBottom: `1px solid ${T.border}` }}>
            <Badge color={resultado.status === "concluido" ? "green" : "red"}>{resultado.status.toUpperCase()}</Badge>
            <span style={{ fontSize: 13, color: T.textM }}>Upload #{resultado.upload_id}</span>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: resultado.erros?.length > 0 ? "1.25rem" : 0 }}>
            <Stat label="Registros processados" value={resultado.total_registros} color={T.green} />
            <Stat label="Período início" value={resultado.periodo_inicio || "—"} color={T.blue} />
            <Stat label="Período fim" value={resultado.periodo_fim || "—"} color={T.cyan} />
          </div>
          {resultado.erros?.length > 0 && (
            <div style={{ background: T.redL, border: `1px solid ${T.redD}`, borderRadius: 8, padding: "1rem" }}>
              <p style={{ margin: "0 0 10px", fontWeight: 700, color: T.red, fontSize: 14 }}>
                <i className="ti ti-alert-circle" aria-hidden="true" /> {resultado.erros.length} erro(s) encontrado(s)
              </p>
              <div style={{ maxHeight: 200, overflowY: "auto", display: "flex", flexDirection: "column", gap: 6 }}>
                {resultado.erros.map((e, i) => (
                  <p key={i} style={{ margin: 0, fontSize: 12, color: T.red }}>
                    <strong>Linha {e.linha}:</strong> {e.erro}
                  </p>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── RELATÓRIOS ───────────────────────────────────────────────────────────────
function Relatorios({ setores, toast }) {
  const [aba, setAba] = useState("setor");
  const [setorId, setSetorId] = useState("");
  const [mes, setMes] = useState(new Date().toISOString().slice(0, 7));
  const [loading, setLoading] = useState(false);
  const [relatorio, setRelatorio] = useState(null);
  const [comparativo, setComparativo] = useState(null);

  const buscarRelatorio = async () => {
    if (!setorId || !mes) return;
    setLoading(true); setRelatorio(null);
    try {
      const res = await http.get(`/relatorios/${setorId}?mes=${mes}`);
      if (res.setor) setRelatorio(res);
      else toast(res.detail || "Nenhum dado encontrado para esse período.", "error");
    } catch { toast("Erro de conexão.", "error"); }
    setLoading(false);
  };

  const buscarComparativo = async () => {
    if (!mes) return;
    setLoading(true); setComparativo(null);
    try {
      const res = await http.get(`/relatorios/comparativo/setores?mes=${mes}`);
      if (res.setores) setComparativo(res);
      else toast(res.detail || "Nenhum dado encontrado.", "error");
    } catch { toast("Erro de conexão.", "error"); }
    setLoading(false);
  };

  return (
    <div>
      <div style={{ marginBottom: "1.75rem" }}>
        <h1 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 700, color: T.text }}>Relatórios</h1>
        <p style={{ margin: 0, fontSize: 14, color: T.textS }}>Análise mensal de ponto por setor</p>
      </div>

      <div style={{ display: "flex", gap: 0, width: "fit-content", border: `1px solid ${T.border}`, borderRadius: 8, overflow: "hidden", marginBottom: "1.5rem" }}>
        {[{ id: "setor", label: "Por setor", icon: "ti-report" }, { id: "comparativo", label: "Comparativo", icon: "ti-chart-bar" }].map(t => (
          <button key={t.id} onClick={() => { setAba(t.id); setRelatorio(null); setComparativo(null); }}
            style={{ padding: "9px 20px", border: "none", cursor: "pointer", fontSize: 14, fontWeight: 600, background: aba === t.id ? T.blueL : T.bgCard, color: aba === t.id ? T.blue : T.textS, borderRight: `1px solid ${T.border}`, fontFamily: "inherit", display: "flex", alignItems: "center", gap: 7 }}>
            <i className={`ti ${t.icon}`} aria-hidden="true" /> {t.label}
          </button>
        ))}
      </div>

      <div style={{ display: "flex", gap: 10, marginBottom: "1.5rem", alignItems: "flex-end" }}>
        {aba === "setor" && (
          <div>
            <label style={s.label}>Setor</label>
            <Sel value={setorId} onChange={e => setSetorId(e.target.value)} style={{ width: 220 }}>
              <option value="">Selecione um setor...</option>
              {setores.map(sec => <option key={sec.id} value={sec.id}>{sec.nome}</option>)}
            </Sel>
          </div>
        )}
        <div>
          <label style={s.label}>Mês de referência</label>
          <Inp type="month" value={mes} onChange={e => setMes(e.target.value)} style={{ width: 180 }} />
        </div>
        <Btn v="primary" onClick={aba === "setor" ? buscarRelatorio : buscarComparativo} disabled={loading || (aba === "setor" && !setorId)}>
          <i className="ti ti-search" aria-hidden="true" />
          {loading ? "Gerando..." : "Gerar relatório"}
        </Btn>
      </div>

      {relatorio && (
        <div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 12, marginBottom: "1.5rem" }}>
            <Stat label="Funcionários" value={relatorio.resumo.total_funcionarios} color={T.blue} />
            <Stat label="Média horas" value={`${relatorio.resumo.media_horas_trabalhadas}h`} color={T.cyan} />
            <Stat label="Atrasos" value={relatorio.resumo.total_atrasos} color={T.amber} />
            <Stat label="Faltas" value={relatorio.resumo.total_faltas} color={T.red} />
            <Stat label="Horas extras" value={`${relatorio.resumo.total_horas_extras}h`} color={T.green} />
          </div>

          {relatorio.insight_llm && (
            <div style={{ ...s.card, marginBottom: "1.5rem", borderLeft: `3px solid ${T.blue}`, borderRadius: "0 12px 12px 0" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                <i className="ti ti-brain" style={{ fontSize: 15, color: T.blue }} aria-hidden="true" />
                <span style={{ fontSize: 11, fontWeight: 700, color: T.blue, letterSpacing: "0.08em", textTransform: "uppercase" }}>Análise da IA</span>
              </div>
              <p style={{ margin: 0, fontSize: 14, lineHeight: 1.8, color: T.textS }}>{relatorio.insight_llm}</p>
            </div>
          )}

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: "1.5rem" }}>
            <div style={s.card}>
              <p style={{ margin: "0 0 2px", fontWeight: 600, fontSize: 14, color: T.text }}>Média de horas por dia</p>
              <p style={{ margin: 0, fontSize: 12, color: T.textM }}>{relatorio.setor} · {relatorio.periodo}</p>
              <BarChart data={relatorio.grafico_horas_diarias} xKey="data" yKey="media_horas" color={T.blue} />
            </div>
            <div style={s.card}>
              <p style={{ margin: "0 0 2px", fontWeight: 600, fontSize: 14, color: T.text }}>Atrasos por semana</p>
              <p style={{ margin: 0, fontSize: 12, color: T.textM }}>{relatorio.setor} · {relatorio.periodo}</p>
              <BarChart data={relatorio.grafico_atrasos_por_semana} xKey="semana" yKey="total_atrasos" color={T.amber} />
            </div>
          </div>

          <div style={{ ...s.card, padding: 0, overflow: "hidden" }}>
            <div style={{ padding: "14px 16px", borderBottom: `1px solid ${T.border}`, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <p style={{ margin: 0, fontWeight: 600, fontSize: 14, color: T.text }}>Detalhamento por funcionário</p>
              <Badge color="blue">{relatorio.funcionarios.length} registros</Badge>
            </div>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead><tr>{["Nome", "Horas trabalhadas", "Atrasos", "Faltas", "Horas extras"].map((h, i) => <th key={i} style={s.th}>{h}</th>)}</tr></thead>
              <tbody>
                {relatorio.funcionarios.map(f => (
                  <tr key={f.funcionario_id}
                    onMouseEnter={e => e.currentTarget.style.background = "rgba(255,255,255,0.03)"}
                    onMouseLeave={e => e.currentTarget.style.background = ""}>
                    <td style={{ ...s.td, fontWeight: 600 }}>{f.nome}</td>
                    <td style={s.td}><span style={{ color: T.cyan, fontWeight: 600 }}>{f.horas_trabalhadas}h</span></td>
                    <td style={s.td}><Badge color={f.atrasos > 0 ? "amber" : "green"}>{f.atrasos}</Badge></td>
                    <td style={s.td}><Badge color={f.faltas > 0 ? "red" : "green"}>{f.faltas}</Badge></td>
                    <td style={s.td}><span style={{ color: T.green }}>{f.horas_extras}h</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {comparativo && (
        <div>
          <div style={{ ...s.card, marginBottom: "1.5rem" }}>
            <p style={{ margin: "0 0 2px", fontWeight: 600, fontSize: 14, color: T.text }}>Média de horas por setor</p>
            <p style={{ margin: 0, fontSize: 12, color: T.textM }}>{comparativo.periodo}</p>
            <BarChart data={comparativo.setores} xKey="setor" yKey="media_horas" color={T.blue} />
          </div>
          <div style={{ ...s.card, padding: 0, overflow: "hidden" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead><tr>{["Setor", "Média horas", "Atrasos", "Faltas", "Horas extras"].map((h, i) => <th key={i} style={s.th}>{h}</th>)}</tr></thead>
              <tbody>
                {comparativo.setores.map(sec => (
                  <tr key={sec.setor}
                    onMouseEnter={e => e.currentTarget.style.background = "rgba(255,255,255,0.03)"}
                    onMouseLeave={e => e.currentTarget.style.background = ""}>
                    <td style={{ ...s.td, fontWeight: 600 }}>{sec.setor}</td>
                    <td style={s.td}><span style={{ color: T.cyan, fontWeight: 600 }}>{sec.media_horas}h</span></td>
                    <td style={s.td}><Badge color={sec.total_atrasos > 5 ? "amber" : "green"}>{sec.total_atrasos}</Badge></td>
                    <td style={s.td}><Badge color={sec.total_faltas > 2 ? "red" : "green"}>{sec.total_faltas}</Badge></td>
                    <td style={s.td}><span style={{ color: T.green }}>{sec.total_horas_extras}h</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

// ── APP ──────────────────────────────────────────────────────────────────────
const NAV_ITEMS = [
  { id: "dashboard", icon: "ti-layout-dashboard", label: "Dashboard" },
  { id: "setores", icon: "ti-building", label: "Setores" },
  { id: "funcionarios", icon: "ti-users", label: "Funcionários" },
  { id: "ponto", icon: "ti-clock-upload", label: "Ponto" },
  { id: "relatorios", icon: "ti-chart-bar", label: "Relatórios" },
];

export default function App() {
  const [pagina, setPagina] = useState("dashboard");
  const [setores, setSetores] = useState([]);
  const [funcionarios, setFuncionarios] = useState([]);
  const [toastData, setToastData] = useState(null);
  const [apiOk, setApiOk] = useState(null);

  const toast = useCallback((message, type = "success") => setToastData({ message, type, id: Date.now() }), []);

  const loadSetores = useCallback(async () => {
    try { const r = await http.get("/setores/"); setSetores(r.setores || []); } catch {}
  }, []);

  const loadFuncionarios = useCallback(async () => {
    try { const r = await http.get("/funcionarios/?apenas_ativos=false&por_pagina=200"); setFuncionarios(r.funcionarios || []); } catch {}
  }, []);

  const refresh = useCallback(() => { loadSetores(); loadFuncionarios(); }, [loadSetores, loadFuncionarios]);

  useEffect(() => {
    fetch(`${API.replace("/api/v1", "")}/`).then(() => setApiOk(true)).catch(() => setApiOk(false));
    refresh();
  }, [refresh]);

  const pages = {
    dashboard: <Dashboard setores={setores} funcionarios={funcionarios} />,
    setores: <Setores setores={setores} onRefresh={refresh} toast={toast} />,
    funcionarios: <Funcionarios setores={setores} funcionarios={funcionarios} onRefresh={refresh} toast={toast} />,
    ponto: <Ponto toast={toast} />,
    relatorios: <Relatorios setores={setores} toast={toast} />,
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: T.bg, fontFamily: "'Segoe UI', system-ui, -apple-system, sans-serif", color: T.text }}>
      <nav style={{ width: 240, background: T.bgCard, borderRight: `1px solid ${T.border}`, display: "flex", flexDirection: "column", flexShrink: 0, position: "sticky", top: 0, height: "100vh" }}>
        <div style={{ padding: "1.5rem 1.25rem", borderBottom: `1px solid ${T.border}` }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{ width: 38, height: 38, borderRadius: 10, background: T.blueL, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <i className="ti ti-building-community" style={{ fontSize: 20, color: T.blue }} aria-hidden="true" />
            </div>
            <div>
              <p style={{ margin: 0, fontWeight: 700, fontSize: 15, color: T.text }}>Sistema RH</p>
              <p style={{ margin: 0, fontSize: 11, color: T.textM }}>v1.0.0</p>
            </div>
          </div>
        </div>

        {apiOk === false && (
          <div style={{ margin: "0.75rem 0.75rem 0", background: T.redL, border: `1px solid ${T.redD}`, borderRadius: 8, padding: "8px 12px" }}>
            <p style={{ margin: 0, fontSize: 11, color: T.red, fontWeight: 600 }}>
              <i className="ti ti-wifi-off" aria-hidden="true" /> API offline
            </p>
          </div>
        )}

        <div style={{ padding: "0.75rem", flex: 1 }}>
          {NAV_ITEMS.map(item => (
            <button key={item.id} onClick={() => setPagina(item.id)}
              style={{ display: "flex", alignItems: "center", gap: 11, padding: "10px 12px", border: "none", cursor: "pointer", textAlign: "left", fontSize: 14, fontWeight: 500, background: pagina === item.id ? T.blueL : "transparent", color: pagina === item.id ? T.blue : T.textS, borderRadius: 8, width: "100%", marginBottom: 2, fontFamily: "inherit", transition: "all 0.15s" }}>
              <i className={`ti ${item.icon}`} style={{ fontSize: 18 }} aria-hidden="true" />
              {item.label}
              {pagina === item.id && <div style={{ marginLeft: "auto", width: 5, height: 5, borderRadius: "50%", background: T.blue }} />}
            </button>
          ))}
        </div>

        <div style={{ padding: "1rem 1.25rem", borderTop: `1px solid ${T.border}` }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{ width: 6, height: 6, borderRadius: "50%", background: apiOk === true ? T.green : apiOk === false ? T.red : T.amber }} />
            <span style={{ fontSize: 12, color: T.textM }}>
              {apiOk === true ? "API conectada" : apiOk === false ? "API desconectada" : "Verificando..."}
            </span>
          </div>
          <p style={{ margin: "4px 0 0", fontSize: 11, color: T.textM }}>FastAPI · MySQL · React</p>
        </div>
      </nav>

      <main style={{ flex: 1, padding: "2rem 2.5rem", overflowY: "auto", minWidth: 0 }}>
        {pages[pagina]}
      </main>

      {toastData && (
        <Toast key={toastData.id} message={toastData.message} type={toastData.type} onClose={() => setToastData(null)} />
      )}
    </div>
  );
}
