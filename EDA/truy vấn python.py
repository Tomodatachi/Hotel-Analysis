import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)
# --- GIAI ĐOẠN 0: TẢI VÀ LÀM SẠCH DỮ LIỆU ---

print("="*60)
print("GIAI ĐOẠN 0: TẢI VÀ LÀM SẠCH DỮ LIỆU")
print("="*60)
weekend_file = r"D:\Study_FPTU\ADYm\Project_scrap\REAL DATA\phase_2_data\weekend_data.csv"
weekday_file = r"D:\Study_FPTU\ADYm\Project_scrap\REAL DATA\phase_2_data\weekday_data.csv"
# 1. Tải dữ liệu
try:
    # Giả định tên file là 'weekday_data.csv' và 'weekend_data.csv'
    df_weekday_raw = pd.read_csv(weekday_file)
    df_weekend_raw = pd.read_csv(weekend_file)
    print("Tải file thành công.")
except FileNotFoundError:
    print("LỖI: Không tìm thấy file CSV. Vui lòng kiểm tra lại tên file.")
    exit()

# 2. Hiển thị kích thước dữ liệu (Shape)
print("\n--- 2: Kích thước dữ liệu thô (Shape) ---")
print(f"Dữ liệu trong tuần (thô): {df_weekday_raw.shape} (Hàng, Cột)")
print(f"Dữ liệu cuối tuần (thô): {df_weekend_raw.shape} (Hàng, Cột)")

# 3. Hiển thị 5 dòng đầu (Head)
print("\n--- 3: Demo dữ liệu (Head) ---")
print("Demo dữ liệu TRONG TUẦN (5 dòng đầu):")
print(df_weekday_raw.head())
print("\nDemo dữ liệu CUỐI TUẦN (5 dòng đầu):")
print(df_weekend_raw.head())


# 2. Tạo bản sao để làm sạch (giữ lại bản gốc nếu cần)
df_weekday = df_weekday_raw.copy()
df_weekend = df_weekend_raw.copy()

# 3. Đổi tên các cột giá để dễ phân biệt và nhất quán
df_weekday = df_weekday.rename(columns={'Price_in_week_2_adults_night': 'Price_Weekday'})
df_weekend = df_weekend.rename(columns={'Price_2_adults_night': 'Price_Weekend'})

# 4. Chuyển đổi các cột quan trọng sang dạng số
# Dùng errors='coerce' để biến các giá trị lỗi (ví dụ: "liên hệ") thành NaN (Not a Number)
cols_to_numeric_wkday = ['Price_Weekday']
cols_to_numeric_wkend = ['Price_Weekend', 'Score', 'Stars', 'Reviews']

for col in cols_to_numeric_wkday:
    if col in df_weekday.columns:
        df_weekday[col] = pd.to_numeric(df_weekday[col], errors='coerce')

for col in cols_to_numeric_wkend:
    if col in df_weekend.columns:
        df_weekend[col] = pd.to_numeric(df_weekend[col], errors='coerce')

print("Đã đổi tên cột và chuyển đổi dữ liệu sang dạng số.")

# 5. Xử lý dữ liệu thiếu (Tùy chọn)
# Ví dụ: df_weekend = df_weekend.dropna(subset=['Price_Weekend', 'Score'])
print("\nBáo cáo dữ liệu thiếu (NaN) sau khi làm sạch:")
print("Dữ liệu trong tuần (thiếu):")
print(df_weekday.isnull().sum())
print("\nDữ liệu cuối tuần (thiếu):")
print(df_weekend.isnull().sum())


# --- GIAI ĐOẠN 1: PHÂN TÍCH RIÊNG LẺ (BỘ CUỐI TUẦN) ---

print("\n" + "="*60)
print("GIAI ĐOẠN 1: PHÂN TÍCH RIÊNG LẺ (BỘ DỮ LIỆU CUỐI TUẦN)")
print("="*60)

print("\n--- 1.1: Thống kê mô tả cơ bản (Describe) ---")
# Cho thấy Min, Max, Mean (trung bình), Median (50% - trung vị)
print(df_weekend[['Price_Weekend', 'Score', 'Stars', 'Reviews']].describe())

print("\n--- 1.2: Phân bố khách sạn theo Tỉnh/Thành (Top 10) ---")
print(df_weekend['Province'].value_counts().head(10))

print("\n--- 1.3: Phân bố khách sạn theo Hạng Sao ---")
print(df_weekend['Stars'].value_counts().sort_index())

print("\n--- 1.4: Giá trung bình (cuối tuần) theo Hạng Sao ---")
print(df_weekend.groupby('Stars')['Price_Weekend'].mean().sort_values(ascending=False))

print("\n--- 1.5: Giá trung bình (cuối tuần) theo Tỉnh/Thành (Top 10) ---")
print(df_weekend.groupby('Province')['Price_Weekend'].mean().sort_values(ascending=False).head(10))

print("\n--- 1.6: Truy vấn 'Ngon-Bổ-Rẻ' (Best Value) ---")
# Tìm KS có điểm >= 8.5 VÀ giá < giá trung bình
try:
    avg_price_weekend = df_weekend['Price_Weekend'].mean()
    print(f"Giá trung bình cuối tuần là: {avg_price_weekend:,.0f} VNĐ")
    
    df_best_value = df_weekend[
        (df_weekend['Score'] >= 8.5) & 
        (df_weekend['Price_Weekend'] < avg_price_weekend)
    ].sort_values(by='Score', ascending=False)
    
    if df_best_value.empty:
        print("Không tìm thấy khách sạn 'Ngon-Bổ-Rẻ' nào (Score >= 8.5 và Giá < TB).")
    else:
        print("Các khách sạn 'Ngon-Bổ-Rẻ' (Score >= 8.5, Giá < TB):")
        print(df_best_value[['Hotel_Name', 'Province', 'Score', 'Price_Weekend']])
except Exception as e:
    print(f"Lỗi khi chạy truy vấn Best Value: {e}")


# --- GIAI ĐOẠN 2: PHÂN TÍCH SO SÁNH (TRONG TUẦN vs. CUỐI TUẦN) ---

print("\n" + "="*60)
print("GIAI ĐOẠN 2: PHÂN TÍCH SO SÁNH (TRONG TUẦN vs. CUỐI TUẦN)")
print("="*60)

print("\n--- 2.1: Gộp (Merge) hai bộ dữ liệu ---")
# Chỉ lấy các cột cần thiết để merge
df_weekday_subset = df_weekday[['Hotel_ID', 'Hotel_Name', 'Province', 'Stars', 'Price_Weekday']]
df_weekend_subset = df_weekend[['Hotel_ID', 'Price_Weekend', 'Score', 'Reviews']] # Lấy thêm Score, Reviews từ bộ cuối tuần

# 'inner' merge: Chỉ giữ lại các Hotel_ID xuất hiện ở CẢ HAI bảng
df_compare = pd.merge(df_weekday_subset, df_weekend_subset, on='Hotel_ID', how='inner')

if df_compare.empty:
    print("LỖI: Không gộp được 2 bảng. Có thể 'Hotel_ID' không khớp nhau.")
else:
    print(f"Gộp thành công. Tìm thấy {len(df_compare)} khách sạn xuất hiện ở cả 2 dataset.")
    print(df_compare.head())

    # --- Chỉ chạy tiếp nếu merge thành công ---
    
    print("\n--- 2.2: Tính toán chênh lệch giá (Diff & % Diff) ---")
    df_compare = df_compare.dropna(subset=['Price_Weekday', 'Price_Weekend']) # Xóa các hàng có giá NaN
    
    df_compare['Price_Diff'] = df_compare['Price_Weekend'] - df_compare['Price_Weekday']
    
    # Chia cho Price_Weekday, nhân 100 để ra %.
    # Xử lý trường hợp Price_Weekday = 0 để tránh lỗi chia cho 0
    df_compare['Price_Diff_Percent'] = df_compare.apply(
        lambda row: (row['Price_Diff'] / row['Price_Weekday']) * 100 if row['Price_Weekday'] != 0 else 0, 
        axis=1
    )
    print("Đã tính xong Price_Diff và Price_Diff_Percent.")

    print("\n--- 2.3: [INSIGHT QUAN TRỌNG] % Tăng giá trung bình theo Tỉnh/Thành ---")
    # Tỉnh/thành nào có nhu cầu cuối tuần tăng vọt?
    province_diff = df_compare.groupby('Province')['Price_Diff_Percent'].mean().sort_values(ascending=False)
    print(province_diff)

    print("\n--- 2.4: [INSIGHT QUAN TRỌNG] % Tăng giá trung bình theo Hạng Sao ---")
    # Phân khúc khách sạn nào tăng giá mạnh nhất?
    stars_diff = df_compare.groupby('Stars')['Price_Diff_Percent'].mean().sort_values(ascending=False)
    print(stars_diff)

    print("\n--- 2.5: Top 10 khách sạn tăng giá mạnh nhất (theo %) ---")
    print(df_compare.sort_values(by='Price_Diff_Percent', ascending=False)[
        ['Hotel_Name', 'Province', 'Price_Weekday', 'Price_Weekend', 'Price_Diff_Percent']
    ].head(10))

    print("\n--- 2.6: Các khách sạn giảm giá hoặc giữ nguyên giá cuối tuần (nếu có) ---")
    df_price_drop = df_compare[df_compare['Price_Diff'] <= 0].sort_values(by='Price_Diff')
    
    if df_price_drop.empty:
        print("Không có khách sạn nào giảm giá hoặc giữ nguyên giá vào cuối tuần.")
    else:
        print("Các khách sạn có giá cuối tuần BẰNG HOẶC THẤP HƠN trong tuần:")
        print(df_price_drop[['Hotel_Name', 'Province', 'Price_Weekday', 'Price_Weekend', 'Price_Diff']])


# --- 4 TRUY VẤN NÂNG CAO ---
# Giả định rằng em đã chạy file code chính và
# đã có DataFrame 'df_weekend' (đã được làm sạch)

