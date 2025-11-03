# 🔒 Security Policy

## Reporting Security Issues

If you discover a security vulnerability in any project within this repository, please report it responsibly:

### **DO NOT** create a public GitHub issue

Instead, please email security details to:
- **Email:** AtlantisPinball@lightspeedup.com  
- **Subject:** [SECURITY] Brief description

We will respond within 48 hours and work with you to address the issue.

---

## Secure Configuration

### Environment Variables

**NEVER commit sensitive data** to the repository:

❌ **Never commit:**
- `.env` files with real credentials
- Database files containing user data
- API keys, passwords, or tokens
- SSL certificates or private keys
- Any file containing personal information

✅ **Always use:**
- `.env.example` files with placeholder values
- Environment variables for secrets
- `.gitignore` to exclude sensitive files
- Secure key management systems for production

### Self-Hosting Security

When deploying these projects:

1. **Change All Default Credentials**
   - Update admin passwords
   - Generate new API keys
   - Use strong, unique passwords

2. **Enable HTTPS/SSL**
   - Use Let's Encrypt for free SSL certificates
   - Never expose HTTP-only services to the internet
   - Configure proper certificate renewal

3. **Firewall Configuration**
   - Only expose necessary ports (80, 443)
   - Block direct database access from internet
   - Use fail2ban or similar for intrusion prevention

4. **Regular Updates**
   - Keep Docker images updated
   - Update dependencies regularly
   - Monitor security advisories

5. **Backup Sensitive Data**
   - Regular database backups
   - Store backups securely (encrypted)
   - Test restore procedures

---

## Privacy Considerations

These projects are designed to be self-hosted to protect your privacy:

- **No Data Collection** - We don't collect any user data
- **No Analytics** - No tracking or telemetry
- **No Third-Party Services** - All data stays on your server
- **Open Source** - Full transparency, audit the code yourself

---

## Supported Versions

We provide security updates for:

| Project | Version | Supported |
|---------|---------|-----------|
| Atlantis Pinball Leaderboard | 1.0.x | ✅ Yes |
| Family Care Dashboard | 0.x | 🚧 Development |

---

## Security Best Practices

### For Users

1. **Strong Passwords**
   - Use password managers
   - Enable 2FA where available
   - Never reuse passwords

2. **Regular Updates**
   - Pull latest code regularly
   - Update Docker images
   - Apply security patches promptly

3. **Access Control**
   - Limit who has admin access
   - Use VPN for remote access
   - Review access logs regularly

### For Contributors

1. **Code Review**
   - All PRs require review
   - Security-sensitive changes need extra scrutiny
   - Test for common vulnerabilities

2. **Dependencies**
   - Keep dependencies up-to-date
   - Use dependency scanners (Dependabot, Snyk)
   - Avoid unmaintained packages

3. **Secure Coding**
   - Validate all user input
   - Use parameterized queries (prevent SQL injection)
   - Sanitize output (prevent XSS)
   - Follow OWASP guidelines

---

## Disclosure Policy

When we receive a security report:

1. **Acknowledgment** - Within 48 hours
2. **Investigation** - Within 1 week
3. **Fix & Testing** - As soon as possible
4. **Public Disclosure** - After fix is released and users have had time to update

We appreciate responsible disclosure and will credit security researchers (unless they prefer to remain anonymous).

---

## Contact

For security concerns:
- **Email:** AtlantisPinball@lightspeedup.com
- **Response Time:** Within 48 hours

Thank you for helping keep our projects secure! 🔒

---

**Last Updated:** November 3, 2025

