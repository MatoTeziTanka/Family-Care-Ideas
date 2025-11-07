"""
Email notification system for Atlantis Pinball Leaderboard
Sends email when scores are updated
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional
from datetime import datetime


class EmailNotifier:
    """Handles email notifications for score updates"""
    
    def __init__(self):
        """Initialize email configuration from environment variables"""
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_username = os.environ.get('SMTP_USERNAME', 'lightspeedup.smtp@gmail.com')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.notification_email = os.environ.get('NOTIFICATION_EMAIL', 'AtlantisPinball@lightspeedup.com')
        self.enabled = bool(self.smtp_password)
    
    def send_score_notification(
        self, 
        player_name: str, 
        score: int, 
        is_high_score: bool = False,
        rank: Optional[int] = None
    ) -> bool:
        """
        Send email notification when a score is added
        
        Args:
            player_name: Name of the player
            score: Score achieved
            is_high_score: Whether this is a new personal high score
            rank: Current leaderboard rank (optional)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.enabled:
            print(f"[EMAIL] Not configured - skipping notification")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self._create_subject(player_name, is_high_score)
            msg['From'] = self.smtp_username
            msg['To'] = self.notification_email
            
            # Create email body
            text_body = self._create_text_body(player_name, score, is_high_score, rank)
            html_body = self._create_html_body(player_name, score, is_high_score, rank)
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"[EMAIL] ✅ Notification sent to {self.notification_email}")
            return True
            
        except Exception as e:
            print(f"[EMAIL] ❌ Failed to send notification: {e}")
            return False
    
    def _create_subject(self, player_name: str, is_high_score: bool) -> str:
        """Create email subject line"""
        if is_high_score:
            return f"🏆 New High Score! - {player_name} - Atlantis Pinball"
        return f"🎮 New Score - {player_name} - Atlantis Pinball"
    
    def _create_text_body(
        self, 
        player_name: str, 
        score: int, 
        is_high_score: bool,
        rank: Optional[int]
    ) -> str:
        """Create plain text email body"""
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        body = f"""
Atlantis Pinball Leaderboard Update

Player: {player_name}
Score: {score:,}
Time: {timestamp}
"""
        
        if is_high_score:
            body += f"\n🏆 This is a NEW PERSONAL HIGH SCORE!\n"
        
        if rank:
            body += f"Current Rank: #{rank}\n"
        
        body += f"""
View the leaderboard: http://pinball.lightspeedup.com

---
Atlantis Pinball Leaderboard
1975 Gottlieb Atlantis Pinball Machine
"""
        return body
    
    def _create_html_body(
        self, 
        player_name: str, 
        score: int, 
        is_high_score: bool,
        rank: Optional[int]
    ) -> str:
        """Create HTML email body with Tron aesthetic"""
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        high_score_badge = ""
        if is_high_score:
            high_score_badge = """
            <div style="background: linear-gradient(135deg, #FFD700, #FFA500); 
                        color: #000; 
                        padding: 15px; 
                        border-radius: 8px; 
                        margin: 20px 0;
                        text-align: center;
                        font-weight: bold;
                        font-size: 18px;">
                🏆 NEW PERSONAL HIGH SCORE! 🏆
            </div>
            """
        
        rank_display = ""
        if rank:
            rank_display = f"""
            <tr>
                <td style="padding: 10px; font-weight: bold; color: #00D9FF;">Current Rank:</td>
                <td style="padding: 10px; color: #FF9500; font-weight: bold; font-size: 24px;">#{rank}</td>
            </tr>
            """
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Arial', sans-serif; background-color: #000000;">
    <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #0A0E27, #000000); padding: 30px; border: 2px solid #00D9FF;">
        
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #00D9FF; 
                       text-shadow: 0 0 10px #00D9FF, 0 0 20px #00D9FF; 
                       font-size: 36px; 
                       margin: 10px 0;
                       letter-spacing: 4px;">
                ATLANTIS PINBALL
            </h1>
            <h2 style="color: #FF9500; 
                       text-shadow: 0 0 10px #FF9500; 
                       font-size: 24px; 
                       margin: 10px 0;
                       letter-spacing: 3px;">
                LEADERBOARD UPDATE
            </h2>
        </div>
        
        {high_score_badge}
        
        <!-- Score Details -->
        <div style="background: rgba(0, 217, 255, 0.1); 
                    border: 2px solid #00D9FF; 
                    border-radius: 8px; 
                    padding: 20px; 
                    margin: 20px 0;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px; font-weight: bold; color: #00D9FF;">Player:</td>
                    <td style="padding: 10px; color: #FFFFFF; font-size: 20px; font-weight: bold;">{player_name}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold; color: #00D9FF;">Score:</td>
                    <td style="padding: 10px; color: #FF9500; font-size: 32px; font-weight: bold; text-shadow: 0 0 10px #FF9500;">{score:,}</td>
                </tr>
                {rank_display}
                <tr>
                    <td style="padding: 10px; font-weight: bold; color: #00D9FF;">Time:</td>
                    <td style="padding: 10px; color: #FFFFFF; font-size: 14px;">{timestamp}</td>
                </tr>
            </table>
        </div>
        
        <!-- View Leaderboard Button -->
        <div style="text-align: center; margin: 30px 0;">
            <a href="http://pinball.lightspeedup.com" 
               style="display: inline-block;
                      background: transparent;
                      border: 2px solid #00D9FF;
                      color: #00D9FF;
                      padding: 15px 40px;
                      text-decoration: none;
                      font-weight: bold;
                      font-size: 16px;
                      letter-spacing: 2px;
                      border-radius: 4px;
                      text-shadow: 0 0 10px #00D9FF;">
                VIEW LEADERBOARD
            </a>
        </div>
        
        <!-- Footer -->
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #00D9FF;">
            <p style="color: #00D9FF; font-size: 12px; margin: 5px 0;">
                🎮 1975 Gottlieb Atlantis Pinball Machine 🎮
            </p>
            <p style="color: rgba(255, 255, 255, 0.5); font-size: 10px; margin: 5px 0;">
                Atlantis Pinball Leaderboard System
            </p>
        </div>
        
    </div>
</body>
</html>
        """
        return html


# Singleton instance
_notifier = None

def get_notifier() -> EmailNotifier:
    """Get or create email notifier instance"""
    global _notifier
    if _notifier is None:
        _notifier = EmailNotifier()
    return _notifier



