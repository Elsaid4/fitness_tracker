from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    """Crea superuser e utente di prova dopo le migrazioni"""
    
    # Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='coach'
        )
        print("✅ Superuser 'admin' creato")
    
    # Utente di prova
    if not User.objects.filter(username='Elsaid', email='test@example.com').exists():
        User.objects.create_user(
            username='Elsaid',
            email='test@example.com',
            password='Firenze1',
            role='user'
        )
        print("✅ Utente di prova 'Elsaid' creato")