import os
import time
import requests

from config import (
    BASE_REST,
    TIMEOUT,
    get_headers,
    storage_upload_url,
    storage_public_url
)


# ========================
# CONFIGURAÇÃO / REQUEST
# ========================

OK_STATUS = [200, 201, 204]


def request(method, endpoint, **kwargs):
    url = f"{BASE_REST}/{endpoint}"

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=get_headers(),
            timeout=TIMEOUT,
            **kwargs
        )

        if response.status_code not in OK_STATUS:
            print(f"[API ERRO] {method} {endpoint}")
            print("Status:", response.status_code)
            print("Resposta:", response.text)

        return response

    except requests.exceptions.Timeout:
        print(f"[API TIMEOUT] {method} {endpoint}")
        return None

    except requests.exceptions.ConnectionError:
        print(f"[API CONEXÃO] Falha ao conectar em {endpoint}")
        return None

    except Exception as erro:
        print(f"[API ERRO GERAL] {method} {endpoint}: {erro}")
        return None


def json_response(response, default=None):
    if default is None:
        default = []

    if not response or response.status_code not in OK_STATUS:
        return default

    try:
        if response.status_code == 204:
            return default

        return response.json()

    except Exception:
        return default


def ok(response):
    return bool(response and response.status_code in OK_STATUS)


# ========================
# USUÁRIOS
# ========================

def login(email, senha):
    email = (email or "").strip().lower()
    senha = senha or ""

    if not email or not senha:
        return None

    response = request("GET", f"usuarios?email=eq.{email}")
    data = json_response(response)

    if not data:
        return None

    user = data[0]

    if user.get("senha") != senha:
        return None

    if "_stories" not in user:
        user["_stories"] = []

    if "_feed" not in user:
        user["_feed"] = []

    if "bio" not in user:
        user["bio"] = ""

    return user


def cadastrar(nome, email, senha):
    nome = (nome or "").strip()
    email = (email or "").strip().lower()
    senha = senha or ""

    if not nome or not email or not senha:
        return False

    check = request("GET", f"usuarios?email=eq.{email}")

    if check and check.status_code == 200 and check.json():
        return False

    data = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "foto": "",
        "bio": ""
    }

    response = request("POST", "usuarios", json=data)
    return ok(response)


def update_user(user_id, nome, foto="", bio=None):
    if not user_id:
        return False

    data = {
        "nome": (nome or "").strip(),
        "foto": foto or ""
    }

    if bio is not None:
        data["bio"] = bio or ""

    response = request(
        "PATCH",
        f"usuarios?id=eq.{user_id}",
        json=data
    )

    return ok(response)


def get_usuario(user_id):
    response = request("GET", f"usuarios?id=eq.{user_id}")
    data = json_response(response)
    return data[0] if data else None


def buscar_usuario_por_email(email):
    email = (email or "").strip().lower()
    response = request("GET", f"usuarios?email=eq.{email}")
    data = json_response(response)
    return data[0] if data else None


# ========================
# CURSOS
# ========================

def get_cursos():
    response = request("GET", "ranking_cursos?order=favoritos.desc,inscritos.desc")
    return json_response(response)


def get_curso(curso_id):
    response = request("GET", f"cursos?id=eq.{curso_id}")
    data = json_response(response)
    return data[0] if data else None


def criar_curso(data):
    if not data:
        return False

    response = request("POST", "cursos", json=data)
    return ok(response)


def update_curso(curso_id, data):
    if not curso_id or not data:
        return False

    response = request(
        "PATCH",
        f"cursos?id=eq.{curso_id}",
        json=data
    )

    return ok(response)


def delete_curso(curso_id):
    response = request("DELETE", f"cursos?id=eq.{curso_id}")
    return ok(response)


# ========================
# FAVORITOS
# ========================

