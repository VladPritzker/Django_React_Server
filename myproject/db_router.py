class DigitalOceanRouter:
    """
    A router to control all database operations on models for DigitalOcean.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read models go to DigitalOcean.
        """
        if model._meta.app_label == 'your_app_label':  # Replace with your app label if needed
            return 'digitalocean'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models go to DigitalOcean.
        """
        if model._meta.app_label == 'your_app_label':  # Replace with your app label if needed
            return 'digitalocean'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the DigitalOcean database is involved.
        """
        if obj1._meta.app_label == 'your_app_label' or obj2._meta.app_label == 'your_app_label':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the your_app_label app only appears in the 'digitalocean' database.
        """
        if app_label == 'your_app_label':  # Replace with your app label if needed
            return db == 'digitalocean'
        return None
