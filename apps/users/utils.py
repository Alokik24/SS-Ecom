def requires_totp(user):
    return (
        user.is_authenticated and (
            user.is_staff or getattr(user, 'role', None) in ['admin', 'vendor']
        )
    )
