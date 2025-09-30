import os
import json

"""
Limpa a tela do terminal, dependendo do sistema operacional.

No Windows, usa o comando 'cls'.
Em sistemas Unix/Linux/Mac, usa o comando 'clear'.
"""
def limpa_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")

"""
Solicita entrada do usuário até que uma opção válida seja fornecida.

Args:
    mensagem (str): Mensagem a ser exibida ao usuário.
    opcoes_validas (list[str]): Lista de respostas aceitas.

Returns:
    str: A escolha válida do usuário.
"""
def entrada_valida(mensagem: str, opcoes_validas: list[str]) -> str:
    while True:
        escolha = input(mensagem).strip()
        if escolha in opcoes_validas:
            return escolha
        print(f"Opção inválida. Escolha entre: {', '.join(opcoes_validas)}.")

"""
Busca um paciente pelo CPF.

Args:
    cpf (str): CPF a ser pesquisado (11 dígitos).
    pacientes (list[dict]): Lista de pacientes cadastrados.

Returns:
    dict | None: Dados do paciente encontrado ou None se não existir.
"""
def buscar_usuario_por_cpf(cpf: str, pacientes: list[dict]) -> dict | None:
    for u in pacientes:
        if u['cpf'] == cpf:
            return u
    return None

"""
Solicita um CPF e busca o paciente correspondente.

Args:
    pacientes (list[dict]): Lista de pacientes cadastrados.

Returns:
    dict | None: Dados do paciente encontrado ou None se cancelar.
"""
def buscar_usuario_por_cpf_interativo(pacientes: list[dict]) -> dict | None:
    while True:
        cpf = input("Digite o CPF do Paciente (11 dígitos): ").strip()
        if cpf.isdigit() and len(cpf) == 11:
            usuario = buscar_usuario_por_cpf(cpf, pacientes)
            if usuario:
                print(f"\nPaciente encontrado: {usuario['nome']}")
                return usuario  
        print("\nCPF inválido ou não cadastrado. Digite exatamente 11 números.")
        escolha = entrada_valida(
            "\nO que deseja fazer?\n1 - Tentar novamente\n2 - Voltar\nEscolha: ", ["1", "2"])
        if escolha == "1":
            continue
        elif escolha == "2":
            return None

"""
Salva uma lista de dados em um arquivo JSON, associada a uma chave específica.
Se o arquivo já existir, o conteúdo é sobrescrito.

Args:
    arquivo (str): Caminho do arquivo JSON.
    chave (str): Nome da chave em que os dados serão salvos.
    lista (list): Lista de dados a serem armazenados.

"""
def salva_dados(arquivo: str, chave: str, lista: list) -> None:
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump({chave: lista}, f)

"""
Carrega uma lista de dados de um arquivo JSON, usando uma chave específica.
Se o arquivo não existir ou estiver corrompido, retorna uma lista vazia.

Args:
    arquivo (str): Caminho do arquivo JSON.
    chave (str): Nome da chave dentro do JSON cujos dados serão carregados.

Returns:
    list: Lista de dados encontrados na chave ou lista vazia se não existir.
"""
def carrega_dados(arquivo: str, chave: str) -> list:
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Arquivo '{arquivo}' corrompido ou inválido.")
        return []
    else:
        return dados.get(chave, [])
    finally:
        print(f"Tentativa de leitura do '{arquivo}' finalizada.")

