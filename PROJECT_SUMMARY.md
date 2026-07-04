# Arogya-App: Project Blueprint & Master Plan

## 1. Project Vision

### Goal
Build a modern, user-friendly, and offline-capable Pharmacy Desktop Application similar to Marge Software.

### Target Users
Medical Store Owners

- Easy-to-use billing system
- Stock management
- Purchase management
- Sales management
- Reports & analytics

### Tech Stack

#### Backend
- Django
- Django REST Framework (REST API)

#### Frontend
- Vue.js (Single Page Application)

#### Desktop Layer
- Electron (Windows Packaging & Offline Support)

---

# 2. App Architecture

The project is divided into four main Django apps:

## users
Handles authentication and user management.

### Features
- Login
- Signup
- Logout
- Password Reset
- Security Question Verification
- JWT Authentication

---

## masters
Handles all master data.

### Features
- Company Master
- Medicine Master
- Salt Master
- Supplier Master
- Customer Master (Optional)

---

## transactions
Handles stock movement and purchase transactions.

### Features
- Purchase Entry
- Purchase Return
- Stock Tracking
- Stock Inward
- Stock Outward
- Batch Management
- Expiry Tracking

---

## core
Contains global configuration and shared utilities.

### Features
- Global Settings
- Shared Utilities
- Permissions
- Helper Functions
- Common APIs

---

# 3. Development Roadmap

| Phase | Module | Status |
|--------|--------|--------|
| Phase 1 | Authentication & System Security | ✅ Completed |
| Phase 2 | Masters Management | ✅ Completed |
| Phase 3 | Transactions & Stock Engine | ✅ Completed |
| Phase 4 | Billing Engine & Invoice System | 🚀 Next |
| Phase 5 | Reports & Financial Analytics | ⏳ Pending |
| Phase 6 | Electron Packaging (Offline Desktop App) | ⏳ Pending |
| Phase 7 | Final UI/UX & Deployment | ⏳ Pending |

---

# Current Progress

## ✅ Last Completed Milestone

Successfully fixed:

- Auth 404 Error
- Auth 400 Error

Updated files:

- `views.py`
- `urls.py`

Authentication module is now working correctly.

---

# Next Milestone

## 🚀 Phase 4 — Billing Engine

Development will focus on:

- Invoice Generation
- GST Calculation
- Thermal Printing
- Stock Deduction
- Payment Handling
- Barcode Billing

---

# Phase 4 Technical Blueprint

## Step 1 — Database Models

### SaleInvoice

- Invoice Number
- Invoice Date
- Customer
- Payment Mode
- Gross Total
- Discount
- GST
- Net Amount
- Created By

---

### SaleItem

- Medicine
- Batch
- Quantity
- Sale Price
- MRP
- GST
- Discount
- Total

---

### Payment

- Cash
- UPI
- Card
- Credit

---

# Billing APIs

Create REST APIs for:

- Create Invoice
- Update Invoice
- Delete Invoice
- Cancel Invoice
- Fetch Invoice
- Search Invoice
- Print Invoice

---

# Billing UI (Vue.js)

Billing screen should include:

- Barcode Scanner
- Medicine Search
- Quantity Entry
- Batch Selection
- Discount
- GST Calculation
- Net Total
- Customer Details
- Payment Mode
- Keyboard Shortcuts

---

# Stock Engine Integration

When an invoice is generated:

- Deduct Stock Automatically
- Prevent Negative Stock
- Support Batch-wise Deduction
- Restore Stock on Invoice Cancellation

---

# Printing Module

Support multiple print formats:

- 58 mm Thermal Printer
- 80 mm Thermal Printer
- A4 Invoice
- Print Preview
- Reprint Invoice

---

# Offline Support (Electron)

Features:

- Local Database
- Offline Billing
- Sync Queue
- Automatic Data Synchronization
- Conflict Resolution

---

# Suggested Project Structure

```text
backend/
│
├── users/
├── masters/
├── transactions/
├── billing/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   ├── invoice.py
│   └── stock.py
│
└── core/

frontend/
│
└── src/
    └── pages/
        └── Billing/
            ├── Billing.vue
            ├── InvoicePrint.vue
            ├── PaymentDialog.vue
            └── SearchMedicine.vue
```

---

# Future Features

To make the application comparable to professional pharmacy software:

- Barcode Billing
- Batch Selection
- Expiry Alerts
- Low Stock Alerts
- Customer Ledger
- Credit Billing
- Sales Return
- Purchase Return
- GST Reports
- Daily Cash Closing
- Shift Management
- Keyboard-only Billing
- PDF Invoice Export
- Auto Invoice Numbering
- Backup & Restore
- Audit Logs

---

# Resume Development

Whenever you want to continue the project, simply say:

> **Start Arogya-App**

Development will resume from **Phase 4 (Billing Engine)**, including:

- Django Models
- REST APIs
- Vue.js Billing Interface
- GST Logic
- Invoice Number Generation
- Stock Deduction
- Thermal Printing
- Electron Offline Integration

---

# Project Vision

**Arogya-App** aims to become a complete, modern, offline-capable Pharmacy Management System with:

- Fast Billing
- Efficient Inventory Management
- Secure Authentication
- Offline Desktop Support
- Professional UI/UX
- GST Compliance
- Thermal Printing
- Enterprise-level Architecture

**Goal:** Deliver a production-ready Pharmacy Management Desktop Application that is scalable, maintainable, and easy to use for medical store owners.