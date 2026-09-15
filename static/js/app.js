document.addEventListener('DOMContentLoaded', () => {
    // --- State ---
    let proceduresData = [];
    let casesData = [];
    let ocrSamplesData = [];
    let regulatoryData = [];

    // --- Tab Switching ---
    const tabItems = document.querySelectorAll('.tab-item');
    const tabContents = document.querySelectorAll('.tab-content');

    tabItems.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.getAttribute('data-tab');
            tabItems.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const activeContent = document.getElementById(target);
            if (activeContent) {
                activeContent.classList.add('active');
            }
        });
    });

    // --- Procedures Module ---
    const proceduresListEl = document.getElementById('procedures-list');
    const procDetailViewEl = document.getElementById('procedure-detail-view');
    const backToProcsBtn = document.getElementById('back-to-procedures-btn');
    const poaProcedureSelect = document.getElementById('poa-procedure-select');

    async function loadProcedures() {
        try {
            const res = await fetch('/api/procedures');
            proceduresData = await res.json();
            renderProceduresGrid(proceduresData);
            populatePoaProcedureSelect(proceduresData);
        } catch (err) {
            console.error('Error loading procedures:', err);
        }
    }

    function renderProceduresGrid(procs) {
        proceduresListEl.innerHTML = '';
        procs.forEach(p => {
            const card = document.createElement('div');
            card.className = 'proc-card';
            card.innerHTML = `
                <div>
                    <span class="category-tag">${p.category}</span>
                    <h3>${p.title_ar}</h3>
                    <p>${p.overview_ar}</p>
                </div>
                <div class="proc-card-footer">
                    <span>${p.steps ? p.steps.length : 0} مراحل تنفيذية</span>
                    <span>عرض التفاصيل والخطوات ←</span>
                </div>
            `;
            card.addEventListener('click', () => showProcedureDetail(p));
            proceduresListEl.appendChild(card);
        });
    }

    function showProcedureDetail(p) {
        proceduresListEl.style.display = 'none';
        procDetailViewEl.style.display = 'block';

        document.getElementById('proc-category').textContent = p.category;
        document.getElementById('proc-title').textContent = p.title_ar;
        document.getElementById('proc-overview').textContent = p.overview_ar;
        document.getElementById('proc-authority').textContent = p.target_authority;
        document.getElementById('proc-law').textContent = p.statutory_basis;
        document.getElementById('proc-poa-text').textContent = p.recommended_poa_text;

        const timelineEl = document.getElementById('proc-steps-timeline');
        timelineEl.innerHTML = '';

        p.steps.forEach(s => {
            const stepEl = document.createElement('div');
            stepEl.className = 'step-box';
            
            const docsList = s.required_documents.map(d => `<li>${d}</li>`).join('');
            const tips = s.critical_tips.map(t => `<div class="step-tips-box">💡 <strong>تنبيه ميداني:</strong> ${t}</div>`).join('');

            stepEl.innerHTML = `
                <div class="step-header">
                    <div>
                        <span class="step-number-tag">المرحلة ${s.step_number}</span>
                        <span class="step-title">${s.title_ar}</span>
                    </div>
                    <span class="badge badge-law">${s.location} (${s.department})</span>
                </div>
                <p class="step-desc">${s.description_ar}</p>
                
                <div class="step-meta">
                    <strong>المدة المقدرة:</strong> ${s.estimated_duration} | 
                    <strong>الرسوم الرسمية:</strong> ${s.official_fees}
                </div>

                <div style="margin-bottom: 8px;">
                    <strong style="font-size: 13px;">المستندات المطلوبة:</strong>
                    <ul class="step-docs-list">${docsList}</ul>
                </div>

                ${tips}
            `;
            timelineEl.appendChild(stepEl);
        });
    }

    backToProcsBtn.addEventListener('click', () => {
        procDetailViewEl.style.display = 'none';
        proceduresListEl.style.display = 'grid';
    });

    document.getElementById('copy-poa-btn').addEventListener('click', () => {
        const text = document.getElementById('proc-poa-text').textContent;
        navigator.clipboard.writeText(text);
        alert('تم نسخ صيغة التوكيل للحافظة بنجاح!');
    });

    // --- Cases Module ---
    const casesContainerEl = document.getElementById('cases-container');
    const openNewCaseModalBtn = document.getElementById('open-new-case-modal');
    const newCaseFormCard = document.getElementById('new-case-form-card');
    const cancelCaseBtn = document.getElementById('cancel-case-btn');
    const createCaseForm = document.getElementById('create-case-form');

    async function loadCases() {
        try {
            const res = await fetch('/api/cases');
            casesData = await res.json();
            renderCases(casesData);
        } catch (err) {
            console.error('Error loading cases:', err);
        }
    }

    function renderCases(cases) {
        casesContainerEl.innerHTML = '';
        if (cases.length === 0) {
            casesContainerEl.innerHTML = '<div class="empty-state">لا توجد معاملات مسجلة حالياً.</div>';
            return;
        }

        cases.forEach(c => {
            const card = document.createElement('div');
            card.className = 'case-card';

            let statusClass = 'status-in-progress';
            let statusText = 'قيد التنفيذ الميداني';
            if (c.status === 'Completed') {
                statusClass = 'status-completed';
                statusText = 'مكتملة ومستلمة';
            } else if (c.status === 'Awaiting Appointment') {
                statusClass = 'status-awaiting-appointment';
                statusText = 'في انتظار الموعد القنصلي';
            }

            card.innerHTML = `
                <div>
                    <div class="case-card-header">
                        <span class="case-client-title">${c.client_name}</span>
                        <span class="case-status-badge ${statusClass}">${statusText}</span>
                    </div>
                    <div class="case-detail-item"><strong>نوع المعاملة:</strong> ${c.case_type}</div>
                    <div class="case-detail-item"><strong>المرحلة الحالية:</strong> ${c.current_stage}</div>
                    <div class="case-detail-item"><strong>الجهة المستهدفة:</strong> ${c.target_office || 'غير محدد'}</div>
                    <div class="case-detail-item"><strong>بيانات التوكيل:</strong> ${c.poa_number || 'بدون توكيل مسجل'}</div>
                    ${c.poa_expiry ? `<div class="case-detail-item"><strong>صلاحية التوكيل حتى:</strong> ${c.poa_expiry}</div>` : ''}
                    ${c.notes ? `<div class="case-notes-box">${c.notes}</div>` : ''}
                </div>
                <div class="case-actions">
                    <button class="btn btn-sm btn-outline advance-btn">تحديث المرحلة</button>
                    ${c.status !== 'Completed' ? '<button class="btn btn-sm btn-secondary complete-btn">إتمام المعاملة</button>' : ''}
                    <button class="btn btn-sm btn-outline delete-btn" style="color: #e53e3e; border-color: #feb2b2;">حذف</button>
                </div>
            `;

            // Action listeners
            card.querySelector('.advance-btn').addEventListener('click', async () => {
                const nextStage = prompt('أدخل اسم المرحلة الجديدة للمعاملة:', c.current_stage);
                if (nextStage && nextStage !== c.current_stage) {
                    await updateCaseField(c.id, { current_stage: nextStage });
                }
            });

            const compBtn = card.querySelector('.complete-btn');
            if (compBtn) {
                compBtn.addEventListener('click', async () => {
                    if (confirm('هل تم استلام كافة المستخرجات الرسمية وإنهاء المعاملة؟')) {
                        await updateCaseField(c.id, { status: 'Completed', current_stage: 'تم إنهاء الإجراء بنجاح' });
                    }
                });
            }

            card.querySelector('.delete-btn').addEventListener('click', async () => {
                if (confirm('هل أنت متأكد من حذف هذا الملف؟')) {
                    await deleteCase(c.id);
                }
            });

            casesContainerEl.appendChild(card);
        });
    }

    openNewCaseModalBtn.addEventListener('click', () => {
        newCaseFormCard.style.display = 'block';
        openNewCaseModalBtn.style.display = 'none';
    });

    cancelCaseBtn.addEventListener('click', () => {
        newCaseFormCard.style.display = 'none';
        openNewCaseModalBtn.style.display = 'inline-flex';
    });

    createCaseForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            client_name: document.getElementById('case-client-name').value,
            case_type: document.getElementById('case-type').value,
            poa_number: document.getElementById('case-poa-number').value || null,
            poa_expiry: document.getElementById('case-poa-expiry').value || null,
            current_stage: document.getElementById('case-current-stage').value || 'البدء في تجهيز المستندات',
            target_office: 'الجهة الإدارية المختصة',
            status: 'In Progress',
            notes: document.getElementById('case-notes').value || null
        };

        try {
            const res = await fetch('/api/cases', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                createCaseForm.reset();
                newCaseFormCard.style.display = 'none';
                openNewCaseModalBtn.style.display = 'inline-flex';
                loadCases();
            }
        } catch (err) {
            console.error('Error creating case:', err);
        }
    });

    async function updateCaseField(caseId, updates) {
        try {
            const res = await fetch(`/api/cases/${caseId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updates)
            });
            if (res.ok) {
                loadCases();
            }
        } catch (err) {
            console.error('Error updating case:', err);
        }
    }

    async function deleteCase(caseId) {
        try {
            const res = await fetch(`/api/cases/${caseId}`, { method: 'DELETE' });
            if (res.ok) {
                loadCases();
            }
        } catch (err) {
            console.error('Error deleting case:', err);
        }
    }

    // --- Historical OCR & Ledger Parser ---
    const ocrSamplesSelect = document.getElementById('ocr-samples-select');
    const ocrRawTextarea = document.getElementById('ocr-raw-text');
    const ocrDocTitleInput = document.getElementById('ocr-doc-title');
    const runOcrBtn = document.getElementById('run-ocr-btn');
    const ocrPlaceholderEl = document.getElementById('ocr-placeholder');
    const ocrExtractedViewEl = document.getElementById('ocr-extracted-view');

    async function loadOcrSamples() {
        try {
            const res = await fetch('/api/ocr/samples');
            ocrSamplesData = await res.json();
            ocrSamplesData.forEach((s, idx) => {
                const opt = document.createElement('option');
                opt.value = idx;
                opt.textContent = s.title;
                ocrSamplesSelect.appendChild(opt);
            });
        } catch (err) {
            console.error('Error loading samples:', err);
        }
    }

    ocrSamplesSelect.addEventListener('change', () => {
        const selectedIdx = ocrSamplesSelect.value;
        if (selectedIdx !== '') {
            const sample = ocrSamplesData[selectedIdx];
            ocrDocTitleInput.value = sample.title;
            ocrRawTextarea.value = sample.sample_text.trim();
        }
    });

    runOcrBtn.addEventListener('click', async () => {
        const text = ocrRawTextarea.value.trim();
        if (!text) {
            alert('يرجى إدخال أو لصق نص الوثيقة المراد فحصها واستخراج بياناتها.');
            return;
        }

        runOcrBtn.disabled = true;
        runOcrBtn.textContent = 'جاري الفحص والاستخراج...';

        try {
            const res = await fetch('/api/ocr/extract', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    document_title: ocrDocTitleInput.value,
                    raw_text: text
                })
            });

            if (res.ok) {
                const data = await res.json();
                displayOcrResults(data);
            } else {
                alert('حدث خطأ أثناء فحص الوثيقة');
            }
        } catch (err) {
            console.error('OCR Error:', err);
        } finally {
            runOcrBtn.disabled = false;
            runOcrBtn.textContent = '⚡ تشغيل الفحص واستخراج البيانات المهيكلة';
        }
    });

    function displayOcrResults(data) {
        ocrPlaceholderEl.style.display = 'none';
        ocrExtractedViewEl.style.display = 'block';

        document.getElementById('res-confidence').textContent = `${Math.round(data.confidence_score * 100)}%`;
        document.getElementById('res-archive-loc').textContent = data.archive_location;
        document.getElementById('res-ledger-type').textContent = data.ledger_type;
        document.getElementById('res-person-name').textContent = data.person_name;
        document.getElementById('res-father-name').textContent = data.father_name || 'غير متوفر بالوثيقة';
        document.getElementById('res-mother-name').textContent = data.mother_name || 'غير متوفر بالوثيقة';
        document.getElementById('res-ledger-page').textContent = `دفتر رقم ${data.ledger_number || '-'} | صحيفة رقم ${data.page_number || '-'}`;
        document.getElementById('res-year').textContent = data.registration_year || 'غير محدد';
        document.getElementById('res-location').textContent = `${data.governorate || ''} ${data.district_kesm ? '- ' + data.district_kesm : ''}`;
        document.getElementById('res-event-date').textContent = data.event_date || 'غير محدد بدقة';
        document.getElementById('res-stamps').textContent = data.official_stamps;
    }

    // --- Smart POA Clause Drafter ---
    const poaClientInput = document.getElementById('poa-client-input');
    const poaAttorneyInput = document.getElementById('poa-attorney-input');
    const generatePoaBtn = document.getElementById('generate-poa-btn');
    const poaOutputTextarea = document.getElementById('poa-output-textarea');
    const copyFullPoaBtn = document.getElementById('copy-full-poa-btn');

    function populatePoaProcedureSelect(procs) {
        poaProcedureSelect.innerHTML = '';
        procs.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p.id;
            opt.textContent = p.title_ar;
            poaProcedureSelect.appendChild(opt);
        });
        generatePoaClause();
    }

    async function generatePoaClause() {
        const procId = poaProcedureSelect.value;
        const client = poaClientInput.value.trim() || 'فؤاد إبراهيم المحمودي';
        const attorney = poaAttorneyInput.value.trim() || 'الأستاذ مؤمن محسن رزق الله - المحامي';

        if (!procId) return;

        try {
            const res = await fetch(`/api/procedures/${procId}/poa-template?client_name=${encodeURIComponent(client)}&attorney_name=${encodeURIComponent(attorney)}`);
            const data = await res.json();
            poaOutputTextarea.value = data.poa_clause;
        } catch (err) {
            console.error('Error generating POA:', err);
        }
    }

    generatePoaBtn.addEventListener('click', generatePoaClause);
    poaProcedureSelect.addEventListener('change', generatePoaClause);

    copyFullPoaBtn.addEventListener('click', () => {
        poaOutputTextarea.select();
        navigator.clipboard.writeText(poaOutputTextarea.value);
        alert('تم نسخ صيغة التوكيل الرسمية بالكامل للحافظة بنجاح!');
    });

    // --- Regulatory Radar Module ---
    const regulatoryContainerEl = document.getElementById('regulatory-feed-container');
    const regSearchInput = document.getElementById('reg-search-input');

    async function loadRegulatoryUpdates(query = '') {
        try {
            let url = '/api/regulatory';
            if (query) {
                url += `?query=${encodeURIComponent(query)}`;
            }
            const res = await fetch(url);
            regulatoryData = await res.json();
            renderRegulatoryFeed(regulatoryData);
        } catch (err) {
            console.error('Error loading regulatory feed:', err);
        }
    }

    function renderRegulatoryFeed(updates) {
        regulatoryContainerEl.innerHTML = '';
        if (updates.length === 0) {
            regulatoryContainerEl.innerHTML = '<div class="empty-state">لا توجد كتب دورية مطابقة لبحثك.</div>';
            return;
        }

        updates.forEach(u => {
            const card = document.createElement('div');
            card.className = 'reg-card';
            card.innerHTML = `
                <div class="reg-header">
                    <div>
                        <span class="category-tag">${u.category}</span>
                        <h4 class="reg-title">${u.title_ar}</h4>
                        <div style="font-size: 13px; color: #4a5568; margin-top: 4px;"><strong>الجهة:</strong> ${u.issuing_body} | <strong>المرجع:</strong> ${u.reference_law}</div>
                    </div>
                    <span class="reg-date">ساري من: ${u.effective_date}</span>
                </div>
                <p class="reg-summary">${u.summary_ar}</p>
                <div class="reg-impact-box">
                    <strong>الأثر الإجرائي المباشر:</strong> ${u.procedural_impact}
                </div>
            `;
            regulatoryContainerEl.appendChild(card);
        });
    }

    regSearchInput.addEventListener('input', () => {
        loadRegulatoryUpdates(regSearchInput.value.trim());
    });

    // Initial Loading
    loadProcedures();
    loadCases();
    loadOcrSamples();
    loadRegulatoryUpdates();
});
