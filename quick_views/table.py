from typing import Dict, Optional, Any
from dataclasses import dataclass
from django.core.paginator import Page
from django.template import loader


@dataclass
class TableConfig:
    table_name: str = "table"  # Unique name for the table to namespace parameters
    columns: Optional[list[str]] = None  # Configuration for table columns
    sortable: bool = False  # Enable/disable sorting
    sort_column: Optional[str] = None  # Column to sort by
    sort_reverse: bool = False  # Whether to sort in descending order


# TODO: Extract page info extraction to the wrapper this class should take data in plain and form so in form of list and numbers
class Table:
    def __init__(
        self,
        page: Page,
        config: Optional[TableConfig] = None,
        template_name: str = "default_table.html",
        column_templates: Optional[Dict[str, str]] = None,
        current_url: str = "",
    ):
        """
        Args:
            page (Page): A paginated subset of data (Django's Page object).
            config (TableConfig): Configuration options for the table (e.g., columns, sortable).
            template_name (str): The default template to use for the table structure.
            column_templates (dict): A dictionary where the key is the column name and the value is the template path.
            current_url (str): The current URL with query parameters.
        """
        self.page = page
        self.config: TableConfig = config or TableConfig(table_name="default")
        self.template_name: str = template_name
        self.column_templates: Dict[str, str] = column_templates or {}
        self.current_url = current_url

        # Set columns
        self.columns: list[str] = self.config.columns or []
        if not self.columns and self.page.object_list:
            self.columns = list(self.page.object_list[0].keys())

    def get_context(self) -> Dict[str, Any]:
        """
        Prepare the context for rendering the table.

        Returns:
            dict: The context dictionary to use for rendering.
        """
        return {
            "data": self.page.object_list,
            "columns": self.columns,
            "column_templates": self.column_templates,
            "is_paginated": self.page.paginator.num_pages > 1,
            "current_page": self.page.number,
            "total_pages": self.page.paginator.num_pages,
            "has_next": self.page.has_next(),
            "has_previous": self.page.has_previous(),
            "sortable": self.config.sortable,
            "sort_column": self.config.sort_column,
            "sort_reverse": self.config.sort_reverse,
            "table_name": self.config.table_name,
            "current_url": self.current_url,
        }

    def render(self) -> str:
        """
        Render the table using the template.

        Returns:
            str: The rendered HTML of the table.
        """
        template = loader.get_template(self.template_name)
        return template.render(self.get_context())
