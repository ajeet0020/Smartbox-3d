# AI_USAGE.md

## 1. AI tools used
- Antigravity (Google DeepMind)

## 2. Prompts I gave
1. "go and check eitire thing what is baisically it will work and"
2. "what happend why is not movieng next" (when runserver started)
3. "curl -X GET http://127.0.0.1:8000/api/boxes/ ... see somthing wrong why is carshed"
4. "how i am test"
5. "and what is left"
6. "now what i am do tell me fast"
7. "i am know means what is happend inside the project but i dont know how to explain and how to check end to end my project"
8. "can't open file 'manage.py': [Errno 2] No such file or directory why happening this errror"
9. "now is this output is correct or not and what next"
10. Feedback on warehouse problem statement and learnings

## 3. Output I accepted
- Overall architecture: pure-Python `packing.py` decoupled from Django/DRF layer.
- 3D guillotine cut space decomposition heuristic and rotation check by sorting dimensions.
- Selection rule: cheapest box, tie-break by smaller volume.
- Sample data seeding script (`seed_sample_data.py`) to test live database records.

## 4. Output I rejected or modified
- Adjusted shell commands from standard Linux/bash (`source .venv/bin/activate`, `curl -X`) to Windows PowerShell equivalents (`.\.venv\Scripts\Activate.ps1`, `curl.exe`).

## 5. Mistakes / Issues encountered and resolved
1. Windows PowerShell alias issue: `curl` in PowerShell maps to `Invoke-WebRequest` which rejected `-X` (fixed by using `curl.exe`).
2. Directory navigation error: Running `manage.py` from outer repository root instead of the inner `boxselector/` project directory with `.venv` active.
3. Test mixed sizes volume constraint fix in test suite.

## 6. How I verified the final code
- Ran `python manage.py test -v 2`: all 25 tests passed cleanly in 0.16s.
- Created and executed `seed_sample_data.py` to populate boxes (Small, Medium, Large) and products (Mug, Book, Shoes).
- Performed manual end-to-end API tests via `curl.exe` and browser for single item fit, multi-item fit with long dimensions, and oversized items.
