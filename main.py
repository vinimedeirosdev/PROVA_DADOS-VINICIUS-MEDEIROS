import streamlit as st
import pandas as pd
import gdown

pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 20)

@st.cache_data
def carregar_dados():
    url = 'https://drive.google.com/uc?id=17U0cPO4r-rnzlZPgTmA-3rAi26HmLTEz'
    arquivo = 'dados.csv'
    gdown.download(url, arquivo, quiet=True)

    df = pd.read_csv(arquivo, sep=';', decimal=',').set_index('Codigo')

    for coluna in ['Quantidade', 'Altura', 'Largura', 'Profundidade']:
        df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

    df['Volume_unitario'] = df['Altura'] * df['Largura'] * df['Profundidade']
    df['Volume_total'] = df['Volume_unitario'] * df['Quantidade']

    return df

def inicializar_caixas():
    if 'df_caixas' not in st.session_state:
        dados_caixas = {
            'Nome': ['Caixa A', 'Caixa B', 'Caixa C', 'Caixa D'],
            'Altura': [20, 30, 20, 8],
            'Largura': [15, 25, 25, 8],
            'Profundidade': [8, 40, 15, 4]
        }
        df_caixas = pd.DataFrame(dados_caixas)
        df_caixas['Volume_total'] = df_caixas['Altura'] * df_caixas['Largura'] * df_caixas['Profundidade']
        st.session_state.df_caixas = df_caixas

def visualizar_dados(df_produtos):
    st.header("Produtos")
    st.dataframe(df_produtos)

    st.header("Embalagens")
    st.dataframe(st.session_state.df_caixas)

    verifica_produtos_estranhos(df_produtos)

def verifica_produtos_estranhos(df_produtos):
    st.header("Produtos Estranhos")

    # Produtos com dados nulos
    produtos_nulos = df_produtos[df_produtos.isnull().any(axis=1)]

    st.subheader("Produtos com dados nulos:")

    if not produtos_nulos.empty:
        st.dataframe(produtos_nulos)
    else:
        st.success("Nenhum produto com dados nulos.")

    st.markdown("---")

    # Estoque negativo
    estoque_negativo = df_produtos[df_produtos['Quantidade'] < 0]

    st.subheader("Produtos com estoque negativo:")

    if not estoque_negativo.empty:
        st.dataframe(estoque_negativo)
    else:
        st.success("Nenhum produto com estoque negativo.")

    st.markdown("---")

    # Quantidade não inteira
    quantidade_nao_inteira = df_produtos[df_produtos['Quantidade'] % 1 != 0]

    st.subheader("Produtos com quantidade não inteira:")

    if not quantidade_nao_inteira.empty:
        st.dataframe(quantidade_nao_inteira)
    else:
        st.success("Todos os produtos possuem quantidade inteira.")

    st.markdown("---")

    # Estoque zerado
    estoque_zerado = df_produtos[df_produtos['Quantidade'] == 0]

    st.subheader("Produtos com estoque zerado:")

    if not estoque_zerado.empty:
        st.dataframe(estoque_zerado)
    else:
        st.success("Nenhum produto com estoque zerado.")

    st.markdown("---")

    # Dimensões inválidas
    dimensoes_invalidas = df_produtos[
        (df_produtos['Altura'].isnull() | (df_produtos['Altura'] <= 0)) |
        (df_produtos['Largura'].isnull() | (df_produtos['Largura'] <= 0)) |
        (df_produtos['Profundidade'].isnull() | (df_produtos['Profundidade'] <= 0))
    ]

    st.subheader("Produtos com dimensões inválidas:")

    if not dimensoes_invalidas.empty:
        st.dataframe(dimensoes_invalidas)
    else:
        st.success("Nenhum produto com dimensões inválidas.")

    st.markdown("---")

    # Códigos duplicados
    duplicados = df_produtos.index.duplicated().sum()

    st.subheader("Produtos com códigos duplicados:")

    if duplicados > 0:
        st.warning(f"Quantidade de códigos duplicados: {duplicados}")
    else:
        st.success("Nenhum código duplicado encontrado.")


def cadastrar_embalagem():
    st.header("Adicionar nova embalagem")

    with st.form("form_embalagem"):
        nome = st.text_input("Nome da Embalagem")
        altura = st.number_input("Altura", min_value=0.0, format="%.2f")
        largura = st.number_input("Largura", min_value=0.0, format="%.2f")
        profundidade = st.number_input("Profundidade", min_value=0.0, format="%.2f")

        enviar = st.form_submit_button("Adicionar Embalagem")

        if enviar:
            if not nome.strip():
                st.error("O nome da embalagem não pode ser vazio.")
            elif any(dim <= 0 for dim in [altura, largura, profundidade]):
                st.error("Todas as dimensões devem ser maiores que 0.")
            else:
                nova_embalagem = {
                    'Nome': nome,
                    'Altura': altura,
                    'Largura': largura,
                    'Profundidade': profundidade,
                    'Volume_total': altura * largura * profundidade
                }
                st.session_state.df_caixas = pd.concat(
                    [st.session_state.df_caixas, pd.DataFrame([nova_embalagem])],
                    ignore_index=True
                )
                st.success(f"Embalagem '{nome}' adicionada com sucesso!")

    st.subheader("Embalagens Cadastradas")
    st.dataframe(st.session_state.df_caixas)

def buscar_embalagem(df_produtos):
    st.header("Encontre a embalagem para seu produto")
    codigo = st.text_input("Código do produto")
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    botao = st.button("Buscar embalagem")

    if botao:
        try:
            codigo_int = int(codigo)
        except ValueError:
            st.error("Código inválido.")
            return

        if codigo_int not in df_produtos.index:
            st.error("Código de produto não encontrado!")
        else:
            produto = df_produtos.loc[codigo_int]
            volume_necessario = produto['Volume_unitario'] * quantidade

            embalagens_possiveis = st.session_state.df_caixas[
                st.session_state.df_caixas['Volume_total'] >= volume_necessario
            ]

            if embalagens_possiveis.empty:
                st.warning("Nenhuma embalagem disponível comporta o volume desse produto com essa quantidade.")
            else:
                embalagem_sugerida = embalagens_possiveis.sort_values('Volume_total').iloc[0]
                st.success(f"Embalagem sugerida: {embalagem_sugerida['Nome']}")
                st.write(f"Dimensões: {embalagem_sugerida['Altura']} x {embalagem_sugerida['Largura']} x {embalagem_sugerida['Profundidade']} cm")
                st.write(f"Volume da embalagem: {embalagem_sugerida['Volume_total']} cm³")
                st.write(f"Volume necessário para o produto: {volume_necessario} cm³")


def main():
    st.title("Gestão de Produtos e Embalagens")

    df_produtos = carregar_dados()
    inicializar_caixas()

    page = st.sidebar.selectbox("Escolha a página", ["Visualizar Dados", "Cadastrar Embalagem", "Buscar Embalagem"])

    if page == "Visualizar Dados":
        visualizar_dados(df_produtos)
    elif page == "Cadastrar Embalagem":
        cadastrar_embalagem()
    elif page == "Buscar Embalagem":
        buscar_embalagem(df_produtos)

if __name__ == "__main__":
    main()
