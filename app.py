import streamlit as st
import requests

st.set_page_config(page_title="โปรแกรมอัตราแลกเปลี่ยนเงินตรา")
st.title("โปรแกรมคำนวณอัตราแลกเปลี่ยนเงินตรา")

try:
    API_KEY = st.secrets["EXCHANGE_API_KEY"]
except KeyError:
    st.error("ไม่พบ API Key กรุณาตั้งค่าใน .streamlit/secrets.toml")
    st.stop()

def get_exchange_data(api_key, base_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        res = requests.get(url)
        return res.json()
    except Exception as e:
        return {"result": "error", "error-type": str(e)}

currencies = ["USD", "THB", "EUR", "JPY", "GBP", "CNY", "KRW", "SGD", "AUD"]

col1, col2 = st.columns(2)
with col1:
    from_curr = st.selectbox("จากสกุลเงิน:", currencies, index=currencies.index("USD"))
    amount = st.number_input("จำนวนเงิน:", min_value=0.01, value=100.0, step=1.0)

with col2:
    to_curr = st.selectbox("ไปยังสกุลเงิน:", currencies, index=currencies.index("THB"))

if st.button("คำนวณอัตราแลกเปลี่ยน"):
    data = get_exchange_data(API_KEY, from_curr)
    
    if data.get("result") == "success":
        rates = data.get("conversion_rates", {})
        rate = rates.get(to_curr)
        if rate:
            result = amount * rate
            st.success("คำนวณสำเร็จ")
            st.metric(label=f"แปลงเป็นเงิน {to_curr}", value=f"{result:,.2f} {to_curr}")
            st.write(f"**อัตราแลกเปลี่ยน:** 1 {from_curr} = {rate:,.4f} {to_curr}")
            st.caption(f"อัปเดตข้อมูลล่าสุดเมื่อ: {data.get('time_last_update_utc')}")
        else:
            st.error("ไม่พบสกุลเงินปลายทาง")
    else:
        st.error(f"ดึงข้อมูลไม่สำเร็จ: {data.get('error-type')}")