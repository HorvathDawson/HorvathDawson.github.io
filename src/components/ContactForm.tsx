import React, { useState } from 'react';
import type { ContactFormData } from '../types';

export const ContactForm: React.FC = () => {
  const [formData, setFormData] = useState<ContactFormData>({
    fullName: '',
    email: '',
    message: '',
  });
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Check reCAPTCHA (would need to integrate with reCAPTCHA v2)
    const recaptchaResponse = (window as any).grecaptcha?.getResponse();
    if (!recaptchaResponse) {
      alert('Please complete the reCAPTCHA.');
      return;
    }

    // Create form data for Google Forms submission
    const googleFormData = new FormData();
    googleFormData.append('entry.2005620554', formData.fullName);
    googleFormData.append('entry.1045781291', formData.email);
    googleFormData.append('entry.839337160', formData.message);
    googleFormData.append('entry.670876903', recaptchaResponse);

    // Submit to Google Forms
    fetch('https://docs.google.com/forms/d/e/1FAIpQLSd-ORTakZ4IOBgNYOtuETuGr5X5I9a8xMa0kjfiJJVOyTIASg/formResponse', {
      method: 'POST',
      body: googleFormData,
      mode: 'no-cors',
    });

    setIsSubmitted(true);
  };

  if (isSubmitted) {
    return (
      <div style={{ marginTop: '150px' }}>
        <div>Your submission has been processed...</div>
      </div>
    );
  }

  return (
    <div style={{ marginTop: '150px' }}>
      <h1 className="heading-3">Contact Me</h1>
      <form 
        id="contact-form"
        onSubmit={handleSubmit}
        action="https://docs.google.com/forms/d/e/1FAIpQLSd-ORTakZ4IOBgNYOtuETuGr5X5I9a8xMa0kjfiJJVOyTIASg/formResponse"
        method="POST"
        target="hidden_iframe"
      >
        <label id="contact-form-name-label" htmlFor="entry.2005620554">
          Full Name
        </label>
        <input
          id="entry.2005620554"
          className="round-field w-input contact-form-name-input"
          type="text"
          name="entry.2005620554"
          value={formData.fullName}
          onChange={handleInputChange}
          placeholder="Leeroy Jenkins"
          maxLength={256}
          required
        />

        <label id="contact-form-email-label" htmlFor="entry.1045781291">
          Email Address
        </label>
        <input
          id="entry.1045781291"
          className="round-field w-input contact-form-email-input"
          type="email"
          name="entry.1045781291"
          value={formData.email}
          onChange={handleInputChange}
          placeholder="JenkinsLeeroy@gmail.com"
          maxLength={256}
          required
        />

        <label id="contact-form-message-label" htmlFor="entry.839337160">
          Message
        </label>
        <textarea
          id="entry.839337160"
          className="textarea round-field w-input contact-form-message-textarea"
          name="entry.839337160"
          value={formData.message}
          onChange={handleInputChange}
          placeholder="Hello, I am messaging to tell you about my project, collaboration ideas, or how you can assist my team..."
          maxLength={5000}
        />

        <div className="g-recaptcha contact-recaptcha" data-theme="light"
             data-sitekey="6LeBU6gqAAAAAEJDe5diUdowY2Q0cwpk0GyEdSdy"></div>

        <input 
          id="contact-form-submit" 
          type="submit"
          className="button-portfolio--tile-2 w-button"
          value="Submit"
        />
      </form>
      <iframe name="hidden_iframe" id="hidden_iframe" style={{display:'none'}}></iframe>
    </div>
  );
};

export default ContactForm;
