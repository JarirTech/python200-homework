import os
import pandas as pd
import matplotlib

# FIX Tkinter thread crash on Windows
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from scipy.stats import pearsonr
from smolagents import tool, CodeAgent, OpenAIServerModel

# =========================
# GLOBAL DATAFRAME
# =========================
df = None

# Local merged dataset
DATA_PATH = "assignments_01\outputs\merged_happiness.csv"

# Optional fallback folder
FALLBACK_DIR = "assignments\resources\happiness_project"


# ================================================================
# cleaning df

def clean_columns(dataframe):
    """
    Normalize column names.
    """

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return dataframe


# =========================
# TOOL 1: LOAD DATA
# =========================
@tool
def load_happiness_data() -> dict:
    """
    Load the World Happiness dataset into memory.

    Returns:
        dict: Dataset shape and column names
    """

    global df

    try:

        # -------------------------
        # OPTION 1: merged file
        # -------------------------
        if os.path.exists(DATA_PATH):

            df = pd.read_csv(
                DATA_PATH,
                sep=",",
                encoding="utf-8",
                on_bad_lines="skip"
            )
        # -------------------------
        # OPTION 2: fallback folder
        # -------------------------
        else:

            files = []

            for file in os.listdir(FALLBACK_DIR):

                if file.endswith(".csv"):

                    temp = pd.read_csv(
                         os.path.join(FALLBACK_DIR, file),
                         sep=",",
                         encoding="utf-8",
                         on_bad_lines="skip"
                    )
                    

                    files.append(temp)

            df = pd.concat(files, ignore_index=True)

        # clean column names
        df = clean_columns(df)

        # numeric conversion
        numeric_cols = [
            "happiness_score",
            "gdp_per_capita",
            "social_support",
            "healthy_life_expectancy",
            "freedom_to_make_life_choices",
            "generosity",
            "perceptions_of_corruption",
            "year"
        ]

        for col in numeric_cols:

            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return {
            "shape": df.shape,
            "columns": df.columns.tolist()
        }

    except Exception as e:

        df = None

        return {
            "error": str(e)
        }


# =========================
# TOOL 2: SUMMARY
# =========================
@tool
def summarize_column(column: str) -> dict:
    """
    Return summary statistics for a numeric column.

    Args:
        column (str): Name of the column

    Returns:
        dict: Statistical summary
    """

    global df

    if df is None:
        load_happiness_data()

    if column not in df.columns:

        return {
            "error": f"Column '{column}' not found"
        }

    summary = df[column].describe()

    return {
        k: round(v, 4)
        for k, v in summary.to_dict().items()
    }


# =========================
# TOOL 3: CORRELATION
# =========================
@tool
def compute_correlation(col1: str, col2: str) -> dict:
    """
    Compute Pearson correlation between two columns.

    Args:
        col1 (str): First numeric column
        col2 (str): Second numeric column

    Returns:
        dict: Correlation statistics
    """

    global df

    if df is None:
        load_happiness_data()

    if col1 not in df.columns or col2 not in df.columns:

        return {
            "error": "Column not found"
        }

    temp = df[[col1, col2]].dropna()

    r, p = pearsonr(temp[col1], temp[col2])

    return {
        "column_1": col1,
        "column_2": col2,
        "pearson_r": round(float(r), 4),
        "p_value": round(float(p), 6),
        "significant": bool(p < 0.05)
    }


# =========================
# TOOL 4: TOP COUNTRIES

@tool
def get_top_n_countries(
    column: str,
    year: int,
    n: int = 5
) -> list:
    """
    Get top N countries ranked by a column.

    Args:
        column (str): Ranking column
        year (int): Year filter
        n (int): Number of countries

    Returns:
        list: Top countries
    """

    global df

    if df is None:
        load_happiness_data()

    if column not in df.columns:

        return [{
            "error": f"Column '{column}' not found"
        }]

    filtered = df[df["year"] == year]

    top = (
        filtered
        .sort_values(column, ascending=False)
        .head(n)[["country", column]]
    )

    return top.to_dict(orient="records")


