# USD Kids Program

## Description
The **USD Kids Program** is an educational Gradio-based web application designed to help young learners explore U.S. currency in an interactive way. This tool allows users to:
- **Explore Currency**: View front and back images of coins and bills, along with their values and types.
- **Compare Amounts**: Compare the value of different currencies (e.g., how many Nickels equal a Quarter).
- **Cost Calculator**: Calculate the total cost of an item with sales tax for any U.S. state, displaying the breakdown in currency denominations.

Built with Python and Gradio, this app uses local image files for currency visuals and includes approximate 2025 state sales tax rates for educational purposes. It’s a fun and engaging way for kids to learn about money management and taxation!

## Features
- Interactive tabs for exploring, comparing, and calculating costs.
- Visual representation of currency using SVG symbols.
- Support for all U.S. coins (Penny, Nickel, Dime, Quarter, Half Dollar, Dollar Coin) and bills ($1, $2, $5, $10, $20, $50, $100).
- State-specific sales tax calculations based on 2025 averages.
- Simple, kid-friendly interface with a blue theme.

## Installation
1. **Clone the Repository**:

git clone https://github.com/your-username/USDKidsProgram.git
cd USDKidsProgram
text
2. **Set Up a Virtual Environment**:

python -m venv venv
call venv\Scripts\activate  # On Windows
source venv/bin/activate    # On macOS/Linux
text
3. **Install Dependencies**:

pip install -r requirements.txt
text
4. **Prepare Image Files**:
- Create an `images` folder in the project directory.
- Add PNG files named `penny_front.png`, `penny_back.png`, etc., for each currency (front and back). These can be placeholder images or sourced from public domain resources (ensure proper licensing).
5. **Run the Application**:
- Use the provided `setup_and_run.bat` (Windows) or run manually:

python app.py
text
- Access the app at `http://localhost:7860`.

## Usage
- **Explore Currency**: Click any coin or bill button to see its images and details.
- **Compare Amounts**: Select two currencies and click "Compare" to see their relationship.
- **Cost Calculator**: Enter an item cost and state, then click "Calculate" to see the total with tax and currency breakdown.

## Known Issues
- **Coin Labeling Flaw**: The original design intended to display cent symbols (e.g., "5¢") on coins, but due to rendering issues with SVG `<text>` elements in Gradio’s Markdown environment, the symbols are not visible. As a workaround, the app currently displays plain numbers (e.g., "5" for Nickel, "25" for Quarter) and "$1" for the Dollar Coin. This ensures visibility but deviates from the intended currency notation. A future update could explore alternative rendering methods (e.g., `<span>` tags or image-based labels) to restore the cent symbols.

## Contributing
This project is open source, and I welcome contributions from the community! To contribute:
1. Fork the repository.
2. Create a branch for your feature or fix: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Description of changes"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request with a detailed description of your changes.

## Support the Project
If you enjoy using the USD Kids Program and find it valuable, consider supporting my work with a donation! Your contributions help me continue developing educational tools for the community. Please visit https://mtnmuscle.com/donation-page/ to send a donation. **Note: All donations are non-refundable and final. Thank you for your support!**

## License
This project is released under the [MIT License](LICENSE). Feel free to use, modify, and distribute it, provided you include the original copyright and license notice.

## Acknowledgments
- Built with Gradio for the interactive interface.
- Inspired by the need to educate kids about U.S. currency in a fun way.
- Thanks to the open-source community for tools and support!
- Utilized Grok AI for helping with code development
- Also this was my first GitHub Repository and my attempt at coding. My hope is it will help educate your children or someone you are helping. My best to you! 