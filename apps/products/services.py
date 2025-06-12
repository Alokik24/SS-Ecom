from apps.users.models import User
from .models import Product

def assign_vendor(validated_data: dict, user: User):
    """
    Attach the vendor to validated data before saving.
    """
    validated_data['vendor'] = user
    return validated_data