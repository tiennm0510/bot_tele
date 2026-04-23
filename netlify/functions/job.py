import asyncio
import sys
import os

# Thêm thư mục gốc vào path để import được file gold.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Import hàm main từ file gold.py của bạn
from src.gold import main


def handler(event, context):
    try:
        # Chạy hàm async main() trong môi trường serverless
        asyncio.run(main())

        return {
            "statusCode": 200,
            "body": "Gửi thông báo giá vàng thành công!"
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": f"Lỗi thực thi: {str(e)}"
        }