def favoritar_curso(usuario_id, curso_id):
    check = request(
        "GET",
        f"favoritos?usuario_id=eq.{usuario_id}&curso_id=eq.{curso_id}"
    )

    if check and check.status_code == 200 and check.json():
        return False

    response = request(
        "POST",
        "favoritos",
        json={
            "usuario_id": usuario_id,
            "curso_id": curso_id
        }
    )

    return ok(response)


def desfavoritar_curso(usuario_id, curso_id):
    response = request(
        "DELETE",
        f"favoritos?usuario_id=eq.{usuario_id}&curso_id=eq.{curso_id}"
    )

    return ok(response)


def get_favoritos_usuario(usuario_id):
    response = request("GET", f"favoritos?usuario_id=eq.{usuario_id}")
    return json_response(response)


# ========================
# INSCRIÇÕES
# ========================

def get_inscricoes(user_id):
    response = request("GET", f"inscricoes?usuario_id=eq.{user_id}")
    return json_response(response)


def criar_inscricao(user_id, curso_id, nome, cpf, horario):
    check = request(
        "GET",
        f"inscricoes?usuario_id=eq.{user_id}&curso_id=eq.{curso_id}"
    )

    if check and check.status_code == 200 and check.json():
        return False

    response = request(
        "POST",
        "inscricoes",
        json={
            "usuario_id": user_id,
            "curso_id": curso_id,
            "nome": nome,
            "cpf": cpf,
            "horario": horario
        }
    )

    return ok(response)


def delete_inscricao(user_id, curso_id):
    response = request(
        "DELETE",
        f"inscricoes?usuario_id=eq.{user_id}&curso_id=eq.{curso_id}"
    )

    return ok(response)


# ========================
# SEGUIDORES
# ========================

def seguir_usuario(seguidor_id, seguindo_id):
    if str(seguidor_id) == str(seguindo_id):
        return False

    check = request(
        "GET",
        f"seguidores?seguidor_id=eq.{seguidor_id}&seguindo_id=eq.{seguindo_id}"
    )

    if check and check.status_code == 200 and check.json():
        return False

    response = request(
        "POST",
        "seguidores",
        json={
            "seguidor_id": seguidor_id,
            "seguindo_id": seguindo_id
        }
    )

    return ok(response)


def deixar_de_seguir(seguidor_id, seguindo_id):
    response = request(
        "DELETE",
        f"seguidores?seguidor_id=eq.{seguidor_id}&seguindo_id=eq.{seguindo_id}"
    )

    return ok(response)


def get_seguidores(user_id):
    response = request("GET", f"seguidores?seguindo_id=eq.{user_id}")
    return json_response(response)


def get_seguindo(user_id):
    response = request("GET", f"seguidores?seguidor_id=eq.{user_id}")
    return json_response(response)


# ========================
# MENSAGENS
# ========================

def enviar_mensagem(remetente, destinatario, mensagem):
    if not mensagem:
        return False

    response = request(
        "POST",
        "mensagens",
        json={
            "remetente_id": remetente,
            "destinatario_id": destinatario,
            "mensagem": mensagem
        }
    )

    return ok(response)


def get_mensagens(user_id, outro_id):
    response = request(
        "GET",
        f"mensagens?or=(and(remetente_id.eq.{user_id},destinatario_id.eq.{outro_id}),and(remetente_id.eq.{outro_id},destinatario_id.eq.{user_id}))&order=criado_em.asc"
    )

    return json_response(response)


# ========================
# NOTIFICAÇÕES
# ========================

def get_notificacoes(user_id):
    response = request(
        "GET",
        f"notificacoes?usuario_id=eq.{user_id}&order=criado_em.desc"
    )

    return json_response(response)


def marcar_notificacao_lida(notif_id):
    response = request(
        "PATCH",
        f"notificacoes?id=eq.{notif_id}",
        json={"lida": True}
    )

    return ok(response)


# ========================
# AVALIAÇÕES
# ========================

