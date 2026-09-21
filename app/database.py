import os
from datetime import datetime
import sqlite3

def get_db_path() -> str:
    # قراءة المسار مع إزالة أي علامات اقتباس زائدة إن وُجدت في متغيرات البيئة
    path = os.environ.get("MASARDOC_DB_PATH", "/tmp/masardoc.db").strip("'\"")
    
    try:
        # استخراج المجلد الأب وإنشاؤه تلقائياً إذا لم يكن موجوداً
        db_dir = os.path.dirname(os.path.abspath(path))
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        return path
    except Exception as e:
        # مسار أمان بديل: إذا فشل إنشاء المسار المحدد (بسبب الصلاحيات مثلاً)، استخدم /tmp
        print(f"[Warning] Failed to use DB path '{path}': {e}. Falling back to /tmp/masardoc.db")
        os.makedirs("/tmp", exist_ok=True)
        return "/tmp/masardoc.db"
        
def get_db():
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        case_type TEXT NOT NULL,
        national_id TEXT,
        poa_number TEXT,
        poa_date TEXT,
        poa_expiry TEXT,
        current_stage TEXT NOT NULL DEFAULT 'Initial Review',
        target_office TEXT,
        status TEXT NOT NULL DEFAULT 'In Progress',
        notes TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        document_name TEXT NOT NULL,
        document_type TEXT NOT NULL,
        issuing_authority TEXT,
        is_verified INTEGER NOT NULL DEFAULT 0,
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (case_id) REFERENCES cases (id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS extracted_ledgers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_title TEXT NOT NULL,
        archive_location TEXT NOT NULL,
        ledger_type TEXT NOT NULL,
        ledger_number TEXT,
        page_number TEXT,
        registration_year TEXT,
        district_kesm TEXT,
        governorate TEXT,
        person_name TEXT NOT NULL,
        father_name TEXT,
        mother_name TEXT,
        event_date TEXT,
        official_stamps TEXT,
        confidence_score REAL NOT NULL,
        raw_text TEXT,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    
    # Prepopulate sample cases if table is empty
    cursor.execute("SELECT COUNT(*) FROM cases")
    if cursor.fetchone()[0] == 0:
        now = datetime.utcnow().isoformat()
        sample_cases = [
            (
                "مؤسسة النور للاستيراد والتصدير",
                "تعديل الشكل القانوني للشركة",
                "29607231201234",
                "توكيل رسمي عام قضايا 1422 لسنة 2024 توثيق الأهرام",
                "2024-04-10",
                "2027-04-10",
                "لجنة البت والتحول بهيئة الاستثمار",
                "الهيئة العامة للاستثمار والمناطق الحرة (GAFI)",
                "In Progress",
                "تم إيداع تقرير تقييم الحصص العينية من مكتب المحاسبة المعتمد، وجارٍ استصدار قرار التحول إلى شركة مساهمة.",
                now, now
            ),
            (
                "ورثة المرحوم فؤاد إبراهيم المحمودي",
                "بحث واستخراج قيود من دار المحفوظات بالقلعة",
                "28503150100456",
                "توكيل خاص بإعلام الوراثة 883 لسنة 2026 توثيق المنصورة",
                "2026-02-15",
                "2027-02-15",
                "البحث بالدفاتر الورقية (مواليد 1932)",
                "دار المحفوظات العمومية - القلعة",
                "In Progress",
                "تم تحديد الدفتر رقم 14 جيزة بحري لسنة 1932، في انتظار سداد رسوم الاستخراج المالي وختم شعار الجمهورية.",
                now, now
            ),
            (
                "د. كريم عثمان (مقيم بهولندا)",
                "تصديقات وزارة الخارجية والسفارة القبرصية",
                "29009110103321",
                "توكيل قنصلي مصدق من سفارة مصر بلاهاي 512/2026",
                "2026-06-01",
                "2027-06-01",
                "تصديق السفارة القبرصية بالقاهرة",
                "سفارة جمهورية قبرص - الزمالك",
                "Awaiting Appointment",
                "تم تصديق الشهادات الجامعية وسجل الوفاة من مكتب تصديقات الخارجية (أحمد عرابي)، ومتبقي موعد السفارة في أغسطس.",
                now, now
            )
        ]
        cursor.executemany("""
        INSERT INTO cases (
            client_name, case_type, national_id, poa_number, poa_date, poa_expiry,
            current_stage, target_office, status, notes, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_cases)
        conn.commit()

    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", get_db_path())
