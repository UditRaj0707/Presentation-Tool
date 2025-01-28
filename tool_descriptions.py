TOOL_DESCRIPTIONS = {
    "add_waterfall_chart": """
        Purpose: Add a slide with a waterfall chart that visually represents incremental changes and totals.

        **Key Use Cases**:
        - Visualizing changes in data over categories, such as expenses, revenue, or margins.
        - Showing the impact of positive and negative contributions on a cumulative total.
        - Displaying totals explicitly if provided or calculated dynamically.

        **Input Format**:
        - `categories_str`: Comma-separated string of category names (e.g., "Category 1, Category 2, Category 3").
        - `values_str`: Comma-separated string of incremental values (e.g., "100, 20, 50, -40, 130, -60, 70, 140").
        - `title`: Title of the slide.
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted. (e.g., insert_at="2")
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_waterfall_chart(
            categories_str="Category 1, Category 2, Category 3, Category 4",
            values_str="100, 20, -10, 30",
            title="Waterfall Chart Example",
            insert_at="2"
        )
    """,
    "add_image_slide": """
        Purpose: Add a slide with an image and a caption.

        **Key Use Cases**:
        - Displaying product images, charts, or visual content.
        - Adding a visual representation with a caption.

        **Input Format**:
        - `image_path`: Path to the image file.
        - `caption`: Caption text for the image.
        - `title`: Title of the slide.
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted. (e.g., insert_at="2")
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_image_slide(image_path='<path_to_image>', caption='Image description', title='Slide Title', insert_at=3)
    """,
    "add_text_with_image_slide": """
        Purpose: Add a slide with a text and image.

        **Key Use Cases**:
        - Combining visual and textual information in one slide.
        - Presenting descriptive text alongside an image.

        **Input Format**:
        - `text_content`: Text content for the slide, separated by paragraphs.
        - `image_path`: Path to the image file.
        - `title`: Title of the slide.
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted.
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_text_with_image_slide(text_content='Paragraph 1.\\n\\nParagraph 2.', image_path='<path_to_image>', title='Slide Title', insert_at="1")
    """,
    "add_bullet_slide": """
        Purpose: Create a slide with bullet points.

        **Key Use Cases**:
        - Listing key points, ideas, or steps.
        - Structuring information concisely.

        **Input Format**:
        - `title`: Title of the slide.
        - `content`: Bullet points separated by semicolons.
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted. (e.g., insert_at="2")
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_bullet_slide(title='Slide Title', content='First point; Second point; Third point', insert_at="4")
    """,
    "add_two_content_bullet_slide": """
        Purpose: Create a slide with two columns of bullet points.

        **Key Use Cases**:
        - Comparing two sets of information side-by-side.
        - Displaying pros and cons or feature comparisons.

        **Input Format**:
        - `title`: Title of the slide.
        - `left_content`: Bullet points for the left column, separated by semicolons.
        - `right_content`: Bullet points for the right column, separated by semicolons.
        - `insert_at`: Optional parameter (integer) specifying the slide index where the slide should be inserted.
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_two_content_bullet_slide(title='Slide Title', left_content='Point 1; Point 2; Point 3', right_content='Item A; Item B; Item C', insert_at=2)
    """,
    "add_table_slide": """
        Purpose: Add a comparison table to the presentation.

        **Key Use Cases**:
        - Comparing data in a structured table format.
        - Displaying tabular information clearly.

        **Input Format**:
        - `title`: Title of the slide.
        - `table_data`: Tabular data in the format "Header1, Header2; Value1, Value2; Value3, Value4".
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted. (e.g., insert_at="2")
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_table_slide(title='Comparison Table', table_data='Header1, Header2; Value1, Value2; Value3, Value4', insert_at="5")
    """,
    "add_bar_chart": """
        Purpose: Create a slide with a clustered bar chart for comparing multiple data series.

        **Key Use Cases**:
        - Visualizing comparative data across multiple categories.
        - Highlighting differences between series.

        **Input Format**:
        - `categories_str`: Comma-separated string of categories.
        - `series_data_str`: Data for multiple series in the format "Series1: values; Series2: values".
        - `title`: Title of the slide.
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted. (e.g., insert_at="2")
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_bar_chart(categories_str='Category A, Category B, Category C', series_data_str='Sales: 50, 70, 90', title='Sales Comparison', insert_at="1")
    """,
    "add_line_chart": """
        Purpose: Create a slide with a multi-series line chart.

        **Key Use Cases**:
        - Showing trends over time across multiple series.
        - Visualizing performance metrics or comparisons.

        **Input Format**:
        - `categories_str`: Comma-separated string of categories.
        - `series_data_str`: Data for multiple series in the format "Series1: values; Series2: values".
        - `title`: Title of the slide.
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted. (e.g., insert_at="2")
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_line_chart(categories_str='Q1 Sales, Q2 Sales, Q3 Sales', series_data_str='West: 30, 28, 35; East: 25, 30, 20; Midwest: 20, 18, 25', title='Line Chart Slide', insert_at="3")
    """,
    "add_pie_chart": """
        Purpose: Create a slide with a pie chart, highlighting category distributions and explaining them in bullet points.

        **Key Use Cases**:
        - Showing proportional data or percentages.
        - Visualizing category-wise breakdowns.

        **Input Format**:
        - `categories_str`: Comma-separated string of category names.
        - `values_str`: Comma-separated string of values.
        - `right_content`: Bullet points for the right column, separated by semicolons.
        - `title`: Title of the slide.
        - `plot_name`: Title of the pie chart.
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted. (e.g., insert_at="2")
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_pie_chart(categories_str='Product A, Product B, Product C', values_str='40, 35, 25', right_content='Product A had the highest demand; Product C had the least demand, title='Sales Distribution', plot_name='Product Share', insert_at="2")
    """,
    "add_area_chart": """
        Purpose: Create a slide with an area chart.

        **Key Use Cases**:
        - Visualizing cumulative data over time.
        - Highlighting trends with shaded areas.

        **Input Format**:
        - `categories_str`: Comma-separated string of categories.
        - `values_str`: Comma-separated string of values.
        - `title`: Title of the slide.
        - `plot_name`: Title of the area chart.
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted. (e.g., insert_at="2")
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_area_chart(categories_str='Q1, Q2, Q3, Q4', values_str='100, 150, 200, 250', title='Revenue Growth', plot_name='Quarterly Revenue', insert_at="4")
    """,
    "add_scatter_chart": """
        Purpose: Create a slide with a scatter plot, visualizing relationships between two datasets.

        **Key Use Cases**:
        - Analyzing correlations between two variables.
        - Displaying distribution or variance in data.

        **Input Format**:
        - `input_x`: Label and values for the x-axis.
        - `input_y`: Label and values for the y-axis.
        - `title`: Title of the slide.
        - `plot_title`: Title of the scatter plot.
        - `insert_at`: Optional parameter specifying the slide index where the slide should be inserted. (e.g., insert_at="2")
          Use this parameter only when the prompt explicitly says "insert a slide at X index."

        **Usage**:
        add_scatter_chart(input_x='Production; 100, 200, 300', input_y='Defects; 2, 3, 1', title='Production vs Defects', plot_title='Scatter Plot', insert_at="2")
    """
}
