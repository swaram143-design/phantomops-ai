import requests


class LiveMarketplaceScraper:

    def __init__(self):

        self.headers = {

            "User-Agent":
                "Mozilla/5.0"
        }

    def scrape_remoteok(
        self
    ):

        projects = []

        try:

            response = requests.get(
                "https://remoteok.com/api",
                headers=self.headers,
                timeout=20
            )

            data = response.json()

            for item in data[1:15]:

                title = (
                    item.get(
                        "position",
                        ""
                    )
                )

                company = (
                    item.get(
                        "company",
                        "Unknown"
                    )
                )

                tags = (
                    item.get(
                        "tags",
                        []
                    )
                )

                description = (
                    " ".join(tags)
                )

                projects.append(
                    {

                        "title":
                            title,

                        "description":
                            description,

                        "client":
                            f"{company.lower()}@remoteok.fake"
                    }
                )

        except Exception as error:

            print(
                f"[Scraper Error] "
                f"{error}"
            )

        return projects


live_marketplace_scraper = (
    LiveMarketplaceScraper()
)