"""Contenu pédagogique de l'application « Avant l'IA, il y avait nous ».

Chaque chapitre suit la même trame que le livre :
la nature → l'idée → comment ça marche → un exemple concret → aujourd'hui.
Pour modifier un texte, il suffit d'éditer ce fichier.
"""

BOOK = {
    "title": "Avant l'IA, il y avait nous",
    "subtitle": "Comment la nature et notre intelligence ont inspiré les machines d'aujourd'hui",
    "author": "Amine CHAÏBI",
    "author_title": "Docteur en informatique · Spécialiste de l'apprentissage automatique",
    "author_bio": [
        "Docteur en informatique, spécialiste de l'apprentissage automatique (machine learning) et de la fouille de données. "
        "Thèse soutenue en 2013 au Laboratoire d'informatique de Paris-Nord (LIPN), Université Paris 13, "
        "sur l'apprentissage topologique non supervisé.",
        "Il a enseigné l'algorithmique et les bases de données à l'université, avant de poursuivre son parcours "
        "dans l'industrie, autour de la data science et de l'apprentissage automatique. Il a aussi publié des chroniques sur le Journal du Net.",
        "L'idée du livre est née d'un atelier sur les algorithmes inspirés des fourmis : raconter les liens entre "
        "l'intelligence humaine, la nature et l'IA, sans exiger la moindre connaissance technique.",
    ],
    "links": [
        ("Publications scientifiques (DBLP)", "https://dblp.org/pid/116/6363"),
        ("Chroniques sur le Journal du Net", "https://www.journaldunet.com/account/amine-chaibi-17708"),
    ],
}

PARTS = [
    {"id": 1, "label": "Partie I", "title": "Le plus extraordinaire des modèles : nous-mêmes"},
    {"id": 2, "label": "Partie II", "title": "Quand la nature devient ingénieure"},
    {"id": 3, "label": "Partie III", "title": "Apprendre aux machines à voir, entendre et agir"},
    {"id": 4, "label": "Partie IV", "title": "Quand les machines apprennent à nous surprendre"},
    {"id": 5, "label": "Partie V", "title": "L'homme face à son invention"},
]

