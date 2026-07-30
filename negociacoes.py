class VisitaRepositorio(RepositorioBase):
    tabela = "Visita"
    classe_entidade = Visita
    pk = "id_visita"
    # status_visita tem valor padrão 'Agendada': não é pedido no cadastro,
    # só pode ser alterado depois (Confirmada/Realizada/Cancelada/...)
    colunas_inserir = ["id_cliente", "id_corretor", "id_imovel", "data_visita", "observacoes"]
    colunas_atualizar = ["id_cliente", "id_corretor", "id_imovel", "data_visita", "observacoes", "status_visita"]
    nome_exibicao = "Visita"
    msg_erro_deletar = "há uma restrição de integridade associada a esta visita."

    def listar_detalhado(self):
        sql = """
        SELECT
            v.id_visita, c.nome AS cliente, co.nome AS corretor, i.id_imovel,
            v.data_visita, v.status_visita, v.observacoes
        FROM Visita v
        JOIN Cliente c ON v.id_cliente = c.id_cliente
        JOIN Corretor co ON v.id_corretor = co.id_corretor
        JOIN Imovel i ON v.id_imovel = i.id_imovel
        """
        with Conexao() as db:
            db.cursor.execute(sql)
            return db.cursor.fetchall()

    def _erro_restricao_horario(self, err):
        if "uc_imovel_janela_hora" in str(err):
            return "este imóvel já tem uma visita marcada nesse horário."
        if "uc_corretor_janela_hora" in str(err):
            return "este corretor já tem compromisso nesse horário."
        return "verifique se cliente, corretor e imóvel informados existem."

    def inserir(self, entidade):
        # Sobrescrito porque o cadastro de visita precisa tratar o erro de
        # horário duplicado de forma amigável (RepositorioBase.inserir não
        # captura exceção nenhuma — deixa propagar).
        valores = tuple(getattr(entidade, c) for c in self.colunas_inserir)
        sql = """
        INSERT INTO Visita (id_cliente, id_corretor, id_imovel, data_visita, observacoes)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            with Conexao() as db:
                db.cursor.execute(sql, valores)
                db.commit()
                novo_id = db.ultimo_id_inserido
            print("\n✅ Visita cadastrada com sucesso!")
            return novo_id
        except mysql.connector.errors.IntegrityError as err:
            print(f"\n❌ Não deu para agendar: {self._erro_restricao_horario(err)}")
            return None

    def atualizar(self, id_registro, entidade):
        valores = tuple(getattr(entidade, c) for c in self.colunas_atualizar)
        sql = """
        UPDATE Visita SET id_cliente=%s, id_corretor=%s, id_imovel=%s,
               data_visita=%s, observacoes=%s, status_visita=%s
        WHERE id_visita=%s
        """
        try:
            with Conexao() as db:
                db.cursor.execute(sql, (*valores, id_registro))
                db.commit()
            print("\n✅ Visita atualizada com sucesso!")
        except mysql.connector.errors.IntegrityError as err:
            print(f"\n❌ Erro: {self._erro_restricao_horario(err)}")

class VendaRepositorio(RepositorioBase):
    tabela = "Venda"
    classe_entidade = Venda
    pk = "id_venda"
    colunas_inserir = ["id_cliente", "id_corretor", "id_imovel", "data_venda", "valor_venda"]
    nome_exibicao = "Registro de venda"
    msg_erro_atualizar = "verifique se os IDs do cliente, corretor e imóvel informados existem."
    msg_erro_deletar = "existe um Contrato gerado e ativo para ela."

    def listar_detalhado(self):
        sql = """
        SELECT v.id_venda, c.nome AS cliente, co.nome AS corretor, i.id_imovel,
               v.data_venda, v.valor_venda
        FROM Venda v
        JOIN Cliente c ON v.id_cliente = c.id_cliente
        JOIN Corretor co ON v.id_corretor = co.id_corretor
        JOIN Imovel i ON v.id_imovel = i.id_imovel
        """
        with Conexao() as db:
            db.cursor.execute(sql)
            return db.cursor.fetchall()

class AluguelRepositorio(RepositorioBase):
    tabela = "Aluguel"
    classe_entidade = Aluguel
    pk = "id_aluguel"
    colunas_inserir = ["id_cliente", "id_corretor", "id_imovel", "data_inicio", "valor_aluguel"]
    nome_exibicao = "Registro de aluguel"
    msg_erro_atualizar = "verifique se os IDs do cliente, corretor e imóvel informados existem."
    msg_erro_deletar = "existe um Contrato gerado e ativo para ele."

    def listar_detalhado(self):
        sql = """
        SELECT a.id_aluguel, c.nome AS cliente, co.nome AS corretor, i.id_imovel,
               a.data_inicio, a.valor_aluguel
        FROM Aluguel a
        JOIN Cliente c ON a.id_cliente = c.id_cliente
        JOIN Corretor co ON a.id_corretor = co.id_corretor
        JOIN Imovel i ON a.id_imovel = i.id_imovel
        """
        with Conexao() as db:
            db.cursor.execute(sql)
            return db.cursor.fetchall()

class ContratoRepositorio(RepositorioBase):
    tabela = "Contrato"
    classe_entidade = Contrato
    pk = "id_contrato"
    colunas_inserir = ["id_venda", "id_aluguel", "data_assinatura", "data_inicio", "data_fim", "clausulas"]
    nome_exibicao = "Contrato"
    msg_erro_atualizar = "verifique se os IDs da venda ou do aluguel associados existem."
    msg_erro_deletar = "constam Pagamentos registrados para ele."

class PagamentoRepositorio(RepositorioBase):
    tabela = "Pagamento"
    classe_entidade = Pagamento
    pk = "id_pagamento"
    # status_pagamento tem valor padrão 'Pendente': só é editável depois
    colunas_inserir = ["id_contrato", "valor_pago", "data_pagamento", "data_vencimento", "forma_pagamento"]
    colunas_atualizar = ["id_contrato", "valor_pago", "data_pagamento", "data_vencimento", "forma_pagamento", "status_pagamento"]
    nome_exibicao = "Pagamento"
    msg_erro_atualizar = "o ID de contrato especificado não existe."
    msg_erro_deletar = "há uma restrição de integridade associada a este pagamento."