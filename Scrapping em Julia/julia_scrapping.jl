using Gumbo, Cascadia, HTTP
using StringEncodings
using DataFrames, CSV

function extract_text(html_element, lista_textos=[])
    if typeof(html_element) == HTMLText
        text = strip(html_element.text)
        if length(text) != 0
            append!(lista_textos, [text])
            return lista_textos
        end
    else
        for c in html_element.children
            extract_text(c, lista_textos)
        end
    end
    return lista_textos
end

construct_url_unidade(href) =
    "https://uspdigital.usp.br/jupiterweb/jupDisciplinaLista?codcg" *
    String(match(r"(?<=codcg)(.*)(?=tipo=D)", href).match) *
    raw"letra=A-Z&tipo=D"

construct_url_disciplina(a_tag) = "https://uspdigital.usp.br/jupiterweb/" *
                            a_tag.attributes["href"]

acha_codigo_disciplina(url) = String(match(r"(?<=sgldis=)(.*?)(?=(?:&verdis|$))", url).match)



function get_informations(htmldocument, url_disc)
    base_selector = "#layout_conteudo > table:nth-child(41) > tbody > tr:nth-child(4) > td > form > table:nth-child(1) > tbody > tr:nth-child(1) > td"
    codigo_disciplina = acha_codigo_disciplina(url_disc)
    ##-- Dados gerais --##
    s = Selector(base_selector * " > table:nth-child(5)")
    dados_gerais = eachmatch(s, htmldocument.root)
    if length(dados_gerais) == 0
        dados_gerais = ["Não há informação sobre"]
    else
        dados_gerais = dados_gerais[1]
        dados_gerais = extract_text(dados_gerais)
    end
    ##-- Creditos --##
    s = Selector(base_selector * " > table:nth-child(7)")
    creditos = eachmatch(s, htmldocument.root)
    if length(creditos) == 0
        creditos = ["Não há informação sobre"]
    else
        creditos = creditos[1]
        creditos = extract_text(creditos)
    end

    ##-- Objetivo --##
    s = Selector(base_selector * " > table:nth-child(9)")
    objetivo = eachmatch(s, htmldocument.root)
    if length(objetivo) == 0
        objetivo = ["Não há informação sobre"]
    else
        objetivo = objetivo[1]
        objetivo = extract_text(objetivo)
    end


    ##--- Docentes ---##
    s = Selector(
        base_selector *
        " > table:nth-child(10) > tbody > tr:nth-child(2) > td > table",
    )
    docentes = eachmatch(s, htmldocument.root)
    if length(docentes) == 0
        docentes = ["Não há informação sobre"]
    else
        docentes = docentes[1]
        docentes = extract_text(docentes)
    end

    ##--- Programacao --##
    s = Selector(base_selector * " > table:nth-child(11)")
    programacao = eachmatch(s, htmldocument.root)
    if length(programacao) == 0
        programacao = ["Não há informação sobre"]
    else
        programacao = programacao[1]
        programacao = extract_text(programacao)
    end

    ##--- Avaliacao ---##
    s = Selector(
        base_selector *
        " > table:nth-child(12) > tbody > tr > td:nth-child(2) > table",
    )
    avaliacao = eachmatch(s, htmldocument.root)
    if length(avaliacao) == 0
        avaliacao = ["Não há informação sobre"]
    else
        avaliacao = avaliacao[1]
        avaliacao = extract_text(avaliacao)
    end

    ##--- Bibliografia ---##
    s = Selector(base_selector * " > table:nth-child(14)")
    bibliografia = eachmatch(s, htmldocument.root)
    if length(bibliografia) == 0
        bibliografia = ["Não há informação sobre"]
    else
        bibliografia = bibliografia[1]
        bibliografia = extract_text(bibliografia)
    end

    return [
        codigo_disciplina,
        dados_gerais,
        creditos,
        objetivo,
        programacao,
        avaliacao,
        bibliografia,
    ]
end



url = "https://uspdigital.usp.br/jupiterweb/jupColegiadoLista?tipo=D"
#base do jupiter com todas as unidades

r = HTTP.get(url)
h = Gumbo.parsehtml(decode(r.body, enc"ISO-8859-1"))
sele = Selector("a.link_gray")
all_data = eachmatch(sele, h.root)
hrefs = [data.attributes["href"] for data in all_data]
urls = [construct_url_unidade(href) for href in hrefs]
#pega todos as unidades de ensino e cria-se uma lista

df = DataFrame(
    Codigo = String[],
    Dados = Array[],
    Creditos = Array[],
    Objetivo = Array[],
    Programacao = Array[],
    Avaliacao = Array[],
    Bibliografia = Array[],
)


