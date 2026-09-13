# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** [Điền Họ và Tên]  
> **Mã Sinh Viên / Mã Học viên:** [Điền MSSV]  
> **Chủ đề Lựa chọn:** [Điền tên chủ đề đã chọn từ docs/DANH_SACH_DE_TAI.md hoặc Đề tài Mở]  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5/ 5 | Phân tích nhu cầu - > tìm phòng - >  tính tổng chi phí +Khoảng cách - >  xếp hạng rồi hỗ trợ đặt lịch.
Why :
Quy  trình có nhiều bước phụ  thuộc với nhau 
 |
| **2. Tool Interaction** | 5/ 5 | Tool tra cứu D/s thông tin phòng 
Check tình trạng phòng 
Hệ thống đặt lịch xem phòng. 
Why : 
hệ thống cần gọi nhiều tool  để hoan thành quy  trình bên trên . Ngoài ra hệ thống cần kiểm tra thông tin phòng có chính xác hay không ?
 |
| **3. Dynamic Decision** | 3/ 5 | Nếu kết quả lọc phòng  == 0 thì phải quyết định thay đổi tiêu chí nào để cận  vs yêu cầu gốc và trả về các phòng gần chuẩn . 
Why:
Impact lớn   khi kết quả bước trước thay đổi  -- > phải thực  hiện lại toàn bộ quy trình nên chấm 3 điểm . 
 |
| **4. Long Horizon Goal** | 3/ 5 | Agent duy trì mục tiêu tìm chỗ ở phù hợp từ khi thu thập yêu cầu đến so sánh, đặt lịch xem phòng và hỗ trợ ra quyết định. 
why : quy trình chủ yếu hoàn thành trong một phiên tương tác và chưa theo dõi người dùng trong thời gian dài. |
| **TỔNG ĐIỂM AGENTIC FIT** | 16/ 20** | Triển khai ReAct Agent.*Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. MÔ TẢ CÁC TOOL VÀ TOOL SCHEMA

Agent công bố hai Tool qua MCP Server. Tool thứ nhất dùng để tra cứu dữ liệu phòng;
Tool thứ hai thực hiện hành động đặt lịch sau khi sinh viên xác nhận.

### 2.1. Tool `search_student_housing`

**Mục đích:** Tìm và xếp hạng các phòng còn trống gần VinUni theo nhu cầu của
sinh viên. Tool đọc dữ liệu chuẩn từ `data/rental_rooms.json`; LLM không tự tạo
địa chỉ, mức giá hoặc tình trạng phòng.

| Tham số | Kiểu | Bắt buộc | Mô tả |
| :--- | :---: | :---: | :--- |
| `max_monthly_budget` | `number` | Có | Tổng ngân sách tối đa mỗi tháng, đơn vị VND. |
| `max_distance_km` | `number` | Có | Khoảng cách tối đa từ phòng đến VinUni, đơn vị km. |
| `room_type` | `string` | Có | Một trong: `private_room`, `studio`, `mini_apartment`, `shared_room`. |
| `require_parking` | `boolean` | Có | `true` nếu sinh viên yêu cầu chỗ để xe, ngược lại là `false`. |

**JSON Schema rút gọn:**

```json
{
  "name": "search_student_housing",
  "description": "Tìm các phòng còn trống gần VinUni theo ngân sách, khoảng cách, loại phòng và yêu cầu chỗ để xe.",
  "parameters": {
    "type": "object",
    "properties": {
      "max_monthly_budget": { "type": "number" },
      "max_distance_km": { "type": "number" },
      "room_type": {
        "type": "string",
        "enum": ["private_room", "studio", "mini_apartment", "shared_room"]
      },
      "require_parking": { "type": "boolean" }
    },
    "required": [
      "max_monthly_budget",
      "max_distance_km",
      "room_type",
      "require_parking"
    ]
  }
}
```

**Quy tắc thực thi:**

1. Chỉ lấy phòng có trạng thái `AVAILABLE` hoặc `LIMITED`.
2. Lọc theo tổng chi phí, khoảng cách, loại phòng và yêu cầu chỗ để xe.
3. Sắp xếp kết quả theo tổng chi phí tăng dần, sau đó theo khoảng cách tăng dần.
4. Trả về `total_matches` và danh sách `properties` có nguồn bài đăng và ảnh nếu có.

