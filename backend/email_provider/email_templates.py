# email_templates.py

Registration = {
    "from": "Rivue <contact@rivue.ai>",
    "subject": "Welcome to Rivue",
    "bcc":"contact@rivue.ai",
    "html": """,
    <html>
        <head>
            <style>
                .email-container {
                    font-family: 'Arial', sans-serif;
                    color: #f0f8ff;
                    line-height: 1.6;
                    background-color: #0e0c14;
                }
                .header {
                    background-color: #4a148c;
                    padding: 20px;
                    text-align: center;
                    border-bottom: 3px solid #6a34b9;
                }
                .content {
                    padding: 20px;
                }
                .footer {
                    background-color: #4a148c;
                    padding: 10px;
                    text-align: center;
                    border-top: 3px solid #6a34b9;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    margin-top: 20px;
                    color: f0f8ff;
                    text-decoration: none;
                    border-radius: 5px;
                    border: 1px solid #6a34b9;
                }
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>Welcome to Rivue</h1>
                </div>
                <div class="content">
                    <p>Dear Rivuer,</p>
                    <p>
                        You're on the brink of an incredible journey! We're thrilled to have you aboard Rivue, where your potential is limitless, and every challenge is a new opportunity for growth.
                    </p>
                    <p>
                        Please confirm your email address to start ascending to new heights:
                    </p>
                    <a href="{{ link }}" class="button">Confirm Email</a>
                    <p>
                        If you have any questions or need assistance, our mentorship team is here for you every step of the way.
                    </p>
                    <p>
                        Embrace your journey,<br>
                        The Rivue.ai Team
                    </p>
                </div>
                <div class="footer">
                    <p>
                        Stay connected:<br>
                        <a href="https://x.com/Rivueai">Twitter/X</a> | <a href="https://discord.gg/33yAcp2qDf">Discord</a>
                    </p>
                </div>
            </div>
        </body>
    </html>
    """,
    "text": """Welcome to Rivue.ai

Dear Rivuer,

You're on the brink of an incredible journey! We're thrilled to have you aboard Rivue.ai, where your potential is limitless, and every challenge is a new opportunity for growth.

Please confirm your email address to start ascending to new heights:
[Confirm Email] {{ confirmation_link }}

If you have any questions or need assistance, our mentorship team is here for you every step of the way.

Embrace your journey,
The Rivue.ai Team"""
}


# email_templates.py

PasswordReset = {
    "from": "Rivue <contact@rivue.ai>",
    "subject": "Reset Your Password",
    "bcc": "contact@rivue.ai",
    "html": """,
    <html>
        <head>
            <style>
                .email-container {
                    font-family: 'Arial', sans-serif;
                    color: #f0f8ff;
                    line-height: 1.6;
                    background-color: #0e0c14;
                }
                .header {
                    background-color: #4a148c;
                    padding: 20px;
                    text-align: center;
                    border-bottom: 3px solid #6a34b9;
                }
                .content {
                    padding: 20px;
                }
                .footer {
                    background-color: #4a148c;
                    padding: 10px;
                    text-align: center;
                    border-top: 3px solid #6a34b9;
                }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    margin-top: 20px;
                    color: #f0f8ff;
                    text-decoration: none;
                    border-radius: 5px;
                    border: 1px solid #6a34b9;
                }
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>Reset Your Password</h1>
                </div>
                <div class="content">
                    <p>Dear Rivuer,</p>
                    <p>
                        We received a request to reset your password. If you made this request, please click the button below to reset your password:
                    </p>
                    <a href="{{ link }}" class="button">Reset Password</a>
                    <p>
                        If you did not request a password reset, please ignore this email or contact our support team if you have concerns.
                    </p>
                    <p>
                        Stay secure,<br>
                        The Rivue.ai Team
                    </p>
                </div>
                <div class="footer">
                    <p>
                        Stay connected:<br>
                        <a href="https://x.com/Rivueai">Twitter/X</a> | <a href="https://discord.gg/33yAcp2qDf">Discord</a>
                    </p>
                </div>
            </div>
        </body>
    </html>
    """,
    "text": """Reset Your Password

Dear Rivuer,

We received a request to reset your password. If you made this request, please use the link below to reset your password:
[Reset Password] {{ reset_link }}

If you did not request a password reset, please ignore this email or contact our support team if you have concerns.

Stay secure,
The Rivue.ai Team"""
}
