class BatizadoOptions:
    NAO_INFORMADO = 0
    ADVENTISTA = 1
    OUTROS = 2
    NAO_BATIZADO = 3

    CHOICES = [
        (NAO_INFORMADO, "Não Informado"),
        (ADVENTISTA, "Adventista"),
        (OUTROS, "Outros"),
        (NAO_BATIZADO, "Não Batizado"),
    ]

    @classmethod
    def get_label(cls, value):
        """Retorna o texto (label)"""
        return dict(cls.CHOICES).get(value, "Sem informação")
