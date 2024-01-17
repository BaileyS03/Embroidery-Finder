# EmbroideryFinder

## Overview

EmbroideryFinder is a personal project aimed at collecting and organizing embroidery-related data from various vendors. The project utilises Python and Scrapy to scrape data from vendor websites and stores the information in a SQLite3 database.

## Features

- **Web Scraping**: The project uses Scrapy, a powerful and flexible web scraping framework in Python, to extract embroidery-related data from vendor websites.
  
- **SQLite3 Database**: The scraped data is stored in an SQLite3 database, providing a structured and efficient way to organize and query the information.

## Getting Started

### Prerequisites

- **Python**: Ensure that you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/EmbroideryFinder.git
    ```

2. **Install the required dependencies:**

    ```bash
    cd EmbroideryFinder
    pip install -r requirements.txt
    ```

### Usage

1. **Run the Scrapy spiders to start scraping data:**

    - For DesignsByJuJu:

        ```bash
        scrapy crawl DesignsByJuJu
        ```

    - For Bunnycup:

        ```bash
        scrapy crawl BunnyCupSetSpider
        ```

   Adjust the spider names (`designsbyjuju` and `bunnycup`) based on your project structure.

2. **The scraped data will be stored in the SQLite3 database (`central_database.db` by default).**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Scrapy community for providing an excellent web scraping framework.
- Special thanks to BunnyCup Embroidery and DesignsByJuJu for inspiration and data.