#======CADASTRO===================================================================
"""
Cadastra novos pacientes interativamente, solicitando nome, CPF e telefone e salva em 'pacientes.json'.

Args:
    pacientes (list[dict]): Lista atual de pacientes cadastrados.

Returns:
    list[dict]: Lista atualizada de pacientes com os novos registros.
"""
def cadastra_paciente(pacientes: list[dict]) -> list[dict]:
    while True:
        print("=== Cadastro de Paciente ===")
        #validação de dados para nome
        while True:
            nome = input("Digite o nome do paciente: ").strip()
            if not nome or len(nome) < 2 or not nome.replace(" ", "").isalpha():
                print("Nome inválido. Digite pelo menos 2 letras e apenas letras.")
            else:
                break
        #validação de dados para CPF
        while True:
            cpf = input("Digite o CPF do paciente (11 dígitos): ").strip()
            if not cpf.isdigit() or len(cpf) != 11:
                print("CPF inválido. Digite exatamente 11 números.")
                continue
            if any(p["cpf"] == cpf for p in pacientes):
                print("Já existe um paciente com esse CPF. Tente outro.")
                continue
            break
        #validação de dados DDD
        print("Digite o dados para contato via Whatsapp: ")
        while True:
            ddd = input("Digite o DDD (2 dígitos): ").strip()
            if not ddd.isdigit() or not (11 <= int(ddd) <= 99):
                print("DDD inválido. Deve ter 2 dígitos entre 11 e 99.")
            else:
                break
        #validação de dados para número de telefone
        while True:
            numero = input("Digite o número de contato (8 ou 9 dígitos): ").strip()
            if not numero.isdigit() or len(numero) not in [8, 9]:
                print("Número inválido. Digite 8 dígitos (fixo) ou 9 dígitos (celular).")
            else:
                break

        if len(numero) == 9:
            telefone = f"+55 ({ddd}) {numero[:5]}-{numero[5:]}"
        else:
            telefone = f"+55 ({ddd}) {numero[:4]}-{numero[4:]}"

        pacientes.append({"nome": nome, "cpf": cpf, "telefone": telefone})
        salva_dados("pacientes.json", "pacientes", pacientes)
        print("Paciente cadastrado com sucesso!")

        opcao = entrada_valida(
            "\nDeseja cadastrar outro paciente?\n1 - Sim\n2 - Não\nEscolha: ", ["1", "2"])
        if opcao == "2":
            break

    return pacientes

#======AGENDAMENTO/ADMINISTRAÇÃO DE DATAS E HORÁRIOS DISPONÍVEIS===================================================================
"""
Salva os horários disponíveis em um arquivo JSON.

Args:
    horarios (dict): Dicionário de horários disponíveis.
    arquivo (str, opcional): Caminho do arquivo JSON. Default é 'horarios.json'.
"""
def salva_horarios(horarios: dict, arquivo: str = "horarios.json") ->None:
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(horarios, f)

"""
Carrega os horários disponíveis de um arquivo JSON.
Se o arquivo não existir ou estiver corrompido, retorna um dicionário vazio.

Args:
    arquivo (str): Caminho do arquivo JSON.

Returns:
    dict: Dicionário de horários disponíveis ou vazio se não existir ou estiver corrompido.
"""
def carrega_horarios(arquivo: str) -> dict:
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado.")
        return {}  
    except json.JSONDecodeError:
        print(f"Arquivo '{arquivo}' corrompido ou inválido.")
        return {}
    else:
        return dados
    finally:
        print(f"Tentativa de leitura do '{arquivo}' finalizada.")  




# horários válidos (intervalos de 30 min, 08:00 até 18:30)
horarios_validos = [f"{h:02d}:00" for h in range(8, 19)] + [f"{h:02d}:30" for h in range(8, 19)]
"""
Verifica se a hora fornecida está dentro da lista de horários válidos.

Args:
    hora (str): Horário no formato "hh:mm".

Returns:
    bool: True se válido, False caso contrário.
"""
def horario_valido(hora: str) -> bool:
    return hora in horarios_validos

"""
Solicita ao usuário um horário válido (08:00 até 18:30, de 30 em 30 minutos).

Returns:
    str | None: Horário escolhido no formato "hh:mm" ou None se cancelar.
"""
def pedir_horario() -> str | None:
    while True:
        hora = input("Digite o horário desejado: ").strip()
        if hora == "0":
            return None
        if horario_valido(hora):
            return hora
        print("Horário inválido. Use formato hh:mm entre 08:00 e 18:30, apenas de 30 em 30 minutos.")


"""
Verifica se a data fornecida é válida (anos 2025 ou 2026).

Args:
    data (str): Data no formato "dd/mm/aaaa".

Returns:
    bool: True se a data for válida, False caso contrário.
"""
def data_valida(data: str) -> bool:
    if len(data) != 10 or data[2] != "/" or data[5] != "/":
        return False
    if not (data[:2].isdigit() and data[3:5].isdigit() and data[6:].isdigit()):
        return False

    dia, mes, ano = int(data[:2]), int(data[3:5]), int(data[6:])
    if ano not in (2025, 2026):
        return False
    if mes < 1 or mes > 12:
        return False
    #lista que representa a quantidade de dias em cada mês do ano
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return 1 <= dia <= dias_por_mes[mes - 1]


