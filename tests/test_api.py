import unittest
import os
import sys

# Add masardoc directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

TEST_DB_PATH = "/tmp/masardoc_test.db"
os.environ["MASARDOC_DB_PATH"] = TEST_DB_PATH

if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

from app.database import init_db
init_db()

from fastapi.testclient import TestClient
from app.main import app

class TestMasarDocAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except OSError:
                pass

    def test_health(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["app"], "MasarDoc")

    def test_procedures_list_and_detail(self):
        res = self.client.get("/api/procedures")
        self.assertEqual(res.status_code, 200)
        procs = res.json()
        self.assertGreaterEqual(len(procs), 3)

        # Check detail
        first_id = procs[0]["id"]
        detail_res = self.client.get(f"/api/procedures/{first_id}")
        self.assertEqual(detail_res.status_code, 200)
        detail = detail_res.json()
        self.assertEqual(detail["id"], first_id)
        self.assertIn("steps", detail)
        self.assertGreater(len(detail["steps"]), 0)

    def test_poa_template_generation(self):
        res = self.client.get("/api/procedures/dar-al-mahfouzat-search/poa-template?client_name=محمد_أحمد&attorney_name=مؤمن_رزق")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("محمد_أحمد", data["poa_clause"])
        self.assertIn("مؤمن_رزق", data["poa_clause"])

    def test_cases_crud(self):
        # 1. Create
        payload = {
            "client_name": "شركة الأمل للتوريدات",
            "case_type": "تعديل الشكل القانوني للشركة",
            "poa_number": "توكيل 112 لسنة 2026",
            "poa_expiry": "2027-12-31",
            "current_stage": "تقديم الملف بهيئة الاستثمار",
            "target_office": "الهيئة العامة للاستثمار",
            "status": "In Progress",
            "notes": "تم توقيع عقد التعديل المبدئي"
        }
        create_res = self.client.post("/api/cases", json=payload)
        self.assertEqual(create_res.status_code, 200)
        case_data = create_res.json()
        case_id = case_data["id"]
        self.assertEqual(case_data["client_name"], payload["client_name"])

        # 2. Read
        get_res = self.client.get(f"/api/cases/{case_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["current_stage"], "تقديم الملف بهيئة الاستثمار")

        # 3. Update
        update_res = self.client.put(f"/api/cases/{case_id}", json={
            "current_stage": "التأشير بالسجل التجاري",
            "status": "Completed"
        })
        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.json()["current_stage"], "التأشير بالسجل التجاري")
        self.assertEqual(update_res.json()["status"], "Completed")

        # 4. Delete
        del_res = self.client.delete(f"/api/cases/{case_id}")
        self.assertEqual(del_res.status_code, 200)

        # 5. Confirm 404
        get_after_del = self.client.get(f"/api/cases/{case_id}")
        self.assertEqual(get_after_del.status_code, 404)

    def test_ocr_extraction(self):
        text = """
        جمهورية مصر العربية - وزارة المالية
        مصلحة دار المحفوظات العمومية - قلعة صلاح الدين
        دفتر رقم: 12 صحيفة رقم: 45 لسنة: 1940 ميلادية
        محافظة: الدقهلية مركز: المنصورة
        اسم المولود: حسن عبد الله الشربيني
        اسم الوالد: عبد الله الشربيني
        اسم الوالدة: فاطمة السيد
        تاريخ الولادة: 5 مايو 1940
        ختم شعار الجمهورية
        """
        payload = {
            "document_title": "قيد ميلاد تجريبي",
            "raw_text": text
        }
        res = self.client.post("/api/ocr/extract", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["ledger_number"], "12")
        self.assertEqual(data["page_number"], "45")
        self.assertEqual(data["registration_year"], "1940")
        self.assertIn("حسن عبد الله الشربيني", data["person_name"])
        self.assertIn("الدقهلية", data["governorate"])
        self.assertIn("المنصورة", data["district_kesm"])
        self.assertGreater(data["confidence_score"], 0.7)

    def test_regulatory_updates(self):
        res = self.client.get("/api/regulatory")
        self.assertEqual(res.status_code, 200)
        updates = res.json()
        self.assertGreaterEqual(len(updates), 3)

        # Filter query
        search_res = self.client.get("/api/regulatory?query=الاستثمار")
        self.assertEqual(search_res.status_code, 200)
        filtered = search_res.json()
        self.assertGreaterEqual(len(filtered), 1)

if __name__ == "__main__":
    unittest.main()
