(.venv) PS D:\VIN_AI\LAB\K4A-Day03-Lab-Chatbot-vs-ReAct-Agent-MCP> py .\src\app.py --all        
==========================================================
🏫 VINUNI AI COURSE - DAY 03 LAB: CHATBOT VS REACT AGENT
==========================================================
🔌 LLM Provider: GeminiProvider
🌐 MCP Server: vinuni-housing-mcp-server

✅ Đã tải thành công 5 Test Cases thử nghiệm.

🚀 [TEST SUITE MODE] Kiểm tra 5 Test Cases:

==================================================
🧪 [TC01] Loại test: direct_query (Độ phức tạp: Low)
📌 Kỳ vọng: Agent trả lời tư vấn chung bằng văn bản và không gọi Tool.

🤖 [REACT AGENT] Câu hỏi: Khi thuê phòng trọ, sinh viên nên dự trù những khoản chi phí nào ngoàitiền thuê?

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
🧠 [Thought]: Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).
[Final Answer]:Ngoài tiền thuê phòng, sinh viên nên dự trù các khoản chi phí sau: tiền điện, tiền nước, tiền internet, chi phí đi lại, ăn uống,, và các chi phí sinh hoạt cá nhân khác.

==================================================
🧪 [TC02] Loại test: chatbot_vs_agent (Độ phức tạp: Medium)
📌 Kỳ vọng: Chatbot Baseline phải nói không có dữ liệu phòng; ReAct Agent phải gọi 'search_student_housing', dùng Observation để trả danh sách phòng phù hợp và không bịa dữ liệu.

💬 [CHATBOT BASELINE] Câu hỏi: Tìm phòng riêng có tổng chi phí dưới 4 triệu đồng mỗi tháng, cáchVinUni tối đa 7 km và cần chỗ để xe.
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.
🤖 Chatbot phản hồi:
Chào bạn,

Rất tiếc, với vai trò là trợ lý, tôi **không có quyền truy cập vào dữ liệu phòng theo thời gian thực** (như địa chỉ, giá cả, tình trạng phòng trống) và không thể tìm kiếm phòng cụ thể theo các tiêu chí bạn đưa ra (phòng riêng dưới 4 triệu, cách VinUni 7km, có chỗ để xe). Tôi cũng không thểđặt lịch xem phòng cho bạn.

Để tìm được phòng phù hợp với yêu cầu của bạn, tôi khuyên bạn nên:
1.  **Sử dụng các nền tảng và ứng dụng tìm phòng trực tuyến:** Các trang web như batdongsan.com.vn, chotot.com, muaban.net, hoặc các nhóm Facebook về thuê phòng trọ khu vực gần VinUni (ví dụ: "Phòng trọ gần VinUni", "Cho thuê nhà trọ Ecopark") sẽ có nhiều thông tin chi tiết.
2.  **Liên hệ các môi giới bất động sản địa phương:** Họ có thể có danh sách các phòng cho thuê phù hợp.
3.  **Khảo sát khu vực gần VinUni:** Tự mình đi xung quanh các khu dân cư gần VinUni (trong bán kính 7km) để tìm các bảng tin cho thuê phòng.

Tuy nhiên, tôi có thể hỗ trợ bạn trong các khía cạnh khác như:

*   **Giải thích cách lựa chọn phòng và lập ngân sách:** Tôi có thể tư vấn những yếu tố cần cân nhắc khi chọn phòng, cách tính toán các chi phí phát sinh ngoài tiền thuê.
*   **Tư vấn cơ bản về quá trình thuê phòng:** Tôi có thể chia sẻ các bước cần thiết khi thuê phòng, những điều cần lưu ý trong hợp đồng thuê nhà, và các quyền lợi nghĩa vụ của người thuê.

Bạn có muốn tôi giúp bạn về cách lựa chọn phòng, lập ngân sách hay quá trình thuê phòng không?

