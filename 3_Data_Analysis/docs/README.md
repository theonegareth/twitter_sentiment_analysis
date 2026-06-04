# Twitter Sentiment & Financial Market Impact — DPR Protests (Aug–Sep 2025)

## Quick Navigation

| Document | Content |
|---|---|
| 📘 **[MASTER_ANALYSIS_REPORT.md](MASTER_ANALYSIS_REPORT.md)** | **Start here** — step-by-step master document, all results, pipeline, file inventory |
| 📊 [pearson_correlation_analysis.md](pearson_correlation_analysis.md) | Pearson + Spearman correlations with p-values and 95% CIs |
| 📊 [correlation_robustness.md](correlation_robustness.md) | Robustness after outlier treatment/winsorization |
| 📊 [outlier_diagnostics.md](outlier_diagnostics.md) | Outlier detection (IQR + Z-score + MAD) with dates |
| 📊 [diagnostic_summary_table.md](diagnostic_summary_table.md) | Unified table: N, mean, SD, skew, kurtosis, normality, stationarity, outliers |
| 📈 [normality_test_report.md](normality_test_report.md) | Shapiro-Wilk + Jarque-Bera + D'Agostino + KS tests |
| 📈 [stationarity_test_report.md](stationarity_test_report.md) | ADF (3 specs) + KPSS (2 specs) on 16 series |
| 📈 [diagnostic_plots.md](diagnostic_plots.md) | Description of all diagnostic charts |
| 🗂 [market_data_merge_analysis.md](market_data_merge_analysis.md) | Trading days, paired observations, non-trading day treatment |
| 🤖 [model_comparison_table.md](model_comparison_table.md) | GPT-5/4.1 model sentiment/emotion accuracy benchmarks |

### Charts
- `charts/` — 9 main PNGs (scatter, timeline, heatmap, event study, boxplots)
- `charts/diagnostics/` — 10 diagnostic PNGs (histograms, Q-Q, violin, ECDF, residuals, pairwise matrix)

### Run All Analyses
```bash
py pearson_correlation_analysis.py
py create_charts.py
py create_diagnostic_plots.py
py normality_tests.py
py stationarity_tests.py
py outlier_diagnostics.py
py correlation_robustness.py
py diagnostic_summary.py
```

---

## Project Background

Indonesian Twitter sentiment analysis during the August–September 2025 DPR protests and their financial market impact. The analysis combines scraped Twitter data (42 keywords across 3 periods), VADER sentiment scoring, Yahoo Finance market data (IHSG, USD/IDR), and GPT model benchmarking.

**Time spans:**
- Before Demo: Aug 1 – Aug 24
- Demo: Aug 25 – Sep 8
- After Demo: Sep 9 – Sep 30

**Minimum target:** 10,000 tweets for sentiment analysis

---

## Keyword List

(Original project specification)

demo DPR
tolak tunjangan
bubarkan DPR
mahasiswa bergerak
ahmad sahroni
uya kuya
eko patrio
ojol dilindas
polisi pembunuh
affan Kurniawan
mako brimob
17+8 tuntutan rakyat
RUU Perampasan Aset
ACAB
IHSG
Saham turun
Saham naik
nilai tukar rupiah
anarkis
bursa efek
BEI (bursa efek indonesia)
anjlok
merah
nyangkut
panic selling
naik
menguat
hijau
rebound
asing cabut
foreign outflow
jual saham
kurs rupiah
nilai tukar
USD/IDR
melemah
Bank Indonesia
ekonomi Indonesia
pasar keuangan
stabilitas ekonomi
krisis ekonomi
dampak demo rupiah

---

## Original Event Log & Keyword Reference