"""
Solicita ao usuário uma data válida no formato dd/mm/aaaa.

Returns:
    str | None: Data válida ou None se cancelar.
"""
def pedir_data() -> str | None:
    while True:
        print("\nDigite a data para agendamento:")
        print("0 - Voltar")
        data = input("Digite a data (dd/mm/aaaa): ").strip()
        if data == "0":
            return None
        if data_valida(data):
            return data
        print("Data inválida. Use formato dd/mm/aaaa e anos 2025 ou 2026.")


"""
Exibe os dias disponíveis com horários cadastrados e permite que o usuário escolha um.

Args:
    horarios_disponiveis (dict): Dicionário de dias e horários cadastrados.

Returns:
    str | None: Dia escolhido no formato "dd/mm/aaaa" ou None se não houver/usuário cancelar.
"""
def escolher_dia_existente(horarios_disponiveis: dict) -> str | None:
    if not horarios_disponiveis:
        print("Nenhum dia cadastrado.")
        return None
    dias = list(horarios_disponiveis.keys())
    while True:
        print("\nDias existentes:")
        for i, d in enumerate(dias, 1):
            print(f"{i}. {d}")
        print("0 - Voltar")

        escolha = input("Escolha o número do dia: ").strip()
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(dias):
            return dias[int(escolha)-1]
        print("Escolha inválida. Digite um número entre 0 e", len(dias))


"""
Gerencia os horários disponíveis: adiciona e remove dias e horários no 'horarios.json' que serão escolhidos pelo paciente para agendar consulta.

Args:
    horarios_disponiveis (dict): Dicionário de horários disponíveis.

Returns:
    dict: Dicionário atualizado de horários disponíveis.
"""
def gerenciar_horarios(horarios_disponiveis: dict) -> dict:
    while True:
        limpa_tela()
        print("=== Gerenciar Horários ===")
        if not horarios_disponiveis:
            print("Nenhum horário cadastrado.")
        else:
            for dia, horas in horarios_disponiveis.items():
                print(f"{dia}: {', '.join(sorted(horas)) if horas else 'Sem horários'}")

        print("\nOpções:")
        print("1. Adicionar dia e horários")
        print("2. Adicionar horário em dia existente")
        print("3. Remover horário de um dia")
        print("4. Remover dia inteiro")
        print("0. Voltar")

        opcao = entrada_valida("Escolha: ", ["0", "1", "2", "3", "4"])

        if opcao == "0":
            break

        elif opcao == "1":
            while True:
                limpa_tela()
                print("=== Adicionar dia e horários ===")
                dia = pedir_data()
                if dia == "0":
                    break
                if dia not in horarios_disponiveis:
                    horarios_disponiveis[dia] = []

                while True:
                    hora = pedir_horario()
                    if hora == "0":
                        break
                    if hora in horarios_disponiveis[dia]:
                        print("Esse horário já existe.")
                    else:
                        horarios_disponiveis[dia].append(hora)
                        print(f"Horário {hora} adicionado em {dia}.")

                    opcao_hora = entrada_valida("Deseja adicionar outro horário?\n1 - Sim\n2 - Não\nEscolha: ", ["1", "2"])
                    if opcao_hora == "2":
                        break
                break

        elif opcao == "2":
            while True:
                limpa_tela()
                print("=== Adicionar horário em dia existente ===")
                dia = escolher_dia_existente(horarios_disponiveis)
                if not dia:
                    break

                if horarios_disponiveis[dia]:
                    print(f"Horários já cadastrados em {dia}: {', '.join(sorted(horarios_disponiveis[dia]))}")
                else:
                    print(f"Nenhum horário cadastrado ainda em {dia}.")

                while True:
                    hora = pedir_horario()
                    if hora == "0":
                        break
                    if hora in horarios_disponiveis[dia]:
                        print("Esse horário já existe.")
                    else:
                        horarios_disponiveis[dia].append(hora)
                        print(f"Horário {hora} adicionado em {dia}.")

                    opcao_hora = entrada_valida("Deseja adicionar outro horário nesse dia?\n1 - Sim\n2 - Não\nEscolha: ", ["1", "2"])
                    if opcao_hora == "2":
                        break
                break

        elif opcao == "3":
            while True:
                limpa_tela()
                print("=== Remover horário de um dia ===")
                dia = escolher_dia_existente(horarios_disponiveis)
                if not dia:
                    break
                if not horarios_disponiveis[dia]:
                    print("Nenhum horário nesse dia.")
                    opcao_dia = entrada_valida("Deseja tentar outro dia?\n1 - Sim\n2 - Não\nEscolha: ", ["1", "2"])
                    if opcao_dia == "2":
                        break
                    else:
                        continue

                while True:
                    print(f"\nHorários em {dia}:")
                    horarios_ordenados = sorted(horarios_disponiveis[dia])
                    for i, h in enumerate(horarios_ordenados, 1):
                        print(f"{i}. {h}")
                    print("0 - Voltar")

                    escolha = input("Escolha o número do horário para remover: ").strip()
                    if escolha == "0":
                        break
                    if escolha.isdigit() and 1 <= int(escolha) <= len(horarios_ordenados):
                        removido = horarios_ordenados[int(escolha) - 1]
                        horarios_disponiveis[dia].remove(removido)
                        print(f"Horário {removido} removido.")

                        opcao_hora = entrada_valida("Deseja remover outro horário nesse dia?\n1 - Sim\n2 - Não\nEscolha: ", ["1", "2"])
                        if opcao_hora == "2":
                            break
                    else:
                        print("Escolha inválida.")

                opcao_dia = entrada_valida("Deseja remover horário de outro dia?\n1 - Sim\n2 - Não\nEscolha: ", ["1", "2"])
                if opcao_dia == "2":
                    break

        elif opcao == "4":
            while True:
                limpa_tela()
                print("=== Remover dia inteiro ===")
                dia = escolher_dia_existente(horarios_disponiveis)
                if not dia:
                    break
                opcao_remover = entrada_valida(f"Tem certeza que deseja remover o dia {dia}?\n1 - Sim\n2 - Não\nEscolha: ", ["1", "2"])
                if opcao_remover == "1":
                    del horarios_disponiveis[dia]
                    print(f"Dia {dia} removido com sucesso.")
                else:
                    print("Remoção cancelada.")

                opcao_dia = entrada_valida("Deseja remover outro dia?\n1 - Sim\n2 - Não\nEscolha: ", ["1", "2"])
                if opcao_dia == "2":
                    break

        salva_horarios(horarios_disponiveis)

    return horarios_disponiveis

