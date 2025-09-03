# Em pacientes_gui.py
from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, 
    QFormLayout, QVBoxLayout, QMessageBox
)
import pacientes_logic 

class JanelaCadastroPaciente(QDialog): # Mudamos para QDialog
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Cadastrar Novo Paciente")
        self.setMinimumWidth(400)

        # --- Layout e Widgets (exatamente como antes) ---
        form_layout = QFormLayout()
        self.nome_input = QLineEdit()
        self.terapeuta_input = QLineEdit()
        self.data_nasc_input = QLineEdit()
        self.celular_input = QLineEdit()
        self.cep_input = QLineEdit()
        self.endereco_input = QLineEdit()
        self.bairro_input = QLineEdit()
        self.cidade_input = QLineEdit()
        self.estado_input = QLineEdit()
        self.nome_resp_input = QLineEdit()
        self.cel_resp_input = QLineEdit()
        self.cpf_resp_input = QLineEdit()
        
        form_layout.addRow(QLabel("Nome Completo:"), self.nome_input)
        form_layout.addRow(QLabel("Terapeuta Responsável:"), self.terapeuta_input)
        # ... (adicione todas as outras linhas do formulário aqui)
        form_layout.addRow(QLabel("CPF do Responsável:"), self.cpf_resp_input)

        self.salvar_button = QPushButton("Salvar Paciente")

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.salvar_button)
        
        self.setLayout(main_layout)

        # --- Conexão do Sinal ao Slot ---
        self.salvar_button.clicked.connect(self.salvar_paciente)

    def salvar_paciente(self):
        dados_paciente = {
            "nome": self.nome_input.text(), "terapeuta_responsavel": self.terapeuta_input.text(),
            "data_nasc": self.data_nasc_input.text(), "celular": self.celular_input.text(),
            "cep": self.cep_input.text(), "endereco": self.endereco_input.text(),
            "bairro": self.bairro_input.text(), "cidade": self.cidade_input.text(),
            "estado": self.estado_input.text(), "nome_resp": self.nome_resp_input.text(),
            "cel_resp": self.cel_resp_input.text(), "cpf_resp": self.cpf_resp_input.text(),
        }

        # Validação simples para o campo nome
        if not dados_paciente["nome"]:
            QMessageBox.warning(self, "Atenção", "O campo 'Nome Completo' é obrigatório.")
            return

        sucesso = pacientes_logic.cadastrar_paciente(**dados_paciente)

        if sucesso:
            QMessageBox.information(self, "Sucesso", "Paciente cadastrado com sucesso!")
            self.accept() # Fecha a janela de diálogo com status de sucesso
        else:
            QMessageBox.critical(self, "Erro", "Ocorreu um erro ao cadastrar o paciente.")