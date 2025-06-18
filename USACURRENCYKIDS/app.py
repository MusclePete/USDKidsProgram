import gradio as gr
from PIL import Image
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Currency data with front/back paths and symbols
currencies = [
    {"name": "Penny", "type": "coin", "value": 1, "front_path": "images/penny_front.png", "back_path": "images/penny_back.png", "symbol": '<svg width="40" height="40"><circle cx="20" cy="20" r="18" fill="#B87333" stroke="#8B5A2B" stroke-width="2"><text x="20" y="21" fill="black" font-size="10" font-family="Arial" text-anchor="middle">1</text></svg>'},
    {"name": "Nickel", "type": "coin", "value": 5, "front_path": "images/nickel_front.png", "back_path": "images/nickel_back.png", "symbol": '<svg width="40" height="40"><circle cx="20" cy="20" r="18" fill="#C0C0C0" stroke="#808080" stroke-width="2"><text x="20" y="21" fill="black" font-size="10" font-family="Arial" text-anchor="middle">5</text></svg>'},
    {"name": "Dime", "type": "coin", "value": 10, "front_path": "images/dime_front.png", "back_path": "images/dime_back.png", "symbol": '<svg width="40" height="40"><circle cx="20" cy="20" r="18" fill="#C0C0C0" stroke="#808080" stroke-width="2"><text x="20" y="21" fill="black" font-size="10" font-family="Arial" text-anchor="middle">10</text></svg>'},
    {"name": "Quarter", "type": "coin", "value": 25, "front_path": "images/quarter_front.png", "back_path": "images/quarter_back.png", "symbol": '<svg width="40" height="40"><circle cx="20" cy="20" r="18" fill="#C0C0C0" stroke="#808080" stroke-width="2"><text x="20" y="21" fill="black" font-size="10" font-family="Arial" text-anchor="middle">25</text></svg>'},
    {"name": "Half Dollar", "type": "coin", "value": 50, "front_path": "images/half_dollar_front.png", "back_path": "images/half_dollar_back.png", "symbol": '<svg width="40" height="40"><circle cx="20" cy="20" r="18" fill="#C0C0C0" stroke="#808080" stroke-width="2"><text x="20" y="21" fill="black" font-size="10" font-family="Arial" text-anchor="middle">50</text></svg>'},
    {"name": "Dollar Coin", "type": "coin", "value": 100, "front_path": "images/dollar_coin_front.png", "back_path": "images/dollar_coin_back.png", "symbol": '<svg width="40" height="40"><circle cx="20" cy="20" r="18" fill="#FFD700" stroke="#D4A017" stroke-width="2"><text x="20" y="21" fill="black" font-size="10" font-family="Arial" text-anchor="middle">$1</text></svg>'},
    {"name": "$1 Bill", "type": "paper", "value": 100, "front_path": "images/1_dollar_front.png", "back_path": "images/1_dollar_back.png", "symbol": '<svg width="60" height="40"><rect width="60" height="40" fill="#008000" stroke="#004D00" stroke-width="2"/><text x="30" y="21" fill="white" font-size="12" font-family="Arial" text-anchor="middle">$1</text></svg>'},
    {"name": "$2 Bill", "type": "paper", "value": 200, "front_path": "images/2_dollar_front.png", "back_path": "images/2_dollar_back.png", "symbol": '<svg width="60" height="40"><rect width="60" height="40" fill="#008000" stroke="#004D00" stroke-width="2"/><text x="30" y="21" fill="white" font-size="12" font-family="Arial" text-anchor="middle">$2</text></svg>'},
    {"name": "$5 Bill", "type": "paper", "value": 500, "front_path": "images/5_dollar_front.png", "back_path": "images/5_dollar_back.png", "symbol": '<svg width="60" height="40"><rect width="60" height="40" fill="#008000" stroke="#004D00" stroke-width="2"/><text x="30" y="21" fill="white" font-size="12" font-family="Arial" text-anchor="middle">$5</text></svg>'},
    {"name": "$10 Bill", "type": "paper", "value": 1000, "front_path": "images/10_dollar_front.png", "back_path": "images/10_dollar_back.png", "symbol": '<svg width="60" height="40"><rect width="60" height="40" fill="#008000" stroke="#004D00" stroke-width="2"/><text x="30" y="21" fill="white" font-size="12" font-family="Arial" text-anchor="middle">$10</text></svg>'},
    {"name": "$20 Bill", "type": "paper", "value": 2000, "front_path": "images/20_dollar_front.png", "back_path": "images/20_dollar_back.png", "symbol": '<svg width="60" height="40"><rect width="60" height="40" fill="#008000" stroke="#004D00" stroke-width="2"/><text x="30" y="21" fill="white" font-size="12" font-family="Arial" text-anchor="middle">$20</text></svg>'},
    {"name": "$50 Bill", "type": "paper", "value": 5000, "front_path": "images/50_dollar_front.png", "back_path": "images/50_dollar_back.png", "symbol": '<svg width="60" height="40"><rect width="60" height="40" fill="#008000" stroke="#004D00" stroke-width="2"/><text x="30" y="21" fill="white" font-size="12" font-family="Arial" text-anchor="middle">$50</text></svg>'},
    {"name": "$100 Bill", "type": "paper", "value": 10000, "front_path": "images/100_dollar_front.png", "back_path": "images/100_dollar_back.png", "symbol": '<svg width="60" height="40"><rect width="60" height="40" fill="#008000" stroke="#004D00" stroke-width="2"/><text x="30" y="21" fill="white" font-size="12" font-family="Arial" text-anchor="middle">$100</text></svg>'},
]

