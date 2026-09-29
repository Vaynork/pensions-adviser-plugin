"""Build the fictional sample fillable fact-find used in examples/.

Usage:
    python examples/make_sample_form.py

Writes examples/sample-firm-fact-find.pdf: a short, two-client, fillable PDF
for the fictional "Harbour Lane Financial Planning Ltd". It exists so anyone
can try /fact-find-setup and /fact-find without using a real firm's form.
Needs reportlab (python -m pip install reportlab).
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parent / "sample-firm-fact-find.pdf"
W, H = A4


def heading(c, y, text):
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, text)
    return y - 22


def text_row(c, y, label, names, width=170):
    c.setFont("Helvetica", 9)
    c.drawString(40, y + 4, label)
    for i, name in enumerate(names):
        c.acroForm.textfield(name=name, tooltip=label, x=230 + i * (width + 10), y=y, width=width, height=16,
                             borderWidth=0.5, fontSize=9)
    return y - 24


def check_row(c, y, label, names):
    c.setFont("Helvetica", 9)
    c.drawString(40, y + 4, label)
    for i, name in enumerate(names):
        c.acroForm.checkbox(name=name, tooltip=label, x=230 + i * 180, y=y, size=14, buttonStyle="check")
    return y - 24


def main():
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("Harbour Lane Financial Planning — Retirement Fact-Find (fictional sample)")

    c.setFont("Helvetica-Bold", 15)
    c.drawString(40, H - 50, "Harbour Lane Financial Planning Ltd — Retirement Fact-Find")
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(40, H - 64, "FICTIONAL SAMPLE FORM for trying the Pensions Adviser (UK) plugin. Not a real firm.")

    y = H - 95
    c.setFont("Helvetica-Bold", 9)
    c.drawString(230, y, "Client 1")
    c.drawString(410, y, "Client 2")
    y -= 20
    y = heading(c, y, "1. About you")
    y = text_row(c, y, "Full name", ["C1_FullName", "C2_FullName"])
    y = text_row(c, y, "Date of birth", ["C1_DOB", "C2_DOB"])
    y = text_row(c, y, "NI number", ["C1_NINO", "C2_NINO"])
    y = text_row(c, y, "Occupation", ["C1_Occupation", "C2_Occupation"])
    y = text_row(c, y, "Planned retirement age", ["C1_RetAge", "C2_RetAge"])
    y = check_row(c, y, "Smoker?", ["C1_Smoker", "C2_Smoker"])

    y = heading(c, y - 6, "2. Your home")
    y = text_row(c, y, "Home address", ["Joint_Address"], width=350)

    y = heading(c, y - 6, "3. Pension plans")
    c.setFont("Helvetica-Bold", 8)
    for x, label in ((40, "Owner"), (120, "Provider"), (260, "Type"), (360, "Value (£)"), (450, "Guarantees?")):
        c.drawString(x, y + 4, label)
    y -= 18
    for n in range(1, 4):
        c.acroForm.textfield(name=f"Pen{n}_Owner", tooltip=f"Pension {n} owner", x=40, y=y, width=70, height=16, borderWidth=0.5, fontSize=8)
        c.acroForm.textfield(name=f"Pen{n}_Provider", tooltip=f"Pension {n} provider", x=120, y=y, width=130, height=16, borderWidth=0.5, fontSize=8)
        c.acroForm.textfield(name=f"Pen{n}_Type", tooltip=f"Pension {n} type", x=260, y=y, width=90, height=16, borderWidth=0.5, fontSize=8)
        c.acroForm.textfield(name=f"Pen{n}_Value", tooltip=f"Pension {n} value", x=360, y=y, width=80, height=16, borderWidth=0.5, fontSize=8)
        c.acroForm.textfield(name=f"Pen{n}_Guarantees", tooltip=f"Pension {n} guarantees", x=450, y=y, width=110, height=16, borderWidth=0.5, fontSize=8)
        y -= 22

    y = heading(c, y - 6, "4. What you want to achieve")
    c.setFont("Helvetica", 9)
    c.drawString(40, y + 4, "Your objectives")
    c.acroForm.textfield(name="Objectives", tooltip="Your objectives", x=230, y=y - 40, width=350, height=56,
                         borderWidth=0.5, fontSize=9, fieldFlags="multiline")
    y -= 70
    y = text_row(c, y, "Retirement income wanted (£ a year)", ["IncomeTarget"], width=170)

    y = heading(c, y - 6, "5. Risk (adviser to complete)")
    y = text_row(c, y, "Risk profile result", ["C1_RiskResult", "C2_RiskResult"])

    y = heading(c, y - 6, "6. Declaration")
    y = check_row(c, y, "I confirm the information is correct", ["C1_Declare", "C2_Declare"])
    y = text_row(c, y, "Signature", ["C1_Signature", "C2_Signature"])

    c.save()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
