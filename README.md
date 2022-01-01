# CatManga-dl
*Update*: RIP [CatManga](https://catmanga.org/), thanks for everything.
A python script that was originally written to download manga from [CatManga](https://catmanga.org/).

## Requirements
  * [Python 3.4+](https://www.python.org/downloads/)
  * bs4
  * requests_html

## Usage
* Download the catmanga-dl.py 
* Navigate to where the file is located
* Open the command line 
* Execute the following command :
```
For Windows : 
catmanga-dl.py [-c Chapters' Links] 
or
catmanga-dl.py [-t Title's Link]
```

```
For Linux & MacOs :
python3 catmanga-dl.py [-c Chapters' Links] 
or 
python3 catmanga-dl.py [-t Title's Link] 
```


### Example usage
```
...>catmanga-dl.py -t https://catmanga.org/series/ranger

            _                                               _ _
   ___ __ _| |_ _ __ ___   __ _ _ __   __ _  __ _        __| | |
  / __/ _` | __| '_ ` _ \ / _` | '_ \ / _` |/ _` |_____ / _` | |
 | (_| (_| | |_| | | | | | (_| | | | | (_| | (_| |_____| (_| | |
  \___\__,_|\__|_| |_| |_|\__,_|_| |_|\__, |\__,_|      \__,_|_|
                                      |___/

Manga : Ranger Reject
Available Chapters : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
Chapters you want to download : 1-5

status : [██████████████████████████████████████████████████] 100%
Downloaded : Ranger Reject Ch. 1 - [Black Cat Scanlations]

... (and so on)
```
