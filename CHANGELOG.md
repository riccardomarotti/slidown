# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [1] - 2025-06-28

### Changed
- **Migration from PyInstaller to AppImage**: Switched packaging from PyInstaller binaries to AppImage format for better Linux compatibility
- Build environment upgraded to Ubuntu 24.04 for better compatibility
- Improved error handling for WebView deletion during file changes
- Enhanced application metadata for better Linux desktop integration

### Fixed
- Application icon now displays correctly on all desktop environments (X11/Wayland)
- Browser opening functionality now works reliably in packaged builds
- Fixed race conditions in file monitoring that caused crashes during file editing
- Resolved compatibility issues between X11 and Wayland environments

### Technical
- Force X11 mode (`QT_QPA_PLATFORM=xcb`) for consistent icon display across desktop environments
- Added protection against RuntimeError when WebView is deleted during file changes
- AppImage packaging provides better desktop integration and dependency isolation
- Manual AppDir creation with appimagetool ensures proper Python environment setup

## [0] - 2025-06-19

### Added
- Live markdown presentation preview with reveal.js
- PDF export functionality using pandoc and wkhtmltopdf
- Multiple presentation themes
- Speaker notes support (excluded from PDF export)
- Event-driven file monitoring 
- CLI command: `slidown presentation.md`
- Improved library compatibility by removing problematic system libraries
