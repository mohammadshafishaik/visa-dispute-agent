"""Professional web UI for dispute submission"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

# Professional banking-style HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dispute Resolution System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
            padding: 20px;
            color: #2c3e50;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .header {
            background: #1a1f36;
            color: white;
            padding: 24px 32px;
            border-bottom: 3px solid #0066cc;
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .header p {
            font-size: 14px;
            color: #a0aec0;
        }
        
        .form-container {
            padding: 32px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 6px;
            color: #2d3748;
            font-weight: 500;
            font-size: 14px;
        }
        
        label .required {
            color: #e53e3e;
        }
        
        input, select, textarea {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #cbd5e0;
            border-radius: 4px;
            font-size: 14px;
            font-family: inherit;
            transition: border-color 0.2s;
            background: white;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #0066cc;
        }
        
        textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        .submit-btn {
            background: #0066cc;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: background 0.2s;
        }
        
        .submit-btn:hover {
            background: #0052a3;
        }
        
        .submit-btn:disabled {
            background: #a0aec0;
            cursor: not-allowed;
        }
        
        .result {
            margin-top: 24px;
            padding: 16px;
            border-radius: 4px;
            display: none;
            border-left: 4px solid;
        }
        
        .result.success {
            background: #f0fdf4;
            border-color: #22c55e;
            color: #166534;
        }
        
        .result.error {
            background: #fef2f2;
            border-color: #ef4444;
            color: #991b1b;
        }
        
        .result.processing {
            background: #fffbeb;
            border-color: #f59e0b;
            color: #92400e;
        }
        
        .result h3 {
            margin-bottom: 12px;
            font-size: 16px;
            font-weight: 600;
        }
        
        .result-details {
            margin-top: 12px;
            padding: 12px;
            background: rgba(255,255,255,0.6);
            border-radius: 4px;
            font-size: 13px;
        }
        
        .result-details p {
            margin: 6px 0;
            line-height: 1.5;
        }
        
        .result-details strong {
            font-weight: 600;
        }
        
        .loader {
            border: 3px solid #e2e8f0;
            border-top: 3px solid #0066cc;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            animation: spin 1s linear infinite;
            margin: 16px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        
        .char-counter {
            font-size: 12px;
            color: #718096;
            text-align: right;
            margin-top: 4px;
        }
        
        .error-message {
            color: #e53e3e;
            font-size: 12px;
            margin-top: 4px;
            display: none;
        }
        
        input:invalid, select:invalid, textarea:invalid {
            border-color: #fc8181;
        }
        
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .container {
                margin: 0;
                border-radius: 0;
            }
            
            .form-container {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Dispute Resolution System</h1>
            <p>Automated dispute processing powered by AI</p>
        </div>
        
        <div class="form-container">
            <div style="background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 16px; margin-bottom: 24px;">
                <h3 style="font-size: 14px; font-weight: 600; margin-bottom: 8px; color: #2d3748;">Validation Rules</h3>
                <ul style="font-size: 13px; color: #4a5568; line-height: 1.8; margin-left: 20px;">
                    <li>Customer ID: Must be 4 uppercase letters followed by 4 numbers (e.g., CUST1234)</li>
                    <li>Phone: Must be exactly 10 digits (without country code)</li>
                    <li>Email: Must contain @ symbol and valid domain (e.g., user@example.com)</li>
                    <li>Description: Minimum 20 characters required</li>
                    <li>Transaction Date: Cannot be in the future</li>
                    <li>All fields marked with * are mandatory</li>
                </ul>
            </div>
            
            <form id="disputeForm">
                <div class="form-row">
                    <div class="form-group">
                        <label for="customerName">Customer Name <span class="required">*</span></label>
                        <input type="text" id="customerName" name="customerName" required 
                               minlength="3" maxlength="100">
                    </div>
                    
                    <div class="form-group">
                        <label for="customerId">Customer ID <span class="required">*</span></label>
                        <input type="text" id="customerId" name="customerId" required 
                               pattern="[A-Z]{4}[0-9]{4}" maxlength="8" 
                               style="text-transform: uppercase;">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="email">Email Address <span class="required">*</span></label>
                        <input type="email" id="email" name="email" required 
                               pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$">
                        <small style="color: #718096; font-size: 12px;">Must contain @ and valid domain (e.g., user@example.com)</small>
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone Number <span class="required">*</span></label>
                        <div style="display: flex; gap: 8px;">
                            <select id="countryCode" name="countryCode" required style="width: 100px;">
                                <option value="+91">+91 (IN)</option>
                                <option value="+1">+1 (US)</option>
                                <option value="+44">+44 (UK)</option>
                                <option value="+971">+971 (UAE)</option>
                                <option value="+65">+65 (SG)</option>
                            </select>
                            <input type="tel" id="phone" name="phone" required 
                                   pattern="[0-9]{10}" maxlength="10" 
                                   style="flex: 1;">
                        </div>
                        <small style="color: #718096; font-size: 12px;">Enter 10-digit number only</small>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="cardNumber">Card Number (Last 4 digits) <span class="required">*</span></label>
                        <input type="text" id="cardNumber" name="cardNumber" required 
                               maxlength="4" pattern="[0-9]{4}">
                    </div>
                    
                    <div class="form-group">
                        <label for="transactionId">Transaction ID <span class="required">*</span></label>
                        <input type="text" id="transactionId" name="transactionId" required 
                               minlength="5" maxlength="50">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="transactionDate">Transaction Date <span class="required">*</span></label>
                        <input type="date" id="transactionDate" name="transactionDate" required>
                        <small style="color: #666; font-size: 12px;">Must be within last 120 days</small>
                    </div>
                    
                    <div class="form-group">
                        <label for="merchantName">Merchant Name <span class="required">*</span></label>
                        <input type="text" id="merchantName" name="merchantName" required 
                               minlength="2" maxlength="100">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="amount">Dispute Amount (INR) <span class="required">*</span></label>
                        <input type="number" id="amount" name="amount" required 
                               step="0.01" min="1" max="10000000">
                    </div>
                    
                    <div class="form-group">
                        <label for="reasonCode">Dispute Reason <span class="required">*</span></label>
                        <select id="reasonCode" name="reasonCode" required>
                            <option value="">Select dispute reason</option>
                            <option value="10.4">Fraud - Card Not Present</option>
                            <option value="10.1">Fraud - Counterfeit Card</option>
                            <option value="11.1">Authorization Issue</option>
                            <option value="12.1">Processing Error</option>
                            <option value="13.1">Goods/Services Not Received</option>
                            <option value="13.2">Recurring Transaction Cancelled</option>
                            <option value="13.3">Goods/Services Not as Described</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="description">Dispute Description (Minimum 20 characters) <span class="required">*</span></label>
                    <textarea id="description" name="description" required 
                              minlength="20" maxlength="1000"></textarea>
                    <div class="char-counter">
                        <span id="charCount">0</span> / 1000 characters (minimum 20)
                    </div>
                </div>
                
                <button type="submit" class="submit-btn" id="submitBtn">Submit Dispute</button>
            </form>
            
            <div id="result" class="result"></div>
        </div>
    </div>
    
    <script>
        const form = document.getElementById('disputeForm');
        const submitBtn = document.getElementById('submitBtn');
        const resultDiv = document.getElementById('result');
        const description = document.getElementById('description');
        const charCount = document.getElementById('charCount');
        const customerId = document.getElementById('customerId');
        
        // Character counter for description
        description.addEventListener('input', () => {
            const count = description.value.length;
            charCount.textContent = count;
            charCount.style.color = count < 20 ? '#e53e3e' : count > 900 ? '#f59e0b' : '#718096';
        });
        
        // Auto-uppercase customer ID
        customerId.addEventListener('input', (e) => {
            e.target.value = e.target.value.toUpperCase();
        });
        
        // Set max date to today and default to 7 days ago for transaction date
        const today = new Date();
        const sevenDaysAgo = new Date(today);
        sevenDaysAgo.setDate(today.getDate() - 7);
        
        // Set min date to 120 days ago (Visa rule)
        const minDate = new Date(today);
        minDate.setDate(today.getDate() - 120);
        
        const todayStr = today.toISOString().split('T')[0];
        const minDateStr = minDate.toISOString().split('T')[0];
        const defaultDate = sevenDaysAgo.toISOString().split('T')[0];
        
        const transactionDateInput = document.getElementById('transactionDate');
        transactionDateInput.setAttribute('max', todayStr);
        transactionDateInput.setAttribute('min', minDateStr);
        transactionDateInput.value = defaultDate;
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const disputeId = 'DSP-' + Date.now();
            
            // Disable submit button
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            
            // Show processing state
            resultDiv.className = 'result processing';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `
                <h3>Processing Dispute</h3>
                <div class="loader"></div>
                <p>Analyzing dispute against Visa regulations...</p>
            `;
            
            // Validate form data
            const customerId = formData.get('customerId');
            const phone = formData.get('phone');
            const description = formData.get('description');
            
            // Validation checks
            if (!/^[A-Z]{4}[0-9]{4}$/.test(customerId)) {
                throw new Error('Customer ID must be 4 letters followed by 4 numbers (e.g., CUST1234)');
            }
            
            if (!/^[0-9]{10}$/.test(phone)) {
                throw new Error('Phone number must be exactly 10 digits');
            }
            
            if (description.length < 20) {
                throw new Error('Description must be at least 20 characters');
            }
            
            // Prepare request with proper field mapping
            const payload = {
                dispute_id: disputeId,
                customer_id: formData.get('customerId'),
                transaction_id: formData.get('transactionId'),
                amount: parseFloat(formData.get('amount')),
                currency: 'INR',
                reason_code: formData.get('reasonCode'),
                description: formData.get('description'),
                timestamp: new Date().toISOString()
            };
            
            // Add optional fields for email service (not in schema)
            const extraData = {
                customer_email: formData.get('email'),
                customer_phone: formData.get('countryCode') + formData.get('phone'),
                customer_name: formData.get('customerName'),
                transaction_date: formData.get('transactionDate'),
                merchant_name: formData.get('merchantName'),
                card_number: formData.get('cardNumber')
            };
            
            // Merge for validation
            const fullPayload = {...payload, ...extraData};
            
            try {
                // Submit dispute with full payload
                const response = await fetch('/webhooks/dispute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(fullPayload)
                });
                
                const data = await response.json();
                
                // Handle rejection (400 status)
                if (response.status === 400 && data.detail) {
                    const rejection = data.detail;
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = `
                        <h3>Dispute Rejected</h3>
                        <div class="result-details">
                            <p><strong>Rejection Code:</strong> ${rejection.rejection_code || 'N/A'}</p>
                            <p><strong>Reason:</strong></p>
                            <p style="padding: 8px; background: #fff; border-radius: 4px;">${rejection.message || data.detail}</p>
                            <p style="margin-top: 12px;">Please correct the information and resubmit.</p>
                        </div>
                    `;
                    return;
                }
                
                if (response.ok) {
                    // Wait for processing
                    await new Promise(resolve => setTimeout(resolve, 3000));
                    
                    // Check review queue
                    const queueResponse = await fetch('/review-queue');
                    const queue = await queueResponse.json();
                    const inQueue = queue.find(item => item.dispute_id === disputeId);
                    
                    if (inQueue) {
                        // Escalated to human review
                        resultDiv.className = 'result processing';
                        resultDiv.innerHTML = `
                            <h3>Escalated to Human Review</h3>
                            <div class="result-details">
                                <p><strong>Dispute ID:</strong> ${disputeId}</p>
                                <p><strong>Status:</strong> Pending Review</p>
                                <p><strong>Confidence Score:</strong> ${(inQueue.confidence_score * 100).toFixed(1)}%</p>
                                <p><strong>Decision:</strong> ${inQueue.decision.toUpperCase()}</p>
                                <p><strong>Reasoning:</strong> ${inQueue.reasoning}</p>
                                <p style="margin-top: 12px;">This case requires specialist review. Expected resolution within 24 hours.</p>
                                <p style="margin-top: 8px; padding: 8px; background: #e8f5e9; border-radius: 4px; border-left: 3px solid #4caf50;">
                                    <strong>📧 Email Notification:</strong><br>
                                    An email with the decision details will be sent to: <strong>${formData.get('email')}</strong>
                                </p>
                            </div>
                        `;
                    } else {
                        // Automated decision
                        resultDiv.className = 'result success';
                        resultDiv.innerHTML = `
                            <h3>Dispute Processed Successfully</h3>
                            <div class="result-details">
                                <p><strong>Dispute ID:</strong> ${disputeId}</p>
                                <p><strong>Status:</strong> ${data.status.toUpperCase()}</p>
                                <p><strong>Customer:</strong> ${formData.get('customerName')}</p>
                                <p><strong>Amount:</strong> ₹${parseFloat(formData.get('amount')).toFixed(2)}</p>
                                <p><strong>Reason:</strong> ${formData.get('reasonCode')}</p>
                                <p style="margin-top: 12px;">Your dispute has been processed successfully.</p>
                                <p style="margin-top: 8px; padding: 8px; background: #e8f5e9; border-radius: 4px; border-left: 3px solid #4caf50;">
                                    <strong>📧 Email Notification:</strong><br>
                                    Decision details will be sent to: <strong>${formData.get('email')}</strong>
                                </p>
                            </div>
                        `;
                    }
                    
                    // Reset form
                    form.reset();
                } else {
                    throw new Error(data.detail || 'Submission failed');
                }
            } catch (error) {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `
                    <h3>Submission Error</h3>
                    <p>${error.message}</p>
                    <p style="margin-top: 12px;">Please verify your information and try again.</p>
                `;
            } finally {
                // Re-enable submit button
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Dispute';
            }
        });
    </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
async def web_interface():
    """Serve the professional web UI"""
    return HTML_TEMPLATE