"""
Agenda uma consulta para um paciente em dia e horário disponível, que ao ser confirmada vai para 'agendamentos.json' de determinado paciente.
Quando a consulta é agendada, o horario disponivel para determinado dia é retirado dos horários disponíveis.

Args:
    agendamentos (list[dict]): Lista de agendamentos existentes.
    pacientes (list[dict]): Lista de pacientes cadastrados.
    horarios_disponiveis (dict): Dicionário de horários disponíveis por dia.

Returns:
    tuple:
        list[dict]: Lista atualizada de agendamentos.
        dict: Dicionário atualizado de horários disponíveis.
"""
def agendar_consulta_com_horarios(agendamentos: list[dict], pacientes: list[dict], horarios_disponiveis: dict) -> tuple[list[dict], dict]:
    print("=== Agendamento de consulta ===")
    paciente = buscar_usuario_por_cpf_interativo(pacientes)

    if not paciente:
        return agendamentos, horarios_disponiveis

    if not horarios_disponiveis:
        print("Não há horários disponíveis para agendamento.")
        return agendamentos, horarios_disponiveis

    while True:
        print("\nDias disponíveis para agendamento:")
        dias = list(horarios_disponiveis.keys())
        for i, dia in enumerate(dias, 1):
            print(f"{i}. {dia} ({len(horarios_disponiveis[dia])} horários disponíveis)")

        try:
            escolha_dia = int(input("Escolha o número do dia: "))
            if 1 <= escolha_dia <= len(dias): 
                dia_escolhido = dias[escolha_dia - 1]
                if not horarios_disponiveis[dia_escolhido]:
                    print("Não há horários disponíveis neste dia.")
                    return agendamentos
                break
            else:
                print("Opção inválida. Digite um número entre 1 e", len(dias))
        except ValueError:
            print("Entrada inválida. Digite apenas números.")

    while True:
        print(f"\nHorários disponíveis em {dia_escolhido}:")
        for i, hora in enumerate(horarios_disponiveis[dia_escolhido], 1):
            print(f"{i}. {hora}")

        try:
            escolha_hora = int(input("Escolha o número do horário: "))
            if 1 <= escolha_hora <= len(horarios_disponiveis[dia_escolhido]):
                horario_escolhido = horarios_disponiveis[dia_escolhido][escolha_hora - 1]
                break
            else:
                print(f"Opção inválida. Digite um número entre 1 e {len(horarios_disponiveis[dia_escolhido])}.")
        except ValueError:
            print("Entrada inválida. Digite apenas números.")

    data_str = f"{dia_escolhido} {horario_escolhido}"
    for ag in agendamentos:
        if ag["cpf"] == paciente["cpf"] and ag["data"] == data_str:
            print("Já existe uma consulta nesse horário para este paciente.")
            return agendamentos

    agendamentos.append({
        "cpf": paciente["cpf"],
        "nome": paciente["nome"],
        "data": data_str
    })
    salva_dados("agendamentos.json", "agendamentos", agendamentos)

    horarios_disponiveis[dia_escolhido].remove(horario_escolhido)
    salva_horarios(horarios_disponiveis)

    print(f"Consulta agendada para {paciente['nome']} em {data_str}!")
    return agendamentos, horarios_disponiveis

