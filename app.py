"""Avant l'IA, il y avait nous — l'application compagnon du livre.

Lancer :  streamlit run app.py
"""

import streamlit as st

import ui
from content import BOOK, PARTS, CHAPTERS, chapters_of, get_chapter

# Valeurs de secours : l'application fonctionne même avec une ancienne version de content.py
BOOK = dict(BOOK)
BOOK["author"] = "Amine CHAÏBI"
BOOK.setdefault("author_title", "Docteur en informatique · Spécialiste de l'apprentissage automatique")
BOOK.setdefault("author_bio", [
    "Docteur en informatique, spécialiste de l'apprentissage automatique (machine learning) et de la fouille de données. "
    "Thèse soutenue en 2013 au Laboratoire d'informatique de Paris-Nord (LIPN), Université Paris 13, "
    "sur l'apprentissage topologique non supervisé.",
    "Il a enseigné l'algorithmique et les bases de données à l'université, avant de poursuivre son parcours "
    "dans l'industrie, autour de la data science et de l'apprentissage automatique. Il a aussi publié des chroniques sur le Journal du Net.",
    "L'idée du livre est née d'un atelier sur les algorithmes inspirés des fourmis : raconter les liens entre "
    "l'intelligence humaine, la nature et l'IA, sans exiger la moindre connaissance technique.",
])
BOOK.setdefault("links", [
    ("Publications scientifiques (DBLP)", "https://dblp.org/pid/116/6363"),
    ("Chroniques sur le Journal du Net", "https://www.journaldunet.com/account/amine-chaibi-17708"),
])
_TITRES_DU_LIVRE = {1: "Un kilo et demi de mystère", 5: "Le jardinier de solutions"}
for _c in CHAPTERS:
    _c["title"] = _TITRES_DU_LIVRE.get(_c["num"], _c["title"])
from demos import REGISTRY

st.set_page_config(page_title=BOOK["title"], page_icon="🐜", layout="wide",
                   initial_sidebar_state="collapsed")

# ───────────────────────────── Style : « observatoire de nuit » ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');
:root {
  --bg: #0F141B; --panel: #161D27; --panel2: #1B2330; --line: #263040; --ink: #E8ECF2; --muted: #8A94A6;
  --amber: #F2B544; --cyan: #5CC8D7;
  --title: 'Manrope', 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --body: 'Inter', 'Helvetica Neue', Arial, sans-serif;
}
html, body, .stApp, .stMarkdown, button, input, select, textarea, label, p {font-family: var(--body) !important;}
.stApp {background: radial-gradient(1200px 600px at 85% -10%, rgba(242,181,68,0.08), transparent 60%),
                     radial-gradient(900px 500px at -10% 10%, rgba(92,200,215,0.06), transparent 60%), var(--bg);}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"],
