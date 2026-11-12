"""Démonstrations interactives, une par chapitre.

Principe commun : un exemple concret, déroulé ÉTAPE PAR ÉTAPE avec les vrais calculs,
pour que le lecteur voie exactement ce que fait l'algorithme.
"""

import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

import ui

AMBER = "#F2B544"
CYAN = "#5CC8D7"
GREEN = "#7BD389"
RED = "#FF6B6B"
GRAY = "#8A94A6"
LINE = "#2A3442"
INK = "#E8ECF2"
BG = "#0F141B"
PANEL = "#1B2330"
FONT = "'EB Garamond', Georgia, serif"


# ═════════════════════════════ Outils communs ═════════════════════════════
def style(chart, height=320):
    return (
        chart.properties(height=height, background="transparent")
        .configure_view(strokeWidth=0)
        .configure_axis(gridColor="#1E2632", domainColor=LINE, tickColor=LINE, labelColor=GRAY,
                        titleColor=GRAY, labelFont=FONT, titleFont=FONT, labelFontSize=11,
                        titleFontSize=12, titleFontWeight="normal")
        .configure_legend(labelFont=FONT, titleFont=FONT, labelColor="#C9D1DC", titleColor=GRAY,
                          orient="bottom", titleFontWeight="normal")
        .configure_text(font=FONT)
    )


def html(s):
    st.markdown(s, unsafe_allow_html=True)


def scenario(text):
    """Le problème concret posé au lecteur."""
    html(f"<div class='scenario'><span>Le problème</span>{text}</div>")


def explain(title, body):
    """Encadré « ce qui se passe » d'une étape."""
    html(f"<div class='explain'><div class='et'>{title}</div><div class='eb'>{body}</div></div>")


def calc(lines):
    """Lignes de calcul, alignées comme sur un cahier."""
    html("<div class='calc'>" + "".join(f"<div>{l}</div>" for l in lines) + "</div>")


def takeaway(text):
    html(f"<div class='take'><span>À retenir</span>{text}</div>")


def stepper(key, n, labels=None):
    """Navigation ⏮ ← → ⏭ entre les étapes. Renvoie l'étape courante (0…n-1)."""
    k = f"step_{key}"
    st.session_state.setdefault(k, 0)
    st.session_state[k] = max(0, min(st.session_state[k], n - 1))

    def move(to):
        st.session_state[k] = max(0, min(n - 1, to))

    i = st.session_state[k]
    c0, c1, c2, c3, c4 = st.columns([1, 1.6, 4, 1.6, 1])
    ui.button(c0, "⏮", key=f"{k}_first", on_click=move, args=(0,), disabled=i == 0, help="Revenir au début")
    ui.button(c1, "← Précédent", key=f"{k}_prev", on_click=move, args=(i - 1,), disabled=i == 0)
    label = labels[i] if labels else ""
    pct = (i + 1) / n * 100
    c2.markdown(f"<div class='stepinfo'><b>Étape {i + 1} / {n}</b> {('· ' + label) if label else ''}"
                f"<div class='bar'><div style='width:{pct:.0f}%'></div></div></div>", unsafe_allow_html=True)
    ui.button(c3, "Suivant →", key=f"{k}_next", on_click=move, args=(i + 1,), disabled=i == n - 1, type="primary")
    ui.button(c4, "⏭", key=f"{k}_last", on_click=move, args=(n - 1,), disabled=i == n - 1, help="Aller à la fin")
    return i


def _result(label, value, caption=""):
    html(f"<div class='result'><div class='result-label'>{label}</div>"
         f"<div class='result-value'>{value}</div><div class='result-caption'>{caption}</div></div>")


def _seed_button(key, label="↻  Relancer"):
    skey = f"seed_{key}"
    st.session_state.setdefault(skey, 7)
    if st.button(label, key=f"btn_{key}"):
        st.session_state[skey] = int(np.random.randint(0, 10_000))
        st.session_state[f"step_{key}"] = 0
    return st.session_state[skey]


def f2(x):
    return f"{x:+.2f}".replace("+", "+ ").replace("-", "− ")


# ═════════════════════════════ 1. Le neurone ═════════════════════════════
def neuron():
    scenario("Ce soir, vais-je aller courir ? Trois signaux entrent dans le neurone. "
             "Chacun a une <b>intensité</b> (à quel point il est vrai) et un <b>poids</b> (à quel point il compte pour moi).")
    signals = [("☀️", "Il fait beau", 0.8, 1.0), ("😴", "Je suis fatigué", 0.6, -1.5), ("🤝", "Un ami m'attend", 1.0, 2.0)]
    xs, ws = [], []
    for i, (ic, name, x0, w0) in enumerate(signals):
        c1, c2 = st.columns(2)
        xs.append(c1.slider(f"{ic} {name} — intensité", 0.0, 1.0, x0, 0.1, key=f"nx{i}"))
        ws.append(c2.slider(f"{ic} poids", -3.0, 3.0, w0, 0.5, key=f"nw{i}"))
    thr = st.slider("Seuil : au-dessus, le neurone dit « oui »", -2.0, 3.0, 1.0, 0.25, key="nthr")
    prods = [x * w for x, w in zip(xs, ws)]
    total = sum(prods)
    on = total >= thr

    # Schéma du neurone
    ys = [55, 135, 215]
    svg = [f"<svg viewBox='0 0 700 270' width='100%' style='max-width:700px'>"]
    for (ic, name, _, _), x, w, y, p in zip(signals, xs, ws, ys, prods):
        col = AMBER if w >= 0 else CYAN
        svg.append(f"<line x1='190' y1='{y}' x2='420' y2='135' stroke='{col}' stroke-width='{1 + abs(w) * 2.2:.1f}' opacity='.85'/>")
        svg.append(f"<rect x='10' y='{y - 26}' width='180' height='52' rx='12' fill='{PANEL}' stroke='{LINE}'/>")
        svg.append(f"<text x='24' y='{y - 4}' fill='{INK}' font-size='14'>{ic} {name}</text>")
        svg.append(f"<text x='24' y='{y + 16}' fill='{GRAY}' font-size='12'>intensité {x:.1f}</text>")
        mx, my = 262, y + (135 - y) * 0.31
        svg.append(f"<rect x='{mx - 52}' y='{my - 14}' width='104' height='24' rx='12' fill='{BG}' stroke='{col}'/>")
        svg.append(f"<text x='{mx}' y='{my + 3}' fill='{col}' font-size='12' text-anchor='middle'>× {w:+.1f} = {p:+.2f}</text>")
    ring = AMBER if on else GRAY
    svg.append(f"<circle cx='470' cy='135' r='52' fill='{PANEL}' stroke='{ring}' stroke-width='3'/>")
    svg.append(f"<text x='470' y='128' fill='{GRAY}' font-size='12' text-anchor='middle'>somme</text>")
    svg.append(f"<text x='470' y='152' fill='{INK}' font-size='22' font-weight='700' text-anchor='middle'>{total:+.2f}</text>")
    svg.append(f"<line x1='522' y1='135' x2='570' y2='135' stroke='{ring}' stroke-width='3'/>")
    svg.append(f"<text x='580' y='130' fill='{ring}' font-size='16' font-weight='700'>{'OUI 🏃' if on else 'NON 🛋️'}</text>")
    svg.append(f"<text x='580' y='152' fill='{GRAY}' font-size='12'>seuil {thr:+.2f}</text></svg>")
    html("".join(svg))

    explain("Le calcul du neurone, en trois gestes", "")
    calc([f"<i>1. Multiplier</i>  chaque intensité par son poids :"] +
         [f"&nbsp;&nbsp;&nbsp;{s[0]} {x:.1f} × {w:+.1f} = <b>{p:+.2f}</b>" for s, x, w, p in zip(signals, xs, ws, prods)] +
         [f"<i>2. Additionner</i> :  {' '.join(f'{p:+.2f}' for p in prods)} = <b>{total:+.2f}</b>",
          f"<i>3. Comparer au seuil</i> :  {total:+.2f} {'≥' if on else '<'} {thr:+.2f}  →  "
          f"<b>{'le neurone s’active : je vais courir' if on else 'le neurone reste éteint : je reste au calme'}</b>"])
    takeaway("Un neurone ne « réfléchit » pas : il multiplie, additionne et compare. "
             "Toute son « opinion » est dans ses poids. Apprendre, ce sera trouver ces poids automatiquement (chapitre 3).")


# ═════════════════════════════ 2. Les k plus proches voisins ═════════════════════════════
ANIMALS = pd.DataFrame([
    ("Minou", 4.0, 9.0, "chat"), ("Félix", 5.2, 8.0, "chat"), ("Nala", 3.5, 9.5, "chat"),
    ("Tigrou", 6.0, 8.5, "chat"), ("Mimi", 4.5, 7.5, "chat"), ("Pacha", 7.0, 8.0, "chat"),
    ("Rex", 30.0, 3.0, "chien"), ("Médor", 12.0, 4.0, "chien"), ("Pupuce", 6.0, 6.0, "chien"),
    ("Bella", 20.0, 2.0, "chien"), ("Filou", 9.0, 6.5, "chien"), ("Oscar", 15.0, 5.0, "chien"),
], columns=["nom", "poids", "oreilles", "espèce"])


