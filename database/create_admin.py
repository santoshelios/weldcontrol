from sqlalchemy.orm import Session
from database.connect import SessionLocal
from database.models import Usuario
import bcrypt


USUARIO = "helio"
SENHA = "123"
PERFIL = "Administrador"


def criar_admin():
    db: Session = SessionLocal()

    try:
        usuario_existente = (
            db.query(Usuario)
            .filter(Usuario.usuario == USUARIO)
            .first()
        )

        if usuario_existente:
            print("⚠️ Usuário já existe.")
            return

        senha_hash = bcrypt.hashpw(
            SENHA.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        novo_usuario = Usuario(
            usuario=USUARIO,
            senha_hash=senha_hash,
            perfil=PERFIL,
            ativo=True
        )

        db.add(novo_usuario)
        db.commit()

        print("✅ Usuário administrador criado com sucesso!")

    finally:
        db.close()


if __name__ == "__main__":
    criar_admin()