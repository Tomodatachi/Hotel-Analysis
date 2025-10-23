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

print("\n" + "="*60)
print("PHÂN TÍCH EDA HOÀN TẤT.")
print("="*60)