def knn():
    scenario("La machine connaît 12 animaux dont on lui a dit l'espèce. Un animal inconnu arrive : "
             "est-ce un chat ou un chien ? Aucune règle n'est écrite — seulement des exemples.")
    c1, c2, c3 = st.columns(3)
    w = c1.slider("🐾 Poids de l'inconnu (kg)", 2.0, 30.0, 6.5, 0.5)
    e = c2.slider("👂 Oreilles pointues (0 à 10)", 0.0, 10.0, 7.0, 0.5)
    k = c3.slider("Nombre de voisins consultés (k)", 1, 7, 3, 2)

    df = ANIMALS.copy()
    df["d_poids"] = (df.poids - w) / 8
    df["d_oreilles"] = (df.oreilles - e) / 3
    df["distance"] = np.sqrt(df.d_poids ** 2 + df.d_oreilles ** 2)
    df = df.sort_values("distance").reset_index(drop=True)
    nn = df.head(k)

    step = stepper("knn", 4, ["Les exemples", "Mesurer les distances", "Garder les k plus proches", "Voter"])

    base = alt.Chart(df).encode(
        x=alt.X("poids:Q", title="Poids (kg, échelle logarithmique)", scale=alt.Scale(type="log", domain=[2.5, 35], nice=False)),
        y=alt.Y("oreilles:Q", title="Oreilles pointues", scale=alt.Scale(domain=[0, 10.5])))
    color = alt.Color("espèce:N", scale=alt.Scale(domain=["chat", "chien"], range=[AMBER, CYAN]), title=None)
    layers = []
    if step >= 1:
        lines = []
        show = df if step == 1 else nn
        for _, r in show.iterrows():
            lines += [{"poids": w, "oreilles": e, "id": r.nom}, {"poids": r.poids, "oreilles": r.oreilles, "id": r.nom}]
        layers.append(alt.Chart(pd.DataFrame(lines)).mark_line(color=GRAY, strokeDash=[3, 3], opacity=.7)
                      .encode(x="poids:Q", y="oreilles:Q", detail="id:N"))
    df["actif"] = True if step < 2 else df.nom.isin(nn.nom)
    layers.append(base.mark_circle(size=170).encode(color=color, opacity=alt.condition("datum.actif", alt.value(1), alt.value(.2)),
                                                    tooltip=["nom", "espèce", "poids", "oreilles"]))
    layers.append(base.mark_text(dy=-15, fontSize=11, color="#C9D1DC").encode(text="nom:N"))
    layers.append(alt.Chart(pd.DataFrame({"poids": [w], "oreilles": [e], "t": ["?"]})).mark_point(
        shape="diamond", size=320, filled=True, color=INK).encode(x="poids:Q", y="oreilles:Q"))
    ui.chart(style(alt.layer(*layers), 330))

    if step == 0:
        explain("Étape 1 — Les exemples connus",
                "Chaque animal est décrit par deux nombres : son poids et la forme de ses oreilles. "
                "Les chats (ambre) sont légers aux oreilles pointues, les chiens (cyan) plus variés. "
                "Le losange blanc est l'inconnu : réglez-le avec les curseurs.")
    elif step == 1:
        r = df.iloc[0]
        explain("Étape 2 — Mesurer la distance à chaque exemple",
                "On mesure à quel point l'inconnu ressemble à chaque animal connu. On divise l'écart de poids par 8 et "
                "l'écart d'oreilles par 3, pour que les deux critères comptent autant.")
        calc([f"Exemple avec {r.nom} :",
              f"&nbsp;&nbsp;écart de poids = ({r.poids:.1f} − {w:.1f}) ÷ 8 = {r.d_poids:+.2f}",
              f"&nbsp;&nbsp;écart d'oreilles = ({r.oreilles:.1f} − {e:.1f}) ÷ 3 = {r.d_oreilles:+.2f}",
              f"&nbsp;&nbsp;distance = √({r.d_poids:.2f}² + {r.d_oreilles:.2f}²) = <b>{r.distance:.2f}</b>"])
        st.dataframe(df[["nom", "espèce", "poids", "oreilles", "distance"]].round(2), hide_index=True, **ui.stretch(st.dataframe))
    elif step == 2:
        explain(f"Étape 3 — Garder les {k} plus proches",
                f"On trie tous les animaux du plus ressemblant au moins ressemblant, et on ne garde que les {k} premiers : "
                + ", ".join(f"<b>{r.nom}</b> ({r.espèce}, distance {r.distance:.2f})" for _, r in nn.iterrows()) + ".")
    else:
        votes = nn["espèce"].value_counts()
        verdict = votes.idxmax()
        explain("Étape 4 — Le vote",
                "Chaque voisin vote pour son espèce : " + " · ".join(f"<b>{v}</b> voix pour « {s} »" for s, v in votes.items())
                + ". La majorité l'emporte.")
        _result("Verdict de la machine", "🐱 C'est un chat" if verdict == "chat" else "🐶 C'est un chien",
                "Essayez un animal de 6 kg aux oreilles mi-pointues : la réponse dépend de k !")
    takeaway("La machine n'a jamais appris ce qu'est un chat. Elle compare au déjà-vu, comme un enfant. "
             "C'est l'idée de base de l'apprentissage automatique : <b>des exemples plutôt que des règles</b>.")


# ═════════════════════════════ 3. Le perceptron ═════════════════════════════
FRUITS = pd.DataFrame([
    ("🍎", 8, 2), ("🍎", 7, 3), ("🍎", 9, 4), ("🍎", 6, 2), ("🍎", 8, 5),
    ("🍋", 2, 8), ("🍋", 3, 9), ("🍋", 1, 6), ("🍋", 4, 7), ("🍋", 3, 5),
], columns=["fruit", "sucre", "acidité"])
FRUITS["y"] = np.where(FRUITS.fruit == "🍎", 1, -1)


@st.cache_data
def _perceptron_events(lr=0.1):
    w1, w2, b = -0.3, 0.4, 0.0  # départ volontairement mauvais
    events = []
    for epoch in range(1, 9):
        errors = 0
        for i, r in FRUITS.iterrows():
            s = w1 * r.sucre + w2 * r["acidité"] + b
            pred = 1 if s > 0 else -1
            ok = pred == r.y
            old = (w1, w2, b)
            if not ok:
                errors += 1
                w1 += lr * r.y * r.sucre
                w2 += lr * r.y * r["acidité"]
                b += lr * r.y
            events.append(dict(epoch=epoch, i=i, score=s, pred=pred, ok=ok, old=old, new=(w1, w2, b)))
        if errors == 0:
            break
    return events


def perceptron():
    scenario("Apprendre à un neurone à distinguer 🍎 pommes et 🍋 citrons à partir de deux mesures : "
             "le <b>sucre</b> et l'<b>acidité</b>. Au départ, ses poids sont mauvais. Il va les corriger seul, erreur après erreur.")
    ev = _perceptron_events()
    step = stepper("perc", len(ev) + 1)
    if step == 0:
        w1, w2, b = ev[0]["old"]
        cur = None
    else:
        e = ev[step - 1]
        w1, w2, b = e["new"]
        cur = e

    df = FRUITS.copy()
    df["vu"] = df.index == (cur["i"] if cur else -1)
    xs = np.linspace(0, 10, 200)
    pts = alt.Chart(df).mark_text(fontSize=26).encode(
        x=alt.X("sucre:Q", scale=alt.Scale(domain=[0, 10]), title="Sucre"),
        y=alt.Y("acidité:Q", scale=alt.Scale(domain=[0, 10]), title="Acidité"), text="fruit:N")
    gs = np.arange(0, 10, 0.5)
    zone = pd.DataFrame([{"x": a, "x2": a + 0.5, "y": c, "y2": c + 0.5,
                          "rep": "zone « pomme »" if w1 * (a + .25) + w2 * (c + .25) + b > 0 else "zone « citron »"}
                         for a in gs for c in gs])
    zones = alt.Chart(zone).mark_rect(opacity=.16).encode(
        x="x:Q", x2="x2:Q", y="y:Q", y2="y2:Q",
        color=alt.Color("rep:N", scale=alt.Scale(domain=["zone « pomme »", "zone « citron »"], range=[RED, AMBER]), title=None))
    ring = alt.Chart(df[df.vu]).mark_circle(size=1400, color=AMBER, opacity=.25).encode(x="sucre:Q", y="acidité:Q")
    layers = [zones, ring, pts]
    if abs(w2) > 1e-9:
        line = pd.DataFrame({"sucre": xs, "acidité": -(w1 * xs + b) / w2}).query("0 <= acidité <= 10")
        layers.insert(1, alt.Chart(line).mark_line(color=INK, strokeWidth=3).encode(x="sucre:Q", y="acidité:Q"))
    ui.chart(style(alt.layer(*layers), 340))

    if cur is None:
        explain("Le point de départ",
                f"Le neurone calcule : <b>score = {w1:+.1f} × sucre {w2:+.1f} × acidité {b:+.1f}</b>. "
                "Si le score est positif, il répond « pomme », sinon « citron ». Les zones colorées montrent ce qu'il répondrait "
                "partout (rouge = pomme, jaune = citron) : pour l'instant, il se trompe sur beaucoup de fruits. Cliquez sur « Suivant » pour lui montrer un fruit.")
    else:
        r = FRUITS.loc[cur["i"]]
        o1, o2, ob = cur["old"]
        truth = "pomme" if r.y == 1 else "citron"
        said = "pomme" if cur["pred"] == 1 else "citron"
        lines = [f"Fruit montré : {r.fruit} (sucre {r.sucre}, acidité {r['acidité']}) — passage n°{cur['epoch']}",
                 f"score = {o1:+.2f} × {r.sucre} {o2:+.2f} × {r['acidité']} {ob:+.2f} = <b>{cur['score']:+.2f}</b>  "
                 f"→ il répond « {said} »"]
        if cur["ok"]:
            lines.append(f"✅ C'est bien un(e) {truth}. <b>On ne touche à rien.</b>")
        else:
            sign = "+" if r.y == 1 else "−"
            lines += [f"❌ Faux, c'était un(e) {truth} ! On pousse les poids vers la bonne réponse ({sign} 0,1 × mesure) :",
                      f"&nbsp;&nbsp;poids du sucre : {o1:+.2f} {sign} 0,1 × {r.sucre} = <b>{w1:+.2f}</b>",
                      f"&nbsp;&nbsp;poids de l'acidité : {o2:+.2f} {sign} 0,1 × {r['acidité']} = <b>{w2:+.2f}</b>",
                      f"&nbsp;&nbsp;biais : {ob:+.2f} {sign} 0,1 = <b>{b:+.2f}</b>  → la ligne bouge"]
        calc(lines)
        if step == len(ev):
            _result("Apprentissage terminé", "Plus aucune erreur",
                    f"Le neurone a trouvé seul ses poids : {w1:+.2f} × sucre {w2:+.2f} × acidité {b:+.2f}.")
    takeaway("Apprendre, pour un neurone, c'est <b>corriger un peu ses poids à chaque erreur</b>. "
             "Personne ne lui a donné la frontière : il l'a trouvée en se trompant.")