# 2025 State sales tax rates (approximate state-level averages for educational simplicity)
state_tax_rates = {
    "Alabama": 4.0, "Alaska": 0.0, "Arizona": 5.6, "Arkansas": 6.5, "California": 7.25,
    "Colorado": 2.9, "Connecticut": 6.35, "Delaware": 0.0, "Florida": 6.0, "Georgia": 4.0,
    "Hawaii": 4.0, "Idaho": 6.0, "Illinois": 6.25, "Indiana": 7.0, "Iowa": 6.0,
    "Kansas": 6.5, "Kentucky": 6.0, "Louisiana": 4.45, "Maine": 5.5, "Maryland": 6.0,
    "Massachusetts": 6.25, "Michigan": 6.0, "Minnesota": 6.875, "Mississippi": 7.0,
    "Missouri": 4.225, "Montana": 0.0, "Nebraska": 5.5, "Nevada": 6.85, "New Hampshire": 0.0,
    "New Jersey": 6.625, "New Mexico": 4.875, "New York": 4.0, "North Carolina": 4.75,
    "North Dakota": 5.0, "Ohio": 5.75, "Oklahoma": 4.5, "Oregon": 0.0, "Pennsylvania": 6.0,
    "Rhode Island": 7.0, "South Carolina": 6.0, "South Dakota": 4.2, "Tennessee": 7.0,
    "Texas": 6.25, "Utah": 4.85, "Vermont": 6.0, "Virginia": 4.3, "Washington": 6.5,
    "West Virginia": 6.0, "Wisconsin": 5.0, "Wyoming": 4.0
}

# Function to load local image with fallback to None
def load_image(image_path, name, side):
    try:
        if not os.path.exists(image_path):
            logger.warning(f"{side} image not found for {name}: {image_path}")
            return None
        img = Image.open(image_path)
        logger.info(f"Loaded {side} image for {name}: {image_path}")
        return img
    except Exception as e:
        logger.error(f"Failed to load {side} image for {name}: {str(e)}")
        return None

# Function to display currency details
def show_currency(currency_name):
    currency = next((c for c in currencies if c["name"] == currency_name), None)
    if not currency:
        return None, None, "Currency not found."
    
    front_img = load_image(currency["front_path"], currency["name"], "front")
    back_img = load_image(currency["back_path"], currency["name"], "back")
    info = f"""
    **{currency['name']}**
    
    - **Value**: ${currency['value'] / 100:.2f} ({currency['value']} cents)
    - **Type**: {currency['type']}
    - **Symbol**: {currency['symbol']}
    """
    return front_img, back_img, info

