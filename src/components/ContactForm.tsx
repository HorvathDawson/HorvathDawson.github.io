import React, { useState } from 'react';

interface ContactFormData {
  fullName: string;
  email: string;
  message: string;
}

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
    setFormData((prev: ContactFormData) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const recaptchaResponse = (window as any).grecaptcha?.getResponse();
    if (!recaptchaResponse) {
      alert('Please complete the reCAPTCHA.');
      return;
    }

    const googleFormData = new FormData();
    googleFormData.append('entry.2005620554', formData.fullName);
    googleFormData.append('entry.1045781291', formData.email);
    googleFormData.append('entry.839337160', formData.message);
    googleFormData.append('entry.670876903', recaptchaResponse);

    fetch('https://docs.google.com/forms/d/e/1FAIpQLSd-ORTakZ4IOBgNYOtuETuGr5X5I9a8xMa0kjfiJJVOyTIASg/formResponse', {
      method: 'POST',
      body: googleFormData,
      mode: 'no-cors',
    });

    setIsSubmitted(true);
  };

  // Inline styles for input fields
  const inputStyle: React.CSSProperties = {
    backgroundColor: 'var(--warm-white)',
    borderRadius: '5px',
    minHeight: '60px',
    marginBottom: '20px',
  };

  const textareaStyle: React.CSSProperties = {
    ...inputStyle,
    minHeight: '140px',
    paddingTop: '14px',
    paddingBottom: '14px',
  };

  if (isSubmitted) {
    return (
      <div style={{ marginTop: '150px' }}>
        <div>Your submission has been processed...</div>
      </div>
    );
  }

  return (
    <>
      <style>
        {`
          #contact-form {
            display: grid;
            grid-column-gap: 20px;
            grid-row-gap: 7px;
            grid-template-rows: auto auto;
            grid-template-columns: 1fr 1fr;
            grid-auto-columns: 1fr;
            grid-auto-flow: row;
          }

          /* Grid Areas - Desktop */
          #contact-form-name-label { grid-area: 1/1/2/2; }
          .contact-name-field      { grid-area: 2/1/3/2; }
          #contact-form-email-label{ grid-area: 1/2/2/3; }
          .contact-email-field     { grid-area: 2/2/3/3; }
          #contact-form-message-label { grid-area: 3/1/4/3; }
          .contact-message-field   { grid-area: 4/1/5/3; }
          .contact-recaptcha-field { grid-area: 5/1/6/2; }
          
          #contact-form-submit {
            grid-area: 5/2/6/3;
            justify-self: end;
          }

          /* Tablet/Mobile Breakpoint */
          @media screen and (max-width: 991px) {
            #contact-form {
              grid-template-columns: 1fr;
            }
            #contact-form-name-label { grid-area: 1/1/2/2; }
            .contact-name-field      { grid-area: 2/1/3/2; }
            #contact-form-email-label{ grid-area: 3/1/4/2; }
            .contact-email-field     { grid-area: 4/1/5/2; }
            #contact-form-message-label { grid-area: 5/1/6/2; }
            .contact-message-field   { grid-area: 6/1/7/2; }
            .contact-recaptcha-field { grid-area: 7/1/8/2; }
            
            #contact-form-submit {
              grid-area: 8/1/9/2;
              justify-self: start;
            }
          }

          @media screen and (max-width: 767px) {
            #contact-form-submit {
              justify-self: start;
            }
          }
        `}
      </style>

      <div style={{ marginTop: '150px' }}>
        <h1 className="section-title">Contact Me</h1>
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
            className="form-input contact-name-field"
            style={inputStyle}
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
            className="form-input contact-email-field"
            style={inputStyle}
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
            className="textarea form-input contact-message-field"
            style={textareaStyle}
            name="entry.839337160"
            value={formData.message}
            onChange={handleInputChange}
            placeholder="Hello, I am messaging to tell you about my project, collaboration ideas, or how you can assist my team..."
            maxLength={5000}
          />

          <div className="g-recaptcha contact-recaptcha-field" data-theme="light"
               data-sitekey="6LeBU6gqAAAAAEJDe5diUdowY2Q0cwpk0GyEdSdy"></div>

          <input 
            id="contact-form-submit" 
            type="submit"
            className="project-cta-button button"
            value="Submit"
          />
        </form>
        <iframe name="hidden_iframe" id="hidden_iframe" style={{display:'none'}}></iframe>
      </div>
    </>
  );
};

export default ContactForm;