# ═════════════════════════════ 4. Les fourmis ═════════════════════════════
@st.cache_data
def _bridge_rounds(ratio, seed, rounds=25, ants=10, evap=0.1, init=5.0):
    rng = np.random.default_rng(seed)
    tau = np.array([init, init])
    L = np.array([1.0, ratio])
    out = []
    for t in range(rounds):
        p = tau ** 2 / (tau ** 2).sum()
        n_short = int(rng.binomial(ants, p[0]))
        before = tau.copy()
        tau = tau * (1 - evap) + np.array([n_short, ants - n_short]) / L
        out.append(dict(t=t + 1, before=before, p=p[0], n_short=n_short, after=tau.copy()))
    return out


def _bridge_svg(tau, n_short, n_long, ratio):
    ws, wl = [1.5 + 14 * v / max(tau.max(), 1e-9) for v in tau]
    return f"""<svg viewBox='0 0 700 250' width='100%' style='max-width:700px'>
      <path d='M 90 125 Q 350 40 610 125' fill='none' stroke='{AMBER}' stroke-width='{ws:.1f}' stroke-linecap='round' opacity='.9'/>
      <path d='M 90 125 Q 350 {125 + 60 * ratio + 40:.0f} 610 125' fill='none' stroke='{CYAN}' stroke-width='{wl:.1f}' stroke-linecap='round' opacity='.9'/>
      <circle cx='70' cy='125' r='34' fill='{PANEL}' stroke='{LINE}'/><text x='70' y='132' text-anchor='middle' font-size='24'>🏠</text>
      <text x='70' y='180' text-anchor='middle' fill='{GRAY}' font-size='12'>fourmilière</text>
      <circle cx='630' cy='125' r='34' fill='{PANEL}' stroke='{LINE}'/><text x='630' y='133' text-anchor='middle' font-size='24'>🍯</text>
      <text x='630' y='180' text-anchor='middle' fill='{GRAY}' font-size='12'>nourriture</text>
      <text x='350' y='60' text-anchor='middle' fill='{AMBER}' font-size='14' font-weight='700'>Pont court · odeur {tau[0]:.1f} · 🐜×{n_short}</text>
      <text x='350' y='{min(240, 125 + 30 * ratio + 50):.0f}' text-anchor='middle' fill='{CYAN}' font-size='14' font-weight='700'>Pont long (×{ratio:.1f}) · odeur {tau[1]:.1f} · 🐜×{n_long}</text>
    </svg>"""


def ants():
    scenario("Deux ponts relient la fourmilière à la nourriture. Le pont long est plus long que le court. "
             "À chaque tour, 10 fourmis partent. Aucune ne sait quel pont est le meilleur. Comment la colonie va-t-elle trouver ?")
    ratio = st.slider("Le pont long est … fois plus long que le court", 1.2, 3.0, 2.0, 0.1)
    seed = _seed_button("ants")
    rounds = _bridge_rounds(ratio, seed)
    step = stepper("ants", len(rounds) + 1)
    if step == 0:
        tau = rounds[0]["before"]
        html(_bridge_svg(tau, 0, 0, ratio))
        explain("Au départ", "Les deux ponts ont exactement la même odeur (5,0). Une fourmi qui arrive n'a donc "
                "aucune préférence : une chance sur deux pour chaque pont. Cliquez sur « Suivant » pour lancer le premier tour.")
    else:
        r = rounds[step - 1]
        b, a = r["before"], r["after"]
        html(_bridge_svg(a, r["n_short"], 10 - r["n_short"], ratio))
        explain(f"Tour {r['t']} — ce qui se passe",
                "Chaque fourmi choisit un pont au hasard, mais elle préfère celui qui sent le plus fort. "
                "Ensuite, une partie de l'odeur s'évapore, et les fourmis en déposent de la nouvelle.")
        calc([f"<i>1. Choisir</i> : chance de prendre le court = {b[0]:.1f}² ÷ ({b[0]:.1f}² + {b[1]:.1f}²) = <b>{r['p']:.0%}</b>",
              f"&nbsp;&nbsp;→ tirage : <b>{r['n_short']}</b> fourmis sur le court, <b>{10 - r['n_short']}</b> sur le long",
              f"<i>2. Évaporer</i> : chaque odeur perd 10 %  ({b[0]:.1f} → {b[0] * .9:.1f} ; {b[1]:.1f} → {b[1] * .9:.1f})",
              f"<i>3. Déposer</i> : chaque fourmi ajoute 1 ÷ longueur du pont",
              f"&nbsp;&nbsp;court : + {r['n_short']} × 1 ÷ 1 = +{r['n_short']:.1f}  →  odeur <b>{a[0]:.1f}</b>",
              f"&nbsp;&nbsp;long : + {10 - r['n_short']} × 1 ÷ {ratio:.1f} = +{(10 - r['n_short']) / ratio:.1f}  →  odeur <b>{a[1]:.1f}</b>"])
        if step == len(rounds):
            _result("Après 25 tours", f"{r['p']:.0%} de chances de prendre le pont court",
                    "Personne n'a décidé : le pont court a gagné parce que ses fourmis reviennent plus vite et l'odeur s'y accumule.")
    takeaway("Trois règles locales suffisent : <b>suivre l'odeur, la renforcer, la laisser s'évaporer</b>. "
             "Les algorithmes de colonies de fourmis copient exactement ce mécanisme pour trouver des tournées de livraison courtes.")
    with st.expander("Et sur un vrai problème ? La tournée de Léa, la livreuse"):
        _tsp_block()


@st.cache_data
def _aco_tsp(n, seed, iters=40, n_ants=15, evap=0.3):
    rng0 = np.random.default_rng(seed)
    pts = rng0.uniform(0, 100, (n, 2))
    D = np.linalg.norm(pts[:, None] - pts[None], axis=-1) + np.eye(n)
    tau = np.ones((n, n))
    rng = np.random.default_rng(seed + 1)
    best, best_len, history = None, np.inf, []
    for _ in range(iters):
        tours = []
        for _ in range(n_ants):
            tour = [int(rng.integers(n))]
            left = set(range(n)) - {tour[0]}
            while left:
                cand = np.array(sorted(left))
                w = tau[tour[-1], cand] * (1 / D[tour[-1], cand]) ** 3
                nxt = int(rng.choice(cand, p=w / w.sum()))
                tour.append(nxt)
                left.remove(nxt)
            length = sum(D[tour[i], tour[(i + 1) % n]] for i in range(n))
            tours.append((tour, length))
            if length < best_len:
                best, best_len = tour, length
        tau *= (1 - evap)
        for tour, length in tours:
            for i in range(n):
                a, b = tour[i], tour[(i + 1) % n]
                tau[a, b] += 100 / length
                tau[b, a] += 100 / length
        history.append((list(best), best_len))
    return pts, history


def _tsp_block():
    st.caption("15 fourmis virtuelles par génération construisent chacune une tournée qui passe par toutes les villes. "
               "Les tournées courtes déposent plus d'odeur sur leurs routes. Faites avancer les générations.")
    it = st.slider("Génération", 1, 40, 1, key="tsp_it")
    pts, history = _aco_tsp(15, 3)
    tour, length = history[it - 1]
    order = tour + [tour[0]]
    route = pd.DataFrame({"x": pts[order, 0], "y": pts[order, 1], "o": range(len(order))})
    chart = (alt.Chart(route).mark_line(color=AMBER, strokeWidth=2.5).encode(x=alt.X("x:Q", axis=None), y=alt.Y("y:Q", axis=None), order="o:Q")
             + alt.Chart(pd.DataFrame({"x": pts[:, 0], "y": pts[:, 1]})).mark_circle(size=110, color=INK).encode(x="x:Q", y="y:Q"))
    ui.chart(style(chart, 300))
    _result("Meilleure tournée trouvée", f"{length:.0f} km", f"Génération 1 : {history[0][1]:.0f} km.")


# ═════════════════════════════ 5. L'algorithme génétique ═════════════════════════════
LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
TARGET = "FOURMI"


@st.cache_data
def _evolve(seed, pop=10, mut=0.08, max_gen=120):
    rng = np.random.default_rng(seed)
    P = ["".join(rng.choice(LETTERS, len(TARGET))) for _ in range(pop)]
    score = lambda s: sum(a == b for a, b in zip(s, TARGET))
    gens = []
    for g in range(max_gen):
        P.sort(key=score, reverse=True)
        rec = dict(g=g, pop=list(P), scores=[score(s) for s in P])
        if score(P[0]) == len(TARGET):
            gens.append(rec)
            break
        parents = P[:4]
        children = [P[0]]  # le meilleur est conservé tel quel
        detail = None
        while len(children) < pop:
            a, b = rng.choice(4, 2, replace=False)
            cut = int(rng.integers(1, len(TARGET)))
            child = parents[a][:cut] + parents[b][cut:]
            mutated = list(child)
            spots = []
            for i in range(len(TARGET)):
                if rng.random() < mut:
                    mutated[i] = str(rng.choice(LETTERS))
                    spots.append(i)
            if detail is None:
                detail = dict(pa=parents[a], pb=parents[b], cut=cut, child=child, final="".join(mutated), spots=spots)
            children.append("".join(mutated))
        rec["parents"], rec["detail"] = parents, detail
        gens.append(rec)
        P = children
    return gens


