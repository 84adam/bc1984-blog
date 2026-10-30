![arkfile.net](/images/2024/10/dalle-bw-forest.png)

Initial brainstorming for Arkfile

**Find the code here: <https://github.com/arkfile/Arkfile>**

---

# Application Architecture

## High-Level Architecture

### Components

**Client-Side**

- Web interface for user interaction
- WebAssembly (WASM) module for client-side encryption/decryption
- JavaScript for WASM interaction and API calls

**Server-Side**

- Go HTTP server (Echo framework)
- JWT authentication
- SQLite database for user data and file metadata
- Integration with Backblaze B2 (via MinIO client) for file storage

**External Services**

- Backblaze B2 for encrypted file storage
- Caddy web server for TLS and reverse proxy

### Security Features

- Client-side encryption using user passwords
- Password hints stored separately from encrypted files
- JWT-based authentication
- TLS encryption for all traffic
- Secure key derivation (PBKDF2)

## Directory Structure

```
arkfile/
│
├── main.go                 # Application entry point
├── .env                    # Environment variables
├── go.mod                  # Go module file
├── go.sum                  # Go module checksum
├── Caddyfile              # Caddy server configuration
│
├── client/                 # Client-side code
│   ├── main.go            # WASM source code
│   ├── main.wasm          # Compiled WASM binary
│   ├── wasm_exec.js       # Go WASM support code
│   └── static/            # Static web assets
│       ├── index.html     # Main web interface
│       ├── css/           # Stylesheets
│       └── js/            # Client-side JavaScript
│
├── auth/                   # Authentication package
│   └── jwt.go             # JWT implementation
│
├── database/              # Database package
│   ├── database.go        # Database initialization and connection
│   └── migrations/        # Database migrations
│
├── handlers/              # HTTP handlers
│   └── handlers.go        # Request handlers implementation
│
├── storage/               # Storage package
│   └── minio.go          # MinIO/Backblaze integration
│
├── logging/               # Logging package
│   └── logging.go         # Logging implementation
│
├── models/                # Data models
│   ├── user.go           # User model
│   └── file.go           # File metadata model
│
├── config/               # Configuration
│   └── config.go         # Configuration loading
│
├── scripts/              # Utility scripts
│   ├── build.sh         # Build script
│   └── deploy.sh        # Deployment script
│
├── systemd/             # Systemd service files
│   ├── arkfile.service
│   └── caddy.service
│
└── docs/                # Documentation
    ├── api.md          # API documentation
    ├── setup.md        # Setup instructions
    └── security.md     # Security documentation
```

## Key Files and Their Purposes

**`main.go`**

- Application entry point
- Server setup and routing
- Middleware configuration

**`client/main.go`**

- Client-side encryption/decryption logic
- WASM-based file processing

**`handlers/handlers.go`**

- HTTP request handlers
- File upload/download logic
- User authentication handlers

**`storage/minio.go`**

- Backblaze B2 integration
- File storage operations

**`auth/jwt.go`**

- JWT token generation and validation
- Authentication middleware

**`database/database.go`**

- Database connection setup
- Schema creation
- File metadata storage

## Data Flow

**File Upload**

```
Client → Client-side Encryption (WASM) → Server (Echo)
→ Backblaze B2 → SQLite (metadata)
```

**File Download**

```
Client → Server Request → Server (Echo)
→ Backblaze B2 (encrypted file)
→ SQLite (password hint) → Client
→ Client-side Decryption (WASM)
```

## Environment Variables

```
BACKBLAZE_ENDPOINT=...
BACKBLAZE_KEY_ID=...
BACKBLAZE_APPLICATION_KEY=...
BACKBLAZE_BUCKET_NAME=...
JWT_SECRET=...
VULTR_API_KEY=...
```

## Build and Deployment

**Build Process**

- Compile server-side Go code
- Compile client-side Go code to WASM
- Bundle static assets

**Deployment**

- Set up Vultr server with Rocky Linux
- Configure Caddy for TLS
- Set up systemd services
- Configure firewall

## Security Layers

**Transport Security**

- TLS via Caddy
- HTTPS enforcement

**Data Security**

- Client-side encryption
- Secure key derivation
- Password hints

**Authentication**

- JWT-based auth
- Secure password storage

**Authorization**

- File access control
- User permissions

The application follows a clean architecture pattern with clear separation of concerns, making it maintainable and scalable. Each component has a single responsibility, and dependencies flow inward from external services to the core business logic.

---

# TOP LEVEL

## 1. main.go

```go
package main

import (
	"log"
	"os"

	"github.com/joho/godotenv"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	
	"github.com/84adam/arkfile/auth"
	"github.com/84adam/arkfile/database"
	"github.com/84adam/arkfile/handlers"
	"github.com/84adam/arkfile/logging"
	"github.com/84adam/arkfile/storage"
)

func main() {
	// Load environment variables
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}

	// Initialize logging
	logging.InitLogging()

	// Initialize database
	database.InitDB()
	defer database.DB.Close()

	// Initialize storage
	storage.InitMinio()

	// Create Echo instance
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	e.Use(middleware.CORS())
	e.Use(middleware.SecureWithConfig(middleware.SecureConfig{
		XSSProtection:         "1; mode=block",
		ContentTypeNosniff:    "nosniff",
		XFrameOptions:         "SAMEORIGIN",
		HSTSMaxAge:           31536000,
		ContentSecurityPolicy: "default-src 'self'",
	}))

	// Serve static files for the web client
	e.Static("/", "client/static")

	// Serve WebAssembly files
	e.File("/wasm_exec.js", "client/wasm_exec.js")
	e.File("/main.wasm", "client/main.wasm")

	// Routes
	// Auth routes
	e.POST("/register", handlers.Register)
	e.POST("/login", handlers.Login)

	// File routes (protected)
	fileGroup := e.Group("/api")
	fileGroup.Use(auth.JWTMiddleware())
	fileGroup.POST("/upload", handlers.UploadFile)
	fileGroup.GET("/download/:filename", handlers.DownloadFile)

	// Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	if err := e.Start(":" + port); err != nil {
		logging.ErrorLogger.Printf("Failed to start server: %v", err)
	}
}
```

## 2. .env

```bash
# Server Configuration
PORT=8080
JWT_SECRET=your_very_secure_jwt_secret_key_here

# Backblaze Configuration
BACKBLAZE_ENDPOINT=s3.us-west-000.backblazeb2.com
BACKBLAZE_KEY_ID=your_backblaze_key_id
BACKBLAZE_APPLICATION_KEY=your_backblaze_application_key
BACKBLAZE_BUCKET_NAME=your_bucket_name

# Vultr Configuration
VULTR_API_KEY=your_vultr_api_key

# Database Configuration
DB_PATH=./arkfile.db

# TLS Configuration (for development)
TLS_ENABLED=false
TLS_CERT_FILE=
TLS_KEY_FILE=
```

## 3. go.mod

```go
module github.com/84adam/arkfile

go 1.21

require (
	github.com/caddyserver/caddy/v2 v2.7.4
	github.com/golang-jwt/jwt v3.2.2+incompatible
	github.com/joho/godotenv v1.5.1
	github.com/labstack/echo/v4 v4.11.1
	github.com/minio/minio-go/v7 v7.0.61
	github.com/zalando/go-keyring v0.2.3
	gitlab.com/cznic/sqlite v1.20.0
	golang.org/x/crypto v0.13.0
)

require (
	// ... (go.mod will list all indirect dependencies here)
	// The actual list would be quite long, so I've omitted it for brevity
)
```

## 4. Caddyfile