"""
Consulta e exibe os agendamentos de um paciente pelo CPF.

Args:
    agendamentos (list[dict]): Lista de agendamentos.
    pacientes (list[dict]): Lista de pacientes cadastrados.
"""
def consultar_agendamentos(agendamentos: list[dict], pacientes: list[dict]) -> None:
    print("=== Consulta de Agendamento ===")
    paciente = buscar_usuario_por_cpf_interativo(pacientes)
    if not paciente:
        return

    cpf = paciente["cpf"]
    encontrados = [ag for ag in agendamentos if ag["cpf"] == cpf]

    print("\n=== Dados do Paciente ===")
    print(f"Nome: {paciente['nome']}")
    print(f"CPF: {paciente['cpf']}")
    print(f"Telefone/WhatsApp: {paciente['telefone']}")

    print("\n=== Agendamentos ===")
    if not encontrados:
        print("Nenhum agendamento encontrado.")
    else:
        for ag in encontrados:
            if "hora" in ag:
                print(f"- {ag['data']} às {ag['hora']}")
            else:
                print(f"- {ag['data']}")

#======LEMBRETES===================================================================
"""
Permite que o paciente confirme ou cancele seus agendamentos.Case cancele, o horário é retirado do 'agendamentos.json' de determinado cpf e volta aos horários disponíveis. Caso confirme ele continua no agendamento. É uma simulação de envio de lembrete ao paciente para confirmação ou cancelamento de consulta.

Args:
    agendamentos (list[dict]): Lista de agendamentos.
    paciente (dict): Dicionário do paciente.
    horarios_disponiveis (dict): Dicionário de horários disponíveis.
"""
def verificar_lembretes_paciente(agendamentos: list[dict], paciente: dict, horarios_disponiveis: dict) -> None:
    cpf = paciente["cpf"]
    encontrados = [ag for ag in agendamentos if ag["cpf"] == cpf]

    if not encontrados:
        print(f"\nNenhum agendamento encontrado para {paciente['nome']}.")
        return

    agendamentos_restantes = encontrados.copy()

    while agendamentos_restantes:
        print(f"\n=== Agendamentos de {paciente['nome']} ===")
        for i, ag in enumerate(agendamentos_restantes, 1):
            print(f"{i}. {ag['data']}")
        print("0 - Voltar")

        escolha = input("Escolha um agendamento para confirmar/cancelar: ").strip()
        if escolha == "0":
            break
        if not escolha.isdigit() or not (1 <= int(escolha) <= len(agendamentos_restantes)):
            print(f"Escolha inválida. Digite um número entre 0 e {len(agendamentos_restantes)}.")
            continue

        agendamento = agendamentos_restantes[int(escolha)-1]

        decisao = entrada_valida("\nDeseja confirmar ou cancelar este agendamento?\n1 - Confirmar\n2 - Cancelar\n0 - Voltar\nEscolha: ", ["0", "1", "2"])

        if decisao == "1":
            print(f"\nConsulta de {paciente['nome']} confirmada!")
            agendamentos_restantes.remove(agendamento)
        elif decisao == "2":
            print(f"\nConsulta de {paciente['nome']} cancelada.")
            agendamentos.remove(agendamento)
            agendamentos_restantes.remove(agendamento)
            salva_dados("agendamentos.json", "agendamentos", agendamentos)

            dia, hora = agendamento["data"].split(" ")
            if dia in horarios_disponiveis:
                horarios_disponiveis[dia].append(hora)
            else:
                horarios_disponiveis[dia] = [hora]
            salva_horarios(horarios_disponiveis)
        elif decisao == "0":
            continue

        if agendamentos_restantes:
            proximo = entrada_valida(
                "\nDeseja verificar o próximo agendamento? 1 - Sim, 2 - Não: ", ["1", "2"])
            if proximo == "2":
                break

    if not agendamentos_restantes:
        print("\nNão há mais lembretes para verificar.")

