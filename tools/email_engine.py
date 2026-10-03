import os,smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
class EmailEngine:
 def __init__(self):self.email=os.getenv("PHANTOMOPS_SMTP_USER","");self.password=os.getenv("PHANTOMOPS_SMTP_PASSWORD","");self.host=os.getenv("PHANTOMOPS_SMTP_HOST","smtp.gmail.com");self.port=int(os.getenv("PHANTOMOPS_SMTP_PORT","587"))
 def send_email(self,to_email,subject,body):
  if not self.email or not self.password:return {"success":False,"error":"SMTP credentials are not configured in environment variables"}
  try:
   m=MIMEMultipart();m["From"]=self.email;m["To"]=to_email;m["Subject"]=subject;m.attach(MIMEText(body,"plain"));server=smtplib.SMTP(self.host,self.port);server.starttls();server.login(self.email,self.password);server.sendmail(self.email,to_email,m.as_string());server.quit();return {"success":True}
  except Exception as e:return {"success":False,"error":str(e)}
 def generate_subject(self,project):return f"AI Automation Proposal for {project.get('marketplace','Opportunity')}"
 def generate_email_body(self,project):return f"Hello,\n\nI recently reviewed your project opportunity.\n\n{project.get('generated_proposal','')}\n\nBest regards,\nPhantomOps AI"
 def send_project_proposal(self,project,email):return self.send_email(email,self.generate_subject(project),self.generate_email_body(project))
email_engine=EmailEngine()
