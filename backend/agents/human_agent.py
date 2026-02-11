import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.state.agent_state import AgentState


class HumanAgent:

    def __init__(self,agent_email: str,ticket_id: str,customer_email: str,issue_summary: str,):
        self.agent_email = agent_email
        self.ticket_id = ticket_id
        self.customer_email = customer_email
        self.issue_summary = issue_summary

    def send_escalation_email(self,state:AgentState):
        sender_email = "amit.rock9889@gmail.com"  ## company email 
        sender_password = "tqnb nurm tucc utvn"  # app password recommended

        subject = f"[Escalation] Ticket #{self.ticket_id} - Customer Support Required"

        body = f"""
        New customer issue has been escalated.

        Ticket ID: {self.ticket_id}
        Customer Email: {self.customer_email}

        Issue Summary:
        {self.issue_summary}

        Please review and respond to the customer.
        """

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = self.agent_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return {"answer":"I’ve shared your request with our support team.They’ll reach out to you at your email address shortly"}

            