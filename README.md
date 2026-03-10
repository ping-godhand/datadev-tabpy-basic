# datadev-tabpy-basic

TabPy Basic for Tableau User Group / Godhand.DEV

# TabPy Setup

# การตั้งค่าสำหรับ TabPy

**TabPy** รองรับ Username/Password Authentication ผ่าน Password File ที่เก็บ Hashed Password โดยใช้งานร่วมกับ **Tableau Desktop**

## 1. สร้าง Password File

Activate Virtual Environment ก่อน:

```powershell
.venv\Scripts\Activate.ps1
```

```bash
.venv\Scripts\Activate.sh
```

ใช้คำสั่ง `tabpy-user` สร้าง Password File พร้อมกำหนด User `admin`:

```powershell
tabpy-user add -u admin -p admin -f ./tabpy-pwd.txt
```

คำสั่งนี้สร้างไฟล์ `tabpy-pwd.txt` ที่เก็บ Username และ Hashed Password (ไม่ใช่ Plaintext)

## 2. สร้าง Config File

สร้างไฟล์ `tabpy.conf` ไว้ที่ Project Root:

```ini
[TabPy]
TABPY_PORT = 9004
TABPY_PWD_FILE = ./tabpy-pwd.txt
```

## 3. Start TabPy พร้อม Authentication

```powershell
tabpy --config ./tabpy.conf
```

ตรวจสอบ Log ต้องเห็นข้อความนี้:

```
Password file is specified: Authentication is enabled
```

## 4. เชื่อมต่อจาก Tableau Desktop

1. ไปที่ **Help > Settings and Performance > Manage Analytics Extension Connection**
2. เลือก **TabPy**
3. กำหนดค่าตามนี้:
   - Server: `localhost`
   - Port: `9004`
   - Sign in with a username and password: **เปิดใช้งาน**
   - Username: `admin`
   - Password: `admin`

## Quick Reference

| Setting | Value |
|---------|-------|
| Server | localhost |
| Port | 9004 |
| Username | admin |
| Password | admin |
| Config File | `tabpy.conf` |
| Password File | `tabpy-pwd.txt` |

## เพิ่ม User เพิ่มเติม

```powershell
tabpy-user add -u xxx -p yyy -f ./tabpy-pwd.txt
```

# Config สำคัญใน tabpy.conf

ตัวอย่าง Config แบบเต็มที่ครอบคลุม Parameter สำคัญ:

```ini
[TabPy]
# --- Network ---
TABPY_PORT = 9004
TABPY_BIND_ADDRESS = 0.0.0.0

# --- Authentication ---
TABPY_PWD_FILE = ./tabpy-pwd.txt

# --- HTTPS/SSL ---
TABPY_TRANSFER_PROTOCOL = https
TABPY_CERTIFICATE_FILE = ./certs/server.crt
TABPY_KEY_FILE = ./certs/server.key

# --- Execution ---
TABPY_EVALUATE_TIMEOUT = 300
TABPY_MAX_REQUEST_SIZE_MB = 100

# --- Logging ---
TABPY_LOG_DETAILS = true

# --- State/Query Storage ---
TABPY_STATE_PATH = ./tabpy-state
TABPY_QUERY_OBJECT_PATH = ./tabpy-query
```

### Network

| Parameter | Default | คำอธิบาย |
|-----------|---------|----------|
| `TABPY_PORT` | 9004 | Port ที่ TabPy รับ Request - ต้องตรงกับค่าที่ตั้งใน Tableau Desktop |
| `TABPY_BIND_ADDRESS` | `0.0.0.0` | IP Address ที่ TabPy bind - ใช้ `127.0.0.1` ถ้าต้องการจำกัดเฉพาะ Local เท่านั้น, ใช้ `0.0.0.0` ถ้าต้องการเปิดให้เครื่องอื่นในเครือข่ายเข้าถึงได้ |

### Authentication

| Parameter | Default | คำอธิบาย |
|-----------|---------|----------|
| `TABPY_PWD_FILE` | ไม่มี | Path ไปยัง Password File - ถ้าไม่กำหนด TabPy ทำงานแบบไม่มี Authentication |

เมื่อกำหนด `TABPY_PWD_FILE` ทุก Request ต้องส่ง HTTP Basic Authentication Header มาด้วย ถ้าไม่ส่งจะได้ HTTP 401 Unauthorized

### HTTPS/SSL

| Parameter | Default | คำอธิบาย |
|-----------|---------|----------|
| `TABPY_TRANSFER_PROTOCOL` | `http` | เปลี่ยนเป็น `https` เพื่อเปิด SSL/TLS |
| `TABPY_CERTIFICATE_FILE` | ไม่มี | Path ไปยัง SSL Certificate (.crt หรือ .pem) |
| `TABPY_KEY_FILE` | ไม่มี | Path ไปยัง Private Key (.key) |

ทั้งสาม Parameter ต้องกำหนดพร้อมกัน ถ้าขาดตัวใดตัวหนึ่ง TabPy จะ Start ไม่ขึ้น สำหรับ Production ควรใช้ HTTPS เสมอ โดยเฉพาะเมื่อเปิด Authentication เพราะ HTTP Basic Auth ส่ง Credentials เป็น Base64 (ไม่ได้เข้ารหัส)

### Execution

| Parameter | Default | คำอธิบาย |
|-----------|---------|----------|
| `TABPY_EVALUATE_TIMEOUT` | 30 (วินาที) | Timeout สำหรับ Script Execution แต่ละครั้ง - ถ้า Script ประมวลผลนานกว่านี้จะถูกตัดทิ้ง ปรับเพิ่มสำหรับ Model ขนาดใหญ่หรือ Data Processing ที่หนัก |
| `TABPY_MAX_REQUEST_SIZE_MB` | 100 (MB) | ขนาด Request สูงสุดที่รับได้ - ป้องกัน Payload ขนาดใหญ่เกินไปส่งเข้ามา |

### Logging

| Parameter | Default | คำอธิบาย |
|-----------|---------|----------|
| `TABPY_LOG_DETAILS` | `false` | เปิดเป็น `true` เพื่อ Log รายละเอียด Request/Response - ใช้ตอน Debug แต่ไม่ควรเปิดใน Production เพราะอาจ Log ข้อมูลที่เป็น Sensitive Data |

### State/Query Storage

| Parameter | Default | คำอธิบาย |
|-----------|---------|----------|
| `TABPY_STATE_PATH` | `./state` | Path เก็บ State ของ TabPy Server เช่น Deployed Endpoints |
| `TABPY_QUERY_OBJECT_PATH` | `./query_objects` | Path เก็บ Query Object ที่ Deploy ผ่าน TabPy API |

ทั้งสอง Path ต้องมีสิทธิ์ Write - ถ้า Path ไม่มีอยู่ TabPy จะสร้างให้อัตโนมัติ

## หมายเหตุ

- Password File เก็บ Hashed Password ไม่ใช่ Plaintext - ปลอดภัยกว่าการเก็บรหัสผ่านตรง
- เพิ่ม `tabpy-pwd.txt` ใน `.gitignore` เพื่อป้องกันการ Commit Credentials ขึ้น Repository
- สำหรับ HTTPS ให้เพิ่ม `TABPY_TRANSFER_PROTOCOL`, `TABPY_CERTIFICATE_FILE` และ `TABPY_KEY_FILE` ใน `tabpy.conf`