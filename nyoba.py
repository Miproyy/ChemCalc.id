import streamlit as st
import pandas as pd
import re

# Konfigurasi halaman
st.set_page_config(page_title="Aplikasi Kimia Interaktif", layout="wide")

# ======================== TEMA CERAH ========================
custom_theme = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f0f2f6;
    color: #1f1f1f;
    font-family: "Segoe UI", sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #dddddd;
}
h1, h2, h3, h4, h5, h6 {
    color: #222222;
}
p, span, div, label {
    color: #333333;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #43a047;
}
input, textarea, .stTextInput>div>div>input {
    background-color: #ffffff !important;
    color: #1f1f1f !important;
    border: 1px solid #cccccc !important;
    border-radius: 6px !important;
}
thead, tbody, tr, th, td {
    background-color: #ffffff !important;
    color: #1f1f1f !important;
    border: 1px solid #e0e0e0 !important;
}
div[data-testid="element-hover"]:hover {
    background-color: #e3f2fd !important;
    border-radius: 8px;
}
.stMarkdown {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}
</style>
"""
st.markdown(custom_theme, unsafe_allow_html=True)
# ============================================================

# Data unsur kimia
elements_data = [
    {"symbol": "H",  "name": "Hidrogen",  "atomic_number": 1,  "atomic_mass": 1.008, "category": "nonlogam"},
    {"symbol": "He", "name": "Helium",    "atomic_number": 2,  "atomic_mass": 4.0026, "category": "gas mulia"},
    {"symbol": "Li", "name": "Litium",    "atomic_number": 3,  "atomic_mass": 6.94,  "category": "logam alkali"},
    {"symbol": "Be", "name": "Berilium",  "atomic_number": 4,  "atomic_mass": 9.0122, "category": "logam alkali tanah"},
    {"symbol": "B",  "name": "Boron",     "atomic_number": 5,  "atomic_mass": 10.81, "category": "metaloid"},
    {"symbol": "C",  "name": "Karbon",    "atomic_number": 6,  "atomic_mass": 12.011, "category": "nonlogam"},
    {"symbol": "N",  "name": "Nitrogen",  "atomic_number": 7,  "atomic_mass": 14.007, "category": "nonlogam"},
    {"symbol": "O",  "name": "Oksigen",   "atomic_number": 8,  "atomic_mass": 15.999, "category": "nonlogam"},
    {"symbol": "F",  "name": "Fluorin",   "atomic_number": 9,  "atomic_mass": 18.998, "category": "halogen"},
    {"symbol": "Ne", "name": "Neon",      "atomic_number": 10, "atomic_mass": 20.180, "category": "gas mulia"},
    # Tambahkan data lain jika diperlukan
]

# Warna kategori
category_colors = {
    "nonlogam": "#4FC3F7",
    "gas mulia": "#81D4FA",
    "logam alkali": "#FF8A65",
    "logam alkali tanah": "#FFB74D",
    "metaloid": "#AED581",
    "halogen": "#BA68C8",
}

# Fungsi tampilan beranda
def render_home():
    st.title("🧪 Aplikasi Kimia Interaktif")
    st.markdown("""
    Selamat datang di Aplikasi Kimia Interaktif!  
    Anda dapat melihat **tabel periodik unsur**, menghitung **massa molar senyawa**, dan mempelajari **konsep dasar kimia**.

    Gunakan menu di sidebar untuk memulai.
    """)

# Fungsi tampilan tabel periodik
def render_periodic_table():
    st.title("📘 Tabel Periodik Unsur")
    cols = st.columns(10)
    selected_element = None
    for idx, element in enumerate(elements_data):
        col = cols[idx % 10]
        with col:
            color = category_colors.get(element["category"], "#E0E0E0")
            if st.button(element["symbol"], key=element["symbol"]):
                selected_element = element
            st.markdown(f"<div style='background-color:{color};padding:4px;border-radius:6px;text-align:center;color:black'>{element['name']}</div>", unsafe_allow_html=True)
    if selected_element:
        st.subheader(f"Detail Unsur: {selected_element['name']}")
        st.write(f"**Simbol:** {selected_element['symbol']}")
        st.write(f"**Nomor Atom:** {selected_element['atomic_number']}")
        st.write(f"**Massa Atom:** {selected_element['atomic_mass']} g/mol")
        st.write(f"**Kategori:** {selected_element['category'].capitalize()}")

# Fungsi kalkulasi massa molar
def render_calculator():
    st.title("🧮 Kalkulator Massa Molar")
    formula = st.text_input("Masukkan rumus senyawa (misal: H2O, CO2, C6H12O6):")
    if formula:
        try:
            mass, detail = calculate_molar_mass(formula)
            st.success(f"Massa molar {formula} = {mass:.3f} g/mol")
            with st.expander("🔍 Rincian perhitungan"):
                st.write(detail)
        except ValueError as e:
            st.error(str(e))

# Fungsi menghitung massa molar
def calculate_molar_mass(formula):
    def parse_formula(formula):
        tokens = re.findall(r'([A-Z][a-z]?|\(|\)|\d+)', formula)
        stack = [{}]
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '(':
                stack.append({})
            elif token == ')':
                top = stack.pop()
                i += 1
                count = int(tokens[i]) if i < len(tokens) and tokens[i].isdigit() else 1
                if i < len(tokens) and tokens[i].isdigit():
                    i += 1
                for el, num in top.items():
                    stack[-1][el] = stack[-1].get(el, 0) + num * count
                continue
            elif re.match(r'[A-Z][a-z]?', token):
                element = token
                i += 1
                count = int(tokens[i]) if i < len(tokens) and tokens[i].isdigit() else 1
                if i < len(tokens) and tokens[i].isdigit():
                    i += 1
                stack[-1][element] = stack[-1].get(element, 0) + count
                continue
            else:
                i += 1
        return stack[0]

    counts = parse_formula(formula)
    total_mass = 0
    detail = []
    for el, count in counts.items():
        data = next((e for e in elements_data if e["symbol"] == el), None)
        if not data:
            raise ValueError(f"Unsur tidak dikenal: {el}")
        mass = data["atomic_mass"] * count
        total_mass += mass
        detail.append(f"{el} ({data['atomic_mass']} × {count}) = {mass:.3f}")
    return total_mass, "\n".join(detail)

# Fungsi tampilan informasi kimia dasar
def render_chem_info():
    st.title("📚 Informasi Kimia Dasar")
    st.markdown("""
