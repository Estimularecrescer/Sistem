# Em main_gui.py
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QHeaderView, QMessageBox, QStackedWidget
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize

import pacientes_logic
from pacientes_gui import JanelaCadastroPaciente

def carregar_estilo():
    with open("style.qss", "r") as f:
        return f.read()


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão da Clínica")
        self.resize(1200, 800)
        
        self.layout_geral = QHBoxLayout()
        self.criar_sidebar()
        self.criar_area_principal()

        self.layout_geral.addWidget(self.sidebar_widget, 1)
        self.layout_geral.addWidget(self.main_area_widget, 4)
        
        widget_central = QWidget()
        widget_central.setLayout(self.layout_geral)
        self.setCentralWidget(widget_central)

    def criar_sidebar(self):
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setObjectName("Sidebar")
        
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_widget.setFixedWidth(200)

        self.btn_nav_pacientes = QPushButton("Pacientes")
        self.btn_nav_pacientes.setIcon(QIcon("icon_pacientes.png"))
        self.btn_nav_pacientes.setIconSize(QSize(32, 32))
        self.btn_nav_pacientes.setCheckable(True) 
        self.btn_nav_pacientes.setChecked(True) 

        self.btn_nav_agenda = QPushButton("Agenda")
        self.btn_nav_agenda.setCheckable(True)
        self.btn_nav_agenda.setEnabled(False) 

        self.sidebar_layout.addWidget(self.btn_nav_pacientes)
        self.sidebar_layout.addWidget(self.btn_nav_agenda)
        self.sidebar_layout.addStretch()

        self.btn_nav_pacientes.clicked.connect(lambda: self.main_stack.setCurrentIndex(0))
        
    def criar_area_principal(self):
        self.main_area_widget = QWidget()
        self.main_area_layout = QVBoxLayout(self.main_area_widget)

        self.logo_label = QLabel()
        self.logo_label.setObjectName("LogoLabel")
        pixmap = QPixmap('logo.png')
        self.logo_label.setPixmap(pixmap.scaledToWidth(300))
        self.main_area_layout.addWidget(self.logo_label)

        self.main_stack = QStackedWidget()
        self.main_area_layout.addWidget(self.main_stack)
        
        self.tela_pacientes = QWidget()
        self.tela_pacientes_layout = QVBoxLayout(self.tela_pacientes)
        self.tabela_pacientes = QTableWidget()
        self.tabela_pacientes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_pacientes.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela_pacientes.itemSelectionChanged.connect(self.atualizar_estado_botoes)
        layout_botoes_pacientes = QHBoxLayout()
        self.btn_adicionar = QPushButton("➕ Adicionar")
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_excluir = QPushButton("❌ Excluir")
        btn_recarregar = QPushButton("🔄 Recarregar")
        layout_botoes_pacientes.addWidget(self.btn_adicionar)
        layout_botoes_pacientes.addWidget(self.btn_editar)
        layout_botoes_pacientes.addWidget(self.btn_excluir)
        layout_botoes_pacientes.addStretch()
        layout_botoes_pacientes.addWidget(btn_recarregar)
        self.tela_pacientes_layout.addLayout(layout_botoes_pacientes)
        self.tela_pacientes_layout.addWidget(self.tabela_pacientes)
        self.main_stack.addWidget(self.tela_pacientes)
        self.btn_adicionar.clicked.connect(self.abrir_janela_cadastro)
        btn_recarregar.clicked.connect(self.carregar_pacientes)
        self.btn_excluir.clicked.connect(self.excluir_paciente_selecionado)
        self.carregar_pacientes()
        self.atualizar_estado_botoes()
        
    # ... Todas as outras funções (carregar_pacientes, abrir_janela_cadastro, etc.) continuam iguais ...
    def carregar_pacientes(self):
        self.tabela_pacientes.setRowCount(0)
        lista_de_pacientes = pacientes_logic.listar_pacientes()
        if not lista_de_pacientes: return
        headers = list(lista_de_pacientes[0].keys())
        self.tabela_pacientes.setColumnCount(len(headers))
        self.tabela_pacientes.setHorizontalHeaderLabels(headers)
        self.tabela_pacientes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i, paciente_dict in enumerate(lista_de_pacientes):
            self.tabela_pacientes.insertRow(i)
            for j, header in enumerate(headers):
                valor = str(paciente_dict.get(header, ""))
                self.tabela_pacientes.setItem(i, j, QTableWidgetItem(valor))

    def abrir_janela_cadastro(self):
        dialog = JanelaCadastroPaciente(self)
        if dialog.exec():
            self.carregar_pacientes()

    def atualizar_estado_botoes(self):
        tem_selecao = bool(self.tabela_pacientes.selectedItems())
        self.btn_editar.setEnabled(tem_selecao)
        self.btn_excluir.setEnabled(tem_selecao)
        
    def excluir_paciente_selecionado(self):
        linha_selecionada = self.tabela_pacientes.currentRow()
        if linha_selecionada < 0: return
        nome_paciente = self.tabela_pacientes.item(linha_selecionada, 0).text()
        confirmacao = QMessageBox.question(self, "Confirmar Exclusão", f"Tem certeza que deseja excluir '{nome_paciente}'?", QMessageBox.Yes | QMessageBox.No)
        if confirmacao == QMessageBox.Yes:
            if pacientes_logic.excluir_paciente(nome_paciente):
                self.carregar_pacientes()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível excluir o paciente.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(carregar_estilo()) # <-- MUDANÇA AQUI
    window = JanelaPrincipal()
    window.show()
    sys.exit(app.exec())