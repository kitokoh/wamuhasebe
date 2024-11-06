import random
import json
import logging
import time
from alright import WhatsApp

class WhatsAppMessenger:
    def __init__(self, message_file='wamessage.json', contact_file='wacontact.json', log_file='whatsapp_log.txt'):
        """Initialisation du WhatsApp Messenger avec des fichiers JSON et la configuration du système de logs."""
        self.message_file = message_file
        self.contact_file = contact_file
        
        # Configurer les logs
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        # Charger les fichiers JSON
        self.messages = self._load_json(self.message_file)
        self.contacts = self._load_json(self.contact_file)

        # Initialiser l'objet WhatsApp
        self.messenger = WhatsApp()

        # Compteurs pour statistiques
        self.messages_envoyes = 0
        self.messages_echoues = 0

    def _load_json(self, file_path):
        """Méthode pour charger un fichier JSON."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"Le fichier {file_path} n'a pas été trouvé.")
            return None

    def send_personalized_message(self, contact):
        """Envoie un message personnalisé à un contact."""
        try:
            # Sélectionner un message aléatoire
            message = random.choice(self.messages)

            # Personnaliser le message avec le nom du contact
            message_text = message.get('text', '').replace("{name}", contact['name'])

            # Envoyer le texte
            if message_text:
                logging.info(f"Envoi du message texte à {contact['phone']}: {message_text}")
                self.messenger.send_message(contact['phone'], message_text)

            # Envoyer une image (si disponible)
            if message.get('image'):
                logging.info(f"Envoi de l'image à {contact['phone']}: {message['image']}")
                self.messenger.send_picture(contact['phone'], message['image'])

            # Envoyer un PDF (si disponible)
            if message.get('pdf'):
                logging.info(f"Envoi du fichier PDF à {contact['phone']}: {message['pdf']}")
                self.messenger.send_file(contact['phone'], message['pdf'])

            # Envoyer une vidéo (si disponible)
            if message.get('video'):
                logging.info(f"Envoi de la vidéo à {contact['phone']}: {message['video']}")
                self.messenger.send_video(contact['phone'], message['video'])

            return True  # Envoi réussi

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi à {contact['phone']}: {str(e)}")
            return False  # Envoi échoué

    def send_messages_to_all_contacts(self):
        """Envoie des messages à tous les contacts de manière séquentielle."""
        if not self.contacts or not self.messages:
            print("Erreur : Messages ou contacts non chargés.")
            return

        for contact in self.contacts:
            print(f"\n--- Envoi du message à {contact['name']} ({contact['phone']}) ---")

            # Envoi du message personnalisé et enregistrement du succès ou de l'échec
            if self.send_personalized_message(contact):
                print(f"Message envoyé à {contact['name']}")
                self.messages_envoyes += 1
            else:
                print(f"Échec de l'envoi à {contact['name']}")
                self.messages_echoues += 1

            # Pause pour éviter d'envoyer trop rapidement (optionnel)
            time.sleep(2)  # 2 secondes de pause entre chaque envoi

        # Résumé final des envois
        self._log_summary()

    def _log_summary(self):
        """Enregistre un résumé des envois."""
        print("\n--- Résumé des envois ---")
        print(f"Messages envoyés avec succès : {self.messages_envoyes}")
        print(f"Messages échoués : {self.messages_echoues}")

        logging.info(f"Messages envoyés avec succès : {self.messages_envoyes}")
        logging.info(f"Messages échoués : {self.messages_echoues}")

# Exemple d'utilisation
if __name__ == "__main__":
    whatsapp_messenger = WhatsAppMessenger()
    whatsapp_messenger.send_messages_to_all_contacts()
