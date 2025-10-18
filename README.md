## 📊 Startup Funding Analysis Dashboard

An interactive **Streamlit dashboard** that provides detailed insights into Indian startup funding trends.
The project visualizes investment patterns, funding types, top investors, and startup performance using a clean and data-driven interface.

---

### 🧠 Features

#### **1️⃣ Overall Analysis**

* 📅 **Month-on-Month (MoM) Trend** – View funding growth by total investment or count.
* 💳 **Metric Cards** – Displays total, maximum, and average funding amounts.
* 🏢 **Sector Analysis (Pie Charts)** – Visualize which industries receive the most funding (by count and total).
* 💸 **Type of Funding** – See distribution by funding type (e.g., Seed, Series A, Debt).
* 🗺️ **City-wise Funding** – Analyze where most startups are located and funded.
* 🔥 **Top Startups & Investors** – Identify leaders by investment amount and frequency.
* 🌡️ **Funding Heatmap** – Explore monthly or yearly trends in a single visualization.

---

#### **2️⃣ Company POV**

Get detailed insights into any **specific startup**:

* 🏷️ Name & Founders
* 🏭 Industry & Sub-industry
* 📍 Location
* 💰 Funding Rounds (Stage, Investors, Date, Amount)
* 🤝 Similar Companies in the same sector

---

#### **3️⃣ Investor POV**

Explore data from an **investor’s perspective**:

* 📈 Yearly investment trends
* 💸 Top startups funded by the investor
* 🏙️ City-wise and industry-wise distribution
* 🔍 Investment stage preferences

---

### 🧰 Tech Stack

| Component           | Technology                                      |
| ------------------- | ----------------------------------------------- |
| **Frontend**        | Streamlit                                       |
| **Backend / Logic** | Python (Pandas, Matplotlib, Seaborn)            |
| **Data**            | Startup funding dataset (CSV/Excel)             |
| **Visualization**   | Line charts, Pie charts, Heatmaps, Metric Cards |

---

### ⚙️ Installation & Setup

```bash
# 1️⃣ Clone the repository
git clone https://github.com/<your-username>/startup-funding-analysis.git
cd startup-funding-analysis

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Run the Streamlit app
streamlit run app.py
```

---

### 📁 Project Structure

```
📦 startup-funding-analysis
├── 📄 app.py                 # Main Streamlit application
├── 📄 README.md              # Project documentation
├── 📄 requirements.txt       # Dependencies
├── 📁 data/                  # Dataset (CSV / Excel)
└── 📁 images/                # Optional visuals or logos
```

---

### 📊 Example Visuals

| Visualization | Description                                  |
| ------------- | -------------------------------------------- |
| MoM Chart     | Month-on-Month funding growth                |
| Pie Charts    | Industry and Funding Type distribution       |
| Heatmap       | Yearly funding intensity                     |
| Metric Cards  | Quick summary of total, max, avg investments |

---

### 🚀 Future Improvements

* Add **AI-based funding prediction** using ML regression models.
* Integrate **filter-based dashboard** (by city, year, or sector).
* Export reports to **PDF or Excel** format.
* Deploy on **Streamlit Cloud or Hugging Face Spaces**.

---
