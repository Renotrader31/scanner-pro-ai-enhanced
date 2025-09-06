# Contributing to Scanner Pro AI

## 🎯 Welcome Contributors!

Thank you for your interest in contributing to Scanner Pro AI! This project aims to provide professional-grade stock scanning and analysis tools.

## 🚀 Getting Started

### Prerequisites
- Basic knowledge of HTML, CSS, JavaScript
- Understanding of financial markets and trading concepts
- Familiarity with REST APIs (Polygon, FMP)

### Development Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/Renotrader31/scanner-pro-ai.git
   cd scanner-pro-ai
   ```

2. **Install dependencies** (optional)
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   # or simply open index.html in your browser
   ```

## 🛠️ Project Structure

```
scanner-pro-ai/
├── index.html                    # Main application
├── README.md                     # Project documentation
├── API_INTEGRATION_GUIDE.md      # API setup guide
├── DEPLOYMENT_GUIDE.md           # Deployment instructions
├── package.json                  # Dependencies
├── vercel.json                   # Vercel configuration
└── netlify.toml                  # Netlify configuration
```

## 🎨 Code Style Guidelines

### HTML
- Use semantic HTML5 elements
- Maintain proper indentation (2 spaces)
- Include accessibility attributes (ARIA labels, alt text)

### CSS
- Use Tailwind CSS classes when possible
- Follow mobile-first responsive design
- Maintain consistent spacing and naming

### JavaScript
- Use modern ES6+ syntax
- Write clear, descriptive function names
- Add comments for complex logic
- Handle errors gracefully

## 📊 Feature Development Areas

### High Priority
- **Live Data Integration**: Polygon API implementation
- **Advanced Filtering**: Additional technical indicators
- **Performance Optimization**: Large dataset handling
- **Mobile Responsiveness**: Touch-friendly interface

### Medium Priority  
- **Export Features**: PDF reports, Excel integration
- **Custom Alerts**: Price/volume notifications
- **Backtesting**: Historical strategy testing
- **Portfolio Tracking**: Position management

### Low Priority
- **Themes**: Dark/light mode variations
- **Internationalization**: Multi-language support
- **Advanced Charts**: Candlestick patterns
- **Social Features**: Share scans/analyses

## 🧪 Testing Guidelines

### Manual Testing
- Test all scan types with various filters
- Verify table sorting and pagination
- Check mobile responsiveness
- Test API integration (if available)

### Browser Compatibility
- Chrome/Chromium (primary)
- Firefox
- Safari
- Edge

### Performance Testing
- Large dataset handling (4,500+ stocks)
- Memory usage optimization
- Load time optimization

## 📝 Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow code style guidelines
   - Add appropriate comments
   - Test thoroughly

4. **Commit your changes**
   ```bash
   git commit -m "feat: add advanced volume analysis filter"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide clear description
   - Reference any related issues
   - Include screenshots if UI changes

## 🐛 Bug Reports

### Before Submitting
- Check existing issues
- Verify the bug in latest version
- Test in different browsers

### Bug Report Template
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to...
2. Click on...
3. See error

**Expected Behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- Browser: [e.g., Chrome 91]
- OS: [e.g., Windows 10]
- Version: [e.g., 2.0.0]
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should it work?

**Additional Context**
Any other relevant information
```

## 🔐 Security

### API Keys
- Never commit API keys to version control
- Use environment variables for production
- Report security vulnerabilities privately

### Data Privacy
- No user data is stored on servers
- All processing happens client-side
- Respect user privacy in any new features

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Inappropriate conduct

## 📞 Contact

- **Issues**: Use GitHub Issues
- **Discussions**: GitHub Discussions
- **Security**: Email privately for security issues

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special thanks for major features

---

**Thank you for helping make Scanner Pro AI better!** 🚀📈