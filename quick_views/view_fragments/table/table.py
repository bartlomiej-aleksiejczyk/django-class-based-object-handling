from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from django.template import loader


@dataclass
class TableConfig:
    table_name: str = "table"  # Unique name for the table to namespace parameters
    columns: Optional[List[str]] = None  # Configuration for table columns
    sortable: bool = False  # Enable/disable sorting
    sort_column: Optional[str] = None  # Column to sort by
    sort_reverse: bool = False  # Whether to sort in descending order
    is_paginated: bool = False
    current_page: int = 1  # Current page number for pagination
    total_pages: int = 1  # Total number of pages for pagination
    has_next: bool = False  # Whether there's a next page
    has_previous: bool = False  # Whether there's a previous page
    template_name: str = (
        "default_table.html"  # Default template to use for the table structure
    )
    column_templates: Optional[Dict[str, str]] = (
        None  # Template paths for specific columns
    )
    current_url: str = ""  # The current URL with query parameters


class Table:
    def __init__(
        self,
        data: List[Dict[str, Any]],
        config: Optional[TableConfig] = None,
    ):
        """
        Args:
            data (list): A list of dictionaries representing the data rows.
            config (TableConfig): Configuration options for the table (e.g., columns, sortable).
        """
        self.data = data
        self.config: TableConfig = config or TableConfig(table_name="default")

        # Set columns
        self.columns: List[str] = self.config.columns or []
        if not self.columns and self.data:
            self.columns = list(self.data[0].keys())

    def get_context(self) -> Dict[str, Any]:
        """
        Prepare the context for rendering the table.

        Returns:
            dict: The context dictionary to use for rendering.
        """
        return {
            "data": self.data,
            "columns": self.columns,
            "column_templates": self.config.column_templates or {},
            "is_paginated": self.config.is_paginated,
            "current_page": self.config.current_page,
            "total_pages": self.config.total_pages,
            "has_next": self.config.has_next,
            "has_previous": self.config.has_previous,
            "sortable": self.config.sortable,
            "sort_column": self.config.sort_column,
            "sort_reverse": self.config.sort_reverse,
            "table_name": self.config.table_name,
            "current_url": self.config.current_url,
        }

    def render(self) -> str:
        """
        Render the table using the template.

        Returns:
            str: The rendered HTML of the table.
        """
        template = loader.get_template(self.config.template_name)
        return template.render(self.get_context())
