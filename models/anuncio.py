class Anuncio:
    def __init__(self, id, id_imovel, titulo, descricao, valor, status):
        self.__id = id
        self.__id_imovel = id_imovel
        self.__titulo = titulo
        self.__descricao = descricao
        self.__valor = valor
        self.__status = status

    @property
    def id(self):
        return self.__id

    @property
    def id_imovel(self):
        return self.__id_imovel

    @property
    def titulo(self):
        return self.__titulo

    @property
    def descricao(self):
        return self.__descricao

    @property
    def valor(self):
        return self.__valor

    @property
    def status(self):
        return self.__status

    @id_imovel.setter
    def id_imovel(self, valor):
        if valor <= 0:
            raise ValueError("O ID do imóvel deve ser maior que zero.")
        self.__id_imovel = valor

    @titulo.setter
    def titulo(self, valor):
        if not valor:
            raise ValueError("O título não pode ser vazio.")
        self.__titulo = valor

    @descricao.setter
    def descricao(self, valor):
        if not valor:
            raise ValueError("A descrição não pode ser vazia.")
        self.__descricao = valor

    @valor.setter
    def valor(self, valor):
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        self.__valor = valor

    @status.setter
    def status(self, valor):
        status_validos = ["Ativo", "Pausado", "Encerrado"]
        if valor not in status_validos:
            raise ValueError(
                f"Status inválido. Utilize: {', '.join(status_validos)}."
            )
        self.__status = valor

    def __str__(self):
        return (
            f"Anuncio("
            f"id={self.__id}, "
            f"id_imovel={self.__id_imovel}, "
            f"titulo='{self.__titulo}', "
            f"valor={self.__valor}, "
            f"status='{self.__status}')"
        )