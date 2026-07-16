# SchoolWise — Django School Management System

## What's in this build
**Step 1 — Auth + Dashboard:** custom User model, login, sidebar/topbar shell, dashboard stat cards.

**Step 2 — Students, Attendance, Announcements, Fees:**
- **`students`** — Student Directory with search/filter, "Enroll Student" modal (Student Details + Parent Details), view/delete.
- **`attendance`** — Mark Attendance: pick a date, then **Section (Technical/Grammar)**, then **Class** — the Student List only appears once a class is chosen. Mark each student Present/Absent/Late, submit in bulk. Feeds the dashboard's "Today's Attendance %".
- **`core` (Announcements)** — full CRUD: create/edit/delete, target audience as real class tags + "All School", "Mark as Important" styling. Feeds the dashboard's "Recent Announcements".
- **`fees`** — Fee Structure Setup, Fee Collection (auto-computed Total/Paid/Balance/Status), Record Payment, printable Receipt, Payment History, Fee Defaulters page.

**Step 3 — Class Setup & Promotion (`academics`):**
- **Add New Class** — pick **Section** (Technical or Grammar) first; **Class Level** then only shows the matching options (Technical → TVEE Intermediate/Advanced Level, Grammar → GCE Ordinary/Advanced Level). "Section / Class Name" is a free text field for the actual class (Form 1, F1MM, A, ...).
- **Subjects & Teachers** — each class row shows its subject count; click it to open a modal listing that class's subjects, assign a new subject + teacher, or remove one.
- **Existing Classes** — edit or delete any class inline.
- **Bulk Promotion** — move every student from a source class to a destination class, or straight to **Alumni** (marks them `is_alumni=True`, clears their class, and removes them from the active Student Directory while keeping the record for history).

**Step 4 — Exams, Timetable, Staff:**
- **`exams`** — Create Exam (name, term, academic year, target classes), then **Enter Marks**: pick Class → Subject, a student grid appears with editable Score/Remarks per student, bulk-saved. Grades (A–F) and percentage are computed automatically.
- **`timetable`** — Pick a class to see its weekly grid (Mon–Fri × 8 periods). Click any slot to assign a Subject + Teacher (or clear it). Subjects offered are limited to that class's assigned subjects (from Class Setup).
- **`staff`** — Staff Directory listing all Teachers/Staff with search. **Add Staff** creates a `User` (inactive) + sends an invite email with a secure set-password link (uses Django's token generator, same mechanism as password reset). Accepting the invite activates the account. Resend invite for pending members; edit role/designation/phone inline; delete removes the account.
  - Dev note: invite emails print to the console (`EMAIL_BACKEND` is the console backend) — check your `runserver` terminal output for the link. Swap in a real backend for production.

Dashboard stat cards and Quick Action buttons are all wired to real data.

Still placeholders (next up): nothing major — Exams, Timetable, and Staff are now built. Possible next steps: exam report cards / class rank sheets, printable timetables, and staff permission scoping (e.g. teachers only seeing their own classes).

## Setup

```bash
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/accounts/login/ to sign in.
Visit http://127.0.0.1:8000/admin/ if you ever want to manage data directly.

## Project layout

```
schoolwise/        # project settings, root urls.py
accounts/          # custom User model, login/logout views, auth backend
core/              # dashboard, Announcement/Event models + full Announcements CRUD
academics/         # SchoolClass + Subject models, Class Setup & Promotion page
students/          # Student model, directory, enroll/view/delete
attendance/        # AttendanceRecord model, Mark Attendance page
fees/              # FeeStructure + Payment models, Fee Management, Receipts, Defaulters
exams/             # Exam + Mark models, Create Exam, Enter Marks grid
timetable/         # TimetableEntry model, weekly grid per class
staff/             # StaffProfile model, Staff Directory, invite/accept flow
templates/         # base.html (sidebar shell) + each app's templates
static/css/style.css
```

## Next modules
Core modules are now built. Natural follow-ups if you want to keep going:
1. **Exam report cards** — per-student summary across subjects/exams, class rank
2. **Printable timetable** — PDF/print-friendly view of a class's weekly grid
3. **Staff permissions** — restrict teacher logins to their own classes/subjects only

Say the word and we'll build the next one the same way: models → admin → views → templates,
verified end-to-end (login, submit real data, check it shows up correctly) before handing it over.