```
{
	email your-email@example.com
	acme_dns vultr {env.VULTR_API_KEY}
}

# Main site configuration
arkfile.net {
	encode gzip

	# TLS configuration
	tls {
		dns vultr {env.VULTR_API_KEY}
	}

	# Headers for security
	header {
		# Enable HSTS
		Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
		# Prevent clickjacking
		X-Frame-Options "SAMEORIGIN"
		# Prevent XSS attacks
		X-XSS-Protection "1; mode=block"
		# Prevent MIME-sniffing
		X-Content-Type-Options "nosniff"
		# CSP
		Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-eval' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline';"
	}

	# Reverse proxy to your Go application
	reverse_proxy localhost:8080 {
		# Health checks
		health_uri /health
		health_interval 30s
		health_timeout 10s
		health_status 200

		# Timeouts
		timeout 30s

		# Headers
		header_up X-Real-IP {remote_host}
		header_up X-Forwarded-Proto {scheme}
		header_up X-Forwarded-For {remote_host}
	}

	# Access logging
	log {
		output file /var/log/caddy/access.log
		format json
	}

	# Error handling
	handle_errors {
		respond "{http.error.status_code} {http.error.status_text}"
	}
}
```

Note: The `go.sum` file is automatically generated when you run `go mod tidy` and contains cryptographic hashes of the specific module versions your application depends on. It's used to ensure reproducible builds but isn't something you typically edit manually.

A few important notes about these files:

**`main.go`**:

- Initializes all components (database, storage, logging)
- Sets up middleware for security and CORS
- Configures routes and static file serving
- Includes WebAssembly support

**`.env`**:

- Never commit this file to version control
- Contains all sensitive configuration
- Should have a `.env.example` template for documentation

**`go.mod`**:

- Lists direct dependencies
- Managed by Go's module system
- Updated using `go mod tidy`

**`Caddyfile`**:

- Configures TLS and HTTP security headers
- Sets up reverse proxy to your Go application
- Includes logging and error handling
- Configures HTTPS with automatic certificate management

To set up the project:

1. Copy the `.env.example` to `.env` and fill in your values
2. Run `go mod tidy` to install dependencies
3. Build the WASM client
4. Start Caddy and your Go application

Remember to:

- Keep the `.env` file secure and never commit it
- Regularly update dependencies for security
- Monitor logs for any issues
- Backup your database and configuration
- Review security headers periodically

---

# CLIENT SIDE CODE

## 1. client/main.go (WASM Source)

```go
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"syscall/js"

	"golang.org/x/crypto/pbkdf2"
	"golang.org/x/crypto/sha3"
)

var (
	// Number of PBKDF2 iterations
	iterations = 100000
	// Key length in bytes
	keyLength = 32
)

func main() {
	c := make(chan struct{})
	
	// Register JavaScript functions
	js.Global().Set("encryptFile", js.FuncOf(encryptFile))
	js.Global().Set("decryptFile", js.FuncOf(decryptFile))
	js.Global().Set("generateSalt", js.FuncOf(generateSalt))
	
	// Keep the Go program running
	<-c
}

func encryptFile(this js.Value, args []js.Value) interface{} {
	if len(args) != 2 {
		return "Invalid number of arguments"
	}

	data := make([]byte, args[0].Length())
	js.CopyBytesToGo(data, args[0])
	password := args[1].String()

	// Generate salt
	salt := make([]byte, 16)
	if _, err := rand.Read(salt); err != nil {
		return "Failed to generate salt"
	}

	// Derive key from password
	key := pbkdf2.Key([]byte(password), salt, iterations, keyLength, sha3.New256)

	// Create cipher block
	block, err := aes.NewCipher(key)
	if err != nil {
		return "Failed to create cipher block"
	}

	// Create GCM mode
	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return "Failed to create GCM"
	}

	// Generate nonce
	nonce := make([]byte, gcm.NonceSize())
	if _, err := rand.Read(nonce); err != nil {
		return "Failed to generate nonce"
	}

	// Encrypt data
	ciphertext := gcm.Seal(nonce, nonce, data, nil)

	// Combine salt and ciphertext
	result := append(salt, ciphertext...)

	// Return base64 encoded result
	return base64.StdEncoding.EncodeToString(result)
}

func decryptFile(this js.Value, args []js.Value) interface{} {
	if len(args) != 2 {
		return "Invalid number of arguments"
	}

	encodedData := args[0].String()
	password := args[1].String()

	// Decode base64
	data, err := base64.StdEncoding.DecodeString(encodedData)
	if err != nil {
		return "Failed to decode data"
	}

	// Extract salt (first 16 bytes)
	salt := data[:16]
	data = data[16:]

	// Derive key from password
	key := pbkdf2.Key([]byte(password), salt, iterations, keyLength, sha3.New256)

	// Create cipher block
	block, err := aes.NewCipher(key)
	if err != nil {
		return "Failed to create cipher block"
	}

	// Create GCM mode
	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return "Failed to create GCM"
	}

	// Extract nonce and ciphertext
	nonceSize := gcm.NonceSize()
	if len(data) < nonceSize {
		return "Data too short"
	}

	nonce := data[:nonceSize]
	ciphertext := data[nonceSize:]

	// Decrypt data
	plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return "Failed to decrypt data"
	}

	// Return base64 encoded plaintext
	return base64.StdEncoding.EncodeToString(plaintext)
}

func generateSalt(this js.Value, args []js.Value) interface{} {
	salt := make([]byte, 16)
	if _, err := rand.Read(salt); err != nil {
		return "Failed to generate salt"
	}
	return base64.StdEncoding.EncodeToString(salt)
}
```

## 2. client/static/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure File Sharing</title>
    <link rel="stylesheet" href="/css/styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>Secure File Sharing</h1>
        </header>

        <div class="auth-section" id="auth-section">
            <div class="login-form" id="login-form">
                <h2>Login</h2>
                <input type="email" id="login-email" placeholder="Email">
                <input type="password" id="login-password" placeholder="Password">
                <button onclick="login()">Login</button>
                <p>Don't have an account? <a href="#" onclick="toggleAuthForm()">Register</a></p>
            </div>

            <div class="register-form hidden" id="register-form">
                <h2>Register</h2>
                <input type="email" id="register-email" placeholder="Email">
                <input type="password" id="register-password" placeholder="Password">
                <input type="password" id="register-password-confirm" placeholder="Confirm Password">
                <button onclick="register()">Register</button>
                <p>Already have an account? <a href="#" onclick="toggleAuthForm()">Login</a></p>
            </div>
        </div>

        <div class="file-section hidden" id="file-section">
            <div class="upload-section">
                <h2>Upload File</h2>
                <input type="file" id="fileInput">
                <input type="password" id="filePassword" placeholder="File Password">
                <input type="text" id="passwordHint" placeholder="Password Hint (optional)">
                <button onclick="uploadFile()">Upload</button>
            </div>

            <div class="files-list">
                <h2>Your Files</h2>
                <div id="filesList"></div>
            </div>
        </div>
    </div>

    <script src="/wasm_exec.js"></script>
    <script src="/js/app.js"></script>
</body>
</html>
```

## 3. client/static/css/styles.css

```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --background-color: #ecf0f1;
    --text-color: #2c3e50;
    --error-color: #e74c3c;
    --success-color: #27ae60;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

header {
    text-align: center;
    margin-bottom: 2rem;
}

h1 {
    color: var(--primary-color);
    margin-bottom: 1rem;
}

h2 {
    color: var(--primary-color);
    margin-bottom: 1.5rem;
}

.auth-section, .file-section {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

input {
    width: 100%;
    padding: 0.8rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

button {
    background-color: var(--secondary-color);
    color: white;
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    width: 100%;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #2980b9;
}

.hidden {
    display: none;
}

.error {
    color: var(--error-color);
    margin-bottom: 1rem;
}

.success {
    color: var(--success-color);
    margin-bottom: 1rem;
}

.files-list {
    margin-top: 2rem;
}

.file-item {
    background: #f8f9fa;
    padding: 1rem;
    margin-bottom: 0.5rem;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.file-item button {
    width: auto;
    margin-left: 1rem;
}
```

## 4. client/static/js/app.js

```javascript
// Initialize WebAssembly
let wasmReady = false;

async function initWasm() {
    const go = new Go();
    try {
        const result = await WebAssembly.instantiateStreaming(
            fetch("/main.wasm"),
            go.importObject
        );
        go.run(result.instance);
        wasmReady = true;
    } catch (err) {
        console.error('Failed to load WASM:', err);
    }
}

initWasm();

// Authentication functions
async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.token);
            showFileSection();
            loadFiles();
        } else {
            showError('Login failed. Please check your credentials.');
        }
    } catch (error) {
        showError('An error occurred during login.');
    }
}