def _word(s, spots=(), cut=None):
    out = []
    for i, ch in enumerate(s):
        cls = "ok" if ch == TARGET[i] else ""
        if i in spots:
            cls += " mut"
        if cut is not None and i == cut:
            out.append("<span class='cut'></span>")
        out.append(f"<span class='lt {cls}'>{ch}</span>")
    return "<span class='word'>" + "".join(out) + "</span>"


def genetic():
    scenario(f"Retrouver le mot caché <b>{TARGET}</b> sans jamais l'écrire. La machine sait seulement "
             "<b>noter</b> un essai : combien de lettres sont à la bonne place. 10 mots tirés au hasard vont évoluer.")
    seed = _seed_button("ga", "↻  Nouvelle population")
    gens = _evolve(seed)
    step = stepper("ga", len(gens), [f"Génération {g['g']}" for g in gens])
    g = gens[step]

    a, b = st.columns([1, 1])
    with a:
        html("<div class='mini-t'>La population et sa note</div>")
        rows = "".join(f"<div class='poprow {'top' if i < 4 else ''}'>{_word(s)}<span class='sc'>{sc}/6</span></div>"
                       for i, (s, sc) in enumerate(zip(g["pop"], g["scores"])))
        html(f"<div class='pop'>{rows}</div>")
        html("<div class='legend'><span class='lt ok'>A</span> lettre à la bonne place · "
             "lignes surlignées = les 4 meilleurs, sélectionnés comme parents</div>")
    with b:
        if g.get("detail"):
            d = g["detail"]
            html("<div class='mini-t'>Comment naît un enfant</div>")
            html(f"<div class='birth'><div><small>Parent A</small>{_word(d['pa'], cut=d['cut'])}</div>"
                 f"<div><small>Parent B</small>{_word(d['pb'], cut=d['cut'])}</div>"
                 f"<div><small>Croisement : début de A + fin de B</small>{_word(d['child'])}</div>"
                 f"<div><small>Mutation : quelques lettres changent au hasard</small>{_word(d['final'], spots=d['spots'])}</div></div>")
        else:
            _result("Mot trouvé !", f"{g['pop'][0]} en {g['g']} générations",
                    "Personne n'a écrit le mot : il est apparu par sélection, croisement et mutation.")
    explain("Ce qui se passe à chaque génération",
            "<b>1. Noter</b> chaque mot (lettres justes). <b>2. Sélectionner</b> les 4 meilleurs. "
            "<b>3. Croiser</b> : couper deux parents au même endroit et recoller les morceaux. "
            "<b>4. Muter</b> : changer parfois une lettre au hasard (encadrée en pointillés) — c'est ce qui apporte des lettres nouvelles. "
            "On garde aussi le meilleur mot intact pour ne jamais reculer.")
    best = [x["scores"][0] for x in gens]
    line = alt.Chart(pd.DataFrame({"génération": range(len(best)), "lettres justes": best})).mark_line(
        color=AMBER, strokeWidth=2.5, interpolate="step-after").encode(
        x="génération:Q", y=alt.Y("lettres justes:Q", scale=alt.Scale(domain=[0, 6])))
    rule = alt.Chart(pd.DataFrame({"g": [step]})).mark_rule(color=GRAY, strokeDash=[4, 4]).encode(x="g:Q")
    ui.chart(style(line + rule, 160))
    takeaway("Aucune intelligence dans chaque étape — seulement <b>noter, garder les meilleurs, mélanger, varier</b>. "
             "Répété assez longtemps, cela trouve des solutions que personne n'a dessinées.")


# ═════════════════════════════ 6. L'essaim ═════════════════════════════
def _gas(x, y):
    return (1.0 * np.exp(-((x - 7) ** 2 + (y - 3) ** 2) / 4)
            + 0.55 * np.exp(-((x - 2.5) ** 2 + (y - 7.5) ** 2) / 3)
            + 0.45 * np.exp(-((x - 3) ** 2 + (y - 2) ** 2) / 2))


@st.cache_data
def _pso(seed, n=10, iters=15):
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 10, (n, 2))
    V = rng.normal(0, 0.4, (n, 2))
    pb, pv = X.copy(), _gas(*X.T)
    hist = []
    for t in range(iters + 1):
        g = pb[pv.argmax()].copy()
        hist.append(dict(X=X.copy(), V=V.copy(), pb=pb.copy(), pv=pv.copy(), g=g, gv=pv.max()))
        r1, r2 = rng.random((2, n, 1))
        V = 0.6 * V + 1.2 * r1 * (pb - X) + 1.2 * r2 * (g - X)
        X = np.clip(X + V, 0, 10)
        val = _gas(*X.T)
        better = val > pv
        pb[better], pv[better] = X[better], val[better]
    return hist


@st.cache_data
def _gas_grid():
    xs = np.linspace(0.125, 9.875, 40)
    gx, gy = np.meshgrid(xs, xs)
    return pd.DataFrame({"x": gx.ravel(), "y": gy.ravel(), "c": _gas(gx, gy).ravel()})


def swarm():
    scenario("Une fuite de gaz dans une zone de 10 × 10 km. Dix drones mesurent la concentration là où ils sont, "
             "et <b>partagent</b> leur meilleure mesure par radio. Aucun ne voit la carte (en couleur, ici, pour vous).")
    seed = _seed_button("pso")
    hist = _pso(seed)
    step = stepper("pso", len(hist), [f"minute {i}" for i in range(len(hist))])
    h = hist[step]
    X = h["X"]
    heat = alt.Chart(_gas_grid()).mark_rect().encode(
        x=alt.X("x:Q", bin=alt.Bin(maxbins=40), axis=None), y=alt.Y("y:Q", bin=alt.Bin(maxbins=40), axis=None),
        color=alt.Color("c:Q", scale=alt.Scale(range=[BG, "#174A52", CYAN]), legend=None))
    d = pd.DataFrame({"x": X[:, 0], "y": X[:, 1], "id": [f"D{i + 1}" for i in range(len(X))]})
    drones = alt.Chart(d).mark_circle(size=120, color=GRAY, stroke=BG, strokeWidth=1.5, opacity=1).encode(x="x:Q", y="y:Q")
    links = pd.DataFrame([{"x": X[0, 0], "y": X[0, 1], "k": "a"}, {"x": h["pb"][0, 0], "y": h["pb"][0, 1], "k": "a"},
                          {"x": X[0, 0], "y": X[0, 1], "k": "b"}, {"x": h["g"][0], "y": h["g"][1], "k": "b"}])
    lk = alt.Chart(links).mark_line(strokeDash=[4, 3], strokeWidth=2).encode(
        x="x:Q", y="y:Q", detail="k:N", color=alt.Color("k:N", scale=alt.Scale(domain=["a", "b"], range=[INK, AMBER]), legend=None))
    d1 = alt.Chart(d.head(1)).mark_circle(size=260, color=INK, stroke=BG, strokeWidth=2, opacity=1).encode(x="x:Q", y="y:Q")
    star = alt.Chart(pd.DataFrame({"x": [h["g"][0]], "y": [h["g"][1]]})).mark_point(
        shape="diamond", size=300, filled=True, color=AMBER).encode(x="x:Q", y="y:Q")
    ui.chart(style(heat + lk + drones + d1 + star, 380))
    html(f"<div class='legend'>⚪ gros point blanc : le drone n°1 (suivi en détail) · ◆ ambre : meilleure mesure de tout l'essaim "
         f"· traits : vers où D1 est attiré</div>")

    x0, y0 = X[0]
    explain(f"Minute {step} — le drone n°1 décide où aller",
            "Chaque drone combine trois envies : <b>garder son élan</b>, <b>retourner vers sa meilleure mesure personnelle</b>, "
            "et <b>aller vers la meilleure mesure de l'essaim</b>. Un peu de hasard dose chaque envie.")
    calc([f"Position de D1 : ({x0:.1f} ; {y0:.1f}) km — gaz mesuré : {_gas(x0, y0):.2f}",
          f"Sa meilleure mesure : {h['pv'][0]:.2f} en ({h['pb'][0, 0]:.1f} ; {h['pb'][0, 1]:.1f})  (trait blanc)",
          f"Meilleure mesure de l'essaim : <b>{h['gv']:.2f}</b> en ({h['g'][0]:.1f} ; {h['g'][1]:.1f})  (trait ambre)",
          "Nouveau déplacement = 0,6 × élan + hasard × (vers sa meilleure) + hasard × (vers celle de l'essaim)"])
    near = (np.hypot(X[:, 0] - 7, X[:, 1] - 3) < 1.5).sum()
    _result("Drones autour de la vraie fuite", f"{near} / {len(X)}",
            "Deux leurres plus faibles peuvent piéger un drone isolé, pas un essaim qui partage ses mesures.")
    takeaway("Pas de chef, pas de carte : <b>chacun suit sa mémoire et celle du groupe</b>. "
             "C'est l'« optimisation par essaim », utilisée pour piloter des flottes de drones ou régler des machines.")


# ═════════════════════════════ 7. La vision ═════════════════════════════
IMG = np.zeros((10, 10), int)
IMG[2:8, 3:8] = 9  # un carré blanc sur fond noir
KERNELS = {
    "Bords verticaux": np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]),
    "Bords horizontaux": np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]),
}


