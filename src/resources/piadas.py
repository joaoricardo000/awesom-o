# coding=utf-8
import random

piadas = [
    """Dois suspeitos de um homicídios foram presos, mas nenhum confessava o crime. O delegado mandou deixar os dois presos por um mês e alimentá-los bem.
Findo o mês, um dos suspeitos havia engordado 5 kg, enquanto o outro manteve o peso. O delegado não teve dúvidas:
"Solta o gordo!"
O escrivão ficou confuso. "Mas por quê, doutor?"
"Porque o que não mata, engorda." """,
]


def get(i=False):
    return piadas[random.randint(0, len(piadas) - 1)]