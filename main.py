from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.label import Label
import json
import os
from datetime import datetime, date

# Onde salva no celular (localStorage do APK)
ARQUIVO = "/storage/emulated/0/Download/produtos.json"

KV = """
<Tela>:
    orientation: 'vertical'
    padding: 15
    spacing: 10

    Label:
        text: 'Controle de Validade'
        size_hint_y: None
        height: 40
        bold: True

    TextInput:
        id: nome
        hint_text: 'Nome: ex Tomate'
        size_hint_y: None
        height: 45

    TextInput:
        id: validade
        hint_text: 'Validade AAAA-MM-DD ex 2026-09-30'
        size_hint_y: None
        height: 45

    BoxLayout:
        size_hint_y: None
        height: 45
        spacing: 10
        TextInput:
            id: qtd
            hint_text: 'Qtd ex 1.5'
            input_filter: 'float'
        Spinner:
            id: tipo
            text: 'un'
            values: ['un', 'kg']

    BoxLayout:
        size_hint_y: None
        height: 45
        spacing: 10
        Button:
            text: 'SALVAR'
            on_press: root.salvar_produto()
        Button:
            text: 'VERIFICAR'
            on_press: root.verificar_produtos()

    Label:
        id: status
        text: ''
        size_hint_y: None
        height: 30

    ScrollView:
        GridLayout:
            id: lista
            cols: 1
            spacing: 5
            size_hint_y: None
            height: self.minimum_height
"""

class Tela(BoxLayout):

    def carregar_lista(self):
        if os.path.exists(ARQUIVO):
            try:
                with open(ARQUIVO, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def salvar_lista(self, lista):
        # Cria pasta se não existir
        os.makedirs(os.path.dirname(ARQUIVO), exist_ok=True)
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)

    def mostrar_na_tela(self, p):
        try:
            hoje = date.today()
            val = datetime.strptime(p["validade"], "%Y-%m-%d").date()
            dias = (val - hoje).days

            if dias < 0:
                cor = "ff0000"
                status = f"VENCIDO {abs(dias)}d"
            elif dias <= 7:
                cor = "ffcc00"
                status = f"VENCE em {dias}d"
            else:
                cor = "00ff00"
                status = f"OK {dias}d"

            texto = f"[color={cor}]{status}[/color] {p['nome']} - {p['qtd']}{p['tipo']}"
            lb = Label(text=texto, markup=True, size_hint_y=None, height=35, halign="left")
            self.ids.lista.add_widget(lb)
        except:
            pass

    def salvar_produto(self):
        nome = self.ids.nome.text.strip()
        validade = self.ids.validade.text.strip()
        qtd = self.ids.qtd.text.strip()
        tipo = self.ids.tipo.text

        if not nome or not validade or not qtd:
            self.ids.status.text = "Preencha tudo!"
            return

        try