def avaliar_curso(user_id, curso_id, nota, comentario):
    check = request(
        "GET",
        f"avaliacoes?usuario_id=eq.{user_id}&curso_id=eq.{curso_id}"
    )

    data = {
        "nota": nota,
        "comentario": comentario or ""
    }

    if check and check.status_code == 200 and check.json():
        response = request(
            "PATCH",
            f"avaliacoes?usuario_id=eq.{user_id}&curso_id=eq.{curso_id}",
            json=data
        )
        return ok(response)

    data["usuario_id"] = user_id
    data["curso_id"] = curso_id

    response = request("POST", "avaliacoes", json=data)
    return ok(response)


def get_avaliacoes(curso_id):
    response = request(
        "GET",
        f"avaliacoes?curso_id=eq.{curso_id}&order=criado_em.desc"
    )

    return json_response(response)


# ========================
# DASHBOARD
# ========================

def get_dashboard():
    response = request("GET", "dashboard_admin")
    data = json_response(response)
    return data[0] if data else {}


# ========================
# FEED / POSTS
# ========================

def criar_post(usuario_id, curso_id=None, texto="", imagem=""):
    data = {
        "usuario_id": usuario_id,
        "texto": texto or "",
        "imagem": imagem or ""
    }

    if curso_id:
        data["curso_id"] = curso_id

    response = request("POST", "posts", json=data)
    return ok(response)


def get_posts():
    response = request("GET", "posts?order=criado_em.desc")
    return json_response(response)


def get_posts_usuario(usuario_id):
    response = request(
        "GET",
        f"posts?usuario_id=eq.{usuario_id}&order=criado_em.desc"
    )

    return json_response(response)


def delete_post(post_id):
    response = request("DELETE", f"posts?id=eq.{post_id}")
    return ok(response)


# ========================
# STORIES
# ========================

def criar_story(usuario_id, titulo, midia_url, legenda="", tipo="imagem"):
    if not usuario_id or not midia_url:
        return False

    data = {
        "usuario_id": usuario_id,
        "titulo": titulo or "Story",
        "midia": midia_url,
        "img": midia_url,
        "legenda": legenda or "",
        "texto": legenda or "",
        "tipo": tipo or "imagem"
    }

    response = request("POST", "stories", json=data)
    return ok(response)


def get_stories_usuario(usuario_id):
    response = request(
        "GET",
        f"stories?usuario_id=eq.{usuario_id}&order=criado_em.desc"
    )

    return json_response(response)


def get_stories():
    response = request("GET", "stories?order=criado_em.desc")
    return json_response(response)


def delete_story(story_id):
    response = request("DELETE", f"stories?id=eq.{story_id}")
    return ok(response)


# ========================
# COMENTÁRIOS
# ========================

def criar_comentario(post_id, usuario_id, comentario):
    if not comentario:
        return False

    response = request(
        "POST",
        "comentarios",
        json={
            "post_id": post_id,
            "usuario_id": usuario_id,
            "comentario": comentario
        }
    )

    return ok(response)


def get_comentarios(post_id):
    response = request(
        "GET",
        f"comentarios?post_id=eq.{post_id}&order=criado_em.asc"
    )

    return json_response(response)


# ========================
# AULAS / VÍDEOS
# ========================

def criar_aula(curso_id, titulo, descricao, video_url):
    response = request(
        "POST",
        "aulas",
        json={
            "curso_id": curso_id,
            "titulo": titulo,
            "descricao": descricao or "",
            "video_url": video_url
        }
    )

    return ok(response)


def get_aulas(curso_id):
    response = request(
        "GET",
        f"aulas?curso_id=eq.{curso_id}&order=criado_em.asc"
    )

    return json_response(response)


def delete_aula(aula_id):
    response = request("DELETE", f"aulas?id=eq.{aula_id}")
    return ok(response)


# ========================
# PAGAMENTOS
# ========================

def criar_pagamento(usuario_id, curso_id, valor, status="pendente"):
    response = request(
        "POST",
        "pagamentos",
        json={
            "usuario_id": usuario_id,
            "curso_id": curso_id,
            "valor": valor,
            "status": status
        }
    )

    return ok(response)


