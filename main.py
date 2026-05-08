import flet as ft
import webbrowser

# =========================
# PÁGINAS PRINCIPAIS
# =========================
from pages.login import login_view
from pages.cadastro import cadastro
from pages.home import home_view
from pages.perfil import perfil
from pages.inscricoes import inscricoes
from pages.cursos import cursos
from pages.inscricao_form import inscricao_form
from pages.criar_curso import criar_curso
from pages.qr_page import qr_page
from pages.editar_perfil import editar_perfil
from pages.adicionar_story import adicionar_story

# =========================
# PÁGINAS EXTRAS
# =========================
from pages.feed import feed_page
from pages.comentarios import comentarios_page
from pages.aulas import aulas_page
from pages.pagamentos import pagamento_page

# =========================
# SISTEMA EXTRA
# =========================
from pages.pages.chat import chat_page
from pages.pages.notificacoes import notificacoes_page
from pages.pages.avaliacoes import avaliacoes_page
from pages.pages.admin_dashboard import admin_dashboard


def main(page: ft.Page):

    # =========================
    # CONFIG PAGE
    # =========================
    page.title = "Apexia"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f172a"

    page.window_width = 400
    page.window_height = 800

    page.padding = 0
    page.spacing = 0

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # =========================
    # STATE
    # =========================
    state = {
        "user": None,
        "curso_id": None,
        "post_id": None,
    }

    # =========================
    # ALERTA
    # =========================
    def alert(msg):

        page.snack_bar = ft.SnackBar(
            content=ft.Text(
                msg,
                color="white"
            ),
            bgcolor="#111827",
            duration=2500
        )

        page.snack_bar.open = True
        page.update()

    # =========================
    # USER
    # =========================
    def get_user():
        return state["user"]

    def set_user(user):

        state["user"] = user

        if "_stories" not in state["user"]:
            state["user"]["_stories"] = []

        if "_feed" not in state["user"]:
            state["user"]["_feed"] = []

        go("/home")

    # =========================
    # LOGOUT
    # =========================
    def logout():

        state["user"] = None
        state["curso_id"] = None
        state["post_id"] = None

        go("/")

    # =========================
    # GO
    # =========================
    def go(route):

        page.route = route
        route_change(None)

    # =========================
    # CURSO
    # =========================
    def abrir_inscricao(curso_id):

        state["curso_id"] = curso_id
        go("/inscricao_form")

    def abrir_avaliacoes(curso_id):

        state["curso_id"] = curso_id
        go("/avaliacoes")

    def abrir_aulas(curso_id):

        state["curso_id"] = curso_id
        go("/aulas")

    def abrir_pagamento(curso_id):

        state["curso_id"] = curso_id
        go("/pagamento")

    # =========================
    # POSTS
    # =========================
    def abrir_comentarios(post_id):

        state["post_id"] = post_id
        go("/comentarios")

    # =========================
    # ROUTER
    # =========================
    def router():

        return {

            # =========================
            # LOJA HTML
            # =========================
            "loja": lambda: webbrowser.open(
                r"file:///C:/Users/sesi2a/Desktop/apexia/assets/loja.html"
            ),

            # =========================
            # PRINCIPAL
            # =========================
            "home": lambda: go("/home"),
            "login": lambda: go("/"),
            "cadastro": lambda: go("/cadastro"),

            # =========================
            # PERFIL
            # =========================
            "profile": lambda: go("/perfil"),
            "perfil": lambda: go("/perfil"),

            "editar_perfil": lambda: go("/editar_perfil"),

            "adicionar_story": lambda: go("/adicionar_story"),

            # =========================
            # CURSOS
            # =========================
            "cursos": lambda: go("/cursos"),
            "criar_curso": lambda: go("/criar_curso"),

            "insc": lambda: go("/inscricoes"),

            # =========================
            # QR
            # =========================
            "qr": lambda: go("/qr"),

            # =========================
            # SOCIAL
            # =========================
            "feed": lambda: go("/feed"),

            # =========================
            # CHAT
            # =========================
            "chat": lambda: go("/chat"),

            # =========================
            # NOTIFICAÇÕES
            # =========================
            "notificacoes": lambda: go("/notificacoes"),

            # =========================
            # ADMIN
            # =========================
            "admin": lambda: go("/admin"),

            # =========================
            # CURSO ACTIONS
            # =========================
            "ir_inscricao": abrir_inscricao,
            "abrir_avaliacoes": abrir_avaliacoes,
            "abrir_aulas": abrir_aulas,
            "abrir_pagamento": abrir_pagamento,

            # =========================
            # POSTS
            # =========================
            "comentarios": abrir_comentarios,

            # =========================
            # LOGOUT
            # =========================
            "logout": logout,
        }

    # =========================
    # LOGIN CHECK
    # =========================
    def precisa_login():

        if not get_user():

            go("/")
            return True

        return False

    # =========================
    # ROUTE CHANGE
    # =========================
    def route_change(e):

        page.controls.clear()

        user = get_user()
        r = router()

        # LOGIN
        if page.route == "/":

            page.add(
                login_view(
                    page,
                    go,
                    set_user
                )
            )

        # CADASTRO
        elif page.route == "/cadastro":

            page.add(
                cadastro(
                    page,
                    alert,
                    lambda: go("/")
                )
            )

        # HOME
        elif page.route == "/home":

            if precisa_login():
                return

            page.add(
                home_view(
                    page,
                    r
                )
            )

        # PERFIL
        elif page.route == "/perfil":

            if precisa_login():
                return

            page.add(
                perfil(
                    page,
                    r,
                    user,
                    alert
                )
            )

        # EDITAR PERFIL
        elif page.route == "/editar_perfil":

            if precisa_login():
                return

            page.add(
                editar_perfil(
                    page,
                    r,
                    user,
                    alert
                )
            )

        # STORY
        elif page.route == "/adicionar_story":

            if precisa_login():
                return

            page.add(
                adicionar_story(
                    page,
                    r,
                    user,
                    alert
                )
            )

        # INSCRIÇÕES
        elif page.route == "/inscricoes":

            if precisa_login():
                return

            page.add(
                inscricoes(
                    page,
                    r,
                    user,
                    alert
                )
            )

        # CURSOS
        elif page.route == "/cursos":

            if precisa_login():
                return

            page.add(
                cursos(
                    page,
                    r,
                    user,
                    alert
                )
            )

        # CRIAR CURSO
        elif page.route == "/criar_curso":

            if precisa_login():
                return

            page.add(
                criar_curso(
                    page,
                    r,
                    alert,
                    user
                )
            )

        # INSCRIÇÃO FORM
        elif page.route == "/inscricao_form":

            if precisa_login():
                return

            if not state["curso_id"]:

                alert("Selecione um curso primeiro")
                go("/cursos")
                return

            page.add(
                inscricao_form(
                    page,
                    r,
                    user,
                    state["curso_id"],
                    alert
                )
            )

        # QR
        elif page.route == "/qr":

            if precisa_login():
                return

            page.add(
                qr_page(
                    page,
                    r,
                    user,
                    alert
                )
            )

        # FEED
        elif page.route == "/feed":

            if precisa_login():
                return

            page.add(
                feed_page(
                    page,
                    r,
                    user,
                    alert
                )
            )

        # CHAT
        elif page.route == "/chat":

            if precisa_login():
                return

            page.add(
                chat_page(
                    page,
                    r,
                    user,
                    alert
                )
            )

        # 404
        else:

            page.add(
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "Página não encontrada",
                        color="white",
                        size=24
                    )
                )
            )

        page.update()

    # =========================
    # EVENTS
    # =========================
    page.on_route_change = route_change

    # =========================
    # START
    # =========================
    page.route = "/"

    route_change(None)


ft.app(target=main)