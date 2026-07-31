class FotoImovel:
    def __init__(self, id, id_anuncio, caminho_foto):
        self.__id = id
        self.__id_anuncio = id_anuncio
        self.__caminho_foto = caminho_foto

    @property
    def id(self):
        return self.__id

    @property
    def id_anuncio(self):
        return self.__id_anuncio

    @property
    def caminho_foto(self):
        return self.__caminho_foto

    @id_anuncio.setter
    def id_anuncio(self, valor):
        if valor <= 0:
            raise ValueError("O ID do anúncio deve ser maior que zero.")
        self.__id_anuncio = valor

    @caminho_foto.setter
    def caminho_foto(self, valor):
        if not valor:
            raise ValueError("O caminho da foto não pode ser vazio.")
        self.__caminho_foto = valor

    def __str__(self):
        return (
            f"FotoImovel("
            f"id={self.__id}, "
            f"id_anuncio={self.__id_anuncio}, "
            f"caminho_foto='{self.__caminho_foto}')"
        )