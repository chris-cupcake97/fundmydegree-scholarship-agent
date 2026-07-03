# Verdict Policy

Never return `eligible` unless all are true:

1. `source_url` exists.
2. Source is official.
3. Page appears current or cycle is known.
4. Nationality/country rule does not block the student.
5. Residence rule does not block the student.
6. Fee-status rule does not block the student.
7. Degree level matches.
8. Field/program rules match.
9. Funding amount does not contradict minimum funding need.
10. Deadline is open or clearly current.
11. Required application process is clear.
12. Every required claim has evidence.

Return `not_eligible` if an official source contains a blocking rule.

Return `unclear` if official evidence is incomplete, vague, unclear, or contradictory.

Return `unverified` if no acceptable official source exists.
