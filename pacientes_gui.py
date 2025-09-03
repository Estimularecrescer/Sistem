# Em pacientes_gui.py
import sys
from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, 
    QFormLayout, QVBoxLayout, QMessageBox
)
import pacientes_logic 

class JanelaCadastroPaciente(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Novo Paciente")
        self.setMinimumWidth(400)

        form_layout = QFormLayout()

        # --- Campos de input (iguais a antes) ---
        self.nome_input = QLineEdit()
        self.telefone_input = QLineEdit()
        self.cpf_input = QLineEdit()
        self.rg_input = QLineEdit()
        self.endereco_input = QLineEdit()
        self.nascimento_input = QLineEdit()
        self.convenio_input = QLineEdit()
        
        # --- Campos de endereço que serão preenchidos ---
        self.cep_input = QLineEdit()
        self.endereco_input = QLineEdit()
        self.bairro_input = QLineEdit()
        self.cidade_input = QLineEdit()
        self.estado_input = QLineEdit()

        # --- Adicionando widgets na ordem correta ---
        form_layout.addRow(QLabel("Nome Completo:"), self.nome_input)
        form_layout.addRow(QLabel("Telefone:"), self.telefone_input)
        form_layout.addRow(QLabel("CPF:"), self.cpf_input)
        form_layout.addRow(QLabel("RG:"), self.rg_input)
        form_layout.addRow(QLabel("Data de Nascimento:"), self.nascimento_input)
        form_layout.addRow(QLabel("Convênio:"), self.convenio_input)
        
        form_layout.addRow(QLabel("--- Endereço ---"))
        form_layout.addRow(QLabel("CEP:"), self.cep_input)
        form_layout.addRow(QLabel("Endereço:"), self.endereco_input)
        form_layout.addRow(QLabel("Bairro:"), self.bairro_input)
        form_layout.addRow(QLabel("Cidade:"), self.cidade_input)
        form_layout.addRow(QLabel("Estado:"), self.estado_input)

        self.salvar_button = QPushButton("Salvar Paciente")

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.salvar_button)
        
        self.setLayout(main_layout)
        
        # --- CONEXÕES DOS BOTÕES E CAMPOS ---
        self.salvar_button.clicked.connect(self.salvar_paciente)
        # MÁGICA AQUI: Conecta o sinal 'editingFinished' do campo CEP a uma nova função
        self.cep_input.editingFinished.connect(self.preencher_endereco_por_cep)

    # --- NOVA FUNÇÃO PARA PREENCHER O ENDEREÇO ---
    def preencher_endereco_por_cep(self):
        """É chamada quando o usuário termina de digitar o CEP."""
        cep = self.cep_input.text()
        if not cep:
            return

        dados_endereco = pacientes_logic.consultar_cep(cep)
        
        if dados_endereco:
            # Preenche os campos da interface com os dados da API
            self.endereco_input.setText(dados_endereco.get('logradouro', ''))
            self.bairro_input.setText(dados_endereco.get('bairro', ''))
            self.cidade_input.setText(dados_endereco.get('localidade', ''))
            self.estado_input.setText(dados_endereco.get('uf', ''))
        else:
            QMessageBox.warning(self, "CEP não encontrado", "O CEP digitado não foi encontrado. Por favor, verifique ou preencha o endereço manualmente.")

    def salvar_paciente(self):
        # Constrói o campo de endereço completo para salvar na planilha
        endereco_completo = (
            f"{self.endereco_input.text()}, "
            f"{self.bairro_input.text()}, "
            f"{self.cidade_input.text()} - {self.estado_input.text()}"
        )

        sucesso = pacientes_logic.cadastrar_paciente(
            nome=self.nome_input.text(),
            telefone=self.telefone_input.text(),
            cpf=self.cpf_input.text(),
            rg=self.rg_input.text(),
            endereco=endereco_completo,
            nascimento=self.nascimento_input.text(),
            convenio=self.convenio_input.text()
        )

        if sucesso:
            QMessageBox.information(self, "Sucesso", "Paciente cadastrado com sucesso!")
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", "Ocorreu um erro ao cadastrar o paciente.")