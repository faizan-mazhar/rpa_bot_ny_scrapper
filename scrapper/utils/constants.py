import os
import re

from RPA.Archive import Archive
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Excel.Files import Files as ExcelFiles

from scrapper import logger

WEB_SITE_URL = "http://www.nytimes.com/"
env = os.getenv('ENV')

OUTPUT_DIR = f"{os.getcwd()}/output"
EXCEL_FILE_PATH = f"{OUTPUT_DIR}/news.xlsx"

IMAGE_BASE_PATH = f"{OUTPUT_DIR}/news_images/"
IMAGES_ARCHIVE = f"{OUTPUT_DIR}/news_images.zip"
PATTERN = "\$?\s?\d+\s?,?.?[(USD)(dollars)]*\d?"


def check_output_folder():
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)


def archive_images():
    archive = Archive()
    archive.archive_folder_with_zip(IMAGE_BASE_PATH, IMAGES_ARCHIVE)


def store_in_excel(data_to_store):
    logger.info("[INFO]: Writing collected news element into excel file.")
    excel_client = ExcelFiles()
    excel_client.open_workbook(EXCEL_FILE_PATH)
    excel_client.append_rows_to_worksheet(data_to_store, header=True)
    excel_client.save_workbook()
    logger.info("[INFO]: Saved updated workbook with new news items.")


def contains_currency(text):
    """
    text: string to check if it contains currency or not
    """
    logger.info("[INFO]: checking if text contains any mention of currency.")
    regexp = re.compile(pattern=PATTERN)
    if regexp.search(text):
        return "True"
    return "False"


if env == 'PROD':
    work_items = WorkItems()
    work_items.get_input_work_item()
    work_item = work_items.get_work_item_variables()
    search_phrase = work_item.get("search_phrase", "")
    sections = work_item.get("sections")
    sections = eval(sections)
    number_of_month = work_item.get("number_of_months", 0)
else:
    search_phrase = 'python'
    sections = []
    number_of_month = 1


check_output_folder()

'''
any,Arts,Business,New York,Opinion,Podcasts,Style,Technology,U.S.,World
'''

