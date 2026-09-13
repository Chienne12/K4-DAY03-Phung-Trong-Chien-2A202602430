"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Khai báo Tool Schemas và lớp thực thi cho Trợ lý tìm phòng sinh viên VinUni.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "search_student_housing",
        "description": (
            "Tìm các phòng còn trống gần VinUni theo ngân sách, khoảng cách, "
            "loại phòng và yêu cầu chỗ để xe."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "max_monthly_budget": {
                    "type": "number",
                    "description": "Tổng ngân sách tối đa mỗi tháng, đơn vị VND."
                },
                "max_distance_km": {
                    "type": "number",
                    "description": "Khoảng cách tối đa từ phòng đến VinUni, đơn vị km."
                },
                "room_type": {
                    "type": "string",
                    "enum": [
                        "private_room",
                        "studio",
                        "mini_apartment",
                        "shared_room"
                    ],
                    "description": "Loại phòng sinh viên muốn tìm."
                },
                "require_parking": {
                    "type": "boolean",
                    "description": "Sinh viên có yêu cầu chỗ để xe hay không."
                }
            },
            "required": [
                "max_monthly_budget",
                "max_distance_km",
                "room_type",
                "require_parking"
            ]
        }
    },

    # --------------------------------------------------------------------------
    # TODO 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_room_viewing'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch xem phòng cho sinh viên VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - property_id (string): Mã phòng cần xem (ví dụ: 'ROOM-002')
    #    - viewing_datetime (string): Ngày giờ xem phòng theo định dạng ISO 8601
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "schedule_room_viewing",
        "description": "Đặt lịch xem một phòng cụ thể sau khi sinh viên xác nhận.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần đặt lịch, ví dụ SV2026001."
                },
                "property_id": {
                    "type": "string",
                    "description": "Mã phòng cần xem, ví dụ ROOM-002."
                },
                "viewing_datetime": {
                    "type": "string",
                    "description": "Ngày giờ xem phòng theo định dạng YYYY-MM-DDTHH:MM:SS."
                }
            },
            "required": ["student_id", "property_id", "viewing_datetime"]
        }
    }
]


# ==============================================================================
# 2. ĐỌC DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "rental_rooms.json"


def load_rental_rooms() -> List[Dict[str, Any]]:
    """Đọc danh sách phòng từ file JSON do đơn vị cung cấp."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            rooms = json.load(file)
    except FileNotFoundError as error:
        raise RuntimeError(f"Không tìm thấy file dữ liệu phòng: {DATA_FILE}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"File dữ liệu phòng không phải JSON hợp lệ: {error}") from error

    if not isinstance(rooms, list):
        raise RuntimeError("Dữ liệu phòng phải là một JSON array.")

    return rooms


def execute_search_student_housing(
    max_monthly_budget: float,
    max_distance_km: float,
    room_type: str,
    require_parking: bool
) -> str:
    """Tìm và xếp hạng các phòng phù hợp với nhu cầu sinh viên."""
    matches = [
        room for room in load_rental_rooms()
        if room["availability"] in {"AVAILABLE", "LIMITED"}
        and room["total_monthly_cost"] <= max_monthly_budget
        and room["distance_km"] <= max_distance_km
        and room["room_type"] == room_type
        and (not require_parking or room["has_parking"])
    ]
    matches.sort(key=lambda room: (room["total_monthly_cost"], room["distance_km"]))

    return json.dumps({
        "status": "SUCCESS",
        "total_matches": len(matches),
        "properties": matches
    }, ensure_ascii=False)


def execute_schedule_room_viewing(
    student_id: str,
    property_id: str,
    viewing_datetime: str
) -> str:
    """Đặt lịch xem phòng sau khi sinh viên xác nhận lựa chọn."""
    normalized_property_id = property_id.strip().upper()
    room: Optional[Dict[str, Any]] = next(
        (
            item for item in load_rental_rooms()
            if item["property_id"] == normalized_property_id
        ),
        None
    )

    if room is None:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy phòng có mã '{property_id}'."
        }, ensure_ascii=False)

    if room["availability"] == "UNAVAILABLE":
        return json.dumps({
            "status": "UNAVAILABLE",
            "property_id": normalized_property_id,
            "message": "Phòng hiện không còn trống để đặt lịch xem."
        }, ensure_ascii=False)

    normalized_student_id = student_id.strip().upper()
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"VIEW-{normalized_student_id}-{normalized_property_id}",
        "student_id": normalized_student_id,
        "property_id": normalized_property_id,
        "viewing_datetime": viewing_datetime,
        "message": (
            f"Đã đặt lịch xem phòng {normalized_property_id} "
            f"cho sinh viên {normalized_student_id} vào {viewing_datetime}."
        )
    }, ensure_ascii=False)


# Router gọi Tool thực tế
TOOL_ROUTER = {
    "search_student_housing": execute_search_student_housing,
    "schedule_room_viewing": execute_schedule_room_viewing
}


def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Trung chuyển yêu cầu đến đúng hàm thực thi Tool."""
    if tool_name not in TOOL_ROUTER:
        return json.dumps({
            "status": "UNKNOWN_TOOL",
            "error": f"Tool '{tool_name}' không tồn tại!"
        }, ensure_ascii=False)

    try:
        return TOOL_ROUTER[tool_name](**arguments)
    except (RuntimeError, TypeError, ValueError) as error:
        return json.dumps({
            "status": "EXECUTION_ERROR",
            "error": str(error)
        }, ensure_ascii=False)
