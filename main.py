import streamlit as st
import requests
import qrcode
from io import BytesIO

def get_crypto_price_in_brl(crypto_id):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": crypto_id,
        "vs_currencies": "brl"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  
        data = response.json()
        if crypto_id in data:
            crypto_price = data[crypto_id]["brl"]
            return crypto_price
        else:
            st.error(f"Dados inválidos retornados pela API para {crypto_id}.")
            return None
    except Exception as e:
        st.error(f"Erro ao obter o preço da criptomoeda: {e}")
        return None

def convert_brl_to_crypto(brl_amount, crypto_price):
    if crypto_price > 0:
        return brl_amount / crypto_price
    return 0

def generate_qr_code(crypto_address, crypto_amount, crypto_id):
    crypto_amount_formatted = f"{crypto_amount:.8f}"
    
    if crypto_id == "bitcoin":
        payment_link = f"bitcoin:{crypto_address}?amount={crypto_amount_formatted}"
    elif crypto_id == "ethereum":
        payment_link = f"ethereum:{crypto_address}?amount={crypto_amount_formatted}"
    elif crypto_id == "dogecoin":
        payment_link = f"dogecoin:{crypto_address}?amount={crypto_amount_formatted}"
    else:
        payment_link = f"{crypto_address}"  
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5, 
        border=2,  
    )
    qr.add_data(payment_link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

st.title("BRL para Criptomoedas com QR Code de Pagamento")
st.write("Este aplicativo exibe o preço atual de criptomoedas em Reais (BRL), converte um valor em BRL para a criptomoeda selecionada e gera um QR Code para pagamento.")

st.sidebar.title("Configurações")
crypto_options = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Doge": "dogecoin",
}
selected_crypto = st.sidebar.selectbox(
    "Selecione a criptomoeda:",
    list(crypto_options.keys())
)
crypto_id = crypto_options[selected_crypto]

if "crypto_price" not in st.session_state:
    st.session_state.crypto_price = get_crypto_price_in_brl(crypto_id)

if st.sidebar.button("Atualizar Preço da Criptomoeda"):
    st.session_state.crypto_price = get_crypto_price_in_brl(crypto_id)
    st.sidebar.write("Preço da criptomoeda atualizado!")

if st.session_state.crypto_price:
    st.metric(label=f"Preço do {selected_crypto} (BRL)", value=f"R$ {st.session_state.crypto_price:,.2f}")
else:
    st.warning(f"Não foi possível obter o preço do {selected_crypto}. Clique no botão para tentar novamente.")

brl_amount = st.number_input(
    "Digite o valor em BRL que deseja converter:",
    min_value=0.0,
    value=100.0,
    step=1.0,
    key="brl_amount"
)

if "last_brl_amount" not in st.session_state:
    st.session_state.last_brl_amount = brl_amount

if st.session_state.last_brl_amount != brl_amount:
    st.session_state.crypto_price = get_crypto_price_in_brl(crypto_id)
    st.session_state.last_brl_amount = brl_amount

# Converter BRL para criptomoeda
if st.session_state.crypto_price:
    crypto_amount = convert_brl_to_crypto(brl_amount, st.session_state.crypto_price)
    st.success(f"R$ {brl_amount:,.2f} equivalem a **{crypto_amount:.8f} {selected_crypto}**.")
else:
    st.warning("Não é possível converter o valor sem o preço da criptomoeda.")

crypto_address = st.text_input(
    f"Digite o endereço da sua carteira de {selected_crypto}:",
    placeholder=f"Ex: {'1ABC...' if selected_crypto == 'Bitcoin' else '0x123...'}"
)

if crypto_address and st.session_state.crypto_price:
    st.write(f"### QR Code para Pagamento em {selected_crypto}")
    qr_code = generate_qr_code(crypto_address, crypto_amount, crypto_id)
    st.image(qr_code, caption=f"Pagamento de {crypto_amount:.8f} {selected_crypto}", use_column_width=False, width=200)
elif crypto_address:
    st.warning("Digite um valor em BRL para gerar o QR Code.")
else:
    st.warning(f"Digite o endereço da sua carteira de {selected_crypto} para gerar o QR Code.")