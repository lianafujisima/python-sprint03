import os
import biblioteca as _b

_b.limpa_tela()

print("Bem-vindo ao sistema de ajuda IMREA HC pelo Whatsapp!")

# Carrega os dados dos arquivos JSON para variáveis, permitindo que o programa os manipule
pacientes = _b.carrega_dados("pacientes.json", "pacientes")
agendamentos = _b.carrega_dados("agendamentos.json", "agendamentos")
horarios_disponiveis = _b.carrega_horarios("horarios.json")
faq_lista = _b.carrega_faq()

while True:
    print("\n=== IMREA HC - Whatsapp ===")
    print("1. Menu Paciente")
    print("2. Menu Administrador")
    print("0. Sair")

    escolha = _b.entrada_valida("Escolha: ", ["0", "1", "2"])
    _b.limpa_tela()

    #encerra o programa
    if escolha == "0":
        print("Saindo do sistema...")
        break

    # Abre o menu do paciente, permitindo cadastro, agendamento, consulta de agendamentos, verificação de lembretes e acesso ao FAQ; retorna listas atualizadas
    elif escolha == "1":
        pacientes, agendamentos, horarios_disponiveis = _b.menu_paciente(pacientes, agendamentos, horarios_disponiveis)
    
    # Abre o menu do administrador, permitindo gerenciamento de horários e FAQ; retorna listas atualizadas
    elif escolha == "2":
        horarios_disponiveis, faq_lista = _b.menu_administrador(pacientes, agendamentos, horarios_disponiveis, faq_lista)

# Salva os dados atualizados de pacientes, agendamentos e horários
_b.salva_dados("pacientes.json", "pacientes", pacientes)
_b.salva_dados("agendamentos.json", "agendamentos", agendamentos)
_b.salva_horarios(horarios_disponiveis)

print("Dados salvos. Sistema finalizado com sucesso!")

