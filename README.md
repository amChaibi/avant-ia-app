# Avant l'IA, il y avait nous — application interactive

Application Streamlit compagnon du livre d'Amine Chaïbi : 15 chapitres, chacun avec
le principe (nature → idée → fonctionnement), un exemple concret et une expérience à manipuler.

## Lancer

    pip install -r requirements.txt
    streamlit run app.py

## Structure

- `app.py` — mise en page, style épuré, navigation (accueil + chapitres, lien direct `?chapitre=4`)
- `content.py` — tous les textes : modifiez-les ici sans toucher au code
- `demos.py` — les 15 démonstrations interactives
- `.streamlit/config.toml` — thème clair (bleu #0071E3)

## Mettre en ligne gratuitement

Déposez le dossier sur GitHub puis déployez-le sur Streamlit Community Cloud (share.streamlit.io).