for url in urls
    println("url da unidade: ", url)
    r = HTTP.get(url)
    h = Gumbo.parsehtml(decode(r.body, enc"ISO-8859-1"))
    disciplinas = eachmatch(sele, h.root)
    url_disciplinas = [
        construct_url_disciplina(disc)
        for
        disc in disciplinas if
        occursin("jupDisciplinaLista?", disc.attributes["href"]) == false
    ]
    #pega-se todas as discipinas dentro da unidade de ensino
    for url_disciplina in url_disciplinas
        println("url da url_disciplina: ", url_disciplina)
        r = HTTP.get(url_disciplina)
        h = Gumbo.parsehtml(decode(r.body, enc"ISO-8859-1"))

        lista_infos = get_informations(h, url_disciplina)
        push!(df, lista_infos)
    end
end

unique!(df)

csv_file = "all_data_JupiterWeb.csv"

CSV.write(csv_file, df, writeheader=true)





## Teste ##
teste = urls[46] #POLI
print(teste)
teste = "https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=PCS3623&verdis=1"
r= HTTP.get(teste)
h= Gumbo.parsehtml(decode(r.body, enc"ISO-8859-1"))


disciplinas = eachmatch(sele, h.root)
url_disciplinas = [construct_url_disciplina(disc) for disc in disciplinas
                if occursin("jupDisciplinaLista?", disc.attributes["href"]) == false]
r= HTTP.get(url_disciplinas[2])
r = HTTP.get("https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=SCE021")
h = Gumbo.parsehtml(decode(r.body, enc"ISO-8859-1"))

url = "https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=SCE021"



## Ignoraveis ##

## Objetivo ##

obj = eachmatch(Selector("b:only-child"), objetivo)
texto_obj = eachmatch(Selector("span:only-child.txt_arial_8pt_gray"), objetivo)
obj_pt = []
obj_en = []

for t in texto_obj
    try
        append!(obj_pt, [strip(t[1].text)])
    catch e
        if size(t[1].children, 1) != 0
            append!(obj_en, [strip(t[1][1].text)])
        end
    end
end

## Docentes ##
docentes = eachmatch(Selector(".txt_arial_8pt_gray"), docentes)
docentes = [strip(d.children[1].text) for d in docentes if size(d.children, 1) == 1]

## Programa ##
programas = eachmatch(Selector("span:only-child.txt_arial_8pt_gray"), programacao)
programas_en = []
programas_pt = []

for p in programas
    try
        append!(programas_pt, extract_text(p))
    catch e
        if size(p[1].children, 1) != 0
            append!(programas_en, [strip(p[1][1].text)])
        end
    end
end

## Avaliacao ##
av = eachmatch(Selector("span:only-child.txt_arial_8pt_gray"), avaliacao)
av = [extract_text(p) for p in av]

## Dados Gerais ##
s = Selector("tbody > tr:nth-child(1) > td > b > font > span")
unidade = strip(eachmatch(s, dados_gerais)[1][1].text)
s = Selector( "tbody > tr:nth-child(3) > td > b > font > span")
departamento = strip(eachmatch(s, dados_gerais)[1][1].text)
s = Selector("tbody > tr:nth-child(5) > td > font > span > b")
disciplina = strip(eachmatch(s, dados_gerais)[1][1].text)
s = Selector("tbody > tr:nth-child(6) > td > font > span")
disciplina_en =  strip(eachmatch(s, dados_gerais)[1][1].text)
println("Dados gerais alcançados")


## Creditos ##
creditos_dict = Dict()
for i = 1:4
    s_valor = Selector("tbody > tr:nth-child($i) > td:nth-child(2) > font > span")
    s_nome = Selector("tbody > tr:nth-child($i) > td:nth-child(1)")
    nome = eachmatch(s_nome, creditos)[1]
    try
        s_nome = Selector("font > span > b")
        nome = strip(eachmatch(s_nome, nome)[1][1].text)
    catch e
        s_nome = Selector("b > font > span")
        nome = strip(eachmatch(s_nome, nome)[1][1].text)
    end
    valor = strip(eachmatch(s_valor, creditos)[1][1].text)
    creditos_dict[nome] = valor
end
println("Creditos avaliados")

## Requisitos ##
disc_ex = "https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=PTC3213&verdis=1"
codigo_disciplina = acha_codigo_disciplina(disc_ex)
url_requisitos =
    "https://uspdigital.usp.br/jupiterweb/listarCursosRequisitos?coddis=$codigo_disciplina"
r = HTTP.get(url)
h = Gumbo.parsehtml(decode(r.body, enc"ISO-8859-1"))
println("Requisitos alcançados")