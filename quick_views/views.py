from django.shortcuts import render
from .table import Table, TableConfig


def my_view(request):
    data = [
        {
            "name": "Alice",
            "age": 30,
            "city": "New York",
            "attributes": {"height": "5ft 5in", "weight": "130lbs"},
        },
        {
            "name": "Bob",
            "age": 25,
            "city": "Los Angeles",
            "attributes": {"height": "5ft 9in", "weight": "150lbs"},
        },
        {
            "name": "Charlie",
            "age": 35,
            "city": "Chicago",
            "attributes": {"height": "6ft", "weight": "180lbs"},
        },
    ]
    config = TableConfig(
        ["name", "age", "city", "attributes"],
        sortable=True,
        page_size=5,
        current_page=1,
    )

    # Define custom template for rendering the 'attributes' column
    column_templates = {"attributes": "json_column.html"}

    table = Table(data, config, column_templates=column_templates)

    return render(request, "my_template.html", {"table": table})
