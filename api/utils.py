from functools import wraps
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
def perfil_requerido(perfil):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            jwt_id = get_jwt_identity()
            user_id = jwt_id.split(';')[0]
            perfil_id = jwt_id.split(';')[1]
            if perfil_id not in perfil:
                return {"error": "Insufficient permissions"}, 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator