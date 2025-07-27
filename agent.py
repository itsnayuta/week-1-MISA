import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_weather(location: str) -> str:
    return f"Thời tiết hiện tại ở {location} là trời nắng, có mây nhẹ."

def get_price_gold(date: str) -> str:
    return f"Giá vàng ngày {date} là 75 triệu VND/lượng."

def get_temperature(location: str) -> str:
    return f"Nhiệt độ hiện tại ở {location} là khoảng 33°C."

tools = [
    {
        "function_declarations": [
            {
                "name": "get_weather",
                "description": "Lấy thông tin thời tiết theo địa điểm",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "get_price_gold",
                "description": "Lấy giá vàng hiện tại",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string"},
                    },
                    "required": ["date"],
                },
            },
            {
                "name": "get_temperature",
                "description": "Lấy nhiệt độ hiện tại theo địa điểm",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                    },
                    "required": ["location"],
                },
            },
        ]
    }
]

TOOLS = {
    "get_weather": get_weather,
    "get_price_gold": get_price_gold,
    "get_temperature": get_temperature,
}

def main():
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        tools=tools,
    )
    chat = model.start_chat(enable_automatic_function_calling=False)

    print("Hệ thống sẵn sàng. Nhập 'exit' hoặc 'quit' để thoát.")

    while True:
        user_input = input("\nBạn: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Gọi Gemini lần 1
        response = chat.send_message(user_input)

        # Kiểm tra tool_call
        if response.candidates and response.candidates[0].content.parts:
            parts = response.candidates[0].content.parts
            part = parts[0]

            if hasattr(part, 'function_call'):
                fn_call = part.function_call
                fn_name = fn_call.name
                fn_args = fn_call.args

                print(f"Agent gọi hàm: {fn_name} với tham số: {fn_args}")

                if fn_name in TOOLS:
                    result = TOOLS[fn_name](**fn_args)

                    # Gửi kết quả function cho Gemini dưới dạng text
                    followup = chat.send_message(f"Kết quả của hàm {fn_name}: {result}")
                    print("Agent:", followup.text)
                else:
                    print(f"Không tìm thấy hàm {fn_name}")
            else:
                print("Agent:", response.text)
        else:
            print("Agent:", response.text)


if __name__ == "__main__":
    main()