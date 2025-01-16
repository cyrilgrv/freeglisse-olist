# Web scrapping and Power BI dashboarding project

# Context
[Freeglisse.com](https://freeglisse.com/fr/12-ski-occasion) positions itself as the leading second-hand ski resale website in France.
It offers an extensive catalog of equipment, categorized by type of use, quality, brand, etc.
Our objective is to analyze the products available for resale on the site to assess its positioning and product offerings. This initiative is being conducted in preparation for the acquisition of the site by a third-party company (Olist).

# Mission
To achieve this, we will first collect product information through web scraping with Python (using BeautifulSoup and Selectolax) and then analyze the gathered data using a Power BI dashboard.

> Note : This project is an exercise as part of a data analysis training program, designed to teach web scraping techniques with Python and to master dashboard design using Power BI.

# Web scraping
## Additional information
Since the products on freeglisse.com are categorized into three quality levels (A, B, and C), we perform web scrapping from the base URLs stored in the [config.py](config.py) file :
```python
BASE_URLS = {
    "A": "https://freeglisse.com/fr/12-ski-occasion/s-1/etat_du_materiel-qualite_a?page=",
    "B": "https://freeglisse.com/fr/12-ski-occasion/s-1/etat_du_materiel-qualite_b?page=",
    "C": "https://freeglisse.com/fr/12-ski-occasion/s-1/etat_du_materiel-qualite_c?page=",
}
```

## Instructions to run the scrapping script :
Clone this repository, create a virtual environment, and install dependencies :
```bash
git clone https://github.com/cyrilgrv/freeglisse-olist/
cd freeglisse-olist
python3 -m venv venv
source venv/bin/activate #Unix
venv\Scripts\activate #Windows 
pip install -r requirements.txt
python main.py
```

# Dashboard :
>Note : The data displayed in this demo dashboard was fetched on on October 12, 2024.

[![Dashboard](https://img.shields.io/badge/Dashboard%20Power%20BI-View%20Online-yellow?logo=power-bi&logoColor=white)](https://app.powerbi.com/view?r=eyJrIjoiODcxMDQzZWUtMmQ3Yy00OTI2LWJlZGMtNTljNGQ5ZjczZDUwIiwidCI6IjJkNjhkYjFhLTNmY2QtNDZjMi1iNDNiLTlhYjE4NjU1NzY1NyIsImMiOjEwfQ%3D%3D)

[![screenshot](dashboard_screenshot.png)](https://app.powerbi.com/view?r=eyJrIjoiODcxMDQzZWUtMmQ3Yy00OTI2LWJlZGMtNTljNGQ5ZjczZDUwIiwidCI6IjJkNjhkYjFhLTNmY2QtNDZjMi1iNDNiLTlhYjE4NjU1NzY1NyIsImMiOjEwfQ%3D%3D)

## Tools Used
![Python Version](https://img.shields.io/badge/Python-3.12-blue)
[![VSCode](https://img.shields.io/badge/Editor-VSCode-blue?logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
![Power BI](https://img.shields.io/badge/Dashboard-Power%20BI-yellow?logo=power-bi&logoColor=white)

## Libraries Used
[![Pandas](https://img.shields.io/badge/Pandas-2.2.3-blue)](https://github.com/pandas-dev/pandas)
[![Requests](https://img.shields.io/badge/Library-Requests-blue?logo=python&logoColor=white)](https://github.com/psf/requests)
[![Beautiful Soup](https://img.shields.io/badge/Library-Beautiful%20Soup-green?logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/)
[![Selectolax](https://img.shields.io/badge/Library-Selectolax-orange?logo=python&logoColor=white)](https://github.com/rushter/selectolax)
[![Progress Bars](https://img.shields.io/badge/Progress%20Bars-tqdm-yellowgreen)](https://github.com/tqdm/tqdm)
