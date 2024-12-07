import requests

from settings import configs
from settings.connections import azure_client
from cexceptions import ExternalSourceException


class MailRepository:
    client = azure_client
    base_url = (
        configs.ms_graph_api_base_url + "/users/" + configs.ms_graph_user + "/sendMail"
    )

    @classmethod
    def _get_token(cls):
        try:
            token = cls.client.get_token(configs.ms_graph_scope)
        except Exception as e:
            raise ExternalSourceException(source="Email Service", source_error=str(e))
        return token

    @classmethod
    def send_mail(
        cls,
        sender_email: str,
        recipients: list[str],
        subject: str,
        text: str | None = None,
        html_str: str | None = None,
        bcc: list[str] | None = None,
        cc: list[str] = None,
        reply_to: str = None,
    ) -> None:
        token = cls._get_token()
        email_data = {
            "message": {
                "subject": subject,
            }
        }
        headers = {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json",
        }
        if html_str:
            mail_body: dict = {
                "body": {
                    "contentType": "HTML",
                    "content": html_str,
                }
            }

        else:
            mail_body: dict = {  # type: ignore
                "body": {
                    "contentType": "Text",
                    "content": text,
                }
            }
        email_data["message"].update(mail_body)
        if recipients:
            recipients_list = [
                {"emailAddress": {"address": recipient_email}}
                for recipient_email in recipients
            ]
            email_data["message"]["toRecipients"] = recipients_list  # type: ignore

        if bcc:
            bcc_list = [{"emailAddress": {"address": bcc_email}} for bcc_email in bcc]
            email_data["message"]["bccRecipients"] = bcc_list  # type: ignore

        if cc:
            cc_list = [{"emailAddress": {"address": cc_email}} for cc_email in cc]
            email_data["message"]["ccRecipients"] = cc_list  # type: ignore
        if reply_to:
            email_data["message"]["replyTo"] = {  # type: ignore
                "emailAddress": {
                    "address": reply_to,
                }
            }
        email_data["message"]["from"] = {  # type: ignore
            "emailAddress": {
                "address": sender_email,
            }
        }
        try:
            response = requests.post(
                url=cls.base_url,
                headers=headers,
                json=email_data,
            )
            response.raise_for_status()
        except Exception as e:
            raise ExternalSourceException(source="Email Service", source_error=str(e))
        return None
