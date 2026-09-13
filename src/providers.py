"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
import re
from typing import Dict, Any, List
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho các LLM Provider hỗ trợ Native Tool Calling"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class MockOfflineProvider(BaseLLMProvider):
    """Offline Mock Provider dùng để chạy thử mà không tốn API Key"""
    def __init__(self):
        self.model_name = "Offline-Mock-Model-2026"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return (
            "[Mock Chatbot Response]: Tôi có thể tư vấn cách chọn phòng và "
            "lập ngân sách, nhưng Chatbot không có Tool để tra cứu phòng hoặc "
            "đặt lịch xem phòng."
        )

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        prompt_lower = prompt.lower()

        # Vòng sau Tool Call: đọc Observation và tạo Final Answer.
        observation_match = re.search(
            r"Observation từ MCP [Ss]erver\s*:\s*(.*)",
            prompt,
            flags=re.DOTALL
        )
        if observation_match:
            try:
                observation, _ = json.JSONDecoder().raw_decode(
                    observation_match.group(1).lstrip()
                )
            except (json.JSONDecodeError, TypeError):
                return {
                    "type": "text",
                    "content": "Không thể đọc kết quả từ MCP Server.",
                    "thought": "Observation không có định dạng JSON hợp lệ."
                }

            if observation.get("status") != "SUCCESS":
                return {
                    "type": "text",
                    "content": observation.get(
                        "message",
                        observation.get("error", "Công cụ không thể hoàn thành yêu cầu.")
                    ),
                    "thought": "Tool trả về trạng thái không thành công."
                }

            if "properties" in observation:
                rooms = observation.get("properties", [])
                if not rooms:
                    content = (
                        "Không tìm thấy phòng phù hợp. Bạn có thể tăng ngân sách, "
                        "mở rộng khoảng cách, đổi loại phòng hoặc bỏ yêu cầu chỗ để xe."
                    )
                else:
                    room_lines = []
                    for room in rooms[:3]:
                        parking = "có chỗ để xe" if room.get("has_parking") else "không có chỗ để xe"
                        room_lines.append(
                            f"- {room.get('property_id')}: {room.get('address')}; "
                            f"{room.get('total_monthly_cost', 0):,.0f} VND/tháng; "
                            f"cách VinUni {room.get('distance_km')} km; {parking}."
                        )
                    content = "Các phòng phù hợp nhất:\n" + "\n".join(room_lines)

                return {
                    "type": "text",
                    "content": content,
                    "thought": "Đã tổng hợp danh sách phòng từ Observation."
                }

            return {
                "type": "text",
                "content": observation.get("message", "Yêu cầu đã được xử lý thành công."),
                "thought": "Đã tổng hợp kết quả hành động từ Observation."
            }

        # Intent đặt lịch xem phòng.
        if "đặt lịch" in prompt_lower:
            student_match = re.search(r"\bSV\d+\b", prompt, flags=re.IGNORECASE)
            property_match = re.search(r"\bROOM-\d+\b", prompt, flags=re.IGNORECASE)
            datetime_match = re.search(
                r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?\b",
                prompt
            )

            missing = []
            if not student_match:
                missing.append("mã sinh viên")
            if not property_match:
                missing.append("mã phòng")
            if not datetime_match:
                missing.append("ngày giờ theo định dạng YYYY-MM-DDTHH:MM:SS")

            if missing:
                return {
                    "type": "text",
                    "content": "Vui lòng cung cấp " + ", ".join(missing) + ".",
                    "thought": "Yêu cầu đặt lịch còn thiếu tham số bắt buộc."
                }

            return {
                "type": "tool_call",
                "tool_name": "schedule_room_viewing",
                "arguments": {
                    "student_id": student_match.group(0).upper(),
                    "property_id": property_match.group(0).upper(),
                    "viewing_datetime": datetime_match.group(0)
                },
                "thought": "Đã đủ thông tin để gọi Tool đặt lịch xem phòng."
            }

        # Intent tìm phòng.
        search_verbs = ("tìm", "tra cứu", "gợi ý", "lọc")
        housing_terms = ("phòng", "studio", "căn hộ", "ở ghép")
        wants_search = (
            any(verb in prompt_lower for verb in search_verbs)
            and any(term in prompt_lower for term in housing_terms)
        )
        if wants_search:
            budget_match = re.search(
                r"(\d+(?:[.,]\d+)?)\s*(?:triệu|tr)\b",
                prompt_lower
            )
            distance_match = re.search(
                r"(\d+(?:[.,]\d+)?)\s*km\b",
                prompt_lower
            )

            room_type = None
            room_type_keywords = {
                "phòng riêng": "private_room",
                "studio": "studio",
                "căn hộ mini": "mini_apartment",
                "ở ghép": "shared_room"
            }
            for keyword, value in room_type_keywords.items():
                if keyword in prompt_lower:
                    room_type = value
                    break

            missing = []
            if not budget_match:
                missing.append("ngân sách")
            if not distance_match:
                missing.append("khoảng cách tối đa")
            if not room_type:
                missing.append("loại phòng")

            if missing:
                return {
                    "type": "text",
                    "content": "Vui lòng cung cấp " + ", ".join(missing) + ".",
                    "thought": "Yêu cầu tìm phòng còn thiếu tham số bắt buộc."
                }

            budget = float(budget_match.group(1).replace(",", ".")) * 1_000_000
            max_distance = float(distance_match.group(1).replace(",", "."))
            require_parking = (
                "chỗ để xe" in prompt_lower
                and "không cần chỗ để xe" not in prompt_lower
            )

            return {
                "type": "tool_call",
                "tool_name": "search_student_housing",
                "arguments": {
                    "max_monthly_budget": budget,
                    "max_distance_km": max_distance,
                    "room_type": room_type,
                    "require_parking": require_parking
                },
                "thought": "Đã đủ tiêu chí để gọi Tool tìm phòng."
            }

        return {
            "type": "text",
            "content": (
                "Ngoài tiền thuê, bạn nên dự trù tiền điện, nước, Internet, "
                "phí dịch vụ, chi phí đi lại và tiền cọc. Hãy so sánh tổng "
                "chi phí mỗi tháng thay vì chỉ nhìn giá thuê niêm yết."
            ),
            "thought": "Câu hỏi chung, không cần gọi Tool."
        }


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider (Native Tool Calling với Google GenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-2.5-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("ℹ️ [Gemini Provider]: Chưa tìm thấy GEMINI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)
        
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Chuẩn hóa function declarations cho Gemini SDK
            function_declarations = []
            for tool in tools_schema:
                # Bỏ qua các tool schema chưa được định nghĩa hoàn chỉnh
                if not tool.get("name") or not tool.get("parameters"):
                    continue
                function_declarations.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                })

            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                tools=[{"function_declarations": function_declarations}] if function_declarations else None,
                temperature=0.2
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Kiểm tra xem Gemini có trả về Tool Call không
            if response.function_calls:
                call = response.function_calls[0]
                args = dict(call.args) if hasattr(call, 'args') and call.args else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.name,
                    "arguments": args,
                    "thought": f"Gemini quyết định gọi công cụ '{call.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": response.text or "",
                    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }

        except Exception as e:
            print(f"⚠️ [Gemini API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (Native Tool Calling với OpenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(model=self.model_name, messages=messages)
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("ℹ️ [OpenAI Provider]: Chưa tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": f"OpenAI quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }
        except Exception as e:
            print(f"⚠️ [OpenAI API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


def get_llm_provider() -> BaseLLMProvider:
    """Factory function khởi tạo Provider theo LLM_PROVIDER env variable"""
    provider_type = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_type == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "your_gemini_api_key_here":
            return GeminiProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if key and key != "your_openai_api_key_here":
            return OpenAIProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "mock":
        return MockOfflineProvider()
    else:
        return MockOfflineProvider()