🤖 [REACT AGENT] Câu hỏi: Tìm phòng riêng có tổng chi phí dưới 4 triệu đồng mỗi tháng, cách VinUni tối đa 7 km và cần chỗ để xe.

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
🧠 [Thought]: Gemini quyết định gọi công cụ 'search_student_housing' với tham số: {"max_monthly_budget": 4000000, "max_distance_km": 7, "require_parking": true, "room_type": "private_room"}
🛠️ [Action]: search_student_housing({'max_monthly_budget': 4000000, 'max_distance_km': 7, 'require_parking': True, 'room_type': 'private_room'})
👁️ [Observation]: {"status": "SUCCESS", "total_matches": 6, "properties": [{"property_id": "ROOM-008", "address": "Thôn Lê Xá, Xã Đa Tốn, Gia Lâm, Hà Nội", "room_type": "private_room", "monthly_rent": 1500000, "electricity_cost": 250000, "water_cost": 80000, "internet_cost": 80000, "service_fee": 40000, "has_parking": true, "transport_cost": 100000, "deposit_months": 1, "distance_km": 2.2, "availability": "LIMITED", "available_from": null, "last_updated": "2024-03-26", "total_monthly_cost": 2050000, "source_listing_url": "https://phongtro123.com/con-1-phong-tro-cho-thue-tai-le-xa-gia-lam-co-dh-nl-gia-chi-1-5-trieu-thang-pr650352.html", "thumbnail_url": null, "collected_at": "2026-09-13T15:30:00+07:00", "estimated_fields": ["electricity_cost", "water_cost", "internet_cost", "service_fee", "transport_cost"]}, {"property_id": "ROOM-010", "address": "Ngách 24/40 Ngọc Động, Xã Đa Tốn, Gia Lâm, Hà Nội", "room_type": "private_room", "monthly_rent": 1500000, "electricity_cost": 250000, "water_cost": 80000, "internet_cost": 80000, "service_fee": 40000, "has_parking": true, "transport_cost": 100000, "deposit_months": 1, "distance_km": 2.6, "availability": "AVAILABLE", "available_from": null, "last_updated": "2024-03-19", "total_monthly_cost": 2050000,"source_listing_url": "https://phongtro123.com/phong-tro-khep-kin-ngoc-dong-da-ton-dt-rong-rai-gia-chi-1-5-trieu-thang-pr649529.html", "thumbnail_url": "https://pt123.cdn.static123.com/images/thumbs/450x300/fit/2024/03/19/cho-thue-phong-tro-gan-vinhomes-ocean-park-gia-lam-1_1710830983.jpg", "collected_at": "2026-09-13T15:30:00+07:00", "estimated_fields": ["electricity_cost", "water_cost", "internet_cost", "service_fee", "transport_cost"]}, {"property_id": "ROOM-015", "address": "Ngõ 68 Đường Ỷ Lan, Xã Phú Thị, Gia Lâm, Hà Nội", "room_type": "private_room", "monthly_rent": 1500000, "electricity_cost": 250000, "water_cost": 80000, "internet_cost": 80000, "service_fee": 40000, "has_parking": true, "transport_cost": 200000, "deposit_months": 1, "distance_km": 6.2, "availability": "AVAILABLE", "available_from": null, "last_updated": "2025-03-25", "total_monthly_cost": 2150000, "source_listing_url": "https://phongtro123.com/chinh-chu-cho-thue-phong-tu-10-15m2-trong-nha-3-tang-pr677677.html", "thumbnail_url": "https://pt123.cdn.static123.com/images/thumbs/450x300/fit/2025/03/25/z6440003013782-91a6ef7a0708f7b16fb4623c0b19e467_1742877399.jpg", "collected_at": "2026-09-13T15:30:00+07:00", "estimated_fields": ["electricity_cost", "water_cost", "internet_cost", "service_fee", "transport_cost"]}, {"property_id": "ROOM-002", "address": "Đường Cửu Việt, Thị trấn Trâu Quỳ, Gia Lâm, Hà Nội", "room_type": "private_room", "monthly_rent": 2000000, "electricity_cost": 300000, "water_cost": 80000, "internet_cost": 100000, "service_fee": 50000, "has_parking": true, "transport_cost": 120000, "deposit_months": 1, "distance_km": 3.2, "availability": "AVAILABLE", "available_from": null, "last_updated": "2025-01-12", "total_monthly_cost": 2650000, "source_listing_url": "https://phongtro123.com/cho-thue-phong-tro-20m2-gan-hoc-vien-nong-nghiep-gia-2tr-pr673528.html", "thumbnail_url": null, "collected_at": "2026-09-13T15:30:00+07:00", "estimated_fields": ["electricity_cost", "water_cost", "internet_cost", "service_fee", "transport_cost"]}, {"property_id": "ROOM-013", "address": "Thị trấn Trâu Quỳ, Gia Lâm, Hà Nội", "room_type": "private_room", "monthly_rent": 2500000, "electricity_cost": 300000, "water_cost": 80000, "internet_cost": 80000, "service_fee": 50000, "has_parking": true, "transport_cost": 120000, "deposit_months": 1, "distance_km": 3.2, "availability": "LIMITED", "available_from": null, "last_updated": "2024-03-11", "total_monthly_cost": 3130000, "source_listing_url": "https://phongtro123.com/con-3-phong-tro-trau-quy-gia-lam-dt-30m2-gan-hoc-vien-nong-nghiep-gia-2-5-trieu-thang-pr648571.html", "thumbnail_url": "https://pt123.cdn.static123.com/images/thumbs/450x300/fit/2024/03/11/cho-thue-phong-tro-trau-quy-gia-lam-ha-noi-1_1710128812.jpg", "collected_at": "2026-09-13T15:30:00+07:00", "estimated_fields": ["electricity_cost", "water_cost", "internet_cost", "service_fee", "transport_cost"]}, {"property_id": "ROOM-016", "address": "Ngõ 6 Đường Bát Khối, Xã Bát Tràng, Gia Lâm, Hà Nội", "room_type": "private_room", "monthly_rent": 2500000, "electricity_cost": 300000, "water_cost": 80000, "internet_cost": 80000, "service_fee": 50000, "has_parking": true, "transport_cost": 180000, "deposit_months": 1, "distance_km": 5.5, "availability": "AVAILABLE", "available_from": null, "last_updated": "2026-07-04", "total_monthly_cost": 3190000, "source_listing_url": "https://phongtro123.com/cho-thue-phong-tro-dong-du-ha-gan-bat-trang-va-vinhome-ocean-park-1-pr673544.html", "thumbnail_url": "https://pt123.cdn.static123.com/images/thumbs/450x300/fit/2025/01/15/img-5290_1736948231.jpg", "collected_at": "2026-09-13T15:30:00+07:00", "estimated_fields": ["electricity_cost", "water_cost", "internet_cost", "service_fee", "transport_cost"]}]}

