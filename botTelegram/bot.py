import os
import unicodedata
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Configuration du logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Ton token ici
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    logger.error("Aucun token trouvé. Définis la variable d'environnement TELEGRAM_TOKEN.")
    exit(1)

# Réponses personnalisées avec les vrais liens
reponses = {
    "conditions": "📋 Conditions générales pour étudier en Belgique :\n• Avoir un diplôme équivalent au CESS belge\n• Justifier de ressources financières suffisantes\n• Ne pas avoir dépassé l'âge limite (selon le niveau d'études)\n• Maîtriser la langue d'enseignement\n\nPlus d'infos : https://www.belgium.be/fr/enseignement/enseignement_superieur/etudier_en_belgique",
    "equivalence": "🟢 Pour faire ton equivalence du bac, commence par ici (Etape 1) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a74099308043aed3df637f7c3a9c",
    "inscription": "🏫 Pour demander une inscription dans une ecole belge (Etape 2) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080eca4cbcd809f0f3580",
    "visa": "� Pour introduire ta demande de visa (Etape 5) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080a192d5d49583b99bea",
    "documents": "📑 Documents nécessaires :\n• Passeport valide\n• Diplômes traduits et légalisés\n• Attestation d'équivalence\n• Preuve d'inscription\n• Justificatifs financiers\n• Attestation médicale\n• Casier judiciaire\n\nListe complète : https://dofi.ibz.be/fr/themes/etudier-en-belgique",
    "delais": "⏰ Délais importants :\n• Équivalence : avant le 15 juillet\n• Inscriptions universitaires : 30 avril (non-UE)\n• Demande de visa : 3 mois avant le départ\n• Campus Belgique : selon calendrier\n\nPlanification : https://www.studyinbelgium.be/fr/deadlines",
    "frais": "💰 Frais à prévoir :\n• Équivalence : 200€\n• Inscription universitaire : 835€/an (non-UE)\n• Visa : 180€\n• Campus Belgique : gratuit\n• Assurance : ~400€/an\n\nDétails : https://www.studyinbelgium.be/fr/costs",
    "hebergement": "� Options d'hébergement :\n• Résidences universitaires : 250-400€/mois\n• Kots privés : 300-600€/mois\n• Appartements : 400-800€/mois\n• Familles d'accueil : 450-650€/mois\n\nRecherche : https://www.kotplanet.be",
    "contact": "📞 Contacts utiles :\n• Ambassade de Belgique au Cameroun : +237 222 79 35 00\n• Service équivalences : equivalences@cfwb.be\n• Campus Belgique : info.cameroun@campusbelgique.be\n• Urgences en Belgique : 112\n\nPlus d'infos : https://cameroun.diplomatie.belgium.be",
    "prise en charge": "💶 Pour comprendre l'annexe 32 et le garant (Etape 3) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080a08d56d98c4133bc76",
    "campus belgique": "🎤 Pour l'entretien Campus Belgique (Etape 4) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a74099308055bc00d5f4449e8111",
    "conseils": "🧠 Conseils pratiques & erreurs a eviter :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080a29936f876d9c9551b",
    "guide": "📘 Voici le guide complet de la procedure d'inscription :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080f0b036defbaa39057f"
}

questions = {
    "conditions": ["condition", "conditions", "prerequis", "exigence", "critere", "eligibilite"],
    "equivalence": ["equivalence", "equivalance", "equivalant", "equivalent", "diplome reconnu", "equiv"],
    "inscription": ["inscription", "admission", "sinscrire", "dossier ecole", "ecole", "universite"],
    "visa": ["visa", "ambassade", "demande de visa", "tls contact", "frais visa"],
    "documents": ["document", "documents", "papier", "papiers", "piece", "pieces", "dossier", "fichier"],
    "delais": ["delai", "delais", "temps", "duree", "date limite", "echeance", "planning"],
    "frais": ["frais", "cout", "prix", "tarif", "montant", "argent", "finance"],
    "hebergement": ["hebergement", "logement", "chambre", "residence", "kot", "appartement"],
    "contact": ["contact", "aide", "support", "telephone", "email", "adresse"],
    "prise en charge": ["prise en charge", "annexe 32", "garant", "qui peut me prendre en charge", "garantie financiere", "membre de la famille"],
    "campus belgique": ["campus belgique", "entretien", "campus", "questions entretien", "test"],
    "conseils": ["conseil", "erreur", "astuce", "important", "a eviter"],
    "guide": ["guide", "toutes les etapes", "procedure complete", "comment faire"]
}  

