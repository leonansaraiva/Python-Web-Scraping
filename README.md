# Data Pirates challenge

Welcome to Data Pirates challenge.


## Scenario:

The Internet Movie Database (IMDb) is an online database of information about music, movies, TV shows and games and television games computer. [Wikipedia]. This challenge consist to collect information from this site and deliver it  in other format.


## Requirements:

 * Get 500 titles from each genre
 * Sorted by 'Rating'
 * This app must run with only one command
 * The output format is JSONL
 * Write each genre in one output file

# Data Pirates Solution

The solution to the problem was made using Python programming language
## Configuration:
* Python 3.6.5
* Windows 10 (64 bits)
* RAM 8 GB 

## Dependencies:

Is necessary to install the libraries:
* BeautifulSoup
* requests
* pandas

## To run it:
To run it is necessary to access the destination folder by the console and run the command:

    $ python dataPirates
   
## Results:

The program was configured to make the requisitions to the server initing by 2000 antil 2018. For each year 30 pages were requested during time 30 minutes. 26 genre were found, with this frequency the number of 500 titles per genre was not reached. The files are save on the paste "files" splits by genre.
 * Output
[('Drama', 10265), ('Comedy', 7171), ('Action', 4167), ('Crime', 3043), ('Romance', 3029), ('Thriller', 2851), ('Adventure', 2426), ('Horror', 2253), ('Mystery', 1561), ('Animation', 1408), ('Documentary', 1314), ('Fantasy', 1204), ('Sci-Fi', 1179), ('Family', 1030), ('Biography', 1012), ('Music', 852), ('History', 665), ('Short', 418), ('War', 406), ('Sport', 405), ('Musical', 226), ('Reality-TV', 202), ('Western', 84), ('Talk-Show', 68), ('Game-Show', 67), ('News', 43)] 

References:
http://www.imdb.com/
http://jsonlines.org
