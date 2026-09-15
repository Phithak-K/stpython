import streamlit as st
import requests

st.title("อัตราแลกเปลี่ยนเงินตรา")

# ดึง API Key จาก .streamlit/secrets.toml
api_key = st.secrets["EXCHANGE_API_KEY"]

# ดึงข้อมูลจาก API (ดึงเรทจาก USD หรือสกุลเงินอื่นตามต้องการ)
url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
response = requests.get(url)
data = response.json()
rates = data["conversion_rates"]

# รายการสกุลเงินให้เลือก
ls_rate = ["THB", "JPY", "EUR", "GBP", "AED", "KRW", "CNY", "SGD"]

# กำหนดค่าเริ่มต้น (ค่าแรกจะเป็น THB)
default_currency = ls_rate[0]

# แสดงผลเริ่มต้นก่อน
st.subheader(f"1 USD = {rates[default_currency]:,.2f} {default_currency}")

# กล่องตัวเลือกให้ผู้ใช้เลือกสกุลเงิน
rate = st.selectbox("เลือกสกุลเงินอื่น", ls_rate, index=0)

# แสดงผลตามสกุลเงินที่เลือก
st.write(f"1 USD = {rates[rate]:,.2f} {rate}")