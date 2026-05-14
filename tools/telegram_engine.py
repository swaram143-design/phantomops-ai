import requests


class TelegramEngine:

    def __init__(self):

        self.bot_token = (
            "8246686795:AAGxU533CPCrleLOcyaDmFSE3g_AJjttnSE"
        )

        self.chat_id = (
            "7238244143s"
        )

    def send_message(
        self,
        message
    ):

        url = (
            f"https://api.telegram.org/bot"
            f"{self.bot_token}/sendMessage"
        )

        payload = {

            "chat_id":
                self.chat_id,

            "text":
                message
        }

        try:

            response = (
                requests.post(
                    url,
                    json=payload,
                    timeout=30
                )
            )

            return {

                "success":
                    response.status_code == 200
            }

        except Exception as error:

            return {

                "success": False,

                "error":
                    str(error)
            }

    def send_opportunity_alert(
        self,
        project
    ):

        message = f"""
🚀 HIGH VALUE OPPORTUNITY

Marketplace:
{project.get('marketplace')}

Score:
{project.get('opportunity_score')}

Priority:
{project.get('priority_action')}

Probability:
{project.get('close_probability')}%

Deal Value:
{project.get('estimated_deal_value')}

Skills:
{', '.join(
    project.get(
        'project_analysis',
        {}
    ).get(
        'skills',
        []
    )
)}

Follow-up:
{project.get('next_followup')}
"""

        return self.send_message(
            message
        )


telegram_engine = (
    TelegramEngine()
)