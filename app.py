import appJar
import payout


def press(btn):
    if btn == "submit":
        lines = ''.join(app.getTextArea("input")).split('\n')
        parsed = payout.parse_lines(lines)
        missing_str = ''
        if abs(sum(parsed[1]) - sum(parsed[2])) > payout.EPSILON:
            missing_str = "\nMissing profits/losses distributed evenly among players\n"
        app.setTextArea("output", payout.string_in_out(*parsed) + missing_str +
                        payout.string_payout(payout.compute_payout(*parsed)))
        app.go()


app = appJar.gui("Payout Calculator")
app.addTextArea("input")
app.setTextAreaWidth("input", 100)
app.setTextAreaHeight("input", 10)
app.setTextArea("input", "Input ledger here.")
app.addButton("submit", press)
app.addTextArea("output")
app.setTextAreaWidth("output", 100)
app.setTextAreaHeight("output", 30)
app.go()
