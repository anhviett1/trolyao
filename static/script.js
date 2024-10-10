
// Kiểm tra xem trình duyệt có hỗ trợ Web Speech API không
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

// Cài đặt cho nhận diện giọng nói
recognition.lang = 'en-US';  // Hoặc 'vi-VN' nếu bạn muốn sử dụng tiếng Việt
recognition.interimResults = false;
recognition.maxAlternatives = 1;

// Khi người dùng bấm nút "Nói"
function startRecognition() {
    recognition.start();
}

// Khi nhận diện giọng nói kết thúc và có kết quả
recognition.onresult = async function(event) {
    const userInput = event.results[0][0].transcript;  
    document.getElementById("command_display").value = userInput;
    sendCommand();
    
};
// Xử lý lỗi nhận diện
recognition.onerror = (event) => {
    console.error('Recognition error:', event.error); 
};

// Lắng nghe sự kiện phím Enter trên ô nhập lệnh (textarea)
document.getElementById("command_display").addEventListener("keydown", function(event){
    if(event.key === "Enter"){
        event.preventDefault();  // Ngăn thêm dòng mới khi nhấn Enter
        sendCommand();  // Gọi hàm gửi lệnh
    }
})

// Gửi lệnh giọng nói đến Flask khi nhấn nút gửi
async function sendCommand() {
    const userInput = document.getElementById("command_display").value;
    
    if (userInput.trim() !== ""){
    //Gửi lệnh dến FLask
        const response = await fetch('/send_command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command: userInput }),
    });

    const result = await response.json();
    // Cập nhật lịch sử trò chuyện trong chatbox
    updateChatbox(userInput, result.response);
    }else{
        alert("Vui lòng nhập lệnh trước khi gửi!!!")
    }
}
// Hàm để cập nhật lịch sử trò chuyện
function updateChatbox(userMessage, assistantMessage) {
    const chatbox = document.getElementById("chatbot");

    // Thêm tin nhắn của người dùng
    const userMsgElement = document.createElement('p');
    userMsgElement.classList.add('message','receiver');
    userMsgElement.textContent = userMessage;
    chatbox.appendChild(userMsgElement);

    // Thêm phản hồi từ trợ lý ảo
    const assistantMsgElement = document.createElement('p');
    assistantMsgElement.classList.add('message','sender');
    assistantMsgElement.textContent = assistantMessage;
    chatbox.appendChild(assistantMsgElement);

    // Cuộn xuống dưới cùng của chatbox khi có tin nhắn mới
    chatbox.scrollTop = chatbox.scrollHeight;
    // Xóa nội dung trong ô nhập sau khi gửi
     document.getElementById("command_display").value = "";
    }
