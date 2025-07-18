import streamlit as st
import re

# =================================================================================
# DATA UNSUR KIMIA
# =================================================================================
# Sumber data: IUPAC, Wikipedia. Massa atom adalah massa atom relatif standar.
ELEMENTS_DATA = {
    'H': {'name': 'Hidrogen', 'number': 1, 'mass': 1.008, 'group': 1, 'period': 1, 'category': 'nonlogam-reaktif'},
    'He': {'name': 'Helium', 'number': 2, 'mass': 4.0026, 'group': 18, 'period': 1, 'category': 'gas-mulia'},
    'Li': {'name': 'Litium', 'number': 3, 'mass': 6.94, 'group': 1, 'period': 2, 'category': 'logam-alkali'},
    'Be': {'name': 'Berilium', 'number': 4, 'mass': 9.0122, 'group': 2, 'period': 2, 'category': 'alkali-tanah'},
    'B': {'name': 'Boron', 'number': 5, 'mass': 10.81, 'group': 13, 'period': 2, 'category': 'metaloid'},
    'C': {'name': 'Karbon', 'number': 6, 'mass': 12.011, 'group': 14, 'period': 2, 'category': 'nonlogam-reaktif'},
    'N': {'name': 'Nitrogen', 'number': 7, 'mass': 14.007, 'group': 15, 'period': 2, 'category': 'nonlogam-reaktif'},
    'O': {'name': 'Oksigen', 'number': 8, 'mass': 15.999, 'group': 16, 'period': 2, 'category': 'nonlogam-reaktif'},
    'F': {'name': 'Fluorin', 'number': 9, 'mass': 18.998, 'group': 17, 'period': 2, 'category': 'nonlogam-reaktif'},
    'Ne': {'name': 'Neon', 'number': 10, 'mass': 20.180, 'group': 18, 'period': 2, 'category': 'gas-mulia'},
    'Na': {'name': 'Natrium', 'number': 11, 'mass': 22.990, 'group': 1, 'period': 3, 'category': 'logam-alkali'},
    'Mg': {'name': 'Magnesium', 'number': 12, 'mass': 24.305, 'group': 2, 'period': 3, 'category': 'alkali-tanah'},
    'Al': {'name': 'Aluminium', 'number': 13, 'mass': 26.982, 'group': 13, 'period': 3, 'category': 'logam-pasca-transisi'},
    'Si': {'name': 'Silikon', 'number': 14, 'mass': 28.085, 'group': 14, 'period': 3, 'category': 'metaloid'},
    'P': {'name': 'Fosfor', 'number': 15, 'mass': 30.974, 'group': 15, 'period': 3, 'category': 'nonlogam-reaktif'},
    'S': {'name': 'Belerang', 'number': 16, 'mass': 32.06, 'group': 16, 'period': 3, 'category': 'nonlogam-reaktif'},
    'Cl': {'name': 'Klorin', 'number': 17, 'mass': 35.45, 'group': 17, 'period': 3, 'category': 'nonlogam-reaktif'},
    'Ar': {'name': 'Argon', 'number': 18, 'mass': 39.948, 'group': 18, 'period': 3, 'category': 'gas-mulia'},
    'K': {'name': 'Kalium', 'number': 19, 'mass': 39.098, 'group': 1, 'period': 4, 'category': 'logam-alkali'},
    'Ca': {'name': 'Kalsium', 'number': 20, 'mass': 40.078, 'group': 2, 'period': 4, 'category': 'alkali-tanah'},
    'Sc': {'name': 'Skandium', 'number': 21, 'mass': 44.956, 'group': 3, 'period': 4, 'category': 'logam-transisi'},
    'Ti': {'name': 'Titanium', 'number': 22, 'mass': 47.867, 'group': 4, 'period': 4, 'category': 'logam-transisi'},
    'V': {'name': 'Vanadium', 'number': 23, 'mass': 50.942, 'group': 5, 'period': 4, 'category': 'logam-transisi'},
    'Cr': {'name': 'Kromium', 'number': 24, 'mass': 51.996, 'group': 6, 'period': 4, 'category': 'logam-transisi'},
    'Mn': {'name': 'Mangan', 'number': 25, 'mass': 54.938, 'group': 7, 'period': 4, 'category': 'logam-transisi'},
    'Fe': {'name': 'Besi', 'number': 26, 'mass': 55.845, 'group': 8, 'period': 4, 'category': 'logam-transisi'},
    'Co': {'name': 'Kobalt', 'number': 27, 'mass': 58.933, 'group': 9, 'period': 4, 'category': 'logam-transisi'},
    'Ni': {'name': 'Nikel', 'number': 28, 'mass': 58.693, 'group': 10, 'period': 4, 'category': 'logam-transisi'},
    'Cu': {'name': 'Tembaga', 'number': 29, 'mass': 63.546, 'group': 11, 'period': 4, 'category': 'logam-transisi'},
    'Zn': {'name': 'Seng', 'number': 30, 'mass': 65.38, 'group': 12, 'period': 4, 'category': 'logam-transisi'},
    'Ga': {'name': 'Galium', 'number': 31, 'mass': 69.723, 'group': 13, 'period': 4, 'category': 'logam-pasca-transisi'},
    'Ge': {'name': 'Germanium', 'number': 32, 'mass': 72.630, 'group': 14, 'period': 4, 'category': 'metaloid'},
    'As': {'name': 'Arsen', 'number': 33, 'mass': 74.922, 'group': 15, 'period': 4, 'category': 'metaloid'},
    'Se': {'name': 'Selenium', 'number': 34, 'mass': 78.971, 'group': 16, 'period': 4, 'category': 'nonlogam-reaktif'},
    'Br': {'name': 'Bromin', 'number': 35, 'mass': 79.904, 'group': 17, 'period': 4, 'category': 'nonlogam-reaktif'},
    'Kr': {'name': 'Kripton', 'number': 36, 'mass': 83.798, 'group': 18, 'period': 4, 'category': 'gas-mulia'},
    'Rb': {'name': 'Rubidium', 'number': 37, 'mass': 85.468, 'group': 1, 'period': 5, 'category': 'logam-alkali'},
    'Sr': {'name': 'Stronsium', 'number': 38, 'mass': 87.62, 'group': 2, 'period': 5, 'category': 'alkali-tanah'},
    'Y': {'name': 'Itrium', 'number': 39, 'mass': 88.906, 'group': 3, 'period': 5, 'category': 'logam-transisi'},
    'Zr': {'name': 'Zirkonium', 'number': 40, 'mass': 91.224, 'group': 4, 'period': 5, 'category': 'logam-transisi'},
    'Nb': {'name': 'Niobium', 'number': 41, 'mass': 92.906, 'group': 5, 'period': 5, 'category': 'logam-transisi'},
    'Mo': {'name': 'Molibdenum', 'number': 42, 'mass': 95.96, 'group': 6, 'period': 5, 'category': 'logam-transisi'},
    'Tc': {'name': 'Teknesium', 'number': 43, 'mass': 98, 'group': 7, 'period': 5, 'category': 'logam-transisi'},
    'Ru': {'name': 'Rutenium', 'number': 44, 'mass': 101.07, 'group': 8, 'period': 5, 'category': 'logam-transisi'},
    'Rh': {'name': 'Rodium', 'number': 45, 'mass': 102.91, 'group': 9, 'period': 5, 'category': 'logam-transisi'},
    'Pd': {'name': 'Paladium', 'number': 46, 'mass': 106.42, 'group': 10, 'period': 5, 'category': 'logam-transisi'},
    'Ag': {'name': 'Perak', 'number': 47, 'mass': 107.87, 'group': 11, 'period': 5, 'category': 'logam-transisi'},
    'Cd': {'name': 'Kadmium', 'number': 48, 'mass': 112.41, 'group': 12, 'period': 5, 'category': 'logam-transisi'},
    'In': {'name': 'Indium', 'number': 49, 'mass': 114.82, 'group': 13, 'period': 5, 'category': 'logam-pasca-transisi'},
    'Sn': {'name': 'Timah', 'number': 50, 'mass': 118.71, 'group': 14, 'period': 5, 'category': 'logam-pasca-transisi'},
    'Sb': {'name': 'Antimon', 'number': 51, 'mass': 121.76, 'group': 15, 'period': 5, 'category': 'metaloid'},
    'Te': {'name': 'Telurium', 'number': 52, 'mass': 127.60, 'group': 16, 'period': 5, 'category': 'metaloid'},
    'I': {'name': 'Iodin', 'number': 53, 'mass': 126.90, 'group': 17, 'period': 5, 'category': 'nonlogam-reaktif'},
    'Xe': {'name': 'Xenon', 'number': 54, 'mass': 131.29, 'group': 18, 'period': 5, 'category': 'gas-mulia'},
    'Cs': {'name': 'Sesium', 'number': 55, 'mass': 132.91, 'group': 1, 'period': 6, 'category': 'logam-alkali'},
    'Ba': {'name': 'Barium', 'number': 56, 'mass': 137.33, 'group': 2, 'period': 6, 'category': 'alkali-tanah'},
    'La': {'name': 'Lantanum', 'number': 57, 'mass': 138.91, 'group': 3, 'period': 6, 'category': 'lantanida'},
    'Ce': {'name': 'Serium', 'number': 58, 'mass': 140.12, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Pr': {'name': 'Praseodimium', 'number': 59, 'mass': 140.91, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Nd': {'name': 'Neodimium', 'number': 60, 'mass': 144.24, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Pm': {'name': 'Prometium', 'number': 61, 'mass': 145, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Sm': {'name': 'Samarium', 'number': 62, 'mass': 150.36, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Eu': {'name': 'Europium', 'number': 63, 'mass': 151.96, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Gd': {'name': 'Gadolinium', 'number': 64, 'mass': 157.25, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Tb': {'name': 'Terbium', 'number': 65, 'mass': 158.93, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Dy': {'name': 'Disprosium', 'number': 66, 'mass': 162.50, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Ho': {'name': 'Holmium', 'number': 67, 'mass': 164.93, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Er': {'name': 'Erbium', 'number': 68, 'mass': 167.26, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Tm': {'name': 'Tulium', 'number': 69, 'mass': 168.93, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Yb': {'name': 'Iterbium', 'number': 70, 'mass': 173.05, 'group': None, 'period': 8, 'category': 'lantanida'},
    'Lu': {'name': 'Lutetium', 'number': 71, 'mass': 174.97, 'group': 4, 'period': 6, 'category': 'lantanida'},
    'Hf': {'name': 'Hafnium', 'number': 72, 'mass': 178.49, 'group': 4, 'period': 6, 'category': 'logam-transisi'},
    'Ta': {'name': 'Tantalum', 'number': 73, 'mass': 180.95, 'group': 5, 'period': 6, 'category': 'logam-transisi'},
    'W': {'name': 'Wolfram', 'number': 74, 'mass': 183.84, 'group': 6, 'period': 6, 'category': 'logam-transisi'},
    'Re': {'name': 'Renium', 'number': 75, 'mass': 186.21, 'group': 7, 'period': 6, 'category': 'logam-transisi'},
    'Os': {'name': 'Osmium', 'number': 76, 'mass': 190.23, 'group': 8, 'period': 6, 'category': 'logam-transisi'},
    'Ir': {'name': 'Iridium', 'number': 77, 'mass': 192.22, 'group': 9, 'period': 6, 'category': 'logam-transisi'},
    'Pt': {'name': 'Platina', 'number': 78, 'mass': 195.08, 'group': 10, 'period': 6, 'category': 'logam-transisi'},
    'Au': {'name': 'Emas', 'number': 79, 'mass': 196.97, 'group': 11, 'period': 6, 'category': 'logam-transisi'},
    'Hg': {'name': 'Raksa', 'number': 80, 'mass': 200.59, 'group': 12, 'period': 6, 'category': 'logam-transisi'},
    'Tl': {'name': 'Talium', 'number': 81, 'mass': 204.38, 'group': 13, 'period': 6, 'category': 'logam-pasca-transisi'},
    'Pb': {'name': 'Timbal', 'number': 82, 'mass': 207.2, 'group': 14, 'period': 6, 'category': 'logam-pasca-transisi'},
    'Bi': {'name': 'Bismut', 'number': 83, 'mass': 208.98, 'group': 15, 'period': 6, 'category': 'logam-pasca-transisi'},
    'Po': {'name': 'Polonium', 'number': 84, 'mass': 209, 'group': 16, 'period': 6, 'category': 'metaloid'},
    'At': {'name': 'Astatin', 'number': 85, 'mass': 210, 'group': 17, 'period': 6, 'category': 'nonlogam-reaktif'},
    'Rn': {'name': 'Radon', 'number': 86, 'mass': 222, 'group': 18, 'period': 6, 'category': 'gas-mulia'},
    'Fr': {'name': 'Fransium', 'number': 87, 'mass': 223, 'group': 1, 'period': 7, 'category': 'logam-alkali'},
    'Ra': {'name': 'Radium', 'number': 88, 'mass': 226, 'group': 2, 'period': 7, 'category': 'alkali-tanah'},
    'Ac': {'name': 'Aktinium', 'number': 89, 'mass': 227, 'group': 3, 'period': 7, 'category': 'aktinida'},
    'Th': {'name': 'Torium', 'number': 90, 'mass': 232.04, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Pa': {'name': 'Protaktinium', 'number': 91, 'mass': 231.04, 'group': None, 'period': 9, 'category': 'aktinida'},
    'U': {'name': 'Uranium', 'number': 92, 'mass': 238.03, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Np': {'name': 'Neptunium', 'number': 93, 'mass': 237, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Pu': {'name': 'Plutonium', 'number': 94, 'mass': 244, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Am': {'name': 'Amerisium', 'number': 95, 'mass': 243, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Cm': {'name': 'Kurium', 'number': 96, 'mass': 247, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Bk': {'name': 'Berkelium', 'number': 97, 'mass': 247, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Cf': {'name': 'Kalifornium', 'number': 98, 'mass': 251, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Es': {'name': 'Einsteinium', 'number': 99, 'mass': 252, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Fm': {'name': 'Fermium', 'number': 100, 'mass': 257, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Md': {'name': 'Mendelevium', 'number': 101, 'mass': 258, 'group': None, 'period': 9, 'category': 'aktinida'},
    'No': {'name': 'Nobelium', 'number': 102, 'mass': 259, 'group': None, 'period': 9, 'category': 'aktinida'},
    'Lr': {'name': 'Lawrensium', 'number': 103, 'mass': 262, 'group': 4, 'period': 7, 'category': 'aktinida'},
    'Rf': {'name': 'Rutherfordium', 'number': 104, 'mass': 267, 'group': 4, 'period': 7, 'category': 'logam-transisi'},
    'Db': {'name': 'Dubnium', 'number': 105, 'mass': 268, 'group': 5, 'period': 7, 'category': 'logam-transisi'},
    'Sg': {'name': 'Seaborgium', 'number': 106, 'mass': 271, 'group': 6, 'period': 7, 'category': 'logam-transisi'},
    'Bh': {'name': 'Bohrium', 'number': 107, 'mass': 272, 'group': 7, 'period': 7, 'category': 'logam-transisi'},
    'Hs': {'name': 'Hassium', 'number': 108, 'mass': 270, 'group': 8, 'period': 7, 'category': 'logam-transisi'},
    'Mt': {'name': 'Meitnerium', 'number': 109, 'mass': 276, 'group': 9, 'period': 7, 'category': 'properti-tak-dikenal'},
    'Ds': {'name': 'Darmstadtium', 'number': 110, 'mass': 281, 'group': 10, 'period': 7, 'category': 'properti-tak-dikenal'},
    'Rg': {'name': 'Roentgenium', 'number': 111, 'mass': 280, 'group': 11, 'period': 7, 'category': 'properti-tak-dikenal'},
    'Cn': {'name': 'Kopernisium', 'number': 112, 'mass': 285, 'group': 12, 'period': 7, 'category': 'logam-transisi'},
    'Nh': {'name': 'Nihonium', 'number': 113, 'mass': 284, 'group': 13, 'period': 7, 'category': 'properti-tak-dikenal'},
    'Fl': {'name': 'Flerovium', 'number': 114, 'mass': 289, 'group': 14, 'period': 7, 'category': 'properti-tak-dikenal'},
    'Mc': {'name': 'Moskovium', 'number': 115, 'mass': 288, 'group': 15, 'period': 7, 'category': 'properti-tak-dikenal'},
    'Lv': {'name': 'Livermorium', 'number': 116, 'mass': 293, 'group': 16, 'period': 7, 'category': 'properti-tak-dikenal'},
    'Ts': {'name': 'Tennessin', 'number': 117, 'mass': 294, 'group': 17, 'period': 7, 'category': 'properti-tak-dikenal'},
    'Og': {'name': 'Oganesson', 'number': 118, 'mass': 294, 'group': 18, 'period': 7, 'category': 'properti-tak-dikenal'},
}

# =================================================================================
# FUNGSI-FUNGSI PERHITUNGAN
# =================================================================================

def parse_formula(formula):
    """Mem-parsing rumus kimia dan mengembalikan dictionary jumlah atom."""
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)|(\()|(\))(\d*)', formula)
    stack = [{}]
    for symbol, count, open_bracket, close_bracket, multiplier in tokens:
        if symbol:
            if symbol not in ELEMENTS_DATA:
                raise ValueError(f"Unsur tidak dikenal: {symbol}")
            num_atoms = int(count) if count else 1
            stack[-1][symbol] = stack[-1].get(symbol, 0) + num_atoms
        elif open_bracket:
            stack.append({})
        elif close_bracket:
            if len(stack) < 2:
                raise ValueError("Tanda kurung tidak cocok dalam rumus.")
            top = stack.pop()
            num_groups = int(multiplier) if multiplier else 1
            for atom, num in top.items():
                stack[-1][atom] = stack[-1].get(atom, 0) + num * num_groups
    if len(stack) != 1:
        raise ValueError("Tanda kurung tidak cocok dalam rumus.")
    return stack[0]

def calculate_molar_mass(atom_counts):
    """Menghitung massa molar dari dictionary jumlah atom."""
    total_mass = 0
    for atom, count in atom_counts.items():
        total_mass += ELEMENTS_DATA[atom]['mass'] * count
    return total_mass

# =================================================================================
# FUNGSI UNTUK TAMPILAN (UI)
# =================================================================================

def get_category_color(category):
    """Memberikan kode warna hex berdasarkan kategori unsur yang baru."""
    colors = {
        'logam-alkali': '#B71C1C',
        'alkali-tanah': '#F57F17',
        'logam-transisi': '#1A237E',
        'logam-pasca-transisi': '#004D40',
        'metaloid': '#1B5E20',
        'nonlogam-reaktif': '#33691E',
        'gas-mulia': '#4A148C',
        'lantanida': '#E65100',
        'aktinida': '#BF360C',
        'properti-tak-dikenal': '#424242'
    }
    return colors.get(category, '#424242')

def periodic_table_view():
    """Menampilkan tabel periodik dengan gaya tema gelap."""
    st.markdown("""
    <style>
        body {
            color: #fafafa;
        }
        .stApp {
            background-color: #0e1117;
        }
        .periodic-table-container {
            padding: 10px;
            background-color: #1f2229;
            border-radius: 10px;
        }
        .periodic-table {
            display: grid;
            grid-template-columns: repeat(18, minmax(60px, 1fr));
            gap: 5px;
        }
        .element-cell {
            border: 1px solid #333;
            border-radius: 8px;
            padding: 5px;
            text-align: center;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            text-decoration: none;
            color: #fafafa;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            aspect-ratio: 1 / 1;
            position: relative;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .element-cell:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            z-index: 10;
        }
        .element-number {
            position: absolute;
            top: 5px;
            left: 5px;
            font-size: 0.6em;
            font-weight: 500;
            color: #a0a0a0;
        }
        .element-symbol {
            font-weight: 600;
            font-size: 1.4em;
            line-height: 1;
            color: #ffffff;
        }
        .element-name {
            font-size: 0.65em;
            margin-top: 2px;
            font-weight: 500;
            color: #d0d0d0;
        }
        .placeholder {
            visibility: hidden;
        }
        .series-spacer {
            grid-column: span 18;
            height: 20px;
        }
        .legend-container {
            margin-top: 25px;
            padding: 15px;
            background-color: #1f2229;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .legend {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9em;
            color: #fafafa;
        }
        .legend-color {
            width: 18px;
            height: 18px;
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

    html = '<div class="periodic-table-container"><div class="periodic-table">'
    table_grid = {(p, g): None for p in range(1, 10) for g in range(1, 19)}

    for symbol, data in ELEMENTS_DATA.items():
        if data['period'] and data['group']:
            table_grid[(data['period'], data['group'])] = (symbol, data)

    lanthanides = sorted([(s, d) for s, d in ELEMENTS_DATA.items() if d['category'] == 'lantanida' and d['group'] is None], key=lambda x: x[1]['number'])
    actinides = sorted([(s, d) for s, d in ELEMENTS_DATA.items() if d['category'] == 'aktinida' and d['group'] is None], key=lambda x: x[1]['number'])
    
    for i, (symbol, data) in enumerate(lanthanides):
        table_grid[(8, i + 3)] = (symbol, data)
    for i, (symbol, data) in enumerate(actinides):
        table_grid[(9, i + 3)] = (symbol, data)

    for period in range(1, 10):
        if period == 8:
            html += '<div class="series-spacer"></div>'
        for group in range(1, 19):
            cell_content = table_grid.get((period, group))
            if cell_content:
                symbol, data = cell_content
                color = get_category_color(data['category'])
                html += f'<a href="?page=Tabel+Periodik&element={symbol}" class="element-cell" style="grid-column: {group}; grid-row: {period}; background-color: {color};">'
                html += f'<div class="element-number">{data["number"]}</div>'
                html += f'<div class="element-symbol">{symbol}</div>'
                html += f'<div class="element-name">{data["name"]}</div>'
                html += '</a>'
            elif period < 8 or (period > 7 and group > 2): 
                 html += f'<div class="placeholder" style="grid-column: {group}; grid-row: {period};"></div>'
    
    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)
    
    legend_categories = {
        'Logam Alkali': 'logam-alkali', 'Alkali Tanah': 'alkali-tanah',
        'Logam Transisi': 'logam-transisi', 'Logam Pasca-Transisi': 'logam-pasca-transisi',
        'Metaloid': 'metaloid', 'Nonlogam Reaktif': 'nonlogam-reaktif',
        'Gas Mulia': 'gas-mulia', 'Lantanida': 'lantanida', 'Aktinida': 'aktinida',
        'Properti Tak Dikenal': 'properti-tak-dikenal'
    }
    legend_html = '<div class="legend-container"><div class="legend">'
    for name, cat in legend_categories.items():
        color = get_category_color(cat)
        legend_html += f'<div class="legend-item"><div class="legend-color" style="background-color:{color};"></div> {name}</div>'
    legend_html += '</div></div>'
    st.markdown(legend_html, unsafe_allow_html=True)

def element_details_view(symbol):
    """Menampilkan detail dari unsur yang dipilih."""
    if symbol in ELEMENTS_DATA:
        data = ELEMENTS_DATA[symbol]
        st.header(f"Detail Unsur: {data['name']} ({symbol})")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Nomor Atom", value=data['number'])
            st.metric(label="Massa Atom (g/mol)", value=f"{data['mass']:.4f}")
        with col2:
            st.metric(label="Golongan", value=data.get('group', 'N/A'))
            st.metric(label="Periode", value=data.get('period', 'N/A'))

        category_name = data['category'].replace('-', ' ').title()
        st.info(f"**Kategori:** {category_name}")
        
        st.write("---")
        if st.button("Kembali ke Tabel Periodik"):
            st.query_params.page = "Tabel Periodik"
            st.query_params.clear() 
            st.rerun()

def display_calculation_breakdown(formula, atom_counts, total_mass):
    """Membuat expander untuk menampilkan rincian perhitungan."""
    with st.expander("Lihat Rincian Perhitungan"):
        st.markdown(f"#### Perhitungan untuk **{formula}**")
        
        calculation_steps = []
        for atom, count in sorted(atom_counts.items()):
            atomic_mass = ELEMENTS_DATA[atom]['mass']
            step_total = atomic_mass * count
            calculation_steps.append(f"- **{count}** atom **{atom}** &times; `{atomic_mass:.4f}` = `{step_total:.4f}`")
        
        st.markdown("\n".join(calculation_steps))
        
        st.markdown("---")
        st.markdown(f"**Total Massa Molar** = **`{total_mass:.4f} g/mol`**")

# =================================================================================
# DEFINISI HALAMAN
# =================================================================================

def landing_page():
    """Fungsi untuk merender halaman utama (Beranda)."""
    st.title("Selamat Datang di Aplikasi Kimia Interaktif ⚛️")
    st.markdown("""
    Aplikasi ini adalah pusat sumber daya Anda untuk menjelajahi dunia kimia yang menakjubkan. Baik Anda seorang siswa yang baru memulai, seorang guru yang mencari alat bantu ajar, atau hanya seorang yang penasaran, Anda akan menemukan alat yang berguna di sini.

    **Gunakan navigasi di sebelah kiri untuk memulai:**

    - **Tabel Periodik**: Jelajahi tabel periodik interaktif, klik pada unsur untuk melihat detailnya.
    - **Kalkulator Kimia**: Hitung massa molar senyawa dengan cepat.
    - **Informasi Kimia**: Baca pengantar singkat tentang konsep-konsep dasar kimia.

    Selamat belajar dan bereksplorasi!
    """)

def periodic_table_page():
    """Fungsi untuk merender halaman Tabel Periodik."""
    st.title("🧪 Tabel Periodik Interaktif")
    
    query_params = st.query_params
    selected_element = query_params.get("element")

    if selected_element:
        element_details_view(selected_element)
    else:
        st.markdown("Klik pada sebuah unsur untuk melihat informasi detailnya.")
        periodic_table_view()

def calculator_page():
    """Fungsi untuk merender halaman Kalkulator Kimia."""
    st.title("🧮 Kalkulator Massa Molar")
    st.markdown("Masukkan rumus kimia dari sebuah senyawa untuk menghitung massa molarnya.")
    
    formula = st.text_input(
        "Masukkan Rumus Kimia (contoh: H2O, C6H12O6, Mg(OH)2)",
        key="formula_input"
    )
    if st.button("Hitung Massa Molar"):
        if formula:
            try:
                atom_counts = parse_formula(formula)
                total_mass = calculate_molar_mass(atom_counts)
                
                st.success(f"**Massa Molar dari {formula} adalah:** `{total_mass:.4f} g/mol`")
                display_calculation_breakdown(formula, atom_counts, total_mass)

            except ValueError as e:
                st.error(f"Error: {e}. Periksa kembali rumus Anda.")
            except Exception as e:
                st.error(f"Terjadi kesalahan tak terduga: {e}")
        else:
            st.warning("Silakan masukkan rumus kimia terlebih dahulu.")

def about_page():
    """Fungsi untuk merender halaman 'Informasi Kimia'."""
    st.title("📖 Informasi Dasar Kimia")
    st.markdown("""
    Kimia adalah studi tentang materi, sifat-sifatnya, bagaimana dan mengapa zat bergabung atau terpisah untuk membentuk zat lain, dan bagaimana zat berinteraksi dengan energi.

    ### Konsep Kunci
    - **Atom**: Unit dasar materi yang terdiri dari inti pusat (proton dan neutron) yang dikelilingi oleh awan elektron. Setiap unsur kimia dicirikan oleh jumlah proton di dalam atomnya.
    - **Unsur**: Zat murni yang hanya terdiri dari atom-atom yang semuanya memiliki jumlah proton yang sama di dalam inti atomnya. Unsur-unsur diatur dalam Tabel Periodik.
    - **Molekul**: Partikel yang terdiri dari dua atau lebih atom yang terikat secara kimia. Molekul bisa terdiri dari atom unsur yang sama (seperti O₂) atau atom dari unsur yang berbeda (seperti H₂O).
    - **Senyawa**: Zat yang terbentuk ketika dua atau lebih unsur kimia yang berbeda terikat secara kimia dalam perbandingan tetap. Contohnya adalah air (H₂O) dan garam dapur (NaCl).
    - **Massa Molar**: Massa dari satu mol suatu zat. Ini adalah properti fisik yang penting dalam stoikiometri dan perhitungan kimia lainnya. Satuannya biasanya gram per mol (g/mol).

    ### Tentang Aplikasi Ini
    Aplikasi ini dibuat untuk menyediakan alat yang mudah diakses untuk:
    1.  **Mempelajari Unsur**: Dengan tabel periodik yang interaktif.
    2.  **Melakukan Perhitungan**: Dengan kalkulator massa molar yang praktis.
    
    Semoga dapat membantu perjalanan belajar kimia Anda!
    """)

# =================================================================================
# APLIKASI UTAMA STREAMLIT (ROUTER)
# =================================================================================

def main():
    st.set_page_config(page_title="Aplikasi Kimia Interaktif", layout="wide")

    # Navigasi di Sidebar
    st.sidebar.title("Navigasi")
    
    pages = ["Beranda", "Tabel Periodik", "Kalkulator Kimia", "Informasi Kimia"]
    
    if 'page' not in st.query_params or st.query_params.page not in pages:
        st.query_params.page = "Beranda"

    default_index = pages.index(st.query_params.page)

    page = st.sidebar.radio(
        "Pilih Halaman",
        pages,
        key="page_selector",
        index=default_index
    )
    
    if st.query_params.page != page:
        st.query_params.page = page
        keys_to_clear = [k for k in st.query_params if k != 'page']
        for k in keys_to_clear:
            del st.query_params[k]
        st.rerun()

    # Routing Halaman
    if page == "Beranda":
        landing_page()
    elif page == "Tabel Periodik":
        periodic_table_page()
    elif page == "Kalkulator Kimia":
        calculator_page()
    elif page == "Informasi Kimia":
        about_page()

if __name__ == "__main__":
    main()
