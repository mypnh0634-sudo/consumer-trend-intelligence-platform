import streamlit as strl
import pandas as pd
import sqlite3
import plotly.express as px
import os

strl.set_page_config(page_title="Hệ thống Phân tích Xu hướng Thị trường", layout="wide")

strl.title("📊 BIỂU ĐỒ PHÂN TÍCH XU HƯỚNG & SỨC KHỎE VIDEO KÊNH ĐỐI THỦ")
strl.markdown("---")

DB_PATH = "database/trend_intelligence.db"

if not os.path.exists(DB_PATH):
    strl.warning("⚠️ Không tìm thấy cơ sở dữ liệu. Vui lòng chạy lệnh `python main.py` trước để thu thập dữ liệu thô.")
else:
    # Đọc dữ liệu từ SQLite để render lên UI
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM tiktok_videos", conn)
    conn.close()

    if df.empty:
        strl.info("Chưa có dữ liệu video nào được lưu trữ trong DB.")
    else:
        # Tính toán nhanh ER cục bộ để phục vụ vẽ đồ thị
        df['er_pct'] = ((df['like_count'] + df['comment_count'] + df['share_count']) / df['view_count'] * 100).round(2)
        df['er_pct'] = df['er_pct'].fillna(0)

        # Khu vực các chỉ số tổng quan (KPI Cards)
        m1, m2, m3, m4 = strl.columns(4)
        m1.metric("Tổng Số Video", len(df))
        m2.metric("Tổng Lượt Xem", f"{df['view_count'].sum():,}")
        m3.metric("Lượt Thích Trung Bình", f"{int(df['like_count'].mean()):,}")
        m4.metric("Tỷ Lệ Tương Tác Cao Nhất", f"{df['er_pct'].max()}%")

        strl.markdown("### 📈 Biểu đồ Xu hướng & Hiệu suất")
        c1, c2 = strl.columns(2)

        with c1:
            fig_views = px.bar(df, x='video_id', y='view_count', color='er_pct',
                               title="Lượt xem từng Video (Màu sắc thể hiện độ tương tác ER)",
                               labels={'view_count': 'Lượt xem', 'video_id': 'Mã Video', 'er_pct': 'Tỷ Lệ ER (%)'})
            strl.plotly_chart(fig_views, use_container_width=True)

        with c2:
            fig_er = px.scatter(df, x='view_count', y='er_pct', size='like_count', hover_name='caption',
                                title="Mối quan hệ giữa Quy mô Lượt xem và Tỷ lệ Tương tác (ER)",
                                labels={'view_count': 'Lượt xem', 'er_pct': 'Tỷ Lệ ER (%)'})
            strl.plotly_chart(fig_er, use_container_width=True)

        # Bảng hiển thị dữ liệu chi tiết
        strl.markdown("### 📋 Danh sách chi tiết dữ liệu đã làm sạch")
        strl.dataframe(df[['video_id', 'username', 'view_count', 'like_count', 'comment_count', 'share_count', 'er_pct', 'caption']], 
                       use_container_width=True)