--- 🔄 Vòng lặp ReAct Loop (Step 2/5) ---
🧠 [Thought]: Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).
[Final Answer]:Tôi đã tìm thấy 6 phòng riêng phù hợp với yêu cầu của bạn:

*   **ROOM-008**: Thôn Lê Xá, Xã Đa Tốn, Gia Lâm, Hà Nội. Tổng chi phí: 2.050.000 VND/tháng. Cách VinUni: 2.2 km. Tình trạng: CÒN ÍT.
*   **ROOM-010**: Ngách 24/40 Ngọc Động, Xã Đa Tốn, Gia Lâm, Hà Nội. Tổng chi phí: 2.050.000 VND/tháng. Cách VinUni: 2.6 km. Tình trạng: CÒN PHÒNG.
*   **ROOM-015**: Ngõ 68 Đường Ỷ Lan, Xã Phú Thị, Gia Lâm, Hà Nội. Tổng chi phí: 2.150.000 VND/tháng. Cách VinUni: 6.2 km. Tình trạng: CÒN PHÒNG.
*   **ROOM-002**: Đường Cửu Việt, Thị trấn Trâu Quỳ, Gia Lâm, Hà Nội. Tổng chi phí: 2.650.000 VND/tháng. Cách VinUni: 3.2 km. Tình trạng: CÒN PHÒNG.
*   **ROOM-013**: Thị trấn Trâu Quỳ, Gia Lâm, Hà Nội. Tổng chi phí: 3.130.000 VND/tháng. Cách VinUni: 3.2 km. Tình trạng: CÒN ÍT.
*   **ROOM-016**: Ngõ 6 Đường Bát Khối, Xã Bát Tràng, Gia Lâm, Hà Nội. Tổng chi phí: 3.190.000 VND/tháng. Cách VinUni: 5.5 km. Tình trạng: CÒN PHÒNG.

Bạn có muốn đặt lịch xem phòng nào không?

==================================================
🧪 [TC03] Loại test: room_viewing_booking (Độ phức tạp: Medium)
📌 Kỳ vọng: Agent gọi 'schedule_room_viewing' với đúng student_id, property_id và viewing_datetime; sau đó trả mã booking từ Observation.

🤖 [REACT AGENT] Câu hỏi: Đặt lịch xem ROOM-002 cho sinh viên SV2026001 vào 2026-09-20T15:00:00.

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
🧠 [Thought]: Gemini quyết định gọi công cụ 'schedule_room_viewing' với tham số: {"viewing_datetime": "2026-09-20T15:00:00", "student_id": "SV2026001", "property_id": "ROOM-002"}
🛠️ [Action]: schedule_room_viewing({'viewing_datetime': '2026-09-20T15:00:00', 'student_id': 'SV2026001', 'property_id': 'ROOM-002'})
👁️ [Observation]: {"status": "SUCCESS", "booking_id": "VIEW-SV2026001-ROOM-002", "student_id": "SV2026001", "property_id": "ROOM-002", "viewing_datetime": "2026-09-20T15:00:00", "message": "Đã đặt lịch xem phòng ROOM-002 cho sinh viên SV2026001 vào 2026-09-20T15:00:00."}

