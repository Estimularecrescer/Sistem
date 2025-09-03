import pacientes_logic

def main():
    print("--- INICIANDO TESTE COMPLETO DO MÓDULO DE PACIENTES ---")

    print("\n[TESTE 1] Listando terapeutas disponíveis...")
    terapeutas = pacientes_logic.listar_terapeutas()
    if terapeutas:
        print("Terapeutas encontrados:", ", ".join(terapeutas))
        terapeuta_exemplo = terapeutas[0] 
    else:
        print("Nenhum terapeuta encontrado. Verifique a planilha 'Terapeutas'.")
        terapeuta_exemplo = "Dra. Exemplo"


    print("\n[TESTE 2] Cadastrando um novo paciente completo...")
    pacientes_logic.cadastrar_paciente(
        nome="Carlos Andrade", 
        terapeuta_responsavel=terapeuta_exemplo,
        data_nasc="15/05/1990",
        celular="(21) 98765-4321",
        cep="22290-240",
        endereco="Av. Pasteur, 250",
        bairro="Urca",
        cidade="Rio de Janeiro",
        estado="RJ",
        nome_resp="Mariana Andrade",
        cel_resp="(21) 99999-0000",
        cpf_resp="123.456.789-00"
    )

    print("\n[TESTE 3] Listando todos os pacientes cadastrados...")
    todos_os_pacientes = pacientes_logic.listar_pacientes()

    if todos_os_pacientes:
        for paciente in todos_os_pacientes:
            print(f"- Nome: {paciente.get('Nome')}, Terapeuta: {paciente.get('Terapeuta Responsavel')}")
    else:
        print("Nenhum paciente encontrado.")
    
    print("\n--- TESTE FINALIZADO ---")

if __name__ == "__main__":
    main()