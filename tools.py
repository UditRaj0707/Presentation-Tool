# from langchain_core.tools import tool
from pptx import Presentation
from pptx.chart.data import XyChartData
from pptx.chart.data import CategoryChartData, ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_LABEL_POSITION, XL_LEGEND_POSITION
from abc import ABC
# import Annotated
from typing import Annotated
from pydantic import BaseModel
from langchain.tools import tool
from langchain.tools import StructuredTool
from tool_descriptions import TOOL_DESCRIPTIONS

import os
from load_dotenv import load_dotenv
load_dotenv()

SAVE_PATH = "output/presentation_test.pptx"
INPUT_PATH = None

def use_presentation(folder_path: str, file_path: str):
    """
    Load an existing presentation file
    Args:
        file_path: Path to the presentation file
    """
    global INPUT_PATH, SAVE_PATH
    INPUT_PATH = folder_path + "/" + file_path
    SAVE_PATH = "output/" + file_path
    print(f"Presentation loaded from: {INPUT_PATH}")
    print(f"Presentation will be saved to: {SAVE_PATH}")
    

class Presentationtools:
    """
    Presentationtools class
    """
    name: str = "presentation_tools"
    description: str = "Tools for interacting with PowerPoint slides"

    def __init__(self):
        self.config = {
            "title_font_size": 24,
        }

    @staticmethod
    def get_presentation():
        if INPUT_PATH is not None:
            return Presentation(INPUT_PATH)
        else:
            return Presentation()


    def add_image_slide(self, image_path: str, caption: str, title: str):
        """
        Add a slide having image with caption to the presentation
        Args:
            image_path: Path to image file
            caption: caption text
            title: Title of the slide
        """
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])
        title_shape = slide.shapes.title
        title_shape.text = title  
        title_shape.text_frame.paragraphs[0].font.size = Pt(self.config["title_font_size"])
        title_shape.text_frame.paragraphs[0].font.bold = True
        
        left = Inches(3)  
        top = Inches(2)   
        width = 4
        height = 4
        pic = slide.shapes.add_picture(
            image_path,
            left,
            top,
            width=Inches(width),
            height=Inches(height)
        )
        
        if caption:
            left = Inches(3)
            top = top + Inches(height) + Inches(0.5) 
            width = Inches(4)
            height = Inches(1)
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            tf.text = caption
            tf.fit_text(font_family="Arial", max_size=12, italic=True)
            
        return self.save_presentation()
    
    def add_text_with_image_slide(self, text_content: str, image_path: str, title: str, **kwargs):
        """
        Add a slide with text on the left half and an image on the right half.

        Args:
            text_content: Text content for the left side, paragraphs separated by double line breaks.
                            Example: "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
            image_path: Path to the image file.
            title: Title of the slide.
        """
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])

        title_shape = slide.shapes.title
        title_shape.text = title
        title_shape.text_frame.paragraphs[0].font.size = Pt(self.config["title_font_size"])
        title_shape.text_frame.paragraphs[0].font.bold = True

        left_text_box = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(4), Inches(4.5))
        text_frame = left_text_box.text_frame
        text_frame.word_wrap = True

        paragraphs = text_content.split('\n\n')
        for i, paragraph in enumerate(paragraphs):
            if i == 0:
                p = text_frame.paragraphs[0] 
            else:
                p = text_frame.add_paragraph()
            p.text = paragraph.strip()
            p.font.size = Pt(14)
            p.space_after = Pt(10) 

        img_left = Inches(5)  
        img_top = Inches(2)
        img_width = Inches(4) 
        img_height = Inches(4.5)
        slide.shapes.add_picture(image_path, img_left, img_top, width=img_width, height=img_height)

        # Save the presentation
        file_path = self.save_presentation()
        return f"Slide with image and text created and saved at: {file_path}"
    
    def add_bullet_slide(self, title: str, content: str):
        """
        Create a slide with bullet points
        Args:
            title: Title of the slide
            content: String of bullet points separated by semicolons
            Example: "First point; Second point; Third point"
        """
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[1])
        title_shape = slide.shapes.title
        title_shape.text = title 
        title_shape.text_frame.paragraphs[0].font.size = Pt(self.config["title_font_size"])
        title_shape.text_frame.paragraphs[0].font.bold = True
        
        bullet_points = [point.strip() for point in content.split(';')]

        text_frame = slide.placeholders[1].text_frame
        text_frame.clear() 
        
        # Add bullet points
        for item in bullet_points:
            paragraph = text_frame.add_paragraph()
            paragraph.text = item
            paragraph.level = 0  
            paragraph.bullet = True
        
        return self.save_presentation()
    
    def add_two_content_bullet_slide(self, title: str, left_content: str, right_content: str):
        """
        Create a slide with two columns of bullet points
        Args:
            title: Title of the slide
            left_content: String with bullet points separated by semicolons
            right_content: String with bullet points separated by semicolons
            Example: 
                left_content = "Point 1; Point 2; Point 3"
                right_content = "Item A; Item B; Item C"
        """
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[3])
        
        title_shape = slide.shapes.title
        title_shape.text = title  
        title_shape.text_frame.paragraphs[0].font.size = Pt(self.config["title_font_size"])
        title_shape.text_frame.paragraphs[0].font.bold = True
        
        left_placeholder = slide.placeholders[1]
        right_placeholder = slide.placeholders[2]
        
        left_points = left_content.split(';')
        left_frame = left_placeholder.text_frame
        left_frame.clear()
        for point in left_points:
            p = left_frame.add_paragraph()
            p.text = point.strip()
            p.level = 0
            p.bullet = True
        
        right_points = right_content.split(';')
        right_frame = right_placeholder.text_frame
        right_frame.clear()
        for point in right_points:
            p = right_frame.add_paragraph()
            p.text = point.strip()
            p.level = 0
            p.bullet = True
        
        return self.save_presentation()
        
    def add_table_slide(self, table_data: str, title: str):
        """
        Add a comparison table to the presentation from string input
        Args:
            table_data: String in format "header1, header2; value1, value2; value3, value4"
            title: Title of the slide
            Example: "Car, Bike; BMW, Harley; Audi, Ducati; Mercedes, Honda"
        """
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()      
        rows = table_data.split(';')
        headers = rows[0].split(',')
        values = [row.split(',') for row in rows[1:]]
        
        table_data = {}
        for i, header in enumerate(headers):
            table_data[header] = [row[i] for row in values]
        
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])
        title_shape = slide.shapes.title
        title_shape.text = title 
        title_shape.text_frame.paragraphs[0].font.size = Pt(self.config["title_font_size"])
        title_shape.text_frame.paragraphs[0].font.bold = True

        rows = len(list(table_data.values())[0]) + 1
        cols = len(table_data.keys())
        table = slide.shapes.add_table(rows, cols, Inches(2), Inches(2), Inches(6), Inches(4)).table
        
        for i, key in enumerate(table_data.keys()):
            table.cell(0, i).text = key
            for j, value in enumerate(table_data[key]):
                table.cell(j + 1, i).text = value
        
        file_path = self.save_presentation()
        return file_path


    def add_bar_chart(self, categories_str: str, series_data_str: str, title: str) -> str:
        """
        Create a slide with a clustered bar chart for comparing multiple data series.

        Args:
            categories_str: String of categories separated by commas.
                            Example: "East, West, Midwest"
            series_data_str: String with series data in the format:
                            "Series1: 19.2, 21.4, 16.7; Series2: 22.3, 28.6, 15.2; Series3: 20.4, 26.3, 14.2"
            title: Title of the slide.

        Example:
            categories_str = "East, West, Midwest"
            series_data_str = "Q1: 19.2, 21.4, 16.7; Q2: 22.3, 28.6, 15.2; Q3: 20.4, 26.3, 14.2"
        """
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()
        # Create a new slide
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])

        # Set slide title with custom font size
        title_shape = slide.shapes.title
        title_shape.text = title
        title_shape.text_frame.paragraphs[0].font.size = Pt(24)
        title_shape.text_frame.paragraphs[0].font.bold = True

        # Initialize the chart data
        chart_data = ChartData()
        chart_data.categories = [c.strip() for c in categories_str.split(",")]

        # Process multiple series data
        series_entries = series_data_str.split(";")
        for series_entry in series_entries:
            series_name, series_values = series_entry.split(":")
            values = [float(v.strip()) for v in series_values.split(",")]
            chart_data.add_series(series_name.strip(), values)

        # Add the clustered bar chart
        x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
        chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data).chart

        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.RIGHT
        chart.legend.include_in_layout = False

        plot = chart.plots[0]
        plot.has_data_labels = True
        data_labels = plot.data_labels

        data_labels.font.size = Pt(6)
        data_labels.font.color.rgb = RGBColor(0, 0, 0)
        data_labels.position = XL_LABEL_POSITION.INSIDE_END


        # Save the presentation
        file_path = self.save_presentation()
        return f"Slide with clustered bar chart created and saved at: {file_path}"



    def add_line_chart(self, categories_str: str, series_data_str: str, title: str, **kwargs) -> str:
        """
        Create a slide with a multi-series line chart.

        Args:
            categories_str: String of categories separated by commas.
                            Example: "Q1 Sales, Q2 Sales, Q3 Sales"
            series_data_str: String of series data in the format:
                            "West: 30, 28, 35; East: 25, 30, 20; Midwest: 20, 18, 25"
            title: Title of the slide.
        """
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])
        title_shape = slide.shapes.title
        title_shape.text = title 
        title_shape.text_frame.paragraphs[0].font.size = Pt(self.config["title_font_size"])
        title_shape.text_frame.paragraphs[0].font.bold = True

        chart_data = CategoryChartData()
        chart_data.categories = [c.strip() for c in categories_str.split(",")]

        series_entries = series_data_str.split(";")
        for series_entry in series_entries:
            series_name, series_values = series_entry.split(":")
            values = [float(v.strip()) for v in series_values.split(",")]
            chart_data.add_series(series_name.strip(), values)

        x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
        slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, x, y, cx, cy, chart_data)

        file_path = self.save_presentation()
        print(f"Slide with multi-series line chart created and saved at: {file_path}")
        return f"Slide with multi-series line chart created and saved at: {file_path}"

    
    def add_pie_chart(self, categories_str: str, values_str: str, title: str, plot_name: str) -> str:
        """
        Create a slide with a pie chart including well-formatted category labels.
        Args:
            categories_str: String of categories separated by commas
            values_str: String of values separated by commas
            title: Title of the slide
            plot_name: Title of the pie chart
        """
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])
        title_shape = slide.shapes.title
        title_shape.text = title  
        title_shape.text_frame.paragraphs[0].font.size = Pt(self.config["title_font_size"])
        title_shape.text_frame.paragraphs[0].font.bold = True

        chart_data = CategoryChartData()
        chart_data.categories = [c.strip() for c in categories_str.split(",")]
        chart_data.add_series(plot_name, (float(v.strip()) for v in values_str.split(",")))

        x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
        chart_shape = slide.shapes.add_chart(XL_CHART_TYPE.PIE, x, y, cx, cy, chart_data)
        chart = chart_shape.chart 

        plot = chart.plots[0]
        plot.has_data_labels = True  
        data_labels = plot.data_labels
        data_labels.show_category_name = True
        data_labels.show_percentage = True
        data_labels.separator = "\n" 
        data_labels.position = XL_DATA_LABEL_POSITION.BEST_FIT  

        file_path = self.save_presentation()
        return f"Slide with pie chart created and saved at: {file_path}"
    
    def add_area_chart(self, categories_str: str, values_str: str, title: str, plot_name : str) -> str:
        """
        Create a slide with an area chart
        Args:
            categories_str: String of categories separated by commas
            values_str: String of values separated by commas
            title: Title of the slide
            plot_name: Title of the area chart
            Example: "A, B, C, D", "1, 2, 3, 4", "Area Chart Slide"
        """
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])
        title_shape = slide.shapes.title
        title_shape.text = title  
        title_shape.text_frame.paragraphs[0].font.size = Pt(self.config["title_font_size"])
        title_shape.text_frame.paragraphs[0].font.bold = True

        chart_data = CategoryChartData()
        chart_data.categories = [c.strip() for c in categories_str.split(",")]
        chart_data.add_series(plot_name, (float(v.strip()) for v in values_str.split(",")))

        x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
        slide.shapes.add_chart(XL_CHART_TYPE.AREA, x, y, cx, cy, chart_data)

        file_path = self.save_presentation()
        return f"Slide with area chart created and saved at: {file_path}"
    
    def add_scatter_chart(self, input_x: str, input_y: str, title: str, plot_title: str) -> str:
        """
    Creates a scatter plot slide with labeled axes.

    Parameters:
    - input_x (str): X-axis label and values in the format "Label; 1, 2, 3, 4" or just "1, 2, 3, 4".
    - input_y (str): Y-axis label and values in the format "Label; 5, 6, 7, 8" or just "5, 6, 7, 8".
    - title (str): The title of the slide.
    - plot_title (str): The title of the scatter plot.
    
    Returns:
    - str: The file path of the saved presentation slide.

    Example:
    - add_scatter_chart("X-Axis; 1, 2, 3, 4", "Y-Axis; 5, 6, 7, 8", "Scatter Plot Slide", "Scatter Plot")
    - add_scatter_chart("1, 2, 3, 4", "5, 6, 7, 8", "Scatter Plot Slide", "Scatter Plot")
    """
        try:
            if ";" in input_x:
                x_label, x_values_str = input_x.split(";")
            else:
                x_label, x_values_str = "X-Axis", input_x
            
            if ";" in input_y:
                y_label, y_values_str = input_y.split(";")
            else:
                y_label, y_values_str = "Y-Axis", input_y
            
            x_values = [float(x.strip()) for x in x_values_str.split(",")]
            y_values = [float(y.strip()) for y in y_values_str.split(",")]
        except ValueError:
            return "Error: Inputs must be in the format 'Label; 1, 2, 3, 4' or '1, 2, 3, 4' with numeric values."
        
        if not hasattr(self, "prs"):
            self.prs = self.get_presentation()
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[5])
        title_shape = slide.shapes.title
        title_shape.text = title  
        title_shape.text_frame.paragraphs[0].font.size = Pt(self.config["title_font_size"])
        title_shape.text_frame.paragraphs[0].font.bold = True

        chart_data = XyChartData()
        series = chart_data.add_series(plot_title)

        for x, y in zip(x_values, y_values):
            series.add_data_point(x, y)

        x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
        chart_shape = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER, x, y, cx, cy, chart_data)
        chart = chart_shape.chart

        category_axis = chart.category_axis
        value_axis = chart.value_axis
        category_axis.has_title = True
        value_axis.has_title = True
        category_axis.axis_title.text_frame.text = x_label.strip()
        value_axis.axis_title.text_frame.text = y_label.strip()

        file_path = self.save_presentation()
        return f"Slide with scatter chart (with axis labels) created and saved at: {file_path}"

    
    def get_slide_layout(self):
        for idx, layout in enumerate(self.prs.slide_layouts):
            print(f"Layout {idx}: {layout.name}")
            slide = self.prs.slides.add_slide(layout)
            for placeholder in slide.placeholders:
                print(f"\tPlaceholder {placeholder.placeholder_format.idx}: {placeholder.name}")


    def save_presentation(self):
        """
        Save the presentation to a file
        """
        print(f"self.save_path: {SAVE_PATH}")
        self.prs.save(SAVE_PATH)
        return SAVE_PATH
    
    def get_tools(self):
        print("🔍 Binding tools...")
        return [
            # StructuredTool.from_function(
            #     func=self.add_single_column_chart,
            #     name="add_single_column_chart"
            # ),
            StructuredTool.from_function(
                func=lambda **kwargs: self.add_image_slide(**kwargs),
                name="add_image_slide",
                description=TOOL_DESCRIPTIONS.get("add_image_slide")
            ),
            StructuredTool.from_function(
                func=lambda **kwargs: self.add_text_with_image_slide(**kwargs),
                name="add_text_with_image_slide",
                description=TOOL_DESCRIPTIONS.get("add_text_with_image_slide")
            ),
            StructuredTool.from_function(
                func=lambda **kwargs: self.add_bullet_slide(**kwargs),
                name="add_bullet_slide",
                description=TOOL_DESCRIPTIONS.get("add_bullet_slide")
            ),
            StructuredTool.from_function(
                func=self.add_two_content_bullet_slide,
                name="add_two_content_bullet_slide",
                description=TOOL_DESCRIPTIONS.get("add_two_content_bullet_slide")
            ),
            StructuredTool.from_function(
                func=self.add_table_slide,
                name="add_table_slide",
                description=TOOL_DESCRIPTIONS.get("add_table_slide")
            ),
            StructuredTool.from_function(
                func=self.add_bar_chart,
                name="add_bar_chart",
                description=TOOL_DESCRIPTIONS.get("add_bar_chart")
            ),
            StructuredTool.from_function(
                func=self.add_line_chart,
                name="add_line_chart",
                description=TOOL_DESCRIPTIONS.get("add_line_chart")
            ),
            StructuredTool.from_function(
                func=self.add_pie_chart,
                name="add_pie_chart",
                description=TOOL_DESCRIPTIONS.get("add_pie_chart")
            ),
            StructuredTool.from_function(
                func=self.add_area_chart,
                name="add_area_chart", 
                description=TOOL_DESCRIPTIONS.get("add_area_chart")
            ),
            StructuredTool.from_function(
                func=self.add_scatter_chart,
                name="add_scatter_chart",
                description=TOOL_DESCRIPTIONS.get("add_scatter_chart")
            )
        ]





    
    