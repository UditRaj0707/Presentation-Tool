from ppt_agent import PresentationAgent

TEMPLATE_PROMPTS = {
    "month_end_closing": [
        "Create a title slide for November 2024 Financial Review with just text, no logos",
        "Create an agenda slide with sections: Key Financial Metrics, Variance Analysis, Challenges and Risks, Action Items and Next Steps",
        "Create a PnL Comparison table slide showing Current Month vs. Previous Month with Variance",
        "Create a PnL comparison table slide showing Current Quarter vs. Last year same quarter with Variance",
        "Create a highlights slide showing Key Achievements, Challenges, and Opportunities",
        "Create a Revenue Highlights table slide showing Top Revenue Streams and Trends or Top Customers",
        "Create a margin waterfall chart slide showing Gross Margin, Operating Margin, Net Margin",
        "Create an Operating Expenses waterfall chart slide showing Fixed Costs, Variable Costs, Other Expenses",
        "Create a Risk and Challenges slide showing Key Risks and Challenges faced during the month",
        "Create an Action Items slide with Prioritized list of action items for the team"
    ],

    "quarterly_business_review": [
        "Create a title slide for Quaterly Business Reviews with just text, no logos",
        "Create an Quaterly Metrics slide with sections: Financials, Operations and Goals Update.",
        "Create a slide with title Quaterly Metrics and a table showing Revenue, Expenses, Profit, and Margin quarter-wise.",
        "Create a table slide with top ten customers and their revenue contribution quarter-wise.",
        "Create a line chart slide showing stock market movememnts of the company and its 8 competitors.",
        "Create a Revenue Highlights table slide showing Top Revenue Streams and Trends or Top Customers",
        "Create a table slide showing the inventory metrics",
        "Create a table slide showing the workforce month-wise per business division."
    ],
    "strategic_review": [
        "Create a presentation for the strategic review."
    ]
}


def main():
    ppt = PresentationAgent()
    info_for_user = """Available Templates:
    1. Month End Closing
    2. Quarterly Business Review (Not available as of now)
    
Select the template you want to use: """

    user_input = int(input(info_for_user))
    if user_input == 1:
        prompt = TEMPLATE_PROMPTS["month_end_closing"]
        ppt.process_query(prompt)

if __name__ == "__main__":
    main()