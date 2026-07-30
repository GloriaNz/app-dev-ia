from models import db, User, Module, Lesson

def seed_database():
    """Initialise la base de données avec la structure complète de la formation Développeur IA & Data."""
    # Vérification si les modules existent déjà
    if Module.query.first() is not None:
        print("[SEED] La base de données contient déjà des modules. Seeding ignoré.")
        return

    print("[SEED] Début de l'initialisation du programme 'Développeur IA & Data'...")

    # --- MODULE 1 (GRATUIT / FREEMIUM) ---
    m1 = Module(
        title="Module 1 : Développer une application web",
        description="Bases fondamentales du web dev moderne (Python, Flask, APIs REST & UI Responsive) pour créer l'interface utilisateur de vos modèles d'IA.",
        order=1,
        is_free=True,
        icon="fa-laptop-code"
    )

    l1_1 = Lesson(
        title="Leçon 1.1 : Architecture d'une application Web Full-Stack avec Flask",
        summary="Comprendre le fonctionnement d'une application Flask, le routage HTTP et la séparation entre Logique Métier et Rendu HTML.",
        content_html="""
        <h3>Bienvenue dans le Module 1 !</h3>
        <p>Dans cette leçon d'introduction, nous allons poser les bases d'une application Web Python moderne destinée à servir de frontend à des algorithmes d'Intelligence Artificielle.</p>
        
        <h4>1. Architecture d'une application Flask</h4>
        <p>Flask est un micro-framework léger et flexible. Il gère le routage des requêtes HTTP (GET, POST, PUT, DELETE) et permet d'associer des vues Python à des routes d'URL.</p>
        
        <pre><code class="language-python">
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title="Développeur IA & Data")

if __name__ == '__main__':
    app.run(debug=True)
        </code></pre>

        <h4>2. Points clés à retenir :</h4>
        <ul>
            <li><strong>WSGI Server :</strong> Interface entre le serveur HTTP et Python.</li>
            <li><strong>Jinja2 :</strong> Moteur de templates pour générer du HTML dynamique côté serveur.</li>
            <li><strong>Stateless REST APIs :</strong> Communication en JSON entre le client (JavaScript) et les endpoints d'inférence IA.</li>
        </ul>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module1_lesson1.pdf",
        order=1,
        duration_minutes=20,
        module=m1
    )

    l1_2 = Lesson(
        title="Leçon 1.2 : Conception de Formulaires & Upload de Fichiers pour les Données d'Entrée IA",
        summary="Sécuriser la réception de fichiers (images, CSV, audio) envoyés par l'utilisateur pour traitement par des modèles d'IA.",
        content_html="""
        <h3>Réceptionner les données utilisateur</h3>
        <p>Pour qu'un modèle d'IA (vision par ordinateur, traitement du langage ou prédiction tabulaire) fonctionne, l'application web doit être capable d'ingérer et valider des fichiers envoyés par l'utilisateur.</p>

        <pre><code class="language-python">
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        </code></pre>
        <p>Toujours utiliser <code>secure_filename()</code> pour éviter les failles d'injection de chemins (Path Traversal Attacks).</p>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module1_lesson2.pdf",
        order=2,
        duration_minutes=25,
        module=m1
    )

    l1_3 = Lesson(
        title="Leçon 1.3 : Intégration d'une API REST pour la Prédiction en Temps Réel",
        summary="Consommer et exposer des endpoints API JSON légers pour les prédictions d'IA interactives.",
        content_html="""
        <h3>Exposer des prédictions via une API JSON</h3>
        <p>Nous abordons ici la création d'endpoints <code>/api/predict</code> acceptant du JSON et renvoyant le résultat du modèle sous forme de payload structuré.</p>
        <pre><code class="language-python">
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Simulation d'inférence
    score = 0.95
    return jsonify({"success": True, "confidence": score, "label": "Positive"})
        </code></pre>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module1_lesson3.pdf",
        order=3,
        duration_minutes=30,
        module=m1
    )


    # --- MODULE 2 (PAYANT) ---
    m2 = Module(
        title="Module 2 : Collecter, stocker et préparer les données d'un projet d'IA",
        description="Pipeline Data Engineering complète : Scraping éthique, nettoyage Pandas/Polars, stockage SQL/NoSQL & Vector Databases (ChromaDB/FAISS).",
        order=2,
        is_free=False,
        icon="fa-database"
    )

    l2_1 = Lesson(
        title="Leçon 2.1 : Data Scraping & Ingestion automatisée avec Python",
        summary="Extraire et structurer des données brutes depuis le Web avec BeautifulSoup, Playwright et APIs tierces.",
        content_html="""
        <h3>Ingestion de données brutes</h3>
        <p>Le succès d'un projet d'IA dépend à 80% de la qualité des données collectées. Nous explorons les techniques de Web Scraping distribué et la gestion des proxies.</p>
        <pre><code class="language-python">
import requests
from bs4 import BeautifulSoup

url = "https://example.com/dataset"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
        </code></pre>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module2_lesson1.pdf",
        order=1,
        duration_minutes=35,
        module=m2
    )

    l2_2 = Lesson(
        title="Leçon 2.2 : Preprocessing, Feature Engineering & Normalisation avec Pandas",
        summary="Traiter les valeurs manquantes, encoder les variables catégorielles et créer des embeddings vectoriels.",
        content_html="""
        <h3>Nettoyage et Transformation de Datasets</h3>
        <p>Apprenez à nettoyer vos DataFrames Pandas, appliquer des transformations Scaling (StandardScaler, MinMaxScaler) et gérer la fuite de données (Data Leakage).</p>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module2_lesson2.pdf",
        order=2,
        duration_minutes=40,
        module=m2
    )

    l2_3 = Lesson(
        title="Leçon 2.3 : Stockage Vectoriel & Vector Databases (ChromaDB / FAISS) pour la RAG",
        summary="Indexer des documents volumineux sous forme de données vectorielles pour créer des systèmes de Retrieval-Augmented Generation (RAG).",
        content_html="""
        <h3>Vector Databases & Embeddings</h3>
        <p>Découvrez comment convertir vos textes en vecteurs de haute dimension et les stocker dans ChromaDB pour effectuer des recherches de proximité cosinus instantanées.</p>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module2_lesson3.pdf",
        order=3,
        duration_minutes=45,
        module=m2
    )


    # --- MODULE 3 (PAYANT) ---
    m3 = Module(
        title="Module 3 : Entraîner, adapter et évaluer des modèles d’IA Open Source",
        description="Fine-tuning de LLM (Mistral/Llama 3 avec QLoRA), Transformers HuggingFace, PyTorch et métriques d'évaluation poussées.",
        order=3,
        is_free=False,
        icon="fa-brain"
    )

    l3_1 = Lesson(
        title="Leçon 3.1 : Fine-Tuning de LLMs Open-Source avec LoRA et QLoRA",
        summary="Adapter un modèle de langage (Llama 3, Mistral 7B) sur vos données métier sur une seule carte GPU grâce à la quantification 4-bit.",
        content_html="""
        <h3>Fine-Tuning efficace avec QLoRA</h3>
        <p>Apprenez à charger un modèle en précision 4-bit avec <code>bitsandbytes</code> et appliquer des adaptateurs LoRA avec la bibliothèque <code>PEFT</code> de HuggingFace.</p>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module3_lesson1.pdf",
        order=1,
        duration_minutes=50,
        module=m3
    )

    l3_2 = Lesson(
        title="Leçon 3.2 : Fine-Tuning de Modèles de Computer Vision (YOLOv8 / ResNet)",
        summary="Entraîner un modèle de détection d'objets ou de classification d'images personnalisé pour la production.",
        content_html="""
        <h3>Vision par Ordinateur Métier</h3>
        <p>Configuration du pipeline d'entraînement YOLOv8 sur un dataset annoté et exportation vers ONNX pour des inférences ultra-rapides.</p>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module3_lesson2.pdf",
        order=2,
        duration_minutes=45,
        module=m3
    )

    l3_3 = Lesson(
        title="Leçon 3.3 : Évaluation, Métriques & Benchmark d'IA (ROUGE, BLEU, RAGAS)",
        summary="Valider scientifiquement la qualité, l'hallucination et les performances temps de réponse de vos modèles.",
        content_html="""
        <h3>Évaluation Rigoureuse des Modèles</h3>
        <p>Mise en place de tests de régression automatisés pour évaluer la fidélité des réponses et limiter la dérive (Data Drift / Concept Drift).</p>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module3_lesson3.pdf",
        order=3,
        duration_minutes=40,
        module=m3
    )


    # --- MODULE 4 (PAYANT) ---
    m4 = Module(
        title="Module 4 : Industrialiser le déploiement de l'IA et piloter le projet",
        description="MLOps moderne : Containerisation Docker, Kubernetes, CI/CD GitHub Actions, Monitoring (Prometheus/Grafana) et gestion du cycle de vie IA.",
        order=4,
        is_free=False,
        icon="fa-rocket"
    )

    l4_1 = Lesson(
        title="Leçon 4.1 : Containerisation de Modèles IA avec Docker & Docker Compose",
        summary="Packager votre application web Flask, la base vectorielle et le modèle d'inférence dans des conteneurs isolés.",
        content_html="""
        <h3>Packaging MLOps avec Docker</h3>
        <p>Optimisation des images Docker pour Python avec support GPU (NVIDIA CUDA Container Toolkit) et builds multi-stages.</p>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module4_lesson1.pdf",
        order=1,
        duration_minutes=45,
        module=m4
    )

    l4_2 = Lesson(
        title="Leçon 4.2 : Orchestration Cloud, Serverless & Scaling d'Inférence IA",
        summary="Déployer sur AWS/GCP (ECS, Cloud Run, SageMaker) avec auto-scaling selon la charge de requêtes.",
        content_html="""
        <h3>Déploiement Cloud à Forte Échelle</h3>
        <p>Mise en place de vLLM ou TGI (Text Generation Inference) pour servir des milliers de requêtes concourantes à faible latence.</p>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module4_lesson2.pdf",
        order=2,
        duration_minutes=50,
        module=m4
    )

    l4_3 = Lesson(
        title="Leçon 4.3 : Monitoring MLOps, Tracking des Coûts API & Gouvernance IA",
        summary="Superviser les métriques de dérive, les coûts d'infrastructure et le respect du RGPD & de l'EU AI Act.",
        content_html="""
        <h3>Gouvernance et Observabilité IA</h3>
        <p>Mettre en place LangSmith / MLflow pour tracer chaque appel d'inférence et garder un contrôle total sur les coûts et l'éthique.</p>
        """,
        video_url="https://www.youtube.com/embed/Z1RJmh_Ouv0",
        pdf_filename="support_module4_lesson3.pdf",
        order=3,
        duration_minutes=40,
        module=m4
    )

    # Ajout des objets à la session DB
    db.session.add_all([m1, m2, m3, m4])
    db.session.commit()

    # Création d'un utilisateur admin par défaut
    admin_user = User(
        username="admin",
        email="admin@formation-ia.fr",
        role="admin",
        has_premium_access=True
    )
    admin_user.set_password("Admin2026!")

    # Création d'un étudiant démonstration par défaut
    student_user = User(
        username="etudiant_demo",
        email="etudiant@formation-ia.fr",
        role="student",
        has_premium_access=False
    )
    student_user.set_password("Etudiant2026!")

    db.session.add(admin_user)
    db.session.add(student_user)
    db.session.commit()

    print("[SEED] Seeding terminé avec succès !")
    print("  -> Compte Admin : admin@formation-ia.fr / Admin2026!")
    print("  -> Compte Étudiant Freemium : etudiant@formation-ia.fr / Etudiant2026!")
