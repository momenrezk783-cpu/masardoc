                <p class="reg-summary">${u.summary_ar}</p>
                ${u.source_url ? `<div style="margin-top: 10px; font-size: 13px;"><a href="${u.source_url}" target="_blank" rel="noreferrer">رابط المصدر</a></div>` : ''}
                <div class="reg-impact-box">
                    <strong>الأثر الإجرائي المباشر:</strong> ${u.procedural_impact}
                </div>
            `;
