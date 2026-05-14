import os

from datetime import (
    datetime
)

from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer

)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import (
    letter
)


class PDFProposalEngine:

    def __init__(self):

        self.output_dir = (
            "generated_proposals"
        )

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    def generate_pdf(
        self,
        company,
        proposal_text
    ):

        filename = (

            f"{company}"
            f"_proposal.pdf"

        ).replace(
            " ",
            "_"
        )

        filepath = os.path.join(
            self.output_dir,
            filename
        )

        doc = (
            SimpleDocTemplate(
                filepath,
                pagesize=letter
            )
        )

        styles = (
            getSampleStyleSheet()
        )

        story = []

        title = (
            Paragraph(
                "PHANTOMOPS AI PROPOSAL",
                styles["Title"]
            )
        )

        story.append(
            title
        )

        story.append(
            Spacer(
                1,
                20
            )
        )

        generated = (
            Paragraph(
                f"Generated: "
                f"{datetime.now()}",
                styles["BodyText"]
            )
        )

        story.append(
            generated
        )

        story.append(
            Spacer(
                1,
                20
            )
        )

        paragraphs = (
            proposal_text.split(
                "\n"
            )
        )

        for line in paragraphs:

            if line.strip():

                paragraph = (
                    Paragraph(
                        line,
                        styles["BodyText"]
                    )
                )

                story.append(
                    paragraph
                )

                story.append(
                    Spacer(
                        1,
                        12
                    )
                )

        doc.build(
            story
        )

        return filepath


pdf_proposal_engine = (
    PDFProposalEngine()
)