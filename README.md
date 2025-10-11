# Soccer Stats

[![Build Status](https://github.com/pekko09/soccer_stats/actions/workflows/update_bvb_fixtures.yml/badge.svg)](https://github.com/pekko09/soccer_stats/actions/workflows/update_bvb_fixtures.yml)
![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## About

**Soccer Stats** is a fun development project to experiment with **Python**, **APIs**, and **GitHub Actions**.  
It currently focuses on **Borussia Dortmund fixtures** and publishes data via **GitHub Pages**.

There is **no commercial interest** — it’s purely a side project created for learning, automation, and fun.  
Additional add-ons and ideas already exist and will be added gradually, **without a fixed release schedule**.

---

## Features

- 🐍 Automated fixture updates using **GitHub Actions**  
- 📅 Automatically published and updated **calendar (ICS)**  
- 🌐 Hosted with **GitHub Pages**  
- 🔄 Regular background updates via API  

---

## Setup for developers

1. **Clone the repository**
   ```bash
   git clone https://github.com/pekko09/soccer_stats.git
   cd soccer_stats

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt

3. **Run locally**
    The main logic is implemented in the fixtures.py module, which defines a class responsible for fetching and preparing fixture data.
    Example usage:
    ```python
    from moduls.fixtures import MatchFixtures
    #Create instance
    bvb = MatchFixtures(teamshort='Dortmund', year_season=2025)
    #Create calendar and write file to docs folder
    bvb.make_ics()

## Future ideas
- Connect to Discord API for automated creation of matchday channels
- Build up statistics database
- Create a shiny app as user interface to input match data like line-ups etc
- Evaluate team statistics
- Create visualizations on team data

## License
This project is licensed under the MIT License.

## Contact
Author: [@pekko09](https://github.com/pekko09)

Feel free to open an issue or discussion for suggestions or questions.

## Class Diagram

```mermaid
classDiagram
    class APIClient {
        <<abstract>>
        + dict API_CONFIG
        + _build_headers() dict
        + query_api(ep: str, api_choice: str = 'oldb', params: dict|None = None) dict|list
        - base_url: str
        - auth_type: str
        - credential: str|None
    }

    class MatchFixtures {
        - str teamshort
        - str team_name
        - int year_season
        - int teamid
        - list matches
        + dict COMP_NAMES
        + __init__(teamshort: str, year_season: int)
        + get_teamid() int
        + get_matches(comp: str) None
        + get_all_matches() None
        + make_ics() None
    }

    APIClient <|-- MatchFixtures : inheritance
``

## Notes:
- **`APIClient`** handles API endpoints, headers, and authentication logic.  
- **`MatchFixtures`** builds on top of it to:
  - Retrieve teams and match data from OpenLigaDB  
  - Store, sort, and manage fixture lists  
  - Export events as `.ics` calendar files for GitHub Pages 