print("\n" + "="*60)
print("GIAI ĐOẠN 3: PHÂN TÍCH NÂNG CAO (TƯƠNG QUAN & GỘP)")
print("="*60)

# ---
# Ý TƯỞNG 1 (Query 17): Phân phối nhãn "Overall" (Sentiment)
# Kỹ thuật: .value_counts()
# ---
print("\n--- 3.1: Phân phối nhãn 'Overall' (Đánh giá chung) ---")
# .value_counts() đếm số lần xuất hiện của mỗi nhãn
# normalize=True sẽ cho chúng ta tỷ lệ % thay vì số đếm
if 'Overall' in df_weekend.columns:
    print("Số lượng theo nhãn:")
    print(df_weekend['Overall'].value_counts())
    
    print("\nTỷ lệ % theo nhãn:")
    print(df_weekend['Overall'].value_counts(normalize=True).mul(100).round(2).astype(str) + ' %')
else:
    print("Không tìm thấy cột 'Overall' trong df_weekend.")

# ---
# Ý TƯỞNG 2 (Query 11): Mối quan hệ giữa SAO, GIÁ, và ĐIỂM
# Kỹ thuật: .groupby().agg()
# ---
print("\n--- 3.2: Thống kê gộp (Giá TB, Điểm TB) theo Hạng Sao ---")
# .agg() cho phép chúng ta thực hiện nhiều phép tính (count, mean, sum...)
# trên nhiều cột khác nhau trong cùng một lệnh groupby
try:
    df_agg_stars = df_weekend.groupby('Stars').agg(
        n_hotels=('Hotel_ID', 'count'),      # Đếm số khách sạn (dùng cột bất kỳ, ở đây là Hotel_ID)
        avg_price=('Price_Weekend', 'mean'), # Tính giá trung bình
        avg_score=('Score', 'mean')          # Tính điểm trung bình
    ).sort_index() # Sắp xếp theo Stars (0, 1, 2...)
    
    print(df_agg_stars)
except Exception as e:
    print(f"Lỗi khi chạy GroupBy Agg: {e}")

# ---
# Ý TƯỞNG 3 (Query 14): Tương quan toán học (SAO vs. GIÁ)
# Kỹ thuật: .corr()
# ---
print("\n--- 3.3: Tương quan Pearson (SAO vs. GIÁ) toàn thị trường ---")
# Tính toán hệ số tương quan Pearson
# Giá trị từ -1 đến 1.
# > 0: Đồng biến (Sao tăng, Giá tăng)
# < 0: Nghịch biến (Sao tăng, Giá giảm)
# Gần 0: Không tương quan
try:
    # Bỏ qua các hàng có giá trị NaN ở 1 trong 2 cột này
    df_corr = df_weekend[['Stars', 'Price_Weekend']].dropna()
    correlation_matrix = df_corr.corr(method='pearson')
    
    print("Ma trận tương quan:")
    print(correlation_matrix)
    
    # Lấy giá trị tương quan cụ thể
    corr_value = correlation_matrix.loc['Stars', 'Price_Weekend']
    print(f"\nHệ số tương quan (Stars vs. Price): {corr_value:.4f}")
    
except Exception as e:
    print(f"Lỗi khi tính tương quan: {e}")

# ---
# Ý TƯỞNG 4 (Query 15): Tương quan (SAO vs. GIÁ) theo TỈNH
# Kỹ thuật: .groupby().apply()
# ---
print("\n--- 3.4: Tương quan (SAO vs. GIÁ) theo từng Tỉnh/Thành ---")

# Đây là một kỹ thuật nâng cao. Chúng ta cần định nghĩa một hàm
# để tính tương quan cho MỖI nhóm (tỉnh)

def calculate_correlation(group):
    # Cần ít nhất 2 điểm dữ liệu để tính tương quan
    if len(group['Stars'].dropna()) < 2 or len(group['Price_Weekend'].dropna()) < 2:
        return np.nan
    return group['Stars'].corr(group['Price_Weekend'], method='pearson')

try:
    # .apply() sẽ chạy hàm 'calculate_correlation' trên mỗi nhóm
    # được tạo ra bởi 'groupby('Province')'
    
    # CẬP NHẬT: Chọn rõ các cột ['Stars', 'Price_Weekend'] trước khi apply
    # để tắt FutureWarning và làm code hiệu quả hơn.
    df_corr_by_province = df_weekend.groupby('Province')[['Stars', 'Price_Weekend']].apply(calculate_correlation)
    
    # Đổi tên Series, sắp xếp và hiển thị
    df_corr_by_province.name = 'Stars_Price_Correlation'
    print(df_corr_by_province.sort_values(ascending=False).dropna())
    
    print("\nÝ nghĩa: Cho thấy ở tỉnh nào, 'sao' ảnh hưởng đến 'giá' mạnh nhất.")
    
except Exception as e:
    print(f"Lỗi khi tính tương quan theo nhóm: {e}")

print("\n" + "="*60)
print("PHÂN TÍCH EDA HOÀN TẤT.")
print("="*60)
