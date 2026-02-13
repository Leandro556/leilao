from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Registrar fonte compatível com caracteres acentuados (PT-BR)
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

# Criar o documento
doc = SimpleDocTemplate("Relatorio_Funcionamento.pdf", pagesize=A4,
                        rightMargin=50, leftMargin=50, topMargin=60, bottomMargin=50)

# Estilos de texto
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Justify", alignment=4, fontName="HeiseiMin-W3", fontSize=12, leading=16))
styles.add(ParagraphStyle(name="Title", alignment=1, fontName="HeiseiMin-W3", fontSize=14, leading=18, spaceAfter=20))

conteudo = []

# Cabeçalho simulando papel timbrado
conteudo.append(Paragraph("<b>[NOME DA EMPRESA LTDA]</b><br/>"
                          "CNPJ: 00.000.000/0001-00<br/>"
                          "Endereço: Rua Exemplo, 123 - Cidade/UF<br/><br/>", styles["Title"]))

# Corpo do texto
texto = """
Prezados,

Em atenção à solicitação quanto ao envio do Relatório de Funcionamento, informamos que nossa empresa encontra-se regularmente credenciada, entretanto <b>ainda não iniciamos nossas atividades operacionais</b>.

Até o presente momento <b>não foram realizadas operações ou atendimentos</b>, razão pela qual não há movimentações a serem relatadas neste instante. Ressaltamos, contudo, que <b>estamos em fase final de preparação</b> e prevemos o início efetivo de nossas operações em breve.

Tão logo nossa unidade esteja em funcionamento, encaminharemos o relatório atualizado em papel timbrado e devidamente assinado por nosso representante legal, conforme solicitado.

Colocamo-nos à disposição para quaisquer esclarecimentos adicionais.

Atenciosamente,<br/><br/><br/>

_______________________________________<br/>
[NOME DO REPRESENTANTE LEGAL]<br/>
[Cargo]<br/>
[NOME DA EMPRESA]
"""
conteudo.append(Paragraph(texto, styles["Justify"]))

# Gerar PDF
doc.build(conteudo)
print("PDF 'Relatorio_Funcionamento.pdf' gerado com sucesso!")