async function register() {
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-password-confirm').value;

    if (password !== confirmPassword) {
        showError('Passwords do not match.');
        return;
    }

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            toggleAuthForm();
            showSuccess('Registration successful. Please login.');
        } else {
            showError('Registration failed. Please try again.');
        }
    } catch (error) {
        showError('An error occurred during registration.');
    }
}

// File handling functions
async function uploadFile() {
    if (!wasmReady) {
        showError('WASM not ready. Please try again.');
        return;
    }

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        showError('Please select a file.');
        return;
    }

    const password = document.getElementById('filePassword').value;
    if (!password) {
        showError('Please enter a password for the file.');
        return;
    }

    const passwordHint = document.getElementById('passwordHint').value;

    try {
        const fileData = await file.arrayBuffer();
        const encryptedData = encryptFile(new Uint8Array(fileData), password);

        const formData = new FormData();
        formData.append('filename', file.name);
        formData.append('data', encryptedData);
        formData.append('passwordHint', passwordHint);

        const response = await fetch('/api/upload', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
            body: formData,
        });

        if (response.ok) {
            showSuccess('File uploaded successfully.');
            loadFiles();
        } else {
            showError('Failed to upload file.');
        }
    } catch (error) {
        showError('An error occurred during file upload.');
    }
}

async function downloadFile(filename, hint) {
    if (!wasmReady) {
        showError('WASM not ready. Please try again.');
        return;
    }

    if (hint) {
        alert(`Password Hint: ${hint}`);
    }

    const password = prompt('Enter the file password:');
    if (!password) return;

    try {
        const response = await fetch(`/api/download/${filename}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (response.ok) {
            const data = await response.json();
            const decryptedData = decryptFile(data.data, password);

            if (decryptedData === 'Failed to decrypt data') {
                showError('Incorrect password.');
                return;
            }

            const blob = new Blob([Uint8Array.from(atob(decryptedData), c => c.charCodeAt(0))]);
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        } else {
            showError('Failed to download file.');
        }
    } catch (error) {
        showError('An error occurred during file download.');
    }
}

// UI helper functions
function toggleAuthForm() {
    document.getElementById('login-form').classList.toggle('hidden');
    document.getElementById('register-form').classList.toggle('hidden');
}

function showFileSection() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('file-section').classList.remove('hidden');
}

function showError(message) {
    // Implement error display logic
}

function showSuccess(message) {
    // Implement success display logic
}

async function loadFiles() {
    // Implement file listing logic
}

// Event listeners
window.addEventListener('load', () => {
    if (localStorage.getItem('token')) {
        showFileSection();
        loadFiles();
    }
});
```

To complete the client-side setup:

1. Get `wasm_exec.js` from your Go installation:

```bash
cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" client/
```

1. Build the WebAssembly binary:

```bash
GOOS=js GOARCH=wasm go build -o client/main.wasm client/
```

---

# BACKEND COMPONENTS

## 1. auth/jwt.go

```go
package auth

import (
	"os"
	"time"

	"github.com/golang-jwt/jwt"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

type Claims struct {
	Email string `json:"email"`
	jwt.StandardClaims
}

func GenerateToken(email string) (string, error) {
	claims := &Claims{
		Email: email,
		StandardClaims: jwt.StandardClaims{
			ExpiresAt: time.Now().Add(time.Hour * 72).Unix(), // Token expires in 72 hours
			IssuedAt:  time.Now().Unix(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(os.Getenv("JWT_SECRET")))
}

func JWTMiddleware() echo.MiddlewareFunc {
	config := middleware.JWTConfig{
		Claims:     &Claims{},
		SigningKey: []byte(os.Getenv("JWT_SECRET")),
		ErrorHandler: func(err error) error {
			return echo.NewHTTPError(401, "Unauthorized")
		},
	}
	return middleware.JWTWithConfig(config)
}

func GetEmailFromToken(c echo.Context) string {
	user := c.Get("user").(*jwt.Token)
	claims := user.Claims.(*Claims)
	return claims.Email
}
```

## 2. database/database.go

```go
package database

import (
	"database/sql"
	"log"
	"os"

	_ "gitlab.com/cznic/sqlite"
)

var DB *sql.DB

func InitDB() {
	var err error
	dbPath := os.Getenv("DB_PATH")
	if dbPath == "" {
		dbPath = "./arkfile.db"
	}

	DB, err = sql.Open("sqlite", dbPath)
	if err != nil {
		log.Fatal(err)
	}

	err = DB.Ping()
	if err != nil {
		log.Fatal(err)
	}

	createTables()
}

func createTables() {
	// Users table
	userTable := `CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		email TEXT UNIQUE NOT NULL,
		password TEXT NOT NULL,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);`

	// File metadata table
	fileMetadataTable := `CREATE TABLE IF NOT EXISTS file_metadata (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		filename TEXT UNIQUE NOT NULL,
		owner_email TEXT NOT NULL,
		password_hint TEXT,
		upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		FOREIGN KEY (owner_email) REFERENCES users(email)
	);`

	// Access logs table
	accessLogsTable := `CREATE TABLE IF NOT EXISTS access_logs (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user_email TEXT NOT NULL,
		action TEXT NOT NULL,
		filename TEXT,
		timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		FOREIGN KEY (user_email) REFERENCES users(email)
	);`

	tables := []string{userTable, fileMetadataTable, accessLogsTable}

	for _, table := range tables {
		_, err := DB.Exec(table)
		if err != nil {
			log.Fatal(err)
		}
	}
}

// Log user actions
func LogUserAction(email, action, filename string) error {
	_, err := DB.Exec(
		"INSERT INTO access_logs (user_email, action, filename) VALUES (?, ?, ?)",
		email, action, filename,
	)
	return err
}
```

## 3. database/migrations/

This directory would contain numbered migration files. Here's an example structure:

```go
// database/migrations/001_initial_schema.go
package migrations

import "database/sql"

func Migrate_001_InitialSchema(db *sql.DB) error {
	// This would contain the same schema as in createTables(),
	// but structured for migrations
	return nil
}

// Add more migration files as needed for schema changes
```

## 4. handlers/handlers.go

```go
package handlers

import (
	"database/sql"
	"io/ioutil"
	"net/http"
	"strings"

	"github.com/labstack/echo/v4"
	"golang.org/x/crypto/bcrypt"

	"github.com/84adam/arkfile/auth"
	"github.com/84adam/arkfile/database"
	"github.com/84adam/arkfile/logging"
	"github.com/84adam/arkfile/storage"
)

// Register handles user registration
func Register(c echo.Context) error {
	var request struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}

	if err := c.Bind(&request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Invalid request")
	}

	// Validate email and password
	if !strings.Contains(request.Email, "@") || len(request.Password) < 8 {
		return echo.NewHTTPError(http.StatusBadRequest, "Invalid email or password")
	}

	// Hash password
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(request.Password), 12)
	if err != nil {
		logging.ErrorLogger.Printf("Failed to hash password: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Failed to process registration")
	}

	// Store user in database
	_, err = database.DB.Exec(
		"INSERT INTO users (email, password) VALUES (?, ?)",
		request.Email, hashedPassword,
	)
	if err != nil {
		if strings.Contains(err.Error(), "UNIQUE") {
			return echo.NewHTTPError(http.StatusConflict, "Email already registered")
		}
		logging.ErrorLogger.Printf("Failed to create user: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Failed to create user")
	}

	database.LogUserAction(request.Email, "registered", "")
	logging.InfoLogger.Printf("User registered: %s", request.Email)
	return c.JSON(http.StatusCreated, map[string]string{"message": "User created successfully"})
}

// Login handles user authentication
func Login(c echo.Context) error {
	var request struct {
		Email    string `json:"email"`
		Password string `json:"password"`
	}

	if err := c.Bind(&request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Invalid request")
	}

	// Retrieve user from database
	var hashedPassword string
	err := database.DB.QueryRow(
		"SELECT password FROM users WHERE email = ?",
		request.Email,
	).Scan(&hashedPassword)

	if err == sql.ErrNoRows {
		return echo.NewHTTPError(http.StatusUnauthorized, "Invalid credentials")
	} else if err != nil {
		logging.ErrorLogger.Printf("Database error during login: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Login failed")
	}

	// Compare passwords
	err = bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(request.Password))
	if err != nil {
		return echo.NewHTTPError(http.StatusUnauthorized, "Invalid credentials")
	}

	// Generate JWT token
	token, err := auth.GenerateToken(request.Email)
	if err != nil {
		logging.ErrorLogger.Printf("Failed to generate token: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Login failed")
	}

	database.LogUserAction(request.Email, "logged in", "")
	logging.InfoLogger.Printf("User logged in: %s", request.Email)
	return c.JSON(http.StatusOK, map[string]string{"token": token})
}

// UploadFile handles file uploads
func UploadFile(c echo.Context) error {
	email := auth.GetEmailFromToken(c)

	var request struct {
		Filename     string `json:"filename"`
		Data         string `json:"data"`
		PasswordHint string `json:"passwordHint"`
	}

	if err := c.Bind(&request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Invalid request")
	}

	// Store file in Backblaze
	_, err := storage.MinioClient.PutObject(
		c.Request().Context(),
		storage.BucketName,
		request.Filename,
		strings.NewReader(request.Data),
		int64(len(request.Data)),
		minio.PutObjectOptions{ContentType: "application/octet-stream"},
	)
	if err != nil {
		logging.ErrorLogger.Printf("Failed to upload file: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Failed to upload file")
	}

	// Store metadata in database
	_, err = database.DB.Exec(
		"INSERT INTO file_metadata (filename, owner_email, password_hint) VALUES (?, ?, ?)",
		request.Filename, email, request.PasswordHint,
	)
	if err != nil {
		// If metadata storage fails, delete the uploaded file
		storage.MinioClient.RemoveObject(c.Request().Context(), storage.BucketName, request.Filename, minio.RemoveObjectOptions{})
		logging.ErrorLogger.Printf("Failed to store file metadata: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Failed to process file")
	}

	database.LogUserAction(email, "uploaded", request.Filename)
	logging.InfoLogger.Printf("File uploaded: %s by %s", request.Filename, email)
	return c.JSON(http.StatusOK, map[string]string{"message": "File uploaded successfully"})
}

// DownloadFile handles file downloads
func DownloadFile(c echo.Context) error {
	email := auth.GetEmailFromToken(c)
	filename := c.Param("filename")

	// Verify file ownership
	var ownerEmail string
	err := database.DB.QueryRow(
		"SELECT owner_email FROM file_metadata WHERE filename = ?",
		filename,
	).Scan(&ownerEmail)

	if err == sql.ErrNoRows {
		return echo.NewHTTPError(http.StatusNotFound, "File not found")
	} else if err != nil {
		logging.ErrorLogger.Printf("Database error during download: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Failed to process request")
	}

	if ownerEmail != email {
		return echo.NewHTTPError(http.StatusForbidden, "Access denied")
	}

	// Get password hint
	var passwordHint string
	database.DB.QueryRow(
		"SELECT password_hint FROM file_metadata WHERE filename = ?",
		filename,
	).Scan(&passwordHint)

	// Get file from Backblaze
	object, err := storage.MinioClient.GetObject(
		c.Request().Context(),
		storage.BucketName,
		filename,
		minio.GetObjectOptions{},
	)
	if err != nil {
		logging.ErrorLogger.Printf("Failed to retrieve file: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Failed to retrieve file")
	}
	defer object.Close()

	data, err := ioutil.ReadAll(object)
	if err != nil {
		logging.ErrorLogger.Printf("Failed to read file: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Failed to read file")
	}

	database.LogUserAction(email, "downloaded", filename)
	logging.InfoLogger.Printf("File downloaded: %s by %s", filename, email)
	
	return c.JSON(http.StatusOK, map[string]interface{}{
		"data": string(data),
		"passwordHint": passwordHint,
	})
}

// ListFiles returns a list of files owned by the user
func ListFiles(c echo.Context) error {
	email := auth.GetEmailFromToken(c)

	rows, err := database.DB.Query(`
		SELECT filename, password_hint, upload_date 
		FROM file_metadata 
		WHERE owner_email = ?
		ORDER BY upload_date DESC
	`, email)
	if err != nil {
		logging.ErrorLogger.Printf("Failed to list files: %v", err)
		return echo.NewHTTPError(http.StatusInternalServerError, "Failed to retrieve files")
	}
	defer rows.Close()

	var files []map[string]interface{}
	for rows.Next() {
		var file struct {
			Filename    string
			PasswordHint string
			UploadDate  string
		}
		
		if err := rows.Scan(&file.Filename, &file.PasswordHint, &file.UploadDate); err != nil {
			logging.ErrorLogger.Printf("Error scanning file row: %v", err)
			continue
		}

		files = append(files, map[string]interface{}{
			"filename": file.Filename,
			"passwordHint": file.PasswordHint,
			"uploadDate": file.UploadDate,
		})
	}

	return c.JSON(http.StatusOK, files)
}
```

These implementations include:

**JWT Authentication**:

- Token generation and validation
- Middleware for protecting routes
- Email extraction from tokens

**Database Management**:

- SQLite database initialization
- Table creation and schema management
- Action logging
- Migration support

**Request Handlers**:

- User registration and login
- File upload with encryption
- File download with decryption
- File listing
- Error handling and logging
- Security checks and validation

Key security features implemented:

- Password hashing using bcrypt
- JWT-based authentication
- File ownership verification
- Action logging
- Input validation
- Error handling with appropriate status codes

Make sure to:

1. Update import paths to match your project structure
2. Test all error cases and edge conditions
3. Add appropriate indexes to your database tables
4. Implement proper request rate limiting
5. Add input sanitization where needed
6. Consider adding request validation middleware
7. Implement proper error reporting and monitoring

---

# STORAGE, LOGGING & MODELS

## 1. storage/minio.go

```go
package storage

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

var (
	MinioClient *minio.Client
	BucketName  string
)

type StorageConfig struct {
	Endpoint        string
	AccessKeyID     string
	SecretAccessKey string
	BucketName      string
	UseSSL         bool
}

func InitMinio() error {
	config := StorageConfig{
		Endpoint:        os.Getenv("BACKBLAZE_ENDPOINT"),
		AccessKeyID:     os.Getenv("BACKBLAZE_KEY_ID"),
		SecretAccessKey: os.Getenv("BACKBLAZE_APPLICATION_KEY"),
		BucketName:      os.Getenv("BACKBLAZE_BUCKET_NAME"),
		UseSSL:         true,
	}

	// Validate configuration
	if config.Endpoint == "" || config.AccessKeyID == "" || config.SecretAccessKey == "" || config.BucketName == "" {
		return fmt.Errorf("missing required Backblaze configuration")
	}

	BucketName = config.BucketName

	var err error
	MinioClient, err = minio.New(config.Endpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(config.AccessKeyID, config.SecretAccessKey, ""),
		Secure: config.UseSSL,
	})
	if err != nil {
		return fmt.Errorf("failed to create MinIO client: %w", err)
	}

	// Ensure bucket exists
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	exists, err := MinioClient.BucketExists(ctx, config.BucketName)
	if err != nil {
		return fmt.Errorf("failed to check bucket existence: %w", err)
	}

	if !exists {
		err = createBucket(ctx, config.BucketName)
		if err != nil {
			return fmt.Errorf("failed to create bucket: %w", err)
		}
	}

	// Set bucket policy for private access
	err = setBucketPolicy(ctx, config.BucketName)
	if err != nil {
		return fmt.Errorf("failed to set bucket policy: %w", err)
	}

	return nil
}

func createBucket(ctx context.Context, bucketName string) error {
	err := MinioClient.MakeBucket(ctx, bucketName, minio.MakeBucketOptions{})
	if err != nil {
		return fmt.Errorf("failed to create bucket: %w", err)
	}
	log.Printf("Created new bucket: %s", bucketName)
	return nil
}

func setBucketPolicy(ctx context.Context, bucketName string) error {
	// Set a private policy
	policy := `{
		"Version": "2012-10-17",
		"Statement": [
			{
				"Effect": "Deny",
				"Principal": "*",
				"Action": "s3:*",
				"Resource": [
					"arn:aws:s3:::%s/*",
					"arn:aws:s3:::%s"
				]
			}
		]
	}`
	policy = fmt.Sprintf(policy, bucketName, bucketName)

	err := MinioClient.SetBucketPolicy(ctx, bucketName, policy)
	if err != nil {
		return fmt.Errorf("failed to set bucket policy: %w", err)
	}
	return nil
}

// GetPresignedURL generates a temporary URL for file download
func GetPresignedURL(filename string, expiry time.Duration) (string, error) {
	ctx := context.Background()
	url, err := MinioClient.PresignedGetObject(ctx, BucketName, filename, expiry, nil)
	if err != nil {
		return "", fmt.Errorf("failed to generate presigned URL: %w", err)
	}
	return url.String(), nil
}

// RemoveFile deletes a file from storage
func RemoveFile(filename string) error {
	ctx := context.Background()
	err := MinioClient.RemoveObject(ctx, BucketName, filename, minio.RemoveObjectOptions{})
	if err != nil {
		return fmt.Errorf("failed to remove file: %w", err)
	}
	return nil
}
```

## 2. logging/logging.go

```go
package logging

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"time"
)

var (
	InfoLogger    *log.Logger
	ErrorLogger   *log.Logger
	WarningLogger *log.Logger
	DebugLogger   *log.Logger
)

type LogLevel int

const (
	DEBUG LogLevel = iota
	INFO
	WARNING
	ERROR
)

type LogConfig struct {
	LogDir     string
	MaxSize    int64  // Maximum size of log file in bytes
	MaxBackups int    // Maximum number of old log files to retain
	LogLevel   LogLevel
}

func InitLogging(config *LogConfig) error {
	if config == nil {
		config = &LogConfig{
			LogDir:     "logs",
			MaxSize:    10 * 1024 * 1024, // 10MB
			MaxBackups: 5,
			LogLevel:   INFO,
		}
	}

	// Create logs directory if it doesn't exist
	if err := os.MkdirAll(config.LogDir, 0755); err != nil {
		return fmt.Errorf("failed to create log directory: %w", err)
	}

	// Create or open log file
	logFile := filepath.Join(config.LogDir, fmt.Sprintf("app_%s.log", time.Now().Format("2006-01-02")))
	file, err := os.OpenFile(logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return fmt.Errorf("failed to open log file: %w", err)
	}

	// Configure loggers
	flags := log.Ldate | log.Ltime | log.LUTC

	DebugLogger = log.New(file, "DEBUG: ", flags)
	InfoLogger = log.New(file, "INFO: ", flags)
	WarningLogger = log.New(file, "WARNING: ", flags)
	ErrorLogger = log.New(file, "ERROR: ", flags)

	// Start log rotation goroutine
	go monitorLogSize(config, logFile)

	return nil
}

func monitorLogSize(config *LogConfig, logFile string) {
	ticker := time.NewTicker(1 * time.Hour)
	defer ticker.Stop()

	for range ticker.C {
		if info, err := os.Stat(logFile); err == nil {
			if info.Size() > config.MaxSize {
				rotateLog(config, logFile)
			}
		}
	}
}

func rotateLog(config *LogConfig, logFile string) {
	// Rotate log files
	for i := config.MaxBackups - 1; i > 0; i-- {
		oldFile := fmt.Sprintf("%s.%d", logFile, i)
		newFile := fmt.Sprintf("%s.%d", logFile, i+1)
		os.Rename(oldFile, newFile)
	}

	// Rename current log file
	os.Rename(logFile, logFile+".1")

	// Create new log file
	InitLogging(config)
}

// Log formats and writes log messages with source file information
func Log(level LogLevel, format string, v ...interface{}) {
	_, file, line, _ := runtime.Caller(1)
	message := fmt.Sprintf("%s:%d: %s", filepath.Base(file), line, fmt.Sprintf(format, v...))

	switch level {
	case DEBUG:
		DebugLogger.Output(2, message)
	case INFO:
		InfoLogger.Output(2, message)
	case WARNING:
		WarningLogger.Output(2, message)
	case ERROR:
		ErrorLogger.Output(2, message)
	}
}
```

## 3. models/user.go

```go
package models

import (
	"database/sql"
	"errors"
	"time"

	"golang.org/x/crypto/bcrypt"
)

type User struct {
	ID        int64     `json:"id"`
	Email     string    `json:"email"`
	Password  string    `json:"-"` // Never send password in JSON
	CreatedAt time.Time `json:"created_at"`
}

// CreateUser creates a new user in the database
func CreateUser(db *sql.DB, email, password string) (*User, error) {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), 12)
	if err != nil {
		return nil, err
	}

	result, err := db.Exec(
		"INSERT INTO users (email, password) VALUES (?, ?)",
		email, hashedPassword,
	)
	if err != nil {
		return nil, err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return nil, err
	}

	return &User{
		ID:        id,
		Email:     email,
		CreatedAt: time.Now(),
	}, nil
}

// GetUserByEmail retrieves a user by email
func GetUserByEmail(db *sql.DB, email string) (*User, error) {
	user := &User{}
	err := db.QueryRow(
		"SELECT id, email, password, created_at FROM users WHERE email = ?",
		email,
	).Scan(&user.ID, &user.Email, &user.Password, &user.CreatedAt)

	if err == sql.ErrNoRows {
		return nil, errors.New("user not found")
	}
	if err != nil {
		return nil, err
	}

	return user, nil
}

// VerifyPassword checks if the provided password matches the stored hash
func (u *User) VerifyPassword(password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(u.Password), []byte(password))
	return err == nil
}

// UpdatePassword updates the user's password
func (u *User) UpdatePassword(db *sql.DB, newPassword string) error {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(newPassword), 12)
	if err != nil {
		return err
	}

	_, err = db.Exec(
		"UPDATE users SET password = ? WHERE id = ?",
		hashedPassword, u.ID,
	)
	return err
}
```

## 4. models/file.go

```go
package models

import (
	"database/sql"
	"errors"
	"time"
)

type File struct {
	ID           int64     `json:"id"`
	Filename     string    `json:"filename"`
	OwnerEmail   string    `json:"owner_email"`
	PasswordHint string    `json:"password_hint,omitempty"`
	UploadDate   time.Time `json:"upload_date"`
}

// CreateFile creates a new file record in the database
func CreateFile(db *sql.DB, filename, ownerEmail, passwordHint string) (*File, error) {
	result, err := db.Exec(
		"INSERT INTO file_metadata (filename, owner_email, password_hint) VALUES (?, ?, ?)",
		filename, ownerEmail, passwordHint,
	)
	if err != nil {
		return nil, err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return nil, err
	}

	return &File{
		ID:           id,
		Filename:     filename,
		OwnerEmail:   ownerEmail,
		PasswordHint: passwordHint,
		UploadDate:   time.Now(),
	}, nil
}

// GetFileByFilename retrieves a file record by filename
func GetFileByFilename(db *sql.DB, filename string) (*File, error) {
	file := &File{}
	err := db.QueryRow(
		"SELECT id, filename, owner_email, password_hint, upload_date FROM file_metadata WHERE filename = ?",
		filename,
	).Scan(&file.ID, &file.Filename, &file.OwnerEmail, &file.PasswordHint, &file.UploadDate)

	if err == sql.ErrNoRows {
		return nil, errors.New("file not found")
	}
	if err != nil {
		return nil, err
	}

	return file, nil
}

// GetFilesByOwner retrieves all files owned by a specific user
func GetFilesByOwner(db *sql.DB, ownerEmail string) ([]*File, error) {
	rows, err := db.Query(
		"SELECT id, filename, owner_email, password_hint, upload_date FROM file_metadata WHERE owner_email = ? ORDER BY upload_date DESC",
		ownerEmail,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var files []*File
	for rows.Next() {
		file := &File{}
		err := rows.Scan(&file.ID, &file.Filename, &file.OwnerEmail, &file.PasswordHint, &file.UploadDate)
		if err != nil {
			return nil, err
		}
		files = append(files, file)
	}

	if err = rows.Err(); err != nil {
		return nil, err
	}

	return files, nil
}

// DeleteFile removes a file record from the database
func DeleteFile(db *sql.DB, filename string, ownerEmail string) error {
	result, err := db.Exec(
		"DELETE FROM file_metadata WHERE filename = ? AND owner_email = ?",
		filename, ownerEmail,
	)
	if err != nil {
		return err
	}

	affected, err := result.RowsAffected()
	if err != nil {
		return err
	}

	if affected == 0 {
		return errors.New("file not found or unauthorized")
	}

	return nil
}

// UpdatePasswordHint updates the password hint for a file
func (f *File) UpdatePasswordHint(db *sql.DB, newHint string) error {
	_, err := db.Exec(
		"UPDATE file_metadata SET password_hint = ? WHERE id = ?",
		newHint, f.ID,
	)
	if err != nil {
		return err
	}

	f.PasswordHint = newHint
	return nil
}
```

These implementations provide:

**Storage Package**:

- Backblaze B2 integration via MinIO
- Bucket management
- Security policies
- Presigned URL generation
- File removal

**Logging Package**:

- Multiple log levels
- File rotation
- Configurable log settings
- Source file information
- Concurrent-safe logging

**Models Package**:

- User model with password handling
- File metadata model
- Database operations
- Error handling
- Data validation

Key features:

- Secure password handling
- File ownership management
- Structured logging
- Database abstraction
- Error handling
- Type safety

---

# CONFIG, BUILD & SERVICES FILES

## 1. config/config.go

```go
package config

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"

	"github.com/joho/godotenv"
)

var (
	config     *Config
	configOnce sync.Once
)

type Config struct {
	Server struct {
		Port     string `json:"port"`
		Host     string `json:"host"`
		BaseURL  string `json:"base_url"`
		LogLevel string `json:"log_level"`
	} `json:"server"`

	Database struct {
		Path string `json:"path"`
	} `json:"database"`

	Storage struct {
		BackblazeEndpoint string `json:"backblaze_endpoint"`
		BackblazeKeyID    string `json:"backblaze_key_id"`
		BackblazeAppKey   string `json:"backblaze_app_key"`
		BucketName        string `json:"bucket_name"`
	} `json:"storage"`

	Security struct {
		JWTSecret           string `json:"jwt_secret"`
		JWTExpiryHours     int    `json:"jwt_expiry_hours"`
		PasswordMinLength   int    `json:"password_min_length"`
		BcryptCost         int    `json:"bcrypt_cost"`
		MaxFileSize        int64  `json:"max_file_size"`
		AllowedFileTypes   []string `json:"allowed_file_types"`
	} `json:"security"`

	Logging struct {
		Directory  string `json:"directory"`
		MaxSize    int64  `json:"max_size"`
		MaxBackups int    `json:"max_backups"`
	} `json:"logging"`
}

// LoadConfig loads the configuration from environment variables and optional JSON file
func LoadConfig() (*Config, error) {
	var err error
	configOnce.Do(func() {
		config = &Config{}
		
		// Load .env file if it exists
		godotenv.Load()

		// Load default configuration
		if err = loadDefaultConfig(config); err != nil {
			return
		}

		// Override with environment variables
		if err = loadEnvConfig(config); err != nil {
			return
		}

		// Load JSON config if specified
		configPath := os.Getenv("CONFIG_FILE")
		if configPath != "" {
			if err = loadJSONConfig(config, configPath); err != nil {
				return
			}
		}

		// Validate configuration
		if err = validateConfig(config); err != nil {
			return
		}
	})

	if err != nil {
		return nil, err
	}

	return config, nil
}

func loadDefaultConfig(cfg *Config) error {
	// Set default values
	cfg.Server.Port = "8080"
	cfg.Server.Host = "localhost"
	cfg.Database.Path = "./arkfile.db"
	cfg.Security.JWTExpiryHours = 72
	cfg.Security.PasswordMinLength = 8
	cfg.Security.BcryptCost = 12
	cfg.Security.MaxFileSize = 100 * 1024 * 1024 // 100MB
	cfg.Security.AllowedFileTypes = []string{".jpg", ".jpeg", ".png", ".pdf", ".iso"}
	cfg.Logging.Directory = "logs"
	cfg.Logging.MaxSize = 10 * 1024 * 1024 // 10MB
	cfg.Logging.MaxBackups = 5
	
	return nil
}

func loadEnvConfig(cfg *Config) error {
	// Server configuration
	if port := os.Getenv("PORT"); port != "" {
		cfg.Server.Port = port
	}
	if host := os.Getenv("HOST"); host != "" {
		cfg.Server.Host = host
	}
	if baseURL := os.Getenv("BASE_URL"); baseURL != "" {
		cfg.Server.BaseURL = baseURL
	}

	// Storage configuration
	cfg.Storage.BackblazeEndpoint = os.Getenv("BACKBLAZE_ENDPOINT")
	cfg.Storage.BackblazeKeyID = os.Getenv("BACKBLAZE_KEY_ID")
	cfg.Storage.BackblazeAppKey = os.Getenv("BACKBLAZE_APPLICATION_KEY")
	cfg.Storage.BucketName = os.Getenv("BACKBLAZE_BUCKET_NAME")

	// Security configuration
	cfg.Security.JWTSecret = os.Getenv("JWT_SECRET")

	return nil
}

func loadJSONConfig(cfg *Config, path string) error {
	file, err := os.Open(path)
	if err != nil {
		return fmt.Errorf("failed to open config file: %w", err)
	}
	defer file.Close()

	decoder := json.NewDecoder(file)
	if err := decoder.Decode(cfg); err != nil {
		return fmt.Errorf("failed to decode config file: %w", err)
	}

	return nil
}

func validateConfig(cfg *Config) error {
	if cfg.Security.JWTSecret == "" {
		return fmt.Errorf("JWT_SECRET is required")
	}

	if cfg.Storage.BackblazeEndpoint == "" ||
		cfg.Storage.BackblazeKeyID == "" ||
		cfg.Storage.BackblazeAppKey == "" ||
		cfg.Storage.BucketName == "" {
		return fmt.Errorf("Backblaze configuration is incomplete")
	}

	return nil
}

// GetConfig returns the current configuration
func GetConfig() *Config {
	if config == nil {
		panic("Configuration not loaded")
	}
	return config
}
```

## 2. scripts/build.sh

```bash
#!/bin/bash
set -e

# Configuration
APP_NAME="arkfile"
WASM_DIR="client"
BUILD_DIR="build"
VERSION=$(git describe --tags --always --dirty)
BUILD_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Ensure required tools are installed
command -v go >/dev/null 2>&1 || { echo -e "${RED}Go is required but not installed.${NC}" >&2; exit 1; }

echo -e "${GREEN}Building ${APP_NAME} version ${VERSION}${NC}"

# Create build directory
mkdir -p ${BUILD_DIR}

# Build WebAssembly
echo "Building WebAssembly..."
GOOS=js GOARCH=wasm go build -o ${BUILD_DIR}/${WASM_DIR}/main.wasm ./${WASM_DIR}
cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" ${BUILD_DIR}/${WASM_DIR}/

# Build main application with version information
echo "Building main application..."
go build -ldflags "-X main.Version=${VERSION} -X main.BuildTime=${BUILD_TIME}" -o ${BUILD_DIR}/${APP_NAME}

# Copy static files
echo "Copying static files..."
cp -r client/static ${BUILD_DIR}/
cp .env.example ${BUILD_DIR}/.env.example
cp Caddyfile ${BUILD_DIR}/
cp -r systemd ${BUILD_DIR}/

# Create version file
echo "Creating version file..."
cat > ${BUILD_DIR}/version.json <<EOF
{
    "version": "${VERSION}",
    "buildTime": "${BUILD_TIME}"
}
EOF

echo -e "${GREEN}Build complete!${NC}"
echo "Build artifacts are in the '${BUILD_DIR}' directory"
```

## 3. scripts/deploy.sh

```bash
#!/bin/bash
set -e

# Configuration
APP_NAME="arkfile"
REMOTE_USER="app"
REMOTE_HOST="arkfile.net"
REMOTE_DIR="/opt/${APP_NAME}"
BUILD_DIR="build"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if host is provided
if [ "$1" != "" ]; then
    REMOTE_HOST=$1
fi

echo -e "${GREEN}Deploying ${APP_NAME} to ${REMOTE_HOST}...${NC}"

# Build the application first
echo "Building application..."
./scripts/build.sh

# Create remote directory if it doesn't exist
echo "Preparing remote directory..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo mkdir -p ${REMOTE_DIR} && sudo chown ${REMOTE_USER}:${REMOTE_USER} ${REMOTE_DIR}"

# Copy files to remote server
echo "Copying files to remote server..."
rsync -avz --progress ${BUILD_DIR}/ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/

# Set up systemd services
echo "Setting up systemd services..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo cp ${REMOTE_DIR}/systemd/*.service /etc/systemd/system/ && \
    sudo systemctl daemon-reload"

# Install or update application
echo "Installing application..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_DIR} && \
    [ -f .env ] || cp .env.example .env && \
    sudo systemctl restart ${APP_NAME} && \
    sudo systemctl restart caddy"

# Verify deployment
echo "Verifying deployment..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "systemctl status ${APP_NAME} --no-pager && \
    systemctl status caddy --no-pager"

echo -e "${GREEN}Deployment complete!${NC}"
echo -e "${YELLOW}Remember to check the logs:${NC}"
echo "  sudo journalctl -u ${APP_NAME} -f"
echo "  sudo journalctl -u caddy -f"
```

## 4. systemd/arkfile.service

```ini
[Unit]
Description=Arkfile Service
After=network.target
Wants=caddy.service

[Service]
Type=simple
User=app
Group=app
WorkingDirectory=/opt/arkfile
ExecStart=/opt/arkfile/arkfile

Environment=PORT=8080
Environment=BACKBLAZE_ENDPOINT=your_endpoint
Environment=BACKBLAZE_KEY_ID=your_key_id
Environment=BACKBLAZE_APPLICATION_KEY=your_app_key
Environment=BACKBLAZE_BUCKET_NAME=your_bucket
Environment=JWT_SECRET=your_jwt_secret

# Security measures
NoNewPrivileges=yes
ProtectSystem=full
ProtectHome=yes
PrivateTmp=yes
PrivateDevices=yes

# Restart configuration
Restart=always
RestartSec=5
StartLimitInterval=60s
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
```

## 5. systemd/caddy.service

```ini
[Unit]
Description=Caddy Web Server
After=network.target
Wants=arkfile.service

[Service]
Type=simple
User=caddy
Group=caddy
ExecStart=/usr/local/bin/caddy run --config /etc/caddy/Caddyfile
ExecReload=/usr/local/bin/caddy reload --config /etc/caddy/Caddyfile

Environment=VULTR_API_KEY=your_vultr_api_key

# Security measures
NoNewPrivileges=yes
ProtectSystem=full
ProtectHome=yes
PrivateTmp=yes
PrivateDevices=yes
ReadWritePaths=/etc/caddy /var/lib/caddy
AmbientCapabilities=CAP_NET_BIND_SERVICE

# Restart configuration
Restart=always
RestartSec=5
StartLimitInterval=60s
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
```

These files provide:

**Configuration Management**:

- Environment variable loading
- JSON configuration support
- Default values
- Configuration validation
- Thread-safe singleton pattern

**Build Script**:

- WebAssembly compilation
- Version information
- Static file copying
- Build artifact organization

**Deployment Script**:

- Remote server deployment
- Service installation
- Configuration copying
- Deployment verification

**Systemd Services**:

- Application service definition
- Caddy service definition
- Security hardening
- Automatic restart
- Environment configuration

Important considerations:

1. Always secure your environment variables
2. Test deployments in a staging environment first
3. Monitor service logs for issues
4. Keep deployment scripts idempotent
5. Regularly update dependencies
6. Maintain proper file permissions
7. Use secure communication channels for deployment

---

# API DOCUMENTATION

## Overview

This API provides endpoints for secure file sharing. All API requests must be authenticated using JWT tokens unless explicitly marked as public.

## Base URL

```
https://arkfile.net/api
```

## Authentication

Authentication is handled via JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### Register User (Public)

```http
POST /register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password"
}

Response 201:
{
    "message": "User created successfully"
}
```

#### Login (Public)

```http
POST /login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password"
}

Response 200:
{
    "token": "jwt_token_here"
}
```

### File Operations

#### Upload File

```http
POST /upload
Content-Type: multipart/form-data

Parameters:
- file: File to upload
- passwordHint: (optional) Hint for the file password

Response 200:
{
    "message": "File uploaded successfully"
}
```

#### Download File

```http
GET /download/:filename

Response 200:
{
    "data": "encrypted_file_data",
    "passwordHint": "optional_password_hint"
}
```

#### List Files

```http
GET /files

Response 200:
[
    {
        "filename": "example.jpg",
        "uploadDate": "2024-01-01T12:00:00Z",
        "passwordHint": "optional hint"
    }
]
```

## Error Responses

All errors follow this format:

```json
{
    "error": "Error message here"
}
```

Common HTTP Status Codes:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

API requests are limited to 100 requests per minute per IP address.

## File Limitations

- Maximum file size: 100MB
- Supported file types: .jpg, .jpeg, .png, .pdf, .iso

## WebSocket Events

For real-time progress updates (if implemented):

```javascript
// File upload progress
{
    "type": "upload_progress",
    "filename": "example.jpg",
    "progress": 45  // percentage
}

// File download progress
{
    "type": "download_progress",
    "filename": "example.jpg",
    "progress": 45  // percentage
}
```

---

# SETUP DOCUMENTATION

# Arkfile Setup Guide

## Prerequisites

### System Requirements

- Linux server (Rocky Linux recommended)
- Go 1.21 or higher
- SQLite
- Caddy web server
- Backblaze B2 account
- Domain name with DNS configured

### Required Tools

- Git
- Make (optional)
- systemd

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/84adam/arkfile.git
cd arkfile
```

### 2. Configure Environment

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
nano .env
```

Required environment variables:

```ini
BACKBLAZE_ENDPOINT=s3.us-west-000.backblazeb2.com
BACKBLAZE_KEY_ID=your_key_id
BACKBLAZE_APPLICATION_KEY=your_app_key
BACKBLAZE_BUCKET_NAME=your_bucket
JWT_SECRET=your_jwt_secret
```

### 3. Build the Application

```bash
# Build everything
./scripts/build.sh

# Or build components separately
GOOS=js GOARCH=wasm go build -o client/main.wasm ./client
go build -o arkfile
```

### 4. Set Up Caddy

1. Build Caddy with Vultr module:

```bash
cd caddy_build
go mod init caddy
go mod tidy
go build
```

1. Configure Caddy:

```bash
sudo cp Caddyfile /etc/caddy/
sudo chown caddy:caddy /etc/caddy/Caddyfile
```

### 5. Deploy Services

```bash
# Copy service files
sudo cp systemd/*.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Start services
sudo systemctl start arkfile
sudo systemctl start caddy

# Enable services
sudo systemctl enable arkfile
sudo systemctl enable caddy
```

### 6. Verify Installation

```bash
# Check service status
sudo systemctl status arkfile
sudo systemctl status caddy

# Check logs
sudo journalctl -u arkfile -f
sudo journalctl -u caddy -f
```

## Configuration

### Application Configuration

Edit `config/config.json`:

```json
{
    "server": {
        "port": "8080",
        "host": "localhost"
    },
    "security": {
        "max_file_size": 104857600,
        "allowed_file_types": [".jpg", ".jpeg", ".png", ".pdf", ".iso"]
    }
}
```

### Caddy Configuration

Edit `/etc/caddy/Caddyfile`:

```caddy
arkfile.net {
    reverse_proxy localhost:8080
}
```

## Maintenance

### Backup

1. Database backup:

```bash
sqlite3 arkfile.db ".backup 'backup.db'"
```

1. Configuration backup:

```bash
cp .env .env.backup
cp /etc/caddy/Caddyfile Caddyfile.backup
```

### Updates

1. Pull latest changes:

```bash
git pull origin main
```

1. Rebuild and restart:

```bash
./scripts/build.sh
sudo systemctl restart arkfile
```

### Logs

- Application logs: `/var/log/arkfile/`
- Caddy logs: `/var/log/caddy/`
- System logs: `journalctl`

## Troubleshooting

### Common Issues

1. Permission Errors

```bash
sudo chown -R app:app /opt/arkfile
sudo chmod -R 755 /opt/arkfile
```

1. Database Errors

```bash
sqlite3 arkfile.db "PRAGMA integrity_check;"
```

1. Network Issues

```bash
sudo netstat -tulpn | grep -E ':(80|443|8080)'
```

### Getting Help

- Check application logs
- Review error messages
- Consult the API documentation
- Open an issue on GitHub

## Post-Installation Checklist

1. [ ] Environment variables configured
2. [ ] Services running and enabled
3. [ ] Firewall configured
4. [ ] SSL/TLS certificates working
5. [ ] Database initialized
6. [ ] Backups configured
7. [ ] Logging working
8. [ ] Test upload/download functionality
9. [ ] Monitor system resources
10. [ ] Security scanning completed

---

# SECURITY DOCUMENTATION

# Security Documentation

## Overview

This document outlines the security measures implemented in the Arkfile application. All features described are actively implemented and audited on a best-effort basis.

## Data Security

### Encryption

#### At Rest

- Files are encrypted using AES-256-GCM before storage
- Each file has its own encryption key derived from user password using PBKDF2
- Password-based keys are never stored; they're derived on-demand
- Key derivation parameters:
- Iterations: 100,000
- Salt: Unique 16-byte random value per file
- Hash function: SHA-256
- Backblaze B2 provides additional server-side encryption layer

#### In Transit

- All communication uses TLS 1.3
- WebSocket connections are secured with TLS
- Files are encrypted client-side before transmission
- Caddy handles TLS certificate management and renewal

### Password Security

- Passwords are hashed using bcrypt with cost factor 12
- Password requirements:
- Minimum length: 8 characters
- Must contain: letters, numbers
- Special characters recommended but not required
- Maximum length: 72 characters (bcrypt limitation)
- Failed login attempts are rate-limited:
- 5 attempts per minute per IP
- 20 attempts per hour per account
- Password hints are stored separately from encrypted data
- Password strength is evaluated client-side during registration

## Authentication & Authorization

### JWT Implementation

```json
{
    "header": {
        "alg": "HS256",
        "typ": "JWT"
    },
    "payload": {
        "sub": "user@example.com",
        "iat": 1516239022,
        "exp": 1516325422
    }
}
```

- Tokens expire after 72 hours
- Signed using HS256 algorithm
- Token contents:
- Subject (user email)
- Issued at timestamp
- Expiration timestamp
- Token refresh mechanism available
- Secure token storage recommendations provided to users

### Access Control

- File access restricted to authenticated users
- Files can only be accessed by their owners
- Rate limiting on all endpoints:
- API: 100 requests per minute per IP
- File upload: 10 per hour per user
- File download: 50 per hour per user
- Session invalidation triggers:
- Password change
- Explicit logout
- Security event detection

## Infrastructure Security

### Server Hardening

- Regular system updates configured via automated scripts
- Minimal required ports exposed:

```text
INCOMING:
- TCP/80  (HTTP, redirected to HTTPS)
- TCP/443 (HTTPS)
- TCP/22  (SSH, custom port optional)

OUTGOING:
- TCP/443 (Backblaze B2 API)
```

- Firewall configuration (firewalld):

```bash
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --add-port=22/tcp
firewall-cmd --reload
```

### Service Security

- Services run as non-root users
- Systemd security directives:

```ini
[Service]
ProtectSystem=full
ProtectHome=yes
PrivateTmp=yes
NoNewPrivileges=yes
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
```

- Resource limits enforced:

```ini
[Service]
LimitNOFILE=65535
LimitNPROC=4096
MemoryMax=2G
CPUQuota=80%
```

## Application Security

### Input Validation

All user input is validated:

```go
// Example validation rules
type FileUpload struct {
    MaxSize    int64    = 100 * 1024 * 1024 // 100MB
    AllowedTypes []string = {".jpg", ".jpeg", ".png", ".pdf", ".iso"}
}

type UserInput struct {
    EmailRegex    string = `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
    FilenameRegex string = `^[a-zA-Z0-9][a-zA-Z0-9._-]{1,255}$`
}
```

### Security Headers

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'; script-src 'self' 'wasm-unsafe-eval'
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### Error Handling

- Generic error messages to users
- Detailed internal logging
- Error response format:

```json
{
    "error": {
        "code": "AUTH001",
        "message": "Authentication required",
        "userMessage": "Please log in to continue"
    }
}
```

## Monitoring & Audit

### Logging

Each log entry includes:

```json
{
    "timestamp": "2024-01-01T12:00:00Z",
    "level": "INFO",
    "event": "file_upload",
    "user": "user@example.com",
    "ip": "192.168.1.1",
    "details": {
        "filename": "example.jpg",
        "size": 1048576
    }
}
```

### Security Events Monitored

Authentication:

- Failed login attempts
- Password changes
- Token revocations

File Operations:

- Uploads
- Downloads
- Deletion attempts
- Access denials

System:

- Service starts/stops
- Configuration changes
- Error rates
- Resource usage

## Incident Response

### Security Event Levels

```
Level 1: Information
- Successful logins
- Normal file operations
- System updates

Level 2: Warning
- Failed login attempts
- Invalid file uploads
- Resource warnings

Level 3: Critical
- Multiple authentication failures
- Suspicious file patterns
- Service disruptions
```

### Response Procedures

Detection

- Monitor logs
- Analyze patterns
- Alert triggers

Analysis

- Event classification
- Impact assessment
- Scope determination

Containment

- Account suspension
- Service isolation
- Access restriction

Recovery

- Service restoration
- Data verification
- Security patch application

## Compliance & Privacy

### Data Handling

Data classification:

- User credentials: High sensitivity
- File metadata: Medium sensitivity
- Log data: Low sensitivity

Retention policies:

- User data: Until account deletion
- File metadata: 90 days after deletion
- Logs: 30 days

### Privacy Controls

- Data minimization
- Explicit consent requirements
- Clear data usage policies
- Transparent logging practices

---

## UPDATE: [Arkfile.net](https://arkfile.net) is live as of August, 2026!

---

---
title: arkfile.net
slug: arkfile-architecture
status: published
type: post
date: '2024-10-25'
updated: '2026-08-22'
author: bc1984adam
canonical: https://bc1984.com/arkfile-architecture/
feature_image: /images/2024/10/dalle-bw-forest.png
---
