 # Deliverables Dashboard + Style Manager

A dashboard application for managing and reviewing deliverable files with Supabase integration.

## Features

- File metadata retrieval from Supabase
- Secure file access with signed URLs
- File approval/rejection workflow
- Support for multiple file types (video, markdown, JSON)
- Real-time status updates
- Comprehensive logging

## Tech Stack

- Python 3.13+
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
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

The test suite includes:
- Integration tests for Supabase functionality
- File metadata retrieval tests
- Signed URL generation tests
- Approval workflow tests

## Project Structure

```
deliverables_dashboard/
├── controllers/         # Business logic
├── services/           # External service integrations
├── utils/             # Helper functions
└── tests/             # Test suite
```

## Recent Updates

- Implemented proper mocking for Supabase integration tests
- Updated datetime handling to use UTC timezone
- Fixed signed URL generation in tests
- Added comprehensive test coverage for all main features

## Contributing

1. Create a feature branch
2. Make your changes
3. Run the test suite
4. Submit a pull request

## License

MIT License
