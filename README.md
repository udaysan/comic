# comic
Requirements:
Python 3.10.8 
Flask 3.0.0
Pillow 10.1.0


Configuration in app.py:
1) This configuration is to enable comic sharing over email.
2) Update the email (smtp_username) and device-specific password (smtp_password) for the corresponding mail in the send_email function of app.py.

Steps to Genearte comic:
1) Run the app.py file.
![Alt text](images/web_page_before_entering_text.png)
2) Enter text in all 10 panels. After that, you can view the generate comic button and click on it.
![Alt text](images/web_page_during_backend_process.png)
3) It will take some time to generate the image.
![Alt text](images/comic_image.png)
4) Once the back-end process is completed, an image will be displayed on the webpage.
5) This page also has options to generate new comics, download generated comics, and share the comics over email.
![Alt text](images/enter_email_address.png)
6) To share comics over mail, make sure you have configured app.py with mail and a device-specific password for the corresponding mail.
![Alt text](images/comic_strip_mail.png)