class BatizadoOptions:
    NAO_BATIZADO = 0
    ADVENTISTA = 1
    OUTROS = 2
    CHOICES = [
        (NAO_BATIZADO, "Não Batizado"),
        (ADVENTISTA, "Adventista"),
        (OUTROS, "Outros"),
    ]

    @classmethod
    def get_label(cls, value):
        """Retorna o texto (label)"""
        return dict(cls.CHOICES).get(value, "Sem informação")
