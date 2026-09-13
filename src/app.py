"""
🚀 CORE AGENT APPLICATION (DAY 03: CHATBOT VS REACT AGENT)
Thực thi so sánh giữa Chatbot Baseline (Cấp 2) và ReAct Agent kết nối MCP Server (Cấp 3).
"""

import json
import os
import sys
import time
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from mcp_server import MCPHousingServer
from prompts import (
    CHATBOT_BASELINE_PROMPT,
    REACT_AGENT_SYSTEM_PROMPT,
    MAX_ITERATIONS
)
from providers import get_llm_provider

load_dotenv()

def load_test_cases():
    """Tải danh sách 5 test cases từ config/test_cases.json hoặc config/test_cases.example.json"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    if not os.path.exists(config_path):
        example_path = os.path.join(base_dir, "config", "test_cases.example.json")
        if os.path.exists(example_path):
            print("⚠️ [CONFIG NOTICE]: Chưa thấy file 'config/test_cases.json'. Đang dùng mẫu 'config/test_cases.example.json'.")
            print("👉 Hãy chạy: copy config/test_cases.example.json config/test_cases.json và viết test cases theo đề tài của bạn!\n")
            config_path = example_path
        else:
            config_path = "test_cases.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_waterfall_trace(trace_data: list):
    """Ghi vết log Waterfall Trace Log ra file docs/trace_waterfall.json"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(base_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    trace_path = os.path.join(docs_dir, "trace_waterfall.json")
    with open(trace_path, "w", encoding="utf-8") as f:
        json.dump(trace_data, f, ensure_ascii=False, indent=2)
    print(f"📊 [OBSERVABILITY]: Đã lưu {len(trace_data)} sự kiện Waterfall Trace tại '{trace_path}'!")


def run_baseline_chatbot(user_query: str, provider):
    """Chạy Chatbot gốc (Cấp 2) không có công cụ gọi Tool"""
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot phản hồi:\n{response}")


