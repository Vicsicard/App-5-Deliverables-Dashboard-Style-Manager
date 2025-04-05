 # Deliverables Dashboard + Style Manager

A dashboard application for managing and reviewing deliverable files with Supabase integration.

## Features

- File metadata retrieval from Supabase
- Secure file access with signed URLs
- File approval/rejection workflow
- Support for multiple file types (video, markdown, JSON)
- Real-time status updates
- Comprehensive logging

## Implementation Status

### Step 1: Flask Setup
- Added required packages to requirements.txt
- Configured environment variables
- Basic Flask app structure

### Step 2: Web Interface for Publishing Summaries
- Implemented /transcript/<transcript_id> route
- Added manifest preview support
- Created dashboard.html template
- Proper error handling and logging
- Supabase integration for data fetching

### Step 3: Copy Embed Code Button
- Added button for website platform videos
- Implemented clipboard copy functionality
- HTML5 video embed code generation
- Success/failure notifications

### Step 4: Retry Failed Uploads
- Added retry button for failed uploads
- Implemented /retry POST endpoint
- Supabase integration for status reset
- Clean redirect handling
- Proper error handling and logging

## Tech Stack

- Python 3.13+
- Flask web framework
- Supabase for storage and database
- pytest for testing
- UTC timezone support for all timestamps

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
```

## Project Structure

```
deliverables_dashboard/
├── templates/          # HTML templates
│   ├── dashboard.html  # Main video listing
│   ├── manifest.html   # Manifest preview
│   └── error.html     # Error display
├── services/          # External integrations
│   ├── video_schedule.py  # Video data handling
│   └── manifest.py    # Manifest fetching
└── supabase_client.py # Supabase configuration
```

## Features

### Video Publishing Dashboard
- View all video publishing records
- Display platform, status, and URLs
- Copy embed code for website videos
- View markdown manifests
- Retry failed uploads

### Error Handling
- User-friendly error pages
- Proper HTTP status codes
- Comprehensive logging
- Clean error recovery

## Contributing

1. Create a feature branch
2. Make your changes
3. Run the test suite
4. Submit a pull request

## License

MIT License
