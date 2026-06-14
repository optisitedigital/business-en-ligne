import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- CONFIGURATION DU MINI-SERVEUR GRATUIT POUR RENDER ---
class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot Optisite Digital en cours d'execution...")

def run_web_server():
    # Render va trouver le port automatiquement grâce à cette ligne
    port = int(os.getenv("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleServer)
    print(f"Mini-serveur active sur le port {port}")
    server.serve_forever()

# --- TON CODE TELEGRAM ---
TOKEN = "8548951881:AAFDr7sumXgUPwOmz5htqEU8nHSN7jmMhzM"
bot = telebot.TeleBot(TOKEN)

DB_FILE = "utilisateurs.txt"

def sauvegarder_utilisateur(user_id):
    """Enregistre chaque visiteur pour pouvoir lui envoyer des offres plus tard"""
    if not os.path.exists(DB_FILE):
        open(DB_FILE, "w").close()
    
    with open(DB_FILE, "r") as f:
        ids = f.read().splitlines()
    
    if str(user_id) not in ids:
        with open(DB_FILE, "a") as f:
            f.write(f"{user_id}\n")

# --- TUNNEL DE VENTE AVEC COPYWRITING ---

@bot.message_handler(commands=['start'])
def commande_start(message):
    sauvegarder_utilisateur(message.chat.id)
    
    texte = (
        "👋 **Salut à toi, futur entrepreneur du digital !**\n\n"
        "Laisse-moi te poser une question honnête...\n"
        "Combien de temps vas-tu encore passer à chercher des opportunités en ligne qui ne rapportent rien ?\n\n"
        "En cette année 2026, il y a un secret que les experts cachent : **La création de sites web professionnels boostée par l'Intelligence Artificielle**. 🚀\n\n"
        "C'est le business ultime en RDC. Pourquoi ? Parce que grâce à l'IA, **tu n'as plus besoin de savoir coder**, ni de passer 5 ans à l'université. Tu peux concevoir des sites magiques pour des entreprises, des boutiques ou des écoles à Kinshasa en moins de 2 heures et les revendre à prix d'or ! 💸"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="🎯 Découvrir la méthode exacte (3 étapes)", callback_data="voir_etapes"))
    bot.send_message(message.chat.id, texte, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "voir_etapes")
def etapes_business(call):
    texte = (
        "🔥 **Voici le plan secret pour générer tes premiers revenus ce mois-ci :**\n\n"
        "1️⃣ **L'Arme Secrète (L'IA) :** Je te montre comment utiliser les meilleurs outils IA pour générer le design d'un site complet en un seul clic.\n"
        "2️⃣ **L'Offre Irrésistible :** Comment packager ton service pour que n'importe quelle boutique ou PME locale te supplie de travailler avec toi.\n"
        "3️⃣ **Le Cash Flow :** Découvre mes scripts exacts de copier-coller pour démarcher et décrocher ton premier client payant en moins de 7 jours.\n\n"
        "⚠️ *Attention : Ce plan n'est pas pour les paresseux. C'est uniquement pour ceux qui sont prêts à appliquer une méthode qui marche déjà.*"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="⚡ Oui, je veux appliquer cette méthode !", callback_data="demande_investissement"))
    bot.edit_message_text(texte, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "demande_investissement")
def verifier_capital(call):
    texte = (
        "Pour t'éviter de perdre des mois à faire des erreurs, j'ai tout résumé dans mon **Guide Pratique de 9 pages** "
        "axé à 100% sur la réalité du marché congolais. 📚\n\n"
        "Ce guide est ton raccourci direct vers l'indépendance financière.\n\n"
        "👉 **As-tu un budget dérisoire d'au moins 5 000 FC prêt à être investi pour transformer tes compétences aujourd'hui ?**"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="✅ Oui, j'ai les 5 000 FC ! Je fonce !", callback_data="voir_guide"))
    markup.add(InlineKeyboardButton(text="❌ Non, je préfère attendre", callback_data="refus_capital"))
    bot.edit_message_text(texte, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "voir_guide")
def aller_vers_boutique(call):
    texte = (
        "🚀 **Félicitations ! Tu as la mentalité des 1% qui réussissent.**\n\n"
        "Pour récupérer ton exemplaire du guide et commencer à te lancer dès aujourd'hui, tu as **deux options ultra-simples** :\n\n"
        "➡️ **Option 1 :** Commande directement sur ma boutique en ligne sécurisée par Mobile Money (livraison instantanée).\n\n"
        "➡️ **Option 2 :** Contacte-moi directement sur WhatsApp pour faire ton transfert manuellement et recevoir ton accès."
    )
    
    markup = InlineKeyboardMarkup()
    # Option 1 : Ton lien exact de boutique Chariow Shop
    markup.add(InlineKeyboardButton(text="🛒 Option 1 : Acheter sur la Boutique en ligne", url="https://zbgbgtgc.mychariow.shop/guide-creer-site-web"))
    # Option 2 : Lien vers ton WhatsApp (Pense à remplacer les XXXXXXXXX par ton numéro)
    markup.add(InlineKeyboardButton(text="💬 Option 2 : Acheter direct par WhatsApp", url="https://wa.me/243977092549"))
    
    bot.edit_message_text(texte, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "refus_capital")
def reponse_refus(call):
    texte = (
        "Je comprends. Sache que pour gagner de l'argent, il faut accepter d'investir un minimum sur soi-même. "
        "Le prix d'un simple forfait internet peut lancer ta carrière.\n\n"
        "Reste ici, je partagerai des conseils gratuits de temps en temps. Bon succès ! 💪"
    )
    bot.edit_message_text(texte, call.message.chat.id, call.message.message_id)

# --- SYSTEME DE MESSAGES DE MASSE (BROADCAST) ---

ADMIN_ID = 123456789  

@bot.message_handler(commands=['broadcast'])
def distribuer_message(message):
    if message.chat.id != ADMIN_ID:
        return
    texte_a_envoyer = message.text.replace("/broadcast", "").strip()
    if not texte_a_envoyer or not os.path.exists(DB_FILE):
        return
    with open(DB_FILE, "r") as f:
        utilisateurs = f.read().splitlines()
    for u_id in utilisateurs:
        try: bot.send_message(int(u_id), texte_a_envoyer)
        except: pass

if __name__ == "__main__":
    # On lance le serveur web en arrière-plan pour valider le port Render gratuitement
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    # On lance le bot Telegram
    print("Le robot Optisite Digital survolté est prêt...")
    bot.infinity_polling()