[data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"] {display: none !important;}
[data-testid="stHeader"] {background: transparent; height: 0;}
.block-container {max-width: 1120px; padding-top: 1.6rem; padding-bottom: 5rem;}

/* Auteur */
.brand small {font-family: var(--body); font-weight: 500; font-size: .85rem; color: var(--muted); letter-spacing: .02em;}
.byline {display: flex; gap: .9rem; align-items: center; margin: 1.4rem 0 .2rem;}
.byline b {display: block; font-family: var(--title); font-size: 1.05rem; color: var(--ink); letter-spacing: .03em;}
.byline span {font-size: .88rem; color: var(--muted);}
.mono-av {width: 46px; height: 46px; flex: 0 0 46px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
          font-family: var(--title); font-weight: 800; color: var(--bg); background: linear-gradient(135deg, var(--amber), var(--cyan));}
.mono-av.big {width: 84px; height: 84px; flex-basis: 84px; font-size: 1.6rem;}
.about {margin-top: 4rem; padding: 2rem; border-radius: 22px; background: var(--panel); border: 1px solid var(--line);}
.about-grid {display: flex; gap: 1.6rem; align-items: flex-start; margin-top: 1rem;}
.about-name {font-family: var(--title); font-weight: 800; font-size: 1.6rem; color: var(--ink); letter-spacing: .02em;}
.about-title {color: var(--amber); font-size: .92rem; margin-bottom: .9rem;}
.about p {color: #C9D1DC; line-height: 1.65; font-size: 1rem; margin: 0 0 .7rem;}
.about-links {display: flex; gap: 1.2rem; flex-wrap: wrap; margin-top: .6rem;}
.about-links a {color: var(--cyan) !important; text-decoration: none; font-weight: 600; font-size: .92rem;}
.footer {margin-top: 3.5rem; padding-top: 1.4rem; border-top: 1px solid var(--line); text-align: center;
         font-size: .82rem; color: var(--muted); line-height: 1.7;}
.footer b {color: var(--ink); font-weight: 600;}
@media (max-width: 700px) {.about-grid {flex-direction: column;}}

/* Barre du haut */
.brand {font-family: var(--title); font-weight: 800; font-size: 1.05rem; color: var(--ink); letter-spacing: -0.01em;
        padding-top: .45rem;}
.brand span {color: var(--amber);}
.topline {height: 1px; background: var(--line); margin: .9rem 0 2.2rem;}

/* Titres */
.kicker {display: inline-flex; gap: .5rem; align-items: center; font-size: .78rem; font-weight: 600; color: var(--amber);
         letter-spacing: .06em; text-transform: uppercase;}
.kicker::before {content: ""; width: 18px; height: 2px; background: var(--amber); display: inline-block;}
.hero {font-family: var(--title); font-weight: 800; font-size: clamp(2.3rem, 5vw, 3.8rem); line-height: 1.04;
       letter-spacing: -0.035em; color: var(--ink); margin: .8rem 0 1rem; max-width: 900px;}
.hero em {font-style: normal; background: linear-gradient(90deg, var(--amber), var(--cyan));
          -webkit-background-clip: text; background-clip: text; color: transparent;}
.lead {font-size: 1.18rem; line-height: 1.6; color: var(--muted); max-width: 720px;}
.meta {display: flex; gap: 1.8rem; margin: 1.6rem 0 .4rem; color: var(--muted); font-size: .9rem;}
.meta b {display: block; font-family: var(--title); font-size: 1.6rem; color: var(--ink); font-weight: 700;}

/* Sommaire */
.part {display: grid; grid-template-columns: 70px 1fr; gap: 1rem; margin-top: 2.6rem; align-items: end;
       padding-bottom: .8rem; border-bottom: 1px solid var(--line);}
.part .roman {font-family: var(--title); font-weight: 800; font-size: 2.2rem; color: var(--amber); line-height: 1;
              letter-spacing: .02em;}
.part .t {font-family: var(--title); font-weight: 700; font-size: 1.3rem; color: var(--ink);}
.part .l {font-size: .75rem; color: var(--muted); text-transform: uppercase; letter-spacing: .1em;}
.row-tag {font-size: .9rem; color: var(--muted); padding: .2rem 0 0 .2rem; line-height: 1.45;}

/* Lignes du sommaire = boutons */
 [class*="st-key-idx"] button {justify-content: flex-start; text-align: left; background: transparent; border: none;
  border-radius: 12px; padding: .85rem 1rem; min-height: 0; color: var(--ink); font-family: var(--title) !important;}
 [class*="st-key-idx"] button p {font-family: var(--title) !important; font-size: 1.12rem; font-weight: 700; text-align: left;}
 [class*="st-key-idx"] button > div {justify-content: flex-start; width: 100%;}
 [class*="st-key-idx"] button:hover {background: var(--panel); color: var(--amber);}

/* Page chapitre */
.bignum {font-family: var(--title); font-weight: 800; font-size: 7rem; line-height: .8; color: transparent;
         -webkit-text-stroke: 1.5px var(--amber); letter-spacing: -0.04em;}
.panel {background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 1.5rem 1.6rem; height: 100%;}
.panel .k {font-size: .74rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; margin-bottom: .7rem;}
.panel .v {font-size: 1.06rem; line-height: 1.65; color: var(--ink);}
.panel.nature .k {color: var(--cyan);} .panel.idea .k {color: var(--amber);}
.panel.idea {border-color: rgba(242,181,68,0.35); background: linear-gradient(160deg, rgba(242,181,68,0.08), var(--panel) 60%);}
.example {margin-top: 1.2rem; padding: 1.4rem 1.6rem; border-radius: 18px; background: var(--panel2);
          font-size: 1.08rem; line-height: 1.65; color: var(--ink);}
.example .k {font-size: .74rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin-bottom: .5rem;}
.neo {margin-top: 1.2rem; display: grid; grid-template-columns: 44px 1fr; gap: 1rem; align-items: start;
      padding: 1.2rem 1.4rem; border: 1px dashed var(--line); border-radius: 18px; color: var(--ink); font-size: 1.05rem; line-height: 1.6;}
.neo .av {width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg, var(--cyan), var(--amber));
          display: flex; align-items: center; justify-content: center; font-family: var(--title); font-weight: 800; color: var(--bg);}
.neo .who {font-size: .74rem; letter-spacing: .1em; text-transform: uppercase; color: var(--cyan); font-weight: 600;}

.timeline {position: relative; margin: .4rem 0 0 .6rem; padding-left: 2rem; border-left: 2px solid var(--line);}
.tl {position: relative; padding: .2rem 0 1.6rem;}
.tl::before {content: attr(data-n); position: absolute; left: -2.95rem; top: .05rem; width: 1.8rem; height: 1.8rem;
             border-radius: 50%; background: var(--bg); border: 2px solid var(--amber); color: var(--amber);
             font-family: var(--title); font-weight: 800; font-size: .85rem; display: flex; align-items: center; justify-content: center;}
.tl .t {font-size: 1.1rem; line-height: 1.6; color: var(--ink);}

.today {padding: 2rem; border-radius: 22px; background: linear-gradient(135deg, #1E2A3A, #142029);
        border: 1px solid var(--line); font-family: var(--title); font-size: 1.45rem; font-weight: 700;
        line-height: 1.4; color: var(--ink); letter-spacing: -0.01em;}

/* Éléments des démos */
.result {background: var(--panel2); border-radius: 14px; padding: 1rem 1.2rem; margin: .8rem 0;}
.result-label {font-size: .72rem; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); font-weight: 600;}
.result-value {font-family: var(--title); font-size: 1.5rem; font-weight: 800; color: var(--amber); margin: .15rem 0;}
.result-caption {font-size: .9rem; color: var(--muted);}
.mono {font-family: 'JetBrains Mono', ui-monospace, Menlo, monospace !important; font-size: 1.35rem; letter-spacing: .12em;
       text-align: center; padding: 1.1rem; background: var(--panel2); border-radius: 14px; color: var(--cyan); margin: .6rem 0;}
.quote {font-family: var(--title); font-size: 1.5rem; font-weight: 700; text-align: center; padding: 1.4rem 1rem;
        color: var(--ink); background: var(--panel2); border-radius: 16px; margin: .8rem 0;}
.duel {font-family: var(--title); font-size: 1.08rem; font-weight: 700; color: var(--ink); margin-top: 1.2rem;}
.verdict {font-size: .95rem; padding: .55rem .9rem; border-radius: 10px; margin-bottom: .4rem;}
.verdict.ok {background: rgba(123,211,137,0.12); color: #9BE3A7;} .verdict.ko {background: rgba(255,107,107,0.12); color: #FF9C9C;}

/* Composants Streamlit */
.stButton button {border-radius: 999px; border: 1px solid var(--line); background: var(--panel); color: var(--ink); font-weight: 500;}
.stButton button:hover {border-color: var(--amber); color: var(--amber);}
.stButton button[kind="primary"] {background: var(--amber); border-color: var(--amber); color: #1A1406; font-weight: 600;}
.stButton button[kind="primary"]:hover {background: #FFC860; color: #1A1406;}
.stTabs [data-baseweb="tab-list"] {gap: 1.8rem; border-bottom: 1px solid var(--line);}
.stTabs [data-baseweb="tab"] {background: transparent !important; padding: .5rem 0; height: auto;}
.stTabs [data-baseweb="tab"] p {font-family: var(--title) !important; font-weight: 700; font-size: 1rem; color: var(--muted);}
.stTabs [aria-selected="true"] p {color: var(--ink) !important;}
.stTabs [data-baseweb="tab-highlight"] {background: var(--amber) !important; height: 3px; border-radius: 3px;}
.stTabs [data-baseweb="tab-border"] {display: none;}
.stTabs [data-baseweb="tab-panel"] {padding-top: 1.6rem;}
[data-testid="stVerticalBlockBorderWrapper"] {border-color: var(--line) !important; border-radius: 18px;}
[data-testid="stCaptionContainer"] p {color: var(--muted);}

/* ── Démos pas à pas ── */
.scenario {font-size: 1.08rem; line-height: 1.6; color: var(--ink); padding: 1.1rem 1.3rem; border-radius: 14px;
           background: rgba(92,200,215,0.07); border: 1px solid rgba(92,200,215,0.25); margin-bottom: 1.2rem;}
.scenario span {display: block; font-size: .72rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--cyan); margin-bottom: .3rem;}
.stepinfo {text-align: center; font-size: .9rem; color: var(--muted); padding-top: .35rem;}
.stepinfo b {color: var(--ink); font-family: var(--title);}
.stepinfo .bar {height: 4px; background: var(--line); border-radius: 4px; margin-top: .45rem; overflow: hidden;}
.stepinfo .bar div {height: 100%; background: var(--amber); border-radius: 4px; transition: width .3s;}
.explain {margin: 1rem 0 .6rem;}
.explain .et {font-family: var(--title); font-weight: 800; font-size: 1.15rem; color: var(--ink); margin-bottom: .35rem;}
.explain .eb {font-size: 1.02rem; line-height: 1.65; color: #C9D1DC;}
.calc {font-family: 'JetBrains Mono', ui-monospace, Menlo, monospace; font-size: .9rem; line-height: 1.9; color: #C9D1DC;
       background: #0B1016; border: 1px solid var(--line); border-left: 3px solid var(--amber); border-radius: 10px;
       padding: .9rem 1.1rem; margin: .6rem 0 1rem; overflow-x: auto;}
.calc b {color: var(--amber);} .calc i {font-style: normal; color: var(--cyan);}
.take {margin-top: 1.4rem; padding: 1rem 1.2rem; border-radius: 14px; background: var(--panel2); font-size: 1rem; line-height: 1.6; color: var(--ink);}
.take span {display: block; font-size: .72rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--amber); margin-bottom: .3rem;}
.legend {font-size: .82rem; color: var(--muted); margin: .4rem 0 .8rem;}
.mini-t {font-family: var(--title); font-weight: 700; color: var(--ink); margin-bottom: .6rem;}
.quote mark {background: rgba(242,181,68,0.25); color: var(--amber); padding: 0 .3rem; border-radius: 6px;}
.kern {border-collapse: collapse;} .kern td {width: 38px; height: 34px; text-align: center; border: 1px solid var(--line);
       font-family: 'JetBrains Mono', monospace; color: var(--amber); background: #0B1016;}

/* mots (génétique) */
.word {display: inline-flex; gap: 3px; align-items: center;}
.lt {display: inline-flex; width: 26px; height: 30px; align-items: center; justify-content: center; border-radius: 6px;
     background: var(--panel2); color: var(--muted); font-family: 'JetBrains Mono', monospace; font-weight: 600;}
.lt.ok {background: rgba(123,211,137,0.18); color: #9BE3A7;}
.lt.mut {outline: 2px dashed var(--amber); outline-offset: 1px;}
.cut {width: 3px; height: 34px; background: var(--amber); border-radius: 2px; margin: 0 3px;}
.pop {display: flex; flex-direction: column; gap: 5px;}
.poprow {display: flex; justify-content: space-between; align-items: center; padding: 3px 8px; border-radius: 8px;}
.poprow.top {background: rgba(242,181,68,0.08);}
.poprow .sc {font-family: var(--title); font-weight: 700; color: var(--ink);}
.birth {display: flex; flex-direction: column; gap: .8rem;}
.birth small {display: block; color: var(--muted); font-size: .78rem; margin-bottom: .25rem;}

/* piste du robot */
.track {position: relative; height: 92px; margin: .6rem 0 1rem; border-bottom: 2px solid var(--line);}
.track .bot {position: absolute; bottom: 8px; font-size: 2.2rem; transform: translateX(-50%); transition: left .4s;}
.track .rec {position: absolute; top: 0; bottom: 0; border-left: 2px dashed var(--amber);}
.track .rec span {position: absolute; top: 0; left: 6px; font-size: .78rem; color: var(--amber); white-space: nowrap;}
.track .ticks {position: absolute; bottom: -24px; left: 0; right: 0; display: flex; justify-content: space-between; font-size: .72rem; color: var(--muted);}

/* morpion */
.board {display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; width: 100%; max-width: 230px; margin: 0 auto;}
.board .cell {aspect-ratio: 1; border-radius: 12px; background: var(--panel2); display: flex; align-items: center;
              justify-content: center; font-family: var(--title); font-weight: 800; font-size: 1.6rem; position: relative; color: var(--ink);}
.board .cell.x {color: var(--amber);} .board .cell.o {color: var(--cyan);}
.board .cell.sc {font-size: 1.05rem; color: var(--muted);}
.board .cell.best {background: var(--amber); color: #1A1406;}
.board .cell small {position: absolute; top: 4px; right: 7px; font-size: .62rem; color: var(--muted); font-weight: 500;}
.verdict-s {text-align: center; margin: .5rem 0 1rem; font-weight: 600; color: var(--muted);}
.verdict-s.win {color: var(--amber);} .verdict-s.loss {color: var(--cyan);}

/* machines à sous */
.machines {display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin: .8rem 0;}
.machine {background: var(--panel2); border: 1px solid var(--line); border-radius: 14px; padding: .8rem; text-align: center;}
.machine.on {border-color: var(--amber); box-shadow: 0 0 0 2px rgba(242,181,68,0.25);}
.machine .mi {font-size: 1.6rem;} .machine .mn {font-family: var(--title); font-weight: 700; color: var(--ink); font-size: .9rem;}
.machine .ms {font-size: .75rem; color: var(--muted); margin: .2rem 0 .4rem;}
.machine .mb {height: 6px; background: var(--line); border-radius: 6px; overflow: hidden;}
.machine .mb div {height: 100%; background: var(--amber);}
.machine .me {font-size: .8rem; color: var(--ink); margin-top: .3rem;} .machine .truth {font-size: .75rem; color: var(--cyan);}

/* patients */
.patients {display: flex; flex-wrap: wrap; gap: 6px; align-items: stretch; margin: .6rem 0;}
.pt {width: 46px; border-radius: 10px; padding: .3rem 0; text-align: center; position: relative; border: 1px solid var(--line); background: var(--panel2);}
.pt .ps {font-size: .72rem; color: var(--muted);} .pt .pi {font-size: 1.1rem;}
.pt .dot {position: absolute; top: 4px; right: 4px; width: 8px; height: 8px; border-radius: 50%; background: var(--red, #FF6B6B);}
.pt.tp {border-color: var(--amber); background: rgba(242,181,68,0.12);}
.pt.fn {border-color: #FF6B6B; background: rgba(255,107,107,0.12);}
.pt.fp {border-color: var(--cyan); background: rgba(92,200,215,0.10);}
.seuil {width: 3px; background: var(--amber); border-radius: 3px; position: relative; margin: 0 4px;}
.seuil span {position: absolute; top: -18px; left: 50%; transform: translateX(-50%); font-size: .7rem; color: var(--amber);}
.cats {display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 1rem 0;}
.cat {border-radius: 12px; padding: .8rem; font-size: .82rem; color: var(--muted); background: var(--panel2); border: 1px solid var(--line);}
.cat b {display: block; font-family: var(--title); font-size: 1.6rem; color: var(--ink);}
.cat.tp {border-color: var(--amber);} .cat.fn {border-color: #FF6B6B;} .cat.fp {border-color: var(--cyan);}
@media (max-width: 700px) {.machines {grid-template-columns: repeat(3, 1fr);} .cats {grid-template-columns: repeat(2, 1fr);}}
</style>
""", unsafe_allow_html=True)


# ───────────────────────────── Navigation ─────────────────────────────
def go(num):
    st.session_state.page = num
    st.query_params["chapitre"] = str(num)


if "page" not in st.session_state:
    try:
        st.session_state.page = int(st.query_params.get("chapitre", 0) or 0)
    except ValueError:
        st.session_state.page = 0
page = st.session_state.page if any(c["num"] == st.session_state.page for c in CHAPTERS) else 0


def md(text):
    """Convertit **gras** en <b>."""
    parts = text.split("**")
    return "".join(f"<b>{p}</b>" if i % 2 else p for i, p in enumerate(parts))


def topbar():
    left, mid, b1, b2, b3 = st.columns([5, 3, 1.3, 1, 1])
    left.markdown("<div class='brand'>Avant l'IA, <span>il y avait nous</span>"
                  f"<small> · {BOOK['author']}</small></div>", unsafe_allow_html=True)
    if page:
        part = next(p for p in PARTS if p["id"] == get_chapter(page)["part"])
        mid.markdown(f"<div class='brand' style='font-weight:500;color:#8A94A6;font-size:.9rem;padding-top:.6rem'>"
                     f"{part['label']} · {page:02d} / {len(CHAPTERS)}</div>", unsafe_allow_html=True)
        ui.button(b1, "Sommaire", on_click=go, args=(0,), key="top_home")
        ui.button(b2, "←", on_click=go, args=(max(1, page - 1),), key="top_prev", disabled=page == 1)
        ui.button(b3, "→", on_click=go, args=(min(len(CHAPTERS), page + 1),), key="top_next",
                  disabled=page == len(CHAPTERS))
    st.markdown("<div class='topline'></div>", unsafe_allow_html=True)


# ───────────────────────────── Accueil : un sommaire ─────────────────────────────
def home():
    st.markdown("<div class='kicker'>Le livre, en version interactive</div>"
                "<div class='hero'>Comprendre l'IA <em>en la touchant du doigt.</em></div>"
                f"<div class='lead'>{BOOK['subtitle']}. Chaque chapitre du livre devient une petite expérience "
                "que l'on manipule soi-même.</div>"
                "<div class='meta'><div><b>5</b>parties</div><div><b>15</b>chapitres</div>"
                "<div><b>15</b>expériences</div></div>", unsafe_allow_html=True)
    c, _ = st.columns([1, 3])
    ui.button(c, "Commencer  →", type="primary", on_click=go, args=(1,), key="start")

    romans = ["1", "2", "3", "4", "5"]
    for p, r in zip(PARTS, romans):
        st.markdown(f"<div class='part'><div class='roman'>{r}</div><div><div class='l'>{p['label']}</div>"
                    f"<div class='t'>{p['title']}</div></div></div>", unsafe_allow_html=True)
        for ch in chapters_of(p["id"]):
            a, b = st.columns([5, 4])
            with a:
                ui.button(st, f"{ch['num']:02d}   {ch['icon']}  {ch['title']}", key=f"idx{ch['num']}",
                          on_click=go, args=(ch["num"],))
            b.markdown(f"<div class='row-tag'>{ch['tagline']}</div>", unsafe_allow_html=True)


# ───────────────────────────── Page chapitre ─────────────────────────────
def chapter(c):
    head, num = st.columns([4, 1])
    with head:
        st.markdown(f"<div class='kicker'>{next(p['title'] for p in PARTS if p['id'] == c['part'])}</div>"
                    f"<div class='hero'>{c['title']}</div><div class='lead'>{c['tagline']}</div>",
                    unsafe_allow_html=True)
    num.markdown(f"<div class='bignum' style='text-align:right'>{c['num']:02d}</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["Le principe", "Comment ça marche", f"{c['icon']}  Expérience guidée", "Aujourd'hui"])
    with t1:
        a, b = st.columns(2)
        a.markdown(f"<div class='panel nature'><div class='k'>Ce que fait la nature</div>"
                   f"<div class='v'>{md(c['nature'])}</div></div>", unsafe_allow_html=True)
        b.markdown(f"<div class='panel idea'><div class='k'>L'idée des chercheurs</div>"
                   f"<div class='v'>{md(c['idea'])}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='example'><div class='k'>Un exemple concret</div>{md(c['example'])}</div>",
                    unsafe_allow_html=True)
        if c.get("neo"):
            st.markdown(f"<div class='neo'><div class='av'>N</div><div><div class='who'>Néo</div>{c['neo']}</div></div>",
                        unsafe_allow_html=True)
    with t2:
        steps = "".join(f"<div class='tl' data-n='{i}'><div class='t'>{md(s)}</div></div>"
                        for i, s in enumerate(c["how"], 1))
        st.markdown(f"<div class='timeline'>{steps}</div>", unsafe_allow_html=True)
    with t3:
        with st.container(border=True):
            REGISTRY[c["demo"]]()
    with t4:
        st.markdown(f"<div class='today'>{md(c['today'])}</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)
    left, _, right = st.columns([2, 1, 2])
    if c["num"] > 1:
        ui.button(left, f"←  {get_chapter(c['num'] - 1)['title']}", on_click=go, args=(c["num"] - 1,), key="prev")
    if c["num"] < len(CHAPTERS):
        ui.button(right, f"{get_chapter(c['num'] + 1)['title']}  →", on_click=go, args=(c["num"] + 1,),
                  type="primary", key="next")
    else:
        ui.button(right, "Retour au sommaire", on_click=go, args=(0,), type="primary", key="end")


def about():
    links = " ".join(f"<a href='{u}' target='_blank'>{t} ↗</a>" for t, u in BOOK["links"])
    paras = "".join(f"<p>{p}</p>" for p in BOOK["author_bio"])
    st.markdown(f"<div class='about'><div class='kicker'>À propos de l'auteur</div>"
                f"<div class='about-grid'><div><div class='about-name'>{BOOK['author']}</div>"
                f"<div class='about-title'>{BOOK['author_title']}</div>{paras}<div class='about-links'>{links}</div></div></div></div>",
                unsafe_allow_html=True)


def footer():
    st.markdown(f"<div class='footer'><b>{BOOK['title']}</b> — {BOOK['subtitle']}<br>"
                f"Un livre d'<b>{BOOK['author']}</b> · © 2026. Tous droits réservés.</div>",
                unsafe_allow_html=True)


topbar()
if page:
    chapter(get_chapter(page))
else:
    home()
footer()
