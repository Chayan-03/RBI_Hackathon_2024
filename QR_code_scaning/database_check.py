import django
from django.conf import settings
from django.db import models

# Configure Django settings (simplified for example)
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    INSTALLED_APPS=[
        'myapp',
    ],
)

django.setup()

# Define your models (simplified for example)
class Account(models.Model):
    account_number = models.CharField(max_length=255)
    upi_id = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

def check_database(info):
    if Account.objects.filter(account_number=info).exists() or \
       Account.objects.filter(upi_id=info).exists() or \
       Account.objects.filter(phone_number=info).exists():
        return True
    return False

# Example usage
if __name__ == "__main__":
    info = 'some_account_number_or_upi_id_or_phone_number'
    result = check_database(info)
    print(result)