# =========================
# TOOL 5: BEST YEAR
# =========================
@tool
def get_best_happiness_year() -> dict:
    """
    Find the year with highest average happiness score.

    Returns:
        dict: Best year and average score
    """

    global df

    if df is None:
        load_happiness_data()

    yearly_avg = (
        df.groupby("year")["happiness_score"]
        .mean()
    )

    best_year = yearly_avg.idxmax()

    return {
        "year": int(best_year),
        "average_happiness_score": round(
            float(yearly_avg.max()),
            4
        )
    }


# ===================================================================================
# TOOL 6: PLOT

@tool
def plot_happiness_by_region() -> dict:
    """
    Plot happiness score over years by region.

    Returns:
        dict: Saved plot path
    """

    global df

    if df is None:
        load_happiness_data()

    os.makedirs("outputs", exist_ok=True)

    regional_avg = (
        df.groupby(
            ["year", "regional_indicator"]
        )["happiness_score"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(12, 6))

    for region in regional_avg["regional_indicator"].unique():

        subset = regional_avg[
            regional_avg["regional_indicator"] == region
        ]

        plt.plot(
            subset["year"],
            subset["happiness_score"],
            label=region
        )

    plt.title("Average Happiness Score by Region")
    plt.xlabel("Year")
    plt.ylabel("Happiness Score")

    plt.legend(
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )

    plt.tight_layout()

    output_path = "outputs/happiness_by_region.png"

    plt.savefig(output_path)

    
    plt.close()

    return {
        "message": "Plot saved successfully",
        "path": output_path
    }


# ===========================================================

# Task 2: Build the Agent
# MODEL

model = OpenAIServerModel(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_id="gpt-4o-mini"
)

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are a World Happiness dataset analyst.

IMPORTANT RULES:
- ALWAYS use tools first.
- NEVER assume load_happiness_data() returns a dataframe.
- load_happiness_data() returns ONLY:
  {
    "shape": ...,
    "columns": ...
  }

- The real dataframe is stored internally.
- Use tools instead of writing custom pandas code whenever possible.
- Be concise.
"""

# AGENT

agent = CodeAgent(
    tools=[
        load_happiness_data,
        summarize_column,
        compute_correlation,
        get_top_n_countries,
        get_best_happiness_year,
        plot_happiness_by_region
    ],
    model=model,
    instructions=SYSTEM_PROMPT,
    additional_authorized_imports=[
        "pandas",
        "matplotlib.pyplot",
        "scipy.stats"
    ],
    max_steps=6
)


# ============================================================
# Task 3: Run Guided Queries

# QUERIES

queries = [

    "Load the happiness data and tell me its shape and column names.",

    "Summarize the happiness_score column.",

    "What is the correlation between gdp_per_capita and happiness_score? Is it significant?",

    "Show me the top 5 happiest countries in 2020.",

    "Plot happiness_score over years by region and save it to outputs/happiness_by_region.png.",

    #Task 4: Your Own Questions
    "Which year had the highest average happiness_score?",

    "Show correlation between freedom_to_make_life_choices and happiness_score."
]
# ==========================================================
#-----Running the Project----
# MAIN

if __name__ == "__main__":

    os.makedirs("outputs", exist_ok=True)

    print("\n===== WORLD HAPPINESS AGENT =====\n")

    for q in queries:

        print("\n" + "=" * 60)
        print("Q:", q)
        print("=" * 60)

        try:

            result = agent.run(
                q,
                reset=False
            )

            print(result)

        except Exception as e:

            print("ERROR:", str(e))

#====================================================================

# Task 5: Reflection
# 
#
# 1. The agent showed statistical significance by using the p-value.
#    It marked the result as significant when the p-value was below 0.05.
#    Yes, it used the p-value correctly.
#
# 2. I was surprised that the agent could automatically create plots
#    and answer custom questions using the tools without extra coding.
#
# 3. One useful additional tool would be a filtering tool.
#    It could filter data by region or year and help answer questions
#    like "Which region had the highest happiness score in 2021?"

