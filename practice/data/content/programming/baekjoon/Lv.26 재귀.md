
```dataview
TABLE
title AS "제목",
level AS "난이도",
tier AS "티어",
accepted_user_count AS "해결수",
average_tries AS "평균시도"
FROM "practice/data/content/programming/baekjoon/scraped"
WHERE contains(tags, "재귀")
AND !contains(tags, "인터랙티브")
AND !contains(tags, "함수 구현")
AND official = true
AND is_solvable = true
AND tier != "Unrated"
AND level < 16
SORT level ASC, accepted_user_count DESC
```




	

