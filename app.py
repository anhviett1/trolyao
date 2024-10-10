from flask import Flask, render_template, request, jsonify
import os
import re
import pyttsx3
import webbrowser
import threading
import speech_recognition as sr
from datetime import date, datetime
from time import strftime


app = Flask(__name__)


# Cấu hình trợ lý ảo
robot_ear = sr.Recognizer()
robot_mouth = pyttsx3.init()

# Biến theo dõi trạng thái chờ chọn trình duyệt
waiting_for_browser_choice = False

# Chức năng chào hỏi theo thời gian
def greeting_by_time():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Chào buổi sáng bạn!"
    elif 12 <= current_hour < 18:
        return "Chào buổi chiều bạn!"
    elif 18 <= current_hour < 22:
        return "Chào buổi tối bạn!"
    return "Sao bạn không đi ngủ. Bạn nên nghỉ ngời đi!"

# Chức năng lấy ngày hôm nay
def get_today_date():
    return date.today().strftime("%B %d, %Y")

#Chức năng mở trình duyệt
def choose_brower(user_input):
    if "chrome" in user_input:
        threading.Thread(target=lambda: os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')).start()          
        return "Mở Google bằng Chrome"
    elif "Cốc cốc" in user_input:
        threading.Thread(target=lambda: os.startfile('C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe')).start()
        return "Mở Google bằng Cốc cốc"
    
# Chức năng mở trình duyệt web với URL
def open_website(user_input):
    reg_ex = re.search(r'mở (.+)', user_input)
    if reg_ex:
        domain = reg_ex.group(1).strip()
        if not domain.startswith("http"):
            domain = "https://" + domain
        threading.Thread(target=lambda: webbrowser.open(domain)).start()
        return f"Trang web {domain} đã được mở."
    return "Xin lỗi, tôi không thể tìm thấy tên miền trong câu lệnh."


# Hàm để nhận dạng giọng nói và phản hồi
def assistant_response(user_input):
    global waiting_for_browser_choice
    user_input = user_input.lower()

    if  not user_input:
        return "I can't hear you, try again."
    elif waiting_for_browser_choice:
        # Nếu đang chờ người dùng chọn trình duyệt
        waiting_for_browser_choice = False
        return choose_brower(user_input)
    elif "hello" in user_input:
        return f"{greeting_by_time()} Tôi có thể giúp gì cho bạn?"
    elif "today" in user_input:
        return f"Bây giờ là: {get_today_date()}"
    elif "Google" in user_input:
        return f"Bạn đã mở trình duyệt {choose_brower()}"      
    elif "mở" in user_input:  
        return open_website(user_input)      
    elif "bye" in user_input:
        return "Goodbye! See you soon."   
    return "Sorry, I don't understand that."

# Route chính cho trang web
@app.route('/')
def index():
    return render_template('indexx.html')

# API để nhận lệnh từ người dùng
@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.get_json()
    user_input = data.get("command")
    response = assistant_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
