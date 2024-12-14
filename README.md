# Automated Data Analysis and Visualization with GPT-4o-Mini

## **Project Overview**
This project showcases an advanced Python script designed to automatically perform data analysis, generate visualizations, and craft insightful narratives using GPT-4o-Mini. It dynamically adapts to any given dataset, offering meaningful insights through detailed reports and visuals in Markdown format.

## **Key Features**
1. **Comprehensive Data Analysis**
   - Summarizes key statistics, identifies missing values, and detects anomalies.
   - Performs advanced analyses such as correlation studies and clustering for deeper insights.
   - Integrates with GPT-4o-Mini to provide additional analytical depth and recommendations.

2. **Dynamic Visualizations**
   - Automatically generates up to 3 charts (PNG format) tailored to the dataset.
   - Includes various visualization types like histograms, heatmaps, and bar charts for clarity.

3. **Narrative Generation**
   - Leverages GPT-4o-Mini to create a cohesive Markdown report (`README.md`).
   - Narratives include dataset descriptions, methodologies, findings, and implications.

4. **Optimized Resource Usage**
   - Processes data locally, sending only summaries to the LLM to minimize token usage while retaining analytical richness.

5. **Universal Dataset Compatibility**
   - Adapts seamlessly to CSV datasets with diverse column types, structures, and complexities.

6. **Standalone Execution**
   - Operates independently, requiring no external dependencies beyond standard Python libraries.

## **Workflow**
### 1. Data Preprocessing
   - Reads and analyzes the input CSV file to extract metadata (e.g., column names, data types).
   - Handles missing data and identifies potential outliers.

### 2. Exploratory Data Analysis (EDA)
   - Provides statistical summaries, correlation matrices, and outlier detection.
   - Clustering techniques group similar data points for actionable insights.

### 3. GPT-4o-Mini Integration
   - Summarized EDA results are sent to the LLM for advanced insights and recommendations.
   - Dynamic prompts ensure tailored narratives based on the dataset's characteristics.

### 4. Visualization
   - Creates professional-grade visualizations using Seaborn and Matplotlib.
   - Outputs PNG files for easy integration into Markdown reports.

### 5. Narrative Report Generation
   - GPT-4o-Mini crafts a structured narrative incorporating key findings, visualizations, and implications.

## **Usage Instructions**
1. **Setup:**
   - Clone this repository and navigate to the project directory.
   - Configure the required environment variable for authentication:
     ```bash
     export AIPROXY_TOKEN=your-token-here
     ```

2. **Run the Script:**
   - Execute the script using the `uv` CLI tool:
     ```bash
     uv run autolysis.py dataset.csv
     ```

3. **Output:**
   - The script generates the following in the current working directory:
     - `README.md`: A Markdown report summarizing the analysis and visualizations.
     - `*.png`: Visualization charts saved as PNG files.

## **Technical Highlights**
- **LLM Optimization:**
  - Efficiently uses GPT-4o-Mini by sending preprocessed summaries rather than raw datasets.
  - Utilizes OpenAI's function-calling API for precise recommendations.

- **Visualization Tools:**
  - Employs Seaborn and Matplotlib to create compelling visualizations.

- **Environment Requirements:**
  - Requires the `AIPROXY_TOKEN` environment variable for GPT-4o-Mini integration.

## **Sample Datasets**
The script has been tested on the following datasets:
1. `goodreads.csv`: Analyzes 10,000 books with metadata such as genres and ratings.
2. `happiness.csv`: Explores global happiness indices and contributing factors.
3. `media.csv`: Examines faculty ratings of movies, TV series, and books.

## **Deliverables**
- **Core Script:**
  - `autolysis.py`: The standalone Python script encapsulating all functionalities.
  
- **Generated Outputs:**
  - Subdirectories for each dataset (e.g., `goodreads/`, `happiness/`, `media/`) containing:
    - `README.md`: Comprehensive Markdown report.
    - `*.png`: Visualization files in PNG format.

## **Licensing**
This project is licensed under the MIT License. For details, refer to the LICENSE file in the repository.

## **Conclusion**
This project exemplifies the power of integrating advanced analytical techniques with GPT-4o-Mini, providing both technical rigor and practical utility for automated data analysis and visualization. Explore the potential of automated insights and storytelling with this cutting-edge tool!