#=======FAQ==================================================================
"""
Salva a lista de perguntas e respostas no arquivo JSON.

Args:
    faq_lista (list[dict]): Lista de perguntas e respostas.
    arquivo (str, opcional): Caminho do arquivo JSON.
"""
def salvar_faq(faq_lista: list[dict], arquivo="faq.json") -> None:
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump({"faq": faq_lista}, f)

"""
Carrega o FAQ do arquivo JSON.
Se o arquivo não existir ou estiver corrompido, retorna um dicionário vazio.

Args:
    arquivo (str, opcional): Caminho do arquivo JSON.

Returns:
    list[dict]: Lista de perguntas e respostas.
"""
def carrega_faq(arquivo: str = "faq.json") -> list[dict]:
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo}' não encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Arquivo '{arquivo}' corrompido ou inválido.")
        return []
    else:
        return dados.get("faq", [])
    finally:
        print(f"Tentativa de leitura de '{arquivo}' finalizada.")

"""
Adiciona uma nova pergunta e resposta ao FAQ.

Args:
    faq_lista (list[dict]): Lista atual de perguntas e respostas.

Returns:
    list[dict]: Lista atualizada de perguntas e respostas.
"""
def adicionar_pergunta(faq_lista: list[dict]) -> list[dict]:
    print("=== Adicionar Pergunta ===")
    while True:
        pergunta = input("Digite a pergunta: ").strip()
        if not pergunta:
            print("A pergunta não pode ser vazia. Tente novamente.")
            continue
        if any(item["pergunta"].lower() == pergunta.lower() for item in faq_lista):
            print("Essa pergunta já existe no FAQ. Digite uma diferente.")
            continue
        break

    while True:
        resposta = input("Digite a resposta: ").strip()
        if not resposta:
            print("A resposta não pode ser vazia. Tente novamente.")
            continue
        break

    faq_lista.append({"pergunta": pergunta, "resposta": resposta})
    print("Pergunta adicionada com sucesso!")
    return faq_lista

"""
Edita uma pergunta ou resposta existente no FAQ.

Args:
    faq_lista (list[dict]): Lista de perguntas e respostas.

Returns:
    list[dict]: Lista atualizada após edição.
"""
def editar_pergunta(faq_lista: list[dict]) -> list[dict]:
    print("=== Editar Pergunta ===")
    for i, item in enumerate(faq_lista, 1):
        print(f"{i}. {item['pergunta']}")
    try:
        escolha = int(input("Escolha o número da pergunta para editar: ")) - 1
        item = faq_lista[escolha]
    except (ValueError, IndexError):
        print("Escolha inválida.")
        return faq_lista
    print(f"Pergunta atual: {item['pergunta']}")
    nova_pergunta = input("Digite a nova pergunta (ENTER para manter): ").strip()
    print(f"Resposta atual: {item['resposta']}")
    nova_resposta = input("Digite a nova resposta (ENTER para manter): ").strip()
    if nova_pergunta:
        item["pergunta"] = nova_pergunta
    if nova_resposta:
        item["resposta"] = nova_resposta
    print("Pergunta atualizada.")
    return faq_lista

