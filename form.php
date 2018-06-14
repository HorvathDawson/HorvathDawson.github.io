< ?php 
if (isset($_POST['submit'])) 
{ 
 $name = $_POST['name']; 
 $email = $_POST['email'];
 $message = $_POST['message'];
 $from = 'Website Contact Form';
 $to = 'Horvath.dawson@gmail.com'; 
 $subject = 'Email Inquiry';
 $body = "From: $name\n E-Mail: $email\n Message:\n $message";

 if (mail ($to, $subject, $body, $from))
	{ 
		header ('Location: index.html');
	}
 else 
	{ 
	echo 'Oops! An error occurred. Try sending your message again.';
	}
}?>