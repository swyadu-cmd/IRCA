# Contributing to Intergalactic Riksbanken Chip Authenticator

## Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/swyadu-cmd/vision_project.git

# Navigate to project
cd chip_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Testing

Before submitting a PR:
1. Test simulator mode: `python main.py`
2. Test camera mode: `python camera_main.py`
3. Verify calibration works correctly
4. Check all keyboard controls function properly

## Areas for Contribution

- [ ] OCR integration for real digit recognition
- [ ] Advanced fake detection algorithms
- [ ] Export/logging features
- [ ] UI improvements
- [ ] Performance optimizations
- [ ] Additional camera support
- [ ] Unit tests
- [ ] Documentation improvements

## Questions?

Open an issue for any questions or concerns.