"""
Remove uma pergunta do FAQ.

Args:
    faq_lista (list[dict]): Lista de perguntas e respostas.

Returns:
    list[dict]: Lista atualizada sem a pergunta removida.
"""
def remover_pergunta(faq_lista: list[dict]) -> list[dict]:
    print("=== Remover Pergunta ===")
    for i, item in enumerate(faq_lista, 1):
        print(f"{i}. {item['pergunta']}")
    try:
        escolha = int(input("Escolha o número da pergunta para remover: ")) - 1
        item = faq_lista.pop(escolha)
        print(f"Pergunta '{item['pergunta']}' removida.")
    except (ValueError, IndexError):
        print("Escolha inválida.")
    return faq_lista

#======MENUS===================================================================
"""
Exibe o menu de perguntas frequentes para o paciente.
O paciente pode visualizar perguntas e respostas já cadastradas.
"""
def menu_faq_paciente()->None:
    faq_lista = carrega_faq()
    if not faq_lista:
        print("Nenhuma pergunta cadastrada.")
        return

    while True:
        print("=== FAQ - Perguntas Frequentes ===")
        for i, item in enumerate(faq_lista, 1):
            print(f"{i}. {item['pergunta']}")
        print("0. Voltar ao Menu Paciente")

        try:
            escolha = int(input("Escolha uma pergunta para ver a resposta: "))
        except ValueError:
            print("Entrada inválida. Digite apenas números.")
            continue

        if escolha == 0:
            break
        elif 1 <= escolha <= len(faq_lista):
            print(f"\n{faq_lista[escolha-1]['pergunta']}")
            print(f"{faq_lista[escolha-1]['resposta']}")
            ver_outra = entrada_valida("Deseja ver outra pergunta? 1 - Sim, 2 - Não: ", ["1", "2"])
            if ver_outra == "2":
                break
        else:
            print(f"Escolha inválida. Digite um número entre 0 e {len(faq_lista)}.")

"""
Exibe o menu administrativo do FAQ.
Permite visualizar, adicionar, editar e remover perguntas e respostas.
As alterações são salvas automaticamente em 'faq.json'.

Args:
    faq_lista (list[dict]): Lista de perguntas e respostas.

Returns:
    list[dict]: Lista atualizada de perguntas e respostas.
"""
def menu_faq_adm(faq_lista: list[dict]) -> list[dict]:
    while True:
        limpa_tela()
        print("=== Gerenciar Menu FAQ ===")
        print("1. Visualizar perguntas e respostas")
        print("2. Adicionar pergunta")
        print("3. Editar pergunta")
        print("4. Remover pergunta")
        print("0. Voltar ao Menu Administrador")
        escolha = entrada_valida("Escolha: ", ["0", "1", "2", "3", "4"])
        
        if escolha == "0":
            limpa_tela()
            break
        elif escolha == "1":
            limpa_tela()
            if not faq_lista:
                print("Nenhuma pergunta cadastrada.")
            else:
                print("=== Perguntas e Respostas ===")
                for i, item in enumerate(faq_lista, 1):
                    print(f"{i}. Pergunta: {item['pergunta']}")
                    print(f"   Resposta: {item['resposta']}\n")
            input("\nPressione ENTER para voltar...")

        elif escolha == "2":
            limpa_tela()
            while True:
                faq_lista = adicionar_pergunta(faq_lista)
                salvar_faq(faq_lista)
                ver_outra = entrada_valida("Deseja adicionar outra pergunta? 1 - Sim, 2 - Não: ", ["1", "2"])
                if ver_outra == "2":
                    break

        elif escolha == "3":
            limpa_tela()
            while True:
                faq_lista = editar_pergunta(faq_lista)
                salvar_faq(faq_lista)
                ver_outra = entrada_valida("Deseja editar outra pergunta? 1 - Sim, 2 - Não: ", ["1", "2"])
                if ver_outra == "2":
                    break

        elif escolha == "4":
            limpa_tela()
            while True:
                faq_lista = remover_pergunta(faq_lista)
                salvar_faq(faq_lista)
                ver_outra = entrada_valida("Deseja remover outra pergunta? 1 - Sim, 2 - Não: ", ["1", "2"])
                if ver_outra == "2":
                    break
    return faq_lista