def run_react_agent(user_query: str, provider, mcp_server: MCPHousingServer) -> list:
    """
    [TASK 2.2] Hoàn thiện vòng lặp:
    Thought -> Action -> Observation -> Final Answer.

    Hàm phải trả về danh sách Waterfall Trace của toàn bộ phiên làm việc.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")

    trace_logs = []
    tools_list = mcp_server.list_tools()
    working_prompt = user_query
    completed = False

    # --------------------------------------------------------------------------
    # TODO 2.2.1: TẠO VÒNG LẶP REACT CÓ GIỚI HẠN
    # - Lặp từ bước 1 đến MAX_ITERATIONS.
    # - Ghi lại thời điểm bắt đầu của từng bước để tính latency_ms.
    # --------------------------------------------------------------------------
    for step in range(1, MAX_ITERATIONS + 1):
        step_start_time = time.time()
        print(f"\n--- 🔄 Vòng lặp ReAct Loop (Step {step}/{MAX_ITERATIONS}) ---")
        try:
            llm_response = provider.generate_with_tools(
                working_prompt,
                tools_list,
                system_prompt = REACT_AGENT_SYSTEM_PROMPT
            )
        except Exception as e : 
            trace_logs.append({
                "step" : step , 
                "action_type" : "PROVIDER_ERROR" ,
                "error" : str(e)
            })
            print(f"LLM provider error : {e}")
            break

        # ----------------------------------------------------------------------
        # TODO 2.2.2: GỌI LLM VỚI NATIVE TOOL CALLING
        # - Gọi provider.generate_with_tools().
        # - Truyền working_prompt, tools_list và REACT_AGENT_SYSTEM_PROMPT.
        # - Bắt lỗi Provider và ghi sự kiện PROVIDER_ERROR vào trace_logs.
        # - Giá trị tạm bên dưới cần được thay bằng phản hồi thật từ Provider.
        # ----------------------------------------------------------------------
        latency_ms = round((time.time() - step_start_time) * 1000, 2)

        # ----------------------------------------------------------------------
        # TODO 2.2.3: GHI NHẬN THOUGHT
        # - Lấy phần giải thích hành động ngắn từ llm_response["thought"].
        # - Không yêu cầu hoặc lưu chuỗi suy luận nội bộ chi tiết của mô hình.
        # ----------------------------------------------------------------------
        thought = llm_response.get("thought", "Đang suy luận...")
        print(f"🧠 [Thought]: {thought}")

        # ----------------------------------------------------------------------
        # TODO 2.2.4: XỬ LÝ FINAL ANSWER
        # Khi type == "text":
        # - Lấy content.
        # - Ghi sự kiện FINAL_ANSWER vào trace_logs.
        # - Đánh dấu completed = True và kết thúc vòng lặp.
        # ----------------------------------------------------------------------
        if llm_response.get("type") == "text":
            final_answer = llm_response.get("content","")
            trace_logs.append({
                "step" : step , 
                "query" : user_query , 
                "action_type" : "FINAL_ANSWER" ,
                "thought" : thought , 
                "output" : final_answer , 
                "latency_ms" : latency_ms
            })
            print(f"[Final Answer]:{final_answer}")
            completed = True
            break 

        # ----------------------------------------------------------------------
        # TODO 2.2.5: XỬ LÝ ACTION VÀ OBSERVATION
        # Khi type == "tool_call":
        # - Lấy tool_name và arguments.
        # - Gọi mcp_server.call_tool(tool_name, arguments).
        # - Lấy result làm Observation.
        # - Bắt lỗi MCP/Tool thành Observation có status EXECUTION_ERROR.
        # - Ghi TOOL_EXECUTION cùng Action và Observation vào trace_logs.
        # ----------------------------------------------------------------------
        elif llm_response.get("type") == "tool_call":
            tool_name = llm_response.get("tool_name")
            arguments = llm_response.get("arguments",{})
            print(f"🛠️ [Action]: {tool_name}({arguments})")
            try: 
                mcp_result = mcp_server.call_tool(tool_name,arguments)
                observation = mcp_result.get("result",{})
            except Exception as e : 
                observation = {
                    "status"  : "EXECUTION_ERROR" ,
                    "error" : str(e)
                }
            print(
                "👁️ [Observation]:",
                json.dumps(observation,ensure_ascii=False)
            )
            trace_logs.append({
                "step" : step , 
                "query" : user_query , 
                "action_type" : "TOOL_EXECUTION" , 
                "thought" : thought , 
                "tool_name" : tool_name , 
                "arguments" : arguments , 
                "observation" : observation, 
                "latency_ms" : latency_ms
            })
            working_prompt = f"""
            Yêu cầu ban đầu của người dùng : 
            {user_query}
            Công cụ vừa thực hiện : 
            {tool_name}
            Tham số : 
            {json.dumps(arguments,ensure_ascii=False)}
            Observation từ MCP server : 
            {json.dumps(observation,ensure_ascii=False)}
            Hãy dựa trên Observation để:
            - Trả lời người dùng nếu đã đủ dữ liệu; hoặc
            - Gọi Tool tiếp theo nếu thực sự cần.
            Không được bịa thông tin ngoài Observation.

