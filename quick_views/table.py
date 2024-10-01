from django.template import loader
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from django.core.paginator import Paginator


@dataclass
class TableConfig:
    columns: Optional[List[str]] = None  # Configuration for table columns
    sortable: bool = False  # Enable/disable sorting
    page_size: int = 10  # Number of rows per page
    current_page: int = 1  # Current page for pagination


class Table:
    def __init__(
        self,
        data: List[Dict[str, Any]],
        config: Optional[TableConfig] = None,
        template_name: str = "default_table.html",
        column_templates: Optional[Dict[str, str]] = None,
    ):
        """
        Args:
            data (list of dicts): The data to render in the table.
            config (TableConfig): Configuration options for the table (e.g., columns, sortable, pagination).
            template_name (str): The default template to use for the table structure.
            column_templates (dict): A dictionary where the key is the column name and the value is the template path.
        """
        self.data: List[Dict[str, Any]] = data
        self.config: TableConfig = config or TableConfig()
        self.template_name: str = template_name
        self.column_templates: Dict[str, str] = column_templates or {}

        # Set columns
        self.columns: List[str] = self.config.columns or []
        if not self.columns and self.data:
            self.columns = list(self.data[0].keys())

        # Handle pagination
        self.paginator = Paginator(self.data, self.config.page_size)
        self.current_page = self.config.current_page

        try:
            self.page_data = self.paginator.page(self.current_page).object_list
        except:
            self.page_data = self.paginator.page(1).object_list

    def get_context(self) -> Dict[str, Any]:
        """
        Prepare the context for rendering the table.

        Returns:
            dict: The context dictionary to use for rendering.
        """
        return {
            "data": self.page_data,
            "columns": self.columns,
            "column_templates": self.column_templates,
            "is_paginated": self.paginator.num_pages > 1,
            "current_page": self.current_page,
            "total_pages": self.paginator.num_pages,
            "has_next": self.current_page < self.paginator.num_pages,
            "has_previous": self.current_page > 1,
            "sortable": self.config.sortable,
        }

    def render(self) -> str:
        """
        Render the table using the template.

        Returns:
            str: The rendered HTML of the table.
        """
        template = loader.get_template(self.template_name)
        return template.render(self.get_context())
