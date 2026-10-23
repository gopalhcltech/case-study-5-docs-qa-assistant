"""Create a print-ready Solstice Docs Q&A presentation PDF."""

from pathlib import Path

from export_architecture_pdf import make_content as architecture_content
from export_architecture_pdf import color, line, rectangle, text


PAGE_WIDTH = 792
PAGE_HEIGHT = 612
OUTPUT = Path(__file__).with_name("SOLSTICE_PRESENTATION.pdf")


def base_page(kicker, title, subtitle, page_number):
    commands = [
        rectangle(0, 0, PAGE_WIDTH, PAGE_HEIGHT, "#F3F6F0", "#F3F6F0", 0),
        text(38, 574, kicker, 8, "F2", "#18776B"),
        text(38, 542, title, 20, "F2"),
        text(38, 523, subtitle, 8, "F1", "#667874"),
        line(38, 508, 754, 508, "#D9E2DC", 1),
        line(38, 26, 754, 26, "#D9E2DC", 1),
        text(38, 12, "SOLSTICE LEARNING  /  DOCS Q&A", 7, "F2", "#667874"),
        text(736, 12, "%02d / 04" % page_number, 7, "F2", "#667874"),
    ]
    return commands


def cover_page():
    commands = [
        rectangle(0, 0, PAGE_WIDTH, PAGE_HEIGHT, "#F3F6F0", "#F3F6F0", 0),
        rectangle(0, 0, 18, PAGE_HEIGHT, "#18776B", "#18776B", 0),
        text(52, 555, "SOLSTICE LEARNING  /  SUPPORT ENGINEERING", 8, "F2", "#18776B"),
        text(52, 482, "Docs Q&A", 42, "F2", "#17312D"),
        text(52, 443, "A grounded-answer assistant for platform admins", 18, "F1", "#18776B"),
        text(52, 401, "PRESENTATION + LOCAL DEMO RUNBOOK", 9, "F2", "#667874"),
        rectangle(52, 327, 688, 48, "#D5ED70", "#D5ED70", 0),
        text(70, 356, "THE PROMISE", 8, "F2", "#17312D"),
        text(70, 339, "Answer from the docs, cite the source, or say the docs don't cover it.", 13, "F2", "#17312D"),
    ]
    cards = [
        (52, "EVIDENCE FIRST", "Short excerpts come directly\nfrom the matching article."),
        (287, "HONEST ABSTENTION", "Below the evidence threshold,\nreturn no invented answer."),
        (522, "LIGHTWEIGHT V1", "Python standard library; no\nLLM, API key, or paid service."),
    ]
    for x, title, detail in cards:
        commands.append(rectangle(x, 191, 218, 97, "#FFFFFF"))
        commands.append(text(x + 14, 262, title, 8, "F2", "#18776B"))
        first, second = detail.split("\n")
        commands.append(text(x + 14, 239, first, 9, "F1"))
        commands.append(text(x + 14, 224, second, 9, "F1"))
    commands.extend([
        text(52, 130, "IN THIS HANDOUT", 8, "F2", "#D96045"),
        text(52, 106, "01  Product + design    02  Architecture    03  Run and test    04  Demo outputs", 10, "F1"),
        line(52, 72, 740, 72, "#D9E2DC", 1),
        text(52, 51, "Local demo backed by six synthetic admin articles and five supplied test questions.", 8, "F1", "#667874"),
        text(52, 29, "01 / 04", 7, "F2", "#667874"),
    ])
    return "\n".join(commands).encode("ascii")


def architecture_page():
    return architecture_content()


def runbook_page():
    commands = base_page(
        "03 / EXECUTION RUNBOOK",
        "Run and verify the local app",
        "From the repository root. No virtual environment or package installation is required for this standard-library demo.",
        3,
    )
    commands.append(rectangle(38, 441, 716, 45, "#D5ED70", "#D5ED70", 0))
    commands.append(text(52, 466, "DEPENDENCIES", 8, "F2"))
    commands.append(text(162, 466, "Python 3.10+ only. No pip install, requirements file, LLM, or API key.", 9, "F2"))

    steps = [
        ("1", "Check Python", "python --version", "Use Python 3.10 or later."),
        ("2", "Run tests", "python -m unittest discover -s starter_kit -p 'test_*.py' -v", "Checks all five example questions, source selection, key facts, and abstention."),
        ("3", "Start the app", "python starter_kit/app.py", "Server listens on http://127.0.0.1:8000 by default."),
        ("4", "Open the browser", "http://127.0.0.1:8000", "Use a sample prompt or enter an admin question. Stop with Ctrl+C."),
    ]
    y_positions = [350, 270, 190, 110]
    for (number, title, command, note), y in zip(steps, y_positions):
        commands.append(rectangle(38, y, 716, 66, "#FFFFFF"))
        commands.append(rectangle(38, y, 33, 66, "#18776B", "#18776B", 0))
        commands.append(text(50, y + 39, number, 13, "F2", "#FFFFFF"))
        commands.append(text(84, y + 47, title.upper(), 8, "F2", "#18776B"))
        commands.append(text(84, y + 27, command, 9, "F2", "#17312D"))
        commands.append(text(84, y + 10, note, 8, "F1", "#667874"))
    commands.append(text(38, 54, "Optional port: PORT=8001 python starter_kit/app.py", 8, "F2", "#667874"))
    return "\n".join(commands).encode("ascii")


