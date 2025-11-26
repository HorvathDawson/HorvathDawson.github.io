import React, { useState, useEffect } from 'react';

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

  // 1. FIX: Load ReCAPTCHA script dynamically when component mounts
  useEffect(() => {
    const script = document.createElement('script');
    script.src = "https://www.google.com/recaptcha/api.js";
    script.async = true;
    script.defer = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

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
    
    // Check if reCAPTCHA is loaded and verified
    // Note: window.grecaptcha might need a type definition or (window as any)
    const recaptchaResponse = (window as any).grecaptcha?.getResponse();
    
    if (!recaptchaResponse) {
      alert('Please complete the reCAPTCHA.');
      return;
    }

    const googleFormData = new FormData();
    // 2. FIX: Map your clean state keys to Google Entry IDs here, upon submission
    googleFormData.append('entry.2005620554', formData.fullName);
    googleFormData.append('entry.1045781291', formData.email);
    googleFormData.append('entry.839337160', formData.message);
    googleFormData.append('entry.670876903', recaptchaResponse);

    fetch('https://docs.google.com/forms/d/e/1FAIpQLSd-ORTakZ4IOBgNYOtuETuGr5X5I9a8xMa0kjfiJJVOyTIASg/formResponse', {
      method: 'POST',
      body: googleFormData,
      mode: 'no-cors',
    })
    .then(() => {
        setIsSubmitted(true);
    })
    .catch(() => {
        // Because of 'no-cors', errors are hard to catch, but good to have
        alert("There was an error submitting the form.");
    });
  };

  // Inline styles
  const inputStyle: React.CSSProperties = {
    backgroundColor: 'var(--warm-white, #f0f0f0)', // Fallback color added
    borderRadius: '5px',
    minHeight: '60px',
    marginBottom: '20px',
    border: '1px solid #ccc', // Added border for visibility
    padding: '0 15px'
  };

  const textareaStyle: React.CSSProperties = {
    ...inputStyle,
    minHeight: '140px',
    paddingTop: '14px',
    paddingBottom: '14px',
  };

  if (isSubmitted) {
    return (
      <div style={{ marginTop: '150px', textAlign: 'center' }}>
        <h3>Thank you!</h3>
        <p>Your submission has been processed.</p>
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

          #contact-form-name-label { grid-area: 1/1/2/2; }
          .contact-name-field      { grid-area: 2/1/3/2; }
          #contact-form-email-label{ grid-area: 1/2/2/3; }
          .contact-email-field     { grid-area: 2/2/3/3; }
          #contact-form-message-label { grid-area: 3/1/4/3; }
          .contact-message-field   { grid-area: 4/1/5/3; }
          
          /* Ensure container has size */
          .contact-recaptcha-field { 
            grid-area: 5/1/6/2; 
            min-height: 78px;
            margin-bottom: 20px;
          }
          
          #contact-form-submit {
            grid-area: 5/2/6/3;
            justify-self: end;
            height: 50px;
            padding: 0 30px;
            cursor: pointer;
          }

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
        `}
      </style>

      <div style={{ marginTop: '150px' }}>
        <h1 className="section-title">Contact Me</h1>
        <form 
          id="contact-form"
          onSubmit={handleSubmit}
        >
          <label id="contact-form-name-label" htmlFor="fullName">
            Full Name
          </label>
          <input
            id="fullName"
            className="form-input contact-name-field"
            style={inputStyle}
            type="text"
            /* 3. FIX: Name matches State key now */
            name="fullName" 
            value={formData.fullName}
            onChange={handleInputChange}
            placeholder="Leeroy Jenkins"
            maxLength={256}
            required
          />

          <label id="contact-form-email-label" htmlFor="email">
            Email Address
          </label>
          <input
            id="email"
            className="form-input contact-email-field"
            style={inputStyle}
            type="email"
            /* 3. FIX: Name matches State key now */
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            placeholder="JenkinsLeeroy@gmail.com"
            maxLength={256}
            required
          />

          <label id="contact-form-message-label" htmlFor="message">
            Message
          </label>
          <textarea
            id="message"
            className="textarea form-input contact-message-field"
            style={textareaStyle}
            /* 3. FIX: Name matches State key now */
            name="message"
            value={formData.message}
            onChange={handleInputChange}
            placeholder="Hello..."
            maxLength={5000}
          />

          {/* ReCAPTCHA Container */}
          <div className="g-recaptcha contact-recaptcha-field" 
               data-sitekey="6LeBU6gqAAAAAEJDe5diUdowY2Q0cwpk0GyEdSdy"></div>

          <input 
            id="contact-form-submit" 
            type="submit"
            className="project-cta-button button"
            value="Submit"
          />
        </form>
      </div>
    </>
  );
};

export default ContactForm;