"""
Menu interativo para pacientes.

Permite que o paciente realizar cadastro, agendamento de consultas, consulta de agendamentos, verificação de lembretes e acesso ao FAQ.

Args:
    pacientes (list[dict]): Lista de pacientes cadastrados.
    agendamentos (list[dict]): Lista de agendamentos existentes.
    horarios_disponiveis (dict): Dicionário de dias e horários disponíveis para agendamento.

Returns:
    tuple:
        list[dict]: Lista atualizada de pacientes após possíveis cadastros.
        list[dict]: Lista atualizada de agendamentos após possíveis alterações.
        dict: Dicionário atualizado de horários disponíveis após possíveis agendamentos ou cancelamentos.
"""
def menu_paciente(pacientes: list[dict], agendamentos: list[dict], horarios_disponiveis: dict) -> tuple[list[dict], list[dict], dict]:
    while True:
        limpa_tela()
        print("=== Menu Paciente ===")
        print("1. Cadastrar paciente")
        print("2. Agendar consulta")
        print("3. Consultar agendamentos")
        print("4. Verificar lembretes / Confirmar ou cancelar consultas")
        print("5. FAQ - Perguntas Frequentes")
        print("0. Voltar ao Menu Principal")
        escolha = entrada_valida("Escolha: ", ["0", "1", "2", "3", "4", "5"])

        if escolha == "0":
            limpa_tela()
            break
        elif escolha == "1":
            limpa_tela()
            pacientes = cadastra_paciente(pacientes)
            input("\nPressione Enter para continuar...")
        elif escolha == "2":
            limpa_tela()
            agendamentos, horarios_disponiveis = agendar_consulta_com_horarios(agendamentos, pacientes, horarios_disponiveis)
            input("\nPressione Enter para continuar...")
        elif escolha == "3":
            limpa_tela()
            consultar_agendamentos(agendamentos, pacientes)
            input("\nPressione Enter para continuar...")
        elif escolha == "4":
            limpa_tela()
            print("=== Verificar lembretes / Confirmar ou cancelar consultas ===")
            paciente = buscar_usuario_por_cpf_interativo(pacientes)
            if paciente:
                verificar_lembretes_paciente(agendamentos, paciente, horarios_disponiveis)
            input("\nPressione Enter para continuar...")
        elif escolha == "5":
            limpa_tela()
            menu_faq_paciente()
            input("\nPressione Enter para continuar...")
    return pacientes, agendamentos, horarios_disponiveis

"""
Menu interativo para administradores.
Permite que o administrador gerencie os horários disponíveis para consultas e o FAQ do sistema.

Args:
    pacientes (list[dict]): Lista de pacientes cadastrados.
    agendamentos (list[dict]): Lista de agendamentos existentes.
    horarios_disponiveis (dict): Dicionário contendo os dias e horários disponíveis para agendamento.
    faq_lista (list[dict]): Lista de perguntas e respostas do FAQ.

Returns:
    tuple:
        dict: Dicionário atualizado de horários disponíveis após possíveis alterações.
        list[dict]: Lista atualizada de perguntas e respostas do FAQ após possíveis alterações.
"""
def menu_administrador(pacientes: list[dict], agendamentos: list[dict], horarios_disponiveis: dict, faq_lista: list[dict]) -> tuple[dict, list[dict]]:
    while True:
        limpa_tela()
        print("=== Menu Administrador ===")
        print("1. Gerenciar horários")
        print("2. Gerenciar menu FAQ")
        print("0. Voltar ao Menu Principal")
        escolha = entrada_valida("Escolha: ", ["0", "1", "2"])
    
        if escolha == "0":
            limpa_tela()
            break
        elif escolha == "1":
            limpa_tela()
            horarios_disponiveis = gerenciar_horarios(horarios_disponiveis)
            input("\nPressione Enter para continuar...")
        elif escolha == "2":
            limpa_tela()
            faq_lista = menu_faq_adm(faq_lista)
            input("\nPressione Enter para continuar...")
    
    return horarios_disponiveis, faq_lista