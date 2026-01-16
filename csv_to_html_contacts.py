import csv

input_csv = "contacts.csv"      # Your exported Google CSV
output_html = "contacts.html"   # Output HTML file for GitHub Pages

def get_labeled_columns(row, prefix):
    """
    Return list of tuples (label, value) for a given prefix
    Only columns with 'Value' in the header are used
    """
    labeled_values = []
    for key, value in row.items():
        if key.startswith(prefix) and "Value" in key and value:
            num = key.split()[1]  # 'E-mail 1 - Value' -> '1'
            type_key = f"{prefix} {num} - Type"
            label = row.get(type_key, "").strip()
            labeled_values.append((label, value))
    return labeled_values

with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

with open(output_html, 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<title>Contacts</title>
<style>
body { font-family: Arial, sans-serif; }
#search { margin-bottom: 10px; padding: 5px; width: 300px; }
.scrollable { max-height: 600px; overflow: auto; border: 1px solid #999; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #999; padding: 5px; text-align: left; vertical-align: top; }
th { position: sticky; top: 0; background: #f2f2f2; z-index: 1; }
.label { font-weight: bold; color: #555; margin-right: 3px; }
/* Alternating row colors */
tr:nth-child(even) { background-color: #f9f9f9; }
tr:nth-child(odd) { background-color: #ffffff; }
</style>
</head>
<body>
<h1>Contacts</h1>
<input type="text" id="search" onkeyup="searchTable()" placeholder="Search contacts...">
<div class="scrollable">
<table id="contactsTable">
<tr><th>Name</th><th>Phones</th><th>Emails</th></tr>
""")

    for row in rows:
        # Combine First, Middle, Last names
        parts = [row.get("First Name", ""), row.get("Middle Name", ""), row.get("Last Name", "")]
        name = " ".join([p for p in parts if p]).strip()

        # Emails and Phones with labels
        emails = get_labeled_columns(row, "E-mail")
        phones = get_labeled_columns(row, "Phone")

        email_links = ", ".join(
            f"<span class='label'>{lbl}</span><a href='mailto:{val}'>{val}</a>" if lbl else f"<a href='mailto:{val}'>{val}</a>"
            for lbl, val in emails
        )

        phone_links = ", ".join(
            f"<span class='label'>{lbl}</span><a href='tel:{val}'>{val}</a>" if lbl else f"<a href='tel:{val}'>{val}</a>"
            for lbl, val in phones
        )

        # Column order: Name | Phones | Emails
        f.write(f"<tr><td>{name}</td><td>{phone_links}</td><td>{email_links}</td></tr>\n")

    f.write("""</table>
</div>
<script>
function searchTable() {
    const input = document.getElementById('search');
    const filter = input.value.toLowerCase();
    const table = document.getElementById('contactsTable');
    const tr = table.getElementsByTagName('tr');

    for (let i = 1; i < tr.length; i++) {
        const tds = tr[i].getElementsByTagName('td');
        let show = false;
        for (let j = 0; j < tds.length; j++) {
            if (tds[j].textContent.toLowerCase().indexOf(filter) > -1) {
                show = true;
                break;
            }
        }
        tr[i].style.display = show ? '' : 'none';
    }
}
</script>
</body>
</html>""")

print(f"Interactive HTML contacts file with sticky headers, alternating row colors, and swapped columns created: {output_html}")

