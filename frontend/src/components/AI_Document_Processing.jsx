// 'use client';
// import React, { useState, useEffect, useRef, useCallback } from 'react';
// import AxiosInstance from "@/components/AxiosInstance";

// /* ─── Global styles - Black & Light Luxury Edition ─── */
// const GLOBAL_CSS = `
//   @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,500;1,600;1,700;1,800&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

//   *, *::before, *::after { box-sizing: border-box; }

//   :root {
//     /* ── Surfaces ── */
//     --page:        #f7f3ec;
//     --cream:       #faf7f1;
//     --cream-dark:  #efe9de;
//     --pure-white:  #ffffff;
//     --ivory:       #f5f0e6;
//     --platinum:    #eceae5;

//     /* ── Black (primary) ── */
//     --black:       #0a0a0a;
//     --black-soft:  #1a1a1a;
//     --black-hover: #262626;

//     /* ── Gold (hairlines & accents only) ── */
//     --gold:        #b8912f;
//     --gold-light:  #d8b95e;
//     --gold-dark:   #8f6f1c;
//     --gold-line:   rgba(184,145,47,0.22);

//     --surface:     #ffffff;
//     --surface-2:   #faf7f1;
//     --surface-3:   #f3ede2;
//     --border:      #e7dfd2;
//     --border-light:#f0e9dd;

//     /* ── All text is black ── */
//     --text-primary:   #0a0a0a;
//     --text-secondary: #333333;
//     --text-muted:     #6b6b6b;

//     /* ── Semantic accents (still colored for meaning) ── */
//     --emerald:  #0f9d6e;
//     --sapphire: #2563eb;
//     --ruby:     #dc2626;
//     --amber:    #d97706;
//     --violet:   #7c3aed;

//     --shadow-sm: 0 1px 2px rgba(10,10,10,0.04), 0 6px 18px -12px rgba(10,10,10,0.12);
//     --shadow-md: 0 2px 4px rgba(10,10,10,0.04), 0 18px 40px -24px rgba(10,10,10,0.22);
//     --shadow-lg: 0 30px 60px -30px rgba(10,10,10,0.28);
//   }

//   body { background: var(--page); }

//   .font-serif { font-family: 'Cormorant Garamond', Georgia, serif; }
//   .font-sans  { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
//   .font-mono  { font-family: 'JetBrains Mono', monospace; }

//   /* Subtle warm glow behind the page */
//   .page-bg {
//     background-color: var(--page);
//     background-image:
//       radial-gradient(1100px 520px at 50% -10%, rgba(184,145,47,0.11), transparent 62%),
//       radial-gradient(700px 400px at 100% 100%, rgba(184,145,47,0.05), transparent 60%);
//     background-repeat: no-repeat;
//     background-attachment: fixed;
//   }

//   ::-webkit-scrollbar { width: 6px; height: 6px; }
//   ::-webkit-scrollbar-track { background: var(--cream-dark); }
//   ::-webkit-scrollbar-thumb { background: #0a0a0a; border-radius: 6px; }
//   ::-webkit-scrollbar-thumb:hover { background: #333333; }

//   @keyframes fadeUp  { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
//   @keyframes fadeIn  { from{opacity:0} to{opacity:1} }
//   @keyframes spinCW  { to{transform:rotate(360deg)} }
//   @keyframes pulse   { 0%,100%{opacity:1} 50%{opacity:.5} }

//   .anim-fade-up { animation:fadeUp .4s cubic-bezier(0.2,0.8,0.4,1) forwards; }
//   .anim-fade-in { animation:fadeIn .3s ease forwards; }
//   .anim-spin    { animation:spinCW .7s linear infinite; }
//   .anim-pulse   { animation:pulse 2s ease infinite; }

//   /* ── Luxury Card ── */
//   .luxury-card {
//     position: relative;
//     background: linear-gradient(160deg, #ffffff 0%, #fdfbf7 100%);
//     border: 1px solid var(--border);
//     box-shadow: var(--shadow-sm);
//     transition: all 0.35s cubic-bezier(0.2,0.8,0.4,1);
//   }
//   .luxury-card::before {
//     content: '';
//     position: absolute;
//     top: 0; left: 0; right: 0;
//     height: 2px;
//     background: linear-gradient(90deg, transparent, var(--gold-line), transparent);
//     opacity: 0;
//     transition: opacity 0.35s ease;
//   }
//   .luxury-card:hover {
//     border-color: rgba(10,10,10,0.18);
//     transform: translateY(-2px);
//     box-shadow: var(--shadow-md);
//   }
//   .luxury-card:hover::before { opacity: 1; }

//   .gold-text {
//     background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 45%, var(--gold-dark) 100%);
//     -webkit-background-clip: text;
//     -webkit-text-fill-color: transparent;
//     background-clip: text;
//   }

//   /* ── Primary Button: Solid Black ── */
//   .btn-primary {
//     background: #0a0a0a;
//     color: #ffffff;
//     font-family: 'Inter', sans-serif;
//     font-weight: 700;
//     letter-spacing: 0.08em;
//     font-size: 0.72rem;
//     text-transform: uppercase;
//     border: 1px solid #0a0a0a;
//     cursor: pointer;
//     position: relative;
//     overflow: hidden;
//     transition: all 0.25s ease;
//     padding: 13px 28px;
//     border-radius: 2px;
//     box-shadow: 0 10px 22px -14px rgba(10,10,10,0.85), inset 0 1px 0 rgba(255,255,255,0.08);
//   }

//   .btn-primary::before {
//     content: '';
//     position: absolute;
//     top: 0; left: -120%;
//     width: 60%;
//     height: 100%;
//     background: linear-gradient(90deg, transparent, rgba(255,255,255,0.24), transparent);
//     transition: left 0.6s ease;
//   }

//   .btn-primary:hover::before { left: 130%; }
//   .btn-primary:hover {
//     background: #262626;
//     border-color: #262626;
//     color: #ffffff;
//     transform: translateY(-1px);
//     box-shadow: 0 16px 30px -16px rgba(10,10,10,0.9);
//   }
//   .btn-primary:active { transform: translateY(0); }
//   .btn-primary:disabled {
//     background: #d6d3cc;
//     border-color: #d6d3cc;
//     color: #8a8579;
//     cursor: not-allowed;
//     transform: none;
//     box-shadow: none;
//   }

//   /* ── Ghost Button: Black Outline ── */
//   .btn-ghost {
//     background: #ffffff;
//     color: #0a0a0a;
//     font-family: 'Inter', sans-serif;
//     font-weight: 700;
//     font-size: 0.7rem;
//     letter-spacing: 0.12em;
//     text-transform: uppercase;
//     border: 1px solid #0a0a0a;
//     cursor: pointer;
//     transition: all 0.2s;
//     padding: 11px 20px;
//     border-radius: 2px;
//   }
//   .btn-ghost:hover {
//     background: #0a0a0a;
//     color: #ffffff;
//     box-shadow: 0 12px 24px -14px rgba(10,10,10,0.9);
//   }
//   .btn-ghost:disabled {
//     opacity: 0.35;
//     cursor: not-allowed;
//     color: #0a0a0a;
//     border-color: #0a0a0a;
//     background: #ffffff;
//   }

//   /* ── Danger Button: Black (turns red on hover) ── */
//   .btn-danger {
//     background: #0a0a0a;
//     color: #ffffff;
//     font-family: 'Inter', sans-serif;
//     font-weight: 700;
//     font-size: 0.7rem;
//     letter-spacing: 0.12em;
//     text-transform: uppercase;
//     border: 1px solid #0a0a0a;
//     cursor: pointer;
//     transition: all 0.2s;
//     padding: 11px 20px;
//     border-radius: 2px;
//   }
//   .btn-danger:hover {
//     background: #dc2626;
//     border-color: #dc2626;
//     color: #ffffff;
//     box-shadow: 0 12px 24px -14px rgba(220,38,38,0.85);
//   }

//   /* ── Form Inputs ── */
//   .inp {
//     background: var(--surface-2);
//     border: 1px solid var(--border);
//     color: #0a0a0a;
//     font-family: 'Inter', sans-serif;
//     font-size: 0.85rem;
//     outline: none;
//     transition: all 0.2s;
//     width: 100%;
//     padding: 12px 16px;
//     border-radius: 2px;
//   }
//   .inp:hover { border-color: rgba(10,10,10,0.22); }
//   .inp:focus {
//     background: #ffffff;
//     border-color: #0a0a0a;
//     box-shadow: 0 0 0 3px rgba(10,10,10,0.08);
//   }
//   .inp::placeholder { color: var(--text-muted); }

//   select.inp {
//     cursor: pointer;
//     appearance: none;
//     background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%230a0a0a' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
//     background-repeat: no-repeat;
//     background-position: right 16px center;
//     padding-right: 40px;
//   }

//   .sect-label {
//     font-family: 'Inter', sans-serif;
//     font-size: 0.68rem;
//     letter-spacing: 0.24em;
//     text-transform: uppercase;
//     color: #0a0a0a;
//     display: flex;
//     align-items: center;
//     gap: 12px;
//     margin-bottom: 20px;
//     font-weight: 700;
//   }
//   .sect-label::after {
//     content: '';
//     flex: 1;
//     height: 1px;
//     background: linear-gradient(90deg, rgba(10,10,10,0.28), transparent);
//   }

//   .badge {
//     font-family: 'Inter', sans-serif;
//     font-size: 0.64rem;
//     letter-spacing: 0.1em;
//     text-transform: uppercase;
//     padding: 4px 10px;
//     border: 1px solid;
//     border-radius: 2px;
//     display: inline-flex;
//     align-items: center;
//     white-space: nowrap;
//     font-weight: 700;
//   }

//   .tab-btn {
//     font-family: 'Inter', sans-serif;
//     font-size: 0.78rem;
//     font-weight: 700;
//     letter-spacing: 0.12em;
//     text-transform: uppercase;
//     padding: 18px 26px;
//     background: transparent;
//     border: none;
//     border-bottom: 2px solid transparent;
//     color: var(--text-muted);
//     cursor: pointer;
//     transition: all 0.2s;
//     white-space: nowrap;
//     position: relative;
//   }
//   .tab-btn:hover { color: #0a0a0a; background: rgba(10,10,10,0.035); }
//   .tab-btn.active {
//     color: #0a0a0a;
//     border-bottom-color: #0a0a0a;
//   }

//   .stat-card {
//     background: #ffffff;
//     border: 1px solid var(--border);
//     padding: 20px 24px;
//     display: flex;
//     flex-direction: column;
//     gap: 6px;
//     position: relative;
//     overflow: hidden;
//     transition: all 0.2s;
//     border-radius: 2px;
//   }
//   .stat-card:hover {
//     border-color: rgba(10,10,10,0.2);
//     transform: translateY(-1px);
//     box-shadow: var(--shadow-sm);
//   }

//   .prog-bar { height: 3px; background: var(--cream-dark); overflow: hidden; border-radius: 3px; }
//   .prog-fill {
//     height: 100%;
//     background: #0a0a0a;
//     transition: width 0.3s;
//     border-radius: 3px;
//   }

//   .h-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
//   .h-dot.ok  { background: var(--emerald); box-shadow: 0 0 0 3px rgba(15,157,110,0.15); }
//   .h-dot.err { background: var(--ruby);    box-shadow: 0 0 0 3px rgba(220,38,38,0.15); }
//   .h-dot.unk { background: var(--text-muted); }
//   .h-dot.proc{ background: var(--amber);   box-shadow: 0 0 0 3px rgba(217,119,6,0.15); animation:pulse 1.6s ease infinite; }

//   .toast {
//     font-family: 'Inter', sans-serif;
//     font-size: 0.82rem;
//     padding: 14px 20px;
//     display: flex;
//     align-items: center;
//     gap: 12px;
//     border-left: 3px solid;
//     border-radius: 2px;
//     animation: fadeUp 0.25s ease;
//     min-width: 280px;
//     max-width: 400px;
//     backdrop-filter: blur(10px);
//   }

//   hr {
//     border: none;
//     height: 1px;
//     background: linear-gradient(90deg, transparent, var(--border), transparent);
//     margin: 20px 0;
//   }

//   /* Drop zone */
//   .dropzone {
//     border: 2px dashed var(--border);
//     border-radius: 4px;
//     padding: 40px;
//     text-align: center;
//     cursor: pointer;
//     background: var(--surface-2);
//     transition: all 0.25s cubic-bezier(0.2,0.8,0.4,1);
//   }
//   .dropzone:hover {
//     border-color: rgba(10,10,10,0.35);
//     background: rgba(10,10,10,0.025);
//   }
//   .dropzone.dragging {
//     border-color: #0a0a0a;
//     background: rgba(10,10,10,0.045);
//     box-shadow: inset 0 0 0 4px rgba(10,10,10,0.03);
//   }

//   /* Document list item */
//   .doc-item {
//     background: var(--surface-2);
//     border: 1px solid var(--border);
//     border-radius: 4px;
//     padding: 16px;
//     cursor: pointer;
//     transition: all 0.25s cubic-bezier(0.2,0.8,0.4,1);
//   }
//   .doc-item:hover {
//     border-color: rgba(10,10,10,0.2);
//     background: #ffffff;
//     box-shadow: var(--shadow-sm);
//     transform: translateY(-1px);
//   }
//   .doc-item.selected {
//     background: linear-gradient(135deg, #ffffff 0%, #faf7f1 100%);
//     border-color: #0a0a0a;
//     box-shadow: 0 0 0 3px rgba(10,10,10,0.06), var(--shadow-sm);
//   }

//   .quote-block {
//     background: linear-gradient(135deg, #fdfbf6 0%, #faf5ea 100%);
//     border-left: 3px solid #0a0a0a;
//     padding: 20px 24px;
//     font-size: 0.95rem;
//     color: #0a0a0a;
//     line-height: 1.75;
//     white-space: pre-wrap;
//     border-radius: 0 3px 3px 0;
//   }

//   .empty-state {
//     text-align: center;
//     padding: 48px 24px;
//     color: var(--text-muted);
//   }
//   .empty-state .icon { font-size: 2rem; margin-bottom: 14px; opacity: 0.55; }
// `;

// /* ─── Toast ─── */
// let _setToasts = null;
// const toast = {
//   _push(type, msg) {
//     const id = Date.now();
//     _setToasts?.(p => [...p, { id, type, msg }]);
//     setTimeout(() => _setToasts?.(p => p.filter(t => t.id !== id)), 4000);
//   },
//   success: m => toast._push('success', m),
//   error:   m => toast._push('error', m),
//   warn:    m => toast._push('warn', m),
//   info:    m => toast._push('info', m),
// };
// const TOAST_CFG = {
//   success: { accent:'#0f9d6e', icon:'✓' },
//   error:   { accent:'#dc2626', icon:'✕' },
//   warn:    { accent:'#d97706', icon:'!' },
//   info:    { accent:'#2563eb', icon:'i' },
// };
// function Toasts() {
//   const [toasts, setToasts] = useState([]);
//   useEffect(() => { _setToasts = setToasts; }, []);
//   return (
//     <div style={{ position:'fixed', bottom:24, right:24, zIndex:9999, display:'flex', flexDirection:'column', gap:12, pointerEvents:'none' }}>
//       {toasts.map(t => {
//         const c = TOAST_CFG[t.type];
//         return (
//           <div key={t.id} className="toast"
//             style={{
//               background:'#ffffff',
//               borderLeftColor:c.accent,
//               border:'1px solid var(--border)',
//               borderLeft:`3px solid ${c.accent}`,
//               boxShadow:'0 18px 40px -18px rgba(10,10,10,0.32)'
//             }}>
//             <span style={{
//               width:22, height:22, borderRadius:'50%',
//               background:`${c.accent}18`, color:c.accent,
//               display:'inline-flex', alignItems:'center', justifyContent:'center',
//               fontWeight:800, fontSize:'0.72rem', flexShrink:0
//             }}>{c.icon}</span>
//             <span style={{ fontWeight:500, color:'#0a0a0a' }}>{t.msg}</span>
//           </div>
//         );
//       })}
//     </div>
//   );
// }

// /* ─── Helpers ─── */
// const fmt = {
//   bytes: b => { if (!b) return '0 B'; const k=1024,s=['B','KB','MB','GB'],i=Math.floor(Math.log(b)/Math.log(k)); return (b/k**i).toFixed(1)+' '+s[i]; },
//   date:  d => d ? new Date(d).toLocaleString() : '—',
//   cut:   (s,n=80) => s && s.length>n ? s.slice(0,n)+'…' : (s||''),
// };