# Function to compare two currencies
def compare_currencies(currency1, currency2):
    if not currency1 or not currency2:
        return "Please select both currencies."
    
    curr1 = next((c for c in currencies if c["name"] == currency1), None)
    curr2 = next((c for c in currencies if c["name"] == currency2), None)
    
    if not curr1 or not curr2:
        return "Invalid currency selection."
    
    value1 = curr1["value"]  # in cents
    value2 = curr2["value"]  # in cents
    
    # Determine larger and smaller currency
    if value1 >= value2:
        larger = curr1
        smaller = curr2
        larger_value = value1
        smaller_value = value2
    else:
        larger = curr2
        smaller = curr1
        larger_value = value2
        smaller_value = value1
    
    # Calculate whole denominations
    count = larger_value // smaller_value
    remainder = larger_value % smaller_value
    
    # Build visual comparison
    left_visual = f"<div style='display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;'>"
    for _ in range(int(count)):
        left_visual += smaller["symbol"]
    left_visual += "</div>"
    
    right_visual = f"<div style='display: flex; justify-content: center;'>{larger['symbol']}</div>"
    
    # Handle remainder
    extra_text = ""
    extra_visual = ""
    if remainder > 0:
        extra_currencies = []
        remaining = remainder
        for curr in sorted(currencies, key=lambda x: x["value"], reverse=True):
            if curr["value"] <= remaining and curr["value"] <= smaller_value:
                curr_count = remaining // curr["value"]
                if curr_count > 0:
                    extra_currencies.append((curr_count, curr))
                    remaining -= curr_count * curr["value"]
        if remaining > 0:
            extra_text = "<br><i>(Exact match not possible with available denominations)</i>"
        else:
            extra_visual = "<div style='display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;'>"
            for count, curr in extra_currencies:
                for _ in range(count):
                    extra_visual += curr["symbol"]
            extra_visual += "</div>"
            extra_text = f"<br>Plus: {extra_visual}"
    
    # Build result text
    result = f"<div style='text-align: center; font-size: 16px;'>"
    result += f"<div style='display: flex; justify-content: space-between; align-items: center; gap: 20px;'>"
    result += f"<div style='flex: 1;'><b>{count} {smaller['name']}</b><br>{left_visual}</div>"
    result += f"<div style='font-size: 20px;'>=</div>"
    result += f"<div style='flex: 1;'><b>1 {larger['name']}</b><br>{right_visual}</div>"
    result += "</div>"
    result += f"<div style='margin-top: 10px;'>Value: ${larger_value / 100:.2f}</div>"
    if extra_text:
        result += extra_text
    result += "</div>"
    
    return result