CHAPTERS = [
    # ───────────────────────────── PARTIE I ─────────────────────────────
    {
        "num": 1, "part": 1, "icon": "🧠",
        "title": "Un kilo et demi de mystère",
        "tagline": "Comment le cerveau a inspiré une nouvelle manière de concevoir les machines.",
        "nature": "Un kilo et demi : c'est à peu près le poids de notre cerveau. Il compte environ 86 milliards de neurones. Aucun d'eux n'est intelligent "
                  "seul : chacun reçoit des signaux, les additionne et décide de « s'allumer » ou non. "
                  "L'intelligence naît de leurs connexions.",
        "idea": "Et si, au lieu d'écrire toutes les règles à la main, on construisait une machine faite "
                "de petites unités simples, reliées entre elles, et capables d'ajuster la force de leurs liens ?",
        "how": [
            "Un neurone artificiel reçoit des nombres en entrée.",
            "Il multiplie chacun par un **poids** : l'importance qu'il lui accorde.",
            "Il additionne le tout et compare le résultat à un **seuil**.",
            "Au-dessus du seuil, il s'active. En dessous, il reste silencieux.",
        ],
        "example": "Décider d'aller courir : « il fait beau » (+), « je suis fatigué » (−), « un ami m'attend » (++). "
                   "Votre cerveau pèse ces signaux sans y penser. Un neurone artificiel fait exactement ce calcul.",
        "today": "Les grands modèles d'IA actuels empilent des milliards de ces petites unités. "
                 "Le principe reste celui d'un neurone qui pèse et additionne.",
        "demo": "neuron",
    },
    {
        "num": 2, "part": 1, "icon": "🐱",
        "title": "Le bébé qui savait reconnaître un chat",
        "tagline": "Comment reconnaître ce qu'on n'a jamais vu exactement de la même façon.",
        "nature": "Personne n'a donné à un enfant la définition d'un chat. Il en a vu quelques-uns, "
                  "et un jour il en reconnaît un nouveau, d'une couleur jamais vue, sous un angle inédit.",
        "idea": "Plutôt que de programmer des règles, on montre des exemples à la machine "
                "et on la laisse trouver ce qui les rapproche : c'est l'**apprentissage automatique**.",
        "how": [
            "On décrit chaque exemple par quelques caractéristiques (taille, forme des oreilles…).",
            "On indique pour chacun la bonne réponse : chat ou chien.",
            "Face à un animal inconnu, la machine cherche les exemples qui lui ressemblent le plus.",
            "Elle répond comme la majorité de ses « voisins ».",
        ],
        "example": "Un animal de 4 kg, aux oreilles pointues, qui miaule un peu : ses plus proches voisins "
                   "connus sont des chats. Verdict : chat — sans qu'aucune règle n'ait été écrite.",
        "today": "Les filtres anti-spam, les recommandations de films ou la détection de fraude bancaire "
                 "reposent sur ce même principe : apprendre à partir d'exemples.",
        "neo": "Néo a deux ans. Il pointe le doigt vers la fenêtre : « Chat ! » C'est un renard. "
               "Il n'a pas tout à fait tort : il a appris, il généralise… et il se trompera de moins en moins.",
        "demo": "knn",
    },
    {
        "num": 3, "part": 1, "icon": "⚡",
        "title": "Le neurone qui rêvait d'être une machine",
        "tagline": "Des premières équations du neurone aux réseaux qui apprennent.",
        "nature": "Quand nous apprenons, certaines connexions entre neurones se renforcent, d'autres s'affaiblissent. "
                  "Apprendre, c'est modifier des liens.",
        "idea": "Donner à un neurone artificiel la capacité de **corriger ses poids** à chaque erreur. "
                "Une machine qui ne se contente pas de calculer : elle s'améliore.",
        "how": [
            "Le neurone fait une prédiction avec ses poids actuels.",
            "On la compare à la bonne réponse.",
            "S'il se trompe, on déplace légèrement ses poids dans la direction qui aurait évité l'erreur.",
            "On recommence sur tous les exemples, encore et encore, jusqu'à ce qu'il ne se trompe plus.",
        ],
        "example": "Séparer des points bleus et orange sur une feuille : au début, la ligne du neurone est tracée au hasard. "
                   "Erreur après erreur, elle pivote et glisse jusqu'à séparer les deux groupes.",
        "today": "En empilant des couches de neurones, on obtient les réseaux profonds (« deep learning ») "
                 "qui reconnaissent les visages, traduisent les langues ou conduisent des voitures.",
        "demo": "perceptron",
    },
    # ───────────────────────────── PARTIE II ─────────────────────────────
    {
        "num": 4, "part": 2, "icon": "🐜",
        "title": "Le génie caché d'une colonie de fourmis",
        "tagline": "Sans chef, sans carte, une colonie trouve le chemin le plus court.",
        "nature": "Chaque fourmi dépose une trace chimique, la phéromone. Celles qui prennent le chemin le plus court "
                  "font l'aller-retour plus vite : leur chemin se charge plus vite en odeur, et attire davantage les suivantes.",
        "idea": "Lâcher des « fourmis virtuelles » dans un problème : chacune construit une solution, "
                "et les meilleures laissent plus de phéromone pour guider les suivantes.",
        "how": [
            "Les fourmis choisissent un chemin, au départ presque au hasard.",
            "Chaque chemin reçoit de la phéromone, d'autant plus qu'il est court.",
            "La phéromone s'évapore un peu à chaque tour : les mauvaises pistes s'effacent.",
            "Petit à petit, presque toutes les fourmis suivent le meilleur chemin.",
        ],
        "example": "Deux ponts relient la fourmilière à la nourriture, l'un deux fois plus long que l'autre. "
                   "En quelques dizaines d'allers-retours, la colonie a « choisi » le court — sans que personne ne décide.",
        "today": "Ces algorithmes aident à organiser des tournées de livraison, à router des données dans les réseaux "
                 "ou à planifier des horaires.",
        "neo": "Néo, sept ans, suit une file de fourmis jusqu'à une miette de gâteau. "
               "« Qui leur a dit où aller ? » Personne. Et c'est justement ça, le génie.",
        "demo": "ants",
    },
    {
        "num": 5, "part": 2, "icon": "🧬",
        "title": "Le jardinier de solutions",
        "tagline": "Laisser l'ordinateur faire pousser des solutions que personne n'aurait dessinées.",
        "nature": "Dans le vivant, chaque génération mélange et modifie légèrement ce qu'elle hérite. "
                  "Les variantes les mieux adaptées à leur environnement se transmettent davantage.",
        "idea": "Faire « évoluer » des solutions au lieu de les calculer : on crée une population d'essais, "
                "on garde les meilleurs, on les croise et on les modifie au hasard.",
        "how": [
            "On crée une population de solutions aléatoires.",
            "On note chacune : à quel point est-elle bonne ?",
            "On sélectionne les meilleures et on les **croise** entre elles.",
            "On ajoute de petites **mutations** au hasard, puis on recommence.",
        ],
        "example": "Retrouver une phrase cachée lettre par lettre : au départ, du charabia. "
                   "Quelques centaines de générations plus tard, la phrase apparaît — sans qu'on l'ait jamais écrite.",
        "today": "Une antenne conçue ainsi a volé sur le satellite ST5 de la NASA en 2006. Ces algorithmes optimisent aussi des emplois du temps, des formes d'ailes "
                 "et aident à régler les paramètres d'autres IA.",
        "demo": "genetic",
    },
    {
        "num": 6, "part": 2, "icon": "🐟",
        "title": "L'abeille, le poisson et le robot",
        "tagline": "L'intelligence collective, du banc de poissons à l'essaim de robots.",
        "nature": "Un banc de poissons esquive un prédateur comme un seul corps. Pourtant, chaque poisson "
                  "ne regarde que ses voisins immédiats et suit trois règles simples.",
        "idea": "Des agents simples qui partagent l'information localement peuvent résoudre ensemble "
                "des problèmes qu'aucun ne pourrait résoudre seul.",
        "how": [
            "Chaque agent explore l'espace et se souvient de sa meilleure découverte.",
            "Il est aussi attiré par la meilleure découverte du groupe.",
            "Il combine ces deux attractions avec un peu d'élan personnel.",
            "L'essaim converge peu à peu vers la meilleure zone.",
        ],
        "example": "Des drones cherchent la source d'une fuite de gaz : chacun mesure la concentration, "
                   "partage sa meilleure mesure, et l'essaim se resserre autour de la fuite.",
        "today": "Spectacles de drones, robots d'entrepôt, exploration de zones sinistrées : "
                 "l'intelligence en essaim se passe de chef central.",
        "demo": "swarm",
    },
    # ───────────────────────────── PARTIE III ─────────────────────────────
    {
        "num": 7, "part": 3, "icon": "👁️",
        "title": "La machine qui ouvrit les yeux",
        "tagline": "Des pixels aux objets : comment une machine apprend à voir.",
        "nature": "Dans notre cortex visuel, certains neurones réagissent à des traits horizontaux, d'autres à des "
                  "verticaux. Plus loin, d'autres combinent ces traits en formes, puis en visages.",
        "idea": "Faire glisser de petits **filtres** sur l'image pour détecter des motifs simples, "
                "puis combiner ces détections couche après couche.",
        "how": [
            "Pour la machine, une image n'est qu'un tableau de nombres (les pixels).",
            "Un filtre est une petite loupe de 3×3 pixels qui glisse sur toute l'image.",
            "Il s'allume là où il trouve son motif : un bord, un coin, une texture.",
            "Les couches suivantes assemblent bords → formes → objets.",
        ],
        "example": "Le filtre « bords verticaux » ne voit d'une maison que ses murs et ses fenêtres. "
                   "Le filtre « bords horizontaux » n'en voit que le toit et le sol.",
        "today": "Déverrouillage par visage, tri des photos, voitures autonomes, contrôle qualité en usine : "
                 "tout part de ces filtres.",
        "neo": "Néo, dix ans, montre une photo floue : « C'est mamie ! » Il lui a suffi d'une silhouette. "
               "Une machine, elle, a dû voir des millions d'images pour en faire autant.",
        "demo": "vision",
    },
    {
        "num": 8, "part": 3, "icon": "🎙️",
        "title": "Allô, est-ce que tu me comprends ?",
        "tagline": "De quelques mots reconnus à des conversations entières.",
        "nature": "Notre oreille interne décompose les sons en fréquences, comme un prisme décompose la lumière. "
                  "Chaque voyelle a sa propre « signature » de fréquences.",
        "idea": "Transformer la voix en image de fréquences — le **spectrogramme** — puis apprendre "
                "à y reconnaître les sons, les mots, et enfin les phrases.",
        "how": [
            "Le micro enregistre une onde : une suite de pressions de l'air.",
            "On la découpe en tranches de quelques millisecondes.",
            "Pour chaque tranche, on mesure l'énergie de chaque fréquence.",
            "Un modèle apprend à associer ces motifs à des sons, puis à des mots.",
        ],
        "example": "Le « a » et le « i » ont la même hauteur de voix, mais leurs fréquences dominantes "
                   "diffèrent nettement : sur le spectrogramme, on les distingue à l'œil.",
        "today": "Assistants vocaux, sous-titres automatiques, dictée, traduction simultanée.",
        "demo": "speech",
    },
    {
        "num": 9, "part": 3, "icon": "🦿",
        "title": "Apprendre à marcher, tomber, recommencer",
        "tagline": "Pourquoi se déplacer dans le monde réel est un défi extraordinaire.",
        "nature": "Un bébé tombe des centaines de fois avant de marcher. Il n'a pas de manuel : "
                  "il essaie, sent ce qui marche, et ajuste.",
        "idea": "Laisser le robot essayer des façons de bouger, mesurer jusqu'où il va, "
                "et garder les réglages qui le font avancer plus loin.",
        "how": [
            "On définit quelques réglages : longueur du pas, rythme, équilibre.",
            "Le robot essaie une variante légèrement différente.",
            "S'il va plus loin sans tomber, on garde ce nouveau réglage.",
            "Sinon on revient en arrière… et on réessaie autrement.",
        ],
        "example": "Un robot qui fait des pas trop grands tombe ; trop petits, il n'avance pas. "
                   "Par essais successifs, il trouve la zone d'équilibre — comme un enfant.",
        "today": "Les robots à pattes s'entraînent d'abord des millions de fois en simulation, "
                 "puis transfèrent ce savoir dans le monde réel.",
        "demo": "walk",
    },
    # ───────────────────────────── PARTIE IV ─────────────────────────────
    {
        "num": 10, "part": 4, "icon": "⚫",
        "title": "Le coup que personne n'attendait",
        "tagline": "Comment une machine a découvert des stratégies que personne ne lui avait apprises.",
        "nature": "Un joueur expérimenté « sent » les bons coups. Cette intuition vient de milliers "
                  "de parties jouées, imaginées, regrettées.",
        "idea": "Pour évaluer un coup, simuler des milliers de parties qui en partent, "
                "et voir combien se terminent par une victoire. Puis apprendre à affiner cette intuition.",
        "how": [
            "Pour chaque coup possible, on imagine la suite de la partie.",
            "On joue des milliers de fins de partie simulées.",
            "On compte les victoires : c'est la « valeur » du coup.",
            "Un réseau de neurones apprend à prédire ces valeurs sans tout simuler.",
        ],
        "example": "Au morpion, la machine découvre seule que la case centrale est la plus prometteuse, "
                   "simplement en jouant des milliers de parties contre elle-même.",
        "today": "Ces méthodes ont battu les champions de go et d'échecs, et servent désormais "
                 "à concevoir des protéines ou optimiser des puces électroniques.",
        "demo": "montecarlo",
    },
    {
        "num": 11, "part": 4, "icon": "🎯",
        "title": "La machine qui apprend de ses erreurs",
        "tagline": "L'apprentissage par renforcement : récompenses, pénalités et curiosité.",
        "nature": "Un chien apprend un tour grâce aux friandises. Personne ne lui explique : "
                  "il essaie, et ce qui est récompensé revient plus souvent.",
        "idea": "Un agent agit, reçoit une récompense ou une pénalité, et ajuste ses choix "
                "pour maximiser ses gains — en équilibrant **exploration** et **exploitation**.",
        "how": [
            "L'agent a plusieurs actions possibles, sans savoir laquelle est la meilleure.",
            "Il essaie, reçoit un score, met à jour son estimation.",
            "La plupart du temps, il choisit l'action qui semble la meilleure.",
            "De temps en temps, il tente autre chose, au cas où il se tromperait.",
        ],
        "example": "Face à cinq machines à sous, faut-il rejouer celle qui a payé une fois, "
                   "ou essayer les autres ? Trop explorer coûte ; pas assez fait rater la meilleure.",
        "today": "C'est ainsi que les assistants conversationnels ont été affinés grâce aux préférences humaines, "
                 "et que des robots apprennent des gestes complexes.",
        "demo": "bandit",
    },
    {
        "num": 12, "part": 4, "icon": "🦜",
        "title": "Le perroquet, le poète et la machine",
        "tagline": "Comment un modèle de langage écrit — et pourquoi parler n'est pas penser.",
        "nature": "Nous anticipons sans cesse le mot suivant : « Il pleut des… » — votre cerveau a déjà complété.",
        "idea": "Entraîner une machine sur d'immenses quantités de texte pour qu'elle devine le mot suivant. "
                "Mot après mot, elle compose des phrases entières.",
        "how": [
            "Le texte est découpé en morceaux (mots ou fragments de mots).",
            "Le modèle apprend, pour chaque contexte, la probabilité de chaque mot suivant.",
            "Pour écrire, il tire un mot selon ces probabilités, l'ajoute, et recommence.",
            "La « température » règle l'audace : basse = prudent, haute = créatif (voire absurde).",
        ],
        "example": "Après « le chat dort sur le… », « canapé » est très probable, « nuage » beaucoup moins. "
                   "Les grands modèles font ce calcul avec un contexte de milliers de mots.",
        "today": "ChatGPT, Claude et les autres assistants reposent sur ce principe, à une échelle gigantesque, "
                 "puis sont affinés pour être utiles et fiables.",
        "neo": "Néo, quinze ans, discute avec une IA pour son exposé. Elle répond avec aplomb… "
               "et invente une date. Il apprend une leçon précieuse : bien parler n'est pas toujours savoir.",
        "demo": "language",
    },
    # ───────────────────────────── PARTIE V ─────────────────────────────
    {
        "num": 13, "part": 5, "icon": "🩺",
        "title": "Le médecin qui ne dort jamais",
        "tagline": "Détecter, analyser, accélérer — sans remplacer le jugement du médecin.",
        "nature": "Un radiologue expérimenté a vu des dizaines de milliers d'images. "
                  "Mais il se fatigue, et certains signes sont minuscules.",
        "idea": "Une IA entraînée sur des millions d'images médicales attribue à chaque cas un **score de risque**. "
                "Le médecin décide où placer le seuil d'alerte — et garde le dernier mot.",
        "how": [
            "Le modèle donne un score entre 0 et 100 à chaque examen.",
            "Au-delà d'un seuil, le cas est signalé au médecin.",
            "Seuil bas : on rate peu de malades, mais on inquiète beaucoup de bien-portants.",
            "Seuil haut : moins de fausses alertes, mais plus de cas manqués. Il n'y a pas de seuil parfait.",
        ],
        "example": "Dans un dépistage, mieux vaut souvent quelques fausses alertes (vérifiées ensuite) "
                   "qu'un cancer manqué. Ce choix est médical et humain, pas technique.",
        "today": "Lecture de mammographies, détection de rétinopathies, découverte de médicaments : "
                 "l'IA est un second regard infatigable.",
        "demo": "medical",
    },
    {
        "num": 14, "part": 5, "icon": "💡",
        "title": "La machine peut-elle avoir une idée ?",
        "tagline": "Créativité, intuition, imagination : que signifie inventer ?",
        "nature": "Beaucoup d'idées humaines naissent d'un mélange : deux choses connues, "
                  "associées d'une façon que personne n'avait tentée.",
        "idea": "Une IA représente ce qu'elle a appris comme des points dans un vaste espace. "
                "Se promener **entre** ces points produit des formes qu'elle n'a jamais vues.",
        "how": [
            "Chaque exemple appris devient un point dans un « espace des idées ».",
            "Deux exemples éloignés peuvent être reliés par un chemin.",
            "Les étapes intermédiaires sont des créations nouvelles.",
            "La question reste ouverte : est-ce inventer, ou recombiner ?",
        ],
        "example": "Entre un cercle et une étoile, il existe une infinité de formes intermédiaires. "
                   "Aucune n'était dans les données — la machine les a « imaginées ».",
        "today": "Génération d'images et de musique, conception de molécules, "
                 "et même aide à la démonstration de théorèmes.",
        "demo": "creativity",
    },
    {
        "num": 15, "part": 5, "icon": "🪞",
        "title": "Et si nous étions devenus le modèle dépassé ?",
        "tagline": "Ce qui nous distingue encore, ce que nous ignorons, ce que nous choisirons.",
        "nature": "Notre cerveau consomme environ 20 watts — moins qu'une ampoule — et apprend "
                  "une nouvelle notion à partir de quelques exemples.",
        "idea": "Comparer honnêtement : les machines excellent là où il y a énormément de données et des règles claires. "
                "Nous restons forts là où il faut du sens, du corps, des valeurs.",
        "how": [
            "Vitesse et mémoire : avantage machine.",
            "Apprendre avec peu d'exemples : avantage humain.",
            "Sobriété énergétique : avantage humain, de très loin.",
            "Décider de ce qui compte : cela reste notre responsabilité.",
        ],
        "example": "Une IA peut résumer mille articles en une minute. "
                   "Choisir lequel mérite d'être cru, et pourquoi, reste une question humaine.",
        "today": "La vraie question n'est peut-être pas « qui est le plus intelligent ? », "
                 "mais « que voulons-nous faire ensemble ? ».",
        "neo": "Néo, adulte, travaille avec une IA tous les jours. Elle va plus vite que lui. "
               "Mais c'est lui qui décide de la question à poser.",
        "demo": "compare",
    },
]


def chapters_of(part_id):
    return [c for c in CHAPTERS if c["part"] == part_id]


def get_chapter(num):
    return next(c for c in CHAPTERS if c["num"] == num)
