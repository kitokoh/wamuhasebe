import random
import json
import logging
import time
from alright import WhatsApp

class WhatsAppMessenger:
    def __init__(self, message_file='wamessage.json', contact_file='wacontact.json', log_file='whatsapp_log.txt'):
        """Initialisation du WhatsApp Messenger avec des fichiers JSON et configuration des logs."""
        self.message_file = message_file
        self.contact_file = contact_file

        # Configurer les logs pour inclure DEBUG pour un maximum de détails
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,  # DEBUG pour capturer tous les détails
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Initialisation de WhatsApp Messenger")

        # Charger les fichiers JSON
        self.messages = self._load_json(self.message_file, "messages")
        self.contacts = self._load_json(self.contact_file, "contacts")

        # Initialiser l'objet WhatsApp
        self.messenger = WhatsApp()

        # Compteurs pour les statistiques
        self.messages_envoyes = 0
        self.messages_echoues = 0

    def _load_json(self, file_path, file_type):
        """Méthode pour charger un fichier JSON."""
        logging.debug(f"Tentative de chargement du fichier {file_type} depuis {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:  # Encodage UTF-8
                data = json.load(file)
                logging.info(f"Fichier {file_type} chargé avec succès : {len(data)} entrées trouvées.")
                return data
        except FileNotFoundError:
            logging.error(f"Le fichier {file_path} n'a pas été trouvé.")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Erreur de décodage JSON dans {file_path} : {str(e)}")
            return None

    def send_personalized_message(self, contact):
        """Envoie un message personnalisé à un contact."""
        try:
            logging.debug(f"Préparation de l'envoi pour le contact : {contact}")
            # Vérifier les informations du contact
            if not contact.get('phone') or not contact.get('MÜKELLEF'):
                logging.error(f"Données de contact invalides : {contact}")
                return False

            # Sélectionner un message aléatoire
            if not self.messages:
                logging.error("Aucun message disponible pour l'envoi.")
                return False

            message = random.choice(self.messages)
            message_text = message.get('text', '')
            
            # Remplacer les placeholders dans le message
            message_text = self._replace_placeholders(message_text, contact)

            logging.debug(f"Message sélectionné : {message_text}")

            # Envoyer le message texte
            if message_text:
                logging.info(f"Envoi du message texte à {contact['phone']} : {message_text}")
                self.messenger.send_direct_message(contact['phone'], message_text)

            # Envoyer une image (si disponible)
            if message.get('image'):
                logging.info(f"Envoi de l'image à {contact['phone']} : {message['image']}")
                self.messenger.send_picture(contact['phone'], message['image'])

            # Envoyer un PDF (si disponible)
            if message.get('pdf'):
                logging.info(f"Envoi du fichier PDF à {contact['phone']} : {message['pdf']}")
                self.messenger.send_file(contact['phone'], message['pdf'])

            # Envoyer une vidéo (si disponible)
            if message.get('video'):
                logging.info(f"Envoi de la vidéo à {contact['phone']} : {message['video']}")
                self.messenger.send_video(contact['phone'], message['video'])

            return True  # Envoi réussi

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi à {contact['phone']} : {str(e)}")
            return False  # Envoi échoué

    def _replace_placeholders(self, message_text, contact):
        """Remplace les placeholders dans le message texte en fonction des données du contact."""
        placeholders = {
            "{SIRA}": contact.get('SIRA', ''),
            "{MÜKELLEF}": contact.get('MÜKELLEF', ''),
            "{KDV}": self._format_money(contact.get('KDV', '')),  # Formater en argent
            "{STOPAJ}": self._format_money(contact.get('STOPAJ', '')),  # Formater en argent
            "{KDV 2}": self._format_money(contact.get('KDV 2', '')),  # Formater en argent
            "{GEÇİCİ VERGİ}": self._format_money(contact.get('GEÇİCİ VERGİ', '')),  # Formater en argent
            "{GELİR V.}": self._format_money(contact.get('GELİR V.', '')),  # Formater en argent
            "{MTV}": self._format_money(contact.get('MTV', '')),  # Formater en argent
            "{T. CEZASI}": self._format_money(contact.get('T. CEZASI', '')),  # Formater en argent
            "{VERGİ YAP.}": self._format_money(contact.get('VERGİ YAP.', '')),  # Formater en argent
            "{SGK}": self._format_money(contact.get('SGK', '')),  # Formater en argent
            "{BAĞ-KUR}": self._format_money(contact.get('BAĞ-KUR', '')),  # Formater en argent
            "{SGK YAPILANDIRMA}": self._format_money(contact.get('SGK YAPILANDIRMA', '')),  # Formater en argent
            "{SMM KDV Sİ}": self._format_money(contact.get('SMM KDV Sİ', '')),  # Formater en argent
            "{E DÖNÜŞÜM}": self._format_money(contact.get('E DÖNÜŞÜM', '')),  # Formater en argent
            "{DEFTER TASTİK}": self._format_money(contact.get('DEFTER TASTİK', '')),  # Formater en argent
            "{E. KALAN TUTAR}": self._format_money(contact.get('E. KALAN TUTAR', '')),  # Formater en argent
            "{MUHASEBE ÜC.}": self._format_money(contact.get('MUHASEBE ÜC.', '')),  # Formater en argent
            "{TOPLAM}": self._format_money(contact.get('TOPLAM', '')),  # Formater en argent
            "{FAZLA ALINAN}": self._format_money(contact.get('FAZLA ALINAN', '')),  # Formater en argent
            "{KALAN}": self._format_money(contact.get('KALAN', '')),  # Formater en argent
            "{SON ÖDEME}": contact.get('SON ÖDEME', ''),
            "{İBAN}": contact.get('İBAN', ''),
        }

        # Remplacer les placeholders dans le message
        for placeholder, value in placeholders.items():
            if value:  # Si la valeur n'est pas vide
                message_text = message_text.replace(placeholder, str(value))
            else:  # Si la valeur est vide, supprimer la ligne correspondante
                message_text = self._remove_line_with_placeholder(message_text, placeholder)

        return message_text
    def _format_money(self, amount):
        """Formate un montant numérique en format monétaire (ex: 12823.0 -> '12 823,00')."""
        try:
            # Convertir en float pour s'assurer que c'est un nombre
            amount = float(amount)
            # Formater avec des espaces comme séparateurs de milliers et une virgule pour les décimales
            formatted_amount = "{:,.2f}".format(amount).replace(",", " ").replace(".", ",")
            return formatted_amount
        except (ValueError, TypeError):
            logging.error(f"Erreur de formatage du montant : {amount}")
            return str(amount)  # Retourner la valeur originale en cas d'erreur
        


    def _remove_line_with_placeholder(self, message_text, placeholder):
        """Supprime la ligne contenant le placeholder si la valeur est vide."""
        lines = message_text.split('\n')
        lines = [line for line in lines if placeholder not in line]
        return '\n'.join(lines)

    def send_messages_to_all_contacts(self):
        """Envoie des messages à tous les contacts de manière séquentielle."""
        logging.info("Début de l'envoi des messages à tous les contacts.")

        if not self.contacts or not self.messages:
            logging.error("Les messages ou contacts ne sont pas chargés.")
            return

        for index, contact in enumerate(self.contacts, start=1):
            logging.debug(f"Traitement du contact {index}/{len(self.contacts)} : {contact}")

            # Envoi du message personnalisé et enregistrement du succès ou de l'échec
            if self.send_personalized_message(contact):
                logging.info(f"Message envoyé avec succès à {contact['MÜKELLEF']} ({contact['phone']}).")
                self.messages_envoyes += 1
            else:
                logging.warning(f"Échec de l'envoi à {contact['MÜKELLEF']} ({contact['phone']}).")
                self.messages_echoues += 1

            # Pause pour éviter d'envoyer trop rapidement (optionnel)
            logging.debug(f"Pause après l'envoi au contact {contact['MÜKELLEF']}.")
            time.sleep(2)  # 2 secondes de pause entre chaque envoi

        # Résumé final des envois
        self._log_summary()

    def _log_summary(self):
        """Enregistre un résumé des envois."""
        logging.info("Résumé des envois :")
        logging.info(f"Messages envoyés avec succès : {self.messages_envoyes}")
        logging.info(f"Messages échoués : {self.messages_echoues}")

        print("\n--- Résumé des envois ---")
        print(f"Messages envoyés avec succès : {self.messages_envoyes}")
        print(f"Messages échoués : {self.messages_echoues}")

# Exemple d'utilisation
if __name__ == "__main__":
    whatsapp_messenger = WhatsAppMessenger()
    whatsapp_messenger.send_messages_to_all_contacts()

