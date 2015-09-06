# coding=utf-8
import random

piadas = [

    """Dois suspeitos de um homicídios foram presos, mas nenhum confessava o crime. O delegado mandou deixar os dois presos por um mês e alimentá-los bem.
Findo o mês, um dos suspeitos havia engordado 5 kg, enquanto o outro manteve o peso. O delegado não teve dúvidas:
"Solta o gordo!"
O escrivão ficou confuso. "Mas por quê, doutor?"
"Porque o que não mata, engorda." """,

    """A menininha conversando com seu pai:
_ Pai, papai!
- O que foi minha filha?
- De onde viemos?
- Filha, o homem é descendente de Adão e Eva.
A menina, um pouco confusa, diz:
- Mas papai, a mamãe me disse que somos descendentes do macaco!
- Olha, querida, é muito simples.Uma coisa é a família da sua mãe, outra é a minha...""",

    """Uma jovem não estava se sentindo bem, com dores estranhas há algum tempo, resolveu procurar um médico.
Após um exame, ele dá a notícia:
- A senhora está com Mal de Chagas!

E ela assustada, pergunta:
- Mal de Chagas? Como é que eu peguei isso?

O médico responde:
- A senhora deve ter sido chupada por um babeiro.
- Filho da mãe!!! - comenta a jovem- Ele me disse que era advogado!""",

    """A faxineira do banco, irada, diz para o gerente:
- Eu estou me demitindo! O senhor não confia em mim!
O gerente, espantado, diz:
- Mas o que é isso, Marina? A senhora trabalha aqui há vinte anos, eu até deixo as chaves do cofre em cima da minha mesa!
- Eu sei! - Diz a faxineira, chorando - Mas nenhuma delas funciona!""",

    """Padre recém chegado na paróquia do interior encontra na estrada uma menina, puxando uma vaca.
E pergunta:
- Onde vai, minha menina ?
- Vou levar a vaca para cruzar com o touro do Seu Zé.
O padre escandalizado, imaginando a cena que a menina iria ver, diz:
- Será que seu pai não poderia fazer isto ?
E ela responde:
- Não. Tem que ser com o touro mesmo ...""",

    """Um mulher, toda boazuda, vai ao médico:
- Doutor, poderia fazer algo por meu marido??  Algo que o fizesse ficar como um touro selvagem!!!!!!!!!!
- É pra já, senhora! Tire a sua roupa!!! E vamos começar pelos chifres....""",

    """A sua vida.""",

    """Um velhinho levanta de madrugada pra mijar, olha pro seu pinto e diz:
- Tá vendo infeliz, quando você precisa eu levanto!""",

    """O garçom fala com o freguês:
- O prato da casa hoje é língua ao molho madeira.
- Não, língua não! Tenho nojo de qualquer coisa que sai da boca de um animal.
E o garçom cínico:
- Então que tal uma omelete?""",

    """E numa cidadezinha do interior, em uma família muito tradicional, filha diz para a mãe:
- Mãe, mamãe....! Meu noivo me seduziu e não sou mais virgem!
- Então corte um limão e chupe.
- E isso vai devolver minha virgindade?
- Não, mas vai fazer sumir esse ar de felicidade que você tem estampado na cara. """,

    """E no supermercado:
- Olha, filho! Uma latinha com o seu nome!
- Eu te odeio, pai!
- Não diga isso, Mucilon.""",

    """Uma perua era a mais nova rica de uma cidade pequena.
Para chamar atenção resolveu decorar toda sua casa com motivos medievais.
Estava terminando de decorar a sala de estar, quando notou que faltavam aquelas bolas de ferro que ficam penduradas nas armaduras de guerra. Desesperada, foi até o antiquário mais próximo, onde foi atendida por um vendedor corcunda.
A mulher, querendo parecer fina e elegante, pergunta gentilmente:
- O senhor tem bolas de ferro????
 Ao que o vendedor respondeu, sem pensar duas vezes:
- Não, é desvio na coluna!""",
]


def get(i=False):
    return piadas[random.randint(0, len(piadas) - 1)]
