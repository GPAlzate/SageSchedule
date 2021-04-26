# CSCI181: Final Project
## Gabe Alzate, Samuel So

Project Outline

1. Gather course information from 2021-2022 course catalog.
    - reach out to registrar for dependencies
    - if not, either i) hard-code information, ii) scrape from course-catalog using NLP techniques (e.g., regex search "pre-requisite")

2. Map out "front-end"
    - Map out user interactions  

Semester-to-semester course schedule
1.  add/remove courses
2.  checkbox of requirements (fulfilled as courses are added)
    - foreign language
    - pe
    - breadth (areas 1-6)
    - overlays (speaking, writing, analyzing difference)
    - ID1
3. customizable number of units
4. valid schedule? (dependencies (pre-reqs), and if current schedule, timing)

TO DO NEXT
1. Search function 
    a. "fuzzier" functionality
    b. based on course description
    c. 
2. Add to schedule
3. Course list: put area/breadth requirements concisely

Things to run:

```
flask run
pnpm run tw:build
```