--- 🔄 Vòng lặp ReAct Loop (Step 2/5) ---
🧠 [Thought]: Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).
[Final Answer]:Đã đặt lịch xem phòng ROOM-002 cho sinh viên SV2026001 vào 2026-09-20T15:00:00. Mã đặt lịch của bạn là VIEW-SV2026001-ROOM-002.

==================================================
🧪 [TC04] Loại test: no_match_reasoning (Độ phức tạp: High)
📌 Kỳ vọng: Agent gọi 'search_student_housing', nhận danh sách rỗng và đề xuất điều chỉnh ngân sách, khoảng cách, loại phòng hoặc yêu cầu chỗ để xe.

🤖 [REACT AGENT] Câu hỏi: Tìm studio có tổng chi phí dưới 2 triệu đồng mỗi tháng, cách VinUni tối đa 2 km và cần chỗ để xe.

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
🧠 [Thought]: Gemini quyết định gọi công cụ 'search_student_housing' với tham số: {"require_parking": true, "max_monthly_budget": 2000000, "max_distance_km": 2, "room_type": "studio"}
🛠️ [Action]: search_student_housing({'require_parking': True, 'max_monthly_budget': 2000000, 'max_distance_km': 2, 'room_type': 'studio'})
👁️ [Observation]: {"status": "SUCCESS", "total_matches": 0, "properties": []}

--- 🔄 Vòng lặp ReAct Loop (Step 2/5) ---
⚠️ [Gemini API Warning]: Không thể kết nối live API (429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-2.5-flash\nPlease retry in 4.334695223s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'location': 'global', 'model': 'gemini-2.5-flash'}, 'quotaValue': '5'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '4s'}]}}). Tự động fallback về Mock.
🧠 [Thought]: Đã tổng hợp danh sách phòng từ Observation.
[Final Answer]:Không tìm thấy phòng phù hợp. Bạn có thể tăng ngân sách, mở rộng khoảng cách, đổiloại phòng hoặc bỏ yêu cầu chỗ để xe.

==================================================
🧪 [TC05] Loại test: edge_case_handling (Độ phức tạp: Medium)
📌 Kỳ vọng: Agent gọi 'schedule_room_viewing', nhận trạng thái NOT_FOUND và thông báo lịch sự rằng mã phòng không tồn tại, không tự tạo booking.

🤖 [REACT AGENT] Câu hỏi: Đặt lịch xem ROOM-999 cho sinh viên SV2026001 vào 2026-09-21T09:00:00.

--- 🔄 Vòng lặp ReAct Loop (Step 1/5) ---
⚠️ [Gemini API Warning]: Không thể kết nối live API (429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. To monitor your current usage, head to: https://ai.dev/rate-limit. \n* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 5, model: gemini-2.5-flash\nPlease retry in 3.39143055s.', 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Learn more about Gemini API quotas', 'url': 'https://ai.google.dev/gemini-api/docs/rate-limits'}]}, {'@type': 'type.googleapis.com/google.rpc.QuotaFailure', 'violations': [{'quotaMetric': 'generativelanguage.googleapis.com/generate_content_free_tier_requests', 'quotaId': 'GenerateRequestsPerMinutePerProjectPerModel-FreeTier', 'quotaDimensions': {'model': 'gemini-2.5-flash', 'location': 'global'}, 'quotaValue': '5'}]}, {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '3s'}]}}). Tự động fallback về Mock.
🧠 [Thought]: Đã đủ thông tin để gọi Tool đặt lịch xem phòng.
🛠️ [Action]: schedule_room_viewing({'student_id': 'SV2026001', 'property_id': 'ROOM-999', 'viewing_datetime': '2026-09-21T09:00:00'})
👁️ [Observation]: {"status": "NOT_FOUND", "message": "Không tìm thấy phòng có mã 'ROOM-999'."}

--- 🔄 Vòng lặp ReAct Loop (Step 2/5) ---
🧠 [Thought]: Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).
[Final Answer]:Không tìm thấy phòng có mã 'ROOM-999'. Vui lòng kiểm tra lại mã phòng.

==================================================
📊 [KẾT QUẢ TEST SUITE]: Đã thực thi 5/5 Test Cases | 0 Test Cases đang chờ điền câu hỏi (TODO)
📊 [OBSERVABILITY]: Đã lưu 9 sự kiện Waterfall Trace tại 'D:\VIN_AI\LAB\K4A-Day03-Lab-Chatbot-vs-ReAct-Agent-MCP\docs\trace_waterfall.json'!
💡 Để trò chuyện trực tiếp từng câu: Chạy 'python src/app.py --interactive'