// /* ─── UI Primitives ─── */
// function SectLabel({ children }) {
//   return <div className="sect-label">{children}</div>;
// }
// function Badge({ children, color, gold }) {
//   // Gold variant now rendered in black to match "all text black"
//   const style = gold
//     ? { borderColor:'rgba(10,10,10,0.25)', color:'#0a0a0a', background:'rgba(10,10,10,0.05)' }
//     : { borderColor:`${color}40`, color, background:`${color}12` };
//   return <span className="badge" style={style}>{children}</span>;
// }
// function Card({ children, style={}, className='' }) {
//   return <div className={`luxury-card ${className}`} style={{ padding:24, ...style }}>{children}</div>;
// }
// function PrimaryBtn({ children, loading, loadText='Processing…', style={}, ...props }) {
//   return (
//     <button className="btn-primary" style={{ ...style }} {...props}>
//       {loading ? (
//         <span style={{ display:'flex', alignItems:'center', gap:8, justifyContent:'center' }}>
//           <span className="anim-spin" style={{ width:14, height:14, border:'2px solid rgba(255,255,255,0.3)', borderTop:'2px solid #ffffff', borderRadius:'50%', display:'inline-block' }} />
//           {loadText}
//         </span>
//       ) : children}
//     </button>
//   );
// }
// function HDot({ status }) {
//   const cls = status==='ready' ? 'ok' : status==='processing' ? 'proc' : status==='error' ? 'err' : 'unk';
//   return <span className={`h-dot ${cls}`} />;
// }

// /* ═══════════════════════════════════ MAIN ═══════════════════════════════════ */
// export default function AIDocumentProcessing() {
//   const [mounted, setMounted] = useState(false);
//   const [tab, setTab] = useState('documents');
//   const [loading, setLoading] = useState(false);

//   /* Documents */
//   const [documents, setDocuments] = useState([]);
//   const [selectedDoc, setSelectedDoc] = useState(null);
//   const [docStatus, setDocStatus] = useState({});
//   const [docDetails, setDocDetails] = useState(null);

//   /* Upload */
//   const [file, setFile] = useState(null);
//   const [uploadPct, setUploadPct] = useState(0);
//   const [dragging, setDragging] = useState(false);
//   const fileRef = useRef();

//   /* Chat */
//   const [queryText, setQueryText] = useState('');
//   const [chatHistory, setChatHistory] = useState([]);
//   const [chatResult, setChatResult] = useState(null);

//   /* Search */
//   const [searchQuery, setSearchQuery] = useState('');
//   const [searchMode, setSearchMode] = useState('semantic');
//   const [searchResults, setSearchResults] = useState([]);

//   /* Extraction */
//   const [extractionFields, setExtractionFields] = useState('');
//   const [extractionResult, setExtractionResult] = useState(null);

//   /* Summary */
//   const [summaryResult, setSummaryResult] = useState(null);

//   /* Reports */
//   const [reportData, setReportData] = useState(null);

//   /* ─ Init ─ */
//   useEffect(() => {
//     setMounted(true);
//     fetchDocuments();
//   }, []);

//   /* ─── API Functions ─── */
//   const fetchDocuments = async () => {
//     try {
//       const r = await AxiosInstance.get('/api/v1/documents/');
//       setDocuments(r.data.data || []);
//     } catch(e) {
//       console.error('Error fetching documents:', e);
//       toast.error('Failed to fetch documents');
//     }
//   };

//   const checkDocumentStatus = async (docId) => {
//     try {
//       const r = await AxiosInstance.get(`/api/v1/documents/${docId}/status`);
//       setDocStatus(prev => ({ ...prev, [docId]: r.data.data }));
//       return r.data.data;
//     } catch(e) {
//       console.error('Error checking document status:', e);
//       return null;
//     }
//   };

//   const getDocumentDetails = async (docId) => {
//     try {
//       const r = await AxiosInstance.get(`/api/v1/documents/${docId}`);
//       setDocDetails(r.data.data);
//       return r.data.data;
//     } catch(e) {
//       console.error('Error fetching document details:', e);
//       return null;
//     }
//   };

//   const uploadDocument = async () => {
//     if (!file) { toast.warn('Select a file first'); return; }
//     const fd = new FormData();
//     fd.append('file', file);
//     setLoading(true);
//     setUploadPct(0);
//     try {
//       const r = await AxiosInstance.post('/api/v1/documents/upload', fd, {
//         headers: { 'Content-Type': 'multipart/form-data' },
//         onUploadProgress: e => setUploadPct(e.total ? Math.round(e.loaded*100/e.total) : 50),
//       });
//       toast.success('Document uploaded successfully');
//       setFile(null);
//       setUploadPct(0);
//       fetchDocuments();

//       // Start polling for status
//       const docId = r.data.data.document_id;
//       pollDocumentStatus(docId);
//     } catch(e) {
//       toast.error(e.response?.data?.detail || 'Upload failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const pollDocumentStatus = (docId) => {
//     const interval = setInterval(async () => {
//       const status = await checkDocumentStatus(docId);
//       if (status && (status.status === 'ready' || status.status === 'error')) {
//         clearInterval(interval);
//         fetchDocuments();
//       }
//     }, 3000);
//   };

//   const deleteDocument = async (docId, filename) => {
//     if (!confirm(`Delete "${filename}"?`)) return;
//     try {
//       await AxiosInstance.delete(`/api/v1/documents/${docId}`);
//       toast.success('Document deleted');
//       if (selectedDoc === docId) setSelectedDoc(null);
//       fetchDocuments();
//     } catch(e) {
//       toast.error('Delete failed');
//     }
//   };

//   const submitChat = async () => {
//     if (!queryText.trim()) { toast.warn('Enter a question first'); return; }
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     setLoading(true);
//     setChatResult(null);
//     try {
//       const r = await AxiosInstance.post('/api/v1/chat/completions', {
//         document_id: selectedDoc,
//         message: queryText,
//       });

//       setChatResult(r.data.data);
//       setChatHistory(prev => [...prev, {
//         question: queryText,
//         answer: r.data.data,
//         timestamp: new Date().toISOString()
//       }]);
//       toast.success('Query completed');
//     } catch(e) {
//       toast.error(e.response?.data?.detail || 'Query failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const submitSearch = async () => {
//     if (!searchQuery.trim()) { toast.warn('Enter a search query first'); return; }
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     setLoading(true);
//     try {
//       const endpoint = searchMode === 'hybrid' ? '/api/v1/search/hybrid' : '/api/v1/search/semantic';
//       const r = await AxiosInstance.post(endpoint, {
//         query: searchQuery,
//         document_id: selectedDoc,
//       });
//       setSearchResults(r.data.data.results || []);
//       toast.success(`Found ${r.data.data.results?.length || 0} results`);
//     } catch(e) {
//       toast.error(e.response?.data?.detail || 'Search failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const submitExtraction = async () => {
//     if (!extractionFields.trim()) { toast.warn('Enter fields to extract first'); return; }
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     const fields = extractionFields.split(',').map(f => f.trim()).filter(f => f);
//     if (fields.length === 0) { toast.warn('Enter at least one field'); return; }

