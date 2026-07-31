class ProprietarioRepositorio(RepositorioBase):
    tabela = "Proprietario"
    classe_entidade = Proprietario
    pk = "id_proprietario"
    colunas_inserir = ["nome", "cpf_cnpj", "telefone", "email"]
    nome_exibicao = "Proprietário"
    campo_nome = "nome"
    msg_erro_atualizar = "este CPF/CNPJ já está cadastrado para outro proprietário."
    msg_erro_deletar = "ele possui Imóveis cadastrados em seu nome."