def _grid_chart(M, title, hl=None, diverging=False, show=None, size=26):
    n, m = M.shape
    rows = []
    for i in range(n):
        for j in range(m):
            visible = show is None or show[i, j]
            rows.append({"r": i, "c": j, "v": float(M[i, j]) if visible else None,
                         "t": str(int(M[i, j])) if visible else ""})
    df = pd.DataFrame(rows)
    scale = (alt.Scale(domain=[-27, 0, 27], range=[CYAN, PANEL, AMBER]) if diverging
             else alt.Scale(domain=[0, 9], range=["#000000", "#FFFFFF"]))
    if diverging:
        scale = alt.Scale(domain=[-27, 0, 27], range=[CYAN, PANEL, AMBER], interpolate="rgb")
    base = alt.Chart(df).encode(x=alt.X("c:O", axis=None), y=alt.Y("r:O", axis=None))
    cells = base.mark_rect(stroke=BG, strokeWidth=1).encode(
        color=alt.condition("datum.v !== null", alt.Color("v:Q", scale=scale, legend=None), alt.value("#141A22")))
    txt = base.mark_text(fontSize=12).encode(text="t:N", color=alt.condition("datum.v > 4", alt.value("#000"), alt.value(GRAY)))
    layers = [cells, txt]
    if hl is not None:
        i0, j0 = hl
        box = pd.DataFrame([{"r": i, "c": j} for i in range(i0, i0 + 3) for j in range(j0, j0 + 3)])
        layers.append(alt.Chart(box).mark_rect(fill=None, stroke=AMBER, strokeWidth=2.5).encode(x="c:O", y="r:O"))
    return alt.layer(*layers).properties(width=m * size, height=n * size, title=alt.TitleParams(title, color=GRAY, fontSize=12, font=FONT))


def vision():
    scenario("Pour une machine, une image n'est qu'un tableau de nombres : ici un carré blanc (9) sur fond noir (0). "
             "Une petite <b>loupe de 3 × 3 nombres</b> — le filtre — va glisser sur toute l'image pour y chercher un motif.")
    name = st.radio("Filtre", list(KERNELS), horizontal=True)
    K = KERNELS[name]
    out = np.zeros((8, 8), int)
    for i in range(8):
        for j in range(8):
            out[i, j] = int((IMG[i:i + 3, j:j + 3] * K).sum())
    step = stepper("vision", 64, None)
    i, j = divmod(step, 8)
    shown = np.zeros((8, 8), bool)
    shown.flat[: step + 1] = True

    a, b = st.columns(2)
    with a:
        ui.chart(style(_grid_chart(IMG, "Image d'entrée (10 × 10)", hl=(i, j), size=34), 340), full=False)
    with b:
        ui.chart(style(_grid_chart(out, "Image de sortie (8 × 8)", diverging=True, show=shown, size=42), 336), full=False)

    win = IMG[i:i + 3, j:j + 3]
    terms = [f"{win[r, c]}×({K[r, c]:+d})" for r in range(3) for c in range(3)]
    kern = "<table class='kern'>" + "".join("<tr>" + "".join(f"<td>{v:+d}</td>" for v in row) + "</tr>" for row in K) + "</table>"
    explain(f"Position {step + 1} / 64 — la loupe est en ligne {i + 1}, colonne {j + 1}",
            f"<div style='display:flex;gap:1.4rem;align-items:center;flex-wrap:wrap'>{kern}<div>On multiplie chacun des 9 nombres "
            "sous la loupe par le nombre du filtre au même endroit, puis on additionne tout. Le résultat devient "
            "<b>un seul pixel</b> de l'image de sortie.</div></div>")
    calc([" + ".join(terms[:3]), " + ".join(terms[3:6]), " + ".join(terms[6:]) + f" = <b>{out[i, j]:+d}</b>",
          ("→ fort en positif ou en négatif : la loupe est sur un bord ! (" + ("de gauche à droite : noir → blanc" if name.startswith("Bords v") else "de haut en bas : noir → blanc")
           + " en ambre, blanc → noir en cyan)") if out[i, j] else "→ 0 : la zone est uniforme, aucun bord ici."])
    if step == 63:
        _result("Résultat", "Le filtre n'a gardé que les bords " + ("verticaux" if "vert" in name else "horizontaux") + " du carré",
                "Changez de filtre pour voir les autres bords.")
    takeaway("Un réseau de vision empile des centaines de ces filtres. Les premiers trouvent des bords, "
             "les suivants combinent les bords en coins, en formes, puis en yeux et en visages. "
             "Et surtout : <b>les nombres des filtres sont appris</b>, pas écrits à la main.")


# ═════════════════════════════ 8. La parole ═════════════════════════════
FORMANTS = {"a": (800, 1200), "é": (400, 2000), "i": (300, 2300), "o": (450, 800), "ou": (320, 750)}
SR, F0 = 8000, 140


def _vowel(v, dur=0.35):
    t = np.arange(int(SR * dur)) / SR
    f1, f2 = FORMANTS[v]
    sig = np.zeros_like(t)
    for h in range(1, int(3800 / F0)):
        f = h * F0
        sig += (np.exp(-((f - f1) / 120) ** 2) + 0.7 * np.exp(-((f - f2) / 160) ** 2) + 0.02) * np.sin(2 * np.pi * f * t)
    return sig * np.minimum(1, np.minimum(t, dur - t) / 0.03)


def _spectrum(sig):
    spec = np.abs(np.fft.rfft(sig * np.hanning(len(sig))))
    freqs = np.fft.rfftfreq(len(sig), 1 / SR)
    harm = np.arange(1, int(3800 / F0)) * F0
    amp = np.array([spec[np.argmin(abs(freqs - f))] for f in harm])
    amp = amp / amp.max()
    peaks = [k for k in range(1, len(amp) - 1) if amp[k] > amp[k - 1] and amp[k] >= amp[k + 1] and amp[k] > 0.15]
    peaks = sorted(sorted(peaks, key=lambda k: -amp[k])[:2])
    return harm, amp, [int(harm[k]) for k in peaks]


def speech():
    scenario("Quelqu'un prononce une voyelle. La machine ne « entend » rien : elle reçoit une onde, une suite de nombres. "
             "Comment peut-elle savoir si c'était un <b>a</b>, un <b>i</b> ou un <b>ou</b> ?")
    c1, c2 = st.columns([2, 1])
    st.session_state.setdefault("mystery", "ou")
    if ui.button(c2, "🎲  Nouvelle voyelle mystère", key="new_vowel"):
        st.session_state.mystery = str(np.random.choice([v for v in FORMANTS if v != st.session_state.mystery]))
        st.session_state["step_speech"] = 0
    v = st.session_state.mystery
    sig = _vowel(v)
    with c1:
        st.audio(sig / np.abs(sig).max() * 0.8, sample_rate=SR)
    step = stepper("speech", 4, ["Le son brut", "Les fréquences", "La comparaison", "Le verdict"])

    if step == 0:
        seg = sig[1200:1200 + 240]
        df = pd.DataFrame({"ms": np.arange(len(seg)) / SR * 1000, "pression": seg})
        ui.chart(style(alt.Chart(df).mark_line(color=CYAN, strokeWidth=2).encode(
            x=alt.X("ms:Q", title="Temps (millisecondes)"), y=alt.Y("pression:Q", title="Pression de l'air", axis=alt.Axis(labels=False))), 230))
        explain("Étape 1 — Ce que reçoit le micro",
                "30 millisecondes du son : une onde qui se répète. À l'œil, impossible de dire quelle voyelle c'est. "
                "Mais cette onde est en réalité la <b>somme de plusieurs vibrations</b> de fréquences différentes.")
    harm, amp, peaks = _spectrum(sig)
    if step == 1:
        df = pd.DataFrame({"Hz": harm, "énergie": amp, "pic": [int(h) in peaks for h in harm]})
        bars = alt.Chart(df).mark_bar(width=8, cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
            x=alt.X("Hz:Q", title="Fréquence (Hz)", scale=alt.Scale(domain=[0, 3800])),
            y=alt.Y("énergie:Q", title="Énergie"),
            color=alt.condition("datum.pic", alt.value(AMBER), alt.value(LINE)))
        lab = alt.Chart(df[df.pic]).mark_text(dy=-10, color=AMBER, fontWeight="bold").encode(x="Hz:Q", y="énergie:Q", text=alt.Text("Hz:Q", format="d"))
        ui.chart(style(bars + lab, 250))
        explain("Étape 2 — Décomposer en fréquences",
                "Comme un prisme sépare les couleurs de la lumière, un calcul (la transformée de Fourier) sépare le son en fréquences. "
                f"Deux zones ressortent : vers <b>{peaks[0]} Hz</b> et vers <b>{peaks[1]} Hz</b>. "
                "Ces deux « bosses », appelées formants, sont la signature d'une voyelle : elles dépendent de la forme de la bouche.")
    if step >= 2:
        tab = pd.DataFrame([{"voyelle": k, "bosse 1 (Hz)": a_, "bosse 2 (Hz)": b_,
                             "écart": int(abs(a_ - peaks[0]) + abs(b_ - peaks[1]))} for k, (a_, b_) in FORMANTS.items()]).sort_values("écart")
        if step == 2:
            explain("Étape 3 — Comparer au dictionnaire",
                    f"La machine connaît la signature de chaque voyelle. Elle calcule l'écart avec ce qu'elle a mesuré "
                    f"({peaks[0]} Hz et {peaks[1]} Hz) : |bosse 1 − {peaks[0]}| + |bosse 2 − {peaks[1]}|. Le plus petit écart gagne.")
            st.dataframe(tab, hide_index=True, **ui.stretch(st.dataframe))
        else:
            best = tab.iloc[0]
            _result("La machine a reconnu", f"« {best.voyelle} »",
                    f"Écart de seulement {best['écart']} Hz. Réponse cachée : « {v} » — "
                    + ("bonne réponse ✅" if best.voyelle == v else "raté ❌"))
            explain("Et pour une phrase entière ?",
                    "On découpe le son en tranches de quelques millisecondes et on refait ce calcul pour chacune. "
                    "Les tranches mises côte à côte forment un <b>spectrogramme</b> : une image du son, qu'un réseau de neurones apprend à lire "
                    "comme on lit une partition.")
    takeaway("Reconnaître la parole, c'est <b>transformer le son en image de fréquences</b>, puis reconnaître des motifs dans cette image. "
             "Les assistants vocaux font la même chose, avec des modèles appris sur des milliers d'heures de voix.")