### 1. Protest Actions & Demands
* demo DPR
* unjuk rasa (demonstration)
* tolak tunjangan (reject allowances)
* bubarkan DPR (dissolve DPR)
* 17+8 tuntutan rakyat (17+8 people's demands)
* RUU Perampasan Aset (Asset Forfeiture Bill)
* anarkis (anarchist/anarchic)
* ricuh (chaotic/riot)
* bentrok (clash)
* kekerasan aparat (apparatus violence)
* represif (repressive)
* usut tuntas (investigate thoroughly)

### 2. Key Incidents & Police Response
* ojol dilindas (online driver run over)
* Affan Kurniawan
* polisi pembunuh (killer police)
* terlindas (run over)
* Rantis (Kendaraan Taktis / Tactical Vehicle)
* gas air mata (tear gas)
* gas air mata kedaluwarsa (expired tear gas)
* water cannon

### 3. Involved Groups & Public Figures
* mahasiswa bergerak (students are moving)
* Aliansi Mahasiswa (Student Alliance)
* BEM SI (All-Indonesia Student Executive Board)
* buruh (workers/laborers)
* Partai Buruh (Labor Party)
* KSPI (Confederation of Indonesian Trade Unions)
* Ahmad Sahroni
* Uya Kuya
* Eko Patrio
* Puan Maharani (DPR Speaker)
* Kapolri (National Police Chief)
* Presiden Prabowo (President Prabowo)
* Sufmi Dasco Ahmad
* Adies Kadir

### 4. Key Institutions & Locations
* DPR (Dewan Perwakilan Rakyat)
* polisi (Polri / National Police)
* mako brimob (Brimob headquarters)
* TNI (Indonesian National Armed Forces)
* Bank Indonesia
* MKD (Mahkamah Kehormatan Dewan / DPR Ethics Council)
* Gedung DPR
* Senayan
* Jakarta
* Medan
* Surabaya
* Pontianak

### 5. Economic Impact & Financial Terms
* IHSG (Jakarta Composite Index)
* Saham turun / Saham naik
* BEI (Bursa Efek Indonesia)
* bursa efek
* anjlok (plummeted)
* merah (red, market down) / hijau (green, market up)
* naik / menguat / rebound
* nyangkut (stuck in a losing stock position)
* panic selling
* jual saham
* asing cabut (foreigners pull out)
* foreign outflow
* investor kabur (investors flee)
* sentimen negatif (negative sentiment)
* nilai tukar rupiah / kurs rupiah
* USD/IDR
* melemah (weakened)
* ekonomi Indonesia
* pasar keuangan
* stabilitas ekonomi
* krisis ekonomi
* dampak demo rupiah

### 6. Viral Hashtags & Symbolic Slang
* ACAB
* 1312
* #PolisiPembunuhRakyat
* #BubarkanDPR
* #TolakTunjanganDPR
* #AffanKurniawan
* #StopKekerasanAparat
* #GejayanMemanggil
* Brave Pink
* Hero Green
* Resistance Blue
* "Demi Un Grr"

### **Monday, August 25, 2025: The Protest Begins**
* **Keywords:** `demo DPR`, `mahasiswa bergerak`, `tolak tunjangan`, `Gedung DPR`, `Senayan`, `ricuh`
* **Summary:** The initial large-scale **demo DPR** (DPR protest) begins at the **Gedung DPR** in **Senayan, Jakarta**. The primary trigger is public anger over proposed parliamentary allowance increases, with protesters carrying signs to **"tolak tunjangan"** (reject allowances). The demonstration, involving students and other groups, turns **ricuh** (chaotic) by the afternoon, leading to clashes with police, who deploy **gas air mata** and **water cannon**.

### **Tuesday, August 26, 2025: Public Anger Simmers**
* **Keywords:** `Ahmad Sahroni`, `Uya Kuya`, `Eko Patrio`
* **Summary:** While the streets are relatively calmer, public anger intensifies online. Statements from politicians like **Ahmad Sahroni** (who called protesters "stupid") and viral videos of **Uya Kuya** and **Eko Patrio** dancing during a parliamentary session are widely circulated, becoming symbols of elite detachment.

### **Wednesday, August 27, 2025: Protests Spread**
* **Keywords:** `Pontianak`, `Medan`, `mahasiswa bergerak`
* **Summary:** The **demo DPR** movement spreads to other major cities. In **Pontianak**, students reportedly storm the regional DPRD building. Protests are also held in **Medan** and **Surabaya**, all echoing the **"tolak tunjangan"** and anti-DPR sentiments.

### **Thursday, August 28, 2025: The Day of Escalation**
* **Keywords:** `buruh`, `bentrok`, `Rantis`, `ojol dilindas`, `Affan Kurniawan`, `polisi pembunuh`
* **Summary:** The protests in Jakarta swell as groups of **buruh** (workers) join students. The situation escalates into a major **bentrok** (clash). In the evening, a police tactical vehicle (**Rantis**) strikes and kills an **ojol** (online driver) named **Affan Kurniawan** in the Pejompongan area. The incident is captured on video, and the keywords **"ojol dilindas"** and **"polisi pembunuh"** go viral, marking a tragic turning point.

### **Friday, August 29, 2025: Financial Panic and Public Fury**
* **Keywords:** `IHSG`, `anjlok`, `melemah`, `USD/IDR`, `asing cabut`, `ACAB`, `1312`, `Mako Brimob`
* **Summary:** The **dampak demo rupiah** (protest's impact on the rupiah) hits the **pasar keuangan** (financial market). The **IHSG** (stock index) **anjlok** (plummets) due to the instability, with **asing cabut** (foreign outflow) reported. The **nilai tukar rupiah** (rupiah exchange rate) **melemah** (weakens) significantly against the **USD/IDR**.
* Simultaneously, outrage over Affan's death peaks. The hashtags **ACAB** and **1312** flood social media. Masses of fellow ojol drivers and protesters gather to demand accountability, with some surrounding the **Mako Brimob** (Brimob Headquarters).

### **Saturday, August 30, 2025: Anger Redirected**
* **Keywords:** `Ahmad Sahroni`, `Uya Kuya`, `Eko Patrio`, `anarkis`
* **Summary:** Protests continue. Public anger, already high from the protest leaders' perceived arrogance, is redirected. Reports and videos emerge of crowds targeting the homes of politicians, including **Ahmad Sahroni**, **Uya Kuya**, and **Eko Patrio**, with some acts of vandalism and property damage reported.

### **Early September (Circa Sept 1-2): Consolidation of Demands**
* **Keywords:** `17+8 tuntutan rakyat`, `RUU Perampasan Aset`, `Hero Green`, `Brave Pink`
* **Summary:** In the wake of the week's chaos, activist groups, influencers, and student bodies consolidate their goals into the **"17+8 tuntutan rakyat"** (17+8 People's Demands). This list broadens the protest's scope beyond just allowances, demanding systemic reform, justice for **Affan Kurniawan**, and the immediate passage of the **RUU Perampasan Aset** (Asset Forfeiture Bill).
* The symbolic language of the protest solidifies. **"Hero Green"** (for Affan's jacket) and **"Brave Pink"** (for a female protester) become viral symbols of solidarity, and the satirical phrase **"Demi Un Grr"** is widely used to mock the DPR.