Berikut beberapa **rumus kimia penting** yang umum dipelajari:

### 1. Massa Molar (Mr)
> Mr = jumlah (massa atom relatif × jumlah atom)

Contoh: H₂O = (2 × 1.008) + (1 × 15.999) = 18.015 g/mol

---

### 2. Konsentrasi Larutan
> M = n / V  
> M: molaritas (mol/L), n: mol zat, V: volume (L)

---

### 3. Hukum Avogadro
> V/n = konstan  
Satu mol gas ideal pada STP = **22.4 liter**

---

### 4. Persamaan Reaksi Kimia
Contoh:  
> CH₄ + 2O₂ → CO₂ + 2H₂O

---

### 5. **Rumus Empiris** (Rumus sederhana)
Contoh: Glukosa → C₆H₁₂O₆  
Rumus empirisnya: **CH₂O**  
(Karena perbandingan 6:12:6 disederhanakan jadi 1:2:1)

---
""")

# Sidebar dan navigasi
st.sidebar.title("🔍 Navigasi")
page = st.sidebar.radio("Pilih Halaman", ("Beranda", "Tabel Periodik", "Kalkulator Kimia", "Informasi Kimia"))

if page == "Beranda":
    render_home()
elif page == "Tabel Periodik":
    render_periodic_table()
elif page == "Kalkulator Kimia":
    render_calculator()
elif page == "Informasi Kimia":
    render_chem_info()