### 2.2. Tool `schedule_room_viewing`

**Mục đích:** Đặt lịch xem một phòng cụ thể sau khi sinh viên xác nhận. Tool kiểm
tra mã phòng và tình trạng phòng trước khi tạo mã booking.

| Tham số | Kiểu | Bắt buộc | Mô tả |
| :--- | :---: | :---: | :--- |
| `student_id` | `string` | Có | Mã sinh viên, ví dụ `SV2026001`. |
| `property_id` | `string` | Có | Mã phòng cần xem, ví dụ `ROOM-002`. |
| `viewing_datetime` | `string` | Có | Ngày giờ xem phòng theo định dạng `YYYY-MM-DDTHH:MM:SS`. |

**JSON Schema rút gọn:**

```json
{
  "name": "schedule_room_viewing",
  "description": "Đặt lịch xem một phòng cụ thể sau khi sinh viên xác nhận.",
  "parameters": {
    "type": "object",
    "properties": {
      "student_id": { "type": "string" },
      "property_id": { "type": "string" },
      "viewing_datetime": { "type": "string" }
    },
    "required": ["student_id", "property_id", "viewing_datetime"]
  }
}
```

**Kết quả thực thi:**

- `SUCCESS`: phòng tồn tại và còn trống; Tool trả `booking_id` cùng thời gian xem.
- `NOT_FOUND`: không tồn tại `property_id` được yêu cầu.
- `UNAVAILABLE`: phòng tồn tại nhưng hiện không còn trống.

### 2.3. Luồng phối hợp Tool

```text
Yêu cầu tìm phòng
→ search_student_housing
→ Observation: danh sách phòng phù hợp
→ Agent trình bày và chờ sinh viên xác nhận
→ schedule_room_viewing
→ Observation: trạng thái và mã booking
→ Final Answer
```

---

## 3. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dưới đây là trace tiêu biểu của **TC03 — Đặt lịch xem phòng**, được trích từ
`docs/trace_waterfall.json` sau khi chạy với `LLM_PROVIDER=gemini`:

```json
[
  {
    "step": 1,
    "query": "Đặt lịch xem ROOM-002 cho sinh viên SV2026001 vào 2026-09-20T15:00:00.",
    "action_type": "TOOL_EXECUTION",
    "thought": "Gemini quyết định gọi công cụ 'schedule_room_viewing' với tham số: {\"viewing_datetime\": \"2026-09-20T15:00:00\", \"student_id\": \"SV2026001\", \"property_id\": \"ROOM-002\"}",
    "tool_name": "schedule_room_viewing",
    "arguments": {
      "viewing_datetime": "2026-09-20T15:00:00",
      "student_id": "SV2026001",
      "property_id": "ROOM-002"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "VIEW-SV2026001-ROOM-002",
      "student_id": "SV2026001",
      "property_id": "ROOM-002",
      "viewing_datetime": "2026-09-20T15:00:00",
      "message": "Đã đặt lịch xem phòng ROOM-002 cho sinh viên SV2026001 vào 2026-09-20T15:00:00."
    },
    "latency_ms": 2226.97
  },
  {
    "step": 2,
    "query": "Đặt lịch xem ROOM-002 cho sinh viên SV2026001 vào 2026-09-20T15:00:00.",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Đã đặt lịch xem phòng ROOM-002 cho sinh viên SV2026001 vào 2026-09-20T15:00:00. Mã đặt lịch của bạn là VIEW-SV2026001-ROOM-002.",
    "latency_ms": 2358.96
  }
]
```

**Đánh giá trace:**

- **Thought:** Gemini nhận diện đúng ý định đặt lịch xem phòng.
- **Action:** Agent chọn đúng Tool `schedule_room_viewing` và truyền đủ ba tham số bắt buộc.
- **Observation:** MCP Server trả trạng thái `SUCCESS` cùng mã booking
  `VIEW-SV2026001-ROOM-002`.
- **Final Answer:** Câu trả lời cuối sử dụng đúng dữ liệu từ Observation, không tự tạo
  mã đặt lịch hoặc thông tin phòng.
- **Kết quả:** Chuỗi ReAct hoàn thành trong 2 bước, tổng độ trễ ghi nhận là
  **4585,93 ms**.

---

## 4. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:**5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
