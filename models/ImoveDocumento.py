class ImovelDocumento:
    def __init__(self, id, id_imovel, id_documento):
        self.__id = id
        self.__id_imovel = id_imovel
        self.__id_documento = id_documento

    @property
    def id(self):
        return self.__id

    @property
    def id_imovel(self):
        return self.__id_imovel

    @property
    def id_documento(self):
        return self.__id_documento

    @id_imovel.setter
    def id_imovel(self, valor):
        if valor <= 0:
            raise ValueError("O ID do imóvel deve ser maior que zero.")
        self.__id_imovel = valor

    @id_documento.setter
    def id_documento(self, valor):
        if valor <= 0:
            raise ValueError("O ID do documento deve ser maior que zero.")
        self.__id_documento = valor

    def __str__(self):
        return (
            f"ImovelDocumento("
            f"id={self.__id}, "
            f"id_imovel={self.__id_imovel}, "
            f"id_documento={self.__id_documento})"
        )