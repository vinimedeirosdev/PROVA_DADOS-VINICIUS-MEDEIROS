
# 📦 Gestão de Produtos e Embalagens

Este é um aplicativo web desenvolvido com **Streamlit** e **Pandas** para auxiliar na visualização, cadastro e busca de embalagens ideais para produtos, com base em suas dimensões e quantidade.

---

## ✅ Funcionalidades

- **Visualizar Dados**: Consulte a tabela de produtos e embalagens cadastradas.
- **Cadastrar Embalagem**: Adicione novas embalagens informando nome e dimensões (altura, largura, profundidade).
- **Buscar Embalagem Ideal**: Informe o código de um produto e a quantidade desejada; o sistema sugere a embalagem mais adequada.

---

## 🛠️ Tecnologias Utilizadas

- [Streamlit] - Criação de aplicações web de forma rápida.
- [Pandas] - Manipulação e análise de dados.
- [gdown] - Download de arquivos diretamente do Google Drive.

---

## 🚀 Como Executar

1. **Clone o repositório:**

```bash
git clone git@github.com:vinimedeirosdev/PROVA_DADOS-VINICIUS-MEDEIROS.git
cd PROVA_DADOS-VINICIUS-MEDEIROS
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**

```bash
streamlit run main.py
```

---

## 📂 Estrutura do Projeto

```
├── main.py                # Código principal da aplicação
├── requirements.txt      # Dependências
├── README.md             # Este arquivo
└── dados.csv             # Arquivo CSV com os produtos (baixado automaticamente via gdown)
```
