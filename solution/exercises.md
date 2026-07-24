# K4 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 14h00–18h00
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng `*Câu trả lời của bạn*` bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.7, 1.2 và 1.8 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Hà Nội."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi? Ở mức nào phản hồi bắt đầu
kém mạch lạc?** (2–3 câu)
> Qua 4 phản hồi, khi temperature tăng từ 0.0 lên 1.8, văn phong trở nên đa dạng và sáng tạo hơn nhưng tính ổn định giảm dần. Ở mức 0.0 kết quả có tính lặp lại nhất quán nhất. Bắt đầu từ mức 1.5 trở lên (đặc biệt là 1.8), phản hồi xuất hiện các từ ngữ bất hợp lý và bắt đầu kém mạch lạc.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho trợ lý soạn thảo hợp đồng pháp lý,
và bao nhiêu cho trợ lý viết slogan quảng cáo? Giải thích khác biệt.**
> Tôi sẽ đặt temperature = 0.0 cho trợ lý soạn thảo hợp đồng pháp lý để đảm bảo tính chính xác tuyệt đối, nhất quán và không có tính suy đoán ngẫu nhiên. Ngược lại, đối với trợ lý viết slogan quảng cáo, tôi sẽ đặt temperature = 0.8 đến 1.0 để khuyến khích mô hình tạo ra nhiều ý tưởng độc đáo, mới lạ và giàu tính sáng tạo.

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 20.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 2 lần,
mỗi lần trung bình ~500 token đầu ra.

**Ước tính chi phí mỗi ngày của model lớn so với model nhỏ cho workload này
(dựa trên bảng giá trong template). Nêu một trường hợp model lớn xứng đáng
với chi phí và một trường hợp model nhỏ là lựa chọn đúng:**
> Với 20.000 người dùng x 2 lần x 500 token = 20.000K output tokens/ngày. Chi phí gpt-4o (0.010$/1K) là 200$/ngày, trong khi gpt-4o-mini (0.0006$/1K) chỉ tốn 12$/ngày. Model lớn xứng đáng chi phí cho các tác vụ quan trọng như chẩn đoán y tế hoặc phân tích pháp lý phức tạp. Model nhỏ là lựa chọn đúng cho tác vụ đơn giản như phân loại email hoặc tóm tắt đoạn văn ngắn.

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích máy học (machine learning) là gì?"** nhưng hai system prompt
khác nhau:
- "Bạn là một nhà thơ, trả lời mọi thứ bằng hình ảnh ví von, tránh thuật ngữ."
- "Bạn là kỹ sư phần mềm senior, trả lời chính xác, có ví dụ code khi phù hợp."

**Hai phản hồi khác nhau như thế nào (giọng văn, độ dài, mức kỹ thuật)?
Từ đó rút ra system prompt điều khiển được những khía cạnh nào của phản hồi?**
(3–4 câu)
> Phản hồi của nhà thơ mang giọng văn bay bổng, dùng hình ảnh ví von như 'vườn hoa tự học đón nắng' và không dùng thuật ngữ kỹ thuật. Phản hồi của kỹ sư senior mang tính cấu trúc, chính xác, giải thích thuật ngữ kèm ví dụ pseudocode minh họa. Từ đó thấy system prompt điều khiển được giọng văn (tone), góc nhìn nhân vật (persona), mức độ kỹ thuật và định dạng đầu ra của câu trả lời.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~150 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Nếu dùng ước lượng thô để dự
toán ngân sách API cho ứng dụng tiếng Việt, bạn sẽ dự toán thiếu hay thừa —
và vì sao?**
> Số token đếm bằng tiktoken cho tiếng Việt thường cao hơn 30% - 50% so với công thức ước lượng thô (số từ / 0.75). Nếu dùng công thức thô cho ứng dụng tiếng Việt, bạn sẽ dự toán THIẾU ngân sách nghiêm trọng vì các bộ tokenizer hiện tại phân tách từ tiếng Việt có dấu thành nhiều sub-word token hơn so với tiếng Anh.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Xét ba ứng dụng: (a) chatbot văn bản, (b) trợ lý giọng nói đọc to phản hồi,
(c) pipeline dịch tài liệu chạy ngầm ban đêm. Ứng dụng nào hưởng lợi nhiều
nhất từ streaming, ứng dụng nào không cần — và tại sao?** (1 đoạn văn)
> Chatbot văn bản hưởng lợi nhiều nhất từ streaming vì người dùng thấy câu trả lời xuất hiện ngay lập tức (giảm latency cảm nhận). Trợ lý giọng nói cũng có thể dùng streaming để bắt đầu tổng hợp tiếng nói (TTS) sớm hơn. Trong khi đó, pipeline dịch tài liệu chạy ngầm ban đêm hoàn toàn KHÔNG cần streaming vì hệ thống cần xử lý trọn vẹn văn bản và người dùng không theo dõi trực tiếp quá trình sinh từ.

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**Khi API quá tải và hàng nghìn client cùng retry, exponential backoff giúp
gì so me với delay cố định? Tra cứu thêm: kỹ thuật "jitter" (thêm độ trễ ngẫu
nhiên) giải quyết vấn đề gì còn sót lại?**
> Exponential backoff tăng khoảng thời gian chờ sau mỗi lần thất bại, giúp hệ thống server có thời gian hồi phục thay vì bị quá tải liên tục bởi các yêu cầu dồn dập. Kỹ thuật "jitter" thêm độ trễ ngẫu nhiên để tránh hiện tượng 'thố sóng' (thắt nút cổ chai), trong đó hàng ngàn client cùng gửi lại request tại chính xác cùng một thời điểm.

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Viết lại system prompt bạn dùng cho trợ lý của mình. Chỉ ra 2 chỗ trong
prompt mà nếu xóa đi, hành vi trợ lý sẽ thay đổi rõ rệt — và mô tả thay đổi
đó:**
> System prompt: 'Bạn là trợ giảng thân thiện của khóa AI, trả lời ngắn gọn bằng tiếng Việt.' Nếu xóa từ 'thân thiện', câu trả lời sẽ trở nên trang trọng và khô khan. Nếu xóa từ 'ngắn gọn', trợ lý sẽ giải thích rất dài dòng và chi tiết quá mức cần thiết.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn giữ history 4 lượt cuối. Hãy mô tả một tình huống hội thoại
cụ thể mà giới hạn này khiến trợ lý trả lời sai/mất ngữ cảnh, và đề xuất một
cách khắc phục (ví dụ: tóm tắt các lượt cũ, tăng giới hạn có chọn lọc...):**
> Khi người dùng khai báo thông tin cá nhân ở lượt 1 (ví dụ: 'Tôi là sinh viên ngành Khoa học máy tính'), sau 5 lượt trao đổi khác, ở lượt 6 hỏi lại 'Tôi học ngành gì?' thì trợ lý sẽ không nhớ do lịch sử đã bị cắt còn 4 lượt cuối. Để khắc phục, ta có thể dùng mô hình LLM để tóm tắt (summarize) nội dung các lượt cũ thành một đoạn thông tin tóm tắt lưu trong memory thay vì xóa bỏ hoàn toàn.

---

## Danh Sách Kiểm Tra Nộp Bài

- [x] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [x] Cả 4 checkpoint pytest đều pass
- [x] Tất cả 9 câu trong file này đã được trả lời
- [x] Đã copy bài làm vào folder `solution/`, push lên GitHub cá nhân và nộp link repo vào vlearn (theo hướng dẫn README)