//     setLoading(true);
//     try {
//       const r = await AxiosInstance.post('/api/v1/extraction/structured', {
//         document_id: selectedDoc,
//         fields: fields,
//       });
//       setExtractionResult(r.data.data);
//       toast.success('Extraction completed');
//     } catch(e) {
//       toast.error(e.response?.data?.detail || 'Extraction failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const generateSummary = async () => {
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     setLoading(true);
//     try {
//       const r = await AxiosInstance.post(`/api/v1/documents/${selectedDoc}/summary`);
//       setSummaryResult(r.data.data);
//       toast.success('Summary generated');
//     } catch(e) {
//       toast.error(e.response?.data?.detail || 'Summary generation failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const downloadReport = async () => {
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     try {
//       const r = await AxiosInstance.get(`/api/v1/documents/${selectedDoc}/report`, {
//         responseType: 'blob',
//       });
//       const url = window.URL.createObjectURL(new Blob([r.data]));
//       const link = document.createElement('a');
//       link.href = url;
//       link.setAttribute('download', `report_${selectedDoc}.pdf`);
//       document.body.appendChild(link);
//       link.click();
//       link.remove();
//       toast.success('Report downloaded');
//     } catch(e) {
//       toast.error('Report download failed');
//     }
//   };

//   const getDocumentReport = async () => {
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     setLoading(true);
//     try {
//       const r = await AxiosInstance.get(`/api/v1/reports/document/${selectedDoc}`);
//       setReportData(r.data.data);
//       toast.success('Report data loaded');
//     } catch(e) {
//       toast.error(e.response?.data?.detail || 'Failed to fetch report');
//     } finally {
//       setLoading(false);
//     }
//   };

//   /* ─── Drag-drop ─── */
//   const onDrop = useCallback(e => {
//     e.preventDefault();
//     setDragging(false);
//     const f = e.dataTransfer.files[0];
//     if (f && f.type === 'application/pdf') {
//       setFile(f);
//     } else {
//       toast.warn('Please upload a PDF file');
//     }
//   }, []);

//   const onDragOver = useCallback(e => {
//     e.preventDefault();
//     setDragging(true);
//   }, []);

//   const onDragLeave = useCallback(e => {
//     e.preventDefault();
//     setDragging(false);
//   }, []);

//   /* ─── TABS ─── */
//   const TABS = [
//     { id:'documents', label:'Documents' },
//     { id:'chat',      label:'Chat' },
//     { id:'search',    label:'Search' },
//     { id:'extraction', label:'Extraction' },
//     { id:'summary',   label:'Summary' },
//     { id:'reports',   label:'Reports' },
//   ];

//   return (
//     <>
//       {mounted && <style suppressHydrationWarning>{GLOBAL_CSS}</style>}
//       <Toasts />

//       <div className="font-sans page-bg" style={{ minHeight:'100vh', color:'#0a0a0a', position:'relative', zIndex:1 }}>

//         {/* ═══ HEADER ═══ */}
//         <header style={{
//           background:'rgba(255,255,255,0.9)',
//           backdropFilter:'blur(20px)',
//           WebkitBackdropFilter:'blur(20px)',
//           borderBottom:'1px solid var(--border)',
//           position:'sticky',
//           top:0,
//           zIndex:40,
//           boxShadow:'0 1px 0 rgba(10,10,10,0.05), 0 10px 30px -24px rgba(10,10,10,0.35)'
//         }}>
//           {/* black hairline */}
//           <div style={{ height:2, background:'#0a0a0a' }} />
//           <div style={{ maxWidth:1400, margin:'0 auto', padding:'0 32px', height:72, display:'flex', alignItems:'center', justifyContent:'space-between' }}>
//             <div style={{ display:'flex', alignItems:'center', gap:24 }}>
//               <div style={{
//                 width:42, height:42,
//                 background:'#0a0a0a',
//                 display:'flex', alignItems:'center', justifyContent:'center',
//                 borderRadius:2,
//                 boxShadow:'0 8px 20px -10px rgba(10,10,10,0.7), inset 0 0 0 1px rgba(216,185,94,0.35)'
//               }}>
//                 <span className="font-serif gold-text" style={{ fontSize:'1.4rem', fontWeight:700 }}>AI</span>
//               </div>
//               <div>
//                 <div className="font-serif" style={{ fontSize:'1.45rem', letterSpacing:'0.02em', lineHeight:1.2, color:'#0a0a0a' }}>
//                   Document Processing
//                 </div>
//                 <div className="font-mono" style={{ fontSize:'0.6rem', letterSpacing:'0.22em', color:'var(--text-muted)', textTransform:'uppercase', marginTop:4 }}>
//                   RAG · Extraction · Search · Summary · Reports
//                 </div>
//               </div>
//             </div>
//             <div style={{ display:'flex', alignItems:'center', gap:24 }}>
//               <div style={{
//                 display:'flex', alignItems:'center', gap:10,
//                 border:'1px solid #0a0a0a',
//                 background:'#ffffff',
//                 padding:'7px 16px',
//                 borderRadius:2
//               }}>
//                 <span style={{ width:6, height:6, borderRadius:'50%', background:'#0a0a0a', display:'inline-block' }} />
//                 <span className="font-mono" style={{ fontSize:'0.65rem', letterSpacing:'0.12em', textTransform:'uppercase', color:'#0a0a0a' }}>
//                   {documents.length} Documents
//                 </span>
//               </div>
//             </div>
//           </div>
//         </header>

//         {/* ═══ TABS ═══ */}
//         <div style={{ background:'rgba(255,255,255,0.65)', backdropFilter:'blur(10px)', borderBottom:'1px solid var(--border)', overflowX:'auto' }}>
//           <div style={{ maxWidth:1400, margin:'0 auto', padding:'0 32px', display:'flex' }}>
//             {TABS.map(t => (
//               <button key={t.id} className={`tab-btn ${tab===t.id?'active':''}`}
//                 onClick={() => setTab(t.id)}>
//                 {t.label}
//               </button>
//             ))}
//           </div>
//         </div>

//         {/* ═══ CONTENT ═══ */}
//         <main style={{ maxWidth:1400, margin:'0 auto', padding:'32px 32px 60px' }}>

//           {/* ── DOCUMENTS TAB ── */}
//           {tab==='documents' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 2fr', gap:24, alignItems:'start' }}>

//               {/* Upload Panel */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Upload Document</SectLabel>
//                   <div
//                     className={`dropzone ${dragging ? 'dragging' : ''}`}
//                     onDrop={onDrop}
//                     onDragOver={onDragOver}
//                     onDragLeave={onDragLeave}
//                     onClick={() => fileRef.current?.click()}
//                   >
//                     <input
//                       ref={fileRef}
//                       type="file"
//                       accept=".pdf"
//                       style={{ display: 'none' }}
//                       onChange={e => {
//                         const f = e.target.files[0];
//                         if (f && f.type === 'application/pdf') {
//                           setFile(f);
//                         } else {
//                           toast.warn('Please upload a PDF file');
//                         }
//                       }}
//                     />
//                     <div style={{ fontSize: '2rem', marginBottom: 12, opacity: 0.7 }}>📄</div>
//                     <div style={{ color: '#0a0a0a', marginBottom: 8, fontWeight: 500 }}>
//                       {file ? file.name : 'Drag & drop PDF here or click to browse'}
//                     </div>
//                     <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
//                       PDF files only, max 10MB
//                     </div>
//                   </div>

//                   {file && (
//                     <div style={{ marginTop: 16 }}>
//                       <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
//                         <span className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a' }}>
//                           {file.name}
//                         </span>
//                         <span className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', fontWeight: 700 }}>
//                           {fmt.bytes(file.size)}
//                         </span>
//                       </div>
//                       {uploadPct > 0 && (
//                         <div className="prog-bar" style={{ marginBottom: 12 }}>
//                           <div className="prog-fill" style={{ width: `${uploadPct}%` }} />
//                         </div>
//                       )}
//                       <div style={{ display: 'flex', gap: 12 }}>
//                         <PrimaryBtn loading={loading} loadText="Uploading…" onClick={uploadDocument} disabled={loading} style={{ flex: 1 }}>
//                           Upload
//                         </PrimaryBtn>
//                         <button className="btn-ghost" onClick={() => { setFile(null); setUploadPct(0); }}>
//                           Clear
//                         </button>
//                       </div>
//                     </div>
//                   )}
//                 </Card>

//                 <Card>
//                   <SectLabel>Document Stats</SectLabel>
//                   <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
//                     <div style={{
//                       background:'linear-gradient(135deg, #fdfbf6, #faf5ea)',
//                       border:'1px solid var(--border)',
//                       borderRadius:3,
//                       padding:'14px 16px'
//                     }}>
//                       <div className="font-mono" style={{ fontSize: '0.62rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.1em', textTransform:'uppercase' }}>Total</div>
//                       <div className="font-serif" style={{ fontSize: '1.9rem', color: '#0a0a0a', lineHeight:1 }}>{documents.length}</div>
//                     </div>
//                     <div style={{
//                       background:'linear-gradient(135deg, #f6fdfa, #eefaf4)',
//                       border:'1px solid rgba(15,157,110,0.18)',
//                       borderRadius:3,
//                       padding:'14px 16px'
//                     }}>
//                       <div className="font-mono" style={{ fontSize: '0.62rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.1em', textTransform:'uppercase' }}>Ready</div>
//                       <div className="font-serif" style={{ fontSize: '1.9rem', color: '#0a0a0a', lineHeight:1 }}>
//                         {documents.filter(d => d.status === 'ready').length}
//                       </div>
//                     </div>
//                   </div>
//                 </Card>
//               </div>

//               {/* Documents List */}
//               <Card>
//                 <SectLabel>Document Library</SectLabel>
//                 {documents.length === 0 ? (
//                   <div className="empty-state">
//                     <div className="icon">📭</div>
//                     <div>No documents uploaded yet</div>
//                   </div>
//                 ) : (
//                   <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
//                     {documents.map(doc => (
//                       <div
//                         key={doc.id}
//                         className={`doc-item ${selectedDoc === doc.id ? 'selected' : ''}`}
//                         onClick={() => {
//                           setSelectedDoc(doc.id);
//                           getDocumentDetails(doc.id);
//                         }}
//                       >
//                         <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 8 }}>
//                           <div style={{ flex: 1, minWidth: 0 }}>
//                             <div style={{ fontWeight: 600, marginBottom: 4, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap', color:'#0a0a0a' }}>{doc.filename}</div>
//                             <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
//                               {fmt.bytes(doc.file_size_mb * 1024 * 1024)} • {doc.page_count || '?'} pages
//                             </div>
//                           </div>
//                           <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink:0 }}>
//                             <HDot status={doc.status} />
//                             <Badge color={doc.status === 'ready' ? '#0f9d6e' : doc.status === 'processing' ? '#d97706' : '#dc2626'}>
//                               {doc.status}
//                             </Badge>
//                           </div>
//                         </div>
//                         {doc.progress && doc.progress < 100 && (
//                           <div className="prog-bar" style={{ marginTop: 8 }}>
//                             <div className="prog-fill" style={{ width: `${doc.progress}%` }} />
//                           </div>
//                         )}
//                         <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 }}>
//                           <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
//                             {fmt.date(doc.created_at)}
//                           </div>
//                           <button
//                             className="btn-danger"
//                             onClick={(e) => { e.stopPropagation(); deleteDocument(doc.id, doc.filename); }}
//                             style={{ padding: '6px 14px', fontSize: '0.62rem' }}
//                           >
//                             Delete
//                           </button>
//                         </div>
//                       </div>
//                     ))}
//                   </div>
//                 )}
//               </Card>
//             </div>
//           )}

//           {/* ── CHAT TAB ── */}
//           {tab==='chat' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               {/* Chat Input */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <SectLabel>Your Question</SectLabel>
//                   <textarea
//                     className="inp"
//                     rows={5}
//                     value={queryText}
//                     onChange={e => setQueryText(e.target.value)}
//                     placeholder="Ask anything about your document..."
//                     style={{ marginBottom: 16, resize: 'vertical', lineHeight: 1.6 }}
//                   />

//                   <PrimaryBtn loading={loading} loadText="Processing…" onClick={submitChat} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
//                     Ask Question
//                   </PrimaryBtn>
//                 </Card>

//                 {chatHistory.length > 0 && (
//                   <Card>
//                     <SectLabel>Chat History</SectLabel>
//                     <div style={{ maxHeight: 300, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 12 }}>
//                       {chatHistory.slice().reverse().map((item, i) => (
//                         <div key={i} style={{ borderBottom: '1px solid var(--border-light)', paddingBottom: 12 }}>
//                           <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 4, fontWeight:700 }}>
//                             Q: {item.question}
//                           </div>
//                           <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: 4, lineHeight:1.6 }}>
//                             {item.answer?.answer?.substring(0, 100)}...
//                           </div>
//                           <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
//                             {fmt.date(item.timestamp)}
//                           </div>
//                         </div>
//                       ))}
//                     </div>
//                   </Card>
//                 )}
//               </div>

//               {/* Chat Result */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {chatResult ? (
//                   <Card>
//                     <SectLabel>Answer</SectLabel>
//                     <div style={{ display:'flex', flexWrap:'wrap', gap:8, marginBottom:16 }}>
//                       <Badge gold>{chatResult.mode || 'RAG'}</Badge>
//                       <Badge color="#2563eb">{chatResult.chunks_used || 0} chunks</Badge>
//                       {chatResult.iterations && <Badge color="#0f9d6e">{chatResult.iterations} iterations</Badge>}
//                     </div>

//                     <div className="quote-block" style={{ marginBottom:20 }}>
//                       {chatResult.answer}
//                     </div>

//                     {chatResult.citations && chatResult.citations.length > 0 && (
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', letterSpacing:'0.15em', textTransform:'uppercase', color:'#0a0a0a', marginBottom:12, fontWeight:700 }}>
//                           Citations
//                         </div>
//                         <div style={{ display:'flex', flexDirection:'column', gap: 8 }}>
//                           {chatResult.citations.map((citation, i) => (
//                             <div key={i} style={{ background:'var(--surface-2)', border:'1px solid var(--border)', padding: 12, borderRadius: 3, fontSize: '0.8rem' }}>
//                               <div className="font-mono" style={{ fontSize: '0.65rem', color: '#0a0a0a', marginBottom: 4, fontWeight:700 }}>
//                                 Page {citation.page_number}
//                               </div>
//                               <div style={{ color: 'var(--text-secondary)', lineHeight:1.6 }}>
//                                 {fmt.cut(citation.content, 150)}
//                               </div>
//                             </div>
//                           ))}
//                         </div>
//                       </div>
//                     )}
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">💬</div>
//                       <div>Select a document and ask a question</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//           {/* ── SEARCH TAB ── */}
//           {tab==='search' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               {/* Search Input */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <SectLabel>Search Mode</SectLabel>
//                   <select
//                     className="inp"
//                     value={searchMode}
//                     onChange={e => setSearchMode(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="semantic">Semantic Search (RAG)</option>
//                     <option value="hybrid">Hybrid Search (Keyword + Semantic)</option>
//                   </select>

//                   <SectLabel>Search Query</SectLabel>
//                   <textarea
//                     className="inp"
//                     rows={3}
//                     value={searchQuery}
//                     onChange={e => setSearchQuery(e.target.value)}
//                     placeholder="Enter search terms..."
//                     style={{ marginBottom: 16, resize: 'vertical' }}
//                   />

//                   <PrimaryBtn loading={loading} loadText="Searching…" onClick={submitSearch} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
//                     Search Document
//                   </PrimaryBtn>
//                 </Card>
//               </div>

//               {/* Search Results */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {searchResults.length > 0 ? (
//                   <Card>
//                     <SectLabel>Search Results ({searchResults.length})</SectLabel>
//                     <div style={{ display:'flex', flexDirection:'column', gap: 12 }}>
//                       {searchResults.map((result, i) => (
//                         <div key={i} style={{ background:'var(--surface-2)', padding: 16, borderRadius: 3, border: '1px solid var(--border)' }}>
//                           <div style={{ display:'flex', justifyContent:'space-between', marginBottom: 8, gap:8, flexWrap:'wrap' }}>
//                             <Badge color="#2563eb">Page {result.page_number}</Badge>
//                             <Badge gold>{(result.similarity * 100).toFixed(1)}% similar</Badge>
//                           </div>
//                           <div style={{ fontSize: '0.9rem', color: '#0a0a0a', lineHeight: 1.65 }}>
//                             {result.content}
//                           </div>
//                         </div>
//                       ))}
//                     </div>
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">🔍</div>
//                       <div>Search results will appear here</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//           {/* ── EXTRACTION TAB ── */}
//           {tab==='extraction' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               {/* Extraction Input */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <SectLabel>Fields to Extract</SectLabel>
//                   <textarea
//                     className="inp"
//                     rows={4}
//                     value={extractionFields}
//                     onChange={e => setExtractionFields(e.target.value)}
//                     placeholder="Enter fields separated by commas (e.g., company_name, revenue, employees, founded_year)"
//                     style={{ marginBottom: 16, resize: 'vertical' }}
//                   />

//                   <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 16 }}>
//                     Maximum 20 fields per request
//                   </div>

//                   <PrimaryBtn loading={loading} loadText="Extracting…" onClick={submitExtraction} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
//                     Extract Fields
//                   </PrimaryBtn>
//                 </Card>
//               </div>

//               {/* Extraction Results */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {extractionResult ? (
//                   <Card>
//                     <SectLabel>Extraction Results</SectLabel>
//                     <div style={{ marginBottom: 16 }}>
//                       <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8 }}>
//                         Document: {extractionResult.filename}
//                       </div>
//                       <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
//                         Model: {extractionResult.model}
//                       </div>
//                     </div>

//                     <div style={{ display: 'grid', gap: 12 }}>
//                       {Object.entries(extractionResult.fields).map(([field, data]) => (
//                         <div key={field} style={{ background:'var(--surface-2)', padding: 16, borderRadius: 3, border: '1px solid var(--border)' }}>
//                           <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.06em' }}>
//                             {field}
//                           </div>
//                           <div style={{ fontSize: '0.9rem', color: '#0a0a0a', marginBottom: 8, lineHeight:1.6 }}>
//                             {data.value || 'Not found'}
//                           </div>
//                           <Badge color={data.status === 'found' ? '#0f9d6e' : data.status === 'not_found' ? '#dc2626' : '#d97706'}>
//                             {data.status}
//                           </Badge>
//                         </div>
//                       ))}
//                     </div>
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">⚡</div>
//                       <div>Extraction results will appear here</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//           {/* ── SUMMARY TAB ── */}
//           {tab==='summary' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               {/* Summary Controls */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
//                     <PrimaryBtn loading={loading} loadText="Generating…" onClick={generateSummary} disabled={loading || !selectedDoc} style={{ flex: 1 }}>
//                       Generate Summary
//                     </PrimaryBtn>
//                     <button
//                       className="btn-ghost"
//                       onClick={downloadReport}
//                       disabled={!selectedDoc}
//                       style={{ flex: 1 }}
//                     >
//                       Download Report
//                     </button>
//                   </div>

//                   <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', lineHeight:1.6 }}>
//                     Summary uses AI to analyze document content and extract key information
//                   </div>
//                 </Card>

//                 {selectedDoc && (
//                   <Card>
//                     <SectLabel>Document Info</SectLabel>
//                     {(() => {
//                       const doc = documents.find(d => d.id === selectedDoc);
//                       return doc ? (
//                         <div style={{ display: 'grid', gap: 12 }}>
//                           <div>
//                             <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Filename</div>
//                             <div style={{ fontWeight:500, color:'#0a0a0a' }}>{doc.filename}</div>
//                           </div>
//                           <div>
//                             <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Size</div>
//                             <div style={{ color:'#0a0a0a' }}>{fmt.bytes(doc.file_size_mb * 1024 * 1024)}</div>
//                           </div>
//                           <div>
//                             <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Pages</div>
//                             <div style={{ color:'#0a0a0a' }}>{doc.page_count || 'Processing...'}</div>
//                           </div>
//                           <div>
//                             <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Status</div>
//                             <Badge color={doc.status === 'ready' ? '#0f9d6e' : '#d97706'}>{doc.status}</Badge>
//                           </div>
//                         </div>
//                       ) : null;
//                     })()}
//                   </Card>
//                 )}
//               </div>

//               {/* Summary Results */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {summaryResult ? (
//                   <Card>
//                     <SectLabel>AI Summary</SectLabel>
//                     <div style={{ marginBottom: 20 }}>
//                       <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8 }}>
//                         Model: {summaryResult.model}
//                       </div>
//                     </div>

//                     {summaryResult.executive_summary && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Executive Summary
//                         </div>
//                         <div className="quote-block">
//                           {summaryResult.executive_summary}
//                         </div>
//                       </div>
//                     )}

//                     {summaryResult.key_points && summaryResult.key_points.length > 0 && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Key Points
//                         </div>
//                         <ul style={{ margin: 0, paddingLeft: 20, color:'#0a0a0a' }}>
//                           {summaryResult.key_points.map((point, i) => (
//                             <li key={i} style={{ marginBottom: 8, lineHeight: 1.65 }}>{point}</li>
//                           ))}
//                         </ul>
//                       </div>
//                     )}

//                     {summaryResult.important_facts && summaryResult.important_facts.length > 0 && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Important Facts
//                         </div>
//                         <ul style={{ margin: 0, paddingLeft: 20, color:'#0a0a0a' }}>
//                           {summaryResult.important_facts.map((fact, i) => (
//                             <li key={i} style={{ marginBottom: 8, lineHeight: 1.65 }}>{fact}</li>
//                           ))}
//                         </ul>
//                       </div>
//                     )}

//                     {summaryResult.important_numbers && summaryResult.important_numbers.length > 0 && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Important Numbers
//                         </div>
//                         <ul style={{ margin: 0, paddingLeft: 20, color:'#0a0a0a' }}>
//                           {summaryResult.important_numbers.map((num, i) => (
//                             <li key={i} style={{ marginBottom: 8, lineHeight: 1.65 }}>{num}</li>
//                           ))}
//                         </ul>
//                       </div>
//                     )}

//                     {summaryResult.risks && summaryResult.risks.length > 0 && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--ruby)', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Risks
//                         </div>
//                         <ul style={{ margin: 0, paddingLeft: 20 }}>
//                           {summaryResult.risks.map((risk, i) => (
//                             <li key={i} style={{ marginBottom: 8, lineHeight: 1.65, color: 'var(--ruby)' }}>{risk}</li>
//                           ))}
//                         </ul>
//                       </div>
//                     )}

//                     {summaryResult.conclusion && (
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Conclusion
//                         </div>
//                         <div className="quote-block">
//                           {summaryResult.conclusion}
//                         </div>
//                       </div>
//                     )}
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">📋</div>
//                       <div>Select a document and generate summary</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//           {/* ── REPORTS TAB ── */}
//           {tab==='reports' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               {/* Report Controls */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
//                     <PrimaryBtn loading={loading} loadText="Loading…" onClick={getDocumentReport} disabled={loading || !selectedDoc} style={{ flex: 1 }}>
//                       Get Report Data
//                     </PrimaryBtn>
//                     <button
//                       className="btn-ghost"
//                       onClick={downloadReport}
//                       disabled={!selectedDoc}
//                       style={{ flex: 1 }}
//                     >
//                       Download PDF
//                     </button>
//                   </div>

//                   <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', lineHeight:1.6 }}>
//                     Reports include document information, AI summary, and extracted data
//                   </div>
//                 </Card>

//                 {selectedDoc && docDetails && (
//                   <Card>
//                     <SectLabel>Document Details</SectLabel>
//                     <div style={{ display: 'grid', gap: 12 }}>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Filename</div>
//                         <div style={{ fontWeight:500, color:'#0a0a0a' }}>{docDetails.filename}</div>
//                       </div>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Size</div>
//                         <div style={{ color:'#0a0a0a' }}>{fmt.bytes(docDetails.file_size_mb * 1024 * 1024)}</div>
//                       </div>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Pages</div>
//                         <div style={{ color:'#0a0a0a' }}>{docDetails.page_count}</div>
//                       </div>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Status</div>
//                         <Badge color={docDetails.status === 'ready' ? '#0f9d6e' : '#d97706'}>{docDetails.status}</Badge>
//                       </div>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Created</div>
//                         <div style={{ color:'#0a0a0a' }}>{fmt.date(docDetails.created_at)}</div>
//                       </div>
//                     </div>
//                   </Card>
//                 )}
//               </div>

//               {/* Report Results */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {reportData ? (
//                   <Card>
//                     <SectLabel>Report Data</SectLabel>
//                     <div style={{
//                       background:'linear-gradient(135deg, #fdfbf6, #faf5ea)',
//                       border:'1px solid var(--border)',
//                       padding: 20,
//                       borderRadius: 3,
//                       whiteSpace: 'pre-wrap',
//                       fontSize: '0.8rem',
//                       lineHeight: 1.7,
//                       fontFamily: "'JetBrains Mono', monospace",
//                       color:'#0a0a0a',
//                       maxHeight: 620,
//                       overflow:'auto'
//                     }}>
//                       {JSON.stringify(reportData, null, 2)}
//                     </div>
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">📊</div>
//                       <div>Select a document and load report data</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//         </main>
//       </div>
//     </>
//   );
// }













// 'use client';
// import React, { useState, useEffect, useRef, useCallback } from 'react';
// import AxiosInstance from "@/components/AxiosInstance";

// /* ─── Global styles - Black & Light Luxury Edition ─── */
// const GLOBAL_CSS = `
//   @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,500;1,600;1,700;1,800&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

//   *, *::before, *::after { box-sizing: border-box; }

//   :root {
//     --page:        #f7f3ec;
//     --cream:       #faf7f1;
//     --cream-dark:  #efe9de;
//     --pure-white:  #ffffff;
//     --ivory:       #f5f0e6;
//     --platinum:    #eceae5;

//     --black:       #0a0a0a;
//     --black-soft:  #1a1a1a;
//     --black-hover: #262626;

//     --gold:        #b8912f;
//     --gold-light:  #d8b95e;
//     --gold-dark:   #8f6f1c;
//     --gold-line:   rgba(184,145,47,0.22);

//     --surface:     #ffffff;
//     --surface-2:   #faf7f1;
//     --surface-3:   #f3ede2;
//     --border:      #e7dfd2;
//     --border-light:#f0e9dd;

//     --text-primary:   #0a0a0a;
//     --text-secondary: #333333;
//     --text-muted:     #6b6b6b;

//     --emerald:  #0f9d6e;
//     --sapphire: #2563eb;
//     --ruby:     #dc2626;
//     --amber:    #d97706;
//     --violet:   #7c3aed;

//     --shadow-sm: 0 1px 2px rgba(10,10,10,0.04), 0 6px 18px -12px rgba(10,10,10,0.12);
//     --shadow-md: 0 2px 4px rgba(10,10,10,0.04), 0 18px 40px -24px rgba(10,10,10,0.22);
//     --shadow-lg: 0 30px 60px -30px rgba(10,10,10,0.28);
//   }

//   body { background: var(--page); }

//   .font-serif { font-family: 'Cormorant Garamond', Georgia, serif; }
//   .font-sans  { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
//   .font-mono  { font-family: 'JetBrains Mono', monospace; }

//   .page-bg {
//     background-color: var(--page);
//     background-image:
//       radial-gradient(1100px 520px at 50% -10%, rgba(184,145,47,0.11), transparent 62%),
//       radial-gradient(700px 400px at 100% 100%, rgba(184,145,47,0.05), transparent 60%);
//     background-repeat: no-repeat;
//     background-attachment: fixed;
//   }

//   ::-webkit-scrollbar { width: 6px; height: 6px; }
//   ::-webkit-scrollbar-track { background: var(--cream-dark); }
//   ::-webkit-scrollbar-thumb { background: #0a0a0a; border-radius: 6px; }
//   ::-webkit-scrollbar-thumb:hover { background: #333333; }

//   @keyframes fadeUp  { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
//   @keyframes fadeIn  { from{opacity:0} to{opacity:1} }
//   @keyframes spinCW  { to{transform:rotate(360deg)} }
//   @keyframes pulse   { 0%,100%{opacity:1} 50%{opacity:.5} }

//   .anim-fade-up { animation:fadeUp .4s cubic-bezier(0.2,0.8,0.4,1) forwards; }
//   .anim-fade-in { animation:fadeIn .3s ease forwards; }
//   .anim-spin    { animation:spinCW .7s linear infinite; }
//   .anim-pulse   { animation:pulse 2s ease infinite; }

//   .luxury-card {
//     position: relative;
//     background: linear-gradient(160deg, #ffffff 0%, #fdfbf7 100%);
//     border: 1px solid var(--border);
//     box-shadow: var(--shadow-sm);
//     transition: all 0.35s cubic-bezier(0.2,0.8,0.4,1);
//   }
//   .luxury-card::before {
//     content: '';
//     position: absolute;
//     top: 0; left: 0; right: 0;
//     height: 2px;
//     background: linear-gradient(90deg, transparent, var(--gold-line), transparent);
//     opacity: 0;
//     transition: opacity 0.35s ease;
//   }
//   .luxury-card:hover {
//     border-color: rgba(10,10,10,0.18);
//     transform: translateY(-2px);
//     box-shadow: var(--shadow-md);
//   }
//   .luxury-card:hover::before { opacity: 1; }

//   .gold-text {
//     background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 45%, var(--gold-dark) 100%);
//     -webkit-background-clip: text;
//     -webkit-text-fill-color: transparent;
//     background-clip: text;
//   }

//   .btn-primary {
//     background: #0a0a0a;
//     color: #ffffff;
//     font-family: 'Inter', sans-serif;
//     font-weight: 700;
//     letter-spacing: 0.08em;
//     font-size: 0.72rem;
//     text-transform: uppercase;
//     border: 1px solid #0a0a0a;
//     cursor: pointer;
//     position: relative;
//     overflow: hidden;
//     transition: all 0.25s ease;
//     padding: 13px 28px;
//     border-radius: 2px;
//     box-shadow: 0 10px 22px -14px rgba(10,10,10,0.85), inset 0 1px 0 rgba(255,255,255,0.08);
//   }

//   .btn-primary::before {
//     content: '';
//     position: absolute;
//     top: 0; left: -120%;
//     width: 60%;
//     height: 100%;
//     background: linear-gradient(90deg, transparent, rgba(255,255,255,0.24), transparent);
//     transition: left 0.6s ease;
//   }

//   .btn-primary:hover::before { left: 130%; }
//   .btn-primary:hover {
//     background: #262626;
//     border-color: #262626;
//     color: #ffffff;
//     transform: translateY(-1px);
//     box-shadow: 0 16px 30px -16px rgba(10,10,10,0.9);
//   }
//   .btn-primary:active { transform: translateY(0); }
//   .btn-primary:disabled {
//     background: #d6d3cc;
//     border-color: #d6d3cc;
//     color: #8a8579;
//     cursor: not-allowed;
//     transform: none;
//     box-shadow: none;
//   }

//   .btn-ghost {
//     background: #ffffff;
//     color: #0a0a0a;
//     font-family: 'Inter', sans-serif;
//     font-weight: 700;
//     font-size: 0.7rem;
//     letter-spacing: 0.12em;
//     text-transform: uppercase;
//     border: 1px solid #0a0a0a;
//     cursor: pointer;
//     transition: all 0.2s;
//     padding: 11px 20px;
//     border-radius: 2px;
//   }
//   .btn-ghost:hover {
//     background: #0a0a0a;
//     color: #ffffff;
//     box-shadow: 0 12px 24px -14px rgba(10,10,10,0.9);
//   }
//   .btn-ghost:disabled {
//     opacity: 0.35;
//     cursor: not-allowed;
//     color: #0a0a0a;
//     border-color: #0a0a0a;
//     background: #ffffff;
//   }

//   .btn-danger {
//     background: #0a0a0a;
//     color: #ffffff;
//     font-family: 'Inter', sans-serif;
//     font-weight: 700;
//     font-size: 0.7rem;
//     letter-spacing: 0.12em;
//     text-transform: uppercase;
//     border: 1px solid #0a0a0a;
//     cursor: pointer;
//     transition: all 0.2s;
//     padding: 11px 20px;
//     border-radius: 2px;
//   }
//   .btn-danger:hover {
//     background: #dc2626;
//     border-color: #dc2626;
//     color: #ffffff;
//     box-shadow: 0 12px 24px -14px rgba(220,38,38,0.85);
//   }

//   .inp {
//     background: var(--surface-2);
//     border: 1px solid var(--border);
//     color: #0a0a0a;
//     font-family: 'Inter', sans-serif;
//     font-size: 0.85rem;
//     outline: none;
//     transition: all 0.2s;
//     width: 100%;
//     padding: 12px 16px;
//     border-radius: 2px;
//   }
//   .inp:hover { border-color: rgba(10,10,10,0.22); }
//   .inp:focus {
//     background: #ffffff;
//     border-color: #0a0a0a;
//     box-shadow: 0 0 0 3px rgba(10,10,10,0.08);
//   }
//   .inp::placeholder { color: var(--text-muted); }

//   select.inp {
//     cursor: pointer;
//     appearance: none;
//     background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%230a0a0a' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
//     background-repeat: no-repeat;
//     background-position: right 16px center;
//     padding-right: 40px;
//   }

//   .sect-label {
//     font-family: 'Inter', sans-serif;
//     font-size: 0.68rem;
//     letter-spacing: 0.24em;
//     text-transform: uppercase;
//     color: #0a0a0a;
//     display: flex;
//     align-items: center;
//     gap: 12px;
//     margin-bottom: 20px;
//     font-weight: 700;
//   }
//   .sect-label::after {
//     content: '';
//     flex: 1;
//     height: 1px;
//     background: linear-gradient(90deg, rgba(10,10,10,0.28), transparent);
//   }

//   .badge {
//     font-family: 'Inter', sans-serif;
//     font-size: 0.64rem;
//     letter-spacing: 0.1em;
//     text-transform: uppercase;
//     padding: 4px 10px;
//     border: 1px solid;
//     border-radius: 2px;
//     display: inline-flex;
//     align-items: center;
//     white-space: nowrap;
//     font-weight: 700;
//   }

//   .tab-btn {
//     font-family: 'Inter', sans-serif;
//     font-size: 0.78rem;
//     font-weight: 700;
//     letter-spacing: 0.12em;
//     text-transform: uppercase;
//     padding: 18px 26px;
//     background: transparent;
//     border: none;
//     border-bottom: 2px solid transparent;
//     color: var(--text-muted);
//     cursor: pointer;
//     transition: all 0.2s;
//     white-space: nowrap;
//     position: relative;
//   }
//   .tab-btn:hover { color: #0a0a0a; background: rgba(10,10,10,0.035); }
//   .tab-btn.active {
//     color: #0a0a0a;
//     border-bottom-color: #0a0a0a;
//   }

//   .stat-card {
//     background: #ffffff;
//     border: 1px solid var(--border);
//     padding: 20px 24px;
//     display: flex;
//     flex-direction: column;
//     gap: 6px;
//     position: relative;
//     overflow: hidden;
//     transition: all 0.2s;
//     border-radius: 2px;
//   }
//   .stat-card:hover {
//     border-color: rgba(10,10,10,0.2);
//     transform: translateY(-1px);
//     box-shadow: var(--shadow-sm);
//   }

//   .prog-bar { height: 3px; background: var(--cream-dark); overflow: hidden; border-radius: 3px; }
//   .prog-fill {
//     height: 100%;
//     background: #0a0a0a;
//     transition: width 0.3s;
//     border-radius: 3px;
//   }

//   .h-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
//   .h-dot.ok  { background: var(--emerald); box-shadow: 0 0 0 3px rgba(15,157,110,0.15); }
//   .h-dot.err { background: var(--ruby);    box-shadow: 0 0 0 3px rgba(220,38,38,0.15); }
//   .h-dot.unk { background: var(--text-muted); }
//   .h-dot.proc{ background: var(--amber);   box-shadow: 0 0 0 3px rgba(217,119,6,0.15); animation:pulse 1.6s ease infinite; }

//   .toast {
//     font-family: 'Inter', sans-serif;
//     font-size: 0.82rem;
//     padding: 14px 20px;
//     display: flex;
//     align-items: center;
//     gap: 12px;
//     border-left: 3px solid;
//     border-radius: 2px;
//     animation: fadeUp 0.25s ease;
//     min-width: 280px;
//     max-width: 400px;
//     backdrop-filter: blur(10px);
//   }

//   hr {
//     border: none;
//     height: 1px;
//     background: linear-gradient(90deg, transparent, var(--border), transparent);
//     margin: 20px 0;
//   }

//   .dropzone {
//     border: 2px dashed var(--border);
//     border-radius: 4px;
//     padding: 40px;
//     text-align: center;
//     cursor: pointer;
//     background: var(--surface-2);
//     transition: all 0.25s cubic-bezier(0.2,0.8,0.4,1);
//   }
//   .dropzone:hover {
//     border-color: rgba(10,10,10,0.35);
//     background: rgba(10,10,10,0.025);
//   }
//   .dropzone.dragging {
//     border-color: #0a0a0a;
//     background: rgba(10,10,10,0.045);
//     box-shadow: inset 0 0 0 4px rgba(10,10,10,0.03);
//   }

//   .doc-item {
//     background: var(--surface-2);
//     border: 1px solid var(--border);
//     border-radius: 4px;
//     padding: 16px;
//     cursor: pointer;
//     transition: all 0.25s cubic-bezier(0.2,0.8,0.4,1);
//   }
//   .doc-item:hover {
//     border-color: rgba(10,10,10,0.2);
//     background: #ffffff;
//     box-shadow: var(--shadow-sm);
//     transform: translateY(-1px);
//   }
//   .doc-item.selected {
//     background: linear-gradient(135deg, #ffffff 0%, #faf7f1 100%);
//     border-color: #0a0a0a;
//     box-shadow: 0 0 0 3px rgba(10,10,10,0.06), var(--shadow-sm);
//   }

//   .quote-block {
//     background: linear-gradient(135deg, #fdfbf6 0%, #faf5ea 100%);
//     border-left: 3px solid #0a0a0a;
//     padding: 20px 24px;
//     font-size: 0.95rem;
//     color: #0a0a0a;
//     line-height: 1.75;
//     white-space: pre-wrap;
//     border-radius: 0 3px 3px 0;
//   }

//   .empty-state {
//     text-align: center;
//     padding: 48px 24px;
//     color: var(--text-muted);
//   }
//   .empty-state .icon { font-size: 2rem; margin-bottom: 14px; opacity: 0.55; }
// `;

// /* ─── Toast ─── */
// let _setToasts = null;
// const toast = {
//   _push(type, msg) {
//     const id = Date.now();
//     _setToasts?.(p => [...p, { id, type, msg }]);
//     setTimeout(() => _setToasts?.(p => p.filter(t => t.id !== id)), 4000);
//   },
//   success: m => toast._push('success', m),
//   error:   m => toast._push('error', m),
//   warn:    m => toast._push('warn', m),
//   info:    m => toast._push('info', m),
// };
// const TOAST_CFG = {
//   success: { accent:'#0f9d6e', icon:'✓' },
//   error:   { accent:'#dc2626', icon:'✕' },
//   warn:    { accent:'#d97706', icon:'!' },
//   info:    { accent:'#2563eb', icon:'i' },
// };
// function Toasts() {
//   const [toasts, setToasts] = useState([]);
//   useEffect(() => { _setToasts = setToasts; }, []);
//   return (
//     <div style={{ position:'fixed', bottom:24, right:24, zIndex:9999, display:'flex', flexDirection:'column', gap:12, pointerEvents:'none' }}>
//       {toasts.map(t => {
//         const c = TOAST_CFG[t.type];
//         return (
//           <div key={t.id} className="toast"
//             style={{
//               background:'#ffffff',
//               borderLeftColor:c.accent,
//               border:'1px solid var(--border)',
//               borderLeft:`3px solid ${c.accent}`,
//               boxShadow:'0 18px 40px -18px rgba(10,10,10,0.32)'
//             }}>
//             <span style={{
//               width:22, height:22, borderRadius:'50%',
//               background:`${c.accent}18`, color:c.accent,
//               display:'inline-flex', alignItems:'center', justifyContent:'center',
//               fontWeight:800, fontSize:'0.72rem', flexShrink:0
//             }}>{c.icon}</span>
//             <span style={{ fontWeight:500, color:'#0a0a0a' }}>{t.msg}</span>
//           </div>
//         );
//       })}
//     </div>
//   );
// }

// /* ─── Helpers ─── */
// const fmt = {
//   bytes: b => { if (!b) return '0 B'; const k=1024,s=['B','KB','MB','GB'],i=Math.floor(Math.log(b)/Math.log(k)); return (b/k**i).toFixed(1)+' '+s[i]; },
//   date:  d => d ? new Date(d).toLocaleString() : '—',
//   cut:   (s,n=80) => s && s.length>n ? s.slice(0,n)+'…' : (s||''),
// };

// /* ─── UI Primitives ─── */
// function SectLabel({ children }) {
//   return <div className="sect-label">{children}</div>;
// }
// function Badge({ children, color, gold }) {
//   const style = gold
//     ? { borderColor:'rgba(10,10,10,0.25)', color:'#0a0a0a', background:'rgba(10,10,10,0.05)' }
//     : { borderColor:`${color}40`, color, background:`${color}12` };
//   return <span className="badge" style={style}>{children}</span>;
// }
// function Card({ children, style={}, className='' }) {
//   return <div className={`luxury-card ${className}`} style={{ padding:24, ...style }}>{children}</div>;
// }
// function PrimaryBtn({ children, loading, loadText='Processing…', style={}, ...props }) {
//   return (
//     <button className="btn-primary" style={{ ...style }} {...props}>
//       {loading ? (
//         <span style={{ display:'flex', alignItems:'center', gap:8, justifyContent:'center' }}>
//           <span className="anim-spin" style={{ width:14, height:14, border:'2px solid rgba(255,255,255,0.3)', borderTop:'2px solid #ffffff', borderRadius:'50%', display:'inline-block' }} />
//           {loadText}
//         </span>
//       ) : children}
//     </button>
//   );
// }
// function HDot({ status }) {
//   const cls = status==='ready' ? 'ok' : status==='processing' ? 'proc' : status==='error' ? 'err' : 'unk';
//   return <span className={`h-dot ${cls}`} />;
// }

// /* ═══════════════════════════════════ MAIN ═══════════════════════════════════ */
// export default function AIDocumentProcessing() {
//   const [mounted, setMounted] = useState(false);
//   const [tab, setTab] = useState('documents');
//   const [loading, setLoading] = useState(false);

//   /* Documents */
//   const [documents, setDocuments] = useState([]);
//   const [selectedDoc, setSelectedDoc] = useState(null);
//   const [docStatus, setDocStatus] = useState({});
//   const [docDetails, setDocDetails] = useState(null);

//   /* Upload */
//   const [file, setFile] = useState(null);
//   const [uploadPct, setUploadPct] = useState(0);
//   const [dragging, setDragging] = useState(false);
//   const fileRef = useRef();

//   /* Chat */
//   const [queryText, setQueryText] = useState('');
//   const [chatHistory, setChatHistory] = useState([]);
//   const [chatResult, setChatResult] = useState(null);

//   /* Search */
//   const [searchQuery, setSearchQuery] = useState('');
//   const [searchMode, setSearchMode] = useState('semantic');
//   const [searchResults, setSearchResults] = useState([]);

//   /* Extraction */
//   const [extractionFields, setExtractionFields] = useState('');
//   const [extractionResult, setExtractionResult] = useState(null);

//   /* Summary */
//   const [summaryResult, setSummaryResult] = useState(null);

//   /* Reports */
//   const [reportData, setReportData] = useState(null);

//   /* ─ Init ─ */
//   useEffect(() => {
//     setMounted(true);
//     fetchDocuments();
//   }, []);

//   /* ─── API Functions ─── */

//   // GET /api/v1/documents/  → List user's documents
//   const fetchDocuments = async () => {
//     try {
//       const r = await AxiosInstance.get('/api/v1/documents/');
//       setDocuments(r.data.data || []);
//     } catch (e) {
//       console.error('Error fetching documents:', e);
//       toast.error('Failed to fetch documents');
//     }
//   };

//   // GET /api/v1/documents/{id}/status/  → Get processing status
//   const checkDocumentStatus = async (docId) => {
//     try {
//       const r = await AxiosInstance.get(`/api/v1/documents/${docId}/status/`);
//       setDocStatus(prev => ({ ...prev, [docId]: r.data.data }));
//       return r.data.data;
//     } catch (e) {
//       console.error('Error checking document status:', e);
//       return null;
//     }
//   };

//   // GET /api/v1/documents/{id}/  → Get document details
//   const getDocumentDetails = async (docId) => {
//     try {
//       const r = await AxiosInstance.get(`/api/v1/documents/${docId}/`);
//       setDocDetails(r.data.data);
//       return r.data.data;
//     } catch (e) {
//       console.error('Error fetching document details:', e);
//       return null;
//     }
//   };

//   // POST /api/v1/documents/upload  → Upload PDF document (NO trailing slash on this route)
//   const uploadDocument = async () => {
//     if (!file) { toast.warn('Select a file first'); return; }
//     const fd = new FormData();
//     fd.append('file', file);
//     setLoading(true);
//     setUploadPct(0);
//     try {
//       const r = await AxiosInstance.post('/api/v1/documents/upload', fd, {
//         headers: { 'Content-Type': 'multipart/form-data' },
//         onUploadProgress: e => setUploadPct(e.total ? Math.round(e.loaded * 100 / e.total) : 50),
//       });
//       toast.success('Document uploaded successfully');
//       setFile(null);
//       setUploadPct(0);
//       fetchDocuments();

//       const docId = r.data.data.document_id;
//       pollDocumentStatus(docId);
//     } catch (e) {
//       toast.error(e.response?.data?.detail || 'Upload failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   const pollDocumentStatus = (docId) => {
//     const interval = setInterval(async () => {
//       const status = await checkDocumentStatus(docId);
//       if (status && (status.status === 'ready' || status.status === 'error')) {
//         clearInterval(interval);
//         fetchDocuments();
//       }
//     }, 3000);
//   };

//   // DELETE /api/v1/documents/{id}/  → Delete document
//   const deleteDocument = async (docId, filename) => {
//     if (!confirm(`Delete "${filename}"?`)) return;
//     try {
//       await AxiosInstance.delete(`/api/v1/documents/${docId}/`);
//       toast.success('Document deleted');
//       if (selectedDoc === docId) setSelectedDoc(null);
//       fetchDocuments();
//     } catch (e) {
//       toast.error('Delete failed');
//     }
//   };

//   // POST /api/v1/chat/completions/  → Chat with documents using RAG
//   const submitChat = async () => {
//     if (!queryText.trim()) { toast.warn('Enter a question first'); return; }
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     setLoading(true);
//     setChatResult(null);
//     try {
//       const r = await AxiosInstance.post('/api/v1/chat/completions/', {
//         document_id: selectedDoc,
//         message: queryText,
//       });

//       setChatResult(r.data.data);
//       setChatHistory(prev => [...prev, {
//         question: queryText,
//         answer: r.data.data,
//         timestamp: new Date().toISOString()
//       }]);
//       toast.success('Query completed');
//     } catch (e) {
//       toast.error(e.response?.data?.detail || 'Query failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   // POST /api/v1/search/semantic/  OR  /api/v1/search/hybrid/
//   const submitSearch = async () => {
//     if (!searchQuery.trim()) { toast.warn('Enter a search query first'); return; }
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     setLoading(true);
//     try {
//       const endpoint = searchMode === 'hybrid'
//         ? '/api/v1/search/hybrid/'
//         : '/api/v1/search/semantic/';
//       const r = await AxiosInstance.post(endpoint, {
//         query: searchQuery,
//         document_id: selectedDoc,
//       });
//       setSearchResults(r.data.data.results || []);
//       toast.success(`Found ${r.data.data.results?.length || 0} results`);
//     } catch (e) {
//       toast.error(e.response?.data?.detail || 'Search failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   // POST /api/v1/extraction/structured/  → Extract structured data
//   const submitExtraction = async () => {
//     if (!extractionFields.trim()) { toast.warn('Enter fields to extract first'); return; }
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     const fields = extractionFields.split(',').map(f => f.trim()).filter(f => f);
//     if (fields.length === 0) { toast.warn('Enter at least one field'); return; }

//     setLoading(true);
//     try {
//       const r = await AxiosInstance.post('/api/v1/extraction/structured/', {
//         document_id: selectedDoc,
//         fields: fields,
//       });
//       setExtractionResult(r.data.data);
//       toast.success('Extraction completed');
//     } catch (e) {
//       toast.error(e.response?.data?.detail || 'Extraction failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   // POST /api/v1/documents/{id}/summary/  → Generate AI summary
//   const generateSummary = async () => {
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     setLoading(true);
//     try {
//       const r = await AxiosInstance.post(`/api/v1/documents/${selectedDoc}/summary/`);
//       setSummaryResult(r.data.data);
//       toast.success('Summary generated');
//     } catch (e) {
//       toast.error(e.response?.data?.detail || 'Summary generation failed');
//     } finally {
//       setLoading(false);
//     }
//   };

//   // GET /api/v1/documents/{id}/report/  → Download PDF report
//   const downloadReport = async () => {
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     try {
//       const r = await AxiosInstance.get(`/api/v1/documents/${selectedDoc}/report/`, {
//         responseType: 'blob',
//       });
//       const url = window.URL.createObjectURL(new Blob([r.data]));
//       const link = document.createElement('a');
//       link.href = url;
//       link.setAttribute('download', `report_${selectedDoc}.pdf`);
//       document.body.appendChild(link);
//       link.click();
//       link.remove();
//       toast.success('Report downloaded');
//     } catch (e) {
//       toast.error('Report download failed');
//     }
//   };

//   // GET /api/v1/reports/document/{id}/  → Get document report
//   const getDocumentReport = async () => {
//     if (!selectedDoc) { toast.warn('Select a document first'); return; }

//     setLoading(true);
//     try {
//       const r = await AxiosInstance.get(`/api/v1/reports/document/${selectedDoc}/`);
//       setReportData(r.data.data);
//       toast.success('Report data loaded');
//     } catch (e) {
//       toast.error(e.response?.data?.detail || 'Failed to fetch report');
//     } finally {
//       setLoading(false);
//     }
//   };

//   /* ─── Drag-drop ─── */
//   const onDrop = useCallback(e => {
//     e.preventDefault();
//     setDragging(false);
//     const f = e.dataTransfer.files[0];
//     if (f && f.type === 'application/pdf') {
//       setFile(f);
//     } else {
//       toast.warn('Please upload a PDF file');
//     }
//   }, []);

//   const onDragOver = useCallback(e => {
//     e.preventDefault();
//     setDragging(true);
//   }, []);

//   const onDragLeave = useCallback(e => {
//     e.preventDefault();
//     setDragging(false);
//   }, []);

//   /* ─── TABS ─── */
//   const TABS = [
//     { id:'documents', label:'Documents' },
//     { id:'chat',      label:'Chat' },
//     { id:'search',    label:'Search' },
//     { id:'extraction', label:'Extraction' },
//     { id:'summary',   label:'Summary' },
//     { id:'reports',   label:'Reports' },
//   ];

//   return (
//     <>
//       {mounted && <style suppressHydrationWarning>{GLOBAL_CSS}</style>}
//       <Toasts />

//       <div className="font-sans page-bg" style={{ minHeight:'100vh', color:'#0a0a0a', position:'relative', zIndex:1 }}>

//         {/* ═══ HEADER ═══ */}
//         <header style={{
//           background:'rgba(255,255,255,0.9)',
//           backdropFilter:'blur(20px)',
//           WebkitBackdropFilter:'blur(20px)',
//           borderBottom:'1px solid var(--border)',
//           position:'sticky',
//           top:0,
//           zIndex:40,
//           boxShadow:'0 1px 0 rgba(10,10,10,0.05), 0 10px 30px -24px rgba(10,10,10,0.35)'
//         }}>
//           <div style={{ height:2, background:'#0a0a0a' }} />
//           <div style={{ maxWidth:1400, margin:'0 auto', padding:'0 32px', height:72, display:'flex', alignItems:'center', justifyContent:'space-between' }}>
//             <div style={{ display:'flex', alignItems:'center', gap:24 }}>
//               <div style={{
//                 width:42, height:42,
//                 background:'#0a0a0a',
//                 display:'flex', alignItems:'center', justifyContent:'center',
//                 borderRadius:2,
//                 boxShadow:'0 8px 20px -10px rgba(10,10,10,0.7), inset 0 0 0 1px rgba(216,185,94,0.35)'
//               }}>
//                 <span className="font-serif gold-text" style={{ fontSize:'1.4rem', fontWeight:700 }}>AI</span>
//               </div>
//               <div>
//                 <div className="font-serif" style={{ fontSize:'1.45rem', letterSpacing:'0.02em', lineHeight:1.2, color:'#0a0a0a' }}>
//                   Document Processing
//                 </div>
//                 <div className="font-mono" style={{ fontSize:'0.6rem', letterSpacing:'0.22em', color:'var(--text-muted)', textTransform:'uppercase', marginTop:4 }}>
//                   RAG · Extraction · Search · Summary · Reports
//                 </div>
//               </div>
//             </div>
//             <div style={{ display:'flex', alignItems:'center', gap:24 }}>
//               <div style={{
//                 display:'flex', alignItems:'center', gap:10,
//                 border:'1px solid #0a0a0a',
//                 background:'#ffffff',
//                 padding:'7px 16px',
//                 borderRadius:2
//               }}>
//                 <span style={{ width:6, height:6, borderRadius:'50%', background:'#0a0a0a', display:'inline-block' }} />
//                 <span className="font-mono" style={{ fontSize:'0.65rem', letterSpacing:'0.12em', textTransform:'uppercase', color:'#0a0a0a' }}>
//                   {documents.length} Documents
//                 </span>
//               </div>
//             </div>
//           </div>
//         </header>

//         {/* ═══ TABS ═══ */}
//         <div style={{ background:'rgba(255,255,255,0.65)', backdropFilter:'blur(10px)', borderBottom:'1px solid var(--border)', overflowX:'auto' }}>
//           <div style={{ maxWidth:1400, margin:'0 auto', padding:'0 32px', display:'flex' }}>
//             {TABS.map(t => (
//               <button key={t.id} className={`tab-btn ${tab===t.id?'active':''}`}
//                 onClick={() => setTab(t.id)}>
//                 {t.label}
//               </button>
//             ))}
//           </div>
//         </div>

//         {/* ═══ CONTENT ═══ */}
//         <main style={{ maxWidth:1400, margin:'0 auto', padding:'32px 32px 60px' }}>

//           {/* ── DOCUMENTS TAB ── */}
//           {tab==='documents' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 2fr', gap:24, alignItems:'start' }}>

//               {/* Upload Panel */}
//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Upload Document</SectLabel>
//                   <div
//                     className={`dropzone ${dragging ? 'dragging' : ''}`}
//                     onDrop={onDrop}
//                     onDragOver={onDragOver}
//                     onDragLeave={onDragLeave}
//                     onClick={() => fileRef.current?.click()}
//                   >
//                     <input
//                       ref={fileRef}
//                       type="file"
//                       accept=".pdf"
//                       style={{ display: 'none' }}
//                       onChange={e => {
//                         const f = e.target.files[0];
//                         if (f && f.type === 'application/pdf') {
//                           setFile(f);
//                         } else {
//                           toast.warn('Please upload a PDF file');
//                         }
//                       }}
//                     />
//                     <div style={{ fontSize: '2rem', marginBottom: 12, opacity: 0.7 }}>📄</div>
//                     <div style={{ color: '#0a0a0a', marginBottom: 8, fontWeight: 500 }}>
//                       {file ? file.name : 'Drag & drop PDF here or click to browse'}
//                     </div>
//                     <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
//                       PDF files only, max 10MB
//                     </div>
//                   </div>

//                   {file && (
//                     <div style={{ marginTop: 16 }}>
//                       <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
//                         <span className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a' }}>
//                           {file.name}
//                         </span>
//                         <span className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', fontWeight: 700 }}>
//                           {fmt.bytes(file.size)}
//                         </span>
//                       </div>
//                       {uploadPct > 0 && (
//                         <div className="prog-bar" style={{ marginBottom: 12 }}>
//                           <div className="prog-fill" style={{ width: `${uploadPct}%` }} />
//                         </div>
//                       )}
//                       <div style={{ display: 'flex', gap: 12 }}>
//                         <PrimaryBtn loading={loading} loadText="Uploading…" onClick={uploadDocument} disabled={loading} style={{ flex: 1 }}>
//                           Upload
//                         </PrimaryBtn>
//                         <button className="btn-ghost" onClick={() => { setFile(null); setUploadPct(0); }}>
//                           Clear
//                         </button>
//                       </div>
//                     </div>
//                   )}
//                 </Card>

//                 <Card>
//                   <SectLabel>Document Stats</SectLabel>
//                   <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
//                     <div style={{
//                       background:'linear-gradient(135deg, #fdfbf6, #faf5ea)',
//                       border:'1px solid var(--border)',
//                       borderRadius:3,
//                       padding:'14px 16px'
//                     }}>
//                       <div className="font-mono" style={{ fontSize: '0.62rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.1em', textTransform:'uppercase' }}>Total</div>
//                       <div className="font-serif" style={{ fontSize: '1.9rem', color: '#0a0a0a', lineHeight:1 }}>{documents.length}</div>
//                     </div>
//                     <div style={{
//                       background:'linear-gradient(135deg, #f6fdfa, #eefaf4)',
//                       border:'1px solid rgba(15,157,110,0.18)',
//                       borderRadius:3,
//                       padding:'14px 16px'
//                     }}>
//                       <div className="font-mono" style={{ fontSize: '0.62rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.1em', textTransform:'uppercase' }}>Ready</div>
//                       <div className="font-serif" style={{ fontSize: '1.9rem', color: '#0a0a0a', lineHeight:1 }}>
//                         {documents.filter(d => d.status === 'ready').length}
//                       </div>
//                     </div>
//                   </div>
//                 </Card>
//               </div>

//               {/* Documents List */}
//               <Card>
//                 <SectLabel>Document Library</SectLabel>
//                 {documents.length === 0 ? (
//                   <div className="empty-state">
//                     <div className="icon">📭</div>
//                     <div>No documents uploaded yet</div>
//                   </div>
//                 ) : (
//                   <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
//                     {documents.map(doc => (
//                       <div
//                         key={doc.id}
//                         className={`doc-item ${selectedDoc === doc.id ? 'selected' : ''}`}
//                         onClick={() => {
//                           setSelectedDoc(doc.id);
//                           getDocumentDetails(doc.id);
//                         }}
//                       >
//                         <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 8 }}>
//                           <div style={{ flex: 1, minWidth: 0 }}>
//                             <div style={{ fontWeight: 600, marginBottom: 4, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap', color:'#0a0a0a' }}>{doc.filename}</div>
//                             <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
//                               {fmt.bytes(doc.file_size_mb * 1024 * 1024)} • {doc.page_count || '?'} pages
//                             </div>
//                           </div>
//                           <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink:0 }}>
//                             <HDot status={doc.status} />
//                             <Badge color={doc.status === 'ready' ? '#0f9d6e' : doc.status === 'processing' ? '#d97706' : '#dc2626'}>
//                               {doc.status}
//                             </Badge>
//                           </div>
//                         </div>
//                         {doc.progress && doc.progress < 100 && (
//                           <div className="prog-bar" style={{ marginTop: 8 }}>
//                             <div className="prog-fill" style={{ width: `${doc.progress}%` }} />
//                           </div>
//                         )}
//                         <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 }}>
//                           <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
//                             {fmt.date(doc.created_at)}
//                           </div>
//                           <button
//                             className="btn-danger"
//                             onClick={(e) => { e.stopPropagation(); deleteDocument(doc.id, doc.filename); }}
//                             style={{ padding: '6px 14px', fontSize: '0.62rem' }}
//                           >
//                             Delete
//                           </button>
//                         </div>
//                       </div>
//                     ))}
//                   </div>
//                 )}
//               </Card>
//             </div>
//           )}

//           {/* ── CHAT TAB ── */}
//           {tab==='chat' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <SectLabel>Your Question</SectLabel>
//                   <textarea
//                     className="inp"
//                     rows={5}
//                     value={queryText}
//                     onChange={e => setQueryText(e.target.value)}
//                     placeholder="Ask anything about your document..."
//                     style={{ marginBottom: 16, resize: 'vertical', lineHeight: 1.6 }}
//                   />

//                   <PrimaryBtn loading={loading} loadText="Processing…" onClick={submitChat} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
//                     Ask Question
//                   </PrimaryBtn>
//                 </Card>

//                 {chatHistory.length > 0 && (
//                   <Card>
//                     <SectLabel>Chat History</SectLabel>
//                     <div style={{ maxHeight: 300, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 12 }}>
//                       {chatHistory.slice().reverse().map((item, i) => (
//                         <div key={i} style={{ borderBottom: '1px solid var(--border-light)', paddingBottom: 12 }}>
//                           <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 4, fontWeight:700 }}>
//                             Q: {item.question}
//                           </div>
//                           <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: 4, lineHeight:1.6 }}>
//                             {item.answer?.answer?.substring(0, 100)}...
//                           </div>
//                           <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
//                             {fmt.date(item.timestamp)}
//                           </div>
//                         </div>
//                       ))}
//                     </div>
//                   </Card>
//                 )}
//               </div>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {chatResult ? (
//                   <Card>
//                     <SectLabel>Answer</SectLabel>
//                     <div style={{ display:'flex', flexWrap:'wrap', gap:8, marginBottom:16 }}>
//                       <Badge gold>{chatResult.mode || 'RAG'}</Badge>
//                       <Badge color="#2563eb">{chatResult.chunks_used || 0} chunks</Badge>
//                       {chatResult.iterations && <Badge color="#0f9d6e">{chatResult.iterations} iterations</Badge>}
//                     </div>

//                     <div className="quote-block" style={{ marginBottom:20 }}>
//                       {chatResult.answer}
//                     </div>

//                     {chatResult.citations && chatResult.citations.length > 0 && (
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', letterSpacing:'0.15em', textTransform:'uppercase', color:'#0a0a0a', marginBottom:12, fontWeight:700 }}>
//                           Citations
//                         </div>
//                         <div style={{ display:'flex', flexDirection:'column', gap: 8 }}>
//                           {chatResult.citations.map((citation, i) => (
//                             <div key={i} style={{ background:'var(--surface-2)', border:'1px solid var(--border)', padding: 12, borderRadius: 3, fontSize: '0.8rem' }}>
//                               <div className="font-mono" style={{ fontSize: '0.65rem', color: '#0a0a0a', marginBottom: 4, fontWeight:700 }}>
//                                 Page {citation.page_number}
//                               </div>
//                               <div style={{ color: 'var(--text-secondary)', lineHeight:1.6 }}>
//                                 {fmt.cut(citation.content, 150)}
//                               </div>
//                             </div>
//                           ))}
//                         </div>
//                       </div>
//                     )}
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">💬</div>
//                       <div>Select a document and ask a question</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//           {/* ── SEARCH TAB ── */}
//           {tab==='search' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <SectLabel>Search Mode</SectLabel>
//                   <select
//                     className="inp"
//                     value={searchMode}
//                     onChange={e => setSearchMode(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="semantic">Semantic Search (RAG)</option>
//                     <option value="hybrid">Hybrid Search (Keyword + Semantic)</option>
//                   </select>

//                   <SectLabel>Search Query</SectLabel>
//                   <textarea
//                     className="inp"
//                     rows={3}
//                     value={searchQuery}
//                     onChange={e => setSearchQuery(e.target.value)}
//                     placeholder="Enter search terms..."
//                     style={{ marginBottom: 16, resize: 'vertical' }}
//                   />

//                   <PrimaryBtn loading={loading} loadText="Searching…" onClick={submitSearch} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
//                     Search Document
//                   </PrimaryBtn>
//                 </Card>
//               </div>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {searchResults.length > 0 ? (
//                   <Card>
//                     <SectLabel>Search Results ({searchResults.length})</SectLabel>
//                     <div style={{ display:'flex', flexDirection:'column', gap: 12 }}>
//                       {searchResults.map((result, i) => (
//                         <div key={i} style={{ background:'var(--surface-2)', padding: 16, borderRadius: 3, border: '1px solid var(--border)' }}>
//                           <div style={{ display:'flex', justifyContent:'space-between', marginBottom: 8, gap:8, flexWrap:'wrap' }}>
//                             <Badge color="#2563eb">Page {result.page_number}</Badge>
//                             <Badge gold>{(result.similarity * 100).toFixed(1)}% similar</Badge>
//                           </div>
//                           <div style={{ fontSize: '0.9rem', color: '#0a0a0a', lineHeight: 1.65 }}>
//                             {result.content}
//                           </div>
//                         </div>
//                       ))}
//                     </div>
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">🔍</div>
//                       <div>Search results will appear here</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//           {/* ── EXTRACTION TAB ── */}
//           {tab==='extraction' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <SectLabel>Fields to Extract</SectLabel>
//                   <textarea
//                     className="inp"
//                     rows={4}
//                     value={extractionFields}
//                     onChange={e => setExtractionFields(e.target.value)}
//                     placeholder="Enter fields separated by commas (e.g., company_name, revenue, employees, founded_year)"
//                     style={{ marginBottom: 16, resize: 'vertical' }}
//                   />

//                   <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 16 }}>
//                     Maximum 20 fields per request
//                   </div>

//                   <PrimaryBtn loading={loading} loadText="Extracting…" onClick={submitExtraction} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
//                     Extract Fields
//                   </PrimaryBtn>
//                 </Card>
//               </div>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {extractionResult ? (
//                   <Card>
//                     <SectLabel>Extraction Results</SectLabel>
//                     <div style={{ marginBottom: 16 }}>
//                       <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8 }}>
//                         Document: {extractionResult.filename}
//                       </div>
//                       <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
//                         Model: {extractionResult.model}
//                       </div>
//                     </div>

//                     <div style={{ display: 'grid', gap: 12 }}>
//                       {Object.entries(extractionResult.fields).map(([field, data]) => (
//                         <div key={field} style={{ background:'var(--surface-2)', padding: 16, borderRadius: 3, border: '1px solid var(--border)' }}>
//                           <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.06em' }}>
//                             {field}
//                           </div>
//                           <div style={{ fontSize: '0.9rem', color: '#0a0a0a', marginBottom: 8, lineHeight:1.6 }}>
//                             {data.value || 'Not found'}
//                           </div>
//                           <Badge color={data.status === 'found' ? '#0f9d6e' : data.status === 'not_found' ? '#dc2626' : '#d97706'}>
//                             {data.status}
//                           </Badge>
//                         </div>
//                       ))}
//                     </div>
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">⚡</div>
//                       <div>Extraction results will appear here</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//           {/* ── SUMMARY TAB ── */}
//           {tab==='summary' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
//                     <PrimaryBtn loading={loading} loadText="Generating…" onClick={generateSummary} disabled={loading || !selectedDoc} style={{ flex: 1 }}>
//                       Generate Summary
//                     </PrimaryBtn>
//                     <button
//                       className="btn-ghost"
//                       onClick={downloadReport}
//                       disabled={!selectedDoc}
//                       style={{ flex: 1 }}
//                     >
//                       Download Report
//                     </button>
//                   </div>

//                   <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', lineHeight:1.6 }}>
//                     Summary uses AI to analyze document content and extract key information
//                   </div>
//                 </Card>

//                 {selectedDoc && (
//                   <Card>
//                     <SectLabel>Document Info</SectLabel>
//                     {(() => {
//                       const doc = documents.find(d => d.id === selectedDoc);
//                       return doc ? (
//                         <div style={{ display: 'grid', gap: 12 }}>
//                           <div>
//                             <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Filename</div>
//                             <div style={{ fontWeight:500, color:'#0a0a0a' }}>{doc.filename}</div>
//                           </div>
//                           <div>
//                             <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Size</div>
//                             <div style={{ color:'#0a0a0a' }}>{fmt.bytes(doc.file_size_mb * 1024 * 1024)}</div>
//                           </div>
//                           <div>
//                             <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Pages</div>
//                             <div style={{ color:'#0a0a0a' }}>{doc.page_count || 'Processing...'}</div>
//                           </div>
//                           <div>
//                             <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Status</div>
//                             <Badge color={doc.status === 'ready' ? '#0f9d6e' : '#d97706'}>{doc.status}</Badge>
//                           </div>
//                         </div>
//                       ) : null;
//                     })()}
//                   </Card>
//                 )}
//               </div>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {summaryResult ? (
//                   <Card>
//                     <SectLabel>AI Summary</SectLabel>
//                     <div style={{ marginBottom: 20 }}>
//                       <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8 }}>
//                         Model: {summaryResult.model}
//                       </div>
//                     </div>

//                     {summaryResult.executive_summary && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Executive Summary
//                         </div>
//                         <div className="quote-block">
//                           {summaryResult.executive_summary}
//                         </div>
//                       </div>
//                     )}

//                     {summaryResult.key_points && summaryResult.key_points.length > 0 && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Key Points
//                         </div>
//                         <ul style={{ margin: 0, paddingLeft: 20, color:'#0a0a0a' }}>
//                           {summaryResult.key_points.map((point, i) => (
//                             <li key={i} style={{ marginBottom: 8, lineHeight: 1.65 }}>{point}</li>
//                           ))}
//                         </ul>
//                       </div>
//                     )}

//                     {summaryResult.important_facts && summaryResult.important_facts.length > 0 && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Important Facts
//                         </div>
//                         <ul style={{ margin: 0, paddingLeft: 20, color:'#0a0a0a' }}>
//                           {summaryResult.important_facts.map((fact, i) => (
//                             <li key={i} style={{ marginBottom: 8, lineHeight: 1.65 }}>{fact}</li>
//                           ))}
//                         </ul>
//                       </div>
//                     )}

//                     {summaryResult.important_numbers && summaryResult.important_numbers.length > 0 && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Important Numbers
//                         </div>
//                         <ul style={{ margin: 0, paddingLeft: 20, color:'#0a0a0a' }}>
//                           {summaryResult.important_numbers.map((num, i) => (
//                             <li key={i} style={{ marginBottom: 8, lineHeight: 1.65 }}>{num}</li>
//                           ))}
//                         </ul>
//                       </div>
//                     )}

//                     {summaryResult.risks && summaryResult.risks.length > 0 && (
//                       <div style={{ marginBottom: 20 }}>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--ruby)', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Risks
//                         </div>
//                         <ul style={{ margin: 0, paddingLeft: 20 }}>
//                           {summaryResult.risks.map((risk, i) => (
//                             <li key={i} style={{ marginBottom: 8, lineHeight: 1.65, color: 'var(--ruby)' }}>{risk}</li>
//                           ))}
//                         </ul>
//                       </div>
//                     )}

//                     {summaryResult.conclusion && (
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
//                           Conclusion
//                         </div>
//                         <div className="quote-block">
//                           {summaryResult.conclusion}
//                         </div>
//                       </div>
//                     )}
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">📋</div>
//                       <div>Select a document and generate summary</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//           {/* ── REPORTS TAB ── */}
//           {tab==='reports' && (
//             <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 <Card>
//                   <SectLabel>Document Selection</SectLabel>
//                   <select
//                     className="inp"
//                     value={selectedDoc || ''}
//                     onChange={e => setSelectedDoc(e.target.value)}
//                     style={{ marginBottom: 20 }}
//                   >
//                     <option value="">Select a document...</option>
//                     {documents.filter(d => d.status === 'ready').map(d => (
//                       <option key={d.id} value={d.id}>{d.filename}</option>
//                     ))}
//                   </select>

//                   <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
//                     <PrimaryBtn loading={loading} loadText="Loading…" onClick={getDocumentReport} disabled={loading || !selectedDoc} style={{ flex: 1 }}>
//                       Get Report Data
//                     </PrimaryBtn>
//                     <button
//                       className="btn-ghost"
//                       onClick={downloadReport}
//                       disabled={!selectedDoc}
//                       style={{ flex: 1 }}
//                     >
//                       Download PDF
//                     </button>
//                   </div>

//                   <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', lineHeight:1.6 }}>
//                     Reports include document information, AI summary, and extracted data
//                   </div>
//                 </Card>

//                 {selectedDoc && docDetails && (
//                   <Card>
//                     <SectLabel>Document Details</SectLabel>
//                     <div style={{ display: 'grid', gap: 12 }}>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Filename</div>
//                         <div style={{ fontWeight:500, color:'#0a0a0a' }}>{docDetails.filename}</div>
//                       </div>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Size</div>
//                         <div style={{ color:'#0a0a0a' }}>{fmt.bytes(docDetails.file_size_mb * 1024 * 1024)}</div>
//                       </div>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Pages</div>
//                         <div style={{ color:'#0a0a0a' }}>{docDetails.page_count}</div>
//                       </div>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Status</div>
//                         <Badge color={docDetails.status === 'ready' ? '#0f9d6e' : '#d97706'}>{docDetails.status}</Badge>
//                       </div>
//                       <div>
//                         <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Created</div>
//                         <div style={{ color:'#0a0a0a' }}>{fmt.date(docDetails.created_at)}</div>
//                       </div>
//                     </div>
//                   </Card>
//                 )}
//               </div>

//               <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
//                 {reportData ? (
//                   <Card>
//                     <SectLabel>Report Data</SectLabel>
//                     <div style={{
//                       background:'linear-gradient(135deg, #fdfbf6, #faf5ea)',
//                       border:'1px solid var(--border)',
//                       padding: 20,
//                       borderRadius: 3,
//                       whiteSpace: 'pre-wrap',
//                       fontSize: '0.8rem',
//                       lineHeight: 1.7,
//                       fontFamily: "'JetBrains Mono', monospace",
//                       color:'#0a0a0a',
//                       maxHeight: 620,
//                       overflow:'auto'
//                     }}>
//                       {JSON.stringify(reportData, null, 2)}
//                     </div>
//                   </Card>
//                 ) : (
//                   <Card>
//                     <div className="empty-state">
//                       <div className="icon">📊</div>
//                       <div>Select a document and load report data</div>
//                     </div>
//                   </Card>
//                 )}
//               </div>
//             </div>
//           )}

//         </main>
//       </div>
//     </>
//   );
// }







'use client';
import React, { useState, useEffect, useRef, useCallback } from 'react';
import AxiosInstance from "@/components/AxiosInstance";

/* ─── Global styles - Black & Light Luxury Edition ─── */
const GLOBAL_CSS = `
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,500;1,600;1,700;1,800&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

  *, *::before, *::after { box-sizing: border-box; }

  :root {
    --page:        #f7f3ec;
    --cream:       #faf7f1;
    --cream-dark:  #efe9de;
    --pure-white:  #ffffff;
    --ivory:       #f5f0e6;
    --platinum:    #eceae5;

    --black:       #0a0a0a;
    --black-soft:  #1a1a1a;
    --black-hover: #262626;

    --gold:        #b8912f;
    --gold-light:  #d8b95e;
    --gold-dark:   #8f6f1c;
    --gold-line:   rgba(184,145,47,0.22);

    --surface:     #ffffff;
    --surface-2:   #faf7f1;
    --surface-3:   #f3ede2;
    --border:      #e7dfd2;
    --border-light:#f0e9dd;

    --text-primary:   #0a0a0a;
    --text-secondary: #333333;
    --text-muted:     #6b6b6b;

    --emerald:  #0f9d6e;
    --sapphire: #2563eb;
    --ruby:     #dc2626;
    --amber:    #d97706;
    --violet:   #7c3aed;

    --shadow-sm: 0 1px 2px rgba(10,10,10,0.04), 0 6px 18px -12px rgba(10,10,10,0.12);
    --shadow-md: 0 2px 4px rgba(10,10,10,0.04), 0 18px 40px -24px rgba(10,10,10,0.22);
    --shadow-lg: 0 30px 60px -30px rgba(10,10,10,0.28);
  }

  body { background: var(--page); }

  .font-serif { font-family: 'Cormorant Garamond', Georgia, serif; }
  .font-sans  { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
  .font-mono  { font-family: 'JetBrains Mono', monospace; }

  .page-bg {
    background-color: var(--page);
    background-image:
      radial-gradient(1100px 520px at 50% -10%, rgba(184,145,47,0.11), transparent 62%),
      radial-gradient(700px 400px at 100% 100%, rgba(184,145,47,0.05), transparent 60%);
    background-repeat: no-repeat;
    background-attachment: fixed;
  }

  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: var(--cream-dark); }
  ::-webkit-scrollbar-thumb { background: #0a0a0a; border-radius: 6px; }
  ::-webkit-scrollbar-thumb:hover { background: #333333; }

  @keyframes fadeUp  { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
  @keyframes fadeIn  { from{opacity:0} to{opacity:1} }
  @keyframes spinCW  { to{transform:rotate(360deg)} }
  @keyframes pulse   { 0%,100%{opacity:1} 50%{opacity:.5} }

  .anim-fade-up { animation:fadeUp .4s cubic-bezier(0.2,0.8,0.4,1) forwards; }
  .anim-fade-in { animation:fadeIn .3s ease forwards; }
  .anim-spin    { animation:spinCW .7s linear infinite; }
  .anim-pulse   { animation:pulse 2s ease infinite; }

  .luxury-card {
    position: relative;
    background: linear-gradient(160deg, #ffffff 0%, #fdfbf7 100%);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    transition: all 0.35s cubic-bezier(0.2,0.8,0.4,1);
  }
  .luxury-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold-line), transparent);
    opacity: 0;
    transition: opacity 0.35s ease;
  }
  .luxury-card:hover {
    border-color: rgba(10,10,10,0.18);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  .luxury-card:hover::before { opacity: 1; }

  .gold-text {
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 45%, var(--gold-dark) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .btn-primary {
    background: #0a0a0a;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    letter-spacing: 0.08em;
    font-size: 0.72rem;
    text-transform: uppercase;
    border: 1px solid #0a0a0a;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
    padding: 13px 28px;
    border-radius: 2px;
    box-shadow: 0 10px 22px -14px rgba(10,10,10,0.85), inset 0 1px 0 rgba(255,255,255,0.08);
  }

  .btn-primary::before {
    content: '';
    position: absolute;
    top: 0; left: -120%;
    width: 60%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.24), transparent);
    transition: left 0.6s ease;
  }

  .btn-primary:hover::before { left: 130%; }
  .btn-primary:hover {
    background: #262626;
    border-color: #262626;
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: 0 16px 30px -16px rgba(10,10,10,0.9);
  }
  .btn-primary:active { transform: translateY(0); }
  .btn-primary:disabled {
    background: #d6d3cc;
    border-color: #d6d3cc;
    color: #8a8579;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .btn-ghost {
    background: #ffffff;
    color: #0a0a0a;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border: 1px solid #0a0a0a;
    cursor: pointer;
    transition: all 0.2s;
    padding: 11px 20px;
    border-radius: 2px;
  }
  .btn-ghost:hover {
    background: #0a0a0a;
    color: #ffffff;
    box-shadow: 0 12px 24px -14px rgba(10,10,10,0.9);
  }
  .btn-ghost:disabled {
    opacity: 0.35;
    cursor: not-allowed;
    color: #0a0a0a;
    border-color: #0a0a0a;
    background: #ffffff;
  }

  .btn-danger {
    background: #0a0a0a;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border: 1px solid #0a0a0a;
    cursor: pointer;
    transition: all 0.2s;
    padding: 11px 20px;
    border-radius: 2px;
  }
  .btn-danger:hover {
    background: #dc2626;
    border-color: #dc2626;
    color: #ffffff;
    box-shadow: 0 12px 24px -14px rgba(220,38,38,0.85);
  }

  .inp {
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: #0a0a0a;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    outline: none;
    transition: all 0.2s;
    width: 100%;
    padding: 12px 16px;
    border-radius: 2px;
  }
  .inp:hover { border-color: rgba(10,10,10,0.22); }
  .inp:focus {
    background: #ffffff;
    border-color: #0a0a0a;
    box-shadow: 0 0 0 3px rgba(10,10,10,0.08);
  }
  .inp::placeholder { color: var(--text-muted); }

  select.inp {
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%230a0a0a' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 16px center;
    padding-right: 40px;
  }

  .sect-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: #0a0a0a;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    font-weight: 700;
  }
  .sect-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(10,10,10,0.28), transparent);
  }

  .badge {
    font-family: 'Inter', sans-serif;
    font-size: 0.64rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 10px;
    border: 1px solid;
    border-radius: 2px;
    display: inline-flex;
    align-items: center;
    white-space: nowrap;
    font-weight: 700;
  }

  .tab-btn {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 18px 26px;
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
    position: relative;
  }
  .tab-btn:hover { color: #0a0a0a; background: rgba(10,10,10,0.035); }
  .tab-btn.active {
    color: #0a0a0a;
    border-bottom-color: #0a0a0a;
  }

  .stat-card {
    background: #ffffff;
    border: 1px solid var(--border);
    padding: 20px 24px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    position: relative;
    overflow: hidden;
    transition: all 0.2s;
    border-radius: 2px;
  }
  .stat-card:hover {
    border-color: rgba(10,10,10,0.2);
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }

  .prog-bar { height: 3px; background: var(--cream-dark); overflow: hidden; border-radius: 3px; }
  .prog-fill {
    height: 100%;
    background: #0a0a0a;
    transition: width 0.3s;
    border-radius: 3px;
  }

  .h-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
  .h-dot.ok  { background: var(--emerald); box-shadow: 0 0 0 3px rgba(15,157,110,0.15); }
  .h-dot.err { background: var(--ruby);    box-shadow: 0 0 0 3px rgba(220,38,38,0.15); }
  .h-dot.unk { background: var(--text-muted); }
  .h-dot.proc{ background: var(--amber);   box-shadow: 0 0 0 3px rgba(217,119,6,0.15); animation:pulse 1.6s ease infinite; }

  .toast {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-left: 3px solid;
    border-radius: 2px;
    animation: fadeUp 0.25s ease;
    min-width: 280px;
    max-width: 400px;
    backdrop-filter: blur(10px);
  }

  hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 20px 0;
  }

  .dropzone {
    border: 2px dashed var(--border);
    border-radius: 4px;
    padding: 40px;
    text-align: center;
    cursor: pointer;
    background: var(--surface-2);
    transition: all 0.25s cubic-bezier(0.2,0.8,0.4,1);
  }
  .dropzone:hover {
    border-color: rgba(10,10,10,0.35);
    background: rgba(10,10,10,0.025);
  }
  .dropzone.dragging {
    border-color: #0a0a0a;
    background: rgba(10,10,10,0.045);
    box-shadow: inset 0 0 0 4px rgba(10,10,10,0.03);
  }

  .doc-item {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 16px;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.2,0.8,0.4,1);
  }
  .doc-item:hover {
    border-color: rgba(10,10,10,0.2);
    background: #ffffff;
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
  }
  .doc-item.selected {
    background: linear-gradient(135deg, #ffffff 0%, #faf7f1 100%);
    border-color: #0a0a0a;
    box-shadow: 0 0 0 3px rgba(10,10,10,0.06), var(--shadow-sm);
  }

  .quote-block {
    background: linear-gradient(135deg, #fdfbf6 0%, #faf5ea 100%);
    border-left: 3px solid #0a0a0a;
    padding: 20px 24px;
    font-size: 0.95rem;
    color: #0a0a0a;
    line-height: 1.75;
    white-space: pre-wrap;
    border-radius: 0 3px 3px 0;
  }

  .empty-state {
    text-align: center;
    padding: 48px 24px;
    color: var(--text-muted);
  }
  .empty-state .icon { font-size: 2rem; margin-bottom: 14px; opacity: 0.55; }
`;

/* ─── Toast ─── */
let _setToasts = null;
const toast = {
  _push(type, msg) {
    const id = Date.now() + Math.random();
    _setToasts?.(p => [...p, { id, type, msg }]);
    setTimeout(() => _setToasts?.(p => p.filter(t => t.id !== id)), 4000);
  },
  success: m => toast._push('success', m),
  error:   m => toast._push('error', m),
  warn:    m => toast._push('warn', m),
  info:    m => toast._push('info', m),
};
const TOAST_CFG = {
  success: { accent:'#0f9d6e', icon:'✓' },
  error:   { accent:'#dc2626', icon:'✕' },
  warn:    { accent:'#d97706', icon:'!' },
  info:    { accent:'#2563eb', icon:'i' },
};
function Toasts() {
  const [toasts, setToasts] = useState([]);
  useEffect(() => { _setToasts = setToasts; }, []);
  return (
    <div style={{ position:'fixed', bottom:24, right:24, zIndex:9999, display:'flex', flexDirection:'column', gap:12, pointerEvents:'none' }}>
      {toasts.map(t => {
        const c = TOAST_CFG[t.type];
        return (
          <div key={t.id} className="toast"
            style={{
              background:'#ffffff',
              border:'1px solid var(--border)',
              borderLeft:`3px solid ${c.accent}`,
              boxShadow:'0 18px 40px -18px rgba(10,10,10,0.32)'
            }}>
            <span style={{
              width:22, height:22, borderRadius:'50%',
              background:`${c.accent}18`, color:c.accent,
              display:'inline-flex', alignItems:'center', justifyContent:'center',
              fontWeight:800, fontSize:'0.72rem', flexShrink:0
            }}>{c.icon}</span>
            <span style={{ fontWeight:500, color:'#0a0a0a' }}>{t.msg}</span>
          </div>
        );
      })}
    </div>
  );
}

/* ─── Helpers ─── */
const fmt = {
  bytes: b => { if (!b) return '0 B'; const k=1024,s=['B','KB','MB','GB'],i=Math.floor(Math.log(b)/Math.log(k)); return (b/k**i).toFixed(1)+' '+s[i]; },
  date:  d => d ? new Date(d).toLocaleString() : '—',
  cut:   (s,n=80) => s && s.length>n ? s.slice(0,n)+'…' : (s||''),
};

// Normalize different backend list shapes into a plain array
function normalizeList(payload) {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload?.results)) return payload.results;
  if (Array.isArray(payload?.data?.results)) return payload.data.results;
  return [];
}

