## Slidown v{{VERSION}}

### Features
- Live markdown presentation preview with reveal.js
- PDF export functionality using pandoc and wkhtmltopdf
- Multiple presentation themes
- Speaker notes support (excluded from PDF export)
- Event-driven file monitoring 
- CLI command: `slidown presentation.md`

### Installation
```bash
# Download and extract the binary
wget https://github.com/riccardomarotti/slidown/releases/download/v{{VERSION}}/slidown-linux-x86_64-v{{VERSION}}.tar.gz
tar -xzf slidown-linux-x86_64-v{{VERSION}}.tar.gz
cd slidown
./slidown presentation.md

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install pandoc wkhtmltopdf
```

### Download
- **Linux binary**: slidown-linux-x86_64-v{{VERSION}}.tar.gz (standalone executable, no Python required)