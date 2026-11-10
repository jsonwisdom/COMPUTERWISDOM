(* BLACKBARPRESS Minnesota Root-to-Roof arithmetic check
   Source: https://mn.gov/deed/newscenter/press-releases/?id=1045-772342
   Public announcement, October 21, 2026. Not proof of actual payment or jobs.
*)
ClearAll[announcedAwards, itemizedJobs, expectedHeadlineJobs, minRyderJobs, checks];
announcedAwards = {175000, 175000, 140000, 800000, 600000, 175000};
itemizedJobs = {14, 15, 7, 75};
expectedHeadlineJobs = 141;
minRyderJobs = 31; (* Source text says "over 30" *)
checks = <|
  "awardsSumTo2065000" -> (Total[announcedAwards] === 2065000),
  "fourExactJobCountsSum111" -> (Total[itemizedJobs] === 111),
  "minimumItemizedJobs142" -> (Total[itemizedJobs] + minRyderJobs === 142),
  "literalMinimumExceedsHeadline141" -> (Total[itemizedJobs] + minRyderJobs > expectedHeadlineJobs),
  "headlineConsistentWithAtMost30Ryder" -> (Total[itemizedJobs] + 30 === expectedHeadlineJobs)
|>;
<|"sourceDate" -> "2026-10-21", "checks" -> checks,
 "allChecksPass" -> And @@ Values[checks],
 "warning" -> "One minor source-text inconsistency; does not indicate actual payment, missing jobs, or wrongdoing."|>