// Normalize single-object response
function normalizeData(payload) {
  return payload?.data ?? payload;
}

/* ─── UI Primitives ─── */
function SectLabel({ children }) {
  return <div className="sect-label">{children}</div>;
}
function Badge({ children, color, gold }) {
  const style = gold
    ? { borderColor:'rgba(10,10,10,0.25)', color:'#0a0a0a', background:'rgba(10,10,10,0.05)' }
    : { borderColor:`${color}40`, color, background:`${color}12` };
  return <span className="badge" style={style}>{children}</span>;
}
function Card({ children, style={}, className='' }) {
  return <div className={`luxury-card ${className}`} style={{ padding:24, ...style }}>{children}</div>;
}
function PrimaryBtn({ children, loading, loadText='Processing…', style={}, ...props }) {
  return (
    <button className="btn-primary" style={{ ...style }} {...props}>
      {loading ? (
        <span style={{ display:'flex', alignItems:'center', gap:8, justifyContent:'center' }}>
          <span className="anim-spin" style={{ width:14, height:14, border:'2px solid rgba(255,255,255,0.3)', borderTop:'2px solid #ffffff', borderRadius:'50%', display:'inline-block' }} />
          {loadText}
        </span>
      ) : children}
    </button>
  );
}
function HDot({ status }) {
  const cls = status==='ready' ? 'ok' : status==='processing' ? 'proc' : status==='error' ? 'err' : 'unk';
  return <span className={`h-dot ${cls}`} />;
}

