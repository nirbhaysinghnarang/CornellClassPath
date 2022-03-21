# CornellClassPath

## Problem Statement.
* Input: Array of course numbers, home base location.
* Output: weekly transport schedule.

## Working
1. For each course number, first validate it. That is, check the course exists in the class roster. (web scraping)

2. Then, grab its weekly schedule. Parse it. (will be of the format <day(s) time>, where <days> is of the format <MWF>, <TR> or <D>), where D is in (M,T,W,R,F))

3. For each day, grab transport times using GMaps API. This means that, on each day, the starting point and ending point will be the same. (home base location) Then, from the home base you go to class 1 and from class 1 to class 2, and so on for *n* classes. After the *n-th* class, you go back to the homebase.
