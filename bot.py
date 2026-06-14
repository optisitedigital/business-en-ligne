import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Récupération automatique du token configuré dans Render
TOKEN = os.getenv("TELEGRAM_TOKEN", "8548951881:AAFdCTwbMnhN7Ugd8bxUSKZXFVYEniix97A")
bot = telebot.TeleBot(TOKEN)

# Fichier texte qui sert de mini base de données pour stocker les clients
DB_FILE = "utilisateurs.txt"

def sauvegarder_utilisateur(user_id):
    """Enregistre l'ID de l'utilisateur pour pouvoir lui envoyer des messages de masse plus tard"""
    if not os.path.exists(DB_FILE):
        open(DB_FILE, "w").close()
    
    with open(DB_FILE, "r") as f:
        ids = f.read().splitlines()
    
    if str(user_id) not in ids:
        with open(DB_FILE, "a") as f:
            f.write(f"{user_id}\n")

# --- TUNNEL DE VENTE PERSUASIF ---

@bot.message_handler(commands=['start'])
def commande_start(message):
    sauvegarder_utilisateur(message.chat.id)
    
    texte = (
        "👋 Bienvenue ! Je suis ton coach virtuel.\n\n"
        "En cette année 2026, le meilleur business en ligne pour générer des revenus depuis la RDC, "
        "c'est **la création de sites web professionnels boostée par l'Intelligence Artificielle**. 🚀\n\n"
        "Grâce à l'IA, tu n'as plus besoin de passer des mois à apprendre à coder. Tu peux concevoir des sites "
        "ultra-modernes pour des clients locaux (boutiques, PME, écoles) en quelques heures seulement."
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="🤔 Comment ça marche ? (Voir les étapes)", callback_data="voir_etapes"))
    bot.send_message(message.chat.id, texte, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "voir_etapes")
def etapes_business(call):
    texte = (
        "🎯 **Voici la feuille de route pour réussir en 2026 :**\n\n"
        "1️⃣ **La Maîtrise :** Apprendre à utiliser les bons outils IA pour générer des structures de site web en un clic.\n"
        "2️⃣ **Le Packaging :** Créer des offres adaptées au marché de Kinshasa et de la RDC.\n"
        "3️⃣ **La Chasse aux Clients :** Utiliser des stratégies simples pour décrocher tes premiers contrats payants.\n\n"
        "⚠️ *Mais attention... ce business demande du sérieux et un minimum d'engagement.*"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="⚡ Je veux me lancer !", callback_data="demande_investissement"))
    bot.edit_message_text(texte, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "demande_investissement")
def verifier_capital(call):
    texte = (
        "Pour activer ton coaching personnalisé, obtenir la formation vidéo complète et débloquer "
        "les outils, un micro-investissement est nécessaire.\n\n"
        "👉 **As-tu un budget d'au moins 5 000 FC disponible pour investir dans ton avenir aujourd'hui ?**"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="✅ Oui, j'ai les 5 000 FC !", callback_data="achat_formation"))
    markup.add(InlineKeyboardButton(text="❌ Non, pas pour l'instant", callback_data="refus_capital"))
    bot.edit_message_text(texte, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "achat_formation")
def finaliser_achat(call):
    texte = (
        "Excellent ! Tu as la bonne mentalité d'entrepreneur. ✨\n\n"
        "**Voici ce que tu vas recevoir immédiatement après ton paiement :**\n"
        "• 📚 La formation vidéo complète (Méthode IA 2026)\n"
        "• 🤖 L'accès à mon coaching pour trouver ton premier client cette semaine.\n\n"
        "📌 **Comment payer (5 000 FC) :**\n"
        "Effectue ton transfert Mobile Money au numéro : `08XXXXXXXX` (Indique ton numéro ici)\n\n"
        "Une fois le transfert fait, clique sur le bouton ci-dessous pour m'envoyer ta capture d'écran de confirmation. "
        "Je validerai ton accès immédiatement !"
    )
    
    markup = InlineKeyboardMarkup()
    # Pense à remplacer 'TonNomUtilisateurTelegram' par ton vrai @pseudo Telegram sans le @
    markup.add(InlineKeyboardButton(text="📨 Envoyer ma preuve de paiement", url="https://t.me/TonNomUtilisateurTelegram"))
    bot.edit_message_text(texte, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "refus_capital")
def reponse_refus(call):
    texte = (
        "Je comprends parfaitement. Créer un vrai business demande un minimum de ressources "
        "pour la connexion et les outils.\n\n"
        "Reste connecté sur ce bot, je partagerai régulièrement des conseils gratuits ici ! 💪"
    )
    bot.edit_message_text(texte, call.message.chat.id, call.message.message_id)

# --- SYSTEME DE MESSAGES DE MASSE (BROADCAST) ---

# RAPPEL : Remplace ceci par ton propre ID Telegram (obtenu via le bot @userinfobot)
ADMIN_ID = 123456789  

@bot.message_handler(commands=['broadcast'])
def distribuer_message(message):
    """Permet à l'admin d'envoyer un message à tous les utilisateurs. Exemple: /broadcast Promo spéciale !"""
    if message.chat.id != ADMIN_ID:
        bot.reply_to(message, "❌ Option réservée à l'administrateur.")
        return
    
    texte_a_envoyer = message.text.replace("/broadcast", "").strip()
    
    if not texte_a_envoyer:
        bot.reply_to(message, "⚠️ Utilisation : `/broadcast Ton message ici`")
        return
        
    if not os.path.exists(DB_FILE):
        bot.reply_to(message, "👥 Aucun utilisateur dans la base de données.")
        return
        
    with open(DB_FILE, "r") as f:
        utilisateurs = f.read().splitlines()
        
    succes = 0
    for u_id in utilisateurs:
        try:
            bot.send_message(int(u_id), texte_a_envoyer)
            succes += 1
        except Exception:
            pass  # Ignore si un utilisateur a bloqué le bot
            
    bot.reply_to(message, f"📢 Message envoyé avec succès à {succes} abonnés !")

if __name__ == "__main__":
    bot.infinity_polling()
