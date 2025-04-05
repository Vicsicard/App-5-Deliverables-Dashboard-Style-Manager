from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for
from deliverables_dashboard.services.video_schedule import fetch_video_schedule
from deliverables_dashboard.services.manifest import fetch_manifest_text
from deliverables_dashboard.supabase_client import supabase
import markdown
import os

# Load environment variables from .env file
load_dotenv()

# Debug: Print environment variables
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_ANON_KEY:", os.getenv("SUPABASE_ANON_KEY"))

app = Flask(__name__)

@app.route("/transcript/<transcript_id>")
def view_publish_summary(transcript_id):
    """
    Display video publishing records for a given transcript ID.
    Handles errors with user-friendly messages and proper logging.
    """
    app.logger.info(f"Fetching publishing records for transcript: {transcript_id}")
    try:
        if not transcript_id or len(transcript_id.strip()) == 0:
            error_msg = "Invalid transcript ID provided"
            app.logger.error(error_msg)
            return render_template("error.html", error=error_msg), 400
            
        video_records = fetch_video_schedule(transcript_id)
        app.logger.info(f"Successfully fetched {len(video_records)} records for transcript: {transcript_id}")
        return render_template("dashboard.html", transcript_id=transcript_id, video_records=video_records)
    except Exception as e:
        error_msg = f"Error loading data for transcript {transcript_id}: {str(e)}"
        app.logger.error(error_msg)
        return render_template("error.html", error=error_msg), 500

@app.route("/manifest")
def view_manifest():
    """
    Display manifest content from a given URL.
    Handles errors with user-friendly messages and proper logging.
    """
    url = request.args.get("url")
    app.logger.info(f"Attempting to fetch manifest from URL: {url}")
    
    if not url:
        error_msg = "Missing manifest URL"
        app.logger.error(error_msg)
        return render_template("error.html", error=error_msg), 400
        
    try:
        content = fetch_manifest_text(url)
        app.logger.info(f"Successfully fetched manifest content from: {url}")
        
        # Convert markdown to HTML if it looks like markdown
        if url.lower().endswith('.md'):
            html_content = markdown.markdown(content)
            return render_template("manifest.html", content=html_content)
        return render_template("manifest.html", content=content, is_plain_text=True)
        
    except Exception as e:
        error_msg = f"Failed to load manifest from {url}: {str(e)}"
        app.logger.error(error_msg)
        return render_template("error.html", error=error_msg), 500

@app.route("/retry", methods=["POST"])
def retry_upload():
    """
    Reset a failed video upload for reprocessing.
    Clears the error and published status so App 7 will retry the upload.
    """
    video_id = request.form.get("video_id")
    app.logger.info(f"Attempting to retry upload for video: {video_id}")
    
    if not video_id:
        error_msg = "Missing video ID"
        app.logger.error(error_msg)
        return render_template("error.html", error=error_msg), 400

    try:
        response = supabase.table("video_schedule") \
            .update({
                "published": False,
                "publish_error": None
            }) \
            .eq("id", video_id) \
            .execute()
        
        if response.get("error"):
            error_msg = f"Supabase update failed: {response['error']}"
            app.logger.error(error_msg)
            return render_template("error.html", error=error_msg), 500
        
        app.logger.info(f"Successfully reset video {video_id} for retry")
        return redirect(request.referrer or url_for("view_publish_summary", transcript_id="unknown"))
    
    except Exception as e:
        error_msg = f"Error retrying upload: {e}"
        app.logger.error(error_msg)
        return render_template("error.html", error=error_msg), 500

if __name__ == "__main__":
    app.run(debug=True)