def normaliser(texte: str) -> str:
    """Supprime les accents et met en minuscules"""
    # Décompose les caractères accentués et retire les diacritiques
    normalized = unicodedata.normalize('NFD', texte)
    stripped = normalized.encode('ascii', 'ignore').decode('utf-8')
    return stripped.lower().strip()

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Récupérer le message et s’assurer qu’il n’est pas None
    message = update.message or update.effective_message
    if not message:
        return
    await message.reply_text(
        "🎓 Bienvenue !\n\n"
        "Ce bot est un guide spécialisé uniquement pour la procédure d’obtention du visa étudiant pour la Belgique, destiné principalement aux Camerounais.\n\n"
        "📌 Il fonctionne par mot-clé. Voici les principaux mots-clés qu’il reconnaît :\n"
        "conditions, equivalence, inscription, visa, documents, delais, frais, hebergement, contact\n\n"
        "👉 Tu peux utiliser la commande /words à tout moment pour revoir cette liste.\n\n"
        "💡 Chaque mot-clé te renvoie :\n\n"
        "    un résumé clair,\n\n"
        "    les liens officiels (sites du gouvernement belge, des Hautes Écoles, etc.),\n\n"
        "    et parfois un PDF ou formulaire directement utile.\n\n"
        "⚠️ Ce n’est pas une intelligence artificielle. Il ne peut pas répondre à des questions ouvertes ni t’expliquer les démarches.\n"
        "Il est conçu pour te donner la bonne information depuis la bonne source, avec les liens pour vérifier toi-même ou aller plus loin.\n\n"
        "✉️ Pour toute suggestion, remarque ou amélioration, utilise la commande /suggest.\n\n"
        "Bonne chance dans tes démarches, et que la force soit avec toi �✨"
    )
    logger.info("Utilisateur a appelé /start")

# Commande /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.effective_message
    if not message:
        return
    texte = (
        "🤖 Commandes disponibles :\n"
        "/start – Présentation du bot\n"
        "/help – Affiche cette aide\n"
        "/guide – Lien vers le guide complet\n"
        "/words – Liste des mots-clés reconnus\n"
        "/suggest – Envoyez une suggestion\n\n"
        "Tu peux aussi envoyer directement un mot-clé pour obtenir une réponse rapide."
    )
    await message.reply_text(texte)
    logger.info("Utilisateur appelé /help")

# Commande /guide
async def guide_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Renvoie le guide complet"""
    message = update.message or update.effective_message
    if not message:
        return
    await message.reply_text(reponses["guide"])
    logger.info("Utilisateur a appelé /guide")

# Commande /words
async def words_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Liste tous les mots-clés et synonymes reconnus par le bot"""
    message = update.message or update.effective_message
    if not message:
        return
    lines = ["Mots reconnus par le bot :"]
    for cle, exprs in questions.items():
        lines.append(f"- {cle} : {', '.join(exprs)}")
    await message.reply_text("\n".join(lines))
    logger.info("Utilisateur a appelé /words")

# Commande /suggest
async def suggest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Invite l’utilisateur à envoyer directement sa suggestion par Telegram"""
    message = update.message or update.effective_message
    if not message:
        return
    await message.reply_text(
        "Pour améliorer ce bot, envoie-moi un message sur Telegram au +32 489 13 44 40 avec ta suggestion. Je te répondrai dès que possible !"
    )
    logger.info("Utilisateur a appelé /suggest")

# Gérer les messages
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Récupérer le message et s’assurer qu’il n’est pas None
    message = update.message or update.effective_message
    if not message or not message.text:
        return
    texte = normaliser(message.text)
    logger.info(f"Reçu message utilisateur : {texte}")
    for cle, expressions in questions.items():
        for mot in expressions:
            if mot in texte:
                logger.info(f"Répondre avec la clé : {cle}")
                await message.reply_text(reponses[cle])
                return
    await message.reply_text(
        "Désolé, je n’ai pas compris 😅\n"
        "Essaie de poser ta question autrement, en utilisant l'un des mots clés que je reconnais :\n"
        "équivalence, admission, visa, prise en charge, campus belgique, conseils."
        
    )

#NE PAS OUBLIER DE REVOIR LE LANCEMENT 
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("guide", guide_command))
    app.add_handler(CommandHandler("words", words_command))
    app.add_handler(CommandHandler("suggest", suggest_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    logger.info("✅ Bot en ligne… Attente des messages")
    # Drop any pending updates to avoid conflicts with other running instances
    app.run_polling(drop_pending_updates=True)