# ═════════════════════════════ 9. Apprendre à marcher ═════════════════════════════
def _distance(L, f):
    if L > 0.85 or f > 2.6:
        return 0.3
    return 2 + 18 * np.exp(-((L - 0.55) / 0.2) ** 2 - ((f - 1.7) / 0.6) ** 2)


@st.cache_data
def _hill_climb(seed, n=40, step=0.35):
    rng = np.random.default_rng(seed)
    cur = np.array([0.2, 0.8])
    cur_d = _distance(*cur)
    log = [dict(i=0, base=cur.copy(), cand=cur.copy(), d=cur_d, record=cur_d, kept=True)]
    for i in range(1, n + 1):
        cand = np.clip(cur + rng.normal(0, step, 2) * [0.35, 1.0], [0.1, 0.5], [1.0, 3.0])
        d = _distance(*cand)
        kept = d > cur_d
        log.append(dict(i=i, base=cur.copy(), cand=cand, d=d, record=max(d, cur_d), kept=kept))
        if kept:
            cur, cur_d = cand, d
    return log


@st.cache_data
def _walk_grid():
    Ls, fs = np.linspace(0.1, 1.0, 30), np.linspace(0.5, 3.0, 30)
    return pd.DataFrame([{"pas": L, "rythme": f, "d": _distance(L, f)} for L in Ls for f in fs])


def walk():
    scenario("Un robot à deux jambes doit apprendre à marcher le plus loin possible en 10 secondes. "
             "Il n'a que deux réglages : la <b>longueur de son pas</b> et son <b>rythme</b>. Personne ne connaît les bons réglages.")
    seed = _seed_button("walk")
    log = _hill_climb(seed)
    step = stepper("walk", len(log), [f"essai {e['i']}" for e in log])
    e = log[step]
    fell = e["d"] < 1
    pos = min(e["d"] / 22, 1) * 100
    rec = min(e["record"] / 22, 1) * 100
    html(f"<div class='track'><div class='rec' style='left:{rec:.0f}%'><span>record {e['record']:.1f} m</span></div>"
         f"<div class='bot' style='left:{pos:.0f}%'>{'💥' if fell else '🤖'}</div>"
         f"<div class='ticks'>{''.join(f'<span>{m} m</span>' for m in range(0, 23, 5))}</div></div>")
    L, f = e["cand"]
    if e["i"] == 0:
        explain("Premier essai", f"Le robot démarre avec des petits pas lents (pas {L:.2f} m, rythme {f:.1f} pas/s). "
                f"Il parcourt {e['d']:.1f} m. C'est son premier record.")
    else:
        bL, bf = e["base"]
        calc([f"<i>1. Partir du meilleur réglage connu</i> : pas {bL:.2f} m, rythme {bf:.2f} pas/s",
              f"<i>2. Le modifier un peu, au hasard</i> : pas <b>{L:.2f}</b> m, rythme <b>{f:.2f}</b> pas/s",
              "<i>3. Essayer</i> : " + ("💥 chute après quelques pas !" if fell else f"il parcourt {e['d']:.1f} m"),
              f"<i>4. Décider</i> : " + (f"<b>✅ {e['d']:.1f} m &gt; ancien record, on garde ce réglage</b>" if e["kept"]
                                         else f"<b>✗ pas mieux que {e['record']:.1f} m, on revient au réglage précédent</b>")])
    trials = pd.DataFrame([{"pas": x["cand"][0], "rythme": x["cand"][1], "kept": x["kept"], "i": x["i"]} for x in log[: step + 1]])
    path = trials[trials.kept]
    heat = alt.Chart(_walk_grid()).mark_rect().encode(
        x=alt.X("pas:Q", bin=alt.Bin(maxbins=30), title="Longueur du pas (m)"),
        y=alt.Y("rythme:Q", bin=alt.Bin(maxbins=30), title="Rythme (pas/s)"),
        color=alt.Color("d:Q", scale=alt.Scale(range=[BG, "#4A3C1C", AMBER]), legend=None))
    tried = alt.Chart(trials).mark_circle(size=40, color=GRAY).encode(x="pas:Q", y="rythme:Q")
    p = alt.Chart(path).mark_line(color=INK, point=alt.OverlayMarkDef(color=INK, size=50)).encode(x="pas:Q", y="rythme:Q", order="i:Q")
    now = alt.Chart(trials.tail(1)).mark_point(size=300, color=RED if fell else CYAN, strokeWidth=3).encode(x="pas:Q", y="rythme:Q")
    with st.expander("Voir la carte cachée des réglages (le robot, lui, ne la voit pas)", expanded=False):
        ui.chart(style(heat + tried + p + now, 300))
        st.caption("Zones claires : réglages qui font marcher loin. Ligne blanche : chemin des records. Points gris : essais ratés.")
    takeaway("Essayer, mesurer, garder ce qui marche mieux : c'est l'apprentissage par essais et erreurs. "
             "Les vrais robots font des <b>millions d'essais en simulation</b> avant de poser un pied dans le monde réel.")


# ═════════════════════════════ 10. Monte-Carlo au morpion ═════════════════════════════
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
NAMES = ["en haut à gauche", "en haut au milieu", "en haut à droite", "au milieu à gauche", "au centre",
         "au milieu à droite", "en bas à gauche", "en bas au milieu", "en bas à droite"]


def _winner(b):
    for a, c, d in LINES:
        if b[a] and b[a] == b[c] == b[d]:
            return b[a]
    return 0


def _playout(start, move, rng):
    b = list(start)
    b[move] = 1
    order = {move: 1}
    player, k = 2, 2
    w = _winner(b)
    while not w and 0 in b:
        free = [i for i in range(9) if b[i] == 0]
        m = int(rng.choice(free))
        b[m] = player
        order[m] = k
        k += 1
        player = 3 - player
        w = _winner(b)
    return b, order, w


@st.cache_data
def _mc_counts(start, n=200, seed=1):
    rng = np.random.default_rng(seed)
    res = {}
    for m in range(9):
        if start[m]:
            continue
        c = {1: 0, 0: 0, 2: 0}
        for _ in range(n):
            c[_playout(start, m, rng)[2]] += 1
        res[m] = c
    return res


def _board(b, order=None, scores=None, best=None):
    cells = []
    for i in range(9):
        s = {1: "✕", 2: "○"}.get(b[i], "")
        cls = "x" if b[i] == 1 else "o" if b[i] == 2 else ""
        sub = ""
        if order and i in order:
            sub = f"<small>{order[i]}</small>"
        if scores and i in scores:
            s, cls = f"{scores[i]:.0%}", "sc"
        if best is not None and i == best:
            cls += " best"
        cells.append(f"<div class='cell {cls}'>{s}{sub}</div>")
    return f"<div class='board'>{''.join(cells)}</div>"


def montecarlo():
    scenario("La machine joue ✕ au morpion. Elle ne connaît <b>aucune stratégie</b>. Pour choisir sa case, "
             "elle va imaginer des centaines de fins de partie jouées au hasard, et compter.")
    sits = {"Plateau vide": (0,) * 9, "○ a pris le centre": (0, 0, 0, 0, 2, 0, 0, 0, 0),
            "○ menace une ligne": (2, 2, 0, 0, 1, 0, 0, 0, 0)}
    sit = st.selectbox("Situation de départ", list(sits))
    start = sits[sit]
    counts = _mc_counts(start)
    scores = {m: (c[1] + 0.5 * c[0]) / sum(c.values()) for m, c in counts.items()}
    best = max(scores, key=scores.get)
    step = stepper("mc", 3, ["Imaginer une partie", "Recommencer 200 fois", "Choisir"])

    if step == 0:
        free = list(counts)
        cand = st.selectbox("Case candidate à tester", free, format_func=lambda m: NAMES[m],
                            index=free.index(4) if 4 in free else 0)
        rng = np.random.default_rng(st.session_state.get("mc_roll", 0))
        if st.button("🎲  Imaginer 3 autres parties", key="mc_reroll"):
            st.session_state["mc_roll"] = st.session_state.get("mc_roll", 0) + 1
            rng = np.random.default_rng(st.session_state["mc_roll"])
        cols = st.columns(3)
        for c in cols:
            b, order, w = _playout(start, cand, rng)
            c.markdown(_board(b, order) + f"<div class='verdict-s {'win' if w == 1 else 'loss' if w == 2 else ''}'>"
                       f"{'✕ gagne' if w == 1 else '○ gagne' if w == 2 else 'match nul'}</div>", unsafe_allow_html=True)
        explain("Étape 1 — Imaginer la suite au hasard",
                f"La machine pose ✕ {NAMES[cand]} (coup n°1), puis joue la fin de partie <b>complètement au hasard</b> pour les deux camps. "
                "Les petits numéros indiquent l'ordre des coups. Une seule partie ne prouve rien… mais des centaines, si.")
    elif step == 1:
        tab = pd.DataFrame([{"case": NAMES[m], "✕ gagne": c[1], "nul": c[0], "○ gagne": c[2],
                             "score": f"{scores[m]:.0%}"} for m, c in counts.items()]).sort_values("score", ascending=False)
        explain("Étape 2 — Recommencer 200 fois pour chaque case",
                "Pour chaque case libre, 200 parties imaginées. Score = (victoires + ½ × nuls) ÷ 200.")
        st.dataframe(tab, hide_index=True, **ui.stretch(st.dataframe))
    else:
        a, b = st.columns([1, 1.4])
        a.markdown(_board(start, scores=scores, best=best), unsafe_allow_html=True)
        with b:
            _result("Coup choisi", f"✕ {NAMES[best]}", f"Score {scores[best]:.0%} sur 200 parties imaginées.")
            explain("Étape 3 — Jouer la case au meilleur score",
                    "Sans connaître la moindre règle de stratégie, la machine retrouve ce qu'un bon joueur sait : "
                    "le centre est fort, et il faut bloquer une ligne menacée.")
    takeaway("AlphaGo utilisait cette idée — <b>simuler beaucoup de suites possibles</b> — guidée par des réseaux de neurones "
             "qui lui disent quels coups méritent d'être explorés. C'est ainsi qu'elle a trouvé des coups qu'aucun humain n'attendait.")


