import logging
import os
import sqlite3
from typing import List, Tuple
import json
from abc import ABC, abstractmethod

from data_collector.scarping.entities.page_data import PageData
from data_collector.entities.url_topic import UrlTopic

class DataCollectionDal(ABC):

    @abstractmethod
    def inset_pages_data(self, pages_data: List[PageData]):
        pass

    @abstractmethod
    def insert_urls_topic(self, urls_topic: List[UrlTopic]):
        pass


class DataCollectionDalSqlLite(DataCollectionDal):
    CREATE_PAGES_DATA_QUERY_FILE_PATH = 'queries/create_page_data_query.sql'
    CREATE_URL_TOPIC_TABLE_QUERY_FILE_PATH = 'queries/create_url_topic_table_query.sql'

    INSERT_PAGES_DATA_QUERY_FORMAT = 'INSERT INTO pages_data  (url, source_url, depth,page_title, links_json) VALUES (?,?,?,?,?)'
    INSERT_URLS_TOPIC_QUERY_FORMAT = 'INSERT INTO urls_topics  (url, topic) VALUES (?,?)'

    def __init__(self, db_file: str = 'scraping_db'):
        self._db_file = db_file
        self._create_pages_data_table()
        self._create_url_topic_table()


    def _create_connection(self):
        return sqlite3.connect(self._db_file)

    def _read_query_from_file(self, query_file: str):

        current_dir = os.path.dirname(__file__)
        query_file_path = os.path.join(current_dir, query_file)

        with open(query_file_path, 'r') as f:
            return f.read()

    def _get_create_pages_table_query(self) -> str:
        return self._read_query_from_file(DataCollectionDalSqlLite.CREATE_PAGES_DATA_QUERY_FILE_PATH)

    def _get_create_url_topic_table_query(self) -> str:
        return self._read_query_from_file(DataCollectionDalSqlLite.CREATE_URL_TOPIC_TABLE_QUERY_FILE_PATH)


    def _create_pages_data_table(self):

        try:

            query = self._get_create_pages_table_query()
            with self._create_connection() as con:

                cur = con.cursor()
                cur.execute(query)
                con.commit()
        except Exception as e:
            logging.exception('_create_pages_data_table')
            raise e

    def _create_url_topic_table(self):

        try:

            query = self._get_create_url_topic_table_query()
            with self._create_connection() as con:

                cur = con.cursor()
                cur.execute(query)
                con.commit()

        except Exception as e:
            logging.exception('_create_pages_data_table')
            raise e

    def _batch_insert(self, query, rows: List[Tuple]):

        try:
            logging.info(f'insert {len(rows)} rows')

            with self._create_connection() as con:

                con.executemany(query, rows)
                con.commit()

                logging.info('insert completed')

        except Exception as e:
            logging.exception(f'insert {query} failed')
            raise e


    def inset_pages_data(self, pages_data: List[PageData]):

        try:
            rows = [(page_data.page_url,
                         page_data.source_url,
                         page_data.depth,
                         page_data.page_title,
                         json.dumps(
                             [link.dict() for link in
                              page_data.page_links]) if page_data.page_links is not None else None)
                        for page_data in pages_data]

            self._batch_insert(DataCollectionDalSqlLite.INSERT_PAGES_DATA_QUERY_FORMAT, rows)

        except Exception as e:
            logging.exception('inset_pages_data')
            raise e

    def insert_urls_topic(self, urls_topic: List[UrlTopic]):

        try:

            rows = [(url_topic.url, url_topic.topic) for url_topic in urls_topic]
            self._batch_insert(DataCollectionDalSqlLite.INSERT_URLS_TOPIC_QUERY_FORMAT, rows)
        except Exception as e:
            logging.exception('insert_urls_topic')
            raise e

