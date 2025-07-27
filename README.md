1. Tìm hiểu
Về mô hình LLM & Transformer
- Cấu trúc của Transformer Decoder.
- Cách sinh ra text tuần tự (token N → N+1).
Về OpenAI Function Calling
- Cách hoạt động của Function Calling.
- Gọi thử API Function Calling.

2. Viết code thực hành Function Calling
- Tạo file .py để gọi Function Calling.
- Tạo khoảng 2–3 hàm/tool bất kỳ.
- Xây dựng vòng lặp chat với GPT:
    + Người dùng chat → Gọi GPT lần 1.
    + Phân tích kết quả GPT trả về.
    + Nếu có tool_call: extract tên hàm và tham số.
    + Gọi hàm thực thi → Lấy kết quả → Gọi GPT lần 2.
    + Trả kết quả cuối cùng cho người dùng.

3. Tìm hiểu FastAPI
Dùng để tạo backend cho AI Agent.

4. Tìm hiểu Streamlit
Dùng để tạo giao diện UI nhanh cho người dùng.