# ═════════════════════════════ 11. Le bandit manchot ═════════════════════════════
TRUE_P = np.array([0.20, 0.35, 0.50, 0.30, 0.65])


@st.cache_data
def _bandit_log(eps, seed, rounds=60):
    rng = np.random.default_rng(seed)
    tries, wins = np.zeros(5, int), np.zeros(5, int)
    log = []
    for t in range(1, rounds + 1):
        est = np.where(tries > 0, wins / np.maximum(tries, 1), 0.0)
        dice = rng.random()
        if dice < eps or tries.sum() == 0:
            a, mode = int(rng.integers(5)), "explore"
        else:
            a, mode = int(np.argmax(est + rng.random(5) * 1e-6)), "exploite"
        r = int(rng.random() < TRUE_P[a])
        log.append(dict(t=t, dice=dice, mode=mode, a=a, r=r, est_before=est.copy(),
                        tries=(tries + np.eye(5, dtype=int)[a]).copy(), wins=(wins + r * np.eye(5, dtype=int)[a]).copy()))
        tries[a] += 1
        wins[a] += r
    return log


def bandit():
    scenario("Cinq machines à sous. Chacune a une chance de gain <b>cachée</b>. L'agent a 60 jetons. "
             "Doit-il rejouer la machine qui lui a déjà rapporté, ou en essayer d'autres ? C'est le dilemme <b>explorer ou exploiter</b>.")
    c1, c2 = st.columns([3, 1])
    eps = c1.slider("Curiosité ε : part des tours où l'agent explore au hasard", 0.0, 1.0, 0.2, 0.05)
    with c2:
        seed = _seed_button("bandit")
    log = _bandit_log(eps, seed)
    reveal = st.toggle("Révéler les vraies chances (l'agent, lui, ne les connaît pas)")
    step = stepper("bandit", len(log), [f"jeton {e['t']}" for e in log])
    e = log[step]
    est = np.where(e["tries"] > 0, e["wins"] / np.maximum(e["tries"], 1), 0)
    cards = []
    for m in range(5):
        cls = "machine on" if m == e["a"] else "machine"
        truth = f"<div class='truth'>vraie : {TRUE_P[m]:.0%}</div>" if reveal else ""
        cards.append(f"<div class='{cls}'><div class='mi'>🎰</div><div class='mn'>Machine {m + 1}</div>"
                     f"<div class='ms'>{e['wins'][m]} gain(s) / {e['tries'][m]} essai(s)</div>"
                     f"<div class='mb'><div style='width:{est[m] * 100:.0f}%'></div></div>"
                     f"<div class='me'>estimation {est[m]:.0%}</div>{truth}</div>")
    html(f"<div class='machines'>{''.join(cards)}</div>")
    eb = e["est_before"]
    if e["mode"] == "explore":
        decision = (f"dé = {e['dice']:.2f} &lt; ε = {eps:.2f}  →  <b>j'explore</b> : je tire une machine au hasard → machine {e['a'] + 1}")
    else:
        decision = (f"dé = {e['dice']:.2f} ≥ ε = {eps:.2f}  →  <b>j'exploite</b> : je joue la meilleure estimation "
                    f"→ machine {e['a'] + 1} ({eb[e['a']]:.0%})")
    calc([f"Jeton n°{e['t']}", decision,
          f"Résultat : {'💰 gagné !' if e['r'] else 'perdu'}  →  nouvelle estimation de la machine {e['a'] + 1} = "
          f"{e['wins'][e['a']]} ÷ {e['tries'][e['a']]} = <b>{est[e['a']]:.0%}</b>"])
    total = int(e["wins"].sum())
    _result("Gains cumulés", f"{total} sur {e['t']} jetons",
            f"Machine la plus jouée : n°{int(np.argmax(e['tries'])) + 1}. La meilleure est la n°5 (65 %). "
            "Avec ε = 0, l'agent s'accroche souvent à la première machine qui a payé.")
    takeaway("L'agent apprend uniquement grâce aux <b>récompenses</b>. Trop peu de curiosité, il rate la meilleure option ; "
             "trop, il gaspille ses jetons. Le même principe a servi à entraîner AlphaGo et à affiner les assistants conversationnels.")


# ═════════════════════════════ 12. Le modèle de langage ═════════════════════════════
CORPUS_TXT = """le chat dort sur le canapé . le chat regarde la fenêtre . le chat mange dans la cuisine .
le chien dort dans le jardin . le chien court dans le jardin . le chien regarde le chat .
la fourmi cherche la nourriture . la fourmi suit le chemin . la fourmi trouve le chemin le plus court .
la machine apprend vite . la machine regarde les images . la machine apprend avec les exemples .
la machine écrit une phrase . le poète écrit une phrase étrange . le poète regarde la lune .
le perroquet répète la phrase . le perroquet répète le mot . le cerveau apprend avec les exemples .
le cerveau cherche le sens . la lune regarde le jardin . le robot apprend à marcher .
le robot tombe dans le jardin . le robot cherche le chemin . le chat suit la fourmi ."""
CORPUS = CORPUS_TXT.split()


@st.cache_data
def _bigrams():
    vocab = sorted(set(CORPUS))
    idx = {w: i for i, w in enumerate(vocab)}
    M = np.zeros((len(vocab), len(vocab)))
    for a, b in zip(CORPUS, CORPUS[1:]):
        M[idx[a], idx[b]] += 1
    return vocab, idx, M


def _probs(row, temp):
    with np.errstate(divide="ignore"):
        logits = np.log(np.where(row > 0, row, 1e-12))
    z = np.exp((logits - logits.max()) / temp) * (row > 0)
    return z / z.sum()


@st.cache_data
def _generate(start, temp, seed, max_len=12):
    vocab, idx, M = _bigrams()
    rng = np.random.default_rng(seed)
    words, steps = [start], []
    w = start
    for _ in range(max_len):
        row = M[idx[w]]
        p = _probs(row, temp)
        dice = rng.random()
        nxt = vocab[int(np.searchsorted(np.cumsum(p), dice))]
        steps.append(dict(prev=w, counts={vocab[i]: int(row[i]) for i in np.nonzero(row)[0]},
                          probs={vocab[i]: float(p[i]) for i in np.nonzero(row)[0]}, dice=dice, chosen=nxt))
        if nxt == ".":
            break
        words.append(nxt)
        w = nxt
    return steps


def language():
    scenario("Un mini-modèle de langage a lu 24 phrases (voir plus bas). Il n'a retenu qu'une chose : "
             "<b>quel mot suit quel mot, et combien de fois</b>. Regardez-le écrire une phrase, mot par mot.")
    c1, c2, c3 = st.columns([1, 2, 1.4])
    start = c1.selectbox("Premier mot", ["le", "la"])
    temp = c2.slider("Température (audace)", 0.3, 3.0, 1.0, 0.1)
    with c3:
        seed = _seed_button("lm", "✨  Autre phrase")
    steps = _generate(start, temp, seed)
    i = stepper("lm", len(steps), [f"mot {k + 1}" for k in range(len(steps))])
    s = steps[i]
    words = [start] + [x["chosen"] for x in steps[: i + 1]]
    shown = " ".join(w for w in words[:-1]) + f" <mark>{words[-1]}</mark>"
    html(f"<div class='quote'>{shown}</div>")

    counts = " · ".join(f"« {w} » ×{c}" for w, c in sorted(s["counts"].items(), key=lambda x: -x[1]))
    explain(f"Quel mot après « {s['prev']} » ?",
            f"Dans les textes lus, après « {s['prev']} », le modèle a vu : {counts}. "
            "Il transforme ces comptes en probabilités, puis <b>tire au sort</b> selon ces probabilités.")
    pdf = pd.DataFrame([{"mot": w, "p": p, "choisi": w == s["chosen"]} for w, p in s["probs"].items()]).sort_values("p", ascending=False).head(10)
    bars = alt.Chart(pdf).mark_bar(cornerRadius=5, height=20).encode(
        x=alt.X("p:Q", title="Probabilité", axis=alt.Axis(format="%")), y=alt.Y("mot:N", sort="-x", title=None),
        color=alt.condition("datum.choisi", alt.value(AMBER), alt.value(LINE)))
    ui.chart(style(bars, max(90, 28 * len(pdf))))
    calc([f"Tirage au sort : dé = {s['dice']:.2f}  →  mot choisi : <b>« {s['chosen']} »</b>"
          + ("  (fin de phrase)" if s["chosen"] == "." else "")])
    takeaway("Le modèle ne sait pas ce qu'est un chat : il <b>prolonge des statistiques</b>. ChatGPT ou Claude font la même chose "
             "avec des milliards de textes et en regardant des milliers de mots en arrière, pas un seul. "
             "Température basse : prudent et répétitif. Haute : surprenant… ou absurde.")
    with st.expander("Les 24 phrases lues par le modèle"):
        st.write(CORPUS_TXT.replace(" .", ".").replace("\n", " "))


# ═════════════════════════════ 13. Le médecin ═════════════════════════════
@st.cache_data
def _patients():
    rng = np.random.default_rng(11)
    sick = rng.normal(68, 13, 8).clip(1, 99).round().astype(int)
    healthy = rng.normal(36, 14, 32).clip(1, 99).round().astype(int)
    df = pd.DataFrame({"score": np.r_[sick, healthy], "malade": [True] * 8 + [False] * 32})
    return df.sort_values("score").reset_index(drop=True)


