import logging
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def hello():
    app.logger.info("Accessed root route")
    return "Hello, World!"

@app.route('/transcribe', methods=['GET'])
def transcribe_video():
    video_id = request.args.get('video_id')
    app.logger.info(f"Accessed transcribe route with video_id: {video_id}")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join([item['text'] for item in transcript])
        app.logger.info("Transcription successful")
        return jsonify({"transcription": full_transcript})
    except Exception as e:
        app.logger.error(f"Error during transcription: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/selenium-example', methods=['GET'])
def selenium_example():
    app.logger.info("Accessed selenium-example route")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.get("https://www.marcusfaust.com")
        page_title = driver.title
        driver.quit()
        app.logger.info(f"Selenium example successful. Page title: {page_title}")
        return jsonify({"page_title": page_title})
    except Exception as e:
        app.logger.error(f"Error in selenium example: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    app.logger.info("Health check accessed")
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.logger.info("Starting Flask application")
    app.run(host="0.0.0.0", port=5000)
