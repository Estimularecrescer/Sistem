# Em pacientes_gui.py
from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, 
    QFormLayout, QVBoxLayout, QMessageBox
)
import pacientes_logic 

class JanelaCadastroPaciente(QDialog):
    def __init__(self, paciente_data=None, parent=None):
        super().__init__(parent)
        
        self.modo_edicao = paciente_data is not None
        self.nome_original = paciente_data.get("Nome") if self.modo_edicao else None

        titulo = "Editar Paciente" if self.modo_edicao else "Cadastrar Novo Paciente"
        self.setWindowTitle(titulo)
        self.setMinimumWidth(400)

        form_layout = QFormLayout()

        # --- Campos de Dados Pessoais ---
        self.nome_input = QLineEdit()
        self.telefone_input = QLineEdit()
        self.cpf_input = QLineEdit()
        self.rg_input = QLineEdit()
        self.nascimento_input = QLineEdit()
        self.convenio_input = QLineEdit()

        form_layout.addRow(QLabel("Nome Completo:"), self.nome_input)
        form_layout.addRow(QLabel("Telefone/Celular:"), self.telefone_input)
        form_layout.addRow(QLabel("CPF:"), self.cpf_input)
        form_layout.addRow(QLabel("RG:"), self.rg_input)
        form_layout.addRow(QLabel("Data de Nascimento:"), self.nascimento_input)
        form_layout.addRow(QLabel("Convênio:"), self.convenio_input)
        
        # --- Campos de Endereço (agora todos incluídos) ---
        self.cep_input = QLineEdit()
        self.endereco_input = QLineEdit()
        self.bairro_input = QLineEdit()
        self.cidade_input = QLineEdit()
        self.estado_input = QLineEdit()

        form_layout.addRow(QLabel("--- Endereço ---"))
        form_layout.addRow(QLabel("CEP:"), self.cep_input)
        form_layout.addRow(QLabel("Endereço (Rua, Nº):"), self.endereco_input)
        form_layout.addRow(QLabel("Bairro:"), self.bairro_input)
        form_layout.addRow(QLabel("Cidade:"), self.cidade_input)
        form_layout.addRow(QLabel("Estado:"), self.estado_input)

        self.salvar_button = QPushButton("Salvar Alterações" if self.modo_edicao else "Salvar Paciente")

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.salvar_button)
        
        # --- Conexões ---
        self.salvar_button.clicked.connect(self.salvar_paciente)
        self.cep_input.editingFinished.connect(self.preencher_endereco_por_cep)

        if self.modo_edicao:
            self.preencher_formulario(paciente_data)

    def preencher_formulario(self, data):
        """Preenche TODOS os campos do formulário com os dados de um paciente existente."""
        self.nome_input.setText(str(data.get("Nome", "")))
        self.telefone_input.setText(str(data.get("Celular", "")))
        self.cpf_input.setText(str(data.get("CPF", "")))
        self.rg_input.setText(str(data.get("RG", "")))
        # Preenche os campos de endereço também
        self.endereco_input.setText(str(data.get("Endereco", "")))
        self.nascimento_input.setText(str(data.get("NASCIMENTO", "")))
        self.convenio_input.setText(str(data.get("convenio", "")))
        self.cep_input.setText(str(data.get("cep", ""))) # <-- CAMPO ADICIONADO

    def preencher_endereco_por_cep(self):
        """É chamada quando o usuário termina de digitar o CEP."""
        cep = self.cep_input.text()
        if not cep:
            return

        dados_endereco = pacientes_logic.consultar_cep(cep)
        
        if dados_endereco:
            self.endereco_input.setText(dados_endereco.get('logradouro', ''))
            self.bairro_input.setText(dados_endereco.get('bairro', ''))
            self.cidade_input.setText(dados_endereco.get('localidade', ''))
            self.estado_input.setText(dados_endereco.get('uf', ''))
        else:
            QMessageBox.warning(self, "CEP não encontrado", "O CEP digitado não foi encontrado.")

    def salvar_paciente(self):
        # Constrói o campo de endereço completo para salvar
        endereco_completo = (
            f"{self.endereco_input.text()}, "
            f"{self.bairro_input.text()}, "
            f"{self.cidade_input.text()} - {self.estado_input.text()}"
        )
        
        # Coleta os dados para enviar para a lógica
        dados_paciente = {
            "nome": self.nome_input.text(),
            "telefone": self.telefone_input.text(),
            "cpf": self.cpf_input.text(),
            "rg": self.rg_input.text(),
            "endereco": endereco_completo,
            "nascimento": self.nascimento_input.text(),
            "convenio": self.convenio_input.text(),
            "cep": self.cep_input.text(), # Salva o CEP também
        }
        
        if not dados_paciente["nome"]:
            QMessageBox.warning(self, "Atenção", "O campo 'Nome Completo' é obrigatório.")
            return

        if self.modo_edicao:
            sucesso = pacientes_logic.editar_paciente(self.nome_original, dados_paciente)
            mensagem = "Paciente atualizado com sucesso!"
        else:
            sucesso = pacientes_logic.cadastrar_paciente(**dados_paciente)
            mensagem = "Paciente cadastrado com sucesso!"

        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.accept()
        else:
            QMessageBox.critical(self, "Erro", "Ocorreu um erro ao salvar os dados do paciente.")