def medical():
    scenario("40 personnes passent un dépistage. 8 sont réellement malades (point rouge — ce que l'IA ignore). "
             "L'IA donne à chacune un <b>score de risque</b> de 0 à 100. Où placer le seuil qui déclenche une alerte pour le médecin ?")
    df = _patients()
    thr = st.slider("Seuil d'alerte : au-dessus, le dossier est envoyé au médecin", 0, 100, 62)
    cells = []
    placed = False
    for _, r in df.iterrows():
        if not placed and r.score >= thr:
            cells.append("<div class='seuil'><span>seuil</span></div>")
            placed = True
        alert = r.score >= thr
        cat = ("tp" if r.malade else "fp") if alert else ("fn" if r.malade else "tn")
        cells.append(f"<div class='pt {cat}'><div class='ps'>{r.score}</div><div class='pi'>{'🔔' if alert else '🧍'}</div>"
                     f"{'<div class=dot></div>' if r.malade else ''}</div>")
    if not placed:
        cells.append("<div class='seuil'><span>seuil</span></div>")
    html(f"<div class='patients'>{''.join(cells)}</div>")
    html("<div class='legend'>Patients rangés par score croissant · 🔔 alerte · point rouge = réellement malade</div>")
    tp = int(((df.score >= thr) & df.malade).sum())
    fn = int(((df.score < thr) & df.malade).sum())
    fp = int(((df.score >= thr) & ~df.malade).sum())
    tn = 40 - tp - fn - fp
    html(f"<div class='cats'><div class='cat tp'><b>{tp}</b>malades détectés</div><div class='cat fn'><b>{fn}</b>malades manqués</div>"
         f"<div class='cat fp'><b>{fp}</b>fausses alertes</div><div class='cat tn'><b>{tn}</b>personnes rassurées à raison</div></div>")
    explain("Ce qu'il faut regarder",
            f"Avec un seuil à {thr} : l'IA repère <b>{tp} malades sur 8</b> ({tp / 8:.0%}), en manque <b>{fn}</b>, "
            f"et inquiète à tort <b>{fp}</b> personnes en bonne santé. Baissez le seuil : moins de malades manqués, mais plus de fausses alertes. "
            "Montez-le : l'inverse. <b>Il n'existe pas de seuil parfait</b>, parce que les scores des malades et des bien-portants se chevauchent.")
    takeaway("Choisir le seuil n'est pas une question technique mais <b>médicale et humaine</b> : vaut-il mieux inquiéter quelques personnes "
             "pour rien, ou rater un malade ? L'IA trie et signale ; le médecin vérifie et décide.")


# ═════════════════════════════ 14. La créativité ═════════════════════════════
ANG = np.arange(12) * 30
SH = {
    "Cercle": np.ones(12),
    "Étoile": np.array([1.0, 0.42] * 6),
    "Carré": np.round(0.8 / np.maximum(np.abs(np.cos(np.radians(ANG + 45))), np.abs(np.sin(np.radians(ANG + 45)))), 2),
    "Fleur": np.array([1.0, 0.75, 0.75] * 4),
    "Goutte": np.array([0.55, 0.6, 0.75, 1.0, 0.75, 0.6, 0.55, 0.5, 0.45, 0.45, 0.45, 0.5]),
}


def _shape_chart(r, color, size, rays=False, labels=False):
    th = np.radians(ANG)
    df = pd.DataFrame({"x": r * np.cos(th), "y": r * np.sin(th), "o": range(12), "r": r})
    sc = alt.Scale(domain=[-1.3, 1.3])
    layers = []
    if rays:
        rr = pd.DataFrame([{"x": 0, "y": 0, "k": k} for k in range(12)] +
                          [{"x": df.x[k], "y": df.y[k], "k": k} for k in range(12)])
        layers.append(alt.Chart(rr).mark_line(color=LINE, strokeWidth=1).encode(x=alt.X("x:Q", axis=None, scale=sc), y=alt.Y("y:Q", axis=None, scale=sc), detail="k:N"))
    layers.append(alt.Chart(df).mark_line(color=color, strokeWidth=3, interpolate="cardinal-closed").encode(
        x=alt.X("x:Q", axis=None, scale=sc), y=alt.Y("y:Q", axis=None, scale=sc), order="o:Q"))
    layers.append(alt.Chart(df).mark_circle(color=color, size=40 if rays else 0).encode(x="x:Q", y="y:Q"))
    if labels:
        layers.append(alt.Chart(df.assign(t=df.r.map(lambda v: f"{v:.2f}"), x=df.x * 1.18, y=df.y * 1.18)).mark_text(
            fontSize=10, color=GRAY).encode(x="x:Q", y="y:Q", text="t:N"))
    return alt.layer(*layers).properties(width=size, height=size)


def creativity():
    scenario("Une IA d'images ne stocke pas des dessins : elle les transforme en <b>listes de nombres</b>. "
             "Ici, une forme est décrite par 12 nombres : la longueur de 12 rayons partant du centre. Que se passe-t-il si l'on mélange deux listes ?")
    c1, c2 = st.columns(2)
    a = c1.selectbox("Forme A", list(SH), index=0)
    b = c2.selectbox("Forme B", list(SH), index=1)
    step = stepper("crea", 3, ["Une forme = 12 nombres", "Mélanger les nombres", "Une forme nouvelle"])
    A, B = SH[a], SH[b]
    if step == 0:
        x, y = st.columns(2)
        with x:
            ui.chart(style(_shape_chart(A, CYAN, 260, rays=True, labels=True), 260), full=False)
        with y:
            ui.chart(style(_shape_chart(B, AMBER, 260, rays=True, labels=True), 260), full=False)
        explain("Étape 1 — Chaque forme est une liste de 12 nombres",
                f"{a} : [{', '.join(f'{v:.2f}' for v in A)}]<br>{b} : [{', '.join(f'{v:.2f}' for v in B)}]<br>"
                "En reliant le bout des 12 rayons par une courbe douce, on retrouve la forme.")
    t = st.slider("Dosage du mélange (0 = tout A, 1 = tout B)", 0.0, 1.0, 0.5, 0.05) if step >= 1 else 0.5
    R = (1 - t) * A + t * B
    if step == 1:
        rows = [f"rayon {k + 1} ({ANG[k]}°) : {1 - t:.2f} × {A[k]:.2f} + {t:.2f} × {B[k]:.2f} = <b>{R[k]:.2f}</b>" for k in range(4)]
        explain("Étape 2 — Mélanger, nombre par nombre",
                "Pour chaque rayon, on prend un peu de A et un peu de B. C'est tout : une simple moyenne pondérée.")
        calc(rows + ["… et de même pour les 8 autres rayons."])
        ui.chart(style(_shape_chart(R, INK, 280, rays=True, labels=True), 280), full=False)
    if step == 2:
        ui.chart(style(_shape_chart(R, INK, 300), 300), full=False)
        strip = alt.hconcat(*[_shape_chart((1 - s) * A + s * B, CYAN if s == 0 else AMBER if s == 1 else INK, 80)
                              for s in np.linspace(0, 1, 6)], spacing=10)
        ui.chart(strip.configure_view(strokeWidth=0).properties(background="transparent"), full=False)
        explain("Étape 3 — Des formes que personne n'a dessinées",
                "Aucune de ces formes intermédiaires n'existait dans les exemples. Elles sont nées d'un simple déplacement "
                "entre deux points de l'« espace des nombres ». Les IA d'images font la même chose avec des milliers de nombres par image.")
    takeaway("Quand une IA « imagine », elle <b>se promène entre des choses apprises</b>. Est-ce inventer, ou recombiner ? "
             "Beaucoup d'idées humaines naissent aussi d'associations inattendues — c'est toute la question du chapitre.")


# ═════════════════════════════ 15. Humain ou machine ? ═════════════════════════════
DUELS = [
    ("Calculer 10 millions d'additions en une seconde", "Machine", "Sans aucune hésitation."),
    ("Reconnaître un nouvel animal après l'avoir vu une seule fois", "Humain",
     "Un enfant généralise avec très peu d'exemples ; une machine en demande souvent des milliers."),
    ("Apprendre en ne consommant que l'énergie d'une ampoule", "Humain", "Notre cerveau fonctionne avec environ 20 watts."),
    ("Lire et résumer mille documents en une minute", "Machine", "La vitesse de lecture des machines est sans rival."),
    ("Décider ce qui est juste dans une situation inédite", "Humain", "Les valeurs, le contexte, la responsabilité : cela reste à nous."),
    ("Battre le champion du monde de go", "Machine", "C'est arrivé — et cela a surpris tout le monde."),
]


def compare():
    scenario("Après quinze chapitres, faisons le point. Pour chaque défi, qui l'emporte aujourd'hui selon vous ?")
    score = answered = 0
    for i, (q, ans, why) in enumerate(DUELS):
        html(f"<div class='duel'>{q}</div>")
        pick = st.radio(q, ["🧠 Humain", "🤖 Machine"], index=None, horizontal=True, key=f"duel{i}", label_visibility="collapsed")
        if pick:
            answered += 1
            ok = ans in pick
            score += ok
            html(f"<div class='verdict {'ok' if ok else 'ko'}'>{'✓' if ok else '✗'} {ans} — {why}</div>")
    if answered == len(DUELS):
        _result("Votre score", f"{score} / {len(DUELS)}",
                "Les machines nous dépassent en vitesse et en mémoire. Le sens, la sobriété et le choix restent humains.")
    takeaway("La vraie question n'est peut-être pas « qui est le plus intelligent ? », mais <b>« que voulons-nous faire ensemble ? »</b>")


REGISTRY = {
    "neuron": neuron, "knn": knn, "perceptron": perceptron, "ants": ants, "genetic": genetic,
    "swarm": swarm, "vision": vision, "speech": speech, "walk": walk, "montecarlo": montecarlo,
    "bandit": bandit, "language": language, "medical": medical, "creativity": creativity,
    "compare": compare,
}
