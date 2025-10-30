🛡️ FastAPI DevSecOps Project:

This repository demonstrates a complete DevSecOps pipeline — integrating secure coding, automated security testing, continuous integration, continuous delivery, and secure deployment using GitHub Actions, Docker, Bandit (SAST), and OWASP ZAP (DAST).
It’s designed to help you implement security-by-design in every stage of your SDLC (Software Development Lifecycle).

🚀 Table of Contents:
Introduction to DevSecOps
DevSecOps Lifecycle
Security Layers in This Project
Pipeline Flow Overview
Tools & Technologies
Security Scanning Types
Local Environment Setup
CI/CD Workflow Explanation
Security Gate Logic
Secrets & Credential Management
Additional DevSecOps Enhancements

🧩 Introduction to DevSecOps:
DevSecOps = Development + Security + Operations.
It’s the practice of integrating security controls and automation throughout the CI/CD pipeline.
Instead of adding security after deployment, DevSecOps brings it into every stage — from code commit to runtime.

Traditional DevOps:
Security is a separate step
Manual review
Vulnerabilities found late
Developers not security-aware

DevSecOps:
Security is integrated
Automated scanning
Vulnerabilities found early
Security built into development

🔄 DevSecOps Lifecycle:
Phase	Purpose	Example Tools
Plan	Define security & compliance goals	Jira, Confluence
Code	Use secure coding standards	Bandit, ESLint, Trivy
Build	Scan dependencies, containers	Grype, Snyk, Trivy
Test	Run SAST, DAST, SCA	Bandit, ZAP, pip-audit
Release	Apply approval gates	GitHub Environments
Deploy	Harden infrastructure	Kubernetes, Terraform
Monitor	Runtime security & alerts	Prometheus, Falco, ELK
Respond	Incident handling & patching	PagerDuty, SIEM


🧱 Security Layers in This Project:
Security Area	Implementation	Tool
Static Code Analysis (SAST)	Detect insecure code patterns	Bandit
Dynamic App Scan (DAST)	Scan running app for exploits	OWASP ZAP
Container Image Scan	Find vulnerabilities in Docker image	Trivy
Secrets Scanning	Detect hardcoded secrets	Gitleaks
Dependency Audit (SCA)	Check library vulnerabilities	pip-audit
Access Control	Secure GitHub Actions secrets	GitHub Environments
Runtime Monitoring	Detect container intrusion	Falco (optional)

🔁 Pipeline Flow Overview
End-to-End Workflow
Developer Commit → GitHub Actions Trigger
  ├── 1️⃣ Lint + Test
  ├── 2️⃣ SAST (Bandit)
  ├── 3️⃣ Build Docker Image
  ├── 4️⃣ Image Scan (Trivy)
  ├── 5️⃣ Run Container
  ├── 6️⃣ DAST (ZAP)
  ├── 7️⃣ Deploy to Staging
  ├── 8️⃣ Manual Approval
  └── 9️⃣ Deploy to Production

Environments:
Environment	Purpose	Deployment
Development	Local testing	Docker Compose
Staging	DAST scan, QA	GitHub Actions
Production	Live traffic	Manual approval (GitHub Environments)

🧰 Tools & Technologies:
Category	Tool	Purpose
CI/CD	GitHub Actions	Automated build, test, deploy
Application	FastAPI	Python Web Framework
Containerization	Docker, Docker Compose	App packaging & deployment
Static Security	Bandit	SAST for Python
Dynamic Security	OWASP ZAP	DAST runtime testing
Dependency Audit	pip-audit	Library CVE detection
Image Vulnerability	Trivy	Container CVE scanning
Secrets Detection	Gitleaks	Detect leaked credentials
Monitoring	Prometheus + Grafana	Runtime metrics
Logging	ELK Stack	Centralized logs
Kubernetes	kubectl, manifests	Cluster deployment

🧪 Security Scanning Types:
Type	Description	Tools
SAST	Static code scan for insecure coding	Bandit
DAST	Black-box test on running app	OWASP ZAP
SCA	Dependency vulnerability check	pip-audit
Container Scan	CVE scan in Docker image	Trivy
Secrets Scan	Detect API keys/passwords	Gitleaks
IaC Scan	Check Terraform/K8s YAMLs	Checkov, Kics

🖥️ Local Environment Setup:
# Clone repo
git clone https://github.com/nahidmozahid/fastapi-devsecops.git
cd fastapi-devsecops

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install bandit pip-audit pytest

# Run app
uvicorn app.main:app --reload

# SAST scan
bandit -r app -f html -o reports/bandit.html

# Dependency audit
pip-audit

# Docker build
docker compose up --build -d

# DAST scan (OWASP ZAP)
docker run --rm --network host -v $(pwd):/zap/wrk/:rw owasp/zap2docker-stable \
  zap-baseline.py -t http://localhost:8000 -r zap-report.html

⚙️ CI/CD Workflow Explanation:
The .github/workflows/security-pipeline.yml runs automatically on every push or PR to main.

Job	Description	Tool:
build_and_sast	Build app, run unit tests & Bandit	Bandit
dependency_audit	Scan dependencies	pip-audit
container_scan	Scan Docker image for CVEs	Trivy
dast_scan	Run app & perform OWASP ZAP DAST test	ZAP
deploy_staging	Deploy to staging server/cluster	Docker or K8s
deploy_production	Deploy to production (manual gate)	kubectl

Example Bandit + ZAP workflow:
- name: Run SAST (Bandit)
  run: bandit -r app -f html -o bandit-report.html || true
- name: Run DAST (OWASP ZAP)
  uses: zaproxy/action-full-scan@v0.6.0
  with:
    target: "http://localhost:8000"
    cmd_options: "-r zap-report.html"
🧱 Security Gate Logic
CI/CD Pipeline will:
✅ Pass → if no critical vulnerabilities found
❌ Fail → if Bandit/ZAP/Trivy detect high severity CVEs

Example condition:
if: success() && !contains(steps.bandit.outputs.severity, 'HIGH')



