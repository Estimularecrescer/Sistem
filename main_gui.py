# Em main_gui.py
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout,
    QHeaderView
)
import pacientes_logic
from pacientes_gui import JanelaCadastroPaciente # Importa nossa janela de cadastro

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão da Clínica")
        self.resize(800, 600)
        
        # --- Layout e Widgets ---
        self.layout_principal = QVBoxLayout()
        
        # Tabela para listar pacientes
        self.tabela_pacientes = QTableWidget()
        self.tabela_pacientes.setColumnCount(4) # Define 4 colunas
        self.tabela_pacientes.setHorizontalHeaderLabels(["Nome", "Terapeuta", "Contato", "Obs."])
        self.tabela_pacientes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # Colunas se ajustam
        
        # Botões de Ação
        self.layout_botoes = QHBoxLayout()
        self.btn_adicionar = QPushButton("Adicionar Novo Paciente")
        self.btn_recarregar = QPushButton("Recarregar Lista")
        self.layout_botoes.addWidget(self.btn_adicionar)
        self.layout_botoes.addWidget(self.btn_recarregar)
        
        self.layout_principal.addLayout(self.layout_botoes)
        self.layout_principal.addWidget(self.tabela_pacientes)
        
        # Widget central para conter o layout
        central_widget = QWidget()
        central_widget.setLayout(self.layout_principal)
        self.setCentralWidget(central_widget)
        
        # --- Conectando Sinais ---
        self.btn_adicionar.clicked.connect(self.abrir_janela_cadastro)
        self.btn_recarregar.clicked.connect(self.carregar_pacientes)
        
        # Carrega os dados iniciais
        self.carregar_pacientes()

    def carregar_pacientes(self):
        """Busca os dados na planilha e preenche a tabela."""
        print("Carregando pacientes...")
        self.tabela_pacientes.setRowCount(0) # Limpa a tabela
        
        lista_de_pacientes = pacientes_logic.listar_pacientes()
        
        for i, paciente in enumerate(lista_de_pacientes):
            self.tabela_pacientes.insertRow(i)
            self.tabela_pacientes.setItem(i, 0, QTableWidgetItem(str(paciente.get("Nome", ""))))
            self.tabela_pacientes.setItem(i, 1, QTableWidgetItem(str(paciente.get("Terapeuta Responsavel", ""))))
            self.tabela_pacientes.setItem(i, 2, QTableWidgetItem(str(paciente.get("Celular", ""))))
            self.tabela_pacientes.setItem(i, 3, QTableWidgetItem(str(paciente.get("Observacoes", ""))))
        print("Pacientes carregados.")

    def abrir_janela_cadastro(self):
        """Abre a janela de diálogo para cadastrar um novo paciente."""
        dialog = JanelaCadastroPaciente(self)
        
        # .exec() abre a janela e pausa o código da janela principal até ela ser fechada
        if dialog.exec():
            # Se o diálogo foi fechado com sucesso (clicando em salvar), recarrega a lista
            self.carregar_pacientes()

# --- Código para iniciar a aplicação ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JanelaPrincipal()
    window.show()
    sys.exit(app.exec())