from time import perf_counter
from spiders import *
from myparser import *


if __name__ == '__main__':

    time_start = time.perf_counter()

    # GET COLLECTION URLS FROM A FILE
    coll_urls = get_coll_urls()

    # GET APP LINKS FROM EACH COLLECTION
    print('MAIN: CRAWLING LINKS')

    collections = []  # [(collection name, 200 links),
                      # (collection name, 200 links),
                      # (collection name, 200 links)]

    for url in coll_urls:
        urlspider = SpiderUrl(url)
        urlspider.scroll_down_inf()
        collections.append(urlspider.crawl_links())

    # GET THE DATA ABOUT EVERY APP IN EVERY COLLECTION
    print('MAIN: CRAWLING APPS')

    collections_data = {}  # {'coll name1': [{'name': 'App1', 'dev': 'Corp1'}, {'name': 'App2', 'dev': 'Corp2'}],
                           #  'coll name2': [{'name': 'App2', 'dev': 'Corp2'}, {'name': 'App2', 'dev': 'Corp2'}]}
                           # OR {coll name: 200 D's with data}
    
    for collection in collections:
        print(f'MAIN: Crawling collection "{collection[0]}"')

        time_s_c = perf_counter()

        appspider = SpiderApp(collection[1])

        collections_data[collection[0]] = appspider.crawl_apps()

        time_f_c = perf_counter()
        time_t_c = time_f_c - time_s_c
        print(f'MAIN: Time taken for "{collection[0]}" is {time_t_c} seconds.')

    appspider.quit()

    print('\nMAIN: All crawling complete\n')

    # PARSE THE DATA INTO JSON
    final_data = lexer(collections_data)
    parser(final_data)

    print('MAIN: All parsing complete\n')

    # REPORT GREAT SUCCESS

    time_finish = time.perf_counter()
    time_t = time_finish - time_start

    print('MAIN: Execution complete, time taken', int(time_t), 'seconds')