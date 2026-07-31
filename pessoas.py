class ProprietarioRepositorio(RepositorioBase):
    tabela = "Proprietario"
    classe_entidade = Proprietario
    pk = "id_proprietario"
    colunas_inserir = ["nome", "cpf_cnpj", "telefone", "email"]
    nome_exibicao = "Proprietário"
    campo_nome = "nome"
    msg_erro_atualizar = "este CPF/CNPJ já está cadastrado para outro proprietário."
    msg_erro_deletar = "ele possui Imóveis cadastrados em seu nome."


class ClienteRepositorio(RepositorioBase):
    tabela = "Cliente"
    classe_entidade = Cliente
    pk = "id_cliente"
    colunas_inserir = ["nome", "cpf", "telefone", "email"]
    nome_exibicao = "Cliente"
    campo_nome = "nome"
    msg_erro_atualizar = "este CPF já está cadastrado para outro cliente."
    msg_erro_deletar = "ele possui registros de Visitas, Vendas ou Aluguéis vinculados."