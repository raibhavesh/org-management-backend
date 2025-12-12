# 🚀 Organization Management Backend — FastAPI + MongoDB

This project is a backend service designed to manage **organizations**, their **admin users**, and dynamic **MongoDB collections**.  
It is built using **FastAPI**, **Motor**, **JWT authentication**, and follows a clean modular project structure.

---

## 📌 Features

### ✔ Organization Features
- Create a new organization  
- Get organization details  
- Update organization name (with automatic collection migration)  
- Delete an organization  

### ✔ Admin Authentication
- Admin login  
- Password hashing (bcrypt)  
- JWT-based authentication  
- Protected routes for update/delete  

### ✔ MongoDB Multi-Tenant Structure
- Uses a **master database `master_db`**
- Each organization gets its own dynamic collection:
