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
    "equivalence": "🟢 Pour faire ton equivalence du bac, commence par ici (Etape 1) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a74099308043aed3df637f7c3a9c",
    "inscription": "🏫 Pour demander une inscription dans une ecole belge (Etape 2) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080eca4cbcd809f0f3580",
    "prise en charge": "� Pour comprendre l'annexe 32 et le garant (Etape 3) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080a08d56d98c4133bc76",
    "campus belgique": "🎤 Pour l'entretien Campus Belgique (Etape 4) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a74099308055bc00d5f4449e8111",
    "visa": "📄 Pour introduire ta demande de visa (Etape 5) :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080a192d5d49583b99bea",
    "conseils": "🧠 Conseils pratiques & erreurs a eviter :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080a29936f876d9c9551b",
    "guide": "📘 Voici le guide complet de la procedure d'inscription :\nhttps://www.notion.so/Visa-Belgique-proc-dure-compl-te-22f0a740993080f0b036defbaa39057f"
}

questions = {
    "equivalence": ["equivalence", "equivalance", "equivalant", "equivalent", "diplome reconnu", "equiv", "condition", "conditions", "prerequis", "exigence", "critere", "eligibilite", "document", "documents", "papier", "papiers", "piece", "pieces", "dossier", "fichier"],
    "inscription": ["inscription", "admission", "sinscrire", "dossier ecole", "ecole", "universite", "delai", "delais", "temps", "duree", "date limite", "echeance", "planning", "frais", "cout", "prix", "tarif", "montant", "argent", "finance"],
    "prise en charge": ["prise en charge", "annexe 32", "garant", "qui peut me prendre en charge", "garantie financiere", "membre de la famille", "hebergement", "logement", "chambre", "residence", "kot", "appartement"],
    "campus belgique": ["campus belgique", "entretien", "campus", "questions entretien", "test", "contact", "aide", "support", "telephone", "email", "adresse"],
    "visa": ["visa", "ambassade", "demande de visa", "tls contact", "frais visa"],
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
    # Récupérer le message et s'assurer qu'il n'est pas None
    message = update.message or update.effective_message
    if not message:
        return
    await message.reply_text(
        "🎓 Bienvenue sur le guide étudiant pour la Belgique !\n\n"
        "Ce bot t'aide avec la procédure d'obtention du **visa étudiant belge**.\n\n"
        "📌 Il fonctionne **par mot-clé** : tape un mot-clé pour obtenir un lien précis vers une étape ou une explication importante.\n"
        "Chaque mot-clé renvoie vers une page Notion contenant **les infos, documents, liens officiels et instructions** utiles.\n\n"
        "� Exemples de mots-clés reconnus :\n"
        "- **equivalence** – obtenir l'équivalence du bac\n"
        "- **inscription** – s'inscrire dans une école/université\n"
        "- **prise en charge** – comprendre l'annexe 32 (garant)\n"
        "- **campus belgique** – réussir l'entretien Campus Belgique\n"
        "- **visa** – préparer la demande de visa\n"
        "- **conseils** – astuces, erreurs à éviter\n"
        "- **guide** – procédure complète, étape par étape\n\n"
        "📖 Tape **/words** pour voir tous les mots-clés reconnus.\n\n"
        "⚠️ Ce bot **n'est pas une intelligence artificielle**. Il ne peut pas t'expliquer, juste t'envoyer **la bonne source officielle** avec les bons documents.\n\n"
        "✉️ Suggestions ? Utilise **/suggest**.\n\n"
        "Bonne chance dans tes démarches. Que la force soit avec toi 💪✨"
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
    """Invite l'utilisateur à envoyer directement sa suggestion par Telegram"""
    message = update.message or update.effective_message
    if not message:
        return
    await message.reply_text(
        "Pour améliorer ce bot, envoie-moi un message sur Telegram au +32 489 13 44 40 avec ta suggestion. Je te répondrai dès que possible !"
    )
    logger.info("Utilisateur a appelé /suggest")

# Gérer les messages
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Récupérer le message et s'assurer qu'il n'est pas None
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
        "Désolé, je n'ai pas compris 😅\n"
        "Essaie de poser ta question autrement, en utilisant l'un des mots clés que je reconnais :\n"
        "équivalence, inscription, visa, prise en charge, campus belgique, conseils."
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
