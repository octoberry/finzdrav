# -*- coding: utf-8 -*-
__author__ = 'fuse'

import requests
import json
from datetime import datetime

base_url = 'http://95.143.124.220:9200/hack'


def get_bar_stats(date_from, date_to):
    query = {
      "query": {
        "filtered": {
          "query": {
            "query_string": {
              "query": "group_name=(*Miscell*)"
            }
          },
          "filter": {
            "bool": {
              "must_not": [
                {
                  "query": {
                    "query_string": {
                      "query": "address_name:(\"NULL\")"
                    }
                  }
                },
                {
                  "query": {
                    "query_string": {
                      "query": "address_name:(\"CARD2CARD OPP PEREVOD\")"
                    }
                  }
                },
                {
                  "query": {
                    "query_string": {
                      "query": "address_name:(\"Alfa-Bank ATM\")"
                    }
                  }
                },
                {
                  "query": {
                    "query_string": {
                      "query": "address_name:(\"APPLE ITUNES STORE-RUB\")"
                    }
                  }
                }
              ]
            }
          }
        }
      },
      "aggs": {
        "range": {
          "date_range": {
            "field": "@timestamp",
            "format": "yyyy-MM-dd",
            "ranges": [
              {
                "to": date_to.strftime('%Y-%m-%d'),
                "from": date_from.strftime('%Y-%m-%d')
              }
            ]
          },
          "aggs": {
            "stats": {
              "extended_stats": {
                "field": "amount"
              }
            }
          }
        }
      }
    }
    res = _search(query)
    return res['aggregations']['range']['buckets'][0]['stats']


def get_mcdonalds_stats(date_from, date_to):
    return get_stats_by_token('FRESHC', date_from, date_to)


def get_stats_by_token(token, date_from, date_to):
    query = {
      "query": {
        "filtered": {
          "query": {
            "query_string": {
              "query": "address_name=(*%s*)" % token
            }
          }
        }
      },
      "aggs": {
        "range": {
          "date_range": {
            "field": "@timestamp",
            "format": "yyyy-MM-dd",
            "ranges": [
              {
                "to": date_to.strftime('%Y-%m-%d'),
                "from": date_from.strftime('%Y-%m-%d')
              }
            ]
          },
          "aggs": {
            "stats": {
              "extended_stats": {
                "field": "amount"
              }
            }
          }
        }
      }
    }
    res = _search(query)
    return res['aggregations']['range']['buckets'][0]['stats']


def _search(query):
    return _post('/_search?pretty', query)

def _post(uri, data):
    r = requests.post(base_url + uri, data=json.dumps(data))
    return r.json()


if __name__ == "__main__":
    date_from = datetime(2014, 5, 1)
    date_to = datetime(2014, 6, 1)
    print get_bar_stats(date_from, date_to)
    print get_mcdonalds_stats(date_from, date_to)
    print get_stats_by_token('FRESHCAFE', date_from, date_to)
