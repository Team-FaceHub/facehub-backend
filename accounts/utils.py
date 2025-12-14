from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """
    Zwraca słownik z refresh i access tokenem dla danego użytkownika.
    Używamy tego w rejestracji i logowaniu.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
