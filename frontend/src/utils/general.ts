export const maskEmailSecure = (email: string) => {
    if (!email || !email.includes('@')) return email;
    
    const [username, domain] = email.split('@');
    const maskedUsername = username.charAt(0) + '*'.repeat(Math.max(username.length - 1, 3));
    
    return `${maskedUsername}@${domain}`;
  }
  