# Function to calculate total cost with sales tax and structured visual representation
def calculate_cost(item_cost, state):
    if item_cost is None or item_cost <= 0:
        return "Please enter a cost greater than $0!"
    if state not in state_tax_rates:
        return "Please select a valid state!"
    
    tax_rate = state_tax_rates[state]
    tax_amount = item_cost * (tax_rate / 100)
    total_cost = item_cost + tax_amount  # Keep unrounded total
    total_cents = int(total_cost * 100)  # Convert to cents
    
    # Build structured visual representation by denomination rows
    visual = "<div style='display: flex; flex-direction: column; gap: 10px; text-align: center;'>"
    
    # Row 1: $100 bills
    hundred_count = total_cents // 10000
    if hundred_count > 0:
        hundred_visual = "<div style='display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;'>"
        for _ in range(hundred_count):
            hundred_visual += next(c["symbol"] for c in currencies if c["value"] == 10000)
        hundred_visual += "</div>"
        visual += f"<div><b>${hundred_count * 100} in $100 bills</b><br>{hundred_visual}</div>"
        total_cents -= hundred_count * 10000
    
    # Row 2: $50 bills
    fifty_count = total_cents // 5000
    if fifty_count > 0:
        fifty_visual = "<div style='display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;'>"
        for _ in range(fifty_count):
            fifty_visual += next(c["symbol"] for c in currencies if c["value"] == 5000)
        fifty_visual += "</div>"
        visual += f"<div><b>${fifty_count * 50} in $50 bills</b><br>{fifty_visual}</div>"
        total_cents -= fifty_count * 5000
    
    # Row 3: $20, $10, $5, $2, $1 bills
    remaining_dollars = total_cents // 100
    if remaining_dollars > 0:
        bill_visual = "<div style='display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;'>"
        for curr in sorted([c for c in currencies if 100 <= c["value"] <= 2000], key=lambda x: x["value"], reverse=True):
            count = remaining_dollars // (curr["value"] // 100)
            if count > 0:
                for _ in range(count):
                    bill_visual += curr["symbol"]
                remaining_dollars -= count * (curr["value"] // 100)
        bill_visual += "</div>"
        visual += f"<div><b>${total_cents // 100 - (total_cents % 100) // 100} in bills</b><br>{bill_visual}</div>"
        total_cents %= 100
    
    # Row for cents: quarters, dimes, nickels, pennies
    if total_cents > 0:
        rounded_cents = round(total_cents % 100)  # Round to nearest whole cent
        cents_visual = "<div style='display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;'>"
        remaining_cents = rounded_cents
        for curr in sorted([c for c in currencies if c["value"] < 100], key=lambda x: x["value"], reverse=True):
            count = remaining_cents // curr["value"]
            if count > 0:
                for _ in range(count):
                    cents_visual += curr["symbol"]
                remaining_cents -= count * curr["value"]
        cents_visual += "</div>"
        visual += f"<div><b>{rounded_cents} cents</b><br>{cents_visual}</div>"
    
    visual += "</div>"
    
    return f"""
    **Cost Calculator**
    
    - **Item Cost**: ${item_cost:.2f}
    - **Sales Tax ({state}):** ${tax_amount:.2f} ({tax_rate:.1f}%)
    - **Total Cost**: ${total_cost:.2f}
    - **Your Money Looks Like:** {visual}
    
    Wow! You learned about extra taxes—cool, right? 😊
    """

# Gradio interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), css=".gradio-container {background-color: #f0f4f8}") as demo:
    gr.Markdown("# USD Currency Explorer for Kids")
    
    with gr.Tabs():
        with gr.TabItem("Explore Currency"):
            gr.Markdown("Click a coin or bill to learn more!")
            with gr.Column():
                # Buttons for each currency (2 per row)
                for i in range(0, len(currencies), 2):
                    with gr.Row():
                        for currency in currencies[i:i+2]:
                            btn = gr.Button(f"{currency['name']}", elem_classes="currency-btn")
                            btn.click(
                                show_currency,
                                inputs=gr.State(value=currency["name"]),
                                outputs=[
                                    gr.Image(label="Front Image"),
                                    gr.Image(label="Back Image"),
                                    gr.Markdown(label="Currency Info")
                                ]
                            )
            
            with gr.Row(visible=False):
                front_image = gr.Image(label="Front Image", width=200, interactive=False, show_download_button=False)
                back_image = gr.Image(label="Back Image", width=200, interactive=False, show_download_button=False)
            info_output = gr.Markdown(label="Currency Info", elem_classes="info-output")
        
        with gr.TabItem("Compare Amounts"):
            gr.Markdown("Select two currencies to see how they compare!")
            with gr.Row():
                currency1 = gr.Dropdown(
                    label="First Currency",
                    choices=[c["name"] for c in currencies],
                    value=currencies[0]["name"]
                )
                currency2 = gr.Dropdown(
                    label="Second Currency",
                    choices=[c["name"] for c in currencies],
                    value=currencies[1]["name"]
                )
            compare_button = gr.Button("Compare")
            output = gr.Markdown(label="Comparison Result")
            compare_button.click(
                fn=compare_currencies,
                inputs=[currency1, currency2],
                outputs=output
            )
        
        with gr.TabItem("Cost Calculator"):
            gr.Markdown("Enter a cost and pick a state to see the total with tax!")
            with gr.Row():
                item_cost = gr.Number(label="Item Cost ($)", value=1.00, precision=2)
                state = gr.Dropdown(
                    label="State",
                    choices=list(state_tax_rates.keys()),
                    value="California"
                )
            calculate_button = gr.Button("Calculate")
            cost_output = gr.Markdown(label="Cost Result")
            calculate_button.click(
                fn=calculate_cost,
                inputs=[item_cost, state],
                outputs=cost_output
            )

# Custom CSS for buttons and image handling
css = """
.currency-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 10px;
    font-size: 16px;
    background-color: #4a90e2;
    color: white;
    border: 2px solid #4a90e2;
    border-radius: 8px;
    transition: background-color 0.2s;
}
.currency-btn:hover {
    background-color: #357abd;
}
.currency-btn svg {
    display: inline-block;
    vertical-align: middle;
}
svg text {
    display: block !important;
    visibility: visible !important;
    fill: currentColor !important;
}
.image-container img {
    pointer-events: none; /* Prevent right-click download */
}
.image-container .download-btn {
    display: none !important; /* Hide download button */
}
.info-output {
    margin-top: 20px;
    text-align: center;
}
"""

# Apply CSS and launch
demo.css = css
demo.launch(server_name="0.0.0.0", server_port=7860)