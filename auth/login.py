import bcrypt
from database.connect import SessionLocal
from database.models import Usuario


def autenticar(usuario, senha):
    db = SessionLocal()

    try:
        user = (
            db.query(Usuario)
            .filter(
                Usuario.usuario == usuario,
                Usuario.ativo == True
            )
            .first()
        )

        if not user:
            return None

        senha_ok = bcrypt.checkpw(
            senha.encode("utf-8"),
            user.senha_hash.encode("utf-8")
        )

        if senha_ok:
            return user

        return None

    finally:
        db.close()