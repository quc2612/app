from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from Google Sheets

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    # Extract video ID from URL
    video_id = None
    if 'youtube.com/watch?v=' in video_url:
        video_id = video_url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in video_url:
        video_id = video_url.split('youtu.be/')[1].split('?')[0]

    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    try:
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'vi'])
        # Combine transcript text
        transcript_text = ' '.join([entry['text'] for entry in transcript])
        return jsonify({'transcript': transcript_text})
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for this video'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)