# F1 Prophet - Setup Instructions

After cloning the repository, follow these steps to get the project running.

---

## **1. Frontend Setup (React)**

### **Create API Configuration File**

Navigate to: `F1-Prophet/Frontend/src/services/`

- Copy `api_start.example.js` → Create `api_start.js`
- Update the `API_START` variable with your backend URL:
  ```javascript
  export const API_START = 'http://localhost:5000/api';
  ```

### **Install Dependencies**

```bash
cd F1-Prophet/Frontend
npm install
```

### **Run Frontend (Development)**

```bash
npm start
```

Frontend will open at `http://localhost:3000`

---

## **2. Backend Setup (Flask)**

### **Create Environment Configuration**

Navigate to: `F1-Prophet/Backend/`

- Copy `.env.example` → Create `.env`
- Fill in required values:
  ```
  SECRET_KEY=
  MYSQL_HOST=
  MYSQL_PORT=
  MYSQL_USER=
  MYSQL_PASSWORD=
  MYSQL_DATABASE=
  PORT=
  ```

### **Setup MySQL Database**

1. Open MySQL client or MySQL Workbench
2. Run the SQL file: `F1-Prophet/Backend/example.sql`
   ```bash
   mysql -u root -p < example.sql
   ```
3. Verify database created:
   ```sql
   USE f1_prophet;
   SHOW TABLES;
   ```

### **Setup Python Virtual Environment**

```bash
cd F1-Prophet/Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Run Backend Server**

```bash
python app.py
```

Backend will start at `http://localhost:5000`

---

## **3. Java Desktop App Setup**

### **Prerequisites**

- Java JDK 11+ installed
- Maven installed (if using Maven)

### **Build & Run**

```bash
cd "F1-Prophet Java app"

# Compile
javac -d out src/*.java

# Run
java -cp out Main
```

app will launch with embedded browser showing frontend at `http://localhost:3000`

or run the precompiled F1 Prophet.exe file in Executable File directory.

---

## **4. Verify Everything is Running**

Check that all services are working:

| Component | URL | Status |
|-----------|-----|--------|
| Frontend | `http://localhost:3000` | Should load React app |
| Backend API | `http://localhost:5000/api/auth/me` | Should return JSON |
| MySQL | `localhost:3306 or 3307` | Should connect |
| Java App | N/A | Should show embedded browser |

---

## **Quick Start (All at Once)**

### **Terminal 1 - Backend:**
```bash
cd F1-Prophet/Backend
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
python app.py
```

### **Terminal 2 - Frontend:**
```bash
cd F1-Prophet/Frontend
npm start
```

### **Terminal 3 - Java App:**
```bash
cd F1-Prophet/JavaApp
javac -d out src/*.java && java -cp out Main
```

---

## **Troubleshooting**

### **Backend won't start**
- Check Python version: `python --version` (should be 3.8+)
- Check `.env` file exists and `DATABASE_URL` is correct
- Verify MySQL is running: `mysql -u root -p`
- Check port 5000 isn't in use: `lsof -i :5000` (macOS/Linux)

### **Frontend won't load**
- Check Node.js installed: `node --version`
- Check `api_start.js` has correct `API_START` URL
- Clear cache: `rm -rf node_modules && npm install`
- Check port 3000 isn't in use: `lsof -i :3000` (macOS/Linux)

### **Java app won't launch**
- Check Java installed: `java -version`
- Verify frontend is running at `http://localhost:3000`
- Check `MainFrame.java` has correct URL

### **Database connection fails**
- Verify MySQL is running
- Check credentials in `.env` match your MySQL setup
- Test connection: `mysql -u root -p -e "USE f1_prophet; SHOW TABLES;"`

---

## **File Structure Reference**

```
├── F1-Prophet Java App/
│   ├── Main.java
│   ├── MainFrame.java
│   ├── HomePage.java
│   └── ...
F1-Prophet/
├── Frontend/
│   ├── src/
│   │   ├── services/
│   │   │   ├── api_start.example.js  ← Copy this
│   │   │   └── api_start.js          ← Create this
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── Backend/
│   ├── .env.example                  ← Copy this
│   ├── .env                          ← Create this
│   ├── example.sql                   ← Run this in MySQL
│   ├── requirements.txt
│   ├── app.py
│   └── ...
│
│
├── LICENSE
└── README.md
```

---

## **Next Steps**

1. Follow setup instructions above
2. Verify all services running (see table above)
3. Test API: `curl http://localhost:5000/api/auth/me`
4. Test frontend: Open `http://localhost:3000` in browser
5. Test Java app: Should load frontend automatically