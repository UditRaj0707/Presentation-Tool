TOOL_DESCRIPTIONS = {
    "add_image_slide": """
        Use this tool to create a slide that contains ONLY an image with an caption below it.
        **Do NOT Use When:**  
        - The slide requires text explanations, descriptions, or bullet points alongside the image.

        Purpose: Add a slide with an image and a caption.

        **Key Use Cases**:
        - Displaying product images, charts, or visual content.
        - Adding a visual representation with a caption.

        **Usage**:
        add_image_slide(image_path='<path_to_image>', caption='Image description', title='Slide Title')
    """,

    "add_text_with_image_slide": """
        Purpose: Add a slide with a text and image.

        **Key Use Cases**:
        - Combining visual and textual information in one slide.
        - Presenting descriptive text alongside an image.

        **Usage**:
        add_image_with_text_slide(text_content='Paragraph 1.\\n\\nParagraph 2.', image_path='<path_to_image>', title='Slide Title')
    """,

    "add_bullet_slide": """
        Purpose: Create a slide with bullet points.

        **Key Use Cases**:
        - Listing key points, ideas, or steps.
        - Structuring information concisely.

        **Usage**:
        add_bullet_slide(title='Slide Title', content='First point; Second point; Third point')
    """,

    "add_two_content_bullet_slide": """
        Purpose: Create a slide with two columns of bullet points.

        **Key Use Cases**:
        - Comparing two sets of information side-by-side.
        - Displaying pros and cons or feature comparisons.

        **Usage**:
        add_two_content_bullet_slide(title='Slide Title', left_content='Point 1; Point 2; Point 3', right_content='Item A; Item B; Item C')
    """,

    "add_table_slide": """
        Purpose: Add a comparison table to the presentation.

        **Key Use Cases**:
        - Comparing data in a structured table format.
        - Displaying tabular information clearly.

        **Usage**:
        add_table_slide(title='Comparison Table', table_data='Header1, Header2; Value1, Value2; Value3, Value4')
    """,

    "add_bar_chart": """
        Purpose: Create a slide with a clustered bar chart for comparing multiple data series.

        **Key Use Cases**:
        - Visualizing comparative data across multiple categories.
        - Highlighting differences between series.

        **Usage**:
        Example 1:
        add_bar_chart(categories_str='Category A, Category B, Category C', values_str='Sales: 50, 70, 90', title='Sales Comparison')
        Example 2:
        add_bar_chart(categories_str='East, West, Midwest', series_data_str='Q1: 19.2, 21.4, 16.7; Q2: 22.3, 28.6, 15.2; Q3: 20.4, 26.3, 14.2', title='Bar Chart Slide')
        
    """,

    "add_line_chart": """
        Purpose: Create a slide with a multi-series line chart.

        **Key Use Cases**:
        - Showing trends over time across multiple series.
        - Visualizing performance metrics or comparisons.

        **Usage**:
        add_line_chart(categories_str='Q1 Sales, Q2 Sales, Q3 Sales', series_data_str='West: 30, 28, 35; East: 25, 30, 20; Midwest: 20, 18, 25', title='Line Chart Slide')
    """,

    "add_pie_chart": """
        Purpose: Create a slide with a pie chart, highlighting category distributions.

        **Key Use Cases**:
        - Showing proportional data or percentages.
        - Visualizing category-wise breakdowns.

        **Usage**:
        add_pie_chart(categories_str='Product A, Product B, Product C', values_str='40, 35, 25', title='Sales Distribution', plot_name='Product Share')
    """,

    "add_area_chart": """
        Purpose: Create a slide with an area chart.

        **Key Use Cases**:
        - Visualizing cumulative data over time.
        - Highlighting trends with shaded areas.

        **Usage**:
        add_area_chart(categories_str='Q1, Q2, Q3, Q4', values_str='100, 150, 200, 250', title='Revenue Growth', plot_name='Quarterly Revenue')
    """,

    "add_scatter_chart": """
        Purpose: Create a slide with a scatter plot, visualizing relationships between two datasets.

        **Key Use Cases**:
        - Analyzing correlations between two variables.
        - Displaying distribution or variance in data.

        **Usage**:
        add_scatter_chart(input_x='Production; 100, 200, 300', input_y='Defects; 2, 3, 1', title='Production vs Defects', plot_title='Scatter Plot')
    """
}