"""
            continue
            # ------------------------------------------------------------------
            # TODO 2.2.6: TRUYỀN OBSERVATION TRỞ LẠI LLM
            # - Cập nhật working_prompt bằng:
            #   + Yêu cầu ban đầu.
            #   + Tool vừa gọi và arguments.
            #   + Observation nhận từ MCP Server.
            # - Yêu cầu LLM trả Final Answer hoặc chọn Tool tiếp theo.
            # - Dùng continue để chạy vòng ReAct kế tiếp, không break tại đây.
            # ------------------------------------------------------------------

        trace_logs.append({
            "step": step,
            "action_type": "INVALID_LLM_RESPONSE",
            "response": llm_response,
            "latency_ms": latency_ms
        })
        print("⚠️ LLM trả về kiểu phản hồi không hợp lệ.")
        break
    else:
        final_answer = (
            "Agent chưa thể hoàn thành yêu cầu trong giới hạn "
            f"{MAX_ITERATIONS} bước."
        )
        print(f"⚠️ {final_answer}")

        trace_logs.append({
            "step": MAX_ITERATIONS,
            "query": user_query,
            "action_type": "MAX_ITERATIONS_REACHED",
            "output": final_answer
        })


    
    return trace_logs


if __name__ == "__main__":
    print("==========================================================")
    print("🏫 VINUNI AI COURSE - DAY 03 LAB: CHATBOT VS REACT AGENT")
    print("==========================================================")
    
    provider = get_llm_provider()
    mcp_server = MCPHousingServer()
    
    print(f"🔌 LLM Provider: {provider.__class__.__name__}")
    print(f"🌐 MCP Server: {mcp_server.server_name}\n")
    
    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases thử nghiệm.\n")
    
    if "--interactive" in sys.argv:
        print("🎮 [INTERACTIVE MODE] Trò chuyện trực tiếp với ReAct Agent:")
        print("💡 Gợi ý câu hỏi thử nghiệm:")
        print("   - Câu hỏi chung: 'Quy chế học vụ VinUni yêu cầu bao nhiêu tín chỉ?'")
        print("   - Tra cứu học vụ: 'Hãy tra cứu thông tin học vụ của sinh viên SV2026001'")
        print("   - Đặt lịch hẹn: 'Đặt lịch hẹn tư vấn cho SV2026001 vào 14:00 ngày 15/09/2026'")
        print("   - Gõ 'exit' hoặc 'quit' để kết thúc phiên trò chuyện.\n")
        while True:
            try:
                user_input = input("👤 Sinh viên hỏi: ").strip()
                if not user_input or user_input.lower() in ["exit", "quit"]:
                    print("👋 Tạm biệt! Kết thúc phiên trò chuyện.")
                    break
                logs = run_react_agent(user_input, provider, mcp_server)
                save_waterfall_trace(logs)
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Đã thoát phiên tương tác.")
                break
    elif "--all" in sys.argv:
        print("🚀 [TEST SUITE MODE] Kiểm tra 5 Test Cases:")
        completed_count = 0
        todo_count = 0
        all_traces = []
        
        for tc in tests:
            print(f"\n==================================================")
            print(f"🧪 [{tc['id']}] Loại test: {tc['type']} (Độ phức tạp: {tc['complexity']})")
            print(f"📌 Kỳ vọng: {tc['expected_behavior']}")
            
            if tc["question"].strip().startswith("TODO"):
                print(f"⏸️ [CHƯA KÍCH HOẠT - ĐANG LÀ TODO]:")
                print(f"   {tc['question']}")
                print(f"   👉 Hãy mở file 'config/test_cases.json' để viết câu hỏi thực tế cho Test Case này!")
                todo_count += 1
            else:
                if tc["type"] == "chatbot_vs_agent":
                    run_baseline_chatbot(tc["question"], provider)
                logs = run_react_agent(tc["question"], provider, mcp_server)
                all_traces.extend(logs)
                completed_count += 1
                
        print(f"\n==================================================")
        print(f"📊 [KẾT QUẢ TEST SUITE]: Đã thực thi {completed_count}/{len(tests)} Test Cases | {todo_count} Test Cases đang chờ điền câu hỏi (TODO)")
        if all_traces:
            save_waterfall_trace(all_traces)
        print(f"💡 Để trò chuyện trực tiếp từng câu: Chạy 'python src/app.py --interactive'")
    else:
        # Chế độ mặc định khi chỉ gõ 'python src/app.py'
        print("ℹ️ HƯỚNG DẪN SỬ DỤNG CHƯƠNG TRÌNH:")
        print("  1. Chat trực tiếp liên tục:   python src/app.py --interactive")
        print("  2. Chạy toàn bộ Test Cases:    python src/app.py --all\n")
        
        sample_query = tests[1]["question"]
        print(f"--- 🏁 DEMO CHẠY THỬ 1 TEST CASE MẪU (TC02: Tra cứu học vụ) ---")
        logs = run_react_agent(sample_query, provider, mcp_server)
        save_waterfall_trace(logs)
        print("\n💡 Hãy thử ngay lệnh: python src/app.py --interactive để chat trực tiếp!")
