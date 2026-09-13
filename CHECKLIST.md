# CHECKLIST BÀI LAB 3: CHATBOT VS REACT AGENT — MCP

> Mã bài học: `DAY03-REACT-AGENT`  
> Hình thức: Bài làm cá nhân  
> Tên repository khi nộp: `K4-DAY03-HoVaTen-MSSV`  
> Nguồn yêu cầu: [`README.md`](README.md)

Đánh dấu `[x]` sau khi hoàn thành từng công việc.

## 1. Chuẩn bị repository và môi trường

- [ ] Fork repository sang GitHub cá nhân.
- [ ] Đổi tên repository đúng mẫu `K4-DAY03-HoVaTen-MSSV`.
- [ ] Clone repository về máy.
- [ ] Kiểm tra Python đang dùng phiên bản 3.10–3.12.
- [ ] Tạo môi trường ảo `.venv`.
- [ ] Kích hoạt môi trường ảo.
- [ ] Cài đặt thư viện từ `requirements.txt`.
- [ ] Copy `.env.example` thành `.env`.
- [ ] Copy `config/test_cases.example.json` thành `config/test_cases.json`.
- [ ] Chạy kiểm tra môi trường bằng `python src/app.py --all`.
- [ ] Xác nhận Mock Offline Mode chạy thành công.
- [ ] Xác nhận hai test mẫu `TC01` và `TC02` chạy thành công.

## 2. Chọn và phân tích bài toán

- [ ] Đọc `docs/CODELAB.md`.
- [ ] Tham khảo các đề tài trong `docs/DANH_SACH_DE_TAI.md`.
- [ ] Chọn một bài toán cụ thể cho Agent.
- [ ] Phân tích đủ bốn tiêu chí Agentic Fit.
- [ ] Điền bảng Agentic Fit/Scoring Matrix trong `docs/trace_eval.md`.
- [ ] Xác định dữ liệu và các công cụ Agent cần sử dụng.

## 3. Thiết kế Tool và MCP Server

- [ ] Khai báo Tool Schema đúng chuẩn JSON Schema trong `src/tools.py`.
- [ ] Viết phần xử lý thực tế cho từng Tool.
- [ ] Hoàn thiện Tool Registry trong `src/mcp_server.py`.
- [ ] Hoàn thiện JSON-RPC Dispatcher.
- [ ] Đảm bảo MCP Client trong `src/app.py` gọi được MCP Server.
- [ ] Không sửa mã nguồn tham khảo trong `src/ai_levels/`.

## 4. Xây dựng Chatbot và ReAct Agent

- [ ] Hoàn thiện System Prompt cho Chatbot trong `src/prompts.py`.
- [ ] Hoàn thiện System Prompt cho ReAct Agent.
- [ ] Xây dựng vòng lặp `Thought -> Action -> Observation -> Final Answer`.
- [ ] Cho Agent tự lựa chọn Tool phù hợp.
- [ ] Truyền kết quả Tool trở lại LLM dưới dạng Observation.
- [ ] Đảm bảo câu trả lời cuối dựa trên dữ liệu do Tool trả về.
- [ ] Thiết lập giới hạn vòng lặp và xử lý lỗi Tool/API.

## 5. Tạo bộ kiểm thử

- [ ] Tùy biến `config/test_cases.json` theo đề tài.
- [ ] Hoàn thiện đủ năm Test Case.
- [ ] Có Test Case thể hiện sự khác biệt giữa Chatbot và ReAct Agent.
- [ ] Có Test Case buộc Agent sử dụng Tool.
- [ ] Xác định expected result hoặc tiêu chí đánh giá cho mỗi Test Case.
- [ ] Chạy toàn bộ test bằng Mock Provider để sửa lỗi logic ban đầu.

## 6. Chạy nghiệm thu bằng LLM thật

- [ ] Tạo Gemini API key hoặc OpenAI API key.
- [ ] Điền `GEMINI_API_KEY` hoặc `OPENAI_API_KEY` vào `.env`.
- [ ] Kiểm tra `.env` không bị commit lên Git.
- [ ] Chuyển provider từ Mock sang LLM thật.
- [ ] Chạy đủ năm Test Case với API thật.
- [ ] Xác nhận Agent thực hiện Native Tool Calling qua MCP.
- [ ] Lưu kết quả chạy thực tế để đưa vào báo cáo.

> **Bắt buộc:** Bài nghiệm thu phải chạy bằng LLM API thật. Chỉ chạy Mock Provider sẽ bị trừ điểm phần ReAct/MCP và nghiệm thu thực tế.

## 7. Xuất Waterfall Trace

- [ ] Ghi lại đầy đủ các bước Thought, Action và Observation.
- [ ] Xuất file `docs/trace_waterfall.json`.
- [ ] Kiểm tra trace có đủ dữ liệu cho từng lần gọi Tool.
- [ ] Kiểm tra Action ghi đúng Tool và arguments.
- [ ] Kiểm tra Observation ghi đúng kết quả MCP Server trả về.
- [ ] Đảm bảo API key và thông tin nhạy cảm không xuất hiện trong trace.

## 8. Hoàn thiện báo cáo

- [ ] Hoàn thiện `docs/trace_eval.md`.
- [ ] Điền bảng Agentic Fit.
- [ ] Trình bày Tool Specs.
- [ ] Ghi kết quả năm Test Case chạy bằng API thật.
- [ ] Đưa bằng chứng Waterfall Trace vào báo cáo.
- [ ] So sánh kết quả Chatbot với ReAct Agent.
- [ ] Tự đánh giá kết quả và các hạn chế còn tồn tại.

## 9. Tự kiểm tra và nộp bài

- [ ] Chạy lại `python src/app.py --all`.
- [ ] Kiểm tra chương trình chạy được trên môi trường mới.
- [ ] Kiểm tra repository không chứa `.env`, API key hoặc dữ liệu bí mật.
- [ ] Kiểm tra repository có đầy đủ code, test, trace và báo cáo.
- [ ] Dọn các file tạm, cache và log không cần thiết.
- [ ] Commit với nội dung rõ ràng.
- [ ] Push toàn bộ bài lên GitHub cá nhân.
- [ ] Kiểm tra tên repository đúng quy định.
- [ ] Nộp link repository lên LMS VLearn đúng hạn.

## 10. Artifact bắt buộc

- [ ] `config/test_cases.json`
- [ ] `src/tools.py`
- [ ] `src/mcp_server.py`
- [ ] `src/prompts.py`
- [ ] `src/app.py`
- [ ] `docs/trace_waterfall.json`
- [ ] `docs/trace_eval.md`
- [ ] Link repository GitHub cá nhân đúng tên quy định.

## Phân bổ thời gian đề xuất

| Phần | Thời gian | Công việc |
|---|---:|---|
| Agentic Fit và Tool Schemas | 45 phút | Phân tích bốn tiêu chí và khai báo Tool Schema |
| ReAct Loop và MCP Integration | 60 phút | Xây dựng MCP Server và vòng lặp ReAct |
| Test và Waterfall Log | 45 phút | Chạy năm Test Case bằng API thật và xuất trace |
| Self-Audit và nộp bài | 30 phút | Hoàn thiện báo cáo, kiểm tra và push GitHub |
