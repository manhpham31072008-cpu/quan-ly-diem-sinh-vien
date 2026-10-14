import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quản lý điểm sinh viên", page_icon="🎓", layout="wide")
st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.caption("Tính điểm tổng kết, xếp loại và thống kê kết quả học tập.")

# 1. Tạo DataFrame
df = pd.DataFrame({
    "Ho_ten": [
        "Nguyễn Minh Anh", "Trần Quốc Bảo", "Lê Hoàng Chi",
        "Phạm Đức Duy", "Võ Ngọc Hà", "Đặng Tuấn Kiệt",
        "Bùi Khánh Linh", "Hoàng Gia Minh", "Đỗ Thảo My",
        "Phan Nhật Nam"
    ],
    "Chuyen_can": [9, 8, 10, 7.5, 8.5, 6, 9.5, 7, 8, 5.5],
    "Giua_ky": [8.5, 7, 9, 6.5, 8, 5.5, 9, 7.5, 6, 5],
    "Cuoi_ky": [9, 7.5, 9.5, 7, 8.5, 6, 9.5, 8, 6.5, 4.5]
})

# 2. Tính điểm tổng kết và xếp loại
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"] + 0.3 * df["Giua_ky"] + 0.5 * df["Cuoi_ky"]
).round(2)

def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7:
        return "Khá"
    elif diem >= 5:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Hiển thị bảng điểm
st.subheader("📋 Bảng điểm sinh viên")
display_df = df.rename(columns={
    "Ho_ten": "Họ tên", "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ", "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết", "Xep_loai": "Xếp loại"
})
st.dataframe(display_df, use_container_width=True, hide_index=True)

# 3. Thống kê
st.subheader("📊 Thống kê kết quả")
diem_tb = df["Tong_ket"].mean()
idx_max = df["Tong_ket"].idxmax()
idx_min = df["Tong_ket"].idxmin()
so_dat = int((df["Tong_ket"] >= 5).sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
c2.metric("Điểm cao nhất", f"{df.loc[idx_max, 'Tong_ket']:.2f}", df.loc[idx_max, "Ho_ten"])
c3.metric("Điểm thấp nhất", f"{df.loc[idx_min, 'Tong_ket']:.2f}", df.loc[idx_min, "Ho_ten"])
c4.metric("Sinh viên đạt (≥ 5)", f"{so_dat}/10")

# 4. Tra cứu điểm sinh viên
st.subheader("🔎 Tra cứu điểm từng sinh viên")
ten_sv = st.selectbox("Chọn sinh viên", df["Ho_ten"].tolist())
sv = df.loc[df["Ho_ten"] == ten_sv].iloc[0]
a, b, c, d = st.columns(4)
a.metric("Chuyên cần", f"{sv['Chuyen_can']:.2f}")
b.metric("Giữa kỳ", f"{sv['Giua_ky']:.2f}")
c.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.2f}")
d.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
st.write(f"**Xếp loại:** {sv['Xep_loai']}")

# 5. Biểu đồ cột
st.subheader("📈 Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df["Ho_ten"], df["Tong_ket"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Họ tên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", labelrotation=45)
for label in ax.get_xticklabels():
    label.set_horizontalalignment("right")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()
st.caption("Người thực hiện: Phạm Duy Mạnh_32")