def marcar_pagamento_pago(usuario_id, curso_id):
    response = request(
        "PATCH",
        f"pagamentos?usuario_id=eq.{usuario_id}&curso_id=eq.{curso_id}",
        json={"status": "pago"}
    )

    return ok(response)


def get_pagamentos_usuario(usuario_id):
    response = request(
        "GET",
        f"pagamentos?usuario_id=eq.{usuario_id}&order=criado_em.desc"
    )

    return json_response(response)


# ========================
# UPLOAD
# ========================

def upload_arquivo(file_path, prefixo="arquivo"):
    try:
        if not file_path or not os.path.exists(file_path):
            print("[UPLOAD] Arquivo não encontrado:", file_path)
            return None

        ext = os.path.splitext(file_path)[1] or ".png"
        file_name = f"{prefixo}_{int(time.time())}{ext}"

        headers = get_headers({
            "Content-Type": "application/octet-stream"
        })

        with open(file_path, "rb") as arquivo:
            response = requests.post(
                storage_upload_url(file_name),
                headers=headers,
                data=arquivo,
                timeout=TIMEOUT
            )

        if response.status_code not in [200, 201]:
            print("[UPLOAD ERRO]", response.text)
            return None

        return storage_public_url(file_name)

    except Exception as erro:
        print("[UPLOAD ERRO GERAL]", erro)
        return None


def upload_imagem(file_path):
    return upload_arquivo(file_path, "imagem")


def upload_story(file_path):
    return upload_arquivo(file_path, "story")


def upload_video(file_path):
    return upload_arquivo(file_path, "video")


# ========================
# PLANOS / ASSINATURAS
# ========================

def get_planos():
    response = request("GET", "planos?order=preco_mensal.asc")
    return json_response(response)


def get_assinatura(usuario_id):
    response = request("GET", f"assinaturas?usuario_id=eq.{usuario_id}")
    data = json_response(response)

    if data:
        return data[0]

    return {
        "plano_codigo": "free",
        "ciclo": "mensal",
        "status": "ativo",
        "valor_pago": 0
    }


def assinar_plano(usuario_id, plano_codigo, ciclo, valor_pago):
    existente = request("GET", f"assinaturas?usuario_id=eq.{usuario_id}")

    data = {
        "usuario_id": usuario_id,
        "plano_codigo": plano_codigo,
        "ciclo": ciclo,
        "valor_pago": valor_pago,
        "status": "ativo"
    }

    if existente and existente.status_code == 200 and existente.json():
        response = request(
            "PATCH",
            f"assinaturas?usuario_id=eq.{usuario_id}",
            json=data
        )
    else:
        response = request("POST", "assinaturas", json=data)

    return ok(response)


def plano_usuario(usuario_id):
    assinatura = get_assinatura(usuario_id)
    return assinatura.get("plano_codigo", "free")


def usuario_pode_criar_curso(usuario_id):
    return True, ""


def usuario_sem_anuncios(usuario_id):
    plano = plano_usuario(usuario_id)
    return plano in ["premium", "superpremium"]


def usuario_tem_aula_criador(usuario_id):
    plano = plano_usuario(usuario_id)
    return plano in ["premium", "superpremium"]


def usuario_tem_materiais_adicionais(usuario_id):
    plano = plano_usuario(usuario_id)
    return plano == "superpremium"


def usuario_tem_chance_empregaticia(usuario_id):
    plano = plano_usuario(usuario_id)
    return plano == "superpremium"


def valor_plano(plano_codigo, ciclo="mensal"):
    precos = {
        "free": 0,
        "basic": 19.90,
        "premium": 49.90,
        "superpremium": 99.90
    }

    valor = precos.get(plano_codigo, 0)

    if ciclo == "anual":
        return round((valor * 12) * 0.90, 2)

    return valor