import xkcd


def get_comic():
    comic_num = int(xkcd.getRandomComic().link.replace(
        "https://www.xkcd.com/", "").strip())
    comic_img_url = xkcd.Comic(comic_num).getImageLink()
    return comic_img_url


if __name__ == "__main__":
    print(get_comic())
