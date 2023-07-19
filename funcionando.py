import json
import os
from datetime import datetime

def load_trade_from_file(journal):
    directory = "C:\\Users\\User\\Desktop\\diarios py\\0atualizando"
    files = os.listdir(directory)
    print("Arquivos disponíveis:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    choice = int(input("Escolha um arquivo para carregar ou 0 para voltar: "))
    if choice == 0:
        return
    filename = files[choice - 1]
    with open(os.path.join(directory, filename), "r") as f:
        journal.trades = json.load(f)
        journal.trade_number = max(t["trade_number"] for t in journal.trades)
    print(f"Trades carregados com sucesso de {filename}.")
def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%d/%m/%y')
            return True
        except ValueError:
            return False
def validate_time(time_str):
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
class TradeJournal:

    def __init__(self):
        self.trades = []
        self.trade_number = 0

    def save_trades(self):
        directory = "C:\\Users\\User\\Desktop\\diarios py\\0atualizando"
        files = os.listdir(directory)
        print("Arquivos disponíveis:")
        for i, file in enumerate(files):
            print(f"{i + 1}. {file}")
        choice = int(input("Escolha um arquivo para adicionar os novos trades ou 0 para criar um novo: "))
        if choice == 0:
            filename = input("Digite o nome do novo arquivo: ")
            with open(os.path.join(directory, filename), "w") as f:
                json.dump(self.trades, f, indent=4)
        else:
            filename = files[choice - 1]
            with open(os.path.join(directory, filename), "r") as f:
                existing_trades = json.load(f)
            trade_numbers = [t["trade_number"] for t in existing_trades]
            new_trades = [t for t in self.trades if t["trade_number"] not in trade_numbers]
            combined_trades = existing_trades + new_trades
            with open(os.path.join(directory, filename), "w") as f:
                json.dump(combined_trades, f, indent=4)
        print(f"Trades salvos com sucesso em {filename}.")

    def add_emotional_trade(self):
        self.trade_number += 1
        ativo = input("Ativo: ").upper()
        date = input("Data (dd/mm/aa): ")
        while not validate_date(date):
            print('\33[31mData inválida\33[m')
            date = input('Digite a data novamente no formato dd/mm/aa: ')
        horario = input("Hora (hh:mm): ")
        while not validate_time(horario):
            print('\33[31mHorário inválido\33[m')
            horario = input('Digite o horário novamente no formato hh:mm: ')
        Periodo = input("Manha/Tarde/Noite: ").capitalize()
        gain_value = input("Qual era o valor do gain: ")
        if gain_value:
            gain_value = float(gain_value)
        else:
            gain_value = None
        loss_value = input("Qual era o valor do loss? ")
        if loss_value:
            loss_value = float(loss_value)
        else:
            loss_value = None
        trades_done = int(input(f"Quantos trades já foram feitos no dia {date} no período {Periodo}? "))
        mood = input("Como estavao seu humor? Descreva o dia todo: ")
        last_trade = input("Como foi o último trade? Descreva com detalhes: ")
        result = input("O trade deu loss ou gain? ").capitalize()
        value = float(input("Qual foi o valor? "))
        moved_stop = input("Moveu o stop? (s/n) ").lower()
        new_stop_value = input("Qual era o novo valor do stop movido? ")
        if new_stop_value:
            new_stop_value = float(new_stop_value)
        else:
            new_stop_value = None
        additional_comment = ""
        add_comment = input("Deseja adicionar mais algum comentário? (s/n) ").lower()
        if add_comment == "s":
            additional_comment = input("Digite seu comentário: ")

        trade = {
            "trade_number": self.trade_number,
            "setup_name": "Emocional",
            "mood": mood,
            "last_trade": last_trade,
            "result": result,
            "value": value,
            "moved_stop": moved_stop,
            "additional_comment": additional_comment,
            "date": date,
            "horario": horario,
            "ativo": ativo,
            "Periodo": Periodo,
            "trades_done": trades_done,
            "gain_value": gain_value,
            "loss_value": loss_value
        }
        if moved_stop == "s":
            trade["new_stop_value"] = new_stop_value
        self.trades.append(trade)

        save_choice = input("\nDeseja salvar o trade no arquivo? (s/n) ")
        while save_choice.lower() == 's':
            directory = "C:\\Users\\User\\Desktop\\diarios py\\0atualizando"
            files = os.listdir(directory)
            print("\nArquivos disponíveis:")
            for i, file in enumerate(files):
                print(f"{i + 1}. {file}")
            while True:
                choice = input("\nEscolha um arquivo para adicionar o novo trade ou 0 para criar um novo: ")
                if choice.isdigit() or (choice.startswith('-') and choice[1:].isdigit()):
                    choice = int(choice)
                    break
                else:
                    print("Entrada inválida. Digite um número inteiro.")

            if choice == 0:
                filename = input("\nDigite o nome do novo arquivo: ")
                with open(os.path.join(directory, filename), "w") as f:
                    json.dump(self.trades, f, indent=4)
            else:
                filename = files[choice - 1]
                with open(os.path.join(directory, filename), "r") as f:
                    existing_trades = json.load(f)
                trade_numbers = [t["trade_number"] for t in existing_trades]
                new_trades = [t for t in self.trades if t["trade_number"] not in trade_numbers]
                combined_trades = existing_trades + new_trades
                with open(os.path.join(directory, filename), "w") as f:
                    json.dump(combined_trades, f, indent=4)
            print(f"\nTrade salvo com sucesso em {filename}.")
            save_choice = input("\nDeseja salvar o trade em outro arquivo? (s/n) ")

    def add_trade(self, filename=None):
        # Inicialização de variáveis
        trade = {}
        confluences = []
        counter_confluences = []
        directory = "C:\\Users\\User\\Desktop\\diarios py\\0atualizando"

        # Adicionando um novo trade
        print("\nAdicionando um novo trade...")
        self.trade_number += 1
        setup_name = input("Digite o nome do setup: ").capitalize()

        if setup_name == "Emocional":
            self.add_emotional_trade()
        else:
            # Informações básicas do trade
            print("\nInformações básicas do trade:")
            trade_type = input("É continuidade ou reversão? ").capitalize()
            date = input("Data (dd/mm/aa): ")
            while not validate_date(date):
                print('\33[31mData inválida\33[m')
                date = input('Digite a data novamente no formato dd/mm/aa: ')

            horario = input("Hora (hh:mm): ")
            while not validate_time(horario):
                print('\33[31mHorário inválido\33[m')
                horario = input('Digite o horário novamente no formato hh:mm: ')

            ativo = input("Ativo: ").upper()
            Periodo = input("Manha/Tarde/Noite: ").capitalize()

            # Informações sobre o mercado
            print("\nInformações sobre o mercado:")
            estado_macro_mercado = input("Qual o estado macro do mercado: ").capitalize()
            estado_intraday_mercado = input("Qual o estado intraday do mercado: ").capitalize()
            market_region = input("Região macro (Alta/Meio/Baixo): ").capitalize()
            intraday_region = input("Em que região intraday o mercado se encontra na hora do trade? ").capitalize()

            # Adicionando confluências
            print("\nAdicionando confluências:")
            n = 1
            while True:
                confluence = input(f"Confluencia {n} ou 'fim' para terminar: ").upper()
                while len(confluence) < 2 and confluence.lower() != 'fim':
                    print('Confluência inválida. Digite mais de um caractere.')
                    confluence = input(f"Confluencia {n} ou 'fim' para terminar: ").upper()

                if confluence.lower() == "fim":
                    break

                if confluence in ["M9", "M20", "M50", "M80", "M200"]:
                    inclination = input(
                        f"A {confluence}: está inclinada? (1. flat, 2. pouco inclinada, 3. muito inclinada, 0. deixar em branco) ")
                    while inclination not in ["1", "2", "3", "0"]:
                        print("Entrada inválida. Escolha entre 1, 2, 3 ou 0 para deixar em branco.")
                        inclination = input(
                            f"A {confluence}: está inclinada? (1. flat, 2. pouco inclinada, 3. muito inclinada, 0. deixar em branco) ")
                    if inclination == "1":
                        inclination = "flat"
                    elif inclination == "2":
                        inclination = "pouco inclinada"
                    elif inclination == "3":
                        inclination = "muito inclinada"
                    else:
                        inclination = ""
                    if inclination:
                        confluence += f" (Inclinação: {inclination})"

                tf_choice = input(f"Deseja adicionar {confluence} por TF ou Localidade? (1.TF, 2.Onde ocorreu?): ")
                if tf_choice == '1':
                    period = input(f"Qual período se encontra a {confluence}? ").upper()
                    confluence += f" ({period})"
                elif tf_choice == '2':
                    repeat_location = input(f"Onde a confluência {confluence} ocorreu? ")
                    confluence += f" ({repeat_location})"

                add_attempt = input(f"Deseja adicionar qual o numero da tentativa? (s/n): ")
                if add_attempt.lower() == 's':
                    attempt_number = input(f"Qual o número da tentativa? (deixe em branco se não houver tentativa): ")
                    if attempt_number:
                        confluence += f" (Tentativa {attempt_number})"

                validate_choice = input(f"A confluência '{confluence}' está correta? (s/n): ")
                if validate_choice.lower() == 'n':
                    continue
                else:
                    n += 1

                confluences.append(confluence)

            trade["confluences"] = confluences

            # Adicionando confluências contrárias
            print("\nAdicionando confluências contrárias:")
            n = 1
            while True:
                counter_confluence = input(f"\033[91mConfluência contra {n}\033[0m ou 'fim' para terminar: ")
                while len(counter_confluence) < 2 and counter_confluence.lower() != 'fim':
                    print('Confluência inválida. Digite mais de um caractere.')
                    counter_confluence = input(f"\033[91mConfluência contra {n}\033[0m ou 'fim' para terminar: ")

                if counter_confluence.lower() == "fim":
                    break

                tf_choice = input(
                    f"Deseja adicionar {counter_confluence} por TF ou Localidade? (1.TF, 2.Onde ocorreu?): ")
                if tf_choice == '1':
                    period = input(f"Qual período se encontra a {counter_confluence}? ").upper()
                    counter_confluence += f" ({period})"
                elif tf_choice == '2':
                    repeat_location = input(f"Onde a confluência {counter_confluence} ocorreu? ")
                    counter_confluence += f" ({repeat_location})"

                add_attempt = input(f"Deseja adicionar qual o numero da tentativa? (s/n): ")
                if add_attempt.lower() == 's':
                    attempt_number = input(f"Qual o número da tentativa? (deixe em branco se não houver tentativa): ")
                    if attempt_number:
                        counter_confluence += f" (Tentativa {attempt_number})"

                validate_choice = input(f"A confluência '{counter_confluence}' está correta? (s/n): ")
                if validate_choice.lower() == 'n':
                    continue
                else:
                    n += 1

                counter_confluences.append(counter_confluence)

            trade["counter_confluences"] = counter_confluences

            # Informações sobre o resultado do trade
            print("\nInformações sobre o resultado do trade:")
            result = input("Foi gain, loss ou 0x0? ").capitalize()
            trade_type = input("Foi compra ou venda? ")
            gain_target = str(input("Qual a ideia inicial das saidas? "))
            loss_target = float(input("Qual o valor inicial do loss? "))

            if result == "0x0":
                after_result = input("Depois foi no alvo ou estopou? ")
                after_coment = input("Comentarios: ")

            if result == "Gain":
                on_target = input("Foi no alvo? (s/n) ")
                if on_target.lower() == "s":
                    on_target_count = 1
                else:
                    on_target_count = 0
                trade["on_target"] = on_target
                trade["on_target_count"] = on_target_count
                conduction_description = input("Descreva a condução (deixe em branco se não quiser adicionar): ")
                trade["conduction_description"] = conduction_description
                gain_value = float(input("Qual foi o valor do gain? "))
                moved_stop = input("Você moveu o stop? (s/n) ")
                if moved_stop.lower() == 's':
                    stop_reason = input("Foi emocional ou técnico? ")
                    new_stop_value = input("Qual o novo valor do stop movido? ")
                    trade["new_stop_value"] = new_stop_value
                    stop_description = input("Descreva como foi: ")
                    trade["moved_stop"] = moved_stop
                    trade["stop_reason"] = stop_reason
                    trade["stop_description"] = stop_description

            if result == "Loss":
                descricao_loss = input("descreva o Loss: ")
                loss_value = float(input("Qual foi o valor do loss? "))
                moved_stop = input("Você moveu o stop? (s/n) ")
                if moved_stop.lower() == 's':
                    stop_reason = input("Foi emocional ou técnico? ")
                    stop_description = input("Descreva como foi essa mexida: ")
                    trade["moved_stop"] = moved_stop
                    trade["stop_reason"] = stop_reason
                    trade["stop_description"] = stop_description

            # Adicionando informações ao dicionário de trades
            trade["trade_number"] = self.trade_number
            trade["setup_name"] = setup_name
            trade["date"] = date
            trade["horario"] = horario
            trade["ativo"] = ativo
            trade["Periodo"] = Periodo
            trade["estado_macro_mercado"] = estado_macro_mercado
            trade["estado_intraday_mercado"] = estado_intraday_mercado
            trade["market_region"] = market_region
            trade["intraday_region"] = intraday_region
            trade["confluences"] = confluences
            trade["result"] = result
            trade["gain_target"] = gain_target
            trade["loss_target"] = loss_target
            trade["trade_type"] = trade_type
            if result == "0x0":
                trade["after_result"] = after_result
                trade["after_coment"] = after_coment

            if result == "Gain":
                trade["gain_value"] = gain_value

            if result == "Loss":
                trade["descricao_loss"] = descricao_loss
                trade["loss_value"] = loss_value

            self.trades.append(trade)

            # Salvando o trade
            print("\nSalvando o trade...")
            save_choice = input("\nDeseja salvar o trade no arquivo? (s/n) ")
            while save_choice.lower() not in ['s', 'n']:
                print("Entrada inválida. Digite 's' para salvar ou 'n' para não salvar.")
                save_choice = input("\nDeseja salvar o trade no arquivo? (s/n) ")

            while save_choice.lower() == 's':
                files = os.listdir(directory)
                print("\nArquivos disponíveis:")
                for i, file in enumerate(files):
                    print(f"{i + 1}. {file}")
                while True:
                    choice = input("\nEscolha um arquivo para adicionar o novo trade ou 0 para criar um novo: ")
                    if choice.isdigit() or (choice.startswith('-') and choice[1:].isdigit()):
                        choice = int(choice)
                        break
                    else:
                        print("Entrada inválida. Digite um número inteiro.")

                if choice == 0:
                    filename = input("\nDigite o nome do novo arquivo: ")
                    with open(os.path.join(directory, filename), "w") as f:
                        json.dump(self.trades, f, indent=4)
                else:
                    filename = files[choice - 1]
                    with open(os.path.join(directory, filename), "r") as f:
                        existing_trades = json.load(f)
                    trade_numbers = [t["trade_number"] for t in existing_trades]
                    new_trades = [t for t in self.trades if t["trade_number"] not in trade_numbers]
                    combined_trades = existing_trades + new_trades
                    with open(os.path.join(directory, filename), "w") as f:
                        json.dump(combined_trades, f, indent=4)
                print(f"\nTrade salvo com sucesso em {filename}.")
                save_choice = input("\nDeseja salvar o trade em outro arquivo? (s/n) ")
                while save_choice.lower() not in ['s', 'n']:
                    print("Entrada inválida. Digite 's' para salvar ou 'n' para não salvar.")
                    save_choice = input("\nDeseja salvar o trade em outro arquivo? (s/n) ")

    def view_trades(self):
        for trade in self.trades:
            print(f"\n\33[34m{trade['trade_number']}º Trade\33[m")
            print(f"Setup: {trade['setup_name']}")
            print(f"Data: {trade['date']}")
            print(f"Ativo: {trade['ativo']}")
            print(f"Horário: {trade['horario']}")
            if 'estado_macro_mercado' in trade:
                print(f"Situação macro do mercado: {trade['estado_macro_mercado']}")
            if 'estado_intraday_mercado' in trade:
                print(f"Situação intraday do mercado: {trade['estado_intraday_mercado']}")
            if 'market_region' in trade:
                print(f"Região do mercado: {trade['market_region']}")
            if 'intraday_region' in trade:
                print(f"Região intraday do mercado: {trade['intraday_region']}")
            if 'confluences' in trade:
                print(f"Confluências: {', '.join(trade['confluences'])}")
            if 'counter_confluences' in trade:
                print("Confluências CONTRA:")
                for confluence in trade["counter_confluences"]:
                    print(confluence)
            if 'result' in trade:
                print(f"Resultado: {trade['result']}", end="")
                if trade["result"] == "0x0":
                    if 'after_result' in trade:
                        print(f"\nDepois: {trade['after_result']}", end="")
                    if 'after_coment' in trade:
                        print(f"\nComentários: {trade['after_coment']}", end="")
                if trade["result"] == "Gain":
                    if 'on_target' in trade:
                        print(f"\nFoi no alvo? {trade['on_target']}", end="")
                    if 'conduction_description' in trade:
                        print(f"\nDescrição da condução: {trade['conduction_description']}", end="")
                    if 'gain_value' in trade:
                        print(f"\nValor do Gain: {trade['gain_value']}", end="")
                    if 'moved_stop' in trade and trade["moved_stop"].lower() == 's':
                        if 'stop_reason' in trade:
                            print(f"\nRazão da movimentação do stop: {trade['stop_reason']}", end="")
                        if 'new_stop_value' in trade:
                            print(f"\nNovo valor do stop movido: {trade['new_stop_value']}", end="")
                        if 'stop_description' in trade:
                            print(f"\nDescrição da movimentação do stop: {trade['stop_description']}", end="")
                if trade["result"] == "Loss":
                    if 'descricao_loss' in trade:
                        print(f"\nDescrição Loss: {trade['descricao_loss']}", end="")
                    if 'loss_value' in trade:
                        print(f"\nValor do Loss: {trade['loss_value']}", end="")
                    if 'moved_stop' in trade and trade["moved_stop"].lower() == 's':
                        if 'stop_reason' in trade:
                            print(f"\nRazão da movimentação do stop: {trade['stop_reason']}", end="")
                        if 'stop_description' in trade:
                            print(f"\nDescrição da movimentação do stop: {trade['stop_description']}", end="")
            if 'gain_target' in trade:
                print(f"\nAlvo de gain financeiro: {trade['gain_target']}")
            if 'loss_target' in trade:
                print(f"Alvo do loss financeiro: {trade['loss_target']}")
            if 'trade_type' in trade:
                print(f"Tipo de trade: {trade['trade_type']}")

    def delete_trade(self, filename=None):
        while True:
            print("\nTrades:")
            for trade in self.trades:
                print(
                    f"{trade['trade_number']}. Data: {trade['date']}, Ativo: {trade['ativo']}, Resultado: {trade['result']}")
            choice = input("\nDigite o número do trade que deseja excluir ou 'v' para voltar: ")
            if choice.lower() == "v":
                break
            choice = int(choice)
            trade_to_delete = None
            for trade in self.trades:
                if trade["trade_number"] == choice:
                    trade_to_delete = trade
                    break
            if trade_to_delete is not None:
                self.trades.remove(trade_to_delete)
                print(f"\nTrade {choice} excluído com sucesso.")

                save_choice = input("\nDeseja salvar as alterações no arquivo? (s/n) ")
                if save_choice.lower() == 's':
                    if filename is None:
                        directory = "C:\\Users\\User\\Desktop\\diarios py\\0atualizando"
                        files = os.listdir(directory)
                        print("\nArquivos disponíveis:")
                        for i, file in enumerate(files):
                            print(f"{i + 1}. {file}")
                        choice = int(input("\nEscolha um arquivo para salvar as alterações ou 0 para criar um novo: "))
                        if choice == 0:
                            filename = input("\nDigite o nome do novo arquivo: ")
                            with open(os.path.join(directory, filename), "w") as f:
                                json.dump(self.trades, f, indent=4)
                        else:
                            filename = files[choice - 1]
                            with open(os.path.join(directory, filename), "w") as f:
                                json.dump(self.trades, f, indent=4)
                        print(f"\nAlterações salvas com sucesso em {filename}.")
                    else:
                        directory = "C:\\Users\\User\\Desktop\\diarios py\\0atualizando"
                        with open(os.path.join(directory, filename), "w") as f:
                            json.dump(self.trades, f, indent=4)
                        print(f"\nAlterações salvas com sucesso em {filename}.")
            else:
                print(f"\nTrade {choice} não encontrado.")

    def hit_rate(self):
        gains = sum(1 for trade in self.trades if trade["result"] == "Gain")
        losses = sum(1 for trade in self.trades if trade["result"] == "Loss")
        zero_zero = sum(1 for trade in self.trades if trade["result"] == "0x0")
        total_trades = len(self.trades)
        hit_rate = gains / total_trades
        print(f"\33[32mGains: {gains}\33[m")
        print(f"\33[31mLosses: {losses}\33[m")
        print(f"\33[33m0x0: {zero_zero}\33[m")
        print(f"Total de trades: {total_trades}")
        return hit_rate

    def average_return(self):
        gains = sum(trade["gain_value"] for trade in self.trades if trade["result"] == "Gain")
        losses = sum(trade["loss_value"] for trade in self.trades if trade["result"] == "Loss")
        total_trades = len(self.trades)
        average_return = (gains - losses) / total_trades
        print(f"\33[32mGanhos totais: R${gains:.2f}\33[m")
        print(f"\33[31mPerdas totais: R${losses:.2f}\33[m")
        if average_return >= 0:
            print(f"\33[32mRetorno médio por trade: R${average_return:.2f}\33[m")
        else:
            print(f"\33[31mRetorno médio por trade: R${average_return:.2f}\33[m")
        return average_return

    def performance_by_setup(self):
        setups = {}
        for trade in self.trades:
            setup_name = trade["setup_name"]
            if setup_name not in setups:
                setups[setup_name] = {"trades": [], "gains": 0, "losses": 0, "total_trades": 0}
            setups[setup_name]["trades"].append(trade)
            setups[setup_name]["total_trades"] += 1
            if trade["result"] == "Gain":
                setups[setup_name]["gains"] += 1
            elif trade["result"] == "Loss":
                setups[setup_name]["losses"] += 1

        while True:
            print("\nSetups:")
            for i, (setup_name, data) in enumerate(setups.items()):
                print(f"{i + 1}. {setup_name} (Taxa de acerto: {data['gains'] / data['total_trades']:.2%})")
            choice = input("\nEscolha um setup pelo número ou 'v' para voltar: ")
            if choice.lower() == "v":
                break
            choice = int(choice)
            chosen_setup = list(setups.keys())[choice - 1]
            data = setups[chosen_setup]
            filter_choice = input("Deseja filtrar por Gain ou Loss? (g/l/n) ")
            confluence_count = {}
            for trade in data["trades"]:
                if filter_choice.lower() == "g" and trade["result"] != "Gain":
                    continue
                if filter_choice.lower() == "l" and trade["result"] != "Loss":
                    continue
                print(f"\33[34m\n{trade['trade_number']}º Trade\33[m")
                print(f"Data: {trade['date']}")
                print(f"Ativo: {trade['ativo']}")
                print(f"Resultado: {trade['result']}")
                for confluence in trade["confluences"]:
                    if confluence not in confluence_count:
                        confluence_count[confluence] = 0
                    confluence_count[confluence] += 1
            sorted_confluences = sorted(confluence_count.items(), key=lambda x: x[1], reverse=True)
            print("\nConfluências:")
            for i, (confluence, count) in enumerate(sorted_confluences):
                print(f"{i + 1}. {confluence} ({count} ocorrências)")

    def view_trades_by_confluence(self):
        while True:
            confluence_count = {}
            for trade in self.trades:
                if trade["result"] != "Gain":
                    continue
                for confluence in trade["confluences"]:
                    if confluence not in confluence_count:
                        confluence_count[confluence] = 0
                    confluence_count[confluence] += 1
            sorted_confluences = sorted(confluence_count.items(), key=lambda x: x[1], reverse=True)
            print("\nConfluências:")
            for i, (confluence, count) in enumerate(sorted_confluences):
                print(f"{i + 1}. {confluence} ({count} ocorrências)")
            choice = input("\nEscolha uma confluência pelo número ou 'v' para voltar: ")
            if choice.lower() == "v":
                break
            choice = int(choice)
            chosen_confluence = sorted_confluences[choice - 1][0]
            print(f"\nTrades com a confluência '{chosen_confluence}':")
            for trade in self.trades:
                if trade["result"] != "Gain":
                    continue
                if chosen_confluence not in trade["confluences"]:
                    continue
                print(f"\33[34m\n{trade['trade_number']}º Trade\33[m")
                print(f"Data: {trade['date']}")
                print(f"Ativo: {trade['ativo']}")
                print(f"Resultado: {trade['result']}")

    def analisar_gains(self):
        print("\nAnálise de Gains:")
        total_gain = 0
        for trade in self.trades:
            if trade["result"] == "Gain":
                print(f"\n\33[34m{trade['trade_number']}º Trade\33[m")
                print(f"Setup: {trade['setup_name']}")
                print(f"Data e Horário: {trade['date']} {trade['horario']}")
                print(f"Ativo: {trade['ativo']}")
                print(f"Valor do Gain: R${trade['gain_value']:.2f}")
                total_gain += trade["gain_value"]
        print(f"\nGanhos totais: R${total_gain:.2f}")

    def analisar_losses(self):
        total_loss = 0
        ativos = set()
        for trade in self.trades:
            if trade["result"] == "Loss":
                total_loss += trade["loss_value"]
                ativos.add(trade["ativo"])

        while True:
            print("\n1. Para analisar por ativo")
            print("2. Para analisar todos")
            print("3. Para voltar ao menu anterior")
            try:
                choice = int(input("\nEscolha uma opção: "))
            except ValueError:
                print("\nOpção inválida, tente novamente.")
                continue
            if choice == 1:
                while True:
                    print("\nAtivos disponíveis para ver os losses:")
                    for i, ativo in enumerate(ativos):
                        print(f"{i + 1}. {ativo}")
                    try:
                        chosen_ativo_index = int(
                            input("\nDigite o número do ativo que deseja ver os losses ou 0 para voltar: ")) - 1
                    except ValueError:
                        print("\nOpção inválida, tente novamente.")
                        continue
                    if chosen_ativo_index == -1:
                        break
                    if chosen_ativo_index < 0 or chosen_ativo_index >= len(ativos):
                        print("\nOpção inválida, tente novamente.")
                        continue
                    chosen_ativo = list(ativos)[chosen_ativo_index]
                    losses_by_ativo = {}
                    for trade in self.trades:
                        if trade["result"] == "Loss" and trade["ativo"] == chosen_ativo:
                            ativo = trade["ativo"]
                            loss_value = trade["loss_value"]
                            if ativo not in losses_by_ativo:
                                losses_by_ativo[ativo] = 0
                            losses_by_ativo[ativo] += loss_value
                            print(
                                f"\n\033[94mTrade número: {trade['trade_number']}\033[0m, Setup: {trade['setup_name']}, Data: {trade['date']}, Hora: {trade['horario']}")
                            loss_target = trade.get('loss_target', '')
                            print(f"Valor inicial do Loss: R${loss_target:.2f}")
                            print(f"Valor do Loss: R${trade['loss_value']:.2f}")
                            counter_confluences = trade.get('counter_confluences', {})
                            print(f"Confluências contrárias ({len(counter_confluences)}): ", end="")
                            for confluence, count in counter_confluences.items():
                                print(f"{confluence} ({count})", end=", ")
                            moved_stop = trade.get('moved_stop', 'n')
                            if moved_stop.lower() == 's':
                                stop_reason = trade.get('stop_reason', '')
                                stop_description = trade.get('stop_description', '')
                                print(f"\nVocê moveu o stop: {moved_stop}")
                                print(f"Razão: {stop_reason}")
                                print(f"Descrição: {stop_description}")
                    for ativo, loss_value in losses_by_ativo.items():
                        print(f"\n\nAtivo: {ativo}, Valor total de loss: R${loss_value:.2f}")
            elif choice == 2:
                for trade in self.trades:
                    if trade["result"] == "Loss":
                        print(
                            f"\n\033[94mTrade número: {trade['trade_number']}\033[0m, Setup: {trade['setup_name']}, Data: {trade['date']}, Hora: {trade['horario']}")
                        loss_target = trade.get('loss_target', '')
                        print(f"Valor inicial do Loss: R${loss_target:.2f}")
                        print(f"Valor do Loss: R${trade['loss_value']:.2f}")
                        counter_confluences = trade.get('counter_confluences', {})
                        print(f"Confluências contrárias ({len(counter_confluences)}): ", end="")
                        for confluence, count in counter_confluences.items():
                            print(f"{confluence} ({count})", end=", ")
                        moved_stop = trade.get('moved_stop', 'n')
                        if moved_stop.lower() == 's':
                            stop_reason = trade.get('stop_reason', '')
                            stop_description = trade.get('stop_description', '')
                            print(f"\nVocê moveu o stop: {moved_stop}")
                            print(f"Razão: {stop_reason}")
                            print(f"Descrição: {stop_description}")
                print(f"\n\nValor total de todos os losses: R${total_loss:.2f}")
            elif choice == 3:
                break

    def analisar_ativo(self):
        ativos = [t["ativo"] for t in self.trades]
        print("\nAtivos disponíveis:")
        for i, ativo in enumerate(set(ativos)):
            trades = [t for t in self.trades if t["ativo"] == ativo]
            gains = sum(1 for t in trades if t["result"] == "Gain")
            losses = sum(1 for t in trades if t["result"] == "Loss")
            hit_rate = gains / (gains + losses) if (gains + losses) > 0 else 0
            trade_count = len(trades)
            total_gain = sum(t["gain_value"] for t in trades if t["result"] == "Gain")
            total_loss = sum(t["loss_value"] for t in trades if t["result"] == "Loss")
            net_profit = total_gain - total_loss
            print(
                f"{i + 1}. {ativo} (T.A: {hit_rate:.2%}, {trade_count} Trades, Acumulado:R$ {net_profit:.2f})")
        choice = int(input("\nEscolha um ativo: "))
        ativo = list(set(ativos))[choice - 1]
        result_choice = input("\nDeseja visualizar apenas os gains, apenas os losses ou todos? (G/L/T): ")
        trades = [t for t in self.trades if t["ativo"] == ativo]
        if result_choice.lower() == "g":
            trades = [t for t in trades if t["result"] == "Gain"]
        elif result_choice.lower() == "l":
            trades = [t for t in trades if t["result"] == "Loss"]
        confluences = {}
        for trade in trades:
            for confluence in trade["confluences"]:
                if confluence not in confluences:
                    confluences[confluence] = 0
                confluences[confluence] += 1
        print("\nTrades:")
        for trade in trades:
            print(
                f"\nTrade {trade['trade_number']}: {trade['setup_name']}, Data: {trade['date']}, Hora: {trade['horario']}, Resultado: {trade['result']}",
                end="")
            if trade["result"] == "Gain":
                print(f", Valor do Gain: {trade['gain_value']}", end="")
            if trade["result"] == "Loss":
                print(f", Valor do Loss: {trade['loss_value']}", end="")
            if trade["result"] == "0x0":
                print(f", Resultado posterior: {trade['after_result']}", end="")
            print()
            print("Confluências:")
            for confluence in trade["confluences"]:
                print(f"{confluence} ({confluences[confluence]})")

    def analisar_periodo(self, start_date, end_date):
        for trade in self.trades:
            if start_date <= trade["date"] <= end_date:
                print(f"Trade: {trade['setup_name']}, Data: {trade['date']}, Ativo: {trade['ativo']}")
                print(f"Resultado: {trade['result']}", end="")
                if trade["result"] == "Gain":
                    print(f", Valor do Gain: {trade['gain_value']}", end="")
                if trade["result"] == "Loss":
                    print(f", Valor do Loss: {trade['loss_value']}", end="")
                print()

    def edit_trade(self, trade_number):
        trade_to_edit = None
        for trade in self.trades:
            if trade["trade_number"] == trade_number:
                trade_to_edit = trade
                break
        if trade_to_edit is None:
            print(f"Trade número {trade_number} não encontrado.")
            return

        print(f"Nome do setup atual: {trade_to_edit['setup_name']}")
        setup_name = input("Digite o novo nome do setup ou deixe em branco para manter o valor atual: ")
        if setup_name:
            trade_to_edit["setup_name"] = setup_name.capitalize()

        print(f"Data atual: {trade_to_edit['date']}")
        date = input("Digite a nova data ou deixe em branco para manter o valor atual: ")
        if date:
            trade_to_edit["date"] = date

        if 'estado_mercado' in trade_to_edit:
            print(f"Situação do mercado atual: {trade_to_edit['estado_mercado']}")
        else:
            print("A chave 'estado_mercado' não existe no dicionário.")

        print(f"Ativo atual: {trade_to_edit['ativo']}")
        ativo = input("Digite o novo ativo ou deixe em branco para manter o valor atual: ")
        if ativo:
            trade_to_edit["ativo"] = ativo.upper()

        print(f"Período atual: {trade_to_edit['Periodo']}")
        Periodo = input("Digite o novo período (Manhã/Tarde/Noite) ou deixe em branco para manter o valor atual: ")
        if Periodo:
            trade_to_edit["Periodo"] = Periodo.capitalize()

        print(f"Horário atual: {trade_to_edit['horario']}")
        horario = input("Digite o novo horário ou deixe em branco para manter o valor atual: ")
        if horario:
            trade_to_edit["horario"] = horario

        if 'estado_mercado' in trade_to_edit:
            print(f"Situação do mercado atual: {trade_to_edit['estado_mercado']}")
            estado_mercado = input("Digite a nova situação do mercado ou deixe em branco para manter o valor atual: ")
            if estado_mercado:
                trade_to_edit["estado_mercado"] = estado_mercado.capitalize()
        else:
            print("A chave 'estado_mercado' não existe no dicionário.")

        # Adicionando a opção de editar ou adicionar mais confluências
        print(f"Confluências atuais: {', '.join(trade_to_edit['confluences'])}")
        choice = input("Deseja editar as confluências? (s/n) ")
        if choice.lower() == "s":
            confluences = []
            n = 1
            while True:
                confluence = input(f"Confluencia {n} ou 'fim' para terminar: ")
                n += 1
                if confluence == "fim":
                    break
                confluences.append(confluence)
            trade_to_edit["confluences"] = confluences

        print(f"Resultado atual: {trade_to_edit['result']}")
        result = input("Digite o novo resultado (Gain/Loss/0x0) ou deixe em branco para manter o valor atual: ")
        if result:
            trade_to_edit["result"] = result.capitalize()
        if trade_to_edit["result"] == "0x0":
            print(f"Depois atual: {trade_to_edit['after_result']}")
            after_result = input("Digite o novo depois (Alvo/Estopou) ou deixe em branco para manter o valor atual: ")
            if after_result:
                trade_to_edit["after_result"] = after_result.capitalize()

        if trade_to_edit["result"] == "Gain":
            print(f"Descrição do Gain atual: {trade_to_edit['descricao_gain']}")
            descricao_gain = input("Digite a nova descrição do Gain ou deixe em branco para manter o valor atual: ")
            if descricao_gain:
                trade_to_edit["descricao_gain"] = descricao_gain

            print(f"Valor do Gain atual: {trade_to_edit['gain_value']}")
            gain_value = input("Digite o novo valor do Gain ou deixe em branco para manter o valor atual: ")
            if gain_value:
                trade_to_edit["gain_value"] = float(gain_value)

        if trade_to_edit["result"] == "Loss":
            print(f"Descrição do Loss atual: {trade_to_edit['descricao_loss']}")
            descricao_loss = input("Digite a nova descrição do Loss ou deixe em branco para manter o valor atual: ")
            if descricao_loss:
                trade_to_edit["descricao_loss"] = descricao_loss

            print(f"Valor do Loss atual: {trade_to_edit['loss_value']}")
            loss_value = input("Digite o novo valor do Loss ou deixe em branco para manter o valor atual: ")
            if loss_value:
                trade_to_edit["loss_value"] = float(loss_value)

        print(f"Alvo de gain financeiro atual: {trade_to_edit['gain_target']}")
        gain_target = input("Digite o novo alvo de gain financeiro ou deixe em branco para manter o valor atual: ")
        if gain_target:
            trade_to_edit["gain_target"] = str(gain_target)

        print(f"Alvo do loss financeiro atual: {trade_to_edit['loss_target']}")
        loss_target = input("Digite o novo alvo do loss financeiro ou deixe em branco para manter o valor atual: ")
        if loss_target:
            trade_to_edit["loss_target"] = float(loss_target)

        print(f"Tipo de trade atual: {trade_to_edit['trade_type']}")
        trade_type = input("Digite o novo tipo de trade (Compra/Venda) ou deixe em branco para manter o valor atual: ")
        if trade_type:
            trade_to_edit["trade_type"] = trade_type.capitalize()

        print(f"Trade número {trade_number} editado com sucesso.")

journal = TradeJournal()
while True:
    print("\nMenu Principal")
    print("1. Carregar os trades a partir de uma lista")
    print("2. Salvar os trades")
    print("3. Adicionar um trade")
    print("4. Ver os trades")
    print("5. Escolha o tipo da análise")
    print("6. Editar um trade")
    print("7. Remover um trade")
    print("8. Sair")
    action = input("\nEscolha uma opção: ")
    if action == "1":
        load_trade_from_file(journal)
    elif action == "2":
        journal.save_trades()
    elif action == "3":
        journal.add_trade()
    elif action == "4":
        journal.view_trades()
    elif action == "5":
        while True:
            print("\nMenu de Análise")
            print("1. Analisar taxa de acerto")
            print("2. Calcular o retorno médio")
            print("3. Analisar o desempenho por setup")
            print("4. Analisar confluências")
            print("5. Analisar gains")
            print("6. Analisar perdas")
            print("7. Analisar ativo")
            print("8. Analisar período")
            print("0. Retornar ao menu principal")
            dados = input("\nEscolha uma opção: ")
            if dados not in ["1", "2", "3", "4", "5", "6", "7", "8", "0"]:
                print("\nOpção inválida. Tente novamente.")
                continue
            if dados == "1":
                hit_rate = journal.hit_rate()
                print(f"\nTaxa de acerto: {hit_rate:.2%}")
            elif dados == "2":
                average_return = journal.average_return()
                print(f"\nRetorno médio: {average_return:.2f}")
            elif dados == "3":
                journal.performance_by_setup()
            elif dados == "4":
                journal.view_trades_by_confluence()
            elif dados == "5":
                journal.analisar_gains()
            elif dados == "6":
                journal.analisar_losses()
            elif dados == "7":
                journal.analisar_ativo()
            elif dados == "8":
                start_date = input("\nDigite a data inicial (formato AAAA-MM-DD): ")
                end_date = input("Digite a data final (formato AAAA-MM-DD): ")
                journal.analisar_periodo(start_date, end_date)
            elif dados == "0":
                break
    elif action == "6":
        trade_number = int(input("\nDigite o número do trade que deseja editar: "))
        journal.edit_trade(trade_number)
    elif action == "7":
        journal.delete_trade()
    elif action == "8":
        break

