from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

app = Flask(__name__)

@app.route('/transcribe', methods=['GET'])
def transcribe_video():
    video_id = request.args.get('video_id')
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join([item['text'] for item in transcript])
        return jsonify({"transcription": full_transcript})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/selenium-example', methods=['GET'])
def selenium_example():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://www.marcusfaust.com")

    page_title = driver.title
    driver.quit()

    return jsonify({"page_title": page_title})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
