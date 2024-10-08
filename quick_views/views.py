from django.core.paginator import Paginator
from django.shortcuts import render
from .view_fragments.table.table import Table, TableConfig


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
        {
            "name": "Adam",
            "age": 14,
            "city": "Olsztyn",
            "attributes": {"height": "4ft", "weight": "120lbs"},
        },
        {
            "name": "Michal",
            "age": 21,
            "city": "Warszawa",
            "attributes": {"height": "5ft", "weight": "123lbs"},
        },
        {
            "name": "Julian",
            "age": 26,
            "city": "Warszawa",
            "attributes": {"height": "6ft", "weight": "113lbs"},
        },
    ]

    page_number = request.GET.get("page", 1)

    paginator = Paginator(data, page_size)

    page_obj = paginator.get_page(page_number)

    # Define custom template for rendering the 'attributes' column
    column_templates = {"attributes": "json_column.html"}

    config = TableConfig(
        "test_table",
        ["name", "age", "city", "attributes"],
        sortable=True,
        is_paginated=True,
        current_url=request.get_full_path(),
        column_templates=column_templates,
    )

    table = Table(
        data=page_obj.object_list(),
        config=config,
    )
    return render(request, "my_template.html", {"table": table})