/* ═══════════════════════════════════ MAIN ═══════════════════════════════════ */
export default function AIDocumentProcessing() {
  const [mounted, setMounted] = useState(false);
  const [tab, setTab] = useState('documents');
  const [loading, setLoading] = useState(false);

  /* Documents */
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);   // always a string
  const [docStatus, setDocStatus] = useState({});
  const [docDetails, setDocDetails] = useState(null);

  /* Upload */
  const [file, setFile] = useState(null);
  const [uploadPct, setUploadPct] = useState(0);
  const [dragging, setDragging] = useState(false);
  const fileRef = useRef();

  /* Extraction */
  const [extractionFields, setExtractionFields] = useState('');
  const [extractionResult, setExtractionResult] = useState(null);

  /* Summary */
  const [summaryResult, setSummaryResult] = useState(null);

  /* ─ Init ─ */
  useEffect(() => {
    setMounted(true);
    fetchDocuments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* ─── API Functions ─── */

  // GET /api/v1/documents/
  const fetchDocuments = async () => {
    try {
      console.log('[API] GET /api/v1/documents/');
      const r = await AxiosInstance.get('/api/v1/documents/');
      console.log('[API] documents list response:', r.data);
      const list = normalizeList(r.data);
      setDocuments(list);
    } catch (e) {
      console.error('[API] fetchDocuments failed:', e?.response?.status, e?.response?.data || e.message);
      toast.error(e.response?.data?.detail || `Failed to fetch documents (${e.response?.status || 'network'})`);
    }
  };

  // GET /api/v1/documents/{id}/status/
  const checkDocumentStatus = async (docId) => {
    try {
      const r = await AxiosInstance.get(`/api/v1/documents/${docId}/status/`);
      console.log(`[API] status ${docId}:`, r.data);
      const data = normalizeData(r.data);
      setDocStatus(prev => ({ ...prev, [docId]: data }));
      return data;
    } catch (e) {
      console.error(`[API] status ${docId} failed:`, e?.response?.status, e?.response?.data || e.message);
      return null;
    }
  };

  // GET /api/v1/documents/{id}/
  const getDocumentDetails = async (docId) => {
    try {
      const r = await AxiosInstance.get(`/api/v1/documents/${docId}/`);
      console.log(`[API] details ${docId}:`, r.data);
      const data = normalizeData(r.data);
      setDocDetails(data);
      return data;
    } catch (e) {
      console.error(`[API] details ${docId} failed:`, e?.response?.status, e?.response?.data || e.message);
      return null;
    }
  };

  // POST /api/v1/documents/upload  (NO trailing slash — matches your backend)
  const uploadDocument = async () => {
    if (!file) { toast.warn('Select a file first'); return; }
    const fd = new FormData();
    fd.append('file', file);
    setLoading(true);
    setUploadPct(0);
    try {
      console.log('[API] POST /api/v1/documents/upload', file.name);
      const r = await AxiosInstance.post('/api/v1/documents/upload', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: e => setUploadPct(e.total ? Math.round(e.loaded * 100 / e.total) : 50),
      });
      console.log('[API] upload response:', r.data);
      toast.success('Document uploaded successfully');
      setFile(null);
      setUploadPct(0);
      await fetchDocuments();

      const docId = r.data?.data?.document_id ?? r.data?.document_id;
      if (docId) pollDocumentStatus(docId);
    } catch (e) {
      console.error('[API] upload failed:', e?.response?.status, e?.response?.data || e.message);
      toast.error(e.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const pollDocumentStatus = (docId) => {
    const interval = setInterval(async () => {
      const status = await checkDocumentStatus(docId);
      if (status && (status.status === 'ready' || status.status === 'error')) {
        clearInterval(interval);
        fetchDocuments();
      }
    }, 3000);
  };

  // DELETE /api/v1/documents/{id}/
  const deleteDocument = async (docId, filename) => {
    if (!confirm(`Delete "${filename}"?`)) return;
    try {
      console.log(`[API] DELETE /api/v1/documents/${docId}/`);
      await AxiosInstance.delete(`/api/v1/documents/${docId}/`);
      toast.success('Document deleted');
      if (String(selectedDoc) === String(docId)) setSelectedDoc(null);
      fetchDocuments();
    } catch (e) {
      console.error('[API] delete failed:', e?.response?.status, e?.response?.data || e.message);
      toast.error(e.response?.data?.detail || 'Delete failed');
    }
  };

  // POST /api/v1/extraction/structured/
  const submitExtraction = async () => {
    if (!extractionFields.trim()) { toast.warn('Enter fields to extract first'); return; }
    if (!selectedDoc) { toast.warn('Select a document first'); return; }

    const fields = extractionFields.split(',').map(f => f.trim()).filter(Boolean);
    if (fields.length === 0) { toast.warn('Enter at least one field'); return; }

    setLoading(true);
    try {
      const payload = { document_id: selectedDoc, fields };
      console.log('[API] POST /api/v1/extraction/structured/', payload);
      const r = await AxiosInstance.post('/api/v1/extraction/structured/', payload);
      console.log('[API] extraction response:', r.data);
      setExtractionResult(normalizeData(r.data));
      toast.success('Extraction completed');
    } catch (e) {
      console.error('[API] extraction failed:', e?.response?.status, e?.response?.data || e.message);
      toast.error(e.response?.data?.detail || 'Extraction failed');
    } finally {
      setLoading(false);
    }
  };

  // POST /api/v1/documents/{id}/summary/
  const generateSummary = async () => {
    if (!selectedDoc) { toast.warn('Select a document first'); return; }
    setLoading(true);
    try {
      console.log(`[API] POST /api/v1/documents/${selectedDoc}/summary/`);
      const r = await AxiosInstance.post(`/api/v1/documents/${selectedDoc}/summary/`);
      console.log('[API] summary response:', r.data);
      setSummaryResult(normalizeData(r.data));
      toast.success('Summary generated');
    } catch (e) {
      console.error('[API] summary failed:', e?.response?.status, e?.response?.data || e.message);
      toast.error(e.response?.data?.detail || 'Summary generation failed');
    } finally {
      setLoading(false);
    }
  };

  // GET /api/v1/documents/{id}/report/
  const downloadReport = async () => {
    if (!selectedDoc) { toast.warn('Select a document first'); return; }
    try {
      console.log(`[API] GET /api/v1/documents/${selectedDoc}/report/`);
      const r = await AxiosInstance.get(`/api/v1/documents/${selectedDoc}/report/`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([r.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${selectedDoc}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('Report downloaded');
    } catch (e) {
      console.error('[API] report download failed:', e?.response?.status, e?.response?.data || e.message);
      toast.error('Report download failed');
    }
  };

  /* ─── Drag-drop ─── */
  const onDrop = useCallback(e => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f && f.type === 'application/pdf') {
      setFile(f);
    } else {
      toast.warn('Please upload a PDF file');
    }
  }, []);

  const onDragOver = useCallback(e => {
    e.preventDefault();
    setDragging(true);
  }, []);

  const onDragLeave = useCallback(e => {
    e.preventDefault();
    setDragging(false);
  }, []);

  /* ─── TABS ─── */
  const TABS = [
    { id:'documents',  label:'Documents' },
    { id:'extraction', label:'Extraction' },
    { id:'summary',    label:'Summary' },
  ];

  return (
    <>
      {mounted && <style suppressHydrationWarning>{GLOBAL_CSS}</style>}
      <Toasts />

      <div className="font-sans page-bg" style={{ minHeight:'100vh', color:'#0a0a0a', position:'relative', zIndex:1 }}>

        {/* ═══ HEADER ═══ */}
        <header style={{
          background:'rgba(255,255,255,0.9)',
          backdropFilter:'blur(20px)',
          WebkitBackdropFilter:'blur(20px)',
          borderBottom:'1px solid var(--border)',
          position:'sticky',
          top:0,
          zIndex:40,
          boxShadow:'0 1px 0 rgba(10,10,10,0.05), 0 10px 30px -24px rgba(10,10,10,0.35)'
        }}>
          <div style={{ height:2, background:'#0a0a0a' }} />
          <div style={{ maxWidth:1400, margin:'0 auto', padding:'0 32px', height:72, display:'flex', alignItems:'center', justifyContent:'space-between' }}>
            <div style={{ display:'flex', alignItems:'center', gap:24 }}>
              <div style={{
                width:42, height:42,
                background:'#0a0a0a',
                display:'flex', alignItems:'center', justifyContent:'center',
                borderRadius:2,
                boxShadow:'0 8px 20px -10px rgba(10,10,10,0.7), inset 0 0 0 1px rgba(216,185,94,0.35)'
              }}>
                <span className="font-serif gold-text" style={{ fontSize:'1.4rem', fontWeight:700 }}>AI</span>
              </div>
              <div>
                <div className="font-serif" style={{ fontSize:'1.45rem', letterSpacing:'0.02em', lineHeight:1.2, color:'#0a0a0a' }}>
                  Document Processing
                </div>
                <div className="font-mono" style={{ fontSize:'0.6rem', letterSpacing:'0.22em', color:'var(--text-muted)', textTransform:'uppercase', marginTop:4 }}>
                  Extraction · Summary · Reports
                </div>
              </div>
            </div>
            <div style={{ display:'flex', alignItems:'center', gap:24 }}>
              <div style={{
                display:'flex', alignItems:'center', gap:10,
                border:'1px solid #0a0a0a',
                background:'#ffffff',
                padding:'7px 16px',
                borderRadius:2
              }}>
                <span style={{ width:6, height:6, borderRadius:'50%', background:'#0a0a0a', display:'inline-block' }} />
                <span className="font-mono" style={{ fontSize:'0.65rem', letterSpacing:'0.12em', textTransform:'uppercase', color:'#0a0a0a' }}>
                  {documents.length} Documents
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* ═══ TABS ═══ */}
        <div style={{ background:'rgba(255,255,255,0.65)', backdropFilter:'blur(10px)', borderBottom:'1px solid var(--border)', overflowX:'auto' }}>
          <div style={{ maxWidth:1400, margin:'0 auto', padding:'0 32px', display:'flex' }}>
            {TABS.map(t => (
              <button key={t.id} className={`tab-btn ${tab===t.id?'active':''}`}
                onClick={() => setTab(t.id)}>
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* ═══ CONTENT ═══ */}
        <main style={{ maxWidth:1400, margin:'0 auto', padding:'32px 32px 60px' }}>

          {/* ── DOCUMENTS TAB ── */}
          {tab==='documents' && (
            <div style={{ display:'grid', gridTemplateColumns:'1fr 2fr', gap:24, alignItems:'start' }}>

              {/* Upload Panel */}
              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                <Card>
                  <SectLabel>Upload Document</SectLabel>
                  <div
                    className={`dropzone ${dragging ? 'dragging' : ''}`}
                    onDrop={onDrop}
                    onDragOver={onDragOver}
                    onDragLeave={onDragLeave}
                    onClick={() => fileRef.current?.click()}
                  >
                    <input
                      ref={fileRef}
                      type="file"
                      accept=".pdf"
                      style={{ display: 'none' }}
                      onChange={e => {
                        const f = e.target.files[0];
                        if (f && f.type === 'application/pdf') {
                          setFile(f);
                        } else {
                          toast.warn('Please upload a PDF file');
                        }
                      }}
                    />
                    <div style={{ fontSize: '2rem', marginBottom: 12, opacity: 0.7 }}>📄</div>
                    <div style={{ color: '#0a0a0a', marginBottom: 8, fontWeight: 500 }}>
                      {file ? file.name : 'Drag & drop PDF here or click to browse'}
                    </div>
                    <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
                      PDF files only, max 10MB
                    </div>
                  </div>

                  {file && (
                    <div style={{ marginTop: 16 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                        <span className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a' }}>
                          {file.name}
                        </span>
                        <span className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', fontWeight: 700 }}>
                          {fmt.bytes(file.size)}
                        </span>
                      </div>
                      {uploadPct > 0 && (
                        <div className="prog-bar" style={{ marginBottom: 12 }}>
                          <div className="prog-fill" style={{ width: `${uploadPct}%` }} />
                        </div>
                      )}
                      <div style={{ display: 'flex', gap: 12 }}>
                        <PrimaryBtn loading={loading} loadText="Uploading…" onClick={uploadDocument} disabled={loading} style={{ flex: 1 }}>
                          Upload
                        </PrimaryBtn>
                        <button className="btn-ghost" onClick={() => { setFile(null); setUploadPct(0); }}>
                          Clear
                        </button>
                      </div>
                    </div>
                  )}
                </Card>

                <Card>
                  <SectLabel>Document Stats</SectLabel>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
                    <div style={{
                      background:'linear-gradient(135deg, #fdfbf6, #faf5ea)',
                      border:'1px solid var(--border)',
                      borderRadius:3,
                      padding:'14px 16px'
                    }}>
                      <div className="font-mono" style={{ fontSize: '0.62rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.1em', textTransform:'uppercase' }}>Total</div>
                      <div className="font-serif" style={{ fontSize: '1.9rem', color: '#0a0a0a', lineHeight:1 }}>{documents.length}</div>
                    </div>
                    <div style={{
                      background:'linear-gradient(135deg, #f6fdfa, #eefaf4)',
                      border:'1px solid rgba(15,157,110,0.18)',
                      borderRadius:3,
                      padding:'14px 16px'
                    }}>
                      <div className="font-mono" style={{ fontSize: '0.62rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.1em', textTransform:'uppercase' }}>Ready</div>
                      <div className="font-serif" style={{ fontSize: '1.9rem', color: '#0a0a0a', lineHeight:1 }}>
                        {documents.filter(d => d.status === 'ready').length}
                      </div>
                    </div>
                  </div>
                </Card>
              </div>

              {/* Documents List */}
              <Card>
                <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
                  <SectLabel>Document Library</SectLabel>
                  <button
                    className="btn-ghost"
                    onClick={fetchDocuments}
                    style={{ padding:'7px 14px', fontSize:'0.62rem', marginBottom:20 }}
                  >
                    Refresh
                  </button>
                </div>
                {documents.length === 0 ? (
                  <div className="empty-state">
                    <div className="icon">📭</div>
                    <div>No documents uploaded yet</div>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    {documents.map(doc => (
                      <div
                        key={doc.id}
                        className={`doc-item ${String(selectedDoc) === String(doc.id) ? 'selected' : ''}`}
                        onClick={() => {
                          setSelectedDoc(String(doc.id));
                          getDocumentDetails(doc.id);
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 8 }}>
                          <div style={{ flex: 1, minWidth: 0 }}>
                            <div style={{ fontWeight: 600, marginBottom: 4, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap', color:'#0a0a0a' }}>
                              {doc.filename || doc.file_name || doc.name || `Document #${doc.id}`}
                            </div>
                            <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                              {doc.file_size_mb ? `${fmt.bytes(doc.file_size_mb * 1024 * 1024)} • ` : ''}
                              {doc.page_count || '?'} pages
                            </div>
                          </div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink:0 }}>
                            <HDot status={doc.status} />
                            <Badge color={doc.status === 'ready' ? '#0f9d6e' : doc.status === 'processing' ? '#d97706' : '#dc2626'}>
                              {doc.status || 'unknown'}
                            </Badge>
                          </div>
                        </div>
                        {doc.progress && doc.progress < 100 && (
                          <div className="prog-bar" style={{ marginTop: 8 }}>
                            <div className="prog-fill" style={{ width: `${doc.progress}%` }} />
                          </div>
                        )}
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 }}>
                          <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>
                            {fmt.date(doc.created_at)}
                          </div>
                          <button
                            className="btn-danger"
                            onClick={(e) => { e.stopPropagation(); deleteDocument(doc.id, doc.filename || doc.file_name); }}
                            style={{ padding: '6px 14px', fontSize: '0.62rem' }}
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            </div>
          )}

          {/* ── EXTRACTION TAB ── */}
          {tab==='extraction' && (
            <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                <Card>
                  <SectLabel>Document Selection</SectLabel>
                  <select
                    className="inp"
                    value={selectedDoc || ''}
                    onChange={e => setSelectedDoc(e.target.value)}
                    style={{ marginBottom: 20 }}
                  >
                    <option value="">Select a document...</option>
                    {documents.filter(d => d.status === 'ready').map(d => (
                      <option key={d.id} value={String(d.id)}>
                        {d.filename || d.file_name || `Document #${d.id}`}
                      </option>
                    ))}
                  </select>

                  <SectLabel>Fields to Extract</SectLabel>
                  <textarea
                    className="inp"
                    rows={4}
                    value={extractionFields}
                    onChange={e => setExtractionFields(e.target.value)}
                    placeholder="Enter fields separated by commas (e.g., company_name, revenue, employees, founded_year)"
                    style={{ marginBottom: 16, resize: 'vertical' }}
                  />

                  <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 16 }}>
                    Maximum 20 fields per request
                  </div>

                  <PrimaryBtn loading={loading} loadText="Extracting…" onClick={submitExtraction} disabled={loading || !selectedDoc} style={{ width: '100%' }}>
                    Extract Fields
                  </PrimaryBtn>
                </Card>
              </div>

              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                {extractionResult ? (
                  <Card>
                    <SectLabel>Extraction Results</SectLabel>
                    <div style={{ marginBottom: 16 }}>
                      {extractionResult.filename && (
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8 }}>
                          Document: {extractionResult.filename}
                        </div>
                      )}
                      {extractionResult.model && (
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                          Model: {extractionResult.model}
                        </div>
                      )}
                    </div>

                    {extractionResult.fields && typeof extractionResult.fields === 'object' ? (
                      <div style={{ display: 'grid', gap: 12 }}>
                        {Object.entries(extractionResult.fields).map(([field, data]) => (
                          <div key={field} style={{ background:'var(--surface-2)', padding: 16, borderRadius: 3, border: '1px solid var(--border)' }}>
                            <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.06em' }}>
                              {field}
                            </div>
                            <div style={{ fontSize: '0.9rem', color: '#0a0a0a', marginBottom: 8, lineHeight:1.6 }}>
                              {(data && typeof data === 'object' ? (data.value ?? 'Not found') : (data || 'Not found'))}
                            </div>
                            {data && typeof data === 'object' && data.status && (
                              <Badge color={data.status === 'found' ? '#0f9d6e' : data.status === 'not_found' ? '#dc2626' : '#d97706'}>
                                {data.status}
                              </Badge>
                            )}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div style={{
                        background:'var(--surface-2)',
                        border:'1px solid var(--border)',
                        padding:16,
                        borderRadius:3,
                        fontFamily:"'JetBrains Mono', monospace",
                        fontSize:'0.75rem',
                        whiteSpace:'pre-wrap',
                        color:'#0a0a0a',
                        maxHeight:520,
                        overflow:'auto'
                      }}>
                        {JSON.stringify(extractionResult, null, 2)}
                      </div>
                    )}
                  </Card>
                ) : (
                  <Card>
                    <div className="empty-state">
                      <div className="icon">⚡</div>
                      <div>Extraction results will appear here</div>
                    </div>
                  </Card>
                )}
              </div>
            </div>
          )}

          {/* ── SUMMARY TAB ── */}
          {tab==='summary' && (
            <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:24, alignItems:'start' }}>

              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                <Card>
                  <SectLabel>Document Selection</SectLabel>
                  <select
                    className="inp"
                    value={selectedDoc || ''}
                    onChange={e => setSelectedDoc(e.target.value)}
                    style={{ marginBottom: 20 }}
                  >
                    <option value="">Select a document...</option>
                    {documents.filter(d => d.status === 'ready').map(d => (
                      <option key={d.id} value={String(d.id)}>
                        {d.filename || d.file_name || `Document #${d.id}`}
                      </option>
                    ))}
                  </select>

                  <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
                    <PrimaryBtn loading={loading} loadText="Generating…" onClick={generateSummary} disabled={loading || !selectedDoc} style={{ flex: 1 }}>
                      Generate Summary
                    </PrimaryBtn>
                    <button
                      className="btn-ghost"
                      onClick={downloadReport}
                      disabled={!selectedDoc}
                      style={{ flex: 1 }}
                    >
                      Download Report
                    </button>
                  </div>

                  <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', lineHeight:1.6 }}>
                    Summary uses AI to analyze document content and extract key information
                  </div>
                </Card>

                {selectedDoc && (
                  <Card>
                    <SectLabel>Document Info</SectLabel>
                    {(() => {
                      const doc = documents.find(d => String(d.id) === String(selectedDoc));
                      return doc ? (
                        <div style={{ display: 'grid', gap: 12 }}>
                          <div>
                            <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Filename</div>
                            <div style={{ fontWeight:500, color:'#0a0a0a' }}>{doc.filename || doc.file_name}</div>
                          </div>
                          {doc.file_size_mb && (
                            <div>
                              <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Size</div>
                              <div style={{ color:'#0a0a0a' }}>{fmt.bytes(doc.file_size_mb * 1024 * 1024)}</div>
                            </div>
                          )}
                          <div>
                            <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Pages</div>
                            <div style={{ color:'#0a0a0a' }}>{doc.page_count || 'Processing...'}</div>
                          </div>
                          <div>
                            <div className="font-mono" style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginBottom: 4, letterSpacing:'0.08em', textTransform:'uppercase' }}>Status</div>
                            <Badge color={doc.status === 'ready' ? '#0f9d6e' : '#d97706'}>{doc.status}</Badge>
                          </div>
                        </div>
                      ) : null;
                    })()}
                  </Card>
                )}
              </div>

              <div style={{ display:'flex', flexDirection:'column', gap:20 }}>
                {summaryResult ? (
                  <Card>
                    <SectLabel>AI Summary</SectLabel>
                    {summaryResult.model && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8 }}>
                          Model: {summaryResult.model}
                        </div>
                      </div>
                    )}

                    {summaryResult.executive_summary && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
                          Executive Summary
                        </div>
                        <div className="quote-block">{summaryResult.executive_summary}</div>
                      </div>
                    )}

                    {Array.isArray(summaryResult.key_points) && summaryResult.key_points.length > 0 && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
                          Key Points
                        </div>
                        <ul style={{ margin: 0, paddingLeft: 20, color:'#0a0a0a' }}>
                          {summaryResult.key_points.map((point, i) => (
                            <li key={i} style={{ marginBottom: 8, lineHeight: 1.65 }}>{point}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {Array.isArray(summaryResult.important_facts) && summaryResult.important_facts.length > 0 && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
                          Important Facts
                        </div>
                        <ul style={{ margin: 0, paddingLeft: 20, color:'#0a0a0a' }}>
                          {summaryResult.important_facts.map((fact, i) => (
                            <li key={i} style={{ marginBottom: 8, lineHeight: 1.65 }}>{fact}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {Array.isArray(summaryResult.important_numbers) && summaryResult.important_numbers.length > 0 && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
                          Important Numbers
                        </div>
                        <ul style={{ margin: 0, paddingLeft: 20, color:'#0a0a0a' }}>
                          {summaryResult.important_numbers.map((num, i) => (
                            <li key={i} style={{ marginBottom: 8, lineHeight: 1.65 }}>{num}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {Array.isArray(summaryResult.risks) && summaryResult.risks.length > 0 && (
                      <div style={{ marginBottom: 20 }}>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: 'var(--ruby)', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
                          Risks
                        </div>
                        <ul style={{ margin: 0, paddingLeft: 20 }}>
                          {summaryResult.risks.map((risk, i) => (
                            <li key={i} style={{ marginBottom: 8, lineHeight: 1.65, color: 'var(--ruby)' }}>{risk}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {summaryResult.conclusion && (
                      <div>
                        <div className="font-mono" style={{ fontSize: '0.7rem', color: '#0a0a0a', marginBottom: 8, fontWeight: 700, letterSpacing:'0.1em', textTransform:'uppercase' }}>
                          Conclusion
                        </div>
                        <div className="quote-block">{summaryResult.conclusion}</div>
                      </div>
                    )}

                    {/* Fallback: raw JSON if the shape isn't one of the known keys */}
                    {!summaryResult.executive_summary &&
                     !summaryResult.key_points &&
                     !summaryResult.important_facts &&
                     !summaryResult.important_numbers &&
                     !summaryResult.risks &&
                     !summaryResult.conclusion && (
                      <div style={{
                        background:'var(--surface-2)',
                        border:'1px solid var(--border)',
                        padding:16,
                        borderRadius:3,
                        fontFamily:"'JetBrains Mono', monospace",
                        fontSize:'0.75rem',
                        whiteSpace:'pre-wrap',
                        color:'#0a0a0a',
                        maxHeight:520,
                        overflow:'auto'
                      }}>
                        {JSON.stringify(summaryResult, null, 2)}
                      </div>
                    )}
                  </Card>
                ) : (
                  <Card>
                    <div className="empty-state">
                      <div className="icon">📋</div>
                      <div>Select a document and generate summary</div>
                    </div>
                  </Card>
                )}
              </div>
            </div>
          )}

        </main>
      </div>
    </>
  );
}