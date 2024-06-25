import time

import selenium_v2 as bf

current_url = "https://e-postulat.ru/index.php/Postulat/issue/current"
releases_temp = list(bf.extract_releases(bf.get_page_source(current_url)))


def main():
    releases = list(bf.extract_releases(bf.get_page_source(current_url)))
    global releases_temp
    if len(releases_temp) == len(releases):
        return -1
    else:
        difference = list([item for item in releases if item not in releases_temp])
        releases_temp = list(releases)
        return difference



if __name__ == "__main__":
    while True:
        print(main())

        time.sleep(3600)


