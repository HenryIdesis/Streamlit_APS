import streamlit as st
import requests

# Base URL da API do backend (Flask)
BASE_URL = "http://127.0.0.1:5000"

# Função genérica para fazer requisições ao backend
def fazer_requisicao(endpoint, method="GET", params=None, data=None):
    url = f"{BASE_URL}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url, params=params)
        else:
            st.error("Método HTTP não suportado.")
            return None

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.warning("⚠️ Recurso não encontrado.")
        elif response.status_code == 500:
            st.error("⚠️ Erro interno do servidor.")
        else:
            st.error(f"⚠️ Erro: {response.status_code} - {response.text}")

        return None

    except Exception as e:
        st.error(f"⚠️ Erro de conexão: {e}")
        return None

# Título principal com layout centralizado e espaçamento
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🚲 Empréstimo de Bikes</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #5D6D7E;'>Encontre a bike ideal para você</h4>", unsafe_allow_html=True)
st.write("")

# Sidebar para os filtros e pesquisa
st.sidebar.header("🔍 Filtros de Pesquisa")
if st.sidebar.button("🔍 Buscar Bikes"):

    bikes = fazer_requisicao('bikes')

    # Verifica se há bikes disponíveis e exibe a mensagem de resultado
    if bikes and 'bikes' in bikes:
        st.write("### 🛒 Resultados de busca:")

        # Itera sobre as bikes retornadas pela API e exibe os detalhes em cards
        for bike in bikes['bikes']:
            if 'marca' in bike and 'modelo' in bike:
                # Exibe cada bike em uma estrutura de card para visualização clean
                st.markdown(
                    f"""
                    <div style='border: 1px solid #E0E0E0; padding: 15px; border-radius: 10px; margin-bottom: 10px; background-color: #F9F9F9;'>
                        <h4>Marca: {bike['marca']}</h4>
                        <p>Modelo: {bike['modelo']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.warning("⚠️ Dados da bike incompletos.")
    else:
        st.warning("⚠️ Nenhuma bike disponível no momento.")
