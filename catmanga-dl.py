import sys, argparse, os, shutil, json, zipfile
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession

DESCRIPTION = '''Download chapters from catmanga.com'''

SIGNATURE = r'''                                           
            _                                               _ _ 
   ___ __ _| |_ _ __ ___   __ _ _ __   __ _  __ _        __| | |
  / __/ _` | __| '_ ` _ \ / _` | '_ \ / _` |/ _` |_____ / _` | |
 | (_| (_| | |_| | | | | | (_| | | | | (_| | (_| |_____| (_| | |
  \___\__,_|\__|_| |_| |_|\__,_|_| |_|\__, |\__,_|      \__,_|_|
                                      |___/                     
'''

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("-c", "--chapter", nargs='+', dest='chapters', help="chapters' link", required=False)
parser.add_argument("-t", "--title", nargs='?', dest='title', help="Title's link", required=False)

session = HTMLSession()
dictionary = {"+" : "", "!" : "", "?" : "", "%" : "", "*" : "", "/" : "", "#" : "", "\\": "", "&" : "and", ":" : "-",  '"' : ""}

def zipping(directory) :
    imgs = os.listdir(directory)
    with zipfile.ZipFile(directory+'.cbz', 'w') as targetfile :
        for img in imgs :
            targetfile.write(directory+'/'+img, img)

def statusBar(total,current):
    end = ''
    if total == current : end = '\n'
    width_of_bar = 50
    x = int((current / total)  * width_of_bar)
    printed_string = "".join([('█' if i < x else ' ') for i in range(width_of_bar)])
    out = "status : [" + printed_string + "] " + str(int((current / total) * 100)) + "%\r"
    print(f"{out}\r",end=end)

def chapterDownloader(link):
    res = session.get(link)
    res.html.render(timeout=10000)
    soup = bs(res.html.html, "html.parser")
    data = json.loads(soup.find("script", type="application/json").string)
    series_title = data["props"]["pageProps"]["series"]["title"]
    try : 
        chapters_title = data["props"]["pageProps"]["chapter"]["title"].translate(str.maketrans(dictionary))
    except :
        pass
    chapter_number = data["props"]["pageProps"]["key"]
    pages = data["props"]["pageProps"]["pages"]
    groups = '[' + " & ".join(data["props"]["pageProps"]["chapter"]["groups"]) + ']'

    try : 
        directory = f"Manga/{series_title}/{series_title} Ch. {chapter_number} - {chapters_title} {groups}"
    except : 
        directory = f"Manga/{series_title}/{series_title} Ch. {chapter_number} - {groups}"

    if not os.path.exists(directory):
        os.makedirs(directory)

    downloaded = 0
    for page in pages :
        image = page.split('/')[-1]
        with open(f"{directory}/{image}", "wb") as img:
            dt = session.get(page)
            img.write(dt.content)
        downloaded+=1    
        statusBar(len(pages),downloaded)
    zipping(directory)
    shutil.rmtree(directory)
    print(f"Downloaded : {series_title} Ch. {chapter_number} - {groups}")

def titleDownloader(link) :
    res = session.get(link)
    res.html.render(timeout=10000)
    soup = bs(res.html.html, "html.parser")
    data = json.loads(soup.find("script", type="application/json").string)
    available_chapters = [chapter["number"] for chapter in data["props"]["pageProps"]["series"]["chapters"]]

    print(available_chapters)
    
    requested_chapters = input("Chapters you want to download : ")
    while requested_chapters == '' :
        requested_chapters = input("Chapters you want to download : ")
    if requested_chapters == '*':
        requested_chapters = available_chapters
    elif '-' in requested_chapters:
        requested_chapters = requested_chapters.split('-')
        l = []
        for x in available_chapters:
            if float(requested_chapters[0]) <= float(x) and float(x) <= float(requested_chapters[1]) :
                l.append(x)
        requested_chapters = l
    else :
        l = requested_chapters.replace(' ','').split(',')
        requested_chapters = [i for i in available_chapters if str(i) in l]

    for i in requested_chapters :
        new_link = f"{link}/{i}"
        chapterDownloader(new_link)

if __name__ == "__main__" :
    print(SIGNATURE)
    args = parser.parse_args()
    if len(sys.argv) > 1 :
        if args.chapters :
            for index, chapter in enumerate(args.chapters):
                print(f"Downloading : {index+1}/{len(args.chapters)}")
                chapterDownloader(chapter)
        elif args.title :
            for title in args.title :
                titleDownloader(title)
    
    else : 
        parser.print_usage()
        parser.print_help()

