"""Generate a one-page architecture diagram PDF using only the standard library."""

from pathlib import Path


PAGE_WIDTH = 792
PAGE_HEIGHT = 612
OUTPUT = Path(__file__).with_name("ARCHITECTURE.pdf")


def color(hex_color):
    values = [int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    return " ".join("%.3f" % value for value in values)


def text(x, y, value, size=9, font="F1", fill="#17312D"):
    safe_value = value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return "%s rg BT /%s %s Tf 1 0 0 1 %s %s Tm (%s) Tj ET" % (
        color(fill), font, size, x, y, safe_value
    )


def rectangle(x, y, width, height, fill, stroke="#D9E2DC", line_width=1):
    return "%s rg %s RG %s w %s %s %s %s re B" % (
        color(fill), color(stroke), line_width, x, y, width, height
    )


def line(x1, y1, x2, y2, stroke="#18776B", line_width=1.5):
    return "%s RG %s w %s %s m %s %s l S" % (
        color(stroke), line_width, x1, y1, x2, y2
    )


def arrow(x1, y1, x2, y2, direction="right", stroke="#18776B"):
    commands = [line(x1, y1, x2, y2, stroke)]
    if direction == "right":
        points = [(x2 - 6, y2 + 4), (x2, y2), (x2 - 6, y2 - 4)]
    elif direction == "left":
        points = [(x2 + 6, y2 + 4), (x2, y2), (x2 + 6, y2 - 4)]
    elif direction == "up":
        points = [(x2 - 4, y2 - 6), (x2, y2), (x2 + 4, y2 - 6)]
    else:
        points = [(x2 - 4, y2 + 6), (x2, y2), (x2 + 4, y2 + 6)]
    commands.append("%s RG 1.5 w %s %s m %s %s l %s %s l S" % (
        color(stroke), *points[0], *points[1], *points[2]
    ))
    return commands


def box(commands, x, y, width, height, label, title, details, accent="#18776B"):
    commands.append(rectangle(x, y, width, height, "#FFFFFF"))
    commands.append(rectangle(x, y + height - 4, width, 4, accent, accent, 0))
    commands.append(text(x + 15, y + height - 22, label, 7, "F2", accent))
    commands.append(text(x + 15, y + height - 43, title, 13, "F2"))
    for index, detail in enumerate(details):
        commands.append(text(x + 15, y + height - 64 - index * 15, detail, 8))


def make_content():
    commands = [
        rectangle(0, 0, PAGE_WIDTH, PAGE_HEIGHT, "#F3F6F0", "#F3F6F0", 0),
        text(38, 566, "SOLSTICE / DOCS Q&A", 8, "F2", "#18776B"),
        text(38, 532, "Answer flow and system boundaries", 22, "F2"),
        text(38, 513, "LOCAL WEB APP  /  EXTRACTIVE RETRIEVAL  /  NO LLM", 8, "F1", "#667874"),
        line(38, 498, 754, 498, "#D9E2DC", 1),
    ]

    box(commands, 38, 326, 195, 158, "01 / USER", "Admin browser", [
        "index.html",
        "Question input + examples",
        "Displays source excerpts",
        "or an honest abstention",
    ])
    box(commands, 298, 326, 195, 158, "02 / HTTP", "Python app", [
        "app.py",
        "GET / serves the interface",
        "POST /ask accepts question JSON",
        "GET /health reports status",
    ], "#D96045")
    box(commands, 558, 326, 196, 158, "03 / DECISION", "Retrieval policy", [
        "retrieval.py",
        "Normalize and weight query terms",
        "Score title + article content",
        "Require score >= 0.50",
        "Return up to 2 source sentences",
        "Otherwise: abstain",
    ], "#B0C840")
    box(commands, 558, 111, 196, 138, "04 / KNOWLEDGE", "Documentation", [
        "data/docs.json",
        "6 articles loaded at startup",
        "All positive answers cite a source",
        "No external service or model",
    ], "#D96045")

    commands.extend(arrow(233, 447, 298, 447, "right"))
    commands.append(text(239, 458, "POST /ask", 7, "F2", "#10574F"))
    commands.extend(arrow(298, 382, 233, 382, "left", "#D96045"))
    commands.append(text(239, 369, "ANSWER JSON", 7, "F2", "#A84432"))

    commands.extend(arrow(493, 447, 558, 447, "right"))
    commands.append(text(515, 458, "query", 7, "F2", "#10574F"))
    commands.extend(arrow(558, 382, 493, 382, "left", "#D96045"))
    commands.append(text(520, 369, "result", 7, "F2", "#A84432"))

    commands.extend(arrow(656, 249, 656, 326, "up"))
    commands.append(text(665, 281, "corpus", 7, "F2", "#10574F"))

    commands.append(rectangle(38, 75, 716, 17, "#D5ED70", "#D5ED70", 0))
    commands.append(text(48, 80, "GROUNDED ANSWERS", 7, "F2", "#17312D"))
    commands.append(text(180, 80, "Query -> ranked article -> evidence threshold -> cited excerpts OR documented no-answer", 7, "F1"))
    commands.append(text(38, 49, "Threshold is a v1 policy (not calibrated confidence); validate against real support questions before production.", 8, "F1", "#667874"))
    commands.append(text(38, 29, "Generated from the current implementation. See export_architecture_pdf.py to regenerate.", 7, "F1", "#667874"))
    return "\n".join(commands).encode("ascii")


def write_pdf(content):
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %s %s] "
         "/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>"
         % (PAGE_WIDTH, PAGE_HEIGHT)).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
        b"<< /Length %d >>\nstream\n%s\nendstream" % (len(content), content),
    ]
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
    write_pdf(make_content())
    print("Wrote %s" % OUTPUT)