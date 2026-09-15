from typing import List, Dict, Any

PROCEDURES_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "dar-al-mahfouzat-search",
        "title_ar": "استخراج القيود والمكلفات التاريخية من دار المحفوظات العمومية بالقلعة",
        "title_en": "Historical Civil Records & Land Registry Extraction (Citadel Archives)",
        "category": "الأرشيف والسجلات الرسمية",
        "target_authority": "مصلحة دار المحفوظات العمومية بالقاهرة (قلعة صلاح الدين)",
        "statutory_basis": "قانون المحفوظات العامة واللائحة التنظيمية لدفاتر القيود القديمة ومكلفات الأطيان والعقارات",
        "overview_ar": "الدليل الإجرائي الميداني لاستخراج شهادات الميلاد، الوفاة، الزواج، الطلاق، ومكلفات الأطيان من ا[...]",
        "overview_en": "End-to-end procedural guide for searching and retrieving pre-digital paper civil registers, birth/death records, and historical tax ledgers (Mokallafat) preserved at the Ci[...]",
        "recommended_poa_text": "يوكل في تمثيلي أمام مصلحة دار المحفوظات العمومية بقلعة صلاح الدين وفروعها، وله حق تقديم ط[...]",
        "steps": [
            {
                "step_number": 1,
                "title_ar": "التحضير المسبق وتحديد بيانات القيد",
                "title_en": "Data Scoping & Record Parameter Identification",
                "location": "مكتب المستشار القانوني / العميل",
                "department": "التوثيق المبدئي",
                "description_ar": "تجميع البيانات الأساسية: الاسم الرباعي، اسم الأم، المحافظة التاريخية، المركز أو القسم، [...]",
                "description_en": "Identify 4-part name, mother's name, historic governorate, district/kesm, sub-district (Sheiakha), and estimated event year (+/- 2 years).",
                "required_documents": [
                    "أصل بطاقة الرقم القومي للوكيل + صورة",
                    "أصل التوكيل الرسمي الخاص أو العام الموثق بالشهر العقاري",
                    "صورة أي مستند قرابة قديم (عقد ملكية، إعلام وراثة قديم، بطاقة ورقية قديمة إن وجدت)"
                ],
                "poa_requirements": "يجب أن ينص التوكيل صراحة على 'التعامل مع دار المحفوظات والاطلاع واستخراج القيود والمكل[...]",
                "estimated_duration": "يوم واحد",
                "official_fees": "بدون رسوم حكومية في هذه المرحلة",
                "critical_tips": [
                    "تأكد من معرفة التقسيم الإداري القديم للقرية أو الحي، حيث تغيرت تبعية عدة مراكز تاريخياً بين الج[...]"
                ]
            },
            {
                "step_number": 2,
                "title_ar": "شراء استمارة البحث وتقديم الطلب بصالة دار المحفوظات",
                "title_en": "Application Submission at Citadel Archives",
                "location": "دار المحفوظات العمومية - باب العزب - القلعة - القاهرة",
                "department": "صالة المواطنين وخزينة الاستمارات",
                "description_ar": "شراء الاستمارة المخصصة للبحث (طلب استخراج قيد ميلاد/وفاة أو مكلفة أطيان) من الخزينة، ومل[...]",
                "description_en": "Purchase search form at the Citadel Archives ticketing window, fill details, and submit to sorting clerk to map to archive ledger category.",
                "required_documents": [
                    "استمارة بحث دار المحفوظات مسددة الرسم",
                    "صورة بطاقة الوكيل وصورة التوكيل الساري",
                    "طابع شهيد + طابع تنمية موارد"
                ],
                "poa_requirements": "الاطلاع على أصل التوكيل وكارنيه المحاماة الساري للوكيل.",
                "estimated_duration": "يوم عمل واحد",
                "official_fees": "حوالي 60 إلى 120 جنيهاً مصرياً حسب نوع الاستمارة وعدد السنوات المطلوب كشفها",
                "critical_tips": [
                    "الوصول مبكراً في تمام الساعة 8:30 صباحاً، حيث تغلق الخزينة أبوابها مبكراً بحدود الواحدة ظهراً."
                ]
            },
            {
                "step_number": 3,
                "title_ar": "الفحص المكتبي والبحث اليدوي بالدفاتر الورقية (الأورنيك)",
                "title_en": "Manual Ledger Archive Search & Matching",
                "location": "دار المحفوظات - غرف الحفظ التاريخية",
                "department": "أقسام الدفاتر (مواليد بحري / مواليد قبلي / مكلفات زراعية)",
                "description_ar": "يقوم أمين الدفاتر بالبحث في المجلدات والقيود القديمة لاستخراج الأورنيك وتطابق رقم القي[...]",
                "description_en": "Archive keeper searches physical binding ledgers (Orneek) to locate matching page, volume number, and entry sequence.",
                "required_documents": [
                    "إيصال تسليم الطلب المحتوي على رقم المتابعة وتاريخ المراجعة"
                ],
                "poa_requirements": "لا يشترط حضور إضافي إلا في حال طلب الموظف مطابقة الاسم مع أصل التوكيل.",
                "estimated_duration": "من 5 إلى 10 أيام عمل",
                "official_fees": "مشمولة في رسم البحث المبدئي",
                "critical_tips": [
                    "في حال عدم العثور على القيد في السنة الأولى المحددة، يحق للباحث التمديد لسنة قبلها وسنة بعدها دو[...]"
                ]
            },
            {
                "step_number": 4,
                "title_ar": "تحرير المستخرج المعتمد وختم النسر",
                "title_en": "Issuance, Verification & Republic Seal Stamping",
                "location": "دار المحفوظات - مكتب المراجعة والختم",
                "department": "إدارة المراجعة وختم شعار الجمهورية",
                "description_ar": "تفريغ محتوى الدفتر التاريخي في شهادة رسمية بيضاء ممهورة ببيانات المجلد والصفحة، ومراجع[...]",
                "description_en": "Transcription of ledger data into verified certificate form, supervisor sign-off, and application of the official Republic Eagle Seal.",
                "required_documents": [
                    "إيصال استلام الطلب",
                    "أصل التوكيل وبطاقة الرقم القومي للاستلام"
                ],
                "poa_requirements": "التوقيع في دفتر الاستلامات باسم الوكيل ورقم توكيله.",
                "estimated_duration": "يوم عمل واحد (يوم الاستلام)",
                "official_fees": "رسم استخراج الشهادة الرسمية (حوالي 80 إلى 150 جنيهاً مصرياً)",
                "critical_tips": [
                    "افحص ختم النسر وتاريخ الإصدار وتطابق الحروف للاسم الرباعي فور الاستلام وقبل مغادرة المقر."
                ]
            }
        ]
    },
    {
        "id": "consular-mfa-legalization",
        "title_ar": "تصديقات المحررات الرسمية وتوثيق القنصليات والسفارات الأجنبية بمصر",
        "title_en": "MFA Authentication & Foreign Consular Legalization Pipeline",
        "category": "التوثيق والتصديقات القنصلية",
        "target_authority": "مكاتب تصديقات وزارة الخارجية المصرية + السفارات والقنصليات المعتمدة",
        "statutory_basis": "قانون السلك الدبلوماسي والقنصلي المصري وقواعد التصديقات الدولية المعمول بها",
        "overview_ar": "المسار القانوني الإلزامي لتصديق المستندات والشهادات الصادرة من الجهات المصرية (أحوال مدنية، [...]",
        "overview_en": "The mandatory legal sequence to authenticate and certify Egyptian civil, educational, commercial, and judicial documents for international legal validity abroad.",
        "recommended_poa_text": "يوكل في تمثيلي أمام كافة مكاتب تصديقات وزارة الخارجية بجمهورية مصر العربية، وأمام كافة ا[...]",
        "steps": [
            {
                "step_number": 1,
                "title_ar": "توثيق الجهة المصدرة للمستند (جهة المنشأ)",
                "title_en": "Origin Authority Certification",
                "location": "الجهة المصدرة المختصة (قطاع الأحوال المدنية بالعباسية / الإدارة المركزية للجامعات / وزارة ا[...]",
                "department": "إدارة التصديقات والمراجعة بالوزارة المعنية",
                "description_ar": "يجب أن يختم المستند أولاً من الإدارة العامة التابعة لها الجهة المصدرة (مثلاً: شهادات الم[...]",
                "description_en": "The original document must first bear the seal of its governing central authority (e.g. Civil Status Authority HQ, Supreme Council of Universities, Ministry of [...]",
                "required_documents": [
                    "أصل المستند المراد توثيقه حديث الإصدار",
                    "بطاقة الرقم القومي لطالب التوثيق"
                ],
                "poa_requirements": "توكيل ساري يتيح التعامل مع الجهة المصدرة.",
                "estimated_duration": "يوم عمل واحد",
                "official_fees": "من 25 إلى 100 جنيه حسب الجهة",
                "critical_tips": [
                    "تأكد من وضوح اسم وتوقيع الموظف المعتمد لدى وزارة الخارجية، حيث توجد نماذج توقيعات معتمدة مخزنة [...]"
                ]
            },
            {
                "step_number": 2,
                "title_ar": "تصديق مكتب وزارة الخارجية المصرية",
                "title_en": "Egyptian Ministry of Foreign Affairs (MFA) Authentication",
                "location": "أحد مكاتب تصديقات الخارجية (أحمد عرابي بالمهندسين / الميريلاند بمصر الجديدة / سان ستيفانو ب[...]",
                "department": "مكتب تصديقات المواطنين",
                "description_ar": "فحص المستند ومطابقة خاتم الجهة المصدرة بنموذج التوقيع المعتمد، ووضع طابع تصديقات وزارة[...]",
                "description_en": "Inspection of origin authority seal against specimen signatures, applying MFA stamp and official authentication seal.",
                "required_documents": [
                    "أصل المستند موثقاً من جهة المنشأ",
                    "بطاقة الوكيل وأصل التوكيل"
                ],
                "poa_requirements": "حق التصديق لدى وزارة الخارجية المصرية.",
                "estimated_duration": "نفس اليوم (في غضون ساعتين)",
                "official_fees": "110 جنيه مصري للمحررات العادية، و220 جنيهاً للمحررات التجارية",
                "critical_tips": [
                    "التأكد من دفع الرسوم عبر الدفع الإلكتروني (فيزا / ماستركارد / ميزة) حيث تم إلغاء التعامل النقدي ت[...]"
                ]
            },
            {
                "step_number": 3,
                "title_ar": "الترجمة المعتمدة الرسمية",
                "title_en": "Certified Sworn Translation",
                "location": "مكتب ترجمة معتمد من السفارة المستهدفة",
                "department": "الترجمة القانونية المعتمدة",
                "description_ar": "ترجمة المستند الموثق من الخارجية بالكامل (بما في ذلك الأختام والأرقام المسلسلة) عبر متر[...]",
                "description_en": "Complete translation of the document including MFA seals into target language by embassy-accredited sworn translator.",
                "required_documents": [
                    "أصل المستند بعد تصديق الخارجية المصرية"
                ],
                "poa_requirements": "لا يتطلب توكيل رسمي للترجمة.",
                "estimated_duration": "1 - 3 أيام عمل",
                "official_fees": "تختلف حسب اللغة وعدد الكلمات (حوالي 250 إلى 600 جنيه للصفحة)",
                "critical_tips": [
                    "راجع قائمة المكاتب المعتمدة المنشورة رسمياً على موقع السفارة (مثل سفارة قبرص، هولندا، ألمانيا) [...]"
                ]
            },
            {
                "step_number": 4,
                "title_ar": "حجز موعد وتقديم المعاملة بالسفارة الأجنبية أو مركز VFS",
                "title_en": "Embassy / VFS Global Consular Submission & Legalization",
                "location": "مقر السفارة الأجنبية بالقاهرة أو فرع VFS Global المعتمد",
                "department": "القسم القنصلي وشؤون التوثيق",
                "description_ar": "حجز موعد مسبق عبر المنظومة الإلكترونية، وإيداع الأصول والمترجمات وسداد الرسوم القنصلي[...]",
                "description_en": "Pre-book consular appointment, submit original authenticated documents and translations, pay consular fees, and collect legalized document.",
                "required_documents": [
                    "أصل المستندات المصدقة من الخارجية والمترجمة",
                    "إيصال حجز الموعد الإلكتروني المطبوع",
                    "أصل جواز السفر / بطاقة الوكيل وأصل التوكيل المعتمد"
                ],
                "poa_requirements": "توكيل خاص ينص صراحة على تمثيل العميل أمام السفارة المعنية أو قنصليتها.",
                "estimated_duration": "من يومين إلى 7 أيام عمل حسب السفارة",
                "official_fees": "تسدد باليورو أو ما يعادله بالجنيه المصري (غالباً من 30 إلى 75 يورو لكل مستند)",
                "critical_tips": [
                    "احرص على تطابق كتابة الأسماء اللاتينية حرفياً مع جواز سفر صاحب الشأن."
                ]
            }
        ]
    },
    {
        "id": "corporate-partnership-to-jsc",
        "title_ar": "تحويل وتعديل الشكل القانوني للشركة من تضامن إلى مساهمة (GAFI)",
        "title_en": "Corporate Restructuring: General Partnership to Joint-Stock Company (GAFI)",
        "category": "الاستثمار وتأسيس الشركات",
        "target_authority": "الهيئة العامة للاستثمار والمناطق الحرة (GAFI) + مصلحة السجل التجاري",
        "statutory_basis": "قانون الشركات رقم 159 لسنة 1981 وقانون الاستثمار رقم 72 لسنة 2017 ولائحته التنفيذية",
        "overview_ar": "المسار الإجرائي والقانوني الكامل لتعديل الشكل القانوني لشركة أشخاص (تضامن أو توصية بسيطة) وتح[...]",
        "overview_en": "Comprehensive statutory roadmap to convert an Egyptian partnership entity into a Joint Stock Company (JSC) or LLC via GAFI Investor Service Center.",
        "recommended_poa_text": "يوكل في تمثيلي أمام الهيئة العامة للاستثمار والمناطق الحرة، ومصلحة السجل التجاري، والغر[...]",
        "steps": [
            {
                "step_number": 1,
                "title_ar": "قرار جماعة الشركاء بالتحول وتعيين مراقب الحسابات",
                "title_en": "Partners' Resolution & Auditor Appointment",
                "location": "مقر الشركة / مكتب المحامي والتوثيق",
                "department": "إدارة الشؤون القانونية",
                "description_ar": "انعقاد جماعة الشركاء وصدور قرار بالإجماع على تعديل الشكل القانوني إلى شركة مساهمة، وتح[...]",
                "description_en": "Unanimous partners' resolution approving structural conversion, setting proposed share capital, and appointing a licensed auditor for net asset valuation.",
                "required_documents": [
                    "عقد الشركة الابتدائي وتعديلاته السابقة ومستخرج حديث من السجل التجاري",
                    "محضر اجتماع جماعة الشركاء موقع وموثق بالشهر العقاري",
                    "بطاقات الرقم القومي لكافة الشركاء"
                ],
                "poa_requirements": "توكيلات تأسيس وشركات تمنح الوكيل حق توقيع محاضر التعديل وتعديل العقود.",
                "estimated_duration": "3 - 5 أيام عمل",
                "official_fees": "رسوم توثيق المحضر بالشهر العقاري (حوالي 250 جنيهاً)",
                "critical_tips": [
                    "يشترط ألا يقل عدد مؤسسي الشركة المساهمة الناتجة عن 3 مساهمين، فإذا كان عدد الشركاء اثنين يجب إدخ[...]"
                ]
            },
            {
                "step_number": 2,
                "title_ar": "تقييم الحصص العينية وإعداد القوائم المالية",
                "title_en": "Asset Valuation & Balance Sheet Verification",
                "location": "مكتب محاسب قانوني معتمد + لجنة التحقق بهيئة الاستثمار",
                "department": "قطاع الأداء الاقتصادي بهيئة الاستثمار",
                "description_ar": "إعداد القوائم المالية وتقرير فحص المركز المالي للشركة القديمة معتمد من المحاسب القانون[...]",
                "description_en": "Preparation of audited financial statements and valuation report, submitted to GAFI Valuation Verification Committee.",
                "required_documents": [
                    "تقرير مراقب الحسابات متضمناً أصول وخصوم الشركة",
                    "القوائم المالية لآخر 3 سنوات أو منذ التأسيس إن كانت أقل",
                    "شهادة قيد مراقب الحسابات بسجل المحاسبين والمراجعين"
                ],
                "poa_requirements": "توكيل يتيح للوكيل أو المحاسب تمثيل الشركة أمام لجان هيئة الاستثمار.",
                "estimated_duration": "10 - 20 يوم عمل",
                "official_fees": "رسوم فحص تقييم الحصص بهيئة الاستثمار (حوالي 1000 إلى 2500 جنيه)",
                "critical_tips": [
                    "احرص على ألا تقل صافي حقوق الملكية المقيمة عن الحد الأدنى لرأس المال المصدر للشركة المساهمة (250 [...]"
                ]
            },
            {
                "step_number": 3,
                "title_ar": "اعتماد ملف التحول وإصدار قرار رئيس الهيئة",
                "title_en": "GAFI Approval & Ministerial Decree Issuance",
                "location": "مركز خدمات المستثمرين بالهيئة العامة للاستثمار (صلاح سالم أو الفروع)",
                "department": "إدارة تعديل الشركات والتحول",
                "description_ar": "إيداع نموذج عقد التأسيس والنظام الأساسي للشركة المساهمة، وسداد رسوم الهيئة ورسوم نقابة[...]",
                "description_en": "Submission of articles of association, payment of statutory fees and bar association stamp, and issuance of GAFI conversion decree.",
                "required_documents": [
                    "مشروع النظام الأساسي للشركة المساهمة",
                    "تقرير لجنة تقييم الحصص المعتمد",
                    "شهادة عدم التباس الاسم التجاري من مصلحة السجل التجاري"
                ],
                "poa_requirements": "توكيل تأسيس وتعديل شركات يتيح التوقيع أمام مأمور الشهر العقاري بالهيئة.",
                "estimated_duration": "5 - 8 أيام عمل",
                "official_fees": "رسوم نشر + رسوم توثيق ونقابة المحامين (تتحدد بنسبة مئوية من رأس المال، بحد أقصى قانوني)",
                "critical_tips": [
                    "إجراءات الشهر العقاري تتم داخل مكاتب الشهر العقاري النموذجية بمركز خدمات المستثمرين لتوفير ال[...]"
                ]
            },
            {
                "step_number": 4,
                "title_ar": "التأشير بالسجل التجاري وتعديل البطاقة الضريبية",
                "title_en": "Commercial Registry Amendment & Tax Card Update",
                "location": "مكتب السجل التجاري المميز بهيئة الاستثمار ومأمورية الضرائب",
                "department": "السجل التجاري والضرائب العامة",
                "description_ar": "التأشير في السجل التجاري بمحو القيد كشركة تضامن وإثبات القيد بالرقم الجديد كشركة مساهم[...]",
                "description_en": "Registering the new legal entity in the Commercial Registry, obtaining updated commercial extract, and modifying tax portal status.",
                "required_documents": [
                    "قرار هيئة الاستثمار بالتحول",
                    "عقد الشركة المعدل المشهر",
                    "أصل السجل التجاري القديم"
                ],
                "poa_requirements": "حق استلام مستخرجات السجل التجاري والتعامل مع الضرائب.",
                "estimated_duration": "يومان عمل",
                "official_fees": "رسوم الغرفة التجارية والسجل التجاري (حوالي 300 إلى 600 جنيه)",
                "critical_tips": [
                    "استخرج 5 مستخرجات رسمية حديثة من السجل التجاري الجديد لتقديمها للجهات المصرفية والتأمينات والج[...]"
                ]
            }
        ]
    },
    {
        "id": "national-id-first-time-foreign-born",
        "title_ar": "استخراج بطاقة الرقم القومي لأول مرة لمواليد الخارج (المملكة المتحدة والدول الأجنبية)",
        "title_en": "First-Time National ID Issuance for Egyptian Citizens Born Abroad (UK & Overseas)",
        "category": "الأحوال المدنية والأرشيف",
        "target_authority": "قطاع الأحوال المدنية (المراكز النموذجية بالقاهرة الجديدة / إدارة مواطني الخارج بالعباسية)",
        "statutory_basis": "قانون الأحوال المدنية رقم 143 لسنة 1994 وتعديلاته بالقانون رقم 140 لسنة 2022 والتعليمات المنظمة لس[...]",
        "overview_ar": "الدليل الإجرائي الميداني لاستخراج بطاقة الرقم القومي لأول مرة للمواطنين المصريين المولودين [...]",
        "overview_en": "Step-by-step procedural guide for Egyptian citizens born overseas (with automated Egyptian birth certificates) issuing their first National ID in Egypt, focusing on New Ca[...]",
        "recommended_poa_text": "يوكل في تمثيلي أمام قطاع مصلحة الأحوال المدنية وفروعها والمراكز النموذجية، وله حق سحب اس[...]",
        "steps": [
            {
                "step_number": 1,
                "title_ar": "تجهيز ملف المستندات الثبوتية والضامن العائلي",
                "title_en": "Document Compilation & Family Guarantor Verification",
                "location": "مكتب المستشار القانوني / محل الإقامة بالقاهرة الجديدة",
                "department": "الإعداد والتوثيق",
                "description_ar": "تجهيز أصل شهادة الميلاد المصرية المميكنة (الكمبيوتر) التي تحمل الرقم القومي المكون من 14 [...]",
                "description_en": "Gather original automated Egyptian birth certificate (with 14-digit national ID), valid British passport, proof of residence in Egypt (utility bill or registere[...]",
                "required_documents": [
                    "أصل شهادة الميلاد المصرية المميكنة الصادرة من مصلحة الأحوال المدنية",
                    "أصل وصورة جواز السفر البريطاني الساري (لإثبات تاريخ الدخول والهوية الشخصية)",
                    "أصل بطاقة الرقم القومي السارية للضامن (أحد الوالدين أو قريب درجة أولى)",
                    "مستند إثبات محل الإقامة (إيصال مرافق حديث كهرباء/غاز/مياه، أو عقد إيجار موثق بالشهر العقاري بال[...]",
                    "مستند إثبات المؤهل الدراسي أو جهة العمل (مصدق من الخارجية المصرية إذا كان صادراً من بريطانيا)"
                ],
                "poa_requirements": "استخراج البطاقة لأول مرة يلزم الحضور الشخصي لصاحب الشأن لالتقاط البصمة والصورة البيوم[...]",
                "estimated_duration": "يوم واحد",
                "official_fees": "بدون رسوم مسبقة",
                "critical_tips": [
                    "الضامن من الدرجة الأولى إلزامي قانوناً في استخراج بطاقة أول مرة ليوقع ويقر بالصلة أمام موظف الس[...]",
                    "إذا كانت الشهادة الدراسية بريطانية ولم تعادل أو تصدق بعد من الخارجية المصرية، تدون المهنة في ال[...]"
                ]
            },
            {
                "step_number": 2,
                "title_ar": "اختيار مقر التقديم بالقاهرة الجديدة وشراء الاستمارة",
                "title_en": "Application Form Purchase & Venue Selection in New Cairo",
                "location": "المراكز النموذجية بالقاهرة الجديدة (مكسيم مول بالتجمع الخامس، سيتي سنتر ألماظة، أو سيتي ست[...]",
                "department": "صالة الخدمات المركزية للأحوال المدنية بالمول",
                "description_ar": "التوجه إلى أحد المراكز النموذجية المميكنة بالأحوال المدنية القريبة من القاهرة الجديدة.[...]",
                "description_en": "Visit a civil status VIP center in New Cairo (Maxim Mall North 90th, City Centre Almaza, or City Stars) and select the desired processing tier.",
                "required_documents": [
                    "ملف المستندات المحضر بالخطوة 1",
                    "استمارة الرقم القومي المشتراة من الخزينة"
                ],
                "poa_requirements": "حضور صاحب الشأن إلزامي للتصوير.",
                "estimated_duration": "ساعة إلى ساعتين عمل",
                "official_fees": "فئات الاستمارة: الفئة العادية 50 ج.م (15 يوماً) | العاجلة 125 ج.م (3 أيام) | الخاصة 175 ج.م (24 ساعة) | [...]",
                "critical_tips": [
                    "المراكز النموذجية بالمولات تعمل فترات مسائية حتى الساعة 8-9 مساءً وتعمل أيام العطلات والجمعة، و[...]"
                ]
            },
            {
                "step_number": 3,
                "title_ar": "استيفاء البيانات وتوقيع الضامن أمام الموثق المختص",
                "title_en": "Form Endorsement & Guarantor In-Person Attestation",
                "location": "شباك المراجعة بالسجل المدني / المركز النموذجي",
                "department": "مكتب مراجعة قيود أول مرة ومواليد الخارج",
                "description_ar": "تفريغ البيانات في الاستمارة: الاسم الرباعي، اسم الأم، تاريخ ومحل الميلاد، الرقم القومي[...]",
                "description_en": "Fill personal details exactly matching the automated birth certificate. The first-degree guarantor signs the endorsement box in front of the officer.",
                "required_documents": [
                    "استمارة الرقم القومي مستوفاة",
                    "أصل بطاقة الضامن + صورة ضوئية",
                    "إيصال سداد رسوم الاستمارة"
                ],
                "poa_requirements": "إقرار الضامن شخصي ولا يجوز بالتوكيل.",
                "estimated_duration": "30 دقيقة",
                "official_fees": "مشمولة في قيمة الاستمارة",
                "critical_tips": [
                    "تأكد من كتابة الاسم باللغة العربية مطابقاً تماماً لحروف شهادة الميلاد المصرية المميكنة دون أي [...]"
                ]
            },
            {
                "step_number": 4,
                "title_ar": "الالتقاط البيومتري (البصمة والصورة) واستلام البطاقة",
                "title_en": "Biometric Capture, Photo & ID Card Handover",
                "location": "غرفة التصوير الرقمي بالسجل المدني",
                "department": "وحدة الالتقاط الرقمي وخزينة التسليم",
                "description_ar": "التقاط البصمات العشرية إلكترونياً والصورة الشخصية الرقمية واستلام إيصال استلام البطاق[...]",
                "description_en": "Digital live capture of facial photo and fingerprints. Collect tracking receipt for pickup (or same-day immediate issuance in VIP tiers).",
                "required_documents": [
                    "إيصال التقديم المالي ومطابقة الوثائق",
                    "أصل جواز السفر البريطاني أو بطاقة الضامن للاستلام"
                ],
                "poa_requirements": "يجوز استلام البطاقة للضامن المقيد بالاستمارة أو صاحب الشأن بنفسه.",
                "estimated_duration": "من 30 دقيقة (VIP) إلى 3-15 يوماً (عادية)",
                "official_fees": "لا توجد رسوم إضافية",
                "critical_tips": [
                    "احتفظ بالإيصال الورقي المختوم، وتأكد فور استلام البطاقة من صحة الرقم القومي ومحل الإقامة والمه[...]"
                ]
            }
        ]
    }
]


def get_all_procedures():
    """Retrieve all procedures from the database."""
    return PROCEDURES_DATABASE


def get_procedure_by_id(proc_id: str):
    """Retrieve a specific procedure by its ID."""
    for proc in PROCEDURES_DATABASE:
        if proc["id"] == proc_id:
            return proc
    return None
