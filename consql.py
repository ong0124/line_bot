# consql.py
from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import timedelta 
import os
from datetime import datetime, timedelta

# 加载 .env 配置
load_dotenv()

# 从环境变量中获取数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# 创建 FastAPI 实例
app = FastAPI()

def create_db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection

# def get_all_users():
#     connection = create_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM users")
#     results = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return results

def timedelta_to_time_str(td: timedelta) -> str:
    """将timedelta转换为HH:MM格式的字符串"""
    try:
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"
    except (AttributeError, TypeError):
        return "00:00"
def convert_location(location_key: str) -> str:
    location_map = {
        "Booking.pier": "水頭碼頭",
        "Booking.airport": "尚義機場",
    }
    return location_map.get(location_key, location_key)  # 若無對應則回傳原值


def get_all_bookings():
    today = datetime.now().date()

    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM booking WHERE DATE(shuttle_date) = %s ORDER BY LineID;", (today,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    
    user_bookings = {}
    for row in results:
        user_id = row.get("LineID")
        time_delta = row.get("shuttle_time")  # 这里获取的是timedelta对象
        
        booking_info = {
            "location": convert_location(row.get("departure_loc", "未知")),
            "date": row.get("shuttle_date", "").strftime("%Y-%m-%d") if row.get("shuttle_date") else "",
            "time": timedelta_to_time_str(time_delta) if time_delta else "00:00"
        }
        user_bookings.setdefault(user_id, []).append(booking_info)

    return user_bookings