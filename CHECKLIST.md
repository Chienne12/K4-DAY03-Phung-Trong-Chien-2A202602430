# CHECKLIST BÀI LAB 3: CHATBOT VS REACT AGENT — MCP

> Mã bài học: `DAY03-REACT-AGENT`  
> Hình thức: Bài làm cá nhân  
> Tên repository khi nộp: `K4-DAY03-HoVaTen-MSSV`  
> Nguồn yêu cầu: [`README.md`](README.md)

Đánh dấu `[x]` sau khi hoàn thành từng công việc.

## 1. Chuẩn bị repository và môi trường

- [x] Fork repository sang GitHub cá nhân.
- [x] Đổi tên repository đúng mẫu `K4-DAY03-HoVaTen-MSSV`.
- [x] Clone repository về máy.
- [x] Kiểm tra Python đang dùng phiên bản 3.10–3.12.
- [x] Tạo môi trường ảo `.venv`.
- [x] Kích hoạt môi trường ảo.
- [x] Cài đặt thư viện từ `requirements.txt`.
- [x] Copy `.env.example` thành `.env`.
- [x] Copy `config/test_cases.example.json` thành `config/test_cases.json`.
- [x] Chạy kiểm tra môi trường bằng `python src/app.py --all`.
- [x] Xác nhận Mock Offline Mode chạy thành công.
- [x] Xác nhận hai test mẫu `TC01` và `TC02` chạy thành công.

## 2. Chọn và phân tích bài toán

- [x] Đọc `docs/CODELAB.md`.
- [x] Tham khảo các đề tài trong `docs/DANH_SACH_DE_TAI.md`.
- [x] Chọn một bài toán cụ thể cho Agent.
- [x] Phân tích đủ bốn tiêu chí Agentic Fit.
- [x] Điền bảng Agentic Fit/Scoring Matrix trong `docs/trace_eval.md`.
- [x] Xác định dữ liệu và các công cụ Agent cần sử dụng.

## 3. Thiết kế Tool và MCP Server

- [x] Khai báo Tool Schema đúng chuẩn JSON Schema trong `src/tools.py`.
- [x] Viết phần xử lý thực tế cho từng Tool.
- [x] Hoàn thiện Tool Registry trong `src/mcp_server.py`.
- [x] Hoàn thiện JSON-RPC Dispatcher.
- [x] Đảm bảo MCP Client trong `src/app.py` gọi được MCP Server.
- [x] Không sửa mã nguồn tham khảo trong `src/ai_levels/`.

## 4. Xây dựng Chatbot và ReAct Agent

- [x] Hoàn thiện System Prompt cho Chatbot trong `src/prompts.py`.
- [x] Hoàn thiện System Prompt cho ReAct Agent.
- [x] Xây dựng vòng lặp `Thought -> Action -> Observation -> Final Answer`.
- [x] Cho Agent tự lựa chọn Tool phù hợp.
- [x] Truyền kết quả Tool trở lại LLM dưới dạng Observation.
- [x] Đảm bảo câu trả lời cuối dựa trên dữ liệu do Tool trả về.
- [x] Thiết lập giới hạn vòng lặp và xử lý lỗi Tool/API.

## 5. Tạo bộ kiểm thử

- [x] Tùy biến `config/test_cases.json` theo đề tài.
- [x] Hoàn thiện đủ năm Test Case.
- [x] Có Test Case thể hiện sự khác biệt giữa Chatbot và ReAct Agent.
- [x] Có Test Case buộc Agent sử dụng Tool.
- [x] Xác định expected result hoặc tiêu chí đánh giá cho mỗi Test Case.
- [x] Chạy toàn bộ test bằng Mock Provider để sửa lỗi logic ban đầu.

## 6. Chạy nghiệm thu bằng LLM thật

- [x] Tạo Gemini API key hoặc OpenAI API key.
- [x] Điền `GEMINI_API_KEY` hoặc `OPENAI_API_KEY` vào `.env`.
- [x] Kiểm tra `.env` không bị commit lên Git.
- [x] Chuyển provider từ Mock sang LLM thật.
- [x] Chạy đủ năm Test Case với API thật.
- [x] Xác nhận Agent thực hiện Native Tool Calling qua MCP.
- [x] Lưu kết quả chạy thực tế để đưa vào báo cáo.

> **Bắt buộc:** Bài nghiệm thu phải chạy bằng LLM API thật. Chỉ chạy Mock Provider sẽ bị trừ điểm phần ReAct/MCP và nghiệm thu thực tế.

## 7. Xuất Waterfall Trace

- [x] Ghi lại đầy đủ các bước Thought, Action và Observation.
- [x] Xuất file `docs/trace_waterfall.json`.
- [x] Kiểm tra trace có đủ dữ liệu cho từng lần gọi Tool.
- [x] Kiểm tra Action ghi đúng Tool và arguments.
- [x] Kiểm tra Observation ghi đúng kết quả MCP Server trả về.
- [x] Đảm bảo API key và thông tin nhạy cảm không xuất hiện trong trace.

## 8. Hoàn thiện báo cáo

- [x] Hoàn thiện `docs/trace_eval.md`.
- [x] Điền bảng Agentic Fit.
- [x] Trình bày Tool Specs.
- [x] Ghi kết quả năm Test Case chạy bằng API thật.
- [x] Đưa bằng chứng Waterfall Trace vào báo cáo.
- [x] So sánh kết quả Chatbot với ReAct Agent.
- [x] Tự đánh giá kết quả và các hạn chế còn tồn tại.

## 9. Tự kiểm tra và nộp bài

- [x] Chạy lại `python src/app.py --all`.
- [x] Kiểm tra chương trình chạy được trên môi trường mới.
- [x] Kiểm tra repository không chứa `.env`, API key hoặc dữ liệu bí mật.
- [x] Kiểm tra repository có đầy đủ code, test, trace và báo cáo.
- [x] Dọn các file tạm, cache và log không cần thiết.
- [x] Commit với nội dung rõ ràng.
- [x] Push toàn bộ bài lên GitHub cá nhân.
- [x] Kiểm tra tên repository đúng quy định.
- [x] Nộp link repository lên LMS VLearn đúng hạn.

## 10. Artifact bắt buộc

- [x] `config/test_cases.json`
- [x] `src/tools.py`
- [x] `src/mcp_server.py`
- [x] `src/prompts.py`
- [x] `src/app.py`
- [x] `docs/trace_waterfall.json`
- [x] `docs/trace_eval.md`
- [x] Link repository GitHub cá nhân đúng tên quy định.

## Phân bổ thời gian đề xuất

| Phần | Thời gian | Công việc |
|---|---:|---|
| Agentic Fit và Tool Schemas | 45 phút | Phân tích bốn tiêu chí và khai báo Tool Schema |
| ReAct Loop và MCP Integration | 60 phút | Xây dựng MCP Server và vòng lặp ReAct |
| Test và Waterfall Log | 45 phút | Chạy năm Test Case bằng API thật và xuất trace |
| Self-Audit và nộp bài | 30 phút | Hoàn thiện báo cáo, kiểm tra và push GitHub |