def demo_page():
    commands = base_page(
        "04 / LIVE DEMO",
        "Show the answer and the boundary",
        "Run the question in the browser, then contrast a documented fact with a deliberate no-answer.",
        4,
    )
    commands.append(rectangle(38, 348, 348, 133, "#FFFFFF"))
    commands.append(rectangle(38, 477, 348, 4, "#18776B", "#18776B", 0))
    commands.append(text(54, 457, "SUPPORTED QUESTION", 8, "F2", "#18776B"))
    commands.append(text(54, 438, "What's the maximum CSV export limit?", 10, "F2"))
    commands.append(text(54, 414, "CSV exports are capped at 10,000 rows.", 10, "F1"))
    commands.append(text(54, 396, "Source: Exporting Reports to CSV / D-03", 8, "F2", "#10574F"))
    commands.append(text(54, 370, "Answer is extracted from the docs; source is shown in the UI.", 8, "F1", "#667874"))

    commands.append(rectangle(406, 348, 348, 133, "#FFFFFF"))
    commands.append(rectangle(406, 477, 348, 4, "#D96045", "#D96045", 0))
    commands.append(text(422, 457, "NOT COVERED", 8, "F2", "#A84432"))
    commands.append(text(422, 438, "Can I connect Solstice to Salesforce?", 10, "F2"))
    commands.append(text(422, 414, "I don't have an answer for that in the", 10, "F1"))
    commands.append(text(422, 398, "documentation.", 10, "F1"))
    commands.append(text(422, 370, "No product integration is guessed or invented.", 8, "F1", "#667874"))

    commands.append(text(38, 318, "OPTIONAL API CHECK", 8, "F2", "#18776B"))
    commands.append(rectangle(38, 216, 716, 84, "#17312D", "#17312D", 0))
    commands.append(text(54, 277, "curl -sS -X POST http://127.0.0.1:8000/ask \\", 8, "F1", "#FFFFFF"))
    commands.append(text(54, 260, "  -H 'Content-Type: application/json' \\", 8, "F1", "#FFFFFF"))
    commands.append(text(54, 243, "  -d '{\"question\":\"What is the maximum CSV export limit?\"}'", 8, "F1", "#FFFFFF"))
    commands.append(text(38, 194, "Observed JSON response", 8, "F2", "#667874"))
    commands.append(rectangle(38, 83, 716, 96, "#FFFFFF"))
    commands.append(text(53, 160, '{"answered": true, "answer": "Important limit: CSV exports are capped at 10,000 rows...",', 8, "F1"))
    commands.append(text(53, 143, ' "source": {"doc_id": "D-03", "title": "Exporting Reports to CSV"},', 8, "F1"))
    commands.append(text(53, 126, ' "confidence": 0.785}', 8, "F1"))
    commands.append(text(53, 101, "The score is a heuristic ranking value, not calibrated probability; UI focuses on answer + citation.", 8, "F2", "#A84432"))
    commands.append(text(38, 52, "Decision rule: accept the top article at >= 0.50 weighted evidence; otherwise abstain.", 8, "F2", "#667874"))
    return "\n".join(commands).encode("ascii")


def write_pdf(pages):
    objects = [None, None,
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"]
    page_object_ids = [5 + 2 * index for index in range(len(pages))]
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join("%d 0 R" % object_id for object_id in page_object_ids)
    objects[1] = ("<< /Type /Pages /Kids [%s] /Count %d >>" % (kids, len(pages))).encode("ascii")

    for index, page_content in enumerate(pages):
        page_id = page_object_ids[index]
        stream_id = page_id + 1
        page = ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] "
                "/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents %d 0 R >>"
                % (PAGE_WIDTH, PAGE_HEIGHT, stream_id)).encode("ascii")
        stream = b"<< /Length %d >>\nstream\n%s\nendstream" % (len(page_content), page_content)
        objects.extend([page, stream])

    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(("%d 0 obj\n" % index).encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref_offset = len(output)
    output.extend(("xref\n0 %d\n" % (len(objects) + 1)).encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(("%010d 00000 n \n" % offset).encode("ascii"))
    output.extend(("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
                   % (len(objects) + 1, xref_offset)).encode("ascii"))
    OUTPUT.write_bytes(output)


if __name__ == "__main__":
    write_pdf([cover_page(), architecture_page(), runbook_page(), demo_page()])
    print("Wrote %s" % OUTPUT)