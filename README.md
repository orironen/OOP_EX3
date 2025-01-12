# מערכת ספרייה

## התקנה והפעלה
כדי להפעיל את המערכת:
```cmd
python main.py
```

## תיאור המערכת
מערכת לניהול ספרייה המאפשרת:
- הוספה והסרה של ספרים
- השאלה והחזרה של ספרים
- חיפוש ספרים לפי כותר, מחבר, ז'אנר ושנה
- צפייה במלאי הספרים
- מעקב אחר ספרים מושאלים
- ניהול רשימות המתנה
- התראות למשתמשים

## תבניות עיצוב (Design Patterns)

### Iterator Pattern
מימוש ב-`database/iterators.py`:
- `BookIterator` - מאפשר מעבר על רשימת הספרים
- `UserIterator` - מאפשר מעבר על רשימת המשתמשים

### Decorator Pattern
מימוש ב-`database/strategies.py`:
- `BooklistDecorator` - מאפשר הוספת פונקציונליות למנגנון החיפוש והתצוגה
- `PopularDecorator` - מסדר לפי פופולריות
- `AlphabeticalDecorator` - מסדר לפי סדר אלפביתי
- `GenreDecorator` - מסדר לפי ז'אנר

### Strategy Pattern
מימוש ב-`database/strategies.py`:
- `SearchByTitle` - חיפוש לפי כותר
- `SearchByAuthor` - חיפוש לפי מחבר
- `SearchByGenre` - חיפוש לפי ז'אנר
- `SearchByYear` - חיפוש לפי שנה

### Observer Pattern
מימוש ב-`database/library.py` ו-`Users/user.py`:
- `Library` כ-Subject
- `User` כ-Observer
- מאפשר שליחת התראות למשתמשים על שינויים במערכת