import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from tile_arrange import arrange_tiles_no_same_outer

# 色マップ
color_map = {
    1: '#396D53',
    2: '#B3DF4B',
    3: '#E6DE5E',
    4: '#DAA000',
    5: '#FF414D',
    6: '#B12320',
    7: '#FFC7C6',
    8: '#C8E3D0',
    9: '#6DC7B7',
}

# セッションステートで保持（初回セット）
if 'color_map' not in st.session_state:
    st.session_state.color_map = color_map.copy()

# 初期tileデータをセッションに保存（初回のみ）
if 'tile_data' not in st.session_state:
    st.session_state.tile_data =   ['127', '138', '149', '159', '164', '179', '183', '192', '215',
                                    '239', '241', '251', '263', '271', '286', '295', '319', '328',
                                    '349', '359', '362', '378', '387', '395', '418', '423', '436',
                                    '457', '461', '475', '489', '495', '513', '524', '536', '541',
                                    '563', '574', '583', '596', '618', '621', '639', '645', '653',
                                    '671', '682', '695', '714', '724', '731', '741', '759', '763',
                                    '789', '796', '815', '824', '835', '841', '859', '864', '873',
                                    '892', '913', '923', '932', '948', '957', '962', '971', '984' ]

new_tile_data = []
# ボタンでシャッフル
if st.button("🔀 タイルをランダムに並び替える"):
    new_tile_data = []
    try:
        grid = arrange_tiles_no_same_outer(st.session_state.tile_data, 8, 9)
        for row in grid:
            new_tile_data += row
            print(row)
        print(new_tile_data)
        st.session_state.tile_data = new_tile_data
    except Exception as e:
        print(f"Error: {e}")
    #random.shuffle(st.session_state.tile_data)

tile_data = st.session_state.tile_data

with st.sidebar.expander('色の変更'):
    # 各色をcolor_pickerで表示・編集
    for key in range(1, 10):
        new_color = st.color_picker(f"{key} の色", st.session_state.color_map[key])
        st.session_state.color_map[key] = new_color


n_cols = st.sidebar.slider("列数 (m)", 8, 11, 9)
n_rows = (len(tile_data) + n_cols - 1) // n_cols

tile_size = st.sidebar.slider("タイル全体のサイズ", 0.5, 1.0, 0.9, step=0.1)
outer_thickness = st.sidebar.slider("外枠の太さ", 0.0, tile_size / 2, 0.18, step=0.01)
middle_thickness = st.sidebar.slider("中間の太さ", 0.0, tile_size / 2, 0.18, step=0.01)

fig, ax = plt.subplots(figsize=(n_cols * tile_size, n_rows * tile_size))
ax.set_xlim(0, n_cols)
ax.set_ylim(0, n_rows)
ax.set_aspect('equal')
ax.axis('off')

for idx, tile in enumerate(tile_data):
    if len(tile) != 3:
        continue

    c1 = color_map.get(int(tile[0]), 'gray')   # 外
    c2 = color_map.get(int(tile[1]), 'white')  # 中
    c3 = color_map.get(int(tile[2]), 'black')  # 中央

    col = idx % n_cols
    row = n_rows - 1 - (idx // n_cols)
    x, y = col, row

    # 一番外側の四角形
    ax.add_patch(patches.Rectangle(
        (x, y), tile_size, tile_size,
        facecolor=c1,
        edgecolor='white',
        linewidth=2
    ))

    # 中間
    inner1 = outer_thickness
    ax.add_patch(patches.Rectangle(
        (x + inner1, y + inner1),
        tile_size - 2 * inner1,
        tile_size - 2 * inner1,
        facecolor=c2,
        edgecolor='none'
    ))

    # 中央
    inner2 = outer_thickness + middle_thickness
    ax.add_patch(patches.Rectangle(
        (x + inner2, y + inner2),
        tile_size - 2 * inner2,
        tile_size - 2 * inner2,
        facecolor=c3,
        edgecolor='none'
    ))

st.pyplot(fig)


# 9個ごとに表示
if new_tile_data:
    for i in range(0, len(new_tile_data), 9):
        line = '　'.join(new_tile_data[i